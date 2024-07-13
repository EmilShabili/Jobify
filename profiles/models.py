from django.db import models
from ckeditor.fields import RichTextField
from services.choices import GENDER_CHOICES, identity_type, academic_degree
from django_countries.fields import CountryField
from mptt.models import MPTTModel, TreeForeignKey
from services.mixin import DateMixin
from django.contrib.auth import get_user_model
from services.uploader import Uploader

User = get_user_model()


class Country(MPTTModel):
    name = CountryField()
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name


class EmploymentType(MPTTModel):
    type = models.CharField(max_length=30)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.type


class Experience(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_title = models.CharField(max_length=50, blank=True, null=True)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, blank=True, null=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    location = CountryField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_working = models.BooleanField(default=False)

    def __str__(self):
        return self.work_title

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.is_working = True
        else:
            self.is_working = False
        return super(Experience, self).save(*args, **kwargs)


class Education(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=50, blank=True, null=True)
    degree = models.CharField(max_length=20, choices=academic_degree, blank=True, null=True)
    field_of_study = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_studying = models.BooleanField(default=False)

    def __str__(self):
        return self.school_name

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.is_studying = True
        else:
            self.is_studying = False
        return super(Education, self).save(*args, **kwargs)


class Certifications(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=50, blank=True, null=True)
    published_by = models.CharField(max_length=50, blank=True, null=True)
    location = CountryField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    upload_cv_or_project = models.FileField(blank=True, null=True)
    expiration_date = models.BooleanField(default=False)

    def __str__(self):
        return self.certification_name

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.expiration_date = False
        else:
            self.expiration_date = True
        return super(Certifications, self).save(*args, **kwargs)


class Skills(DateMixin):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(DateMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to=Uploader.upload_profile_photo, blank=True, null=True)
    background_image = models.ImageField(upload_to=Uploader.upload_background_image, blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    skills = models.ManyToManyField(Skills, blank=True)
    identity_type = models.CharField(choices=identity_type, max_length=20, blank=True, null=True)
    identity_number = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    birth_place = CountryField(blank=True, null=True)
    date_of_brith = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    address = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    profile_viewed_count = models.PositiveBigIntegerField(default=0, editable=False)

    def __str__(self):
        return self.user.fullname()
