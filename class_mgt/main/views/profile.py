from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from main.forms import ResetPwdForm
from main.models import Event, Participation


@login_required
def profile(request):
    form = ResetPwdForm(request.POST or None, request=request)

    username = request.user.username
    event_hlist = Event.objects.filter(e_organizer=request.user)
    event_hcount = event_hlist.count()
    event_plist = request.user.e_participant.all()
    event_pcount = Participation.objects.filter(p_member=request.user).count()

    if request.method == 'POST' and form.is_valid():
        request.user.set_password(form.cleaned_data['new_pwd'])
        request.user.save()
        logout(request)
        return redirect('login')
    else:
        return render(request, 'profile.html', locals())
