from django.core.management.base import BaseCommand
from django.utils.text import slugify
from books.models import BookCategory

class Command(BaseCommand):
    help = 'Create initial book categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Fiction',
                'description': 'Fiction novels and stories',
                'color': '#FF6B6B'
            },
            {
                'name': 'Non-Fiction',
                'description': 'Non-fictional works and memoirs',
                'color': '#4ECDC4'
            },
            {
                'name': 'Business',
                'description': 'Business and entrepreneurship books',
                'color': '#45B7D1'
            },
            {
                'name': 'Self-Help',
                'description': 'Personal development and self-improvement',
                'color': '#96CEB4'
            },
            {
                'name': 'Science',
                'description': 'Science and technology books',
                'color': '#FFEAA7'
            },
            {
                'name': 'History',
                'description': 'Historical books and chronicles',
                'color': '#DFE6E9'
            },
            {
                'name': 'Mystery & Thriller',
                'description': 'Mystery, suspense, and thriller novels',
                'color': '#74B9FF'
            },
            {
                'name': 'Romance',
                'description': 'Romance and love stories',
                'color': '#FD79A8'
            },
            {
                'name': 'Fantasy',
                'description': 'Fantasy and magical worlds',
                'color': '#A29BFE'
            },
            {
                'name': 'Education',
                'description': 'Educational and learning materials',
                'color': '#55EFC4'
            },
            {
                'name': 'Biography',
                'description': 'Biographies and life stories',
                'color': '#6C5CE7'
            },
            {
                'name': 'Poetry',
                'description': 'Poetry and verse collections',
                'color': '#F368E7'
            }
        ]

        created_count = 0
        for cat_data in categories:
            slug = slugify(cat_data['name'])
            category, created = BookCategory.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'color': cat_data['color']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category "{category.name}"')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category "{category.name}" already exists')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal new categories created: {created_count}')
        )
