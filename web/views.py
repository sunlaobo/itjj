from django.shortcuts import render
from models import Proxy

# Create your views here.
def index(request):
    latest_question_list = Proxy.objects.order_by('-create_time')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'index.html', context)