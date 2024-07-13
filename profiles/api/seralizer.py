from ..models import (
    Skills, EmploymentType, Education, Experience, Certifications, Profile)
from rest_framework import serializers


class SkillsSerializerProfile(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ("name",)


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ("type",)


class EducationSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Education
        fields = (
            "id",
            "school_name",
            "degree",
            "field_of_study",
            "grade",
            "info",
            "start_date",
            "end_date",
            "is_studying",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "degree": {"write_only": True},
            "field_of_study": {"write_only": True},
            "grade": {"write_only": True},
        }

    def get_info(self, obj):
        return f"{obj.degree} - {obj.field_of_study}"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "id",
            "work_title",
            "employment_type",
            "company_name",
            "location",
            "start_date",
            "end_date",
            "is_working",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "location": {"write_only": True},
            "employment_type": {"write_only": True}
        }

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["employment_type"] = EmploymentTypeSerializer(instance.employment_type).data
        return repr_


class CertificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certifications
        fields = (
            "id",
            "certification_name",
            "published_by",
            "location",
            "start_date",
            "end_date",
            "expiration_date",
            "upload_cv_or_project",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "location": {"write_only": True},
            "upload_cv_or_project": {"write_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "profile_photo",
            "background_image",
            "fullname",
            "address",
            "portfolio_link",
            "bio",
        )

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        experience = ExperienceSerializer(instance.user.experience_set.all(), many=True).data
        education = EducationSerializer(instance.user.education_set.all(), many=True).data
        certifications = CertificationsSerializer(instance.user.certifications_set.all(), many=True).data
        skills = SkillsSerializerProfile(instance.skills.all(), many=True).data
        repr_["experience"] = experience
        repr_["education"] = education
        repr_["certifications"] = certifications
        repr_["skills"] = skills
        return repr_


class ProfileEditSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "background_image",
            "profile_photo",
            "first_name",
            "last_name",
            "bio",
            "headline",
            "portfolio_link",
            "gender",
            "birth_place",
            "date_of_brith",
            "address",
            "zip_code",
            "detail_address",
            "identity_type",
            "identity_number",
            "fullname",
        )

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"
