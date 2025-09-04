web: gunicorn --bind 0.0.0.0:$PORT agri_project.wsgi:application
release: DJANGO_SETTINGS_MODULE=agri_project.settings_production python manage.py migrate && DJANGO_SETTINGS_MODULE=agri_project.settings_production python manage.py create_default_superuser
