#!/usr/bin/env python
"""
Quick setup script to get TrackMyJourney running immediately
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 TrackMyJourney Quick Setup")
    print("=" * 40)
    
    # Install requirements
    run_command("pip install Django==4.2.7 Pillow==10.1.0 django-crispy-forms==2.1 crispy-bootstrap5==0.7", "Installing packages")
    
    # Remove old database
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("🗑️ Removed old database")
    
    # Create migrations and migrate
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Applying migrations")
    
    # Create superuser
    run_command('python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin123\') if not User.objects.filter(username=\'admin\').exists() else print(\'Admin exists\')"', "Creating superuser")
    
    # Create directories
    os.makedirs('media/avatars', exist_ok=True)
    os.makedirs('staticfiles', exist_ok=True)
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Login: admin / admin123")
    print("\n✨ Your website is ready!")

if __name__ == "__main__":
    main()
