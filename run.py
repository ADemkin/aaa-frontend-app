from aiohttp.web import run_app
from lib.app import create_app
# запускаем приложение через этот файл

def main() -> None:
    app = create_app()
    run_app(app, port=8000)
    # run_app(app, host='0.0.0.0', port=8000)
    # создаем application и его запускаем


if __name__ == "__main__":
    main()
