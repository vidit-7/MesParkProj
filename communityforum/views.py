from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.core.paginator import Paginator

from communityforum.forms import ForumPostForm
from communityforum.models import ForumPost,ForumComment,Topic

import json

# Create your views here.

def communityHome(request):
    topics = Topic.objects.all()

    q = request.GET.get('search') if request.GET.get('search') != None else ''
    
    forumPostsAll = ForumPost.objects.filter(Q(title__icontains=q)|Q(topics__name__icontains=q)).order_by('-posted').distinct()
    count = forumPostsAll.count()
    paginator = Paginator(forumPostsAll, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'forumPosts':page_obj,'topics':topics,'count':count, 'q':q}
    return render(request,'communityforum/community-home.html',context)

@login_required(login_url='centBaseLoginUser')
def communityCreatePost(request):
    form = ForumPostForm()
    if request.method == 'POST':
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            nousrfrm = form.save(commit=False)
            nousrfrm.user = request.user
            nousrfrm.save()
            form.save_m2m()
            messages.success(request,'Your post has been created!')
            return redirect('communityForumHome')
    context = {'form':form,'act':'Create'}
    return render(request,'communityforum/createpost.html',context)


@login_required(login_url='centBaseLoginUser')
def communityEditPost(request,pk):
    posttoedit = ForumPost.objects.get(id=pk)

    if posttoedit.user == request.user:
        form = ForumPostForm(instance=posttoedit)
        if request.method == 'POST':
            form = ForumPostForm(request.POST, instance=posttoedit)
            if form.is_valid():
                form.save()
                messages.success(request,'Your post has been updated!')
                return redirect('communityForumHome')
    else:
        return HttpResponse('Unauthorized')
    
    context = {'form':form, 'act':'Update'}
    return render(request,'communityforum/createpost.html',context)


@login_required(login_url='centBaseLoginUser')
def communityDeletePost(request,pk):
    posttd = ForumPost.objects.get(id=pk)

    if request.method=='POST':
        if posttd.user == request.user:
            posttd.delete()
            messages.success(request,'The post has been deleted.')
            return redirect('communityForumHome')
        else:
            return HttpResponse('Unauthorized')
    
    context = {'obj':posttd}
    return render(request,'communityforum/delete_confirm.html',context)
    

def communitySeePost(request,pk):
    forumPost = ForumPost.objects.get(id=pk)
    fcomments = ForumComment.objects.filter(forumpost__id=pk).order_by('-posted')

    # if request.method == 'POST':
    #     newcomment = ForumComment.objects.create(
    #         user = request.user,
    #         forumpost = forumPost,
    #         comment = request.POST.get('comment'),
    #     )
        
    #     return redirect('seeFPost', pk = forumPost.id)

    context = {'forumPost':forumPost,'fcomments':fcomments}
    return render(request, 'communityforum/discuss.html', context)

@login_required(login_url='centBaseLoginUser')
def communityAddComment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            postId = data['postId']
            commentData = data['commentData']
            tgtpost = ForumPost.objects.get(id=postId)
        except:
            return JsonResponse({'success':False, 'error':'invalid'})
        
        if str(commentData).strip() == "":
            return JsonResponse({'success':False, 'error':'empty'})
        
        createdComment = ForumComment.objects.create(
            user = request.user,
            forumpost = tgtpost,
            comment = commentData,
        )
        
        ctxDict = {'createdcomment':commentData,'success': True}
        messages.success(request, "Comment posted!")
        return JsonResponse(ctxDict)
    else:
        return HttpResponse('Invalid request')

# @login_required(login_url='centBaseLoginUser')
# def communityDeleteComment(request,pk):
#     commenttd = ForumComment.objects.get(id=pk)

#     if request.method=='POST':
#         if commenttd.user == request.user:
#             commenttd.delete()
#             messages.success(request,'The comment has been deleted.')
#             return redirect('communityForumHome')
#         else:
#             return HttpResponse('Unauthorized')
    
#     context = {'obj':commenttd}
#     return render(request,'communityforum/delete_confirm.html',context)

@login_required(login_url='centBaseLoginUser')
def communityDeleteComment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            commentId = data['commentId']
            commenttd = ForumComment.objects.get(id=commentId)
        except:
            # messages.warning(request, "comment not found")
            return JsonResponse({"success":False})

        if commenttd.user == request.user:
            commenttd.delete()
            messages.success(request,'The comment has been deleted.')
            return JsonResponse({'message': 'The comment has been deleted', 'success':True})
        else:
            return HttpResponse('Unauthorized')
    else:
        return HttpResponse('Invalid request')
