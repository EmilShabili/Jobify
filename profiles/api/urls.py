from django.urls import path
from . import views

app_name = "profile_app"

urlpatterns = [
    path('experience/', views.ExperienceCreateView.as_view(), name='create-experience'),
    path('experience/update/<id>/', views.ExperienceUpdateView.as_view(), name='update-experience'),
    path('experience/delete/<id>/', views.ExperienceDeleteView.as_view(), name='delete-experience'),
    path('education/', views.EducationCreateView.as_view(), name='create-education'),
    path('education/update/<id>/', views.EducationUpdateView.as_view(), name='update-education'),
    path('education/delete/<id>/', views.EducationDeleteView.as_view(), name='delete-education'),
    path('certification/', views.CertificationCreateView.as_view(), name='create-certification'),
    path('certification/update/<id>/', views.CertificationUpdateView.as_view(), name='update-certification'),
    path('certification/delete/<id>/', views.CertificationDeleteView.as_view(), name='delete-certification'),
    path('skills/', views.SkillsCreateView.as_view(), name='create-skills'),
    path('skills/update/<id>/', views.SkillsUpdateView.as_view(), name='update-skills'),
    path('skills/delete/<id>/', views.SkillsDeleteView.as_view(), name='delete-skills'),
    path('profile/', views.MyProfileView.as_view(), name='profile'),
    path('profile/detail/<id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('update/', views.ProfileEditView.as_view(), name='update'),
]
