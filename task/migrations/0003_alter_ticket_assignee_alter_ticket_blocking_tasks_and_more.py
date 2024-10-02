# Generated by Django 4.2.4 on 2024-10-02 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0002_ticket_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='blocking_tasks',
            field=models.ManyToManyField(blank=True, related_name='blocked_by_tasks', to='task.ticket'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='number',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('todo', 'To do'), ('in_progress', 'In progress'), ('code_review', 'Code review'), ('dev_test', 'Dev test'), ('testing', 'Testing'), ('done', 'Done'), ('wontfix', 'Wontfix')], default='todo', max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='task_type',
            field=models.CharField(choices=[('bug', 'Bug'), ('task', 'Task')], default='task', max_length=10),
        ),
    ]
