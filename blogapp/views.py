from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Profile
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.conf import settings
from django.db.models import Q


class PostListView(ListView):
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query)).distinct()
        else:
            return Post.objects.order_by('-created_on')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, *args, **kwargs):
        liked = False
        subscribed = False
        read_status = False
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        if post.read_status.filter(id=self.request.user.id).exists():
            read_status = True
        context['read_status'] = read_status
        if not self.request.user.is_anonymous:
            author_profile = Profile.objects.get_or_create(user=post.author)[0]
            if author_profile.followers.filter(id=self.request.user.id):
                subscribed = True
        context['subscribed'] = subscribed
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        author = form.cleaned_data.get('author')
        subscribes = Profile.objects.get_or_create(user=author)[0].followers.all()
        if subscribes:
            messages = list()
            subject = 'New post was added'
            from_email = settings.EMAIL_HOST_USER
            for person in subscribes:
                body = f"Hi {person.username}! Dont miss {author}'s new post{form.cleaned_data.get('title')}"
                message2 = subject, body, from_email, [person.email]
                messages.append(message2)
            send_mass_mail(messages, fail_silently=False)
        return super(AddPostView, self).form_valid(form)


class EditPostView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    fields = ['title', 'author', 'content', 'status']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class UserBlogView(ListView):
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['pk']).order_by('-created_on')


class MySubscriptsView(ListView):
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        users = Profile.objects.get_or_create(user=self.request.user)[0].following.all()
        return Post.objects.filter(author__in=users)


def like_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def subscribe_view(request, author, blog_id):
    user = User.objects.get(id=request.user.id)
    author = User.objects.get(id=author)
    author_profile = Profile.objects.get_or_create(user=author)[0]
    user_profile = Profile.objects.get_or_create(user=user)[0]
    if author_profile.followers.filter(id=user.id):
        author_profile.followers.remove(user)
        user_profile.following.remove(author)
    else:
        author_profile.followers.add(user)
        user_profile.following.add(author)
    return HttpResponseRedirect(reverse('post_detail', args=[str(blog_id)]))


def read_status_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.read_status.filter(id=request.user.id).exists():
        post.read_status.remove(request.user)
    else:
        post.read_status.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))
