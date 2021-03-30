from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, account_type, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not account_type:
            raise ValueError('Users must have account type')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            account_type=account_type,
        )

        user.is_active = True
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, account_type, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
            account_type=account_type,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=60)
    account_type = models.CharField(max_length=20)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    owner = models.BigIntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','account_type']

    objects = MyUserManager()

    class Meta:
        db_table = "account_users"

    def __str__(self):
        return f"{self.email}"

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def capitalize_account_type(self):
        return capitalize(self.account_type)



class Profile (models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True)
    zone = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=80, null=True)
    image = models.ImageField(upload_to="users", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        db_table = "user_profiles"

    #Methods
    def __str__(self):
        return f"{self.user}"


    @property
    def get_user_image(self):
        if self.image:
            return self.image.url
        return 'assets/images/user.svg'