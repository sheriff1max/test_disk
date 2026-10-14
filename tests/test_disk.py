"""Тестовый сценарий:
1. Создание папки
2. Создание файлa
3. Копия файла
4. Удаление всего

Тесты идут по порядку и работают в уникальной папке, которая чистится в конце.
"""


import uuid
import pytest


FOLDER = f"/autotests-{uuid.uuid4().hex[:8]}"
FILE = f"{FOLDER}/note.txt"
COPY = f"{FOLDER}/note-copy.txt"
CONTENT = b"hello from autotests"


@pytest.fixture(scope="module", autouse=True)
def cleanup(disk):
    yield
    disk.delete(FOLDER)


def test_create_folder__put_get(disk):
    """PUT создаёт папку, GET отдаёт её метаинформацию."""
    created = disk.create_folder(FOLDER)
    assert created.status_code == 201

    info = disk.get_info(FOLDER)
    assert info.status_code == 200
    assert info.json()["type"] == "dir"


def test_upload_file__post_put(disk):
    """GET-ссылка на загрузчик + PUT содержимого файла."""
    link = disk.get_upload_link(FILE, overwrite=True)
    assert link.status_code == 200
    assert link.json()["method"] == "PUT"

    uploaded = disk.upload(link.json()["href"], CONTENT)
    assert uploaded.status_code in (201, 202)

    info = disk.get_info(FILE)
    assert info.status_code == 200
    assert info.json()["size"] == len(CONTENT)


def test_copy_file__post(disk):
    """POST копирует файл, копия доступна по новому пути."""
    copied = disk.copy(FILE, COPY, overwrite=True)
    assert copied.status_code in (201, 202)

    assert disk.get_info(COPY).status_code == 200


def test_delete_file__delete(disk):
    """DELETE удаляет файл безвозвратно, GET возвращает 404."""
    deleted = disk.delete(COPY)
    assert deleted.status_code == 204

    assert disk.get_info(COPY).status_code == 404
