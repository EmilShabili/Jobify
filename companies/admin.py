from django.contrib import admin
from .models import WorkerLevel, Job,Experience,JobProposal,JobSaved

admin.site.register(Experience)
admin.site.register(WorkerLevel)
admin.site.register(Job)
admin.site.register(JobProposal)
admin.site.register(JobSaved)
