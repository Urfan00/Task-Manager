from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay
from .models import MemberTaskStatistic

def base_data(request):
    data = {}

    # Retrieve MemberTaskStatistic instances for the current user (you might need to adjust this part)
    if request.user.is_authenticated:
        user = request.user
        member_task_statistics = MemberTaskStatistic.objects.filter(member=user)

        # Group data by day of the week and calculate the sum of sent_task_count for each day
        daily_sent_task_counts = member_task_statistics.annotate(
            day_of_week=ExtractWeekDay('created_at')
        ).values('day_of_week').annotate(total_sent_task_count=Sum('sent_task_count'))

        # Create a list to store sent_task_count values for each day of the week
        sent_task_counts = [0] * 7  # Initialize with zeros for each day of the week

        # Update the list with the calculated values
        for entry in daily_sent_task_counts:
            day_of_week = entry['day_of_week']
            sent_task_counts[day_of_week - 1] = entry['total_sent_task_count']

        # Add the extracted data to the 'data' dictionary
        data['sent_task_counts'] = sent_task_counts

    return data
