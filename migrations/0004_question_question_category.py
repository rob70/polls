# Generated by Django 3.0.8 on 2021-03-15 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_questioncategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.QuestionCategory'),
        ),
    ]