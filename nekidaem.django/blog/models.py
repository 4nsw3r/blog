from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=1024, verbose_name='Название блога')
    subscribes = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='subscribe')  # Подписки

    def get_absolute_url(self):
        return '/author/%i/' % self.pk

    def __str__(self):
        return (f'{self.user.username}: {self.blog_name}')


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Post(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    published = models.DateTimeField(blank=True, null=True, verbose_name='Опубликовано')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    read_by = models.ManyToManyField(User, related_name='read_articles', blank=True)

    def get_absolute_url(self):
        return '/post/%i/' % self.pk

    def __str__(self):
        return f'{self.title}:{self.author}'

    class Meta:
        ordering = ('-published',)


# send mail
@receiver(post_save, sender=Post)
def send_notify_about_new_article(sender, instance, created, **kwargs):
    if created:
        for sub in instance.author.subscribes.all():
            if sub.user.email:
                send_mail(
                    '"{}" - new post in {} {}.'.format(instance.title,
                                                        instance.author.user.username,
                                                        instance.author.blog_name),
                    'Link to new post: {}'.format(
                        settings.BASE_URL + reverse('view_post', args=[instance.pk])),
                    'testnekidaem@gmail.com',
                    [sub.user.email],
                    fail_silently=False,
                )
