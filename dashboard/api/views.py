from ..models import Notification
from .serializer import NotificationSerializer, ProfileViewCountSerializer, ProfileDashboardSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from companies.models import JobProposal
from profiles.models import Profile
from services.utils import get_new_test


class ApplicationSentView(generics.GenericAPIView):

    def get(self, *args, **kwargs):
        application_sent_count = JobProposal.objects.filter(user=self.request.user).count()
        context = {
            "application_sent_count": application_sent_count,
        }
        return Response(context)


class ProfileViewCount(generics.ListAPIView):
    serializer_class = ProfileViewCountSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by("-created_at")


class MarkAllAsReadView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        qs = request.user.notification_set.filter(is_read=False).update(is_read=True)
        return Response({})


class VacancyStaticsView(generics.GenericAPIView):
    permission_classes = IsAuthenticated,

    def get(self, *args, **kwargs):
        test = get_new_test(self.request)
        context = {
            "labels": test[0],
            "interview_count": test[1],
            "sent_count": test[2]
        }
        print(context)
        return Response(context)


class ProfileDashboardView(generics.RetrieveAPIView):
    serializer_class = ProfileDashboardSerializer

    def get_object(self):
        return self.request.user
