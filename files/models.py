from django.conf import settings
from django.db import models
from accounts.models import User

class File (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="files", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "files"

    #Methods
    def __str__(self):
        return self.name


class FileReciever (models.Model):
    PENDING = "pending"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WORK_DONE = "work done"
    file = models.ForeignKey(File, related_name="file_receivers", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receivers", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "file_recivers"

    #Methods
    def __str__(self):
        return self.receiver.name


class ArchiveFile (models.Model):
    RESENT = 1
    REJECTED = 0
    ACCEPTED = 2
    FORWARDED = 3
    file = models.ForeignKey(File, related_name="archive_files", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_archive_files", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "archive_files"

    #Methods
    def __str__(self):
        return self.file


class ForwardFile (models.Model):
    file = models.ForeignKey(File, related_name="forward_files", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_forward_files", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "forward_files"

    #Methods
    def __str__(self):
        return self.file


class ForwardFileReceiver (models.Model):
    PENDING = 1
    REJECTED = 0
    ACCEPTED = 2
    forward_file = models.ForeignKey(ForwardFile, related_name="forward_file_receivers", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="forward_receivers", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "forward_file_recivers"

    #Methods
    def __str__(self):
        return self.receiver.name



class OldFile (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="old_files", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20)
    file = models.FileField(upload_to='oldfiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "old_files"

    #Methods
    def __str__(self):
        return self.name

