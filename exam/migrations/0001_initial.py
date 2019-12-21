# Generated by Django 3.0 on 2019-12-21 12:30

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('total_time', models.FloatField(help_text='total time should be in minutes')),
                ('is_published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExamQuestion',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('time_per_question', models.IntegerField(default=0, editable=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
            ],
        ),
        migrations.AddIndex(
            model_name='exam',
            index=models.Index(fields=['id'], name='exam_exam_id_5eaed9_idx'),
        ),
        migrations.AddIndex(
            model_name='examquestion',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['id'], name='exam_examqu_id_7cad19_brin'),
        ),
    ]
