# Generated by Django 3.2.4 on 2021-07-12 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0004_auto_20210711_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc.usercharity', to_field='username'),
        ),
        migrations.AlterField(
            model_name='provide',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc.usersponsor', to_field='username'),
        ),
        migrations.AlterField(
            model_name='usercharity',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='usersponsor',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]