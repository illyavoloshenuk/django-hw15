from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task


@receiver(post_save, sender=Task)
def notify_task_status_change(sender, instance, created, **kwargs):
    if created:
        return

    if instance.previous_status == instance.status:
        return

    owner = instance.owner
    if not owner.email:
        return

    if instance.status == Task.STATUS_CLOSED:
        subject = f'Задача "{instance.title}" закрыта'
        message = (
            f'Здравствуйте, {owner.username}!\n\n'
            f'Ваша задача "{instance.title}" была закрыта.\n'
            f'Статус изменён с "{instance.previous_status}" на "{instance.status}".\n'
        )
    else:
        subject = f'Статус задачи "{instance.title}" изменён'
        message = (
            f'Здравствуйте, {owner.username}!\n\n'
            f'Статус вашей задачи "{instance.title}" изменён.\n'
            f'Было: {instance.previous_status}\n'
            f'Стало: {instance.status}\n'
        )

    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@todoapp.com',
        recipient_list=[owner.email],
        fail_silently=False,
    )