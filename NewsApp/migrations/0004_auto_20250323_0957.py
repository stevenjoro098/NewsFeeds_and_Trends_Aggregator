# Generated by Django 3.2.5 on 2025-03-23 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0003_alter_gdletnewsmodel_seendate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gdletnewsmodel',
            options={'ordering': ('-seendate',)},
        ),
        migrations.AddField(
            model_name='gdletnewsmodel',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
