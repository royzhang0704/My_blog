# Generated by Django 5.0.6 on 2024-07-23 11:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="test",
            new_name="text",
        ),
    ]
