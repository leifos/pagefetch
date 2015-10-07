from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from pagefetch.game_models import HighScore, PlayerAchievement, UserProfile, Achievement, Category
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
from django.forms import ModelForm
from forms import *
from configuration import MEDIA_URL, UPLOAD_DIR
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from ifind.common.utils import encode_string_to_url



def profile_page(request, username):
    view_permission = False
    context = RequestContext(request, {})
    user = User.objects.get(username=username)
    if user:
        user_profile = user.get_profile()
        achievements = PlayerAchievement.objects.filter(user=user)
        #TODO(mtbvc): do the following in a cleaner way
        #filter out achievements player got from all that are available
        available_achievements = Achievement.objects.all()
        player_badges = [item.achievement for item in achievements]
        av_achievements = []
        for item in available_achievements:
            if item not in player_badges:
                av_achievements.append(item)
        #do same with highscores
        available_cats = Category.objects.all()
        highscores = HighScore.objects.filter(user=user)
        scores = list(highscores)
        player_cats = [item.category for item in highscores]
        for item in available_cats:
            if item not in player_cats:
                scores.append(HighScore(category=item, highest_score=0))
        progress = get_progress(user, user_profile)
        for score in scores:
            score.url = encode_string_to_url(score.category.name)
            print score.url
    if request.user == user:
        view_permission = True
    return render_to_response('profiles/profile_page.html', {'usr': user,
                                                             'profile': user_profile,
                                                             'murl': MEDIA_URL,
                                                             'achievements': achievements,
                                                             'available_achievements': av_achievements,
                                                             'view_perm': view_permission,
                                                             'highscores': scores,
                                                             'progress': progress,
                                                             'total_score' : sum(i.highest_score for i in highscores)},
                                                              context)


@login_required
def edit_profile(request, username):
    #if usr1 tries accessing usr2 profile edit page, redirect to usr1 edit page
    if username != request.user.username:
        return redirect('/profile/%s/edit_profile' % request.user.username)
    context = RequestContext(request, {})
    usr = User.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=usr)
    profile_form = ProfileForm(instance=profile)
    user_form = UserForm(instance=usr)

    if request.method == 'GET':
        return render_to_response('profiles/edit_profile.html', {'profile_form': profile_form,
                                                                 'user_form': user_form},context)
    else:
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(data=request.POST, instance=usr)
        if profile_form.is_valid() and user_form.is_valid():
            if request.FILES:
                #os.remove(profile.profile_pic.url)
                #os.remove(os.path.join(settings.MEDIA_ROOT, profile.profile_pic.))
                print profile.profile_pic
                print "----"
                print request.FILES['profile_pic']
                print MEDIA_URL + UPLOAD_DIR + '/' + str(profile.profile_pic)
                print profile.profile_pic.file
                #print os.path.join(MEDIA_URL, profile.profile_pic)
            user_form.save()
            profile_form.save()

        else:
            return render_to_response('profiles/edit_profile.html', {'profile_form': profile_form,
                                                                     'user_form': user_form},context)
        return HttpResponseRedirect(reverse('profile', args=(usr.username,)))



@login_required
def graphs(request, username):
    context = RequestContext(request, {})
    return render_to_response('profiles/graphs.html', {}, context)




def get_progress(user,profile):
    progress = 0
    factor = 20 #TODO(mtbvc): don't hardcode this
    #profile_form = ProfileForm(instance=profile)
    #for item in profile_form:
    #    print item
    #    if item:
    #        progress += factor

    if user.email:
        progress += factor
    if profile.age:
        progress += factor
    if profile.gender:
        progress += factor
    if profile.country:
        progress += factor
    if profile.city:
        progress += factor

    if progress > 100:
        progress = 100
    return progress
