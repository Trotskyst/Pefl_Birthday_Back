from rest_framework import serializers
from managers.models import *


class CounriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemps
        fields = ('id', 'name', 'link')


class ManagersListSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(source='manager.nickname', read_only=True)
    link_manager = serializers.CharField(source='manager.link', read_only=True)
    team = serializers.CharField(source='team.name', read_only=True)
    link_team = serializers.CharField(source='team.link', read_only=True)
    div = serializers.CharField(source='team.div.name', read_only=True)
    country = serializers.CharField(source='team.div.chemp.name', read_only=True)

    class Meta:
        model = Manager
        fields = ('manager', 'link_manager', 'country', 'div', 'team', 'link_team', 'gender', 'timestamp', 'birthday', 'link_photo')


class ManagerCountSerializer(serializers.ModelSerializer):
    count_birthday = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        fields = ('count_birthday', )

    def get_count_birthday(self, obj):
        return Manager.objects.exclude(birthday__isnull=True).count()
