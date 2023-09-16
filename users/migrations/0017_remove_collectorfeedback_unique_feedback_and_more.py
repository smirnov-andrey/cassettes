# Generated by Django 4.1.7 on 2023-08-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_collectorfeedback_unique_feedback_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='collectorfeedback',
            name='unique_feedback',
        ),
        migrations.RemoveConstraint(
            model_name='collectorfeedback',
            name='self_feedback',
        ),
        migrations.AddConstraint(
            model_name='collectorfeedback',
            constraint=models.UniqueConstraint(fields=('user', 'collector'), name='unique_feedback_relationships', violation_error_message='Feedback with this User and Collector already exists'),
        ),
        migrations.AddConstraint(
            model_name='collectorfeedback',
            constraint=models.CheckConstraint(check=models.Q(('user', models.F('collector')), _negated=True), name='prevent_self_feedback', violation_error_message='Feedback with matching User and Collector is not allowed'),
        ),
    ]