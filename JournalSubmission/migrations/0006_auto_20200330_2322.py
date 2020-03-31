# Generated by Django 3.0.3 on 2020-03-31 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200317_1854'),
        ('JournalSubmission', '0005_submission_inreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='editorApproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='reviewer1_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='reviewer2_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='reviewer3_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='reviewer1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewer_1', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='reviewer2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewer_2', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='reviewer3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewer_3', to='users.Profile'),
        ),
    ]
