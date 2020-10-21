from .views import PostDetailView, PostListView, AddPostView, UserBlogView,\
    EditPostView, DeletePostView, like_view, MySubscriptsView, subscribe_view, read_status_view
from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('blog/<int:pk>/', UserBlogView.as_view(), name='user_blog'),
    path('my_subscripts/', MySubscriptsView.as_view(), name='my_subscripts'),
    path('post/edit/<int:pk>/', EditPostView.as_view(), name='edit_post'),
    path('post/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('like/<int:pk>/', like_view, name='like_post'),
    path('read/<int:pk>/', read_status_view, name='read_status_post'),
    path('subscribe/<int:author>/<int:blog_id>/', subscribe_view, name='subscribe_post'),
]