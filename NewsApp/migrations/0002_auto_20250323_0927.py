# Generated by Django 3.2.5 on 2025-03-23 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gdletnewsmodel',
            name='snippet',
        ),
        migrations.AddField(
            model_name='gdletnewsmodel',
            name='sourcecountry',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
