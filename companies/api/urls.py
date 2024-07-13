from django.urls import path
from . import views

app_name = "companies_app"

urlpatterns = [
    path("jobs/", views.JobListView.as_view(), name='jobs'),
    path("skills/list/", views.SkillsListView.as_view(),name='list-skills'),
    path("skills/", views.SkillsCreateView.as_view(), name='create-skills'),
    path("skills/<id>/", views.SkillsUpdateView.as_view(), name='update-skills'),
    path("skills/delete/<id>/", views.SkillsDeleteView.as_view(), name='delete-skills'),
    path("detail/job/<id>/",views.JobDetailView.as_view(),name='job-detail'),
    path("job/", views.JobCreateView.as_view(), name='job-create'),
    path("update/job/<id>/", views.JobUpdateView.as_view(), name='job-update'),
    path("proposal/",views.JobProposalView.as_view(),name='proposal'),
    path("application/",views.ApplicationView.as_view(),name='application'),
    path("saved/job/list/",views.JobSavedListView.as_view(),name='job-saved'),
    path("save/job/",views.JobSavedCreateView.as_view(),name='save-job'),
]
