# 🎁 Sistemas de Gestión de Tickets 🎉

✨ *Descripción*

¡Bienvenido al proyecto *Sistemas de Gestión de Tickets*! 🛒

Al finalizar esta tarea, los estudiantes habrán mejorado su dominio de la Programación Orientada a Objetos en Python, adquiriendo competencias
en el diseño e implementación de bases de datos relacionales. También desarrollarán habilidades para manejar la validación de entradas, el control
de errores y excepciones, y la creación de interfaces de usuario intuitivas.

🚀 *Características Principales*



🎨 *Diseño Minimalista y Oscuro*

La interfaz de usuario está diseñada con un estilo minimalista y una paleta de colores oscura, que brinda una experiencia visual moderna y elegante.

🛠️ *Tecnologías Utilizadas*

* *Backend:*
    * *Django:* El sólido framework web de Python que impulsa la aplicación.
    * *sqlite3:* Base de datos  eficiente para almacenar los datos.
* *Frontend:*
    * *HTML, CSS, JavaScript:* Lenguajes esenciales para crear la interfaz de usuario.
    * *Font Awesome:* Biblioteca de iconos para añadir elementos visuales atractivos.  

## ⚙️ Cómo Ejecutar la Aplicación  

1. *Clonar el repositorio:*
   ```bash
   git clone https://github.com/SnayderCJ/ticket_system.git 
   cd ticket_system
   ```
    

3. *Crear (o activar) un entorno virtual::*   
    ```bash
    py -m venv venv  
    venv\Scripts\activate 
    ```

4. *Instalar las dependencias:*
    ```bash
    pip install -r requirements.txt
    ```

5. *Aplicar las migraciones:*
    ```bash
    py manage.py makemigrations
    py manage.py migrate
    ```

6. *Crear un superusuario:*
    ```bash
    py manage.py createsuperuser
    ```

7. *Ejecutar el servidor de desarrollo:*
    ```bash
    py manage.py runserver
    ```

8. *Acceder a la aplicación en tu navegador:*
    
    *   Abre tu navegador web y visita: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (para la interfaz principal)
    

9. *Iniciar sesión en el panel de administración:*
    
    *   Accede al panel de administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (utiliza las credenciales del superusuario). que creaste en el paso 5.
    

## Explora y disfruta de Sistema de Gestión de Tickets!** 🎉  
