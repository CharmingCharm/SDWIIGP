# How to build up

1. Run a shell which is in python environment

	e.g. Anaconda Prompt, Windows cmd in python's virtual environment (venv)

2. Install requirements
	```shell
	pip install -r requirements.txt
	```

3. Create your own environment file private.env

	Sample file: `app/private.env.example`

4. Start up Flask backend
	```shell

	# To run server on http://localhost:5000 :
	python manage.py runserver
	
	# To manage database:
	python manage.py db

	# To add your first user (as a teacher):
	python manage.py adduser root password true
	```

5. Setup Judger (Docker required)
	```shell
	docker-compose up -d
	```
