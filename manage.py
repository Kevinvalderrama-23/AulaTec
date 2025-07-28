#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aulatec.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

#Comandos para migrar:
#python manage.py makemigrations tu_APP (crea la migracion)
#python manage.py migrate.py tu_APP (aplica las migraciones a la base de datos )

#Orden de como crear un modelo con su respectivo CRUD:
# Crear el modelo(models.py), crear el formulario(forms.py),
#crear las respectivas vistas(views.py), crear las urls(urls.py) y 
#crear las plantillas(templates).

#MariaDb motor de la base de datos.


#Tengo errores en la plantilla, matricula.list.html 
#contraseña  #:quoXt}*p<M.
#correo 12345678912