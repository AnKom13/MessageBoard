# Generated by Django 4.2.4 on 2023-08-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='Содержание'),
        ),
    ]
