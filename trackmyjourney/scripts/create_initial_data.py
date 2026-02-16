import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackmyjourney.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Category as BlogCategory
from resources.models import ResourceCategory
from books.models import BookCategory

User = get_user_model()

def create_blog_categories():
    categories = [
        ('Cybersecurity', 'cybersecurity', 'Security and privacy topics', '#dc3545', 'fas fa-shield-alt'),
        ('Machine Learning', 'machine-learning', 'ML algorithms and applications', '#28a745', 'fas fa-brain'),
        ('Artificial Intelligence', 'artificial-intelligence', 'AI research and development', '#007bff', 'fas fa-robot'),
        ('Data Science', 'data-science', 'Data analysis and visualization', '#6f42c1', 'fas fa-chart-bar'),
        ('Web Development', 'web-development', 'Frontend and backend development', '#fd7e14', 'fas fa-code'),
        ('Mobile Development', 'mobile-development', 'iOS and Android development', '#20c997', 'fas fa-mobile-alt'),
        ('Cloud Computing', 'cloud-computing', 'Cloud platforms and services', '#17a2b8', 'fas fa-cloud'),
        ('Programming', 'programming', 'Programming languages and techniques', '#6c757d', 'fas fa-laptop-code'),
        ('Tech News', 'tech-news', 'Latest technology news and trends', '#ffc107', 'fas fa-newspaper'),
        ('Research', 'research', 'Academic and industry research', '#e83e8c', 'fas fa-microscope'),
    ]
    
    for name, slug, description, color, icon in categories:
        category, created = BlogCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
                'color': color,
                'icon': icon
            }
        )
        if created:
            print(f"Created blog category: {name}")

def create_resource_categories():
    categories = [
        ('Programming', 'programming', 'Programming resources and tools', '#007bff', 'fas fa-code'),
        ('Data Science', 'data-science', 'Data analysis and ML resources', '#28a745', 'fas fa-chart-line'),
        ('Cybersecurity', 'cybersecurity', 'Security tools and guides', '#dc3545', 'fas fa-shield-alt'),
        ('Design', 'design', 'UI/UX and graphic design resources', '#6f42c1', 'fas fa-palette'),
        ('Documentation', 'documentation', 'Guides and documentation', '#6c757d', 'fas fa-book'),
        ('Tools & Software', 'tools-software', 'Development tools and software', '#fd7e14', 'fas fa-tools'),
        ('Templates', 'templates', 'Code templates and boilerplates', '#20c997', 'fas fa-file-code'),
        ('Datasets', 'datasets', 'Data collections and samples', '#17a2b8', 'fas fa-database'),
    ]
    
    for name, slug, description, color, icon in categories:
        category, created = ResourceCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
                'color': color,
                'icon': icon
            }
        )
        if created:
            print(f"Created resource category: {name}")

def create_book_categories():
    categories = [
        ('Programming', 'programming', 'Programming and development books', '#007bff', 'fas fa-code'),
        ('Data Science', 'data-science', 'Data science and analytics books', '#28a745', 'fas fa-chart-bar'),
        ('Cybersecurity', 'cybersecurity', 'Security and privacy books', '#dc3545', 'fas fa-shield-alt'),
        ('AI & Machine Learning', 'ai-ml', 'AI and ML books', '#6f42c1', 'fas fa-brain'),
        ('Business', 'business', 'Business and management books', '#fd7e14', 'fas fa-briefcase'),
        ('Science', 'science', 'Science and research books', '#17a2b8', 'fas fa-flask'),
        ('Self Help', 'self-help', 'Personal development books', '#20c997', 'fas fa-heart'),
        ('Reference', 'reference', 'Reference and manual books', '#6c757d', 'fas fa-book-open'),
    ]
    
    for name, slug, description, color, icon in categories:
        category, created = BookCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
                'color': color,
                'icon': icon
            }
        )
        if created:
            print(f"Created book category: {name}")

if __name__ == "__main__":
    print("Creating initial categories...")
    create_blog_categories()
    create_resource_categories()
    create_book_categories()
    print("Initial data created successfully!")
