from http import HTTPStatus


def test_integration(
    client,
    image_file,
    save_artifact,
):
    response = client.post("/", files={"file": image_file})
    assert response.status_code == HTTPStatus.OK, response.text
    text = response.text.lower()
    word_want = "angeles"
    assert word_want in text, f"слово {word_want} не найдено в {text}"
    save_artifact(text, "avito.html")


class TestPageContent:
    """
    Этот тест проверяет разное поведение страницы в зависимости от ответа модели.

    Такие тесты позволяют проверять поведение всей системы быстро, без
    включения её медленных компонентов- в нашем случае модели.
    """

    @staticmethod
    def test_index_page_contain_valid_multipart_form(client, save_artifact):
        response = client.get("/")
        assert response.status_code == HTTPStatus.OK, response.text
        text = response.text.lower()
        assert "</form>" in text, "На странице нет формы"
        assert 'method="post"' in text, "У формы не указан POST метод"
        assert 'enctype="multipart/form-data"' in text, "у формы не указан enctype"
        assert "submit" in text, "у формы нет кнопки отправки"
        save_artifact(text, "empty.html")

    @staticmethod
    def test_if_model_gives_error_then_response_contain_error_text(
        client,
        model_mock,
        image_file,
        save_artifact,
    ):
        error_message = "какая-то ошибка"
        model_mock.readtext.side_effect = Exception(error_message)
        response = client.post("/", files={"file": image_file})
        assert response.status_code == HTTPStatus.OK, response.text
        text = response.text.lower()
        assert error_message in text, "в ответе нет ошибки"
        save_artifact(text, "error.html")

    @staticmethod
    def test_if_model_gives_words_then_response_contain_table(
        client,
        model_mock,
        image_file,
    ):
        model_mock.readtext.return_value = [
            [[(156, 146), (194, 146), (194, 172), (156, 172)], "word", 0.9]
        ]
        response = client.post("/", files={"file": image_file})
        assert response.status_code == HTTPStatus.OK, response.text
        text = response.text.lower()
        assert "<table" in text, "на странице нет таблицы"

    @staticmethod
    def test_if_model_gives_not_words_then_response_not_contain_table(
        client,
        model_mock,
        image_file,
    ):
        model_mock.readtext.return_value = []
        response = client.post("/", files={"file": image_file})
        assert response.status_code == HTTPStatus.OK, response.text
        text = response.text.lower()
        assert "</table>" not in text, "на странице не должно быть таблицы"
