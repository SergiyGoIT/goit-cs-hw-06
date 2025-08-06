# goit-cs-hw-06 — Final Project (Computer Systems)

Вебзастосунок, який:

- обробляє HTTP-запити без фреймворків;
- приймає повідомлення через HTML-форму;
- передає дані на socket-сервер (UDP);
- зберігає повідомлення в MongoDB;
- запускається у Docker через `docker-compose`.

## Структура

- `main.py` — запускає HTTP і Socket сервери в окремих процесах
- `http_server.py` — обробка HTML-сторінок та POST-запиту
- `socket_server.py` — приймає та зберігає повідомлення
- `db.py` — взаємодія з MongoDB
- `templates/` — HTML-шаблони
- `static/` — CSS та зображення
- `Dockerfile`, `docker-compose.yaml` — інфраструктура

---

## Запуск

```bash
docker-compose up --build
```

---

## Доступ

- http://localhost:3000 — головна сторінка
- http://localhost:3000/message — форма для повідомлень

---

## MongoDB

Підключення до бази:

```bash
docker exec -it mongo_container mongosh
use messages_db
db.messages.find().pretty()
```
