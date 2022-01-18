from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.conf import settings


class SetupMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_request(request, response)

    def process_request(self, request, response):
        if not request.is_ajax():
            from aurora.frontend.models import Configuration
            try:
                configuration = Configuration.objects.get(site=request.site)
            except Configuration.DoesNotExist:
                configuration = None
            if not configuration:
                url_match = request.resolver_match
                if url_match:
                    if not url_match.url_name in ['frontend_configuration_add', 'frontend_configuration_change', 'login']:
                        messages.info(request, f"{_('Please configure Frontend for this site')} -> {request.site}")
                        return redirect('admin:frontend_configuration_add')
        return response
