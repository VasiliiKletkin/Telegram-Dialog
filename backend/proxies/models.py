from django.db import models


class ProxyServer(models.Model):
    is_active = models.BooleanField(default=False)

    protocol = models.CharField(max_length=10, default='socks5')
    address = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

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
