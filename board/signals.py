from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Comment


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Comment)
def new_comment(sender, instance, created, **kwargs):
    if created:
        subject = f'Пришел новый отклик на сообщение "{instance.announcement.title}" от {instance.announcement.author.username}'
        message = f'{instance.content}'
        recipient_list = {instance.announcement.author.username},
    else:
        subject = f'Изменен статус отклика'
        message = f'Изменен статус отклика "{instance.content}" на "{instance.get_status_display()}"'
        recipient_list = {instance.author.username}
    #    print('почта ушла')

    send_mail(
        subject=subject,
        message=message,
        from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        recipient_list=recipient_list,
    )
    #    print(instance.announcement.author.username)
    #print(f'{instance.status} {instance.get_status_display()}')
