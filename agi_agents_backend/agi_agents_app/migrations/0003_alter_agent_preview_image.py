# Generated by Django 5.0.6 on 2024-08-19 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agi_agents_app', '0002_agent_access_agent_created_by_agent_demo_video_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='preview_image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
