# Generated by Django 5.0.6 on 2024-09-06 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agi_agents_app', '0004_alter_agent_accessory_model_alter_agent_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='email',
            field=models.EmailField(blank=True, max_length=150, null=True),
        ),
    ]
