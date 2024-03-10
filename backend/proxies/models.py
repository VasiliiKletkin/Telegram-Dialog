from django.db import models
from model_utils.models import TimeStampedModel


class ProxyServer(TimeStampedModel):
    is_active = models.BooleanField(default=False)

    protocol = models.CharField(max_length=10, default='socks5')
    address = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    info_check_proxy = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.address}:{self.port}"

    def get_proxy_dict(self):
        return {
            'proxy_type': self.protocol,
            'addr': self.address,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'rdns': True
        }
