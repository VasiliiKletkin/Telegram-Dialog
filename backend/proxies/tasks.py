import json
from core.celery import app
from proxy_checker import ProxyChecker
from .models import ProxyServer


@app.task
def check_proxy(id):
    proxy = ProxyServer.objects.get(id=id)
    checker = ProxyChecker()
    check_proxy = checker.check_proxy(f"{proxy.address}:{proxy.port}", user=proxy.username, password=proxy.password)
    proxy.is_active = True if check_proxy else False
    proxy.info_check_proxy = json.dumps(check_proxy)
    proxy.save()
