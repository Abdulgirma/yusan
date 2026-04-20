from django.db import models


class Student(models.Model):
    DEPARTMENTS = [
        ('ICT', 'Information & Communication Technology'),
        ('CS', 'Computer Science'),
        ('SE', 'Software Engineering'),
        ('CY', 'Cyber Security'),
        ('DM', 'Digital Marketing'),
        ('GD', 'Graphic Design'),
        ('NE', 'Network Engineering'),
        ('WD', 'Web Development'),
    ]

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, choices=DEPARTMENTS)
    password = models.CharField(max_length=200)
    reg_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.reg_number}"

    def get_department_display_name(self):
        return dict(self.DEPARTMENTS).get(self.department, self.department)
