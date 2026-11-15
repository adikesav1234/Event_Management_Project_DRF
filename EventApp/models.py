from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EventDb(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventMemberDb(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='event_members')
    event = models.ForeignKey(EventDb,on_delete=models.CASCADE,related_name='event_details')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['event','user'],name='unique_event_member')]

    def __str__(self):
        return f"{self.user.username}-{self.event.title}"
    
