"""
Security middleware for iAmSmartGate
"""
from flask import request, jsonify
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def require_https():
    """
    Decorator to enforce HTTPS for specific endpoints.
    In production, requires requests to be made over secure HTTPS connection.
    In development (localhost), allows HTTP for testing.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if running on localhost (development mode)
            is_localhost = request.host.startswith('localhost') or request.host.startswith('127.0.0.1')
            
            # In production, enforce HTTPS
            if not is_localhost and not request.is_secure:
                logger.warning(f"[SECURITY] Non-HTTPS request blocked from {request.remote_addr} to {request.path}")
                return jsonify({
                    'error': 'HTTPS required',
                    'message': 'This endpoint requires a secure HTTPS connection'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_https_for_gates():
    """
    Decorator specifically for gate endpoints.
    Enforces HTTPS and logs security events.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if running on localhost (development mode)
            is_localhost = request.host.startswith('localhost') or request.host.startswith('127.0.0.1')
            
            # In production, enforce HTTPS for gate operations
            if not is_localhost:
                if not request.is_secure:
                    logger.error(f"[SECURITY] Gate API called over insecure connection from {request.remote_addr}")
                    return jsonify({
                        'error': 'HTTPS required for gate operations',
                        'message': 'Gate API endpoints must use secure HTTPS connection'
                    }), 403
                
                # Log successful HTTPS gate access
                logger.info(f"[SECURITY] Secure gate API access from {request.remote_addr} to {request.path}")
            else:
                logger.debug(f"[DEV] Localhost gate API access to {request.path} (HTTP allowed)")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
