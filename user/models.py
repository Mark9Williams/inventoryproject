from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')

    def __str__(self):
        return f'{self.staff.username}-Profile'


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    sur_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)  # Optional field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.sur_name}"


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=255)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    summary = models.TextField()
    diagnosis = models.TextField()

    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.sur_name}"