"""
URL configuration for MessageBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from board.views import AnnouncementList, AnnouncementDetail, AnnouncementEdit, AnnouncementDelete, AnnouncementCreate
from board.views import CommentList, CommentCreate, accept, reject

urlpatterns = [
    path('', AnnouncementList.as_view(), name='ann_list'),
    path('announcements/', AnnouncementList.as_view(), name='ann_list'),
    path('announcement/<int:pk>/', AnnouncementDetail.as_view(), name='ann_detail'),
    path('announcement/<int:pk>/edit/', AnnouncementEdit.as_view(), name='ann_edit'),
    path('announcement/<int:pk>/delete/', AnnouncementDelete.as_view(), name='ann_delete'),
    path('announcement/<int:pk>/comments/', CommentList.as_view(), name='ann_comment_list'),
    path('announcement/create/', AnnouncementCreate.as_view(), name='ann_create'),
    path('announcement/<int:pk>/comments/create/', CommentCreate.as_view(), name='comment_create'),
    path('announcement/comment/accept/<int:id>', accept, name='accept'),
    path('announcement/comment/reject/<int:id>', reject, name='reject'),
]
