from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0002_remove_submission_exercise_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="base_score",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="time_bonus",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="total_score",
        ),
    ]

