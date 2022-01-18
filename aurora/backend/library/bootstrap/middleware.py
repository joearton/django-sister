from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.conf import settings


# Every middleware class name must be endswith Middleware

class MediaMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_request(request, response)

    def process_request(self, request, response):
        if request.path.startswith(settings.MEDIA_URL + 'private'):
            if not request.user.is_authenticated:
                raise Http404()
            url_split = request.path.split('/')
            if len(url_split) >= 2:
                private_media = url_split[2]
                # media_server(request, private_media)
        return response



class MaintenanceMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.maintenance_path = '/' + settings.BACKEND_SETTINGS['maintenance_path']

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_request(request, response)

    def process_request(self, request, response):
        if settings.MAINTENANCE:
            if not request.path == self.maintenance_path:
                return redirect(self.maintenance_path)
        return response

