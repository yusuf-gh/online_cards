# Generated by Django 5.0.6 on 2024-07-12 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cards',
            name='expiry_month',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='cards',
            name='expiry_year',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
