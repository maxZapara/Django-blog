from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

from .models import Post


@login_required(login_url="/login")
def create_post(request):
    from .forms import PostForm
     
     
    form=PostForm()

    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            new_post=form.save()
            form.clean()
            print("f")
    
    return render(request, 'core/create_post.html', context={'name':'Max', 'form': form})


def index(request):
    from django.contrib import messages
    posts = Post.objects.all()
    messages.info(request, "Get all posts")

    return render(request, 'core/index.html', context={'name':'Max', 'posts': posts})

@login_required(login_url="/login")
def post_view(request, post_id):
    from django.shortcuts import get_object_or_404
    from .models import Comment
    from .forms import CommentForm
    from django.contrib import messages

    post=get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        print('form')
        form=CommentForm(request.POST)
        if form.is_valid():
            print('valid')
            comment=form.save(commit=False)
            comment.post=post
            comment.author=request.user
            comment.save()
            print(comment)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form=CommentForm()
    comments=Comment.objects.filter(post=post).order_by('-created_at').all()
    print(comments)
    
    return render(request, 'core/post_view.html', context={'post':post, 'form':form, 'comments':comments})

def delete_comment(request,comment_id):
    from .models import Comment
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse

    
    if request.method == 'POST':
        comment=get_object_or_404(Comment, id=comment_id)
        comment.delete()

        return JsonResponse({"status":"success"})
    
    return JsonResponse({"status":"error"}, status=400)