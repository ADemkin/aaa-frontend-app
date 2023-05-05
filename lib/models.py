from easyocr import Reader


def create_model() -> Reader:
    return Reader(["en", "ru"])
