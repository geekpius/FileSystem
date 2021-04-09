from django.db import models


class Zone (models.Model):
    name = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "zones"

    #Methods
    def __str__(self):
        return self.name

    @property
    def get_status(self):
        if self.is_active:
            return 'Deactivate'
        return 'Activate'


class Department (models.Model):
    zone = models.CharField(max_length=60)
    name = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "departments"

    #Methods
    def __str__(self):
        return self.name

    @property
    def get_status(self):
        if self.is_active:
            return 'Deactivate'
        return 'Activate'