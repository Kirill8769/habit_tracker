# Generated by Django 5.0.6 on 2024-06-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0012_alter_habit_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.TextField(choices=[('Monday', 'Понедельник'), ('Tuesday', 'Вторник'), ('Wednesday', 'Среда'), ('Thursday', 'Четверг'), ('Friday', 'Пятница'), ('Saturday', 'Суббота'), ('Sunday', 'Воскресенье'), ('Everyday', 'Каждый день')], help_text='Выберите периодичность выполнения', verbose_name='Периодичность'),
        ),
    ]