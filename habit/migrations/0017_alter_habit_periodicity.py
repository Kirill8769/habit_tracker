# Generated by Django 5.0.6 on 2024-06-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0016_alter_habit_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.CharField(choices=[('Monday', 'Понедельник'), ('Tuesday', 'Вторник'), ('Wednesday', 'Среда'), ('Thursday', 'Четверг'), ('Friday', 'Пятница'), ('Saturday', 'Суббота'), ('Sunday', 'Воскресенье'), ('Everyday', 'Каждый день')], default='Everyday', help_text='Выберите периодичность выполнения', max_length=10, verbose_name='Периодичность'),
        ),
    ]
