from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
#from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, nickname, email, password, **extra_fields):
        if not user_id:
            raise ValueError('Users require an id field')
        if not nickname:
            raise ValueError('Users require a nickname field')
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, nickname, email, password=None, **extra_fields):
        return self._create_user(user_id, nickname, email, password, **extra_fields)

    def create_superuser(self, user_id, nickname, email, password, **extra_fields):
        user = self.create_user(
            user_id=user_id,
            nickname=nickname,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=20, primary_key=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now
        self.save(update_fields=['deleted_at'])

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'nickname', ]

    def __str__(self):
        return self.nickname


class Size(models.Model):
    Left_Right = {
        ('left', '왼발'),
        ('right', '오른발'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    left_right = models.CharField(null=False, max_length=10, choices=Left_Right)
    length = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)


class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class Shoe(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    price = models.IntegerField()
    # 크롤링한 정보 데베에 저장해야 할지 말아야 할지 찾아보기


class Review(models.Model):
    Length_Recommendation = {
        ('long', '길어요'),
        ('normal', '적당해요'),
        ('short', '짧아요'),
    }
    Width_Recommendation = {
        ('wide', '넓어요'),
        ('normal', '적당해요'),
        ('narrow', '좁아요'),
    }
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.CharField(null=True, max_length=10, choices=Length_Recommendation)
    width = models.CharField(null=True, max_length=10, choices=Width_Recommendation)
    # content = models.TextField()
    # star_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # 별점은 (저장된 값/2)


class Style(models.Model):
    style_name = models.CharField(max_length=30)
    description = models.TextField()
    characteristics = models.TextField()


class StyleImage(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, primary_key=True)
    image = models.TextField()  # 이미지 url 저장


class StyleMatch(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)


class UserStyle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    style = models.CharField(max_length=50)  # 유사도 높은 style id 순서대로 저장(','로 구분하고 이용할 때 리스트로 파싱)
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
