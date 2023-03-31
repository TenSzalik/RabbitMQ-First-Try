# About

This is my first encounter with RabbitMQ :)

# How it works?

There are three endpoints:

- /api/send/ - send a message to the queue
- /api/receive/ - takes the first message from the queue, encodes it with base64 and returns it, also writes it to the db
- /api/messages/ - get all decoded messages from db

    ![api send explained](https://i.imgur.com/7GXgB8D.jpeg "/api/send/")

    ![api send explained](https://i.imgur.com/TPny4RM.jpeg "/api/send/")

# How to run?

- Install MongoDB and set the:
    - server on `localhost:27017` (default for this db)
    - database name "`Message`"
    - collection name "`encoded-message`"

- Download RabbitMQ-server docker image and set:
    - host: "`localhost`"
    - username: "`admin`"
    - password: "`admin2023`"

- Create python venv and install `requirements.txt` (pip install -r requirements.txt)

- Run uvicorn (uvicorn main:app --reload)
