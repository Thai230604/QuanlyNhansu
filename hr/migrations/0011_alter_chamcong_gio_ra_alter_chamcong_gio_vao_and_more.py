# Generated by Django 5.1.2 on 2024-10-29 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_alter_chamcong_gio_ra_alter_chamcong_gio_vao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamcong',
            name='gio_ra',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chamcong',
            name='gio_vao',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chamcong',
            name='ngay_cham_cong',
            field=models.DateField(),
        ),
    ]
