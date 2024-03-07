from django.shortcuts import render
from django.middleware.csrf import get_token
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView






class APIPesel:
    API_URL = f'http://api_medicine:8001/clients/get_client_by_pesel/'

    def fetch_data(self, pesel):
        return requests.get(f'{self.API_URL}?pesel={pesel}')

    def parse_data(self, response):
        name = response.get('name')
        last_name = response.get('last_name')
        return {"name": name,
                "last_name": last_name}


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csrf_token'] = get_token(self.request)
        return context

    def post(self, request, *args, **kwargs):
        error_message = None
        pesel = request.POST.get('pesel')
        if pesel:
            api_pesel = APIPesel()
            response = api_pesel.fetch_data(pesel)
            print(response)
            if response.status_code == 200:
                data = api_pesel.parse_data(response.json())
                print(data)
                context = {
                    "title": "Home",
                    "name": data.get("name"),
                    "last_name": data.get("last_name"),
                    "pesel": pesel,
                }
                return render(request, self.template_name, context)
            elif response.status_code == 404:
                error_message = "No PESEL in database"
        else:
            error_message = "Please enter Pesel"

        context = {"title": "Home", "error_message": error_message}
        print(context)
        return render(request, self.template_name, context)












