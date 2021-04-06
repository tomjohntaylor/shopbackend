## 1. API documentation
Website is accessible on http://shopapi.tj-t.com/ as DEV project (DEBUG=True, etc.).
If there are any problems viewing the page contact tomasz.jan.krawczyk@gmail.com.

Auto-generated documentation and API swagger are accessible on:
- http://shopapi.tj-t.com/swagger/
- http://shopapi.tj-t.com/redoc/

Basic endpoints explanation:
1. Viewing current profile: http://shopapi.tj-t.com/profile/ (GET)
1. Viewing and creating current profile's orders: http://shopapi.tj-t.com/profile/orders (GET, POST)
1. Viewing, editing and deleting specific order: http://shopapi.tj-t.com/profile/orders/<int:pk> (GET, PUT, DELETE)
1. Viewing product list: http://shopapi.tj-t.com/products/ (GET)
1. Viewing product detail: http://shopapi.tj-t.com/products/<int:pk> (GET)

## 2. Features missing - must have for production-ready API
#### Deployment on production web server
Proper configuration of settings.py (DEBUG=False, ALLOWED_HOSTS, etc.) and provission on HA web server. This project is configured for combination of Ubuntu 18.04 OS + Gunicorn + nginx deployment using Ansible.
#### Authentication
This project use Django standard User model and custom Profile model. For API there was also installed rest_framework.authtoken app and endpoints connected to it. For production-ready API token authentication system is suggested, especially JWT.
#### Persistence storage system (DB)
This project use Django standard sqlite3 DB. For production-ready API suggested to use are more advanced DBs (ex. Postgre, MySQL, Oracle) provisioned on a different server that web server.
#### Product images handling
In this project is used standard Django model's ImageField. For production-ready API use cases (UI JS app, mobile app) suggested to use are third party image storage, ex. AWS S3. In case of proper handling of image file uploads custom storage system implementation in Django is needed (for AWS S3 there are some ready to use packages). If file upload will not be served via website images urls should be stored in Django standard model field, ex. TextField (urls separated by spaces, string splitting and joining in backed)
#### More API functionalities needed for shop application
Product attributes system, categorization and filtering. Integration with front-end applications functionalities (ex. cart). Integration with other services: payment system, file storage, e-mail app for sale process notifications, etc.



