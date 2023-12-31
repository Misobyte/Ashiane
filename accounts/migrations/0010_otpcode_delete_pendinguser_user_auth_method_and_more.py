# Generated by Django 4.2.3 on 2023-08-20 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_pendinguser_id_alter_pendinguser_otp_code_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OtpCode",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        verbose_name="شناسه",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت"),
                ),
                (
                    "otp_code",
                    models.CharField(
                        max_length=8, null=True, verbose_name="کد فعال سازی"
                    ),
                ),
            ],
            options={
                "verbose_name": "کد فعال سازی",
                "verbose_name_plural": "کد های فعال سازی",
            },
        ),
        migrations.DeleteModel(
            name="PendingUser",
        ),
        migrations.AddField(
            model_name="user",
            name="auth_method",
            field=models.CharField(
                choices=[("number", "شماره تلفن"), ("email", "ایمیل")],
                max_length=6,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="otp_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="user",
                to="accounts.otpcode",
            ),
        ),
    ]
