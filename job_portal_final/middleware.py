from django.utils import timezone
import pytz
import requests
from .settings import TIMEZONE_API_TOKEN

# NOTE: timezoneapi autodetects clients ip so this is not required, but incase it does not function as expected try getting client ip manually
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        user_timezone = request.session.get('user_timezone')
        if user_timezone:
            timezone.activate(pytz.timezone(user_timezone))
        else:
            try:
                timezoneapi_response = requests.get('https://timezoneapi.io/api/ip/?token={token}'.format(token=TIMEZONE_API_TOKEN))
                timezoneapi_response.raise_for_status()
                timezoneapi_response_json = timezoneapi_response.json()
                user_timezone = timezoneapi_response_json['data']['timezone']['id']
                request.session['user_timezone'] = user_timezone
                timezone.activate(pytz.timezone(user_timezone))
            except requests.exceptions.HTTPError as e:
                timezone.deactivate()
                print(e)

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response
