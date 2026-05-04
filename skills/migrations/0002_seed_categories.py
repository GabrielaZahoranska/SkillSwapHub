from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('skills', 'Category')
    names = [
        'Programming',
        'Cooking',
        'Fitness',
        'Music',
        'Languages',
        'Art & Design',
    ]
    for name in names:
        Category.objects.get_or_create(name=name)


def unseed_categories(apps, schema_editor):
    Category = apps.get_model('skills', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
