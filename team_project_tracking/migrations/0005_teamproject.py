# Generated by Django 2.2.4 on 2019-11-30 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team_project_tracking', '0004_auto_20191129_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('project_status', models.CharField(choices=[('in-progress', 'in-progress'), ('complete', 'complete')], default='in-progress', max_length=15)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_with_project', to='team_project_tracking.Team')),
            ],
            options={
                'db_table': 'team_project',
                'unique_together': {('team', 'project_name')},
            },
        ),
    ]
