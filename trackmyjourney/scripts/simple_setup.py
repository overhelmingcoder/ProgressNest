#!/usr/bin/env python
"""
Simple setup script for TrackMyJourney
This script will set up the entire Django project
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(e.stderr)
        return False

def main():
    print("🚀 TrackMyJourney Setup")
    print("=" * 40)
    
    # Install requirements
    print("📦 Installing requirements...")
    run_command("pip install Django==4.2.7 Pillow==10.1.0 django-crispy-forms==2.1 crispy-bootstrap5==0.7", "Installing packages")
    
    # Remove old database
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("🗑️  Removed old database")
    
    # Create migrations
    print("\n📝 Creating migrations...")
    apps = ['accounts', 'goals', 'achievements', 'blog', 'resources', 'books', 'groups', 'community']
    
    for app in apps:
        migrations_dir = f"{app}/migrations"
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(migrations_dir, file))
    
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Applying migrations")
    
    # Create superuser
    print("\n👤 Creating superuser...")
    run_command('python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin123\') if not User.objects.filter(username=\'admin\').exists() else None"', "Creating superuser")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin: http://127.0.0.1:8000/admin")
    print("4. Login: admin / admin123")
    print("\n✨ Your website is ready!")

if __name__ == "__main__":
    main()
