# Generated by Django 2.2.4 on 2019-11-21 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import partial_date.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team_project_tracking', '0006_auto_20191121_0028'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_status',
        ),
        migrations.RemoveField(
            model_name='course',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='course',
            name='year',
        ),
        migrations.CreateModel(
            name='CourseOffering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('--', '--'), ('fall', 'fall'), ('spring', 'spring'), ('summer', 'summer')], default='--', max_length=6)),
                ('year', partial_date.fields.PartialDateField()),
                ('course_status', models.CharField(choices=[('active', 'active'), ('discontinued', 'discontinued')], default='active', max_length=10)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='team_project_tracking.Course')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty', to=settings.AUTH_USER_MODEL)),
                ('teaching_assistant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teaching_assistant', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course_offering',
                'unique_together': {('course', 'semester', 'year', 'faculty')},
            },
        ),
    ]