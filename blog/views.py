from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm
# Create your views here.


def post_list_view(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')

    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html',{'post_list': post_list})

def post_detail_view(request,post,year):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,)

    return render(request,'blog/post_detail.html',{'post' : post})


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