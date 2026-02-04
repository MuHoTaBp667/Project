from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import PsAors, PsAuths, PsEndpoints

def combined_view(request):
    aors_data = PsAors.objects.all().values('id','contact','max_contacts')
    auth_data = PsAuths.objects.all().values('id')
    endpoints_data = PsEndpoints.objects.all().values('id', 'context', 'callerid', 'tnumber', 'transport')
    context = {
        'aors': aors_data,
        'auth': auth_data,
        'endpoints_data': endpoints_data,
    }
    return render(request, 'combined_view.html', context)