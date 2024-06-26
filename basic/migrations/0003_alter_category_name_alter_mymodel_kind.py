# Generated by Django 5.0.3 on 2024-04-03 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Имя категории', max_length=100),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kinds', to='basic.category'),
        ),
    ]
