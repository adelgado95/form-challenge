import requests
from django.views.generic.base import TemplateView
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Persona
from formadmin import settings

COUNTRIES_DATA = {
    'es': {
        'thanks_text' : 'Enhorabuena, gracias por registrate desde España!!!',
        'country_name': 'España',
        'flag' : 'https://ipdata.co/flags/es.png'
    },
    'pe': {
        'thanks_text' : 'Felicidades, gracias por registrate desde Perú !!!',
        'country_name': 'Perú',
        'flag' : 'https://ipdata.co/flags/pe.png'
    },
    'us' : {
        'thanks_text' : 'Congrats, thanks for register from United States !!!',
        'country_name': 'United States',
        'flag' : 'https://ipdata.co/flags/us.png'
    },
    'mx': {
        'thanks_text' : 'Felicidades, gracias por registrate desde México !!!',
        'country_name': 'México',
        'flag' : 'https://ipdata.co/flags/mx.png'
    },
    'ni': {
        'thanks_text' : 'Felicidades, gracias por registrate desde Nicaragua !!!',
        'country_name': 'Nicaragua',
        'flag' : 'https://ipdata.co/flags/ni.png'
    },
}


class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

@csrf_exempt
def add_person(request):
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    email = request.POST.get('email')
    Persona.objects.create(nombre=nombre, apellido=apellido, email=email)
    ip = get_client_ip(request)
    data = get_data_by_ip(ip)
    cdata = None
    try:
        code = str(data['country_code']).lower()
        cdata = COUNTRIES_DATA['code']
        cdata.update(data)
    except:
       cdata =  {
            'thanks_text' : 'Felicidades, gracias por registrate desde Nicaragua !!!',
            'country_name': 'Nicaragua',
            'flag_image' : 'https://ipdata.co/flags/ni.png'
        }
    return render(request, 'index/skull.html', context=cdata)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]        
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_data_by_ip(ip):
    api_key = settings.IP_DATA_APIKEY
    url = 'https://api.ipdata.co/{0}?api-key={1}'.format(ip, api_key)
    r = requests.get(url)
    return r.json()

