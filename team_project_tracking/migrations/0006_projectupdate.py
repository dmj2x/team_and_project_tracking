# Generated by Django 2.2.4 on 2019-12-04 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team_project_tracking', '0005_teamproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_title', models.CharField(max_length=20)),
                ('update_notes', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_update', to='team_project_tracking.TeamProject')),
            ],
            options={
                'db_table': 'project_update',
                'unique_together': {('project', 'update_title')},
            },
        ),
    ]
