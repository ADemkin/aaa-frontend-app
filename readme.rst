========================
AAA Frontend Application
========================

Описание
========

В этом репозитории находится то приложение, которое должно получиться у студентов
ААА в результате выполнения домашнего задания.

Приложение позволяет загрузить изображение и распознать на нём текст.

В результате выполнения домашнего задания студент познакомится с:

* вёрсткой HTML документа
* CSS фреймворком Bootstrap
* веб фреймворком aiohttp
* шаблонизатором Jinja

Требования
==========

Для работы сервиса вам нужен Python 3.12.

Установка
=========

Для сборки докер образа::

$ make build

Запуск
======

Для запуска в режиме разработки с автоматической перезагрузкой сервера при
изменении кода::

$ make dev


Для запуска приложения напрямую::

$ make run


Для запуска тестов::

$ make test

Для выполнения линтеров::

$ make lint

или каждый по отдельности::

$ make flake8
$ make pycodestyle
$ make pylint


Полезные ссылки
===============

* `Базовый шаблон HTML документа и блоки Bootstrap <https://getbootstrap.com/docs/5.2/getting-started/introduction/>`_
* `Описания HTML тегов и их аттрибутов <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form>`_
* `MVC паттерн проектирования UI <https://en.wikipedia.org/wiki/Model–view–controller>`_
* `XKCD как пример MPA приложения <https://xkcd.com>`_
* `Документация Jinja <https://jinja.palletsprojects.com/en/3.1.x/>`_
* `Документация aiohttp <https://docs.aiohttp.org/en/stable/>`_
