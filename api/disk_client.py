import requests


class DiskClient:
    def __init__(
            self,
            token: str,
            base_url: str = "https://cloud-api.yandex.net/v1/disk",
        ):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"OAuth {token}"
        self.session.headers["Accept"] = "application/json"

        self.base_url = base_url

    def request(
            self,
            method: str,
            url_path: str,
            **params,
        ) -> requests.Response:
        # bool -> "true"/"false", как ожидает API
        params = {
            k: str(v).lower()
            if isinstance(v, bool) else v
            for k, v in params.items()
        }
        return self.session.request(
            method,
            f"{self.base_url}{url_path}",
            params=params,
            timeout=30
        )

    def get_info(
            self,
            path: str,
            **params
        ) -> requests.Response:
        """GET — метаинформация о ресурсе (файл/папка)"""
        return self.request("GET", "/resources", path=path, **params)

    def create_folder(
            self,
            path: str
        ) -> requests.Response:
        """PUT — создание папки"""
        return self.request("PUT", "/resources", path=path)

    def get_upload_link(
            self,
            path: str,
            overwrite: bool = True
        ) -> requests.Response:
        """GET — ссылка на загрузчик файла"""
        return self.request(
            "GET",
            "/resources/upload",
            path=path,
            overwrite=overwrite
        )

    @staticmethod
    def upload(
            href: str,
            data: bytes
        ) -> requests.Response:
        """PUT — отправка содержимого файла по ссылке загрузчика (токен не нужен)"""
        return requests.put(href, data=data, timeout=60)

    def copy(
            self,
            source: str,
            destination: str,
            overwrite: bool = True
        ) -> requests.Response:
        """POST — копирование ресурса"""
        return self.request(
            "POST",
            "/resources/copy",
            **{"from": source},
            path=destination,
            overwrite=overwrite
        )

    def delete(
            self,
            path: str,
            permanently: bool = True
        ) -> requests.Response:
        """DELETE — удаление ресурса"""
        return self.request(
            "DELETE",
            "/resources",
            path=path,
            permanently=permanently
        )
