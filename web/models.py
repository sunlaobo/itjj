#coding: utf8
from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Proxy(models.Model):
    ip=models.CharField('IP',max_length=30,db_index=True)
    port=models.IntegerField('端口',db_index=True)
    type=models.CharField('代理类型',max_length=10,default='http')
    country=models.CharField('地区',max_length='100',default='',null=True)
    create_time = models.DateTimeField('入库时间',default=timezone.now)

    def __unicode__(self):
        return u'%s:%s' % (self.ip, self.port)

    def was_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)

