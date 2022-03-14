from django.urls import path, re_path
from aurora.frontend.views.homepage import FrontendDefault
from aurora.frontend.views.media import MediaDownload, media_unlock
from aurora.frontend.views.page import ContactPage, AboutPage
from aurora.frontend.views.post import *
from aurora.frontend.views.directory import DirectoryLV
from aurora.frontend.views.people import PeopleLV, PeopleDV
from aurora.frontend.views.category import CategoryLV


urlpatterns = [
    path('', FrontendDefault.as_view(), name = 'aurora.frontend.index'),

    # default post and page URL
    path('posts', PostLV.as_view(), name = 'aurora.frontend.post.list'),
    path('directory', DirectoryLV.as_view(), name = 'aurora.frontend.directory'),
    path('people', PeopleLV.as_view(), name = 'aurora.frontend.people'),
    path('p/<slug:slugname>', PeopleDV.as_view(), name = 'aurora.frontend.people.detail'),
    path('contact', ContactPage.as_view(), name = 'aurora.frontend.contact'),
    path('about', AboutPage.as_view(), name = 'aurora.frontend.about'),

    path('post/<int:year>/<int:month>/<int:day>/<slug:slugname>', PostDetailView.as_view(), name = 'aurora.frontend.post.detail'),
    path('category/<slug:category>', CategoryLV.as_view(), name = 'aurora.frontend.category.list'),
    path('media/<slug:post_slugname>/<int:media_id>', MediaDownload.as_view(), name = 'aurora.frontend.media.download'),
    path('media/unlock', media_unlock, name = 'aurora.frontend.media.unlock'),
]

