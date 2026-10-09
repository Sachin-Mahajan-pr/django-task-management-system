# Task Management System API

## Project Overview

A RESTful Task Management API developed using Python, Django, and Django REST Framework. The application allows authenticated users to create tasks, view their tasks, assign tasks to other users, update task statuses, and filter tasks using query parameters.

## Technologies Used

* Python
* Django
* Django REST Framework
* Simple JWT Authentication
* SQLite / configured database
* Postman

## Features

* JWT access and refresh token authentication
* Create and list tasks
* Retrieve a single task by ID
* Assign and reassign tasks
* Update task status
* Filter tasks by status
* Filter tasks by assigned user
* Permission-based task operations

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

Alternatively, open the existing project folder containing `manage.py`.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Base URL:

```text
http://127.0.0.1:8000/
```

## API Endpoints

| Method | Endpoint                  | Description               |
| ------ | ------------------------- | ------------------------- |
| POST   | `/api/token/`             | Obtain JWT tokens         |
| POST   | `/api/token/refresh/`     | Refresh access token      |
| GET    | `/api/tasks/`             | List accessible tasks     |
| POST   | `/api/tasks/`             | Create a task             |
| GET    | `/api/tasks/<id>/`        | Retrieve a single task    |
| PATCH  | `/api/tasks/<id>/assign/` | Assign or reassign a task |
| PATCH  | `/api/tasks/<id>/status/` | Update task status        |

Note: The single-task GET endpoint must be implemented in `TaskDetailAPIView` and configured in `myapp/urls.py`.

## Authentication

Obtain JWT tokens.

**Method:** POST

```text
http://127.0.0.1:8000/api/token/
```

Request body:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Copy the access token from the response.

For protected APIs, select **Authorization → Bearer Token** in Postman and paste the access token.

## API Request Examples

### 1. Create a Task

**Method:** POST

```text
http://127.0.0.1:8000/api/tasks/
```

Request body:

```json
{
    "title": "Complete Python Practical",
    "description": "Implement and test Django REST APIs",
    "assigned_to": 2
}
```

The API sets the creator to the authenticated user and initializes the task status to `open`.

The example fields must match the fields accepted by `TaskSerializer`.

### 2. Get All Accessible Tasks

**Method:** GET

```text
http://127.0.0.1:8000/api/tasks/
```

Returns tasks created by or assigned to the authenticated user.

### 3. Get a Single Task

**Method:** GET

```text
http://127.0.0.1:8000/api/tasks/1/
```

Replace `1` with an existing task ID.

### 4. Assign or Reassign a Task

**Method:** PATCH

```text
http://127.0.0.1:8000/api/tasks/1/assign/
```

Request body:

```json
{
    "assigned_to": 2
}
```

Only the task creator can assign or reassign a task. The target user must be active.

### 5. Update Task Status

**Method:** PATCH

```text
http://127.0.0.1:8000/api/tasks/1/status/
```

Request body:

```json
{
    "status": "in_progress"
}
```

Supported status values:

* `open`
* `in_progress`
* `done`

Only the creator or assigned user can update the status, subject to the model's status-transition rules.

## Filtering Tasks

Use query parameters with the task list endpoint.

| Purpose                       | Endpoint                                |
| ----------------------------- | --------------------------------------- |
| Open tasks                    | `/api/tasks/?status=open`               |
| In-progress tasks             | `/api/tasks/?status=in_progress`        |
| Completed tasks               | `/api/tasks/?status=done`               |
| Tasks assigned to user 2      | `/api/tasks/?assigned_to=2`             |
| Open tasks assigned to user 2 | `/api/tasks/?status=open&assigned_to=2` |

## Testing

Test all endpoints using Postman.

1. Obtain an access token.
2. Add the token as a Bearer token.
3. Create a task.
4. Retrieve tasks and test filtering.
5. Assign a task to another active user.
6. Update the task status.
7. Verify authentication and permission errors.

## Expected HTTP Status Codes

* `200 OK` — Request successful
* `201 Created` — Task created
* `400 Bad Request` — Invalid request data
* `401 Unauthorized` — Missing or invalid authentication
* `403 Forbidden` — Permission denied
* `404 Not Found` — Task not found

## Developer Notes

* Keep model, serializer, and request field names consistent.
* Use valid user IDs and task IDs when testing.
* Keep secret keys and authentication tokens out of version control.
