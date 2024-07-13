from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("application-sent-count/", views.ApplicationSentView.as_view(), name='application-sent-count'),
    path("vacancy-statics/", views.VacancyStaticsView.as_view(), name="vacancy-statics"),
    path("notifications/", views.NotificationListView.as_view(), name='notifications'),
    path("notifications/mark-all-as-read/", views.MarkAllAsReadView.as_view(), name='mark-all-as-read'),
    path("profile/view-count/", views.ProfileViewCount.as_view(), name="profile-view-count"),
    path("profile/dashboard/", views.ProfileDashboardView.as_view(), name="profile-dashboard"),
]
