# Generated by Django 4.1.7 on 2023-03-07 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(help_text='Order of section in profile')),
                ('profile', models.PositiveIntegerField(help_text='Order of profile in the wall')),
                ('initial_height', models.PositiveIntegerField()),
                ('yards_per_foot', models.PositiveIntegerField(help_text='Area of the section')),
            ],
            options={
                'unique_together': {('profile', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveIntegerField()),
                ('team', models.CharField(max_length=50)),
                ('ice_used', models.PositiveIntegerField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_wall.section')),
            ],
        ),
        migrations.AddIndex(
            model_name='ledger',
            index=models.Index(fields=['day'], name='the_wall_le_day_e8fde9_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='ledger',
            unique_together={('section', 'day')},
        ),
    ]
