import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')
django.setup()

from django.contrib.auth import get_user_model
from goals.models import Goal, Milestone
from achievements.models import Achievement
from blog.models import BlogPost, Category
from community.models import Community

User = get_user_model()

# Create sample users
users_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
]

for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            password='password123',
            **user_data
        )
        print(f"Created user: {user.username}")

# Create blog categories
categories_data = [
    {'name': 'Fitness', 'description': 'Health and fitness related posts'},
    {'name': 'Technology', 'description': 'Tech tutorials and insights'},
    {'name': 'Personal Development', 'description': 'Self-improvement and growth'},
    {'name': 'Travel', 'description': 'Travel experiences and tips'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f"Created category: {category.name}")

# Create sample goals
john = User.objects.get(username='john_doe')
goals_data = [
    {
        'title': 'Learn Python Programming',
        'description': 'Complete a comprehensive Python course and build 3 projects',
        'category': 'education',
        'priority': 'high',
        'start_date': date.today() - timedelta(days=30),
        'end_date': date.today() + timedelta(days=60),
        'progress': 65,
        'status': 'in_progress'
    },
    {
        'title': 'Run a 10K Marathon',
        'description': 'Train for and complete a 10K marathon race',
        'category': 'fitness',
        'priority': 'medium',
        'start_date': date.today() - timedelta(days=45),
        'end_date': date.today() + timedelta(days=30),
        'progress': 80,
        'status': 'in_progress'
    }
]

for goal_data in goals_data:
    goal, created = Goal.objects.get_or_create(
        user=john,
        title=goal_data['title'],
        defaults=goal_data
    )
    if created:
        print(f"Created goal: {goal.title}")

# Create sample achievements
achievements_data = [
    {
        'title': 'Completed First Python Project',
        'description': 'Built a web scraper using Python and BeautifulSoup',
        'category': 'technology',
        'badge_type': 'bronze',
        'date_achieved': date.today() - timedelta(days=10)
    },
    {
        'title': 'Ran 5K Without Stopping',
        'description': 'Achieved my first milestone in marathon training',
        'category': 'fitness',
        'badge_type': 'silver',
        'date_achieved': date.today() - timedelta(days=5)
    }
]

for ach_data in achievements_data:
    achievement, created = Achievement.objects.get_or_create(
        user=john,
        title=ach_data['title'],
        defaults=ach_data
    )
    if created:
        print(f"Created achievement: {achievement.title}")

# Create sample communities
communities_data = [
    {
        'name': 'Python Developers',
        'description': 'A community for Python enthusiasts to share knowledge and collaborate',
        'category': 'technology'
    },
    {
        'name': 'Fitness Enthusiasts',
        'description': 'Share your fitness journey and motivate each other',
        'category': 'fitness'
    }
]

for comm_data in communities_data:
    community, created = Community.objects.get_or_create(
        name=comm_data['name'],
        defaults={**comm_data, 'creator': john}
    )
    if created:
        print(f"Created community: {community.name}")

print("Sample data created successfully!")
