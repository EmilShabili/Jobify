from django.db import models
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from services.mixin import DateMixin
from services.uploader import JobUploader
from django.contrib.auth import get_user_model
from profiles.models import Skills
from services.choices import status

User = get_user_model()


class WorkerLevel(MPTTModel):
    name = models.CharField(max_length=30)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.name


class Experience(DateMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background_image = models.ImageField(upload_to=JobUploader.upload_background_image, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=JobUploader.upload_profile_photo, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = CountryField(blank=True, null=True)
    experience = models.ForeignKey(Experience, on_delete=models.SET_NULL, blank=True, null=True)
    worker_level = models.ForeignKey(WorkerLevel, on_delete=models.SET_NULL, blank=True, null=True)
    employment_type = models.ForeignKey("profiles.EmploymentType", on_delete=models.SET_NULL, blank=True, null=True)
    offer_salary = models.PositiveIntegerField(blank=True, null=True)
    job_description = models.CharField(max_length=250, blank=True, null=True)
    requirements = RichTextField(blank=True, null=True)
    skills = models.ManyToManyField(Skills, blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.title}"


class JobProposal(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    work_position = models.CharField(max_length=100)
    portfolio = models.URLField(blank=True, null=True)
    bid = models.PositiveIntegerField()
    project_duration = models.CharField(max_length=50, blank=True, null=True)
    upload_cv_or_project = models.FileField()
    status = models.CharField(max_length=30, choices=status, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.work_position}"


class JobSaved(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.job}"


