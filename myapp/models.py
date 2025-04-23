from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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
    face_image = models.ImageField(upload_to='face_images/', null=True, blank=True)

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
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)  # Field for the certificate

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
class HomeCollection(models.Model):
    location = models.CharField(max_length=255)  # Location field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HomeCollection at {self.location}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('collected', 'Collected'),
        ('test done', 'Test Done'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    test = models.ForeignKey(TestName, on_delete=models.CASCADE)
    test_types = models.ManyToManyField(TestType, related_name='bookings')
    home_collection = models.ForeignKey(
        HomeCollection,
        on_delete=models.SET_NULL,  # Allows the reference to be null if no home collection is involved
        null=True,
        blank=True,
        related_name='bookings'
    )





    def __str__(self):
        return f"Booking for {self.user} on {self.appointment_date} at {self.appointment_time}"
class Amount(models.Model):
    amount_id = models.AutoField(primary_key=True)  # Primary key, auto-increment
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)  # Foreign key referencing TestType
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount to be paid

    def __str__(self):
        return f"Amount for {self.test_type} - {self.amount}"
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)  # Primary key, auto-increment
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)  # Foreign key referencing Booking
    amount = models.ForeignKey(Amount, on_delete=models.CASCADE)  # Foreign key referencing Amount
    payment_date = models.DateField()  # Date of payment
    status = models.CharField(max_length=50)  # Status of the payment (e.g., completed, pending, failed)

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking.id} - Status: {self.status}"
class LabTechnicianSchedule(models.Model):
    technician = models.ForeignKey(LabTechnician, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    def __str__(self):
        return f'Schedule for {self.technician} for Booking ID: {self.booking.id}'
class Notification(models.Model):
    lab_technician = models.ForeignKey(LabTechnician, on_delete=models.CASCADE, related_name='notifications')  # Foreign key to LabTechnician
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
class CollectionStatus(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)  # Foreign key to Booking
    technician = models.ForeignKey(LabTechnician, on_delete=models.SET_NULL, null=True)  # Foreign key to LabTechnician
    is_collected = models.BooleanField(default=False)

    def __str__(self):
        return f"Collection Status for Booking ID {self.booking.id}: {'Collected' if self.is_collected else 'Not Collected'} by Technician ID: {self.technician.labtech_id if self.technician else 'N/A'}"
class TestResult(models.Model):
    result_id = models.AutoField(primary_key=True)  # Primary key, auto-increment
    collection_status = models.ForeignKey(CollectionStatus, on_delete=models.CASCADE)  # Foreign key to CollectionStatus
    test_types = models.ManyToManyField(TestType, related_name='test_results')  # Many-to-many relationship with TestType

    def __str__(self):
        return f"Test Result ID: {self.result_id} for Collection ID: {self.collection_status.id}"

class TestValue(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='values')  # Link to TestResult
    result_value = models.CharField(max_length=255)  # Result value as varchar

    def __str__(self):
        return f"Result Value: {self.result_value} for Test Result ID: {self.test_result.result_id}"
