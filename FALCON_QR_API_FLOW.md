# Falcon QR Signing API Flow

This document describes the HTTP calls and UI flow used in `public/appQsQRSig.html` to produce a Falcon-signed QR code for an email/message.
 
## Cryptography
- Signing mechanism: `ckm-icc-shake256-mm-falcon` (IronCAP Falcon variant).
- HSM slots: private `1654338351` with ID `0128600B`; public `602869399` with ID `0000600B` (UI defaults).
- Signature is fetched as a hex string and padded to fit QR capacity (Version 26, EC level L).

## Service endpoints
All endpoints are Cloud Run/Firebase HTTPS functions returning JSON.

- Show keyring: `POST https://showkey-kez6dpnjlq-uc.a.run.app`
  - Body: `slot`, `pin`
  - Returns `console_log` with keyring details.
- Retrieve & read public key:
  - `POST https://retrievepubkey-kez6dpnjlq-uc.a.run.app` with `slot`, `pin`, `id`, `mechanism`
  - Then `GET https://readpubkey-kez6dpnjlq-uc.a.run.app` → `content` (PEM/hex) and `console_log`.
- Persist message: `POST https://writemessage-kez6dpnjlq-uc.a.run.app`
  - Body: `message` (UI strips whitespace and text outside ``` fences).
- Hash message: `POST https://hashmessage-kez6dpnjlq-uc.a.run.app`
  - Returns `binary_content` (hash) → stored as `hashContent`.
- Sign hash: `POST https://signmessage-kez6dpnjlq-uc.a.run.app`
  - Body: `slot`, `pin`, `id`, `mechanism`
  - On success, signature is read separately.
- Read signature: `GET https://readsignature-kez6dpnjlq-uc.a.run.app`
  - Returns `content` (signature hex) → stored as `signatureData`.
- Verify signature (optional pre-QR sanity check):
  - `POST https://verifysignature-kez6dpnjlq-uc.a.run.app` with `slot`, `pin`, `id`, `mechanism`
  - Returns `console_log` describing verification result.

### Endpoint usage snippets (from appQsQRSig.html)
These match the live UI calls so you can replay them easily.

- Show keyring
  ```javascript
  $.ajax({
    url: "https://showkey-kez6dpnjlq-uc.a.run.app",
    method: "POST",
    data: { slot: $("#slot").val(), pin: $("#pin").val() },
    dataType: "json"
  })
  ```
- Retrieve then read public key
  ```javascript
  $.ajax({
    url: "https://retrievepubkey-kez6dpnjlq-uc.a.run.app",
    method: "POST",
    data: {
      slot: $("#slot").val(),
      pin: $("#pin").val(),
      id: $("#id").val(),
      mechanism: $("#quantumSafeKey").text()
    },
    dataType: "json",
    success: () => $.ajax({ url: "https://readpubkey-kez6dpnjlq-uc.a.run.app", method: "GET", dataType: "json" })
  })
  ```
- Persist message (UI first trims to text between ``` fences and strips whitespace)
  ```javascript
  $.ajax({
    url: "https://writemessage-kez6dpnjlq-uc.a.run.app",
    method: "POST",
    data: { message: serializedText },
    dataType: "json"
  })
  ```
- Hash message
  ```javascript
  $.ajax({
    url: "https://hashmessage-kez6dpnjlq-uc.a.run.app",
    method: "POST",
    data: {},
    dataType: "json"
  })
  ```
- Sign hash
  ```javascript
  $.ajax({
    url: "https://signmessage-kez6dpnjlq-uc.a.run.app",
    method: "POST",
    data: {
      slot: $("#slot").val(),
      pin: $("#pin").val(),
      id: $("#id").val(),
      mechanism: $("#quantumSafeKey").text()
    },
    dataType: "json"
  })
  ```
- Read signature
  ```javascript
  $.ajax({ url: "https://readsignature-kez6dpnjlq-uc.a.run.app", method: "GET", dataType: "json" })
  ```
- Verify signature
  ```javascript
  $.ajax({
    url: "https://verifysignature-kez6dpnjlq-uc.a.run.app",
    method: "POST",
    data: {
      slot: $("#slot").val(),
      pin: $("#pin").val(),
      id: $("#id").val(),
      mechanism: $("#quantumSafeKey").text()
    },
    dataType: "json"
  })
  ```

## End-to-end flow to produce the QR
1. **Configure keys**: enter `pin`; optionally call *Show keyring* to confirm HSM slot; call *Retrieve pub key* (triggers read) to cache public key.
2. **Enter message**: paste plaintext, click *INPUT TEXT* → UI serializes between ``` fences and `POST`s to *Persist message*.
3. **Hash content**: click *HASH CONTENT* → `POST` *Hash message*; capture `hashContent` for QR URL query parameter.
4. **Sign hash**: click *Sign Content Hash* → `POST` *Sign hash*; then `GET` *Read signature* to populate `signatureData` (hex Falcon signature).
5. **(Optional) Verify**: click *Verify Quantum Signature* → `POST` *Verify signature*; review `console_log`.
6. **Generate QR**:
   - Build verifier URL: `https://quantumsign-verifier.web.app?slot=602869399&id=0000600B&hash=<hashContent>`; pad with `?padding=` to 1,273 chars for QR capacity.
   - Pad signature hex to 1,852 characters (Version 26 alphanumeric limit).
   - Create two QRs (URL forced to Version 26, EC `L`, width 1250 px); then combine side-by-side into one PNG.
   - Render combined PNG into the UI and show a credential summary (mechanism, URL sans padding, slots, hash, lengths).
7. **Save**: user can download the combined QR as PNG; signature can also be saved as a raw blob (optional UI hook).

## Minimal cURL examples
```bash
# Sign (after hash is stored server-side)
curl -X POST \
  -d "slot=1654338351" -d "pin=<PIN>" -d "id=0128600B" \
  -d "mechanism=ckm-icc-shake256-mm-falcon" \
  https://signmessage-kez6dpnjlq-uc.a.run.app

# Fetch signature hex
curl https://readsignature-kez6dpnjlq-uc.a.run.app

# Hash current stored message
curl -X POST https://hashmessage-kez6dpnjlq-uc.a.run.app
```

## Notes
- The UI pads both URL and signature to fixed lengths to avoid QR resizing; padding is removed from the displayed URL when summarizing.
- The verifier site receives `slot`, `id`, and `hash` via the left QR; the right QR carries the Falcon signature hex.
- Keep the PIN out of the URL or QR; only the signer uses it when calling the signing endpoint.
