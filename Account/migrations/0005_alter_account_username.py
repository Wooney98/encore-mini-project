# Generated by Django 4.1.4 on 2022-12-25 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_account_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=40, unique=True, verbose_name='name'),
        ),
    ]
