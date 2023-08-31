import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
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


class AnnouncementEdit(LoginRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'


class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    model = AnnouncementForm
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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Comment.objects.filter(announcement_id=self.kwargs.get('pk'))
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

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  #  это то же, что и message
            from_email='ankom888@yandex.ru',
            to=['ankom@list.ru'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        # есть еще функции mail_managers, send_mass_mail() см. https://django.fun/ru/docs/django/4.1/topics/email/
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )



        # отправляем письмо
        # send_mail(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=appointment.message,  # сообщение с кратким описанием проблемы
        #     from_email='ankom888@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=['ankom@list.ru', ]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        # )

#        return redirect('appointments:make_appointment')
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
