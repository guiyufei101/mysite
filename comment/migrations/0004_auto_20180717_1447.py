# Generated by Django 2.0.7 on 2018-07-17 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20180717_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='comment.Comment'),
        ),
    ]
