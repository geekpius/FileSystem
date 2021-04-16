from django.conf import settings
from django.db import models
from accounts.models import User

class File (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="files", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20)
    file = models.FileField(upload_to='files')
    status = models.IntegerField(default=1)
    receiver = models.ForeignKey(User, related_name="receivers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "files"

    #Methods
    def __str__(self):
        return self.name

    # @property
    # def get_status(self):
    #     if self.is_active:
    #         return 'Deactivate'
    #     return 'Activate'