import django_filters

from django.contrib.auth import get_user_model
from .models import Message

User  = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Field to filter by the user who sent the message
    # Since a conversation has many participants, we'll filter by the sender.
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    # Fields to filter by a time range (start and end date/time)
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender','sent_at'] # What field(s) on the Message model would link to the sender?
                                        # And what field holds the time?
                                        