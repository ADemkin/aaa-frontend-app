from aiohttp.web import run_app
from lib.app import create_app


def main() -> None:
    app = create_app()
    run_app(app, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()
