# Generated by Django 3.1.7 on 2021-04-07 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'departments',
            },
        ),
    ]