from unittest.mock import patch
from unittest.mock import MagicMock
from aiohttp import FormData
from http import HTTPStatus

import pytest


async def test_index_page_contain_valid_multipart_form(client):
    response = await client.get('/')
    text = await response.text()
    assert response.status == HTTPStatus.OK, text
    assert 'method="post"' in text.lower(), 'У формы не указан POST метод'
    assert 'enctype="multipart/form-data"' in text.lower(), 'у формы не указан enctype'
    assert 'type="submit"' in text.lower(), 'у формы нет кнопки отправки'


@pytest.mark.parametrize('image_path,text_expected', [
    ('images/avito.jpg', 'Avito'),
    # ('images/signs.jpg', 'Albuquerque'),
    # ('images/signs-small.jpg', 'Angeles'),
])
async def test_if_sent_image_with_word_then_word_appear_in_response(
        client,
        image_path,
        text_expected,
):
    form = FormData()
    form.add_field(
        name='image',
        value=open(image_path, 'rb'),
        content_type='image/jpeg',
        filename='test_image.jpg',
    )
    response = await client.post('/', data=form)
    text = await response.text()
    assert response.status == HTTPStatus.OK, text
    assert text_expected in text


async def test_if_sent_faulty_image_then_error_appear_in_response(client):
    form = FormData()
    form.add_field(
        name='image',
        value=open('images/error.jpg', 'rb'),
        content_type='image/jpeg',
        filename='test_image.jpg',
    )
    error_message = 'something nasty happened'
    model = client.app['model']
    # Тут мы мокаем модель, заставляя её всегда рейзить ошибку
    mock = MagicMock(side_effect=ValueError(error_message))
    with patch.object(model, 'readtext', mock):
        response = await client.post('/', data=form)
    text = (await response.text()).lower()
    assert response.status == HTTPStatus.OK, text
    assert error_message in text, f'expected {error_message} in {text}'
