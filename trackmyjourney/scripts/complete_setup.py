#!/usr/bin/env python
import os
import sys
import django
import subprocess
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(e.stderr)
        return False

def setup_django():
    """Setup Django project"""
    print("🚀 Starting TrackMyJourney setup...")
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("⚠️  Requirements installation failed. Continuing anyway...")
    
    # Remove old migration files
    print("\n🧹 Cleaning old migration files...")
    apps = ['accounts', 'goals', 'achievements', 'blog', 'resources', 'books', 'groups', 'community']
    
    for app in apps:
        migrations_dir = project_dir / app / 'migrations'
        if migrations_dir.exists():
            for file in migrations_dir.glob('*.py'):
                if file.name != '__init__.py':
                    file.unlink()
                    print(f"   Removed {file}")
    
    # Remove database
    db_file = project_dir / 'db.sqlite3'
    if db_file.exists():
        db_file.unlink()
        print("   Removed old database")
    
    # Create migrations
    print("\n📝 Creating new migrations...")
    for app in apps:
        if not run_command(f"python manage.py makemigrations {app}", f"Creating migrations for {app}"):
            print(f"⚠️  Failed to create migrations for {app}")
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    # Create superuser
    print("\n👤 Creating superuser...")
    try:
        django.setup()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Superuser created (username: admin, password: admin123)")
        else:
            print("ℹ️  Superuser already exists")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
    
    # Create sample data
    print("\n📊 Creating sample data...")
    try:
        from blog.models import Category
        from books.models import BookCategory
        
        # Create blog categories
        blog_categories = [
            ('Programming', 'programming'),
            ('Technology', 'technology'),
            ('Career', 'career'),
            ('Education', 'education'),
        ]
        
        for name, slug in blog_categories:
            Category.objects.get_or_create(name=name, defaults={'slug': slug})
        
        # Create book categories
        book_categories = [
            ('Programming', 'programming'),
            ('Science', 'science'),
            ('Business', 'business'),
            ('Fiction', 'fiction'),
        ]
        
        for name, slug in book_categories:
            BookCategory.objects.get_or_create(name=name, defaults={'slug': slug})
        
        print("✅ Sample data created")
    except Exception as e:
        print(f"⚠️  Error creating sample data: {e}")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static files collection failed")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin: http://127.0.0.1:8000/admin (admin/admin123)")
    print("\n🚀 Your TrackMyJourney website is ready!")

if __name__ == '__main__':
    setup_django()
