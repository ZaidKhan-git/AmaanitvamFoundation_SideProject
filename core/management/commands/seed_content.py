"""
Management command to seed initial site content.
Run with: python manage.py seed_content
"""
from django.core.management.base import BaseCommand
from core.models import SiteContent


class Command(BaseCommand):
    help = 'Seeds the database with initial site content'

    def handle(self, *args, **options):
        content_data = [
            # =================================================================
            # HOME PAGE
            # =================================================================
            # Hero Section
            {
                'key': 'home_hero_tag',
                'page': 'home',
                'section': 'Hero',
                'label': 'Hero Tag Line',
                'content_type': 'text',
                'text_content': 'Take Action Now',
            },
            {
                'key': 'home_hero_title_1',
                'page': 'home',
                'section': 'Hero',
                'label': 'Hero Title Line 1',
                'content_type': 'text',
                'text_content': 'Every Child Deserves',
            },
            {
                'key': 'home_hero_title_2',
                'page': 'home',
                'section': 'Hero',
                'label': 'Hero Title Line 2 (Red)',
                'content_type': 'text',
                'text_content': 'A Fighting Chance',
            },
            {
                'key': 'home_hero_description',
                'page': 'home',
                'section': 'Hero',
                'label': 'Hero Description',
                'content_type': 'text',
                'text_content': 'Millions of children in India face hunger, lack access to education, and are denied basic healthcare. Your support can change their story.',
            },
            {
                'key': 'home_hero_image',
                'page': 'home',
                'section': 'Hero',
                'label': 'Hero Background Image URL',
                'content_type': 'url',
                'text_content': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            },
            # Urgent Appeal
            {
                'key': 'home_urgent_text',
                'page': 'home',
                'section': 'Urgent Appeal',
                'label': 'Urgent Appeal Text',
                'content_type': 'text',
                'text_content': 'Children need your help now. Every donation makes a difference.',
            },
            # What We Do Section
            {
                'key': 'home_whatwedo_description',
                'page': 'home',
                'section': 'What We Do',
                'label': 'What We Do Description',
                'content_type': 'text',
                'text_content': "We fight for children's rights every day, ensuring they have access to the essentials they need to survive and thrive.",
            },
            {
                'key': 'home_education_desc',
                'page': 'home',
                'section': 'What We Do',
                'label': 'Education Card Description',
                'content_type': 'text',
                'text_content': 'We ensure children have access to quality education, school supplies, and the support they need to succeed academically.',
            },
            {
                'key': 'home_healthcare_desc',
                'page': 'home',
                'section': 'What We Do',
                'label': 'Healthcare Card Description',
                'content_type': 'text',
                'text_content': 'We provide essential healthcare services, vaccinations, and medical support to children in underserved communities.',
            },
            {
                'key': 'home_nutrition_desc',
                'page': 'home',
                'section': 'What We Do',
                'label': 'Nutrition Card Description',
                'content_type': 'text',
                'text_content': 'We combat hunger by providing nutritious meals and food security programs to children and their families.',
            },
            # Ways to Give
            {
                'key': 'home_give_description',
                'page': 'home',
                'section': 'Ways to Give',
                'label': 'Ways to Give Description',
                'content_type': 'text',
                'text_content': 'Your generosity helps us save and improve the lives of children every day.',
            },
            # CTA Section
            {
                'key': 'home_cta_title',
                'page': 'home',
                'section': 'CTA',
                'label': 'CTA Section Title',
                'content_type': 'text',
                'text_content': "Children Can't Wait. Act Now.",
            },
            {
                'key': 'home_cta_description',
                'page': 'home',
                'section': 'CTA',
                'label': 'CTA Section Description',
                'content_type': 'text',
                'text_content': 'Every minute without action is a minute of suffering for a child. Your donation today can save lives.',
            },
            
            # =================================================================
            # ABOUT PAGE
            # =================================================================
            {
                'key': 'about_hero_description',
                'page': 'about',
                'section': 'Hero',
                'label': 'About Hero Description',
                'content_type': 'text',
                'text_content': "A Section 8 Non-Profit Company fighting for children's rights across India.",
            },
            {
                'key': 'about_mission_quote',
                'page': 'about',
                'section': 'Mission',
                'label': 'Mission Statement Quote',
                'content_type': 'text',
                'text_content': 'We believe every child deserves a chance to survive, learn, and be protected — no matter where they live or their circumstances.',
            },
            {
                'key': 'about_story_1',
                'page': 'about',
                'section': 'Our Story',
                'label': 'Our Story Paragraph 1',
                'content_type': 'html',
                'text_content': 'Amaanitvam Foundation was born from a simple belief: every child, regardless of their circumstances, deserves a chance to dream and the support to achieve those dreams.',
            },
            {
                'key': 'about_story_2',
                'page': 'about',
                'section': 'Our Story',
                'label': 'Our Story Paragraph 2',
                'content_type': 'html',
                'text_content': "Registered on September 12, 2025, we started with a vision to provide support to children in underserved communities in Delhi. Today, we're working across Art & Culture, Children, Education & Literacy, Environment & Forests, and Food Processing sectors.",
            },
            {
                'key': 'about_story_3',
                'page': 'about',
                'section': 'Our Story',
                'label': 'Our Story Paragraph 3',
                'content_type': 'html',
                'text_content': 'The name "Amaanitvam" comes from Sanskrit, meaning "dignity" — a core value that drives everything we do. We believe in empowering children, not through charity alone, but by building systems that foster independence and self-worth.',
            },
            
            # =================================================================
            # WHAT WE DO PAGE
            # =================================================================
            {
                'key': 'whatwedo_hero_description',
                'page': 'what_we_do',
                'section': 'Hero',
                'label': 'What We Do Hero Description',
                'content_type': 'text',
                'text_content': 'Empowering children through quality education and learning opportunities.',
            },
            {
                'key': 'whatwedo_mission_text',
                'page': 'what_we_do',
                'section': 'Mission',
                'label': 'Mission Statement',
                'content_type': 'text',
                'text_content': 'Every child deserves the chance to learn, grow, and dream big.',
            },
            {
                'key': 'whatwedo_education_intro',
                'page': 'what_we_do',
                'section': 'Education',
                'label': 'Education Section Intro',
                'content_type': 'html',
                'text_content': 'We believe education is the foundation for breaking the cycle of poverty. Our education programs provide children with the tools, resources, and support they need to succeed academically and build a brighter future.',
            },
            {
                'key': 'whatwedo_cta_title',
                'page': 'what_we_do',
                'section': 'CTA',
                'label': 'CTA Title',
                'content_type': 'text',
                'text_content': 'Help Us Do More',
            },
            {
                'key': 'whatwedo_cta_description',
                'page': 'what_we_do',
                'section': 'CTA',
                'label': 'CTA Description',
                'content_type': 'text',
                'text_content': 'Your support enables us to expand our education programs and reach more children in need.',
            },
            
            # =================================================================
            # DONATE PAGE
            # =================================================================
            {
                'key': 'donate_hero_description',
                'page': 'donate',
                'section': 'Hero',
                'label': 'Donate Hero Description',
                'content_type': 'text',
                'text_content': 'Your contribution directly impacts the lives of underprivileged children.',
            },
            {
                'key': 'donate_impact_text',
                'page': 'donate',
                'section': 'Impact',
                'label': 'Impact Section Text',
                'content_type': 'text',
                'text_content': 'Every rupee you donate goes directly towards our programs for children.',
            },
        ]

        created_count = 0
        updated_count = 0

        for item in content_data:
            obj, created = SiteContent.objects.update_or_create(
                key=item['key'],
                defaults={
                    'page': item['page'],
                    'section': item['section'],
                    'label': item['label'],
                    'content_type': item['content_type'],
                    'text_content': item['text_content'],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded site content: {created_count} created, {updated_count} updated'
            )
        )
