# Generated by Django 4.0 on 2023-03-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_alter_schedule_id_alter_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
