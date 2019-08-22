from django.db import models
import datetime


class Gender(models.Model):
    name = models.CharField(max_length=10, verbose_name='Пол')

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'
        # ordering = [id, ]

    def __str__(self):
        return self.name


class Chemps(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    name = models.CharField(verbose_name='Чемпионат', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на чемпионат', db_index=True, max_length=1000)

    class Meta:
        verbose_name = 'Чемпионат'
        verbose_name_plural = 'Чемпионаты'
        ordering = ['name']

    def __str__(self):
        return self.name

class Divs(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    chemp = models.ForeignKey(Chemps, verbose_name='Чемпионат', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Дивизион', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на дивизион', db_index=True, max_length=1000)
    sort = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Дивизион'
        verbose_name_plural = 'Дивизионы'
        ordering = ['sort']

    def __str__(self):
        return self.name


class Teams(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Команда', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на команду', db_index=True, max_length=1000)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['name']

    def __str__(self):
        return self.name


class ManagerLink(models.Model):
    nickname = models.CharField(verbose_name='Имя пользователя', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на пользователя', null=True, blank=True, max_length=4000)

    class Meta:
        verbose_name = 'Ссылки на менеджеров'
        verbose_name_plural = 'Ссылки на менеджеров'
        ordering = ['nickname']

    def __str__(self):
        return self.nickname


class Manager(models.Model):

    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    gender = models.ForeignKey(Gender, verbose_name='Пол', on_delete=models.CASCADE, null=True, blank=True)
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True, db_index=True)
    manager = models.ForeignKey(ManagerLink, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Teams, verbose_name='Команда', on_delete=models.CASCADE, null=True, blank=True)
    link_photo = models.CharField(verbose_name='Ссылка на фото', null=True, blank=True, max_length=4000)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
        ordering = ['manager']

    def __str__(self):
        return self.manager.nickname


