from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import Announcement, Comment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .filters import AnnouncementFilter, CommentFilter
from django.db.models import Q
from .forms import AnnouncementForm

from django.shortcuts import get_object_or_404


# Create your views here.


def index(request):
    return HttpResponse("Welcome to 'Message Board'")


def index2(request):
    return HttpResponse("Welcome --- 'Message Board'")


# class AnnouncementsList(LoginRequiredMixin, ListView):
class AnnouncementList(ListView):
    model = Announcement
    template_name = 'announcement_list1.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnnouncementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AnnouncementDetail(DetailView):
    # Указываем модель, объекты которой мы будем выводить
    model = Announcement
    template_name = 'announcement_detail.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = AnnouncementFilter(self.request.GET, queryset)
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(announcement_id=self.object.pk).filter(
            Q(status='a') | Q(status='w'))
        return context

    def __str__(self):
        return self.title


class AnnouncementEdit(UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'


class AnnouncementDelete(DeleteView):
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('ann_list')


class CommentList(ListView):
    model = Comment
    template_name = 'comment_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def accept(request, id):
    comment = Comment.objects.get(pk=id)
    comment.status = 'a'
    comment.save()
    return redirect('ann_detail', pk=id)


def reject(request, id):
    comment = Comment.objects.get(pk=id)
    comment.status = 'r'
    comment.save()
    return redirect("ann_detail", pk=id)
