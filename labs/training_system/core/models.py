from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Employee(models.Model):
    employee_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['employee_code']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code})"

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=30)
    attendees = models.ManyToManyField(
        Employee,
        through='TrainingRecord',
        related_name='enrolled_courses'
    )
    class Meta:
        ordering = ['code']

        def __str__(self):
            return f"{self.code}: {self.title}"

class TrainingRecord(models.Model):
    STATUS_CHOICES = [
        ('REGISTERED', 'Registered'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='training_records'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='training_records'
    )
    enrollment_date = models.DateField(auto_now_add=True)
    completion_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REGISTERED'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    class Meta:
        ordering = ['-enrollment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'course'],
                name='unique_employee_course_enrollment'
            )
        ]

    def __str__(self):
        return f"{self.employee.employee_code} - {self.course.code} [{self.completion_status}]"
