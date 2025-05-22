from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from communityforum.forms import ForumPostForm
from communityforum.models import ForumPost,ForumComment,Topic

import json

# Create your views here.

def communityHome(request):
    topics = Topic.objects.all()

    q = request.GET.get('search') if request.GET.get('search') != None else ''
    
    forumPosts = ForumPost.objects.filter(Q(title__icontains=q)|Q(topics__name__icontains=q)).order_by('-posted').distinct()
    count = forumPosts.count()

    context = {'forumPosts':forumPosts,'topics':topics,'count':count}
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
    data = json.loads(request.body)

    postId = data['postId']
    commentData = data['commentData']

    success = True
    try:
        tgtpost = ForumPost.objects.get(id=postId)
    except:
        success = False

    createdComment = ForumComment.objects.create(
        user = request.user,
        forumpost = tgtpost,
        comment = commentData,
    )

    ctxDict = {
        'createdcomment':commentData,
        'success': success
    }
    messages.success(request, "Comment posted!")
    return JsonResponse(ctxDict)

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
    data = json.loads(request.body)
    commentId = data['commentId']

    success = True

    try:
        commenttd = ForumComment.objects.get(id=commentId)
    except:
        # messages.warning(request, "comment not found")
        success = False
        return JsonResponse({"success":success})

    if commenttd.user == request.user:
        commenttd.delete()
        messages.success(request,'The comment has been deleted.')
        return JsonResponse({'message': 'The comment has been deleted', 'success':success})
    else:
        return HttpResponse('Unauthorized')
