from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        blank=True,
        choices=GENDER_CHOICES
    )
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)  # Ensure email is unique
    role = models.IntegerField(default=0)
    from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    lad_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profiles')
    city = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    license_no = models.CharField(max_length=255)
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.city}'
    # myapp/models.py

from django.db import models
from django.conf import settings

class LabTechnician(models.Model):
    labtech_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_technicians')
    specialization = models.CharField(max_length=255)
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.specialization}'

class TestName(models.Model):
    name_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=50)
    lad_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_name

class Tests(models.Model):
    test_id = models.AutoField(primary_key=True)
    name_id = models.ForeignKey(TestName, on_delete=models.CASCADE)
    test_type_names = models.CharField(max_length=300)
    

    def __str__(self):
        return self.test_type_names
class TestType(models.Model):
    testtype_id = models.AutoField(primary_key=True)
    test_id = models.ForeignKey(Tests, on_delete=models.CASCADE)
    tests_names = models.CharField(max_length=300)
    normal_range = models.CharField(max_length=100)

    def __str__(self):
        return self.tests_names

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking with {self.user} on {self.appointment_date}"

