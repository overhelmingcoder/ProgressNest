import os
import django
import subprocess
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')

def run_command(command):
    """Run a command and print the output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Success")
        if result.stdout:
            print(result.stdout)
    else:
        print("❌ Error")
        if result.stderr:
            print(result.stderr)
    return result.returncode == 0

def main():
    print("🚀 Setting up TrackMyJourney project...")
    
    # Install requirements
    print("\n📦 Installing requirements...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install requirements")
        return
    
    # Make migrations
    print("\n🔄 Creating migrations...")
    apps = ['accounts', 'goals', 'achievements', 'blog', 'resources', 'books', 'groups', 'community']
    
    for app in apps:
        if not run_command(f"python manage.py makemigrations {app}"):
            print(f"Failed to create migrations for {app}")
            return
    
    # Apply migrations
    print("\n📊 Applying migrations...")
    if not run_command("python manage.py migrate"):
        print("Failed to apply migrations")
        return
    
    # Create superuser
    print("\n👤 Creating superuser...")
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@trackmyjourney.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✅ Superuser created (admin/admin123)")
    else:
        print("✅ Superuser already exists")
    
    # Create initial data
    print("\n📝 Creating initial data...")
    if not run_command("python scripts/create_initial_data.py"):
        print("Failed to create initial data")
        return
    
    # Collect static files
    print("\n🎨 Collecting static files...")
    if not run_command("python manage.py collectstatic --noinput"):
        print("Failed to collect static files")
        return
    
    print("\n🎉 Project setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin: http://127.0.0.1:8000/admin (admin/admin123)")

if __name__ == "__main__":
    main()
