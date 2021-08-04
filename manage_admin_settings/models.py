from django.db import models
import django


# ________________________________________model for Email Settings______________________________________________________
class Email_Setting(models.Model):
    smtp_host = models.CharField(max_length=150, default="")
    smtp_username = models.CharField(max_length=150, default="")
    smtp_port = models.CharField(max_length=150, default="")
    smtp_password = models.CharField(max_length=150, default="")
    status = models.BooleanField(default=True)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    updated_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.smtp_host)

    class Meta:
        verbose_name_plural = "Email Setting"



# ________________________________________Model for Social Settings______________________________________________________
class SocialKeys(models.Model):
    social_type = models.CharField(max_length=150, default="")
    key = models.CharField(max_length=500, default="")
    secret_key = models.CharField(max_length=500, default="")
    updated_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.social_type)
