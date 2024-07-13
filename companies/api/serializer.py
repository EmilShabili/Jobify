from rest_framework import serializers
from ..models import Job, Experience, WorkerLevel, JobProposal, JobSaved
from profiles.models import EmploymentType
from datetime import datetime
from profiles.models import Skills
from pytz import timezone as tz


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ("name",)


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ("type",)


class WorkerLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerLevel
        fields = ("name",)


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ("name",)


class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "id",
            "profile_photo",
            "title",
            "job_description",
            "location",
            "offer_salary",
        )

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        if instance.skills.all():
            repr_["skills"] = SkillsSerializer(instance.skills.all(), many=True).data

        return repr_


class JobSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "background_image",
            "profile_photo",
            "title",
            "company_name",
            "location",
            'day',
            "experience",
            "worker_level",
            "employment_type",
            "offer_salary",
            "job_description",
            "requirements",
            "skills",
        )
        extra_kwargs = {
            "experience": {"write_only": True}
        }

    def get_day(self, obj):
        date = datetime.now().replace(tzinfo=tz('UTC')) - obj.created_at.replace(tzinfo=tz('UTC'))

        return date.days

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        if instance.skills.all():
            repr_["skills"] = SkillsSerializer(instance.skills.all(), many=True).data
        repr_["experience"] = ExperienceSerializer(instance.experience).data
        repr_["worker_level"] = WorkerLevelSerializer(instance.worker_level).data
        repr_["employment_type"] = EmploymentTypeSerializer(instance.employment_type).data
        return repr_


class JobProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposal
        exclude = ("user",
                   "id",
                   "updated_at",
                   )
        extra_kwargs = {
            "user": {"read_only": True},
            "job": {"write_only": True}
        }


class JobProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("profile_photo",
                  )


class ApplicationSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    day = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobProposal
        fields = (
            "title",
            "description",
            'day',
        )

    def get_title(self, obj):
        return obj.job.title

    def get_description(self, obj):
        return obj.job.job_description

    def get_day(self, obj):
        date = datetime.now().replace(tzinfo=tz('UTC')) - obj.created_at.replace(tzinfo=tz('UTC'))
        return date.days

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["profile_photo"] = JobProfilePhotoSerializer(instance.job.profile_photo).data
        return repr_


class JobSavedSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    salary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobSaved
        fields = ("job",
                  "title",
                  "description",
                  "skills",
                  "salary",
                  )

    def get_title(self, obj):
        return obj.job.title

    def get_description(self, obj):
        return obj.job.job_description

    def get_skills(self, obj):
        return SkillsSerializer(obj.job.skills.all(), many=True).data

    def get_salary(self, obj):
        return obj.job.offer_salary
