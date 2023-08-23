from django_filters import FilterSet
from .models import Announcement, Comment


class AnnouncementFilter(FilterSet):
    class Meta:
        model = Announcement
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
            'author': ['exact']
        }


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'status': ['exact'],
            'author': ['exact'],
        }
