from django.contrib.admin.decorators import display
from django.contrib.auth.models import Group
from django.urls.base import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import admin, messages
from django.contrib.auth import login, logout
from django.urls import path, reverse
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.html import format_html, mark_safe
from aurora.backend.library import groups
from aurora.backend.models import User, UserProperty
from aurora.backend.views.admin.features import AdminFeatures
from aurora.backend.views.auth import DefaultDashboardView
from django.conf import settings
from aurora.backend.views.auth.activation import shared_activate_user
from aurora.backend.views.admin import backend
from aurora.backend.library.ui.html import HTMLUI


ui = HTMLUI()


class backendAdmin(admin.ModelAdmin, AdminFeatures):
    actions = ["export_as_csv"]
    

class UserPropertyInline(admin.StackedInline):
    model = UserProperty


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(UserAdmin, AdminFeatures, DefaultDashboardView):
    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['fullname', 'group', 'is_staff', 'last_login']
    inlines = (UserPropertyInline, )
    actions = ['activate_user']

    def fullname(self, obj):
        text_color = "text-dark small"
        if not obj.is_active:
            text_color = "text-secondary small"
        username = obj.username
        fullname = obj.get_full_name()
        if fullname:
            username += ' ({0}) '.format(fullname)
        return format_html('{} {}',
            ui.divs('{0}'.format(obj.email), text_color),
            ui.divs('{0}'.format(username), 'text-primary'),
        )
    fullname.short_description = _('Account')


    def group(self, obj):
        html = ''
        group_list = obj.groups.all()
        if obj.is_superuser:
            html = ui.badge_block(_('SUPER USER'), 'success')
        else:
            if group_list:
                for i in group_list:
                    bg_color = 'light'
                    if hasattr(i, 'get_group_color'):
                        bg_color = i.get_group_color()
                    html += ui.badge_block(i.name.upper(), bg_color)
            else:
                html = ui.badge_block(_('NO GROUP'), 'dark')
        return format_html(html)
    group.short_description = _('Group')


    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.is_superuser:
            if not 'signin_as' in list_display:
                list_display.append('signin_as')
        return list_display


    def signin_as(self, obj):
        return format_html(
            "<a href='signin_as/{0}' class='btn btn-info btn-sm'><i class='fa fa-user'></i></a>", obj.pk
        )


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('signin_as/<int:pk>', self.admin_site.admin_view(self.signin_as_user), name='admin.signin_as'),
        ]
        return my_urls + urls


    def signin_as_user(self, request, pk):
        if request.user.is_superuser:
            previous_user = request.user.pk
            user = User.objects.get(pk = pk)
            logout(request)
            login(request, user)
            request.session['previous_signin_in'] = previous_user
            messages.info(request, _('You are signed in as ') + user.get_full_name())
            return self.go_to_dashboard(request)
        if not request.user.is_staff:
            messages.info(request, _('Signed out, you are not authorized to use the system'))
        return redirect('admin:index')


    def activate_user(self, request, queryset):
        if queryset:
            for obj in queryset:
                shared_activate_user(request, obj)
            messages.info(request, _("User activation successful"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    activate_user.short_description = _("Activate User")



admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(GroupAdmin, AdminFeatures, DefaultDashboardView):
    list_display = ['name', 'table_access', 'users_count']

    @display(description=_('Accessibility'))
    def table_access(self, obj):
        permissions = obj.permissions.all()
        responses = {}
        for permission in permissions:
            app_label = permission.content_type.app_label
            code_name = permission.codename
            if not app_label in responses:
                responses[app_label] = []
            responses[app_label].append(code_name)
        output, counter = '', 0
        if responses:
            for app_label, actions in responses.items():
                output += f"{app_label} ({len(actions)})"
                if counter != len(responses.items()) - 1:
                    output += " | "
                if counter != 0 and counter % 7 == 0:
                    output += "<br/>"
                counter += 1        
        return format_html(output)


    @display(description=_('User Counts'))
    def users_count(self, obj):
        return obj.user_set.count()


