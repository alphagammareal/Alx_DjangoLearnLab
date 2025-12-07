from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CommentForm


# List and Detail (public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' 
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create (authenticated users only)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # set the author before saving
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created successfully.")
        return response

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

# Update (only author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this post.")
        return redirect('blog:post_detail', pk=self.get_object().pk)

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

# Delete (only author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this post.")
        return redirect('blog:post_detail', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted.")
        return super().delete(request, *args, **kwargs)
# REGISTER VIEW
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

# PROFILE VIEW
@login_required
def profile_view(request):
    if request.method == "POST":
        new_email = request.POST.get("email")
        request.user.email = new_email
        request.user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("blog:profile")
    return render(request, "blog/profile.html")

# Add comment
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

# Edit comment
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

# Delete comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You cannot delete this comment.")
        return redirect('blog:post_detail', pk=self.get_object().post.id)

    def get_success_url(self):
        messages.success(self.request, "Comment deleted.")
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.id})