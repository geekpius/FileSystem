# Generated by Django 3.1.7 on 2021-04-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_accounttype_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
