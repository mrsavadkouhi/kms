import time
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse


def get_avatar_directory_path(instance, filename):
    return 'users/%d_avatar_%s' % (int(time.time()), filename)


PERMISSIONS = [
    ('knowledge', 'مدیریت دانش'),
    ('center', 'رشد، خلاقیت و نوآوری'),
    ('resume', 'آموزش و امور محققین'),
    ('future', 'آینده پژوهی'),
]


class Permission(models.Model):
    code = models.CharField(max_length=30, choices=PERMISSIONS)

    def __str__(self):
        return self.code


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_avatar_directory_path, max_length=255, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mobile_number = models.CharField(max_length=11, verbose_name='تلفن همراه', unique=True)
    permissions = models.ManyToManyField(to=Permission, blank=True, verbose_name='دسترسی ها')

    @property
    def has_no_perms(self):
        if self.permissions.all().count():
            return False
        return True

    def has_perms(self, perms):
        if self.permissions.filter(code__in=perms).count():
            return True
        return False

    def get_absolute_url(self):
        return reverse('accounts:profile_details', kwargs={'pk': self.id})


@receiver(pre_save, sender=Profile, dispatch_uid="delete_old_avatar_image_before_save")
def delete_old_avatar_image(sender, instance, raw, update_fields, **kwargs):
    try:
        obj = Profile.objects.get(id=instance.id)
        if obj.avatar != instance.avatar:
            obj.avatar.delete(save=False)
    except Exception:
        pass


@receiver(pre_delete, sender=Profile, dispatch_uid='delete_avatar_file_on_object_delete')
def delete_avatar_media(sender, instance, using, **kwargs):
    instance.avatar.delete(save=False)
