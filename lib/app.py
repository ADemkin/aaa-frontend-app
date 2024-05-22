from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp.web import Application

from lib import views
from lib.models import create_model
# асинхронный код


lib = Path("lib")

def create_app() -> Application:
    # центральный элемент фреймворка

    app = Application()
    # setup routes
    app.router.add_static("/static/", lib / "static")
    # подключаем пути в роутер
    # добавляем статику - картинки, jss, css - то, что пользователю
    # показывается
    app.router.add_view("/", views.IndexView, name="index")
    # добавляем хендлер на приложение, чтобы 
    # заходя в корень приложения - попадали в обработчик

    # setup templates
    aiohttp_jinja2.setup(
        app=app,
        loader=jinja2.FileSystemLoader(lib / "templates"),
    )
    # магия, которая позволяет из папки templates 
    # загружать шаблоны с разными именами
    app["model"] = create_model()
    return app


async def async_create_app() -> Application:
    return create_app()
