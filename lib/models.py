from easyocr import Reader as Reader


def get_model() -> Reader:
    return Reader(["en"])
