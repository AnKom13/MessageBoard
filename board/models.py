from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Announcement(models.Model):
    CATEGORY = [
        ('tank', 'Танки'),
        ('heal', "Хилы"),
        ('dd', "ДД"),
        ('trader', 'Торговцы'),
        ('gildmaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('skinner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('wizard', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    title = models.CharField(max_length=255, unique=True, verbose_name='Title')

    #    content = models.TextField(verbose_name='Содержание')
    content = RichTextField(blank=True, null=True, verbose_name='Содержание')

    category = models.CharField(max_length=10, choices=CATEGORY, verbose_name='Category')
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('ann_detail', args=[str(self.id)])


class Comment(models.Model):
    STATUS = [
        ('w', 'wait'),
        ('a', "accept"),
        ('r', "reject"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS, default='w', verbose_name='Status')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name='announcement')

    class Meta:
        ordering = ['id']
