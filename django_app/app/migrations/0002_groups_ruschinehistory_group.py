# Generated by Django 4.0 on 2021-12-30 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='Default', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='ruschinehistory',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.groups'),
            preserve_default=False,
        ),
    ]
