# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_tag_headline_image_headline_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='headline',
            name='category',
        ),
        migrations.AddField(
            model_name='headline',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='news_pdfs/', verbose_name='PDF файл'),
        ),
    ]

