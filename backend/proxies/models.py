from django.db import models
from model_utils.models import TimeStampedModel
import requests


class ProxyServer(TimeStampedModel):
    SOCKS5 = "socks5"
    SOCKS4 = "socks4"

    PROTOCOL_CHOICE = ((SOCKS5, "Socks5"), (SOCKS4, "Socks4"))

    is_active = models.BooleanField(default=False)

    protocol = models.CharField(
        max_length=10,
        choices=PROTOCOL_CHOICE,
        default=SOCKS5,
    )
    address = models.CharField(max_length=100, unique=True)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    errors = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.address}:{self.port}"

    @property
    def is_ready(self):
        return self.is_active and not self.errors

    def check_obj(self):
        try:
            proxies = {"http": str(self)}
            response = requests.get(
                "http://www.httpbin.org/ip",
                proxies=proxies,
            )
            resp_data = response.json()

            if resp_data["origin"] != self.address:
                raise Exception(
                    f'Ip address{self.address} is not equal from http://www.httpbin.org/ip {resp_data["origin"]}'
                )

        except Exception as error:
            self.error = str(error)
        else:
            self.error = None
        finally:
            self.save()

    def get_proxy_dict(self):
        return {
            "proxy_type": self.protocol,
            "addr": self.address,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "rdns": True,
        }
