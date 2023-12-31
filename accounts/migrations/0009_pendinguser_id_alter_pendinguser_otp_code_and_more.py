# Generated by Django 4.2.2 on 2023-06-28 05:23

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0008_remove_pendinguser_full_name_remove_pendinguser_id_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="pendinguser",
            name="id",
            field=models.CharField(
                default="jncnjhdsohceisojcskijcdsj",
                max_length=32,
                primary_key=True,
                serialize=False,
                verbose_name="شناسه",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="pendinguser",
            name="otp_code",
            field=models.CharField(
                max_length=8, null=True, verbose_name="کد فعال سازی"
            ),
        ),
        migrations.AlterField(
            model_name="pendinguser",
            name="password",
            field=models.CharField(max_length=255, null=True, verbose_name="رمز عبور"),
        ),
        migrations.AlterField(
            model_name="pendinguser",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="حداکثر ۶۰ حرف و فقط حروف و اعداد و غیره.",
                max_length=60,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="نام کاربری",
            ),
        ),
    ]
