from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ProfileForm, CustomPasswordChangeForm
from centbase.models import Profile

from communityforum.models import ForumPost,ForumComment,Topic
# Create your views here.

def baseHome(request):
    return render(request, 'centbase/home.html')

def baseLoginUser(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upassword = request.POST.get('password')

        uexists = True

        try:
            User.objects.get(username=uname)
        except:
            messages.warning(request, f"Matching username not found.")
            uexists = False

        loguser = authenticate(request, username=uname, password=upassword)

        if loguser is not None:
            login(request, loguser)
            messages.success(request, f"You have been logged in successfully.")
            return redirect('centBaseHome')
        else:
            if uexists:
                messages.error(request, f"Authentication failed for {uname}. Incorrect password.")

    context = {}
    return render(request,'centbase/login.html',context)

@login_required(login_url="centBaseLoginUser")
def baseLogoutUser(request):
    context = {}
    if request.user.is_authenticated:
        if request.method=='POST':
            logout(request)
            messages.info(request, f"You have been logged out.")
            return redirect('centBaseHome')
        return render(request,'centbase/logout-confirm.html',context)
    return redirect('centBaseHome')

def baseRegisterUser(request):
    if request.method == 'POST':
        regform = UserRegistrationForm(request.POST)
        if regform.is_valid():
            # save uname and pass
            user = regform.save(commit=False)
            # save f and l name
            first_name = regform.cleaned_data.get('first_name')
            last_name = regform.cleaned_data.get('last_name')
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            username = regform.cleaned_data.get('username')
            messages.success(request, f"New user @{username} has been created successfully.")
            return redirect('centBaseLoginUser')
    else:
        regform = UserRegistrationForm()

    context = {'regform':regform}
    return render(request,'centbase/register.html',context)

def baseProfile(request, pk):
    try:
        founduser = User.objects.get(id=pk)
    except:
        return HttpResponse("404 not found")

    forumPosts = ForumPost.objects.filter(user=pk).order_by('-updated','-posted')
    forumComments = ForumComment.objects.filter(user=pk).order_by('-posted')

    profile = Profile.objects.get(user=founduser)
    context = {'profile':profile, 'forumPosts':forumPosts, 'forumComments': forumComments}
    return render(request, 'centbase/profile.html', context)

@login_required(login_url="centBaseLoginUser")
def baseEditProfile(request):
        if request.method == 'POST':
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile = profile_form.save(commit=False)
                if not profile.pic:
                    profile.pic = "defaults/defaultuser.png"
                if not profile.about:
                    profile.about = "No information."
                profile.save()

                messages.success(request, "Your profile has been updated")
                return redirect("centBaseProfile",pk=request.user.id)
                # return HttpResponse("done")
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)

        context = {"user_form":user_form, "profile_form":profile_form}
        return render(request, "centbase/edit-profile.html", context)


def changeUserPass(request):
    if request.method == "POST":
        pass_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if pass_form.is_valid():
            upd_user = pass_form.save()
            update_session_auth_hash(request, upd_user)
            messages.info(request, "Your password has been updated successfully, use your new password from now on.")
            return redirect('centBaseEditProfile')
        else:
            context = {'pass_form': pass_form}
            return render(request, "centbase/change-pass.html", context)
        
    pass_form = CustomPasswordChangeForm(user=request.user)
    context = {'pass_form': pass_form}
    return render(request, "centbase/change-pass.html", context)