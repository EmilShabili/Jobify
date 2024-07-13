import django_filters
from ..models import Job, Experience,WorkerLevel,Skills
from django_countries import countries
from profiles.models import EmploymentType


class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    salary = django_filters.RangeFilter(field_name="offer_salary", )
    experience = django_filters.ModelChoiceFilter(field_name="experience", queryset=Experience.objects.all())
    location = django_filters.ChoiceFilter(field_name="location", choices=countries)
    employment_type = django_filters.ModelChoiceFilter(field_name="employment_type",queryset=EmploymentType.objects.all())
    worker_level = django_filters.ModelChoiceFilter(field_name="worker_level", queryset=WorkerLevel.objects.all())
    skills = django_filters.ModelMultipleChoiceFilter(field_name='skills', queryset=Skills.objects.all())
    class Meta:
        model = Job
        fields = (
            "search",
            "salary",
            "skills",
            "location",
            "experience",
            "worker_level",
            "employment_type",
        )
