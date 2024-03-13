import json
import requests
from core.celery import app
from .models import ProxyServer


print()


@app.task
def check_proxy(id):
    proxy = ProxyServer.objects.get(id=id)

    proxies = {
        'http': str(proxy)
    }
    response = requests.get('http://www.httpbin.org/ip', proxies=proxies,)
    resp_data = response.json()
    proxy.is_active = True if resp_data["origin"] == proxy.address else False
    proxy.info_check_proxy = json.dumps(resp_data)
    proxy.save()
