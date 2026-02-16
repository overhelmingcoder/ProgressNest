#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')
django.setup()

from django.core.management import execute_from_command_line

def run_migrations():
    """Run migrations to fix the model issues"""
    print("🔧 Creating and applying migrations...")
    
    try:
        # Make migrations for all apps
        print("📝 Making migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Apply migrations
        print("⚡ Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting model fixes and migrations...")
    success = run_migrations()
    
    if success:
        print("\n✅ All model issues have been fixed!")
        print("You can now run: python manage.py runserver")
    else:
        print("\n❌ There were issues with the migration process.")
        print("Please check the error messages above.")
