import requests


class DiskConnectionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DiskAuthError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('UnauthorizedError. Wrong authorization params.', *args)


class Disk:
    DOWNLOAD_LINK = 'https://cloud-api.yandex.net/v1/disk/resources/download'

    def __init__(self, token):
        self._token = token

    def _get_headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self._token}'
        }

    def _get_download_url(self, filepath: str) -> str:
        params = {'path': filepath}
        headers = self._get_headers()

        res = requests.get(
            self.DOWNLOAD_LINK,
            params=params,
            headers=headers
        ).json()

        if 'error' in res:
            error = res['error']
            if error == 'UnauthorizedError':
                raise DiskAuthError
            else:
                raise DiskConnectionError(error)

        return res['href']

    def get_file(self, filepath: str) -> bytes:
        download_url = self._get_download_url(filepath)

        res = requests.get(download_url)

        return res.content
