import requests
from core.celery import app
from .models import ProxyServer


@app.task
def check_proxy(proxy_server_id):
    try:
        proxy = ProxyServer.objects.get(id=proxy_server_id)
        proxies = {'http': str(proxy)}
        response = requests.get('http://www.httpbin.org/ip', proxies=proxies,)
        resp_data = response.json()

        if resp_data["origin"] != proxy.address:
            raise Exception(f'Ip address{proxy.address} is not equal from http://www.httpbin.org/ip {resp_data["origin"]}')

    except Exception as error:
        proxy.error = str(error)
        proxy.is_active = False
    else:
        proxy.error = None
        proxy.is_active = True
    finally:
        proxy.save()
