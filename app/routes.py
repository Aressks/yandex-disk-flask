from flask import render_template, request, redirect, url_for
from .yandex_disk_api import fetch_files_and_folders
from .download_manager import download_selected_files, download_folder_files

def setup_routes(app):
    """Настройка маршрутов Flask-приложения."""

    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Главная страница с формой для ввода публичной ссылки."""
        if request.method == 'POST':
            public_key = request.form['public_key']
            return redirect(url_for('view_folder', public_key=public_key, path=''))
        return render_template('index.html')

    @app.route('/view_folder', methods=['GET'])
    def view_folder():
        """Отображение файлов и папок на Яндекс.Диске по указанной публичной ссылке."""
        public_key = request.args.get('public_key')
        path = request.args.get('path', '')

        parent_path = '/'.join(path.split('/')[:-1]) if path else None

        files, folders = fetch_files_and_folders(public_key, path)
        if files is None or folders is None:
            error = "Ошибка при получении файлов. Проверьте публичную ссылку."
            return render_template('index.html', error=error)

        return render_template('view_folder.html', files=files, folders=folders, public_key=public_key, current_path=path, parent_path=parent_path)

    @app.route('/download', methods=['POST'])
    def download_file():
        """Загрузка одного файла по переданному URL."""
        download_url = request.form['download_url']
        file_name = request.form['file_name']

        return download_selected_files([download_url], file_name)

    @app.route('/download_folder', methods=['POST'])
    def download_folder():
        """Скачивание всех файлов из выбранной папки."""
        public_key = request.form['public_key']
        folder_path = request.form['folder_path']

        return download_folder_files(public_key, folder_path)

    @app.route('/download_selected_files', methods=['POST'])
    def download_selected():
        """Скачивание выбранных файлов в архиве ZIP."""
        selected_files = request.form.getlist('selected_files')
        return download_selected_files(selected_files)