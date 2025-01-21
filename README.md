# Telegram-Dialog

This project is a system that works with Telegram sessions, allowing for automatic replies to user messages and conducting meaningful dialogues on behalf of users. The system utilizes the Telegram API for integration and interaction with users, enabling a high level of automation in communication.

The project is developed using the Django framework, which ensures flexibility, scalability, and ease of maintenance. Users can interact with the system, which will carry on a conversation by responding to their questions, maintaining the dialogue, and performing other actions on behalf of the user, making the communication more personalized and effective.

Key features:
	•	Automatic interaction with users via Telegram.
	•	Conducting meaningful dialogues and supporting various communication scenarios.
	•	Integration with Django for easy management and configuration.
	•	The ability to customize and adapt the system to specific tasks.

This project can be useful for automating customer communication, user support, or creating chatbots for various needs.
## Stack

* Postgres
* Django
* PytelegramBot
* Rabbit MQ
* Celery

## Start project with `docker-compose`

$ cp .env.example .env
$ docker-compose up -d --build

Exec commands for docker containers:

```bash
# load database dump from staging
$ make dcreatedb
$ make dloaddump
# dump database from docker container
$ make dcreatedump
# delete database from docker container
$ make ddeletedb

# make migrations && migrate
$ make dmigr
```
