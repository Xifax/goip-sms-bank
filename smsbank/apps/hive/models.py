# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    """GSM module, provided by GOIP SMS bank"""
    ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField(verbose_name=u'порт')
    online = models.NullBooleanField(
        default=False,
        blank=True,
        verbose_name=u'онлайн'
    )

    # Additional properties
    imei = models.CharField(max_length=17, null=True, blank=True)
    device_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('ip', 'port')

        verbose_name = u'устройство'
        verbose_name_plural = u'устройства'

    def __unicode__(self):
        return u'%s:%d [%s]' % (
            self.ip,
            self.port,
            u'онлайн' if self.online else u'оффлайн'
        )


class Sms(models.Model):
    """SMS, send or received by device"""
    recipient = models.CharField(max_length=100, verbose_name=u'получатель')
    message = models.CharField(max_length=10000, verbose_name=u'сообщение')

    # Set current datetime on creation
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    device = models.ForeignKey(
        Device,
        null=True,
        blank=True,
        verbose_name=u'устройство'
    )

    class Meta:
        verbose_name = u'смс'
        verbose_name_plural = u'смс'

    def __unicode__(self):
        return u'[%s]%s:%s' % (self.date, self.recipient, self.message)


class DeviceList(models.Model):
    """Lists devices associated with user"""
    user = models.ForeignKey(
        User,
        related_name='device_list',
        verbose_name=u'пользователь'
    )

    devices = models.ManyToManyField(
        Device,
        related_name='profiles',
        null=True,
        blank=True,
        verbose_name=u'устройства'
    )

    class Meta:
        verbose_name = u'устройство пользователя'
        verbose_name_plural = u'устройства пользователя'

    def __unicode__(self):
        return u'%s' % self.user.username
        # return u'%s' % u', '.join([str(d) for d in self.devices])
