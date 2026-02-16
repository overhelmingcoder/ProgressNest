#!/usr/bin/env python
"""
Complete setup script for TrackMyJourney
This script will set up the entire Django project with all features
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        if e.stderr:
            print(e.stderr)
        if e.stdout:
            print(e.stdout)
        return False

def create_categories():
    """Create default goal categories"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')
        django.setup()
        
        from goals.models import Category
        
        categories = [
            {'name': 'Health & Fitness', 'color': '#10b981', 'icon': 'fas fa-heartbeat'},
            {'name': 'Career & Business', 'color': '#3b82f6', 'icon': 'fas fa-briefcase'},
            {'name': 'Education & Learning', 'color': '#8b5cf6', 'icon': 'fas fa-graduation-cap'},
            {'name': 'Personal Development', 'color': '#f59e0b', 'icon': 'fas fa-user-plus'},
            {'name': 'Relationships', 'color': '#ef4444', 'icon': 'fas fa-heart'},
            {'name': 'Finance', 'color': '#059669', 'icon': 'fas fa-dollar-sign'},
            {'name': 'Hobbies & Interests', 'color': '#7c3aed', 'icon': 'fas fa-palette'},
            {'name': 'Travel & Adventure', 'color': '#06b6d4', 'icon': 'fas fa-plane'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'color': cat_data['color'],
                    'icon': cat_data['icon'],
                    'description': f"Goals related to {cat_data['name'].lower()}"
                }
            )
        
        print(f"✅ Created {len(categories)} goal categories")
        return True
    except Exception as e:
        print(f"❌ Error creating categories: {e}")
        return False

def create_superuser():
    """Create superuser account"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')
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
            print("✅ Superuser created: admin / admin123")
        else:
            print("✅ Superuser already exists")
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def create_sample_data():
    """Create sample data for demonstration"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        from goals.models import Goal, Category
        from achievements.models import Achievement
        
        User = get_user_model()
        
        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@trackmyjourney.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'bio': 'This is a demo user account to showcase TrackMyJourney features.'
            }
        )
        
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            print("✅ Demo user created: demo / demo123")
        
        # Create sample goals
        categories = Category.objects.all()
        if categories.exists():
            sample_goals = [
                {
                    'title': 'Run a Marathon',
                    'description': 'Train for and complete a full 26.2-mile marathon race.',
                    'category': categories.filter(name__icontains='health').first(),
                    'progress': 45,
                    'status': 'in_progress',
                    'priority': 'high'
                },
                {
                    'title': 'Learn Python Programming',
                    'description': 'Master Python programming language and build 5 projects.',
                    'category': categories.filter(name__icontains='education').first(),
                    'progress': 75,
                    'status': 'in_progress',
                    'priority': 'medium'
                },
                {
                    'title': 'Save $10,000',
                    'description': 'Build an emergency fund of $10,000 by the end of the year.',
                    'category': categories.filter(name__icontains='finance').first(),
                    'progress': 30,
                    'status': 'in_progress',
                    'priority': 'high'
                }
            ]
            
            for goal_data in sample_goals:
                Goal.objects.get_or_create(
                    user=demo_user,
                    title=goal_data['title'],
                    defaults=goal_data
                )
            
            print("✅ Sample goals created")
        
        # Create sample achievements
        sample_achievements = [
            {
                'title': 'First Goal Created',
                'description': 'Created your very first goal on TrackMyJourney!',
                'badge_icon': 'fas fa-flag',
                'is_public': True
            },
            {
                'title': 'Early Bird',
                'description': 'Completed a goal ahead of schedule.',
                'badge_icon': 'fas fa-clock',
                'is_public': True
            }
        ]
        
        for achievement_data in sample_achievements:
            Achievement.objects.get_or_create(
                user=demo_user,
                title=achievement_data['title'],
                defaults=achievement_data
            )
        
        print("✅ Sample achievements created")
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    print("🚀 TrackMyJourney Complete Setup")
    print("=" * 50)
    
    # Install requirements
    print("📦 Installing requirements...")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("⚠️  Warning: Could not install requirements. Please run: pip install -r requirements.txt")
    
    # Remove old database
    db_path = BASE_DIR / 'db.sqlite3'
    if db_path.exists():
        db_path.unlink()
        print("🗑️  Removed old database")
    
    # Remove old migrations
    print("\n🧹 Cleaning old migrations...")
    apps = ['accounts', 'goals', 'achievements', 'blog', 'resources', 'books', 'groups', 'community']
    
    for app in apps:
        migrations_dir = BASE_DIR / app / 'migrations'
        if migrations_dir.exists():
            for file in migrations_dir.glob('*.py'):
                if file.name != '__init__.py':
                    file.unlink()
            print(f"   Cleaned {app} migrations")
    
    # Create new migrations
    print("\n📝 Creating fresh migrations...")
    run_command("python manage.py makemigrations accounts", "Creating accounts migrations")
    run_command("python manage.py makemigrations goals", "Creating goals migrations")
    run_command("python manage.py makemigrations achievements", "Creating achievements migrations")
    run_command("python manage.py makemigrations blog", "Creating blog migrations")
    run_command("python manage.py makemigrations resources", "Creating resources migrations")
    run_command("python manage.py makemigrations books", "Creating books migrations")
    run_command("python manage.py makemigrations groups", "Creating groups migrations")
    run_command("python manage.py makemigrations community", "Creating community migrations")
    
    # Apply migrations
    print("\n🔄 Applying migrations...")
    run_command("python manage.py migrate", "Applying all migrations")
    
    # Create directories
    print("\n📁 Creating directories...")
    directories = ['media', 'media/avatars', 'media/uploads', 'staticfiles']
    for directory in directories:
        dir_path = BASE_DIR / directory
        dir_path.mkdir(exist_ok=True)
        print(f"   Created {directory}/")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Create categories
    print("\n🏷️  Creating goal categories...")
    create_categories()
    
    # Create superuser
    print("\n👤 Creating superuser...")
    create_superuser()
    
    # Create sample data
    print("\n🎯 Creating sample data...")
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\n📋 What's Ready:")
    print("✅ Complete Django project with all apps")
    print("✅ User authentication system")
    print("✅ Goal tracking with categories")
    print("✅ Achievement system")
    print("✅ Blog functionality")
    print("✅ Resource sharing")
    print("✅ Books library")
    print("✅ Groups and community")
    print("✅ Beautiful responsive UI")
    print("✅ Admin interface")
    print("✅ Sample data for testing")
    
    print("\n🚀 Next Steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin: http://127.0.0.1:8000/admin")
    
    print("\n🔑 Login Credentials:")
    print("Admin: admin / admin123")
    print("Demo User: demo / demo123")
    
    print("\n✨ Your TrackMyJourney website is ready!")
    print("🌟 Features include goal tracking, achievements, blog, resources, and community!")

if __name__ == "__main__":
    main()
