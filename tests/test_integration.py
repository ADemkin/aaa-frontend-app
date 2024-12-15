from unittest.mock import MagicMock

# from aiohttp import FormData
from http import HTTPStatus
from lib.models import get_model
from lib.models import Reader

import pytest


def test_index_page_contain_valid_multipart_form(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK, response.text
    text = response.text.lower()
    assert "<form " in text, "На странице нет формы"
    assert 'method="post"' in text, "У формы не указан POST метод"
    assert 'enctype="multipart/form-data"' in text, "у формы не указан enctype"
    assert "submit" in text, "у формы нет кнопки отправки"


@pytest.mark.parametrize(
    "image_path,text_expected",
    [
        ("images/avito.jpg", "avito"),
        # ('images/signs.jpg', 'albuquerque'),
        # ('images/signs-small.jpg', 'angeles'),
    ],
)
def test_if_sent_image_with_word_then_word_appear_in_response(
    client,
    image_path,
    text_expected,
):
    with open(image_path, "rb") as file:
        response = client.post("/", files={"file": file})
    assert response.status_code == HTTPStatus.OK, response.text
    text = response.text.lower()
    assert text_expected in text, f"expected {text_expected} in {text}"


def test_if_sent_faulty_image_then_error_appear_in_response(app, client):
    image_path = "images/error.jpg"
    error_message = "something nasty happened"
    # не смотря на то, что отправляется настоящее изображение,
    # модель мокается, чтобы контролировать исключение - оно
    # может быть разным на разных платформах
    mock = MagicMock(spec=Reader)
    mock.readtext.side_effect = Exception(error_message)
    app.dependency_overrides[get_model] = lambda: mock
    with open(image_path, "rb") as file:
        response = client.post("/", files={"file": file})
    app.dependency_overrides.clear()
    assert response.status_code == HTTPStatus.OK, response.text
    text = response.text.lower()
    assert error_message in text, f"expected {error_message} in {text}"
