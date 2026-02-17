from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import PsAors, PsAuths, PsEndpoints
from .forms import RegistrationForm

def combined_view(request):
    # получаем данные из 3 таблиц
    aors_data = PsAors.objects.all().values('id','contact','max_contacts')
    auth_data = PsAuths.objects.all().values('id')
    endpoints_data = PsEndpoints.objects.all().values('id', 'context', 'callerid', 'tnumber', 'transport')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
             # если запросотправлен методом пост создаем объект класса RegistrationForm
        if form.is_valid():
            id_value = form.cleaned_data['ID']
            callerid_value = form.cleaned_data['CallerID']
            tnumber_value = form.cleaned_data['Tnumber']
            context_value = form.cleaned_data['ContextRF']
            # если форма "валидна" получаем очищенные данные
            PsAors.objects.create(
                id=id_value,
                max_contacts=2
            )
            PsAuths.objects.create(id=id_value)

            PsEndpoints.objects.create(
                id=id_value,
                context=context_value,
                callerid=callerid_value,
                tnumber=tnumber_value,
                transport='transport-udp',
                disallow='all', 
                allow='alaw,ulaw',  
                direct_media='yes')
            # добавляем записи в таблицы
            return redirect('combined_view')
            # перенаправляем пользователя после заполнения формы
    else:
        form = RegistrationForm()


    context = {
        'aors': aors_data,
        'auth': auth_data,
        'endpoints_data': endpoints_data,
        'form': form,
    }
    return render(request, 'combined_view.html', context)
    # берем шаблон страницы подставляем в него данные из контекста возвращаем это обратно уже с данными