# Generated by Django 4.0 on 2023-03-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0016_course_dp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('perm', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='pre',
            field=models.IntegerField(default=0),
        ),
    ]
