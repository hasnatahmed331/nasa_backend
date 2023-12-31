# Generated by Django 4.2.5 on 2023-10-08 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_project_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='CommunicationAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('approved', 'Approved')], max_length=20)),
                ('message', models.TextField(blank=True, null=True)),
                ('has_access_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_to', to='main.customuser')),
                ('to_this_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_from', to='main.customuser')),
            ],
        ),
    ]
