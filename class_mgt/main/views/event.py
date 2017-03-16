from datetime import datetime
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from main.forms import HiddenForm, NewEventForm
from main.models import *
from pytz import timezone as tz


@login_required
def event_list(request):
    username = request.user.username
    event_list = Event.objects.filter(
        e_deadline__gt=timezone.localtime(timezone.now()))
    p_event_list = Event.objects.filter(
        e_enddate__lt=timezone.localtime(timezone.now()))
    return render(request, 'event_list.html', locals())


@login_required
def event_details(request):
    username = request.user.username
    form = HiddenForm(request.POST or None)

    try:
        eventid = request.GET['eventid']
    except:
        eventid = None

    if eventid != None:
        event = Event.objects.get(id=eventid)

        if event.e_organizer == request.user and \
            timezone.localtime(timezone.now()) < event.e_deadline:

            print(event.e_organizer, username)

            status = 'owner'
            form.initial['hidden_data'] = 'remove'
            form.initial['eventid'] = event.id
            return render(request, 'event_details.html', {'username': username,
                                                          'event': event,
                                                          'status': status,
                                                          'form': form})

        elif event.e_organizer == request.user and \
            timezone.localtime(timezone.now()) > event.e_deadline:
            status = 'owner_disabled'
            print(status)
            return render(request, 'event_details.html', {'username': username,
                                                          'event': event,
                                                          'status': status,
                                                          'form': form})

        elif event in request.user.e_participant.all() and \
            timezone.localtime(timezone.now()) < event.e_deadline:
            status = 'participated'
            form.initial['hidden_data'] = 'quit'
            form.initial['eventid'] = event.id
            return render(request, 'event_details.html', {'username': username,
                                                          'event': event,
                                                          'status': status,
                                                          'form': form})

        elif event in request.user.e_participant.all()  and \
            timezone.localtime(timezone.now()) > event.e_deadline:
            status = 'participated_disabled'
            form.initial['hidden_data'] = 'quit'
            form.initial['eventid'] = event.id
            return render(request, 'event_details.html', {'username': username,
                                                          'event': event,
                                                          'status': status,
                                                          'form': form})
        elif timezone.localtime(timezone.now()) > event.e_deadline:
            status = 'apply_disabled'
            form.initial['hidden_data'] = 'join'
            return render(request, 'event_details.html', {'username': username,
                                                          'event': event,
                                                          'status': status,
                                                          'form': form})

        else:
            status = 'apply'
            form.initial['hidden_data'] = 'join'
            return render(request, 'event_details.html', {'username': username,
                                                          'event': event,
                                                          'status': status,
                                                          'form': form})

    else:
        return redirect('event_list')


@login_required
def add_event(request):
    username = request.user.username
    form = NewEventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            e_name = form.cleaned_data['e_name']
            e_startdate = datetime.strptime(
                form.cleaned_data['e_startdate'],
                '%Y/%m/%d %I:%M %p').replace(tzinfo=tz('Asia/Taipei'))
            e_enddate = datetime.strptime(
                form.cleaned_data['e_enddate'],
                '%Y/%m/%d %I:%M %p').replace(tzinfo=tz('Asia/Taipei'))
            e_place = form.cleaned_data['e_place']
            e_description = form.cleaned_data['e_description']
            e_deadline = datetime.strptime(
                form.cleaned_data['e_deadline'],
                '%Y/%m/%d %I:%M %p').replace(tzinfo=tz('Asia/Taipei'))

            event = Event.objects.create(
                e_name=e_name,
                e_startdate=e_startdate,
                e_enddate=e_enddate,
                e_place=e_place,
                e_description=e_description,
                e_deadline=e_deadline,
                e_postdate=timezone.localtime(timezone.now()),
                e_organizer=request.user)

            participation = Participation.objects.create(
                p_event=event,
                p_member=event.e_organizer)

            notification = Notification.objects.create(
                n_from=User.objects.get(username='system'),
                n_to=request.user,
                n_timestamp=timezone.localtime(timezone.now()),
                n_content='你已成功發佈了新活動：%s!\n\
                    活動詳情請<a href="/event_details?eventid=%d">按此</a>' % (
                    event.e_name, event.id))

            return render(request, 'event_added.html', {'username': username,
                                                        'event': event})
        else:
            return render(request, 'add_event.html', {'username': username,
                                                      'form': form})
    else:
        form.initial['e_startdate'] = timezone.localtime(timezone.now(
        )).strftime('%Y/%m/%d %I:%M %p')
        form.initial['e_enddate'] = timezone.localtime(timezone.now(
        )).strftime('%Y/%m/%d %I:%M %p')
        form.initial['e_deadline'] = timezone.localtime(timezone.now(
        )).strftime('%Y/%m/%d %I:%M %p')
        return render(request, 'add_event.html', {'username': username,
                                                  'form': form})


@login_required
def event_record(request):
    username = request.user.username
    past_events = request.user.e_participant.filter(
        e_enddate__lt=timezone.localtime(timezone.now()))
    incoming_events = request.user.e_participant.filter(
        e_enddate__gt=timezone.localtime(timezone.now()))
    return render(request, 'event_record.html', locals())


@login_required
def remove_event(request):
    username = request.user.username
    form = HiddenForm(request.POST or None)

    edetails_url = 'http://' + request.META[
        'HTTP_HOST'] + '/event_details?eventid='
    eremove_url = 'http://' + request.META['HTTP_HOST'] + '/remove_event'

    if 'HTTP_REFERER' in request.META.keys():
        referer = request.META['HTTP_REFERER']
    else:
        referer = 'nothing'

    if request.method == 'POST' and edetails_url in referer:
        eventid = urlparse(referer).query.split('=')[-1]
        event = Event.objects.get(id=eventid)

        return render(request, 'remove_event.html', {'username': username,
                                                     'event': event,
                                                     'referer': referer,
                                                     'form': form})
    elif request.method == 'POST' and referer == eremove_url:
        if form.data['hidden_data'] == 'remove':
            event = Event.objects.get(id=form.data['eventid'])
            event_name = event.e_name
            event.delete()
            Notification.objects.create(
                n_from=User.objects.get(username='system'),
                n_to=request.user,
                n_timestamp=timezone.localtime(timezone.now()),
                n_content='你已取消了活動：%s!' % event_name)

            return render(request, 'event_removed.html',
                          {'username': username,
                           'event_name': event_name})
    else:
        return redirect('event_list')


@login_required
def join_event(request):
    username = request.user.username
    form = HiddenForm(request.POST or None)

    edetails_url = 'http://' + request.META[
        'HTTP_HOST'] + '/event_details?eventid='

    if 'HTTP_REFERER' in request.META.keys():
        referer = request.META['HTTP_REFERER']
    else:
        referer = 'nothing'

    if request.method == 'POST' and edetails_url in referer:

        eventid = urlparse(referer).query.split('=')[-1]
        event = Event.objects.get(id=eventid)

        Participation.objects.create(p_member=request.user, p_event=event)

        Notification.objects.create(
            n_from=User.objects.get(username='system'),
            n_to=request.user,
            n_timestamp=timezone.localtime(timezone.now()),
            n_content='你已報名參加：%s!' % event.e_name)

        return render(request, 'join_event.html', {'username': username,
                                                   'event': event,
                                                   'referer': referer,
                                                   'form': form})
    else:
        return redirect('event_list')


@login_required
def quit_event(request):
    username = request.user.username
    form = HiddenForm(request.POST or None)

    edetails_url = 'http://' + request.META[
        'HTTP_HOST'] + '/event_details?eventid='
    equit_url = 'http://' + request.META['HTTP_HOST'] + '/quit_event'

    if 'HTTP_REFERER' in request.META.keys():
        referer = request.META['HTTP_REFERER']
    else:
        referer = 'nothing'

    if request.method == 'POST' and edetails_url in referer:
        eventid = urlparse(referer).query.split('=')[-1]
        event = Event.objects.get(id=eventid)

        return render(request, 'quit_event.html', {'username': username,
                                                   'event': event,
                                                   'referer': referer,
                                                   'form': form})

    elif request.method == 'POST' and referer == equit_url:
        print(form.data)
        if form.data['hidden_data'] == 'quit':
            event = Event.objects.get(id=form.data['eventid'])

            p_obj = Participation.objects.get(p_member=request.user,
                                              p_event=event)

            p_obj.delete()

            Notification.objects.create(
                n_from=User.objects.get(username='system'),
                n_to=request.user,
                n_timestamp=timezone.localtime(timezone.now()),
                n_content='你已取消報名：%s!' % event.e_name)

            return render(request, 'event_quit.html',
                          {'username': username,
                           'event_name': event.e_name})
    else:
        return redirect('event_list')
