from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Post, Comment
from taggit.models import Tag
from .forms import PostForm, CustomUserCreationForm, CommentForm

# --------------------------
# Post Views
# --------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created successfully.")
        return response

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this post.")
        return redirect('blog:post_detail', pk=self.get_object().pk)

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this post.")
        return redirect('blog:post_detail', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)


# --------------------------
# User Views
# --------------------------

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("blog:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        new_email = request.POST.get("email")
        request.user.email = new_email
        request.user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("blog:profile")
    return render(request, "blog/profile.html", {"user": request.user})


# --------------------------
# Comment Views
# --------------------------

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('blog:post_detail', pk=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You cannot edit this comment.")
        return redirect('blog:post_detail', pk=self.get_object().post.id)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You cannot delete this comment.")
        return redirect('blog:post_detail', pk=self.get_object().post.id)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Comment deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.id})


# --------------------------
# Search & Tag Views
# --------------------------

def post_search(request):
    query = request.GET.get('q', '').strip()
    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        messages.success(self.request, "Comment added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()  # redirects to post detail