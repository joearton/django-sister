from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post, Files
from aurora.frontend.views import frontendView
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings


def transfer_file(request, media):
    if media.meta:
        # menyimpan data jumlah pengunjung
        if 'view_count' in media.meta:
            prev_count = media.meta['view_count']
            media.meta = {'view_count': prev_count + 1}
        else:
            media.meta = {'view_count': 1}
    else:
        media.meta = {'view_count': 1}
    media.save()
    return redirect(media.upload.url)


def media_unlock(request):
    password = request.POST.get('password')
    post_slugname = request.POST.get('post-id')
    media_id = request.POST.get('media-id')
    post = Post.objects.get(slugname = post_slugname)
    media = Files.objects.get(pk = media_id)
    if password:
        if check_password(password, post.password):
            return transfer_file(request, media)
        else:
            warning_message = _('Incorrect password')
    else:
        warning_message = _('Password must be filled')
    messages.warning(request, warning_message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MediaDownload(frontendView):

    def get(self, request, post_slugname, media_id):
        post = Post.objects.get(slugname=post_slugname)
        media = Files.objects.get(pk = media_id)
        if not post.password:
            return transfer_file(request, media)

