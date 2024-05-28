# askme_yagmurov
Для запуска проекта: <br/>

python3 -m venv askme_venv - создайте виртуальное окружение с помощью встроенного модуля venv
source askme_venv/bin/activate - активируйте виртуальное окружение(Linux и macOS)
pip install -r requirements.txt - установите зависимости
docker-compose -f docker-compose.yml up -d --build <br/>
Для доступа через Nginx: Откройте браузер и перейдите по адресу http://127.0.0.1/ либо http://localhost <br/>
Для доступа через Gunicorn: Откройте браузер и перейдите по адресу http://127.0.0.1:9000/ <br/>
Для доступа через к стороннему серверу Gunicorn, который слушает запросы: Откройте браузер и перейдите по адресу http://localhost:8081/ либо используйте курлы <br/>
