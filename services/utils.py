from companies.models import JobProposal
from django.db.models.functions import TruncDay, Cast
from django.db.models import CharField
from django.utils import timezone


# fuad muellimin qaytaradigi date responsene uygun date filter etmek
# def get_statistic_data(user):
#     qs = JobProposal.objects.annotate()
#     all_application = qs.filter(user=user).count()
#     interview_count = qs.filter(user=user, status="Interviews").count()
#     return {
#         "Application Sent": all_application,
#         "Interview": interview_count,
#     }
#
#
# def get_statistic_data(user, start_date=None, end_date=None):
#     qs = JobProposal.objects.annotate() #created at bunun icinde deyisecem
#     if start_date and end_date:
#         qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
#
#     all_application = qs.filter(user=user).count()
#     interview_count = qs.filter(user=user, status="Interviews").count()
#
#     return {
#         "Application Sent": all_application,
#         "Interview": interview_count,
#     }































from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from django.db.models import DateField


def get_new_test(data):
    application_sent = JobProposal.objects.annotate(date=TruncDay("created_at", output_field=DateField())).filter(
        user=data.user
    ).order_by("date")
    interview_applications = JobProposal.objects.annotate(date=TruncDay("updated_at", output_field=DateField())).filter(
        user=data.user, status="Interviews"
    ).order_by("date")

    if "from_date" in data.GET and data.GET.get("from_date"):
        from_date = data.GET.get("from_date")
        application_sent = application_sent.filter(date__gte=from_date)
        interview_applications = interview_applications.filter(date__gte=from_date)

    labels = [date.strftime("%d.%m.%Y") for date in application_sent.values_list("date", flat=True)]
    interview_count = application_sent.count()
    application_sent_count = interview_applications.count()

    return labels, interview_count, application_sent_count


# def get_application_sent(data):
#     get_application_count = JobProposal.objects.filter(user=data.user).count()
#     return get_application_count













