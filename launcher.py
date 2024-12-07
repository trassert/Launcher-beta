import requests
import flet as ft
import subprocess
import minecraft_launcher_lib as minecraft_launcher

from time import sleep
from flet import Theme
from modules import db
from random import choice
from os import path, replace
from psutil import _psutil_windows as cext
from minecraft_launcher_lib.utils import get_minecraft_directory


minecraft_directory = get_minecraft_directory().replace(
    'minecraft',
    'trassert'
)
version = '1.20.1'
title = 'Trassert : Лаунчер'
alert_nicks = [
    'Ты не ввёл ник, дружище!',
    'Пожалуйста, введи ник!',
    'Я не могу играть с тобой, придумай себе ник',
    'Напиши ник, пожааалуйста',
    'Не ввёл ник, пожалуйста, введи ник',
    'Пупсик, как тебя зовут-то? Введи ник'
]
alert_start = [
    'Подожди пока игра запустится!',
    'Это что, кликер тебе? Погоди, игра скоро включится',
    'Не тыкай, игра и так запускается',
    'Быстрее не запустится если ещё раз нажмёшь',
    'Тапаем тапаем (игра и так запускается 😡)',
    'Майнкрафт уже запускается.'
]
load_ver = 'Скачиваем версию'
start = 'Запустил майнкрафт!'
nick_hint = "Пожалуйста, введите свой ник"
play_text = "Играть"
settings_text = 'Настройки'
settings_off = 'Выйти из настроек'
memory_text = 'Выделяемое количество ОЗУ'
new_png_text = 'Загрузка новых картинок   '

tg_tag = '@trassert_server, @trassert_ch'
tiktok_tag = '@trassert_server, @trassert_main'
github_tag = '@trassert'
brawl_tag = '2Y28YY0U9'


def get_fabric():
    for versions in minecraft_launcher.utils.get_installed_versions(
        minecraft_directory
    ):
        if 'fabric-loader' in versions['id']:
            fabric = versions['id']
            return fabric
    return None


def get_memory():
    return round(cext.virtual_mem()[0]/1024**3)


def has_admin():
    import os
    if os.name == 'nt':
        try:
            _ = os.listdir(
                    os.sep.join(
                        [
                            os.environ.get('SystemRoot', 'C:\\windows'), 'temp'
                        ]
                    )
                )
        except:
            return False
        else:
            return True
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return True
        else:
            return False


server = 'trassert.ddns.net:5000'


def launcher(page):
    'Игра не работает'
    db.settings('game_work', False)

    'Стандартные опции'
    options = {'jvmArguments': []}

    'Если включены случайные изображения'
    if db.settings('images') is True:
        try:
            response = requests.get(f'http://{server}/get_image', timeout=5)
            header = response.headers.get('Content-Disposition')
            for line in header.split("\n"):
                if 'filename' in line:
                    theme, structure = line.split(
                        '=')[1].replace('"', '').split('.')
                    page.theme = Theme(theme)
            with open(f"images\\image.{structure}", mode="wb") as file:
                file.write(response.content)
            image = f'image.{structure}'
        except:
            image = 'default.jpg'
            page.theme = Theme(color_scheme_seed='purple')
    else:
        image = 'default.jpg'
        page.theme = Theme(color_scheme_seed='purple')

    'Стандартное расположение'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = title
    page.padding = 0

    'Стартовая кнопка'
    success = ft.Text(
        value=start,
        color=ft.colors.WHITE70,
        weight=ft.FontWeight.BOLD
        )

    'Ник в базе'
    nick = db.settings('nickname')

    'Медиа'
    media = ft.Column(
        [
            ft.Row(
                [
                    ft.Icon(name=ft.icons.TELEGRAM),
                    ft.Text(tg_tag, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD, selectable=True)
                ]
            ),
            ft.Row(
                [
                    ft.Icon(name=ft.icons.TIKTOK),
                    ft.Text(tiktok_tag, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD, selectable=True)
                ]
            ),
            ft.Row(
                [
                    ft.Image(src="images\\github.png", width=24, height=24),
                    ft.Text(github_tag, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD, selectable=True)
                ]
            ),
            ft.Row(
                [
                    ft.Image(src="images\\brawl.png", width=24, height=24),
                    ft.Text(brawl_tag, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD, selectable=True)
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    error_text = None
    'Выставление сервера по умолчанию, если нет'
    if path.exists('servers.dat'):
        try:
            replace(
                'servers.dat',
                path.join(minecraft_directory, 'servers.dat')
            )
        except OSError:
            error_text = 'Не удалось установить сервер по умолчанию'

    'Если есть незначительные ошибки'
    if error_text:
        errors = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.icons.WARNING_ROUNDED),
                        ft.Text(
                            error_text,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE70
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text()
            ],
            alignment=ft.MainAxisAlignment.END
        )
    else:
        errors = ft.Column()

    'Текстовое поле с ником'
    nickname = ft.TextField(
        label="Ник",
        hint_text=nick_hint,
        border_color='white',
        cursor_color='white',
        hint_style=ft.TextStyle(
            color=ft.colors.WHITE38
        ),
        label_style=ft.TextStyle(
            color=ft.colors.WHITE38, weight=ft.FontWeight.BOLD
        ),
        text_style=ft.TextStyle(
            color=ft.colors.WHITE54, weight=ft.FontWeight.BOLD
        ),
        value=nick if nick is not None else ''
    )
    column = ft.Column(
        controls=[nickname],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    def play_click(e):
        'Если нажата кнопка Играть'

        'Если игра уже запущена'
        play.disabled = True
        page.update()

        if db.settings('game_work') is True:
            play.disabled = False
            page.update()
            return page.open(
                ft.AlertDialog(
                    title=ft.Text(
                        choice(alert_start),
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD
                    )
                )
            )

        'Если поле "ник" пустое'
        if nickname.value == '':
            return page.open(
                ft.AlertDialog(
                    title=ft.Text(
                        choice(alert_nicks),
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD
                    )
                )
            )
        else:
            db.settings('nickname', nickname.value)

        'Если есть V6'
        try:
            requests.get("https://v6.ident.me", timeout=4).text
            options["jvmArguments"].append(
                '-Djava.net.preferIPv6Addresses=true'
            )
            options["jvmArguments"].append(
                '-Djava.net.preferIPV4stack=false'
            )
        except:
            pass

        'Преопределение стандартных опций'
        try:
            with open(path.join(minecraft_directory, 'options.txt'), 'r') as r:
                minecraft_options = r.read()
                if 'lastServer:trassert.ddns.net' not in minecraft_options:
                    minecraft_options = minecraft_options.split('\n')
                    with open(
                        path.join(minecraft_directory, 'options.txt'), 'w'
                    ) as w:
                        n = 0
                        server_count = False
                        for line in minecraft_options:
                            if 'lastServer' in line:
                                minecraft_options[n] = 'lastServer:trassert.ddns.net\n'
                                server_count = True
                            n += 1
                        if server_count is False:
                            minecraft_options.append('\nlastServer:trassert.ddns.net\n')
                w.write(''.join(minecraft_options))
        except:
            with open(path.join(minecraft_directory, 'options.txt'), 'w') as w:
                w.write(
                    'lang:ru_ru\n'
                    'lastServer:trassert.ddns.net\n'
                    'skipMultiplayerWarning:true\nfullscreen:true'
                )

        options['username'] = nickname.value
        options['jvmArguments'].append(f"-Xmx{db.settings('memory')}G")

        'С этого момента игре нельзя запускаться ещё раз'
        db.settings('game_work', True)
        play.disabled = False
        page.update()

        'Если нет фабрик'
        try:
            if get_fabric() is None:
                raise TypeError
            column.controls.append(success)
            page.update()
            sleep(5)
            column.controls.remove(success)
            page.window.minimized = True
            page.update()
            subprocess.call(
                minecraft_launcher.command.get_minecraft_command(
                    version=get_fabric(),
                    minecraft_directory=minecraft_directory,
                    options=options
                )
            )
            db.settings('game_work', False)
            page.window.minimized = False
            page.update()
        except (minecraft_launcher.exceptions.VersionNotFound, TypeError):
            if has_admin() is False:
                'Если нет админ. привелегий'
                if get_fabric() is None:
                    db.settings('game_work', False)
                    return page.open(
                        ft.AlertDialog(
                            title=ft.Text(
                                'Произошла ошибка при установке!\n'
                                'Ошибка: Невозможно запустить Java!\n'
                                'Решение: Запустите от имени администратора.',
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.BOLD
                            )
                        )
                    )

            progress_bar = ft.ProgressBar(
                value=0.0,
                width=300,
            )
            mean = ft.Text(
                value=load_ver,
                color=ft.colors.WHITE70,
                weight=ft.FontWeight.BOLD
                )
            column.controls.append(progress_bar)
            column.controls.append(mean)
            max_value = [0]

            'Максимум прогресс-бара'
            def maximum(max_value, value): max_value[0] = value

            'Прогресс-бар'
            def update_progress(iteration, total):
                percent = (
                    "{0:." + str(1) + "f}"
                    ).format(
                        100 * (iteration / float(total))
                        )
                progress_bar.value = float(percent)/100
                page.update()

            'Статус прогресс-бара'
            def update_status(text):
                if len(text) < 32:
                    mean.value = text
                else:
                    mean.value = text[:32] + "..."
                page.update()

            'КБ от установки'
            callback = {
                "setStatus":
                    lambda text: update_status(text),
                "setProgress":
                    lambda value: update_progress(value, max_value[0]),
                "setMax":
                    lambda value: maximum(max_value, value)
            }

            'Если возникли ошибки при установке'
            try:
                minecraft_launcher.fabric.install_fabric(
                    version,
                    minecraft_directory,
                    callback=callback
                )
            except FileNotFoundError:
                db.settings('game_work', False)
                return page.open(
                    ft.AlertDialog(
                        title=ft.Text(
                            'Произошла ошибка при установке!\n'
                            'Ошибка: Не удается найти Java!'
                        )
                    )
                )
            except Exception as exception:
                db.settings('game_work', False)
                return page.open(
                    ft.AlertDialog(
                        title=ft.Text(
                            'Произошла ошибка при установке!\n'
                            f'Ошибка: {exception}'
                        )
                    )
                )
            column.controls.remove(progress_bar)
            column.controls.remove(mean)
            page.update()
            column.controls.append(success)
            page.update()
            sleep(5)
            column.controls.remove(success)
            page.window.minimized = True
            page.update()
            subprocess.call(
                minecraft_launcher.command.get_minecraft_command(
                    version=get_fabric(),
                    minecraft_directory=minecraft_directory,
                    options=options
                )
            )
            db.settings('game_work', False)
            page.window.minimized = False
            page.update()

    def settings_click_off(e):
        db.settings('images', images_switch.value)
        db.settings('memory', round(memory_slider.value))
        container.content = column
        page.update()

    def settings_click(e):
        global images_switch
        images = db.settings('images')
        images_switch = ft.Switch(
            label=new_png_text,
            value=images if images is not None else False,
            label_style=ft.TextStyle(
                color=ft.colors.WHITE54, weight=ft.FontWeight.BOLD),
            label_position=ft.LabelPosition.LEFT
        )
        global memory_slider
        memory_slider = ft.Slider(min=2, max=get_memory(
        ), divisions=get_memory()-2, label="{value} Гб")
        if db.settings('memory') is not None:
            memory_slider.value = db.settings('memory')
        else:
            memory_slider.value = round(get_memory()*0.8)
            db.settings('memory', memory_slider.value)
        container.content = ft.Column(
            controls=[
                images_switch,
                ft.Row(
                    controls=[
                        ft.Text(value=memory_text, color=ft.colors.WHITE70,
                                weight=ft.FontWeight.BOLD),
                        memory_slider
                    ]
                ),
                ft.ElevatedButton(
                    text=settings_off, on_click=settings_click_off
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.update()

    play = ft.ElevatedButton(text=play_text, on_click=play_click)
    play.style = ft.ButtonStyle()
    settings = ft.IconButton(
        tooltip=settings_text,
        on_click=settings_click,
        icon=ft.icons.SETTINGS
        )
    settings.style = ft.ButtonStyle()
    column.controls.append(ft.Row([settings, play]))
    container = ft.Container(
        content=column,
        padding=10,
        bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
        border_radius=ft.border_radius.all(15),
    )

    menu = ft.Container(
        content=ft.Stack(
            [
                media,
                ft.Column(
                    [
                        ft.Row(
                            [container],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    ft.MainAxisAlignment.CENTER
                ),
                errors
            ]
        ),
        image_src=f'images\\{image}',
        image_fit=ft.ImageFit.COVER,
        expand=True
    )
    page.add(menu)


if __name__ == '__main__':
    ft.app(launcher)
