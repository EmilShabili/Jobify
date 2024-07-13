from django.utils.text import slugify


class Uploader:

    @staticmethod
    def upload_profile_photo(instance, filename):
        return f"users/{instance.user.fullname()}/{filename}"

    @staticmethod
    def upload_background_image(instance, filename):
        return f"profiles/background/{slugify(instance.user.fullname())}/{filename}"


class JobUploader:
    @staticmethod
    def upload_profile_photo(instance, filename):
        return f"companies/{slugify(instance.company_name)}/{filename}"

    @staticmethod
    def upload_background_image(instance, filename):
        return f"companies/background/{slugify(instance.company_name)}/{filename}"


class NotificationUploader:

    @staticmethod
    def notification_logo(instance, filename):
        return f"notification/{slugify(instance.title)}/{filename}"

