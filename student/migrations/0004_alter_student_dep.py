# Generated by Django 4.0 on 2023-03-12 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_dep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dep',
            field=models.IntegerField(null=True),
        ),
    ]
