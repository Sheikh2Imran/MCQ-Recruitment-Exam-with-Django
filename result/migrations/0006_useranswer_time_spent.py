# Generated by Django 3.0 on 2019-12-20 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0005_auto_20191218_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='time_spent',
            field=models.IntegerField(null=True),
        ),
    ]
