# Generated by Django 3.1.1 on 2020-10-23 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfund', '0010_auto_20201022_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20)),
                ('caption', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
    ]
