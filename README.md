The Culinary Platform is a Django-based web application designed for managing recipes, chefs, and ingredients.

Users can create, edit, and delete recipes with details like name, description, price, and associated chefs and ingredients.

It also supports chef management, ingredient tracking, and dish type organization, offering search and filtering capabilities.

The platform features an intuitive UI powered by HTML, CSS, and Bootstrap, making it easy for culinary enthusiasts to organize their kitchen effectively.


## Installation

Python must be already installed


git clone https://github.com/xrkxdd/kitchenservice1.git
cd kitchenservice1
python -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Before starting the project, you need to configure the environment file.

Rename the env-example file to .env