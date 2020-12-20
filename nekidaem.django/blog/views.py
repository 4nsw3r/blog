from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView, FormView, RedirectView
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, PublicateConfirm, CreatePostForm, SubscribeConfirm, UnsubscribeConfirm
from .models import Post, Profile, ReadedPost

import datetime


# Create your views here.
# create blog if is none, email, css, docker


class CreatePost(CreateView):
    """"Форма создания поста"""
    form_class = CreatePostForm
    template_name = 'posts/create_post.html'

    def get_success_url(self):
        return reverse('author_blog_list', args=(self.request.user.id,))

    def get_initial(self):
        initial = super(CreatePost, self).get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user
        return initial

    def form_valid(self, form):
        form.data.author = self.request.user
        return super(CreatePost, self).form_valid(form)


class DeletePostView(DeleteView):
    """Удаление поста"""
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('index')


class UpdatePostView(UpdateView):
    """Редактирование поста"""
    model = Post
    template_name = 'posts/update_post.html'
    fields = ['title', 'content']


class ViewPost(DetailView):
    """Детализация поста"""
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    template_name = 'posts/post_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ViewPost, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            post_id = self.kwargs['pk']
            readed, created = ReadedPost.objects.get_or_create(post_id=post_id,
                                                               user_id=user_id,
                                                               defaults={'post_id': post_id, 'user_id': user_id})
            if created:
                readed.save()
        return context


class Subscribe(FormView):
    """Форма подписки"""
    form_class = SubscribeConfirm
    template_name = 'authors/subscribe_confirm.html'
    success_url = reverse_lazy('authors')

    def form_valid(self, form):
        author_id = self.kwargs['author_id']
        user_id = self.request.user.id
        subscriber = Profile.objects.get(pk=user_id)
        author = Profile.objects.get(pk=author_id)
        author.subscribe.add(subscriber)
        author.save()
        return super(Subscribe, self).form_valid(form)



class Unsubscribe(FormView):
    """Форма отписки"""
    form_class = UnsubscribeConfirm
    template_name = 'authors/subscribe_confirm.html'
    success_url = reverse_lazy('authors')

    def form_valid(self, form):
        author_id = self.kwargs['author_id']
        user_id = self.request.user.id
        subscriber = Profile.objects.get(pk=user_id)
        author = Profile.objects.get(pk=author_id)
        author.subscribe.remove(subscriber)
        author.save()
        #ReadedPost.objects.filter(user_id=author_id).delete()


        return super(Unsubscribe, self).form_valid(form)


class Publicate(FormView):
    """"Форма публикации"""
    form_class = PublicateConfirm
    success_url = reverse_lazy('index')
    template_name = 'authors/post_publicate_confirm.html'

    def form_valid(self, form):
        public_post = Post.objects.get(pk=int(self.kwargs['pk']))
        public_post.published = datetime.datetime.now()
        public_post.save()
        return super(Publicate, self).form_valid(form)


class PostsListView(ListView):
    """Главная страница"""
    model = Post
    context_object_name = 'posts_list'
    queryset = Post.objects.exclude(published__isnull=True)
    template_name = 'posts/index.html'


class AuthorsListView(ListView):
    """"Список авторов"""
    model = Profile
    context_object_name = 'authors_list'
    template_name = 'authors/authors_list.html'

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super(AuthorsListView, self).get_context_data(*args, **kwargs)
            context['user_profile'] = Profile.objects.get(pk=int(self.request.user.id))
            return context


class AuthorDetails(DetailView):
    """"Инфо об авторе"""
    model = Profile
    context_object_name = 'author_details'
    pk_url_kwarg = "pk"
    template_name = 'authors/author_details.html'


class AuthorBlogList(ListView):
    """Личный блог"""
    model = Post
    context_object_name = 'author_posts_list'
    pk_url_kwarg = "author_id"
    template_name = 'posts/author_posts_list.html'

    def get_queryset(self):
        author_id = int(self.kwargs['author_id'])
        return Post.objects.filter(author_id=author_id)


class RibbonBlogList(ListView):
    """Персональная лента"""
    model = Post
    context_object_name = 'ribbon'
    pk_url_kwarg = "author_id"
    template_name = 'posts/posts_ribbon.html'
   # queryset = Post.objects.exclude().order_by('-published')

    def get_queryset(self):
        author_id = int(self.kwargs['author_id'])
        return Post.objects.exclude(author_id=author_id)


class LoginView(FormView):
    """"Форма авторизации"""
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'authors/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(RedirectView):
    """"Форма выхода из уч. записи"""
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


# class BlogView(DetailView):
#     model = Profile
#     context_object_name = 'blog'
#     template_name = 'base_generic.html'
#     queryset = Profile.objects.all()
#     #queryset = Profile.objects.exclude(blog_name__isnull=True).exclude(blog_name__exact='')