from django.core.management.base import BaseCommand
from homepage.models import FakePost, HomePageSettings

class Command(BaseCommand):
    help = 'Create sample data for homepage'

    def handle(self, *args, **options):
        # Create homepage settings
        settings, created = HomePageSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(self.style.SUCCESS('Created homepage settings'))

        # Create sample posts
        sample_posts = [
            {
                'title': 'Cybersecurity Career Path: A Complete Guide',
                'content': 'In an era where cyber threats are increasing at an unprecedented rate, the demand for skilled cybersecurity professionals has never been higher. This comprehensive guide will walk you through everything you need to know about starting and advancing your career in cybersecurity.',
                'author_name': 'Ali Hossain',
                'tags': 'cybersecurity, career, guide',
                'likes_count': 45,
                'comments_count': 12,
            },
            {
                'title': 'AI-Powered Cyber Threats: The New Frontier',
                'content': 'Attackers are leveraging AI to create sophisticated malware, automate phishing attacks, and bypass traditional security measures. Learn how to defend against these emerging threats and stay ahead of cybercriminals.',
                'author_name': 'Mahathir Khandaker',
                'tags': 'AI, threats, malware',
                'likes_count': 32,
                'comments_count': 8,
            },
            {
                'title': 'Understanding Zero-Day Exploits: The Invisible Cyber Threat',
                'content': 'A zero-day exploit is a cyberattack targeting a software vulnerability unknown to the vendor, leaving no time for patches. Discover how these attacks work and how to protect your systems.',
                'author_name': 'Mohammad Rahat Hossain',
                'tags': 'zero-day, exploits, security',
                'likes_count': 28,
                'comments_count': 15,
            },
            {
                'title': 'Cloud Security Enhancements for 2025',
                'content': 'With more businesses migrating to the cloud, securing cloud environments against misconfigurations and data breaches is a top priority. Learn the latest cloud security best practices.',
                'author_name': 'Sifat Mahmud',
                'tags': 'cloud, security, best-practices',
                'likes_count': 38,
                'comments_count': 6,
            },
            {
                'title': 'Rise in Ransomware Attacks: Prevention Strategies',
                'content': 'Ransomware remains a major threat, with attackers using double extortion tactics to pressure victims into paying. Learn effective prevention and response strategies.',
                'author_name': 'Mahathir Mohammad',
                'tags': 'ransomware, prevention, security',
                'likes_count': 41,
                'comments_count': 9,
            },
        ]

        for post_data in sample_posts:
            post, created = FakePost.objects.get_or_create(
                title=post_data['title'],
                defaults=post_data
            )
            if created:
                self.stdout.write(f'Created post: {post.title}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
