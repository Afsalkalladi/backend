# Generated by Django 5.1.4 on 2025-07-16 21:10

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid mobile number', regex='^\\+?1?\\d{9,15}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Alumni',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid mobile number', regex='^\\+?1?\\d{9,15}$')])),
                ('student_id', models.CharField(blank=True, max_length=20, null=True)),
                ('branch', models.CharField(max_length=100)),
                ('year_of_admission', models.PositiveIntegerField()),
                ('year_of_passout', models.PositiveIntegerField()),
                ('cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('current_workplace', models.CharField(blank=True, max_length=200, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('current_location', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, help_text='Notable achievements and awards')),
                ('willing_to_mentor', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Alumni',
                'ordering': ['-year_of_passout', 'last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(help_text='Role/Position in the team', max_length=100)),
                ('bio', models.TextField(help_text='Brief description about the member')),
                ('image', models.ImageField(blank=True, null=True, upload_to='team_members/')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('github_url', models.URLField(blank=True, null=True)),
                ('team_type', models.CharField(choices=[('eesa', 'EESA Team'), ('tech', 'Tech Team')], max_length=10)),
                ('is_active', models.BooleanField(default=True, help_text='Is this member currently active?')),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower numbers appear first)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Team Member',
                'verbose_name_plural': 'Team Members',
                'ordering': ['team_type', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Created'), ('update', 'Updated'), ('delete', 'Deleted'), ('approve', 'Approved'), ('reject', 'Rejected'), ('upload', 'Uploaded'), ('download', 'Downloaded'), ('verify', 'Verified'), ('feature', 'Featured'), ('unfeature', 'Unfeatured'), ('publish', 'Published'), ('unpublish', 'Unpublished'), ('activate', 'Activated'), ('deactivate', 'Deactivated')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('object_repr', models.CharField(help_text='String representation of the object', max_length=200)),
                ('changes', models.JSONField(blank=True, help_text='What fields were changed', null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['user', 'timestamp'], name='accounts_au_user_id_d4cccd_idx'), models.Index(fields=['content_type', 'object_id'], name='accounts_au_content_659137_idx'), models.Index(fields=['action', 'timestamp'], name='accounts_au_action_11cc52_idx')],
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid mobile number', regex='^\\+?1?\\d{9,15}$')])),
                ('semester', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=100)),
                ('event_title', models.CharField(max_length=200)),
                ('payment_status', models.CharField(choices=[('pending', 'Payment Pending'), ('paid', 'Payment Completed'), ('exempted', 'Fee Exempted')], default='pending', max_length=20)),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-registered_at'],
                'unique_together': {('email', 'event_title')},
            },
        ),
    ]
