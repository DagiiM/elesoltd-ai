from rest_framework import serializers
from datetime import datetime, timezone
from rest_framework import status
from rest_framework.response import Response

class CardNumberField(serializers.CharField):
    def to_representation(self, value):
        # Check if the value is None or an empty string
        if not value:
            return value

        # Format the credit card number with spaces every four digits
        formatted_value = ''
        for i in range(0, len(value), 4):
            formatted_value += value[i:i+4] + ' '

        # Return the formatted value
        return formatted_value.strip()


class ExpirationDateField(serializers.DateField):
    def __init__(self, **kwargs):
        kwargs['format'] = '%m/%Y'  # Set the date format to MM/YYYY
        super().__init__(**kwargs)

    def to_representation(self, value):
        # Return None for null values
        if value is None:
            return None

        # Convert the date to MM/YYYY format
        formatted_date = value.strftime('%m/%Y')
        return formatted_date

class SanitizedDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Return None for null values
        if value is None:
            return None

        # Convert the datetime to UTC and round to the nearest second
        utc_datetime = value.astimezone(timezone.utc)
        rounded_datetime = datetime.utcfromtimestamp(
            round(utc_datetime.timestamp())
        )

        # Convert the datetime to ISO 8601 format
        formatted_datetime = rounded_datetime.isoformat()

        return formatted_datetime

    
def handle_validation_error(e):
    '''errors = {}
    for field, error_list in e.message_dict.items():
        errors[field] = error_list[0]
        '''
    return Response({'errors': e}, status=status.HTTP_400_BAD_REQUEST)

