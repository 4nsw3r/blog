import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = bool(os.getenv("DEBUG"))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    },
}
INTERNAL_IPS = ['127.0.0.1']

CRISPY_TEMPLATE_PACK = 'bootstrap3'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testnekidaem@gmail.com'
EMAIL_HOST_PASSWORD = 'qaz321wsx'
EMAIL_PORT = 587
EMAIL_USE_TLS = True