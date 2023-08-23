from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Announcement, Comment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .filters import AnnouncementFilter
# from .forms import AnnouncementForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(announcement_id=self.object.pk)
        return context

    def __str__(self):
        return self.title

    # def get(self, request, pk):
    #     try:
    #         announcement = Announcement.objects.get(pk=pk)
    #     except:
    #         return HttpResponse(content=(f'object {pk} does not exists'), status=404)
    #     return HttpResponse(content=announcement, status=200)


#    template_name = 'ann_list.html'
# Поле, которое будет использоваться для сортировки объектов
#    ordering = '-time_create'
# Указываем имя шаблона, в котором будут все инструкции о том,
# как именно пользователю должны быть показаны наши объекты
#    template_name = 'ann_list.html'
# Это имя списка, в котором будут лежать все объекты.
# Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
#    context_object_name = 'announcement'

# По ТЗ надо выводить список новостей, а не всех постов (кроме новостей есть еще и статьи)
# Для этого реализован этот фильтр. Если его убрать, тогда queryset вернет все записи
# queryset = Post.objects.all().filter(property='N')
#    paginate_by = 10  # количество записей на странице

# Переопределяем функцию получения списка статей
# @property
#   def get_queryset(self):
# Получаем обычный запрос
#        queryset = super().get_queryset()
#        queryset = Announcement.objects.filter(property='A')
# Сохраняем нашу фильтрацию в объекте класса,
# чтобы потом добавить в контекст и использовать в шаблоне.
#        self.filterset = ArticlesFilter(self.request.GET, queryset)
#        return self.filterset.qs
#        return queryset

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     # Добавляем в контекст объект фильтрации.
#     context['filterset'] = self.filterset
#     return context

#       return HttpResponse(render(request, 'anns_list.html', context))

class CommentList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Comment
    template_name = 'comment_list.html'


#    context_object_name = 'comment_announcement_list'

# def get_queryset(self):
#     self.comment = get_object_or_404(Comment, announcement=self.kwargs['pk'])
#     queryset = Comment.objects.filter(announcement=self.ategory).order_by('-time_create')
#     return queryset




def accept(request, oid):
    comment = Comment.objects.get(pk=oid)
    comment.status = 'a'
    comment.save()
    return redirect('ann_detail', pk=oid)


def reject(request, oid):
    comment = Comment.objects.get(pk=oid)
    comment.status = 'r'
    comment.save()
    return redirect("ann_detail", pk=oid)
