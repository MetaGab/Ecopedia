# Generated by Django 2.1.4 on 2018-12-06 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='slug',
            field=models.CharField(default='a', max_length=256),
            preserve_default=False,
        ),
    ]