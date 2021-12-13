import requests

from vk_api import VkApi
from vk_api.exceptions import ApiError
from requests.exceptions import ConnectionError
from os import path


class GetUploadUrlError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UploadUrlNotExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(['Not expected uploar_url param', *args])


class ImageUploadError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(['Error on load image to VK', *args])


class SetHeaderPhotoError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(['Wrong photo params', *args])


class VkConnection:
    def __init__(self, api_token: str):
        self._vk_session = VkApi(token=api_token)

    def get_upload_url(self, group_id: int, img_width: int, img_height: int) -> str:
        try:
            upload_params = self._vk_session.method(
                'photos.getOwnerCoverPhotoUploadServer',
                {
                    "group_id": group_id,
                    'crop_x2': img_width,
                    'crop_y2': img_height
                })
        except ApiError as e:
            raise GetUploadUrlError(e)

        if 'upload_url' in upload_params:
            return upload_params['upload_url']
        else:
            raise UploadUrlNotExistsError

    def set_header_image(self, upload_url: str, byte_image: bytes) -> None:
        try:
            image_params = requests.post(
                upload_url,
                files = {
                    'file': byte_image
                }).json()
        except ConnectionError as e:
            raise ImageUploadError(e)

        try:
            self._vk_session.method('photos.saveOwnerCoverPhoto', image_params)
        except ApiError as e:
            raise SetHeaderPhotoError(e)
