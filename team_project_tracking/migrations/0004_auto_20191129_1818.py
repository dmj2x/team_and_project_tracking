# Generated by Django 2.2.4 on 2019-11-29 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_project_tracking', '0003_profile_user_role'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='team',
            name='team_team_na_70f4b5_idx',
        ),
        migrations.AddField(
            model_name='teammember',
            name='team_creator',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together={('team_name', 'course_offering')},
        ),
        migrations.AddIndex(
            model_name='team',
            index=models.Index(fields=['team_name', 'course_offering'], name='team_team_na_38b48e_idx'),
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_creator',
        ),
    ]