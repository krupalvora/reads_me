# Generated by Django 4.1.5 on 2023-01-25 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='order_by',
            field=models.CharField(choices=[('views', 'views'), ('date added', 'date added'), ('recently viewed', 'recently viewed'), ('shuffle', 'shuffle')], default=None, max_length=32, null=True),
        ),
    ]
