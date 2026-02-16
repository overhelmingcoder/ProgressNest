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

def setup_database():
    print("🚀 Setting up TrackMyJourney database...")
    
    # Make migrations
    print("📝 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Apply migrations
    print("🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    print("📁 Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("✅ Database setup complete!")
    print("🔑 Now create a superuser with: python manage.py createsuperuser")

if __name__ == '__main__':
    setup_database()
