from django.db import models
from services.mixin import DateMixin
from django.contrib.auth import get_user_model
from services.uploader import NotificationUploader

User = get_user_model()


class Notification(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    logo = models.ImageField(upload_to=NotificationUploader.notification_logo, blank=True, null=True)

    def __str__(self):
        return self.title
