# Generated by Django 4.0.4 on 2022-05-12 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.cart'),
        ),
    ]
