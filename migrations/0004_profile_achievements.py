# Generated by Django 3.2.7 on 2021-09-04 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='achievements',
            field=models.CharField(max_length=120, null=True),
        ),
    ]