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
    },
    'pe': {
        'thanks_text' : 'Felicidades, gracias por registrate desde Perú !!!',
    },
    'us' : {
        'thanks_text' : 'Congrats, thanks for register from United States !!!',
    },
    'mx': {
        'thanks_text' : 'Felicidades, gracias por registrate desde México !!!',
    },
    'ni': {
        'thanks_text' : 'Felicidades, gracias por registrate desde Nicaragua !!!',
    },
    'ger': {
        'thanks_text' : 'Felicidades, gracias por registrate desde Alemania !!!',
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
    cdata = {}
    cdata.update(data)
    try:
        code = str(data['country_code']).lower()
        thanks_text = COUNTRIES_DATA[code]['thanks_text']
        cdata.update({'thanks_text': thanks_text})
    except:
       cdata =  {
            'thanks_text' : 'Felicidades, gracias por registrate desde Nicaragua-DefaultMessagge',
            'country_name': 'Nicaragua-DefaultCountry',
            'flag_image' : 'https://ipdata.co/flags/ni.png'
        }
    cdata.update({
        'cdata': cdata
    })
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

