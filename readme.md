# hyper_resource_py
Tool to work with apis of level three.

#Generate code by Reverse engineering

Before any procedure, certify yourself that your python installations has the requirements specified in requirements.txt

0. Open console

1. Start a Django project

	django-admin startproject [project_name]

2. Got to project folder through console

	cd path/to/your/project/[project_name]

3. Create a app inside the project folder

	django-admin startapp [app_name]

4. Type the command below and fallow the instructions on console

	python generator_models_settings_files.py [project_name] [app_name]

5. Generate the necessary files using the command below

	python generator_files.py [project_name] [app_name]

6. Start your application through console

	python manage.py runserver

7. Access your project using the browser

	http://localhost:8000
