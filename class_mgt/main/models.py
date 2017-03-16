from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Event(models.Model):
    e_name = models.CharField(max_length=255)
    e_startdate = models.DateTimeField()
    e_enddate = models.DateTimeField()
    e_place = models.TextField()
    e_description = models.TextField()
    e_deadline = models.DateTimeField()
    e_postdate = models.DateTimeField()
    e_organizer = models.ForeignKey(User, related_name='e_organizer')
    e_participant = models.ManyToManyField(User,
                                           related_name='e_participant',
                                           through='Participation')
    e_admin = models.ManyToManyField(User, related_name='e_admin')

    def __str__(self):
        return self.e_name


class Participation(models.Model):
    p_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    p_member = models.ForeignKey(User, on_delete=models.CASCADE)
    p_is_paid = models.BooleanField(default=False)

    def __str__(self):
        return "event: %s, member: %s" % (self.p_event, self.p_member)


class Notification(models.Model):
    n_from = models.ForeignKey(User, related_name='n_from')
    n_to = models.ForeignKey(User, related_name='n_to')
    n_timestamp = models.DateTimeField()
    n_content = models.TextField()
    n_read = models.BooleanField(default=False)

    def __str__(self):
        return "sent:%s, from:%s, to:%s" % (self.n_timestamp,
                                            self.n_from,
                                            self.n_to)
