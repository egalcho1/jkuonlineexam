# Generated by Django 4.0 on 2023-03-15 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0012_course_c_code_course_sem_course_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(choices=[('Option1', 'A'), ('Option2', 'B'), ('Option3', 'C'), ('Option4', 'D')], max_length=200),
        ),
    ]
