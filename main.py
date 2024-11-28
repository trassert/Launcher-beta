import zipfile
import requests
import flet as ft

from sys import exit
from time import sleep
from modules import db
from subprocess import check_output
from os import getcwd, path, remove, mkdir
from minecraft_launcher_lib.utils import get_minecraft_directory

title = 'Trassert : Лаунчер'
p_load = 'Загрузка'
other = 'Лаунчер уже запущен'
no_v6 = 'У вас нет IPv6'
no_conn = 'Сервер обновлений недоступен'
find_upd = 'Поиск обновлений'
prog_upd = 'Обновляю лаунчер'
mods_upd = 'Обновляю моды'
unzipping = 'Распаковка'
update_success = 'Обновление прошло успешно'


minecraft_directory = get_minecraft_directory(
    ).replace('minecraft', 'trassert')

t = 2
current_running = []
default_version = 12


def is_process_running():
    'Проверка на двойной запуск'
    try:
        output = check_output("tasklist /FI \"IMAGENAME eq flet.exe\"")
        return 'flet.exe' in str(output).replace('flet.exe', '', 1)
    except:
        return False


server = 'trassert.ddns.net:5000'


def main(page):
    current_running.append(1)
    page.title = title
    page.window.center()
    page.window.width = 400
    page.window.height = 150
    page.window.visible = True
    page.update()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    text = ft.Text(
        value=p_load,
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.PRIMARY
    )
    page.add(text)

    'Если уже запущен'
    if is_process_running():
        text.value = other
        text.color = ft.colors.ERROR
        page.update()
        sleep(t)
        page.window.destroy()
        exit(0)

    mods_version = db.settings('mods_version')
    if mods_version is None:
        mods_version = 37
        db.settings('mods_version', 37)

    launcher_version = db.settings('launcher_version')
    if launcher_version is None:
        launcher_version = default_version
        db.settings('launcher_version', default_version)

    'Если нет интернета'
    try:
        text.value = find_upd
        text.color = ft.colors.PRIMARY
        page.update()
        launcher_newest_version = requests.get(
            f'http://{server}/version'
            '?q=prog'
            f'&version={launcher_version}',
            timeout=5
            ).text
        current_need_update = 0
        while 'True' not in launcher_newest_version:
            text.value = prog_upd
            page.update()
            current_need_update = int(launcher_newest_version)
            response = requests.get(
                f'http://{server}/download'
                f'?q=prog&version={launcher_newest_version}', timeout=5)
            text.value = unzipping
            page.update()
            with open("archive.zip", mode="wb") as file:
                file.write(response.content)
            zipfile.ZipFile("archive.zip", 'r').extractall(getcwd())
            remove('archive.zip')
            if path.isfile('delfile.txt'):
                with open('delfile.txt', 'r') as f:
                    for x in f.readlines():
                        try:
                            remove(x.replace('\n', ''))
                        except:
                            pass
                remove('delfile.txt')
            launcher_newest_version = requests.get(
                f'http://{server}/version'
                f'?q=prog&version={launcher_newest_version}',
                timeout=5).text
        'Если лаунчер обновился'
        if current_need_update != 0:
            db.settings('launcher_version', current_need_update)
            text.value = update_success
            page.update()
        current_need_update = 0
        text.value = find_upd
        page.update()
        mods_newest_version = requests.get(
            f'http://{server}/version'
            f'?q=mods&version={mods_version}',
            timeout=5).text
        while 'True' not in mods_newest_version:
            text.value = mods_upd
            page.update()
            current_need_update = int(mods_newest_version)
            response = requests.get(
                f'http://{server}/download'
                f'?q=mods&version={mods_newest_version}', timeout=5)
            text.value = unzipping
            page.update()
            
            'Если директории майнкрафта ещё нет'
            if not path.exists(minecraft_directory):
                mkdir(path.join(minecraft_directory, 'mods'))
            with open(
                path.join(minecraft_directory, 'archive.zip'), mode="wb"
            ) as file:
                file.write(response.content)
            'Распаковка архива'
            zipfile.ZipFile(
                path.join(minecraft_directory, 'archive.zip')
                ).extractall(
                    path.join(minecraft_directory, 'mods')
                    )
            'Удаление архива'
            remove(path.join(minecraft_directory, 'archive.zip'))
            if path.isfile(
                path.join(
                    minecraft_directory,
                    'mods',
                    'delfile.txt'
                )
            ):
                'Если нужно удалять какие либо моды'
                with open(
                    path.join(minecraft_directory, 'mods', 'delfile.txt'), 'r'
                ) as f:
                    for unnecessary_mods in f.readlines():
                        'Построчное удаление'
                        try:
                            remove(
                                path.join(
                                    minecraft_directory,
                                    'mods',
                                    unnecessary_mods.replace('\n', '')
                                    )
                                )
                        except:
                            pass
                remove(
                    path.join(
                        minecraft_directory,
                        'mods',
                        'delfile.txt'
                    )
                )
            mods_newest_version = requests.get(
                f'http://{server}/version'
                f'?q=mods&version={mods_newest_version}',
                timeout=5
                ).text
        'Если моды обновились'
        if current_need_update != 0:
            db.settings('mods_version', current_need_update)
            text.value = update_success
            page.update()
    except requests.exceptions.ConnectionError:
        text.value = no_conn
        text.color = ft.colors.ERROR
        page.update()
        sleep(t)
    current_running.remove(1)
    page.window.close()


ft.app(target=main, name='trassert')
if current_running == []:
    'Проверка на двойной запуск'
    from launcher import launcher
    ft.app(target=launcher, name='trassert')
