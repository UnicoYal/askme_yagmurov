# askme_yagmurov
Для запуска проекта: <br/>

python3 -m venv askme_venv - создайте виртуальное окружение с помощью встроенного модуля venv <br/>
source askme_venv/bin/activate - активируйте виртуальное окружение(Linux и macOS) <br/>
pip install -r requirements.txt - установите зависимости <br/>
Создайте локально БД в PG (Докер и скрипты будут чуть позже, извините) <br/>
Создайте .env файл в папке с setting.py и добавьте следующие энвы для базы данных("DB_NAME", "DB_USER", "DB_USER_PASSWORD", "DB_HOST", "DB_DB_PORT") <br/>
python3 manage.py migrate - для прогона миграций <br/>
python3 manage.py fill_db [ratio] - для предзаполнения БД <br/>
python3 manage.py runserver - запустите сервер <br/>
Откройте браузер и перейдите по адресу http://127.0.0.1:8000/ <br/>
