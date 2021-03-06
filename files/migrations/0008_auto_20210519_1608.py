# Generated by Django 3.1.7 on 2021-05-19 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0007_auto_20210518_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forwardfile',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='forwardfile',
            name='status',
        ),
        migrations.CreateModel(
            name='ForwardFileReciever',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('forward_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forward_file_receivers', to='files.forwardfile')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forward_receivers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'forward_file_recivers',
            },
        ),
    ]
