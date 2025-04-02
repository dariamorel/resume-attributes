В данном репозитории хранится проект "Извлечение ключевых атрибутов резюме на русском". Оценить работоспособность проекта можно через взаимодействие с сайтом. Перед этим необходимо установить все используемые в проекте библиотеки. 

**Установить необходимые для корректной работы проекта библиотеки:**

```
pip install -r requirements.txt
``` 

**Запустить сайт с локального устройства:**

```
cd website
python manage.py runserver
```

**Запустить тесты:**

Работоспособность тестов можно проверить запустив через IDE файл `testing/main.py`. В той же директории хранятся все файлы с тестами. 

Основной код, отвечающий за работоспособность алгоритмов извлечения ключевых атрибутов из резюме лежит в папке `website/extractor/structure`.
