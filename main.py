import random
from typing import Optional

import config
import requests
import sys

from src.vk_connection import VkConnection
from src.vk_connection import GetUploadUrlError, ImageUploadError, UploadUrlNotExistsError, SetHeaderPhotoError
from src.logger import Logger, LogLevel
from src.disk import Disk, DiskConnectionError, DiskAuthError

from requests.exceptions import ConnectionError


def get_now_week(logger) -> Optional[int]:
    try:
        now_week = requests.get('https://api-mosit.venomroms.com/now_week').json()
    except ConnectionError as e:
        logger.log(f'Connection error on api-mosit.venomroms.com: {e}')
        return None

    return now_week


def get_image(now_week: int) -> Optional[bytes]:
    disk = Disk(config.DISK_TOKEN)

    byte_file = disk.get_file(
        config.DISK_FOLDER_PATH + f'{now_week}.jpg'
    )

    return byte_file


def main():
    error_logger = Logger(
        'error_logger',
        LogLevel.ERROR,
        '[%(levelname)s] [%(asctime)s] - %(message)s',
        config.ERROR_LOG_FILENAME
    )

    info_logger = Logger(
        'info_logger',
        LogLevel.INFO,
        '[%(levelname)s] [%(asctime)s] - %(message)s',
        config.INFO_LOG_FILENAME
    )

    vk_connection = VkConnection(config.API_TOKEN)
    try:
        upload_url = vk_connection.get_upload_url(
            config.GROUP_ID,
            config.STANDARD_HEADER_IMG_WIDTH,
            config.STANDARD_HEADER_IMG_HEIGHT
        )
    except GetUploadUrlError as e:
        error_logger.log(str(e))
        sys.exit(0)

    now_week = get_now_week(error_logger)

    if now_week is None:
        sys.exit(1)

    try:
        byte_image = get_image(now_week)
        vk_connection.set_header_image(
            upload_url,
            byte_image
        )
    except ImageUploadError as e:
        error_logger.log(str(e))
        sys.exit(2)
    except UploadUrlNotExistsError as e:
        error_logger.log(str(e))
        sys.exit(3)
    except SetHeaderPhotoError as e:
        error_logger.log(str(e))
        sys.exit(4)
    except DiskAuthError as e:
        error_logger.log(str(e))
        sys.exit(5)
    except DiskConnectionError as e:
        error_logger.log(str(e))
        sys.exit(6)

    info_logger.log(f'Set image for {now_week} week')


if __name__ == '__main__':
    main()
