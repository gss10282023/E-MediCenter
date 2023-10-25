# E-MediCenter

E-MediCenter is a digital platform for medical services. It provides an efficient and user-friendly interface for both doctors and patients to engage and manage their medical needs.

Ensure you have the following installed on your system:

- Python 3.8 ![Python Badge](https://img.shields.io/badge/Python-3.8-blue?style=flat&logo=python&logoColor=white)
- Django 3.2.5 ![Django Badge](https://img.shields.io/badge/Django-3.2.5-092E20?style=flat&logo=django&logoColor=white)
- Pillow 8.3.1![Pillow Badge](https://img.shields.io/badge/Pillow-8.3.1-FF69B4?style=flat&logo=pillow&logoColor=white)
- Google Maps API ![Google Maps Badge](https://img.shields.io/badge/GoogleMaps-API-blue?style=flat&logo=google-maps)

## Running the Application

### Using Docker

1. Build the Docker image:

   ```cobol
   docker-compose build

2. Run the Docker container:

   ``````cobol
   docker-compose up
   ``````

3. Access the application at `http://localhost:8000/`.

### Without Docker (Using Django)

1. **Install the Dependencies**

   ``````cobol
   pip install -r requirements.txt
   ``````

2.  **Run the Django Server**

   ``````cobol
   python manage.py runserver
   ``````

## Development Guidelines

- Ensure the media directory is set up correctly.
- Regularly backup your database.
- Handle Google Maps API keys securely.

## Contributors

- Haolan Zou

- Shanshan Gao

-  Xiaoxin Wang

-  Kechang Chen

-  Jinqi Lin 

  