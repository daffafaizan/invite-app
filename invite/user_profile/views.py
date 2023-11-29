from django.shortcuts import render
from find_teams.models import Lamaran

# Create your views here.
def delete_application(request, application_id):
    lamaran = Lamaran.objects.get(id=application_id)
    lamaran.delete()

    return render(request, "vacancies.html")