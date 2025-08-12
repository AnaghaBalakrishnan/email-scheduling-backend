#  Email Scheduling System - Backend
 The **Email Scheduling System Backend** is a robust, production-ready backend application built
 with **Python**, **Django REST Framework**, and **Celery**.  
It offers secure user authentication, profile management, and email scheduling with asynchronous
 delivery.--
 
 # Features-
  **JWT Authentication**  Secure user registration & login with Access & Refresh tokens.- 
  
  **OTP Email Verification**  Verify new accounts via email with a One-Time Password.-
  
  **AWS S3 File Uploads**  Store profile pictures securely on AWS S3.- 
  
  **Email Scheduling (CRUD)**  Create, view, edit, and delete scheduled emails.-
  
  **Asynchronous Email Delivery**  Uses Celery + Redis to send scheduled emails without blocking.- 
  
  **Production Deployment Ready**  Configured for AWS EC2, Gunicorn, Nginx, and PostgreSQL.-

  
  **Security Best Practices**  Includes API throttling & Djangos built-in security features.--
  
  # Technology Stack- 
  **Framework:** Django, Django REST Framework- 
  
  **Database:** PostgreSQL (Production), SQLite3 (Development)-
  
  **Asynchronous Tasks:** Celery, Redis- 
  
  **Authentication:** `djangorestframework-simplejwt`-
  
  **File Storage:** AWS S3 (`boto3`, `django-storages`)-
  
  **Environment Variables:** `python-dotenv`--
  
  # Setup & Installation
### 1 Prerequisites
- Python **3.10+**
- PostgreSQL Server
- Redis Server
 ### 2 Clone the Repository
 ```bash
 git clone https://github.com/your-username/email-scheduling-backend.git
 cd email-scheduling-backend
 ```
 ### 3 Create Virtual Environment & Install Dependencies
 ```bash
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate
 pip install -r requirements.txt
 ```
 ### 4 Configure Environment Variables
 Create a `.env` file in the project root:
 ```
 # Django
 SECRET_KEY=your-super-secret-key
 DEBUG=True
 SERVER_IP=127.0.0.1
 # Database
 DB_NAME=your_db_name
 DB_USER=your_db_user
 DB_PASSWORD=your_db_password
 DB_HOST=localhost
 DB_PORT=5432
# Email
 EMAIL_HOST_USER=your-email@gmail.com
 EMAIL_HOST_PASSWORD=your-gmail-app-password
 # AWS S3
 AWS_ACCESS_KEY_ID=your_aws_access_key
 AWS_SECRET_ACCESS_KEY=your_aws_secret_key
 AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
 AWS_S3_REGION_NAME=your-aws-region
 ```
 ### 5 Apply Database Migrations
 ```bash
 python manage.py makemigrations
 python manage.py migrate
 ```--
##  Running the Application
 ### Start Development Server
 ```bash
 python manage.py runserver
 ```
 ### Start Celery Worker (For Asynchronous Email Sending)
 ```bash
 celery -A backend worker --loglevel=info
 ```

