import os
import zipfile
import shutil
import requests
from flask import send_file
from urllib.parse import urlparse, unquote, parse_qs
from typing import List

from .yandex_disk_api import fetch_files_from_folder

def download_selected_files(selected_files: List[str], zip_filename: str = 'selected_files.zip') -> str:
    """Скачивает выбранные файлы и архивирует их."""
    temp_dir = 'downloads/temp'
    os.makedirs(temp_dir, exist_ok=True)

    for file_url in selected_files:
        parsed_url = urlparse(file_url)
        file_name = unquote(parse_qs(parsed_url.query).get('filename', [None])[0])
        if not file_name:
            continue

        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    zip_filepath = os.path.join('downloads', zip_filename)
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for file_name in os.listdir(temp_dir):
            zipf.write(os.path.join(temp_dir, file_name), file_name)

    shutil.rmtree(temp_dir)
    return send_file(zip_filepath, as_attachment=True)

def download_folder_files(public_key: str, folder_path: str) -> str:
    """Скачивает все файлы из папки и архивирует их."""
    files = fetch_files_from_folder(public_key, folder_path)
    if not files:
        return "Ошибка: файлы не найдены."

    temp_dir = os.path.join('downloads', os.path.basename(folder_path))
    os.makedirs(temp_dir, exist_ok=True)

    for file in files:
        response = requests.get(file['download_url'], stream=True)
        if response.status_code == 200:
            with open(os.path.join(temp_dir, file['name']), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    zip_filepath = f"{temp_dir}.zip"
    shutil.make_archive(temp_dir, 'zip', temp_dir)
    shutil.rmtree(temp_dir)

    return send_file(zip_filepath, as_attachment=True)