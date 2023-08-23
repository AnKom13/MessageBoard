from django import forms
from .models import Announcement, Comment
from django.core.exceptions import ValidationError


class AnnouncementForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(Announcement, self).__init__(*args, **kwargs)
    #     self.fields['property'].initial = 'N'

    class Meta:
        model = Announcement
        # fields = '__all__' #все поля кроме id
        # лучше все перечислять, чтобы не вывести поля которые не нужны
        fields = ['title', 'category', 'content', ]

# def clean_property(self):
#     pr = self.cleaned_data.get("property")
#     if pr != 'N':
#         raise ValidationError("Это не статья, а новость")
#     return 'N'

class CommentForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(Announcement, self).__init__(*args, **kwargs)
    #     self.fields['property'].initial = 'N'

    class Meta:
        model = Comment
        # fields = '__all__' #все поля кроме id
        # лучше все перечислять, чтобы не вывести поля которые не нужны
        fields = ['author', 'content', 'status']