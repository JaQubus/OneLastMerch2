# Generated by Django 5.1.6 on 2025-03-02 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui_ux', '0002_prize_spinresult_delete_userprize'),
    ]

    operations = [
        migrations.AddField(
            model_name='prize',
            name='color',
            field=models.CharField(default='#FF6F61', max_length=7),
        ),
    ]
