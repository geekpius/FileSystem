# Generated by Django 3.1.7 on 2021-06-28 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0011_auto_20210521_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='type',
        ),
        migrations.AlterField(
            model_name='filereciever',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
