# Дешборд

### Запуск

Введите команды:
    
    git clone https://github.com/assigdev/WW91IGRvbid0IGZpbmQgdGhpcyEh.git
    docker-compose up
    docker-compose exec dashboard_app python manage.py createsuperuser
    
затем перейто по ссылке [http://127.0.0.1:8000](http://127.0.0.1:8000)


### System stories

##### Сценарий взаимодействия при параллельном обновлении через действие в админке:

- Сервис1 запускает фоновую задачу и отображает сообщение о том, что данные будут обновлены
- Celery worker выполняя фоновую задачу, обращается в сервис2 через REST API, передавая функцию в текстовом виде и параметры.
- Сервис2 обрабатывает запрос, генерирует точки для графика по переданным данным.
- Сelery worker получает точки и передает их в сервис3 по REST API.
- Сервис3 принимает набор точек и возвращает изображение.
- Сelery worker получает изображение и сохраняет в БД, обновляет дату обновления.
