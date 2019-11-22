# Generated by Django 2.2.4 on 2019-11-21 23:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team_project_tracking', '0008_auto_20191121_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='course_offering',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='team_course_offering', to='team_project_tracking.CourseOffering'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together={('team_name', 'course_offering', 'team_creator')},
        ),
        migrations.AddIndex(
            model_name='team',
            index=models.Index(fields=['team_name', 'course_offering', 'team_creator'], name='team_team_na_70f4b5_idx'),
        ),
        migrations.RemoveField(
            model_name='team',
            name='course',
        ),
    ]
