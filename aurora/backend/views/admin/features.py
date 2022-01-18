import json
import csv
from django.http import HttpResponse
from django.utils.translation import gettext as _


class AdminFeatures:

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response, dialect='excel')
        writer.writerow(field_names)
        for obj in queryset:
            columns = []
            for field in field_names:
                data = '{0}'.format(getattr(obj, field))
                columns.append(data)
            row = writer.writerow(columns)
        return response

    export_as_csv.short_description = _("Download as CSV")
