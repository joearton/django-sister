from django.utils.translation import gettext as _
from django.utils.text import Truncator
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html, mark_safe
from django.utils.http import urlquote


class HTMLUI:
    
    def __init__(self):
        pass

    def button(self, href, label, accent='primary', size='', icon=None, target='self', css_class=''):
        if icon:
            icon = f'<i class="fa fa-{icon}"></i>'
        html = f'<a class="btn {size} btn-{accent} {css_class}" href="{href}" target="_{target}">{icon} {label}</a>'
        return html
        

    def button_sm(self, href, label, accent='primary', icon=None, target='self', css_class=''):
        return self.button(href, label, accent, 'btn-sm', icon, target, css_class)


    def button_lg(self, href, label, accent='primary', icon=None, target='self', css_class=''):
        return self.button(href, label, accent, 'btn-lg', icon, target, css_class)


    def link(self, href, label, css_class='', target='self'):
        html = f'<a class="{css_class}" href="{href}" target="_{target}">{label}</a>'
        return html


    def div(self, *args, css_class=''):
        content = ''
        for arg in args:
            content += arg + ' '
        html = f'<div class="{css_class}">{content}</div>'
        return html


    def pdf_viewer(self, url, label=_('View'), css_class=''):
        if url == '#':
            return self.badge(_('File Not Found'), 'warning')
        return format_html(
            '<a class="{}" href="{}?url={}" target="_blank">{}</a>',
            css_class, reverse('aurora.pilar.pdfviewer'),
            url, mark_safe(label))


    def pdf_viewer_block(self, url, label=_('View')):
        response = self.pdf_viewer(url, label)
        return format_html("<div>{}</div>", response)


    def pdf_viewer_img(self, url, link_class='', img_class=''):
        return format_html(
            '<a class="{}" href="{}?url={}" target="_blank"><img class="{}" src="{}" alt="img" /></a>',
            link_class, reverse('aurora.pilar.pdfviewer'), url, img_class, url)


    def badge(self, text, level='info'):
        return format_html('<span class="badge bg-{}">{}</span>', level, mark_safe(text))


    def badge_block(self, text, level='info'):
        return format_html('<div><span class="badge badge-{}">{}</span></div>', level, mark_safe(text))


    def divs(self, text, class_name='divs'):
        return format_html('<div class="{}">{}</div>', class_name, mark_safe(text))


    def span(self, text, class_name='span'):
        return format_html('<span class="{}">{}</span>', class_name, mark_safe(text))


    def a(self, text, link, css_class='', target="_self", icon=False):
        html = '<a href="{link}" class="{css_class}" target="{target}">{text}</a>'
        if icon:
            html = '<a href="{link}" class="{css_class}" target="{target}"><i class="{icon}"></i> {text}</a>'
            return format_html(html, link=link, css_class=css_class, text=text, target=target, icon=icon)
        return format_html(html, link=link, css_class=css_class, text=text, target=target)


    def button_a(self, text, link, css_class='btn-primary', target="_self", icon=False):
        html = '<a href="{link}" class="btn btn-{css_class}" target="{target}">{text}</a>'
        if icon:
            html = '<a href="{link}" class="btn {css_class}" target="{target}"><i class="{icon}"></i> {text}</a>'
            return format_html(html, link=link, css_class=css_class, text=text, target=target, icon=icon)
        return format_html(html, link=link, css_class=css_class, text=text, target=target)


    def progress_bar(self, label='', percent='', bg='info', thin='1rem'):
        if percent <= 0:
            label = ""
        html = f'\
        <div class="progress" style="height: {thin};" title="{label}" >\
            <div class="progress-bar bg-{bg} small" role="progressbar" style="width:{percent}%;" aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100">\
                <div class="p-1">{label}</div>\
            </div>\
        </div>'
        return format_html(html)


    def alert(self, text, level='info'):
        return format_html('<div class="alert alert-{}">{}</div>', level, mark_safe(text))


    def mobile_number_features(self, mobile_number, target=""):
        if not mobile_number:
            return format_html('<a class="btn btn-warning btn-sm btn-disable" href="#">- kosong -</a>')
        target = urlquote(target)
        output = f'\
        <div class="btn-group" role="group">\
            <button id="btn-group-mobile_number" type="button" class="btn btn-success btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">\
                <i class="fab fa-whatsapp"></i> {mobile_number}\
            </button>\
            <div class="dropdown-menu" aria-labelledby="btn-group-mobile_number">\
                <a class="dropdown-item d-none d-md-block" href="https://api.whatsapp.com/send?phone={mobile_number[1:]}&text={target}" target="_blank">{_("Send WhatsApp")}</a>\
                <a class="dropdown-item d-md-none" href="https://wa.me/{mobile_number[1:]}?text={target}" target="_blank">{_("Send WhatsApp")}</a>\
                <a class="dropdown-item" href="tel:{mobile_number}" target="_blank">{_("Call")}</a>\
                <a class="dropdown-item" href="sms:{mobile_number}" target="_blank">{_("Send SMS")}</a>\
            </div>\
        </div>'
        return format_html(output)

