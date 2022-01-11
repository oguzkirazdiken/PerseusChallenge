# Generated by Django 4.0.1 on 2022-01-09 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_certificate_course_alter_certificate_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='course',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.CASCADE, to='api.course'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='user',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
    ]
