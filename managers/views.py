import rest_framework
from rest_framework import generics
from managers.serializers import *
from managers.models import *
from django.db.models.functions import Extract

class ManagersListAllView(generics.ListAPIView):
    """Список всех менеджеров"""
    serializer_class = ManagersListSerializer
    queryset = Manager.objects.all()


class ManagersListMonthView(generics.ListAPIView):
    """Список всех менеджеров на выбранный месяц"""
    serializer_class = ManagersListSerializer

    def get_queryset(self):
        month = self.kwargs['month']
        queryset = Manager.objects.filter(birthday__month=month)
        return queryset


class ManagersListDayView(generics.ListAPIView):
    """Список всех менеджеров на указанную дату"""
    serializer_class = ManagersListSerializer

    def get_queryset(self):
        month = self.kwargs['month']
        day = self.kwargs['day']
        queryset = Manager.objects.filter(birthday__month=month, birthday__day=day)
        return queryset


class ManagersListLetterView(generics.ListAPIView):
    """Список всех менеджеров на указанную букву"""
    serializer_class = ManagersListSerializer

    def get_queryset(self):
        letter = self.kwargs['letter']
        if len(letter) == 1:
            queryset = Manager.objects.filter(manager__nickname__istartswith=letter).exclude(
                birthday__isnull=True).order_by(
                'manager__nickname')
        else:
            queryset = Manager.objects.all().exclude(birthday__isnull=True).exclude(
                manager__nickname__istartswith='q').exclude(manager__nickname__istartswith='s').exclude(
                manager__nickname__istartswith='w').exclude(manager__nickname__istartswith='d').exclude(
                manager__nickname__istartswith='e').exclude(manager__nickname__istartswith='f').exclude(
                manager__nickname__istartswith='r').exclude(manager__nickname__istartswith='g').exclude(
                manager__nickname__istartswith='t').exclude(manager__nickname__istartswith='h').exclude(
                manager__nickname__istartswith='y').exclude(manager__nickname__istartswith='j').exclude(
                manager__nickname__istartswith='u').exclude(manager__nickname__istartswith='k').exclude(
                manager__nickname__istartswith='i').exclude(manager__nickname__istartswith='l').exclude(
                manager__nickname__istartswith='o').exclude(manager__nickname__istartswith='z').exclude(
                manager__nickname__istartswith='p').exclude(manager__nickname__istartswith='x').exclude(
                manager__nickname__istartswith='c').exclude(manager__nickname__istartswith='v').exclude(
                manager__nickname__istartswith='b').exclude(manager__nickname__istartswith='n').exclude(
                manager__nickname__istartswith='m').exclude(manager__nickname__istartswith='a').order_by(
                'manager__nickname')
        return queryset


class ChempsCountriesView(generics.ListAPIView):
    """Список стран"""
    serializer_class = CounriesListSerializer
    queryset = Chemps.objects.all()


class ManagersCountryView(generics.ListAPIView):
    """Список менеджеров из выбранной страны"""
    serializer_class = ManagersListSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        queryset = Manager.objects.filter(team__div__chemp__name__iexact=country).exclude(
            birthday__isnull=True).annotate(b_month=Extract('birthday', 'month')).annotate(
            b_day=Extract('birthday', 'day')).order_by(
            'b_month', 'b_day', 'team__div__sort', 'manager__nickname')
        return queryset


class ManagersWomanView(generics.ListAPIView):
    """Список девушек"""
    serializer_class = ManagersListSerializer

    def get_queryset(self):
        queryset = Manager.objects.filter(gender__name__iexact='Женский').exclude(birthday__isnull=True)
        return queryset


class ManagersCountView(generics.ListAPIView):
    """Количество менеджеров в базе с днями рождения"""
    serializer_class = ManagerCountSerializer

    def get_queryset(self):
        queryset = Manager.objects.all()[:1]
        return queryset
