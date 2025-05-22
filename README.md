# Mesozoic Prak - A theme park web application
### A simple django application crated for learning purpose. 
### Follow the instructions below to run the project on your computer.

========================================================================

## You must have python 3.10.x or higher installed to run this project.

1. ## Download or clone the project
    1. Download the project zip file and unzip it in any folder of your choosing 
    2. Or open a terminal in the location of the outer folder and paste the git clone command.

2. ## Create a virtual environment and install necessary dependencies
    1. Open a terminal inside the main project folder or cd into it.
    2. Run ```python -m venv env``` to create a virtual environment. (Optional step)
    3. To activate the venv on - cmd (windows): ```env/bin/activate.bat``` or bash: ```source env/bin/activate``` (Optional step)
    4. Then run ```pip install -r requirements.txt``` to install dependencies.
    5. Create a file name ```secrets.py``` in ```MesPrakProj/MesParkProj``` and paste the following in it ```my_secret_key = "enter-your-secret-key-here"```. OR just run ```python -c "from django.core.management.utils import get_random_secret_key; print(f\"my_secret_key = '{get_random_secret_key()}'\")" > MesParkProj/secrets.py``` in the terminal.

3. ## Making migrations and creating a superuser
    1. First run ```python manage.py makemigrations```
    2. Then run ```python manage.py migrate``` 
    3. To create a superuser run ```python manage.py createsuperuser``` and provide the necessary details.

4. ## Run the application
    1. Enter ```python manage.py runserver``` in the terminal to run the development server.
    2. Open ```localhost:8000/admin``` in a browser of your choice, login as a superuser and create products or tours from the admin panel.
    3. ```localhost:8000``` in a browser to open the application as a visitor or customer.

## You'll need an internet connection for bootstrap cdn. To use the project completely offline, do the following:

- Download compiled bootstrap css and js files from the bootstrap website.
- Paste ```bootstrap.min.css``` in ```static/css``` and ```bootstrap.bundle.min.js``` in ```static/js```
- Paste ```bootstrap-icons.css``` in ```static/css```
- Download  ```bootstrap-icons.woff``` and ```bootstrap-icons.woff2```, then paste those files in ```static/css/fonts```
