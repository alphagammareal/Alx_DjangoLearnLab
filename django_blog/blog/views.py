from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post
from .forms import CustomUserCreationForm



# POST LIST
def post_list(request):
    posts = Post.objects.select_related('author').all()
    return render(request, 'blog/post_list.html', {'posts': posts})


# POST DETAIL
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# USER REGISTRATION
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})




# USER PROFILE
@login_required
def profile(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email", request.user.email)
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("blog:profile")

    return render(request, "blog/profile.html")


