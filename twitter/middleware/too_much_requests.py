from tw_auth.models import Request
from django.contrib.auth import authenticate

from django.utils.timezone import now


class HandleTooMuchRequests:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META['REMOTE_ADDR']
        browser = request.META['HTTP_USER_AGENT']
        current_time = now()

        Request.objects.create(ip_addr=ip_address, browser=browser, created_at=current_time)

        h = 2
        n = 5

        # user_requests = Request.objects.filter(user=user).order_by('-created_at')[:n]
        # if (user_requests[0].created_at - user_requests[n-1].created_at).total_seconds() < h:
        #     print('Warning!!!\nSeems user %s is doing a DDOS Attack!' % user)

        ip_requests = Request.objects.filter(ip_addr=ip_address).order_by('-created_at')[:n]
        if (ip_requests[0].created_at - ip_requests[n - 1].created_at).total_seconds() < h:
            print('Warning!!!\nSeems ip %s is doing a DDOS Attack!' % ip_address)

        unauthorized_ip_requests = Request.objects.filter().order_by('-created_at')[:4*n]

        is_brute_force = False

        if len(unauthorized_ip_requests) == 4*n:
            is_brute_force = True

            for i in range(n):
                if not unauthorized_ip_requests[4 * i + 2].unauthorized:
                    is_brute_force = False

        if is_brute_force:
            print('Warning!!!\nSeems ip %s is doing a Brute Force Attack!' % ip_address)

        return self.get_response(request)
