from django.shortcuts import render
from django.http import *
from base.models import *
from hydromet.models import *
from datetime import timedelta, datetime
from django.utils import formats

# Create your views here.


def rpluie(request):
    return render(request, "public/rapports.html", {})


def acc(request):
    return render(request, "public/accueil_rapport.html", {})


def json_rap(request):
    """
        Recuperation des donnes et
        Encodage en JSON
    """
    obsv = Observation.objects.select_related('idStation')  # getting all Observation entries in all relationship
    foundCommune = []  # list of all found Commune
    numberFound = []  # occurence of a commune
    sumOfRead = []  # store the sum of rain's quantity
    dep = []
    datex = []
    for qtt in obsv:
        if qtt.idStation.idSiteSeninnelle.sectionCommunale.commune.commune in foundCommune:  # getting the name of the communes
            ids = foundCommune.index(qtt.idStation.idSiteSeninnelle.sectionCommunale.commune.commune)
            numberFound[ids] = numberFound[ids] + 1  # increment the number of occurence of commune
            sumOfRead[ids] = sumOfRead[ids] + float(float(qtt.quantitePluie))
            datex.append(qtt.dateDebut)
        else:
            foundCommune.append(qtt.idStation.idSiteSeninnelle.sectionCommunale.commune.commune)
            numberFound.append(1)
            sumOfRead.append(float(qtt.quantitePluie))
            dep.append(qtt.idStation.idSiteSeninnelle.sectionCommunale.commune.departement.departement)
            datex.append(qtt.dateDebut)

    overAll = []
    for index in range(len(foundCommune)):
        overAll.append({'dep': dep[index], 'com': foundCommune[index], 'date': datex[index],
                        'moy': (sumOfRead[index] / numberFound[index])})  # lack of precision in the date
    reponseJson = {'table': overAll}
    # hh = {'id': 1, 'personne': [{'nom': 'Alexis', 'prenom': 'Rulx Philome'}, {'nom': 'Philers beme', 'prenom': 'Chana'}]}
    # hh = {'f': foundCommune , 'nbr' : numberFound , 'sum' : sumOfRead, 'dep' : dep}
    return JsonResponse(reponseJson)


def imp(request):
    recupAll = Observation.objects.select_related('idStation')
    dd = []
    for e in recupAll:
        dd.append(e)
    return render(request, "public/test.html", {'val': dd})


def json_graph(request):
    datas = Observation.objects.all()
    tous = []
    for info in datas:
        tous.append({'dates': info.dateDebut, 'qtt': info.quantitePluie})

    responsJson = {'table': tous}
    return JsonResponse(responsJson)


def station_map(request):
    departement_lst = Departement.objects.all();
    return render(request, "public/map_stations.html", {'departement_lst': departement_lst})


def json_map(request):
    stations_list = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for station in Station.objects.all():
        observation = Observation.objects.filter(idStation=station.id).order_by('-pk').first()
        if not observation:
            quantite_pluie = '-'
            statut = 'off_activity'
            date_update = ''
        else:
            quantite_pluie = observation.quantitePluie
            statut = 'high_activity'
            date_update = datetime.combine(observation.dateFin, datetime.min.time())

        if date_update and date_update >= today:
            statut = 'high_activity'
        elif date_update and date_update < today and date_update >= today-timedelta(days=7):
            statut = 'low_activity'
        elif date_update:
            statut = 'no_activity'

        format_date = formats.date_format(date_update, "SHORT_DATE_FORMAT") if date_update else '--'

        stations_list.append(
            {'nomStation': station.nomStation, 'latitude': station.latitude, 'longitude': station.longitude,
             'qt': quantite_pluie, 'statut': statut, 'dateUpdate' : format_date, 'today': today})

    return JsonResponse({'stations_lst': stations_list})
    # return HttpResponse(stations)
