from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Announcement, Comment
from .forms import AnnouncementForm
from .filters import AnnouncementFilter, CommentFilter
import datetime


# Create your views here.
class AnnouncementList(ListView):
    model = Announcement
    template_name = 'announcement_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnnouncementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AnnouncementDetail(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'announcement_detail.html'


class AnnouncementEdit(LoginRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'


class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('ann_list')


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    model = Announcement
    fields = ['title', 'category', 'content', ]
    template_name = 'announcement_edit.html'
    success_url = '/board/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment

    fields = ['content', ]
    template_name = 'comment_edit.html'
    success_url = '/board/'

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        form.instance.status = 'w'
        form.instance.time_create = datetime.datetime.now()
        form.instance.announcement_id = self.kwargs['pk']
        return super().form_valid(form)


class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Comment.objects.filter(announcement_id=self.kwargs.get('pk'))
        #        .filter(
        #            Q(status='a') | Q(status='w'))
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def post(self, request, *args, **kwargs):
        appointment = Comment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'yandex_created.html',
            {
                'appointment': appointment,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email=None,
            to=[request.user.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()
        return redirect('/')


def accept(request, id):
    comment = Comment.objects.get(pk=id)
    comment.status = 'a'
    comment.save()
    return redirect('ann_comment_list', pk=comment.announcement.id)


def reject(request, id):
    comment = Comment.objects.get(pk=id)
    comment.status = 'r'
    comment.save()
    return redirect('ann_comment_list', pk=comment.announcement.id)
