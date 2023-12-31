# Generated by Django 4.2.2 on 2023-06-24 08:33

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_otpcode_phone_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="otpcode",
            options={
                "verbose_name": "کد فعال سازی",
                "verbose_name_plural": "کد های فعال سازی",
            },
        ),
        migrations.AlterField(
            model_name="otpcode",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None, verbose_name="شماره تلفن"
            ),
        ),
    ]
