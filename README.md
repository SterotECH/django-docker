# Django Docker Template

This Django Docker template provides a starting point for your Django web application development. It includes Docker and Docker Compose configurations, necessary packages for Django, and implements a basic authentication API.

## Features

- Dockerized development environment for Django.
- Pre-configured Docker Compose setup for development and testing.
- Django authentication API implemented.
- Easily extendable for adding your own Django apps and functionalities.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get started with your Django project using this template:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/SterotECH/django-docker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django-docker
   ```

3. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

4. Access the Django development server at `http://localhost:8000/` in your web browser.

5. You can start building your Django application, taking advantage of the Dockerized development environment.

## Docker Compose Configuration

This template includes a Docker Compose configuration with the following services:

- Django web application
- PostgreSQL database
- Redis for caching
- Nginx as a reverse proxy (optional)

You can customize these services as needed for your project.

## Authentication API

The Django project in this template already includes a basic authentication API. You can extend it to suit your specific authentication requirements.

## Customization

Feel free to customize and extend this template to meet your project's needs. You can add your Django apps, modify the database settings, and enhance the authentication system as required.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thank you to the Django and Docker communities for their fantastic tools and resources.

## Support

If you encounter any issues or have questions about this template, please [open an issue](https://github.com/SterotECH/django-docker/issues) on GitHub.
