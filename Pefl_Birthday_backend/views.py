from django.shortcuts import render, get_object_or_404, get_list_or_404
from managers.models import *
from managers.functions import *
import sys
from lxml import etree
from itertools import islice
import lxml.html as html
from lxml import etree
import logging


logger = logging.getLogger(__name__)


def index_view(request):
    data = {

    }
    return render(request, 'index.html', data)


def download_chemp(request):
    pefl_url = 'http://pefl.ru/'
    # print('ssss')
    # logger.error(pefl_url)
    doc = text_from_link(pefl_url)

    # ссылка на Турниры
    url = pefl_url + find_link_by_link_text(doc, ' Турниры')
    doc = text_from_link(url)

    elements = doc.xpath('//a[contains(@href, "plug.php?p=refl&t=t&")]')

    chemps = []
    divs = []
    commands = []

    # составлям список стран
    for links in elements:
        link = links.get('href').replace('plug.php?p=refl&t=t&j=', '!')
        text = links.text
        chemps.append([text, link])

    chemps = sorted(set(map(tuple, chemps)), reverse=False)

    count_chemp = len(chemps)

    Chemps.objects.all().delete()
    Chemps.objects.bulk_create(
        Chemps(name=name, link=link) for name, link in chemps)


    print('Всего стран =', len(chemps))
    print('Составлям список дивизионов')

    count = 0
    count_all = 0

    for name, link in chemps:
        chemp = name
        chemp_link = link.replace('!', 'plug.php?p=refl&t=t&j=')

        count += 1
        print(count, 'страна из', count_chemp)
        doc = text_from_link3(pefl_url + chemp_link, count+1)
        number = 0

        # составлям список дивизионов
        elements = doc.xpath('//td/a[contains(@href, "plug.php?p=refl&t=v&")]')
        for links in elements:
            div_link = links.get('href').replace('plug.php?p=refl&t=v&j=', '!')
            div = links.text
            count_all += 1
            number += 1

            try:
                chemp_id = Chemps.objects.get(name__iexact=chemp)
            except Exception:
                chemp_id = None

            divs.append([chemp_id, div, div_link, number])

        # break

    # print(divs)

    Divs.objects.all().delete()
    Divs.objects.bulk_create(
        Divs(chemp=chemp_id, name=name, link=link, sort=number) for chemp_id, name, link, number in divs)

    print('Всего дивизионов =', count_all)
    print('Составлям список команд')

    count = 0
    count_commands = 0

    for chemp_id, name, link, number in divs:
        div = name
        div_link = link = link.replace('!', 'plug.php?p=refl&t=v&j=')
        count += 1

        try:
            div_id = Divs.objects.get(name__iexact=div, chemp=chemp_id)
        except Exception:
            div_id = None

        if count_commands // 5 == count_commands / 5:
            print(count, 'дивизион из', count_all)

        doc = text_from_link(pefl_url + div_link)

        # ссылка на Таблицу
        url = pefl_url + find_link_by_link_text(doc, 'Таблица')
        doctxt = text_from_link2(url)

        json_list = []
        for s in doctxt.split('\n'):
            if s.startswith('getjson'):
                json_list = s.split('\'')
                # print(json_list)
                url = json_list[1]

        json_text = text_from_json(pefl_url + 'json.php?' + url)
        command_list = []
        for text in json_text['data']:
            # print(text[1]);
            command_list.append(text[1].split('|'))
        # print(command_list)

        for command in command_list:
            commands.append([div_id, command[0], '!' + command[1]])

        # if count == 3:
        #     break

    # print(commands)

    count_all = len(commands)

    # очищаем список команд
    Teams.objects.all().delete()

    info_for_adding = []
    count = 0

    # print(commands)

    for div_id, command, command_link in commands:
        count += 1

        info_for_adding.append([div_id, command, command_link])

        if count // 100 == count / 100:
            print(count, 'из', count_all)

        if count // 100 == count / 100:
            # Добавляем их
            Teams.objects.bulk_create(
                Teams(div=div_id, name=command, link=command_link) for
                div_id, command, command_link in info_for_adding)
            info_for_adding = []

    # Добавляем оставшиеся
    Teams.objects.bulk_create(
        Teams(div=div_id, name=command, link=command_link) for
        div_id, command, command_link in info_for_adding)

    print('Всего команд:', count)
    data = {
        # 'text1': 'Всего стран =' + str(len(chemps)),
        'text1': pefl_url,
    }
    return render(request, 'download.html', data)


def download(request):
    pefl_url = 'http://pefl.ru/'

    print('старт')

    # очищаем список менеджеров
    Manager.objects.all().delete()

    # # Добавляем их
    # Managers2.objects.bulk_create(Managers2(nickname=name, link_manager=link) for name, link in links_for_job)

    links_for_job = ManagerLink.objects.all()

    gender_list = Gender.objects.all()
    team_list = Teams.objects.all()

    # print(links_for_job)

    count_all = len(links_for_job)

    # count_all = 14725
    print(count_all)

    # for d in links_for_job:
    #     print(len(d))
    #     break

    info_for_adding = []

    count = 0

    # f = open('text.txt', 'w')

    for d in links_for_job:
        # if d.nickname == 'Lestius':
        nickname = d.nickname
        link0= d.link
        link = 'users.php?m=details&id='+link0
        # print(link0, link)
        count += 1
        doc = text_from_link(pefl_url + link)
        elements = doc.xpath('//td/a[contains(@href, "plug.php?p=refl&t=k&")]')
        if not elements:
            info_link_team = None
            info_team = None
        else:
            for links in elements:
                info_link_team = links.get('href')
                # print(info_link_team)
                # 'http://pefl.ru/plug.php?p=refl&t=k&j='
                info_team = links.text

        # фото
        elements = doc.xpath('//a[contains(@href, "plug.php?p=photo&")]')
        for links in elements:
            link_photo = links.get('href')

        tmp = doc.xpath("//td/b[contains(., 'День рождения :')]/../following-sibling::td/text()")
        info_birthday = tmp[0] if tmp and tmp[0] != '---' else None
        tmp = doc.xpath("//td/b[contains(., 'Пол :')]/../following-sibling::td/text()")
        info_gender_text = tmp[0] if tmp else None

        gender = None
        if not info_gender_text:
            gender = None
        else:
            gender = Gender.objects.get(name__iexact=info_gender_text)

        if not info_link_team:
            info_link_team = None
        elif "&j=0&" in info_link_team or "&j=&" in info_link_team:
            info_link_team = None

        team_id = None

        # print(info_link_team)

        if not info_link_team:
            team_id = None
        else:
            info_link_team = info_link_team.replace('http://pefl.ru/', '')
            info_link_team = info_link_team.replace('http://www.pefl.ru/', '')
            info_link_team = info_link_team.replace('plug.php?p=refl&t=k&j=','!')
            try:
                team_id = Teams.objects.get(link=info_link_team)
            except Exception:
                team_id = None
                print(nickname, link, info_link_team)
        # print(nickname, link, info_link_team, team_id)

        manager = ManagerLink.objects.get(nickname__iexact=nickname)

        if "&j=all&z" in link_photo:
            link_photo = None

        if link_photo:
            link_photo = link_photo.replace('http://pefl.ru/', '')
            link_photo = link_photo.replace('http://www.pefl.ru/', '')
            link_photo = link_photo.replace('plug.php?p=photo&j='+link0+'&z=', '')


        link = link.replace('http://pefl.ru/', '')
        link = link.replace('http://www.pefl.ru/', '')

        info_for_adding.append(
            [manager, nickname, link, info_birthday, gender, link_photo, team_id, info_link_team])

        if count // 100 == count / 100:
            # Добавляем их
            # print(info_for_adding)
            Manager.objects.bulk_create(
                Manager(manager=manager,
                         birthday=birthday,
                         gender=gender,
                         link_photo=link_photo,
                         team=team_id
                         ) for
                manager, nickname, link, birthday, gender, link_photo, team_id, info_link_team in info_for_adding)
            info_for_adding = []
            # break

        if count // 20 == count / 20:
            print(count, 'из', count_all)


    # Добавляем оставшиеся
    Manager.objects.bulk_create(
        Manager(manager=manager,
                 birthday=birthday,
                 gender=gender,
                 link_photo=link_photo,
                 team=team_id
                 ) for
        manager, nickname, link, birthday, gender, link_photo, team_id, info_link_team in info_for_adding)

    info_for_adding = []

    data = {

    }
    print('конец')
    return render(request, 'download.html', data)

    # return doc











def download_continue(request):
    pefl_url = 'http://pefl.ru/'

    print('старт')

    # очищаем список менеджеров
    # Manager.objects.all().delete()

    # # Добавляем их
    # Managers2.objects.bulk_create(Managers2(nickname=name, link_manager=link) for name, link in links_for_job)

    # links_for_job = ManagerLink.objects.all()

    manager_ids = list(Manager.objects.all().values_list("manager__manager", flat=True))
    # print(manager_ids)
    # print(len(manager_ids))
    links_for_job = ManagerLink.objects.exclude(id__in=manager_ids)

    # print(list(links_for_job.id))

    # print(links_for_job[0])
    gender_list = Gender.objects.all()
    team_list = Teams.objects.all()

    # print(links_for_job)

    count_all = len(links_for_job)

    # count_all = 14725
    print(count_all)

    # for d in links_for_job:
    #     print(len(d))
    #     break

    info_for_adding = []

    count = 0

    # f = open('text.txt', 'w')

    for d in links_for_job:
        # if d.nickname == 'Lestius':
        nickname = d.nickname
        link0= d.link
        link = 'users.php?m=details&id='+link0
        # print(link0, link)
        count += 1
        doc = text_from_link(pefl_url + link)
        elements = doc.xpath('//td/a[contains(@href, "plug.php?p=refl&t=k&")]')
        if not elements:
            info_link_team = None
            info_team = None
        else:
            for links in elements:
                info_link_team = links.get('href')
                # print(info_link_team)
                # 'http://pefl.ru/plug.php?p=refl&t=k&j='
                info_team = links.text

        # фото
        elements = doc.xpath('//a[contains(@href, "plug.php?p=photo&")]')
        for links in elements:
            link_photo = links.get('href')

        tmp = doc.xpath("//td/b[contains(., 'День рождения :')]/../following-sibling::td/text()")
        info_birthday = tmp[0] if tmp and tmp[0] != '---' else None
        tmp = doc.xpath("//td/b[contains(., 'Пол :')]/../following-sibling::td/text()")
        info_gender_text = tmp[0] if tmp else None

        gender = None
        if not info_gender_text:
            gender = None
        else:
            gender = Gender.objects.get(name__iexact=info_gender_text)

        if not info_link_team:
            info_link_team = None
        elif "&j=0&" in info_link_team or "&j=&" in info_link_team:
            info_link_team = None

        team_id = None

        # print(info_link_team)

        if not info_link_team:
            team_id = None
        else:
            info_link_team = info_link_team.replace('http://pefl.ru/', '')
            info_link_team = info_link_team.replace('http://www.pefl.ru/', '')
            info_link_team = info_link_team.replace('plug.php?p=refl&t=k&j=','!')
            try:
                team_id = Teams.objects.get(link=info_link_team)
            except Exception:
                team_id = None
                print(nickname, link, info_link_team)
        # print(nickname, link, info_link_team, team_id)

        manager = ManagerLink.objects.get(nickname__iexact=nickname)

        if "&j=all&z" in link_photo:
            link_photo = None

        if link_photo:
            link_photo = link_photo.replace('http://pefl.ru/', '')
            link_photo = link_photo.replace('http://www.pefl.ru/', '')
            link_photo = link_photo.replace('plug.php?p=photo&j='+link0+'&z=', '')


        link = link.replace('http://pefl.ru/', '')
        link = link.replace('http://www.pefl.ru/', '')

        info_for_adding.append(
            [manager, nickname, link, info_birthday, gender, link_photo, team_id, info_link_team])

        if count // 100 == count / 100:
            # Добавляем их
            # print(info_for_adding)
            Manager.objects.bulk_create(
                Manager(manager=manager,
                         birthday=birthday,
                         gender=gender,
                         link_photo=link_photo,
                         team=team_id
                         ) for
                manager, nickname, link, birthday, gender, link_photo, team_id, info_link_team in info_for_adding)
            info_for_adding = []
            # break

        if count // 20 == count / 20:
            print(count, 'из', count_all)


    # Добавляем оставшиеся
    Manager.objects.bulk_create(
        Manager(manager=manager,
                 birthday=birthday,
                 gender=gender,
                 link_photo=link_photo,
                 team=team_id
                 ) for
        manager, nickname, link, birthday, gender, link_photo, team_id, info_link_team in info_for_adding)

    info_for_adding = []

    data = {

    }
    print('конец')
    return render(request, 'download.html', data)

    # return doc










def download_managerlink(request):
    pefl_url = 'http://pefl.ru/'

    step = 50
    i = 0

    print('старт')
    links_for_job = []

    # очищаем список ссылок на менеджеров
    ManagerLink.objects.all().delete()

    for j in range(10000):
        i += 1
        url = pefl_url + 'users.php?filter=all&sort=name&way=asc&from=' + \
              str(step * i) + '&tc=&nc='
        doc = text_from_link(url)
        elements = doc.xpath('//a[contains(@href, "users.php?m=details")]')
        # составлям список менеджеров
        for links in elements:
            link = links.get('href').replace('users.php?m=details&id=','');
            text = links.text

            links_for_job.append([text, link])

        # проверяем, есть ли ссылка на следующую страницу
        get_next = doc.xpath('//a[contains(@href, "users.php?filter=all&sort=name&way=asc&from=' +
                             str(step * (i + 1)) + '&tc=&nc=")]')
        if get_next is None:
            break

        # if i > 20:
        #     print(links_for_job)
        #     break

        if i // 20 == i / 20:
            print(i)

        if links_for_job == []:
            break

        if i // 100 == i / 100:
            # Добавляем их
            # print(info_for_adding)
            ManagerLink.objects.bulk_create(ManagerLink(nickname=nickname, link=link) for nickname, link in links_for_job)
            links_for_job = []
            # break

    # добавляем оставшиеся
    ManagerLink.objects.bulk_create(ManagerLink(nickname=nickname, link=link) for nickname, link in links_for_job)
    links_for_job = []

    data = {

    }
    print('конец')
    return render(request, 'download.html', data)
