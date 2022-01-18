from dal import autocomplete
from django.http import Http404


class BaseQueryAC(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        # for security, avoid direct access to autocomplete
        if not 'Sec-Fetch-Site' in request.headers:
            raise Http404()
        sfs = request.headers.get('Sec-Fetch-Site')
        if not sfs == 'same-origin':
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
