from .serializer import JobSerializer, JobListSerializer, JobProposalSerializer, JobSavedSerializer, SkillsSerializer,ApplicationSerializer
from ..models import Job, JobProposal, JobSaved
from profiles.models import Skills
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
from rest_framework.response import Response


class SkillsListView(generics.ListAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer


class SkillsCreateView(generics.CreateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        obj, created = Skills.objects.get_or_create(
            name=request.data.get("name")
        )
        serializer = self.serializer_class(obj).data
        return Response(serializer)


class SkillsDeleteView(generics.DestroyAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class SkillsUpdateView(generics.UpdateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class JobListView(generics.ListAPIView):
    queryset = Job.objects.order_by("-created_at")
    serializer_class = JobListSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = JobFilter
    ordering_fields = ("title", "offer_salary", "created_at")


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = "id"


class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class JobProposalView(generics.CreateAPIView):
    queryset = JobProposal.objects.all()
    serializer_class = JobProposalSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ApplicationView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, ):
        user = self.request.user
        return JobProposal.objects.filter(user=user)


class JobSavedListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, ):
        user = self.request.user
        saved_jobs = JobSaved.objects.filter(user=user).values_list("job_id", flat=True)
        return Job.objects.filter(id__in=saved_jobs)


class JobSavedCreateView(generics.CreateAPIView):
    queryset = JobSaved.objects.all()
    serializer_class = JobSavedSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        job = Job.objects.get(id=request.data.get("job"))
        obj, created = JobSaved.objects.get_or_create(user=request.user, job=job)
        if not created:
            obj.delete()
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


