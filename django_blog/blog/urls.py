from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:post_list'), name='logout'),

    # Comment URLs
path('post/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete')
]
