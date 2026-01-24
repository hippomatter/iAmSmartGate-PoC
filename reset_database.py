#!/usr/bin/env python3
"""
Reset Database Script for iAmSmartGate
Deletes the existing database and creates a fresh one with updated schema
"""
import os
import sys

def reset_database():
    """Reset the database"""
    print("=" * 60)
    print("iAmSmartGate - Reset Database")
    print("=" * 60)
    print()
    
    # Get database path
    db_path = os.path.join('backend', 'instance', 'iamsmartgate.db')
    
    # Check if database exists
    if os.path.exists(db_path):
        print(f"⚠️  Found existing database: {db_path}")
        print("⚠️  WARNING: This will delete all existing data!")
        print()
        
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Operation cancelled")
            return
        
        # Delete database
        try:
            os.remove(db_path)
            print(f"✅ Database deleted: {db_path}")
        except Exception as e:
            print(f"❌ Error deleting database: {e}")
            return
    else:
        print(f"ℹ️  No existing database found at: {db_path}")
    
    print()
    print("✅ Database reset complete!")
    print()
    print("📝 The new database will be created automatically when you run:")
    print("   • python backend/app.py")
    print("   • Or run start.bat")
    print()
    print("🔧 New schema includes:")
    print("   • signature_method field in Pass table (default: FALCON-128)")
    print("   • System state for QR signature method configuration")
    print()

if __name__ == '__main__':
    try:
        reset_database()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
