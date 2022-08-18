from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import os


# Create your models here.

# sex_choice = (
#     ('Male', 'Male'),
#     ('Female', 'Female')
# )

class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    mark = (
        ('Absent', 'Absent'),
        ('Present', 'Present'),
    )
    attendance = models.CharField(max_length=20, default='Absent', choices=mark)
    profile_pic = models.ImageField(default="static/img/nobody.jpg", upload_to='images')

    # contact_number = models.CharField(max_length=50)
    # date_of_birth = models.CharField(max_length=50)
    # date_of_joining = models.CharField(max_length=50)
    # department = models.CharField(max_length=50)
    # designation = models.CharField(max_length=50)
    # gender = models.CharField(max_length=50, choices=sex_choice, default='Male')
    # team = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def num_photos(self):
        try:
            DIR = f"app/facerec/dataset/{self.name}_{self.id}"
            img_count = len(os.listdir(DIR))
            return img_count
        except:
            return 0


class Detected(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    time_stamp = models.DateTimeField()
    photo = models.ImageField(upload_to='detected/', default='app/static/img/nobody.jpg')

    def __str__(self):
        emp = Employee.objects.get(name=self.emp_id)
        # return f"{emp.name} {self.time_stamp}"
        return emp.name

        

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description
