# Generated by Django 4.2.4 on 2023-08-31 07:20

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_comment_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='announcement',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Содержание'),
        ),
    ]
