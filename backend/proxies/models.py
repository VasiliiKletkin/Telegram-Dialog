from django.db import models


class ProxyServer(models.Model):
    is_active = models.BooleanField(default=True)

    type = models.CharField(max_length=10, default='socks5')
    address = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.is_active} {self.type}  {self.address}:{self.port}:{self.username}:{self.password}"

    def get_proxy_dict(self):
        return {
            'proxy_type': self.type,
            'addr': self.address,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'rdns': True
        }
