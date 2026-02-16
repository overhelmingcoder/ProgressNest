from django.core.management.base import BaseCommand
from goals.models import Category

class Command(BaseCommand):
    help = 'Create default goal categories'

    def handle(self, *args, **options):
        categories_data = [
            'Fitness & Health',
            'Education & Learning',
            'Career & Professional',
            'Personal Development',
            'Creative & Artistic',
            'Technology & Coding',
            'Finance & Wealth',
            'Social & Relationships',
            'Travel & Adventure',
            'Hobbies & Recreation',
        ]

        created_count = 0
        for category_name in categories_data:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal new categories created: {created_count}')
        )
