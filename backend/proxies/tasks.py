
import requests
from core.celery import app

from .models import ProxyServer


@app.task
def check_proxy(id):
    proxy = ProxyServer.objects.get(id=id)
    try:
        proxies = {
            proxy.protocol: f"{proxy.protocol}://{proxy.username}:{proxy.password}@{proxy.address}:{proxy.port}",
        }
        res = requests.get("https://ifconfig.me/", proxies=proxies)
        if not res.status_code == 200:
            raise Exception
        proxy.is_active = True
    except Exception:
        proxy.is_active = False
    finally:
        proxy.save()