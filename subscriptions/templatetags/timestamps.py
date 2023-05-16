import datetime
from django import template

register = template.Library()


@register.simple_tag
def get_data_from_timestamp(psql_timestamp: str):
    timestamp = datetime.datetime.strptime(psql_timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
    return timestamp.strftime('%d-%m-%Y')

