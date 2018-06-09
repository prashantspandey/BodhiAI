from Private_Messages.models import *
from rest_framework import serializers


class PrivateMessageModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = [
            'sender',
            'receiver',
            'subject',
            'body',
            'sent_date',

        ]
