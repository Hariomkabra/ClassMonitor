from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
from django.conf import settings
import markdown

# Custom User model
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    # Override groups and user_permissions to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='classroom_user_groups',  # Custom related name for User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='classroom_user_permissions',  # Custom related name for User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    name = models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic", blank=True)

    def get_absolute_url(self):
        return reverse('classroom:student_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

# Teacher model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='teacher_profile')
    name = models.CharField(max_length=250)
    subject_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic", blank=True)
    class_students = models.ManyToManyField(Student, through="StudentsInClass", related_name="teachers")

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

# StudentMarks model
class StudentMarks(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='given_marks', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="marks", on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()

    def __str__(self):
        return self.subject_name

# StudentsInClass model
class StudentsInClass(models.Model):
    teacher = models.ForeignKey(Teacher, related_name="classes", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="classrooms", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} in {self.teacher.name}'s class"

    class Meta:
        unique_together = ('teacher', 'student')

# MessageToTeacher model
class MessageToTeacher(models.Model):
    student = models.ForeignKey(Student, related_name='student_messages', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='teacher_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = markdown.markdown(self.message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'message']

# ClassNotice model
class ClassNotice(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='notices', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='notices')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = markdown.markdown(self.message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher', 'message']

# ClassAssignment model
class ClassAssignment(models.Model):
    student = models.ManyToManyField(Student, related_name='assignments')
    teacher = models.ForeignKey(Teacher, related_name='assignments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']

# SubmitAssignment model
class SubmitAssignment(models.Model):
    student = models.ForeignKey(Student, related_name='submitted_assignments', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='submitted_assignments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment, related_name='submissions', on_delete=models.CASCADE)
    submit = models.FileField(upload_to='submissions')

    def __str__(self):
        return "Submitted: " + str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['-created_at']
