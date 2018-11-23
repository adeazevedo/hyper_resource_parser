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
	
4. Copy the follow folders and files from 'hyper_resource_py' to your project folder

	Files: 
	
		context_generator.py
		
		generator_files.py
		
		generator_models_setting_files.py
		
		modeler_generator.py
		
		serializer_generator.py
		
		settings_generator.py
		
		settings_template.py
		
		urler_generator.py
		
		urler_project_generator.py
		
		viewer_generator.py
	Folders:
	
		expression_interface
		
		hyper_resource
		
		image_generator

5. Type the command below and fallow the instructions on console

	python generator_models_settings_files.py [project_name] [app_name]

6. Generate the necessary files using the command below

	python generator_files.py [project_name] [app_name]

7. Start your application through console

	python manage.py runserver

8. Access your project using the browser

	http://localhost:8000
