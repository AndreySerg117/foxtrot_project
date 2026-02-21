# constant
default_auto_field = 'django.db.models.BigAutoField' нужен для того, чтобы по умолчанию джанго создавал поле
id для моделей с типом BigAutoField

AUTH_USER_MODEL = "user.User" в джанго нужен для того, чтобы использовать свою собственную модель пользователя
вместо стандартной