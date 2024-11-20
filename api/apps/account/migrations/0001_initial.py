# Generated by Django 5.1.3 on 2024-11-20 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('name', models.CharField(max_length=200)),
                ('avatar', models.ImageField(blank=True, default='profile_icon.png', null=True, upload_to='', verbose_name='Avatar')),
                ('tc', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_email_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_online', models.BooleanField(default=False)),
                ('auth_provider', models.CharField(choices=[('email', 'Email'), ('google', 'Google'), ('facebook', 'Facebook'), ('twitter', 'Twitter')], default='email', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
