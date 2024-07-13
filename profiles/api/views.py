from .seralizer import (
    ProfileEditSerializer, ProfileSerializer, ExperienceSerializer, EducationSerializer, CertificationsSerializer,
    SkillsSerializerProfile
)
from ..models import Profile, Experience, Education, Certifications, Skills
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response


class SkillsCreateView(generics.CreateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializerProfile
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        obj, created = Skills.objects.get_or_create(
            name=request.data.get("name")
        )
        if not obj in user.profile.skills.all():
            user.profile.skills.add(obj)
        serializer = self.serializer_class(obj).data
        return Response(serializer)


class SkillsDeleteView(generics.DestroyAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializerProfile
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_destroy(self, instance):
        user = self.request.user
        if instance in user.profile.skills.all():
            user.profile.skills.remove(instance)
        return instance


class SkillsUpdateView(generics.UpdateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializerProfile
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceCreateView(generics.CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceUpdateView(generics.UpdateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceDeleteView(generics.DestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class EducationCreateView(generics.CreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class EducationUpdateView(generics.UpdateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class EducationDeleteView(generics.DestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class CertificationCreateView(generics.CreateAPIView):
    queryset = Certifications.objects.all()
    serializer_class = CertificationsSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CertificationUpdateView(generics.UpdateAPIView):
    queryset = Certifications.objects.all()
    serializer_class = CertificationsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CertificationDeleteView(generics.DestroyAPIView):
    queryset = Certifications.objects.all()
    serializer_class = CertificationsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class MyProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)


class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        id_ = self.kwargs.get(self.lookup_field)
        return Profile.objects.get(id=id_)

    def get(self, request, id):
        profile = self.get_object()
        if request.user != profile.user:
            profile.profile_viewed_count += 1
            profile.save()
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileEditView(generics.UpdateAPIView):
    serializer_class = ProfileEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.profile
