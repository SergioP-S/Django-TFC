# Listopia, plataforma de listas colaborativas con Django

¡Bienvenido al proyecto de Listopia! Este README te guiará a través del proceso para importar y configurar el proyecto en tu máquina local.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos en tu sistema:

- **Python**: Versión 3.12.4 o superior.
- **virtualenv**: Herramienta para gestionar entornos virtuales en Python.

Si no tienes `virtualenv` instalado, puedes hacerlo ejecutando:

```bash
pip install virtualenv
```

## Pasos para configurar el proyecto

1. **Clonar el repositorio**  
   Clona el repositorio en tu máquina local utilizando el comando:

   ```bash
   git clone https://github.com/SergioP-S/Django-TFC
   ```

2. **Navegar a la subcarpeta del proyecto**  
   Una vez clonado el repositorio, navega a la subcarpeta correspondiente:

   ```bash
   cd DJANGO-LISTOPIA
   ```

3. **Crear un entorno virtual**  
   Crea un entorno virtual utilizando `virtualenv`:

   ```bash
   python -m venv venv
   ```

4. **Activar el entorno virtual**  
   Activa el entorno virtual con el siguiente comando:

   - En **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - En **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

5. **Instalar las dependencias**  
   Instala los paquetes necesarios desde el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

6. **Ejecutar el servidor local**  
   Con el entorno virtual activo, puedes iniciar el servidor local utilizando:

   ```bash
   python manage.py runserver
   ```

7. **Acceder al programa**  
   Abre un navegador web y accede a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para ver el programa en funcionamiento.

## Notas

- Recuerda activar el entorno virtual cada vez que trabajes en el proyecto para garantizar que utilizas las dependencias correctas.
- Si encuentras problemas, asegúrate de que tienes instalada la versión correcta de Python y que las dependencias se han instalado sin errores.

¡Disfruta trabajando con el proyecto!
