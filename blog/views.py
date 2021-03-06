from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm
from taggit.models import Tag
# Create your views here.


def post_list_view(request, tag_slug=None):
    post_list = Post.objects.all()
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html',{'post_list': post_list,'tag':tag})

def post_detail_view(request,post,year):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,)
    comments = post.comments.filter(active=True)
    new_comment = None
    #comment posted
    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
    # create comment object but don't save in database yet
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post = post
            # save the comment to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,'blog/post_detail.html',{'post' : post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form})


# def post_detail_view(request,post,year,month,day):
#     post = get_object_or_404(Post,
#                              slug=post,
#                              status='published',
#                              publish__year=year,
#                              publish__month=month,
#                              publish__day=day)
#     return render(request,'blog/post_detail.html',{'post' : post})

from django.core.mail import send_mail
from .forms import EmailSendForm

def mail_send_view(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message = 'Read post at :\n {}\n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'snehalkarale21@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form, 'post':post, 'sent':sent})