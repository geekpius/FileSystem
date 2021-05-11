from django.conf import settings
from django.db import models

class Support (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="supports", on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    subject = models.CharField(max_length=60)
    message = models.TextField()
    is_served = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "supports"

    #Methods
    def __str__(self):
        return self.subject

