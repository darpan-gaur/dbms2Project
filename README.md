# dbms-2 Project
The Job Portal system serves as a platform that bridges job seekers and employers. We have developed a web-based application for job seekers and employers to connect with each other. Job seekers can create profiles, browse job listings, apply for positions, and track the status of their applications. Employers can post job openings, review applications, and manage candidate information efficiently. The system also provides notifications to keep users informed about relevant events.

## Project Setup


#### 1. Clone the repository
```bash
git clone <repository-url>
cd dbms2Project
```
#### 2. Install dependencies
```bash
pip install django
pip install django-widget-tweaks
```
#### 3. Database Setup
1. Install PostgreSQL
2. Create a database named `job-portal`
3. Set up .env file with the following variables:
```bash
DB_USER = 'database_user'
DB_PASSWORD = 'database_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'job-portal'
```

#### 4. Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
#### 4. Run the server
```bash
python manage.py runserver
```
#### 6. Visit the application: 
- visit localhost:8000/

