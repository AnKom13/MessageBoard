from django import forms
from .models import Announcement, Comment


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'category', 'content', ]


class AnnouncementForm1(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'category', 'content', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content', 'status']
