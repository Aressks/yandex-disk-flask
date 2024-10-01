import requests
from typing import List, Tuple, Optional

YANDEX_DISK_API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'

def fetch_files_from_folder(public_key: str, path: str = '') -> List[dict]:
    """Рекурсивно получает все файлы в папке на Яндекс.Диске."""
    response = requests.get(YANDEX_DISK_API_URL, params={'public_key': public_key, 'path': path})
    if response.status_code == 200:
        data = response.json()
        files = []
        for item in data.get('_embedded', {}).get('items', []):
            if item['type'] == 'file':
                files.append({
                    'name': item['name'],
                    'path': item['path'],
                    'download_url': item['file']
                })
            elif item['type'] == 'dir':
                # Рекурсивный вызов для вложенных папок
                files.extend(fetch_files_from_folder(public_key, item['path']))
        return files
    return []

def fetch_files_and_folders(public_key: str, path: str = '') -> Tuple[Optional[List[dict]], Optional[List[dict]]]:
    """Получает файлы и папки в текущей директории."""
    response = requests.get(YANDEX_DISK_API_URL, params={'public_key': public_key, 'path': path})
    if response.status_code == 200:
        data = response.json()
        files, folders = [], []
        for item in data.get('_embedded', {}).get('items', []):
            if item['type'] == 'file':
                files.append({
                    'name': item['name'],
                    'download_url': item['file'],
                    'size': item['size']
                })
            elif item['type'] == 'dir':
                folders.append({
                    'name': item['name'],
                    'path': item['path']
                })
        return files, folders
    return None, None