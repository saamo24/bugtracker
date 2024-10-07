# bugtracker

This project is a simplified version of a task tracker inspired by tools like Jira or Redmine. It allows users to manage tasks, assign roles, track task statuses, and more. The project includes user registration, role-based task assignment, status transitions, and a simple search/filter mechanism.

---

## Features

- User Registration and Authentication (JWT)
- Role-based Access Control: Manager, Team Lead, Developer, Test Engineer
- Task Management: Create, Read, Update, Delete tasks
- Status transitions between tasks in a strict sequence
- Task blocking and subtask handling
- Search and filter tasks by various fields (title, description, status, creator, etc.)
- History tracking of task status changes
- Swagger-UI for API documentation
- Docker and Docker-Compose support for easy setup

---

## Task Fields

- **Number** (generated automatically)
- **Type** (bug or task)
- **Priority** (critical, high, medium, low)
- **Status** (To do, In progress, Code review, Dev test, Testing, Done, Wontfix)
- **Title** (required)
- **Description**
- **Assignee**
- **Creator** (automatically assigned)
- **Created At** (generated automatically)
- **Updated At** (generated automatically)
- **Blocking Tasks** (other tasks blocked by this one)

---

## User Roles

- **Manager**: Manages users, cannot be assigned tasks.
- **Team Lead**: Can be assigned to any task status.
- **Developer**: Can’t be assigned to "Testing" tasks.
- **Test Engineer**: Can’t be assigned to "In Progress", "Code Review", or "Dev Test" tasks.

---

## Status Transitions

Tasks can only transition between statuses in the following order:

1. To do
2. In progress
3. Code review
4. Dev test
5. Testing
6. Done

Tasks can transition to "To do" or "Wontfix" from any status.

---

## Requirements

- **Python Framework**: Django and Django REST Framework
- **Database**: PostgreSQL
- **Swagger UI**: For API documentation and testing
- **Docker**: Dockerfile and docker-compose for containerized development

---

## API Endpoints

### User Management

- **Register**: `/api/user/register/`  
  Allows a new user to register with a username and password.

- **Login**: `/api/user/login/`  
  Returns a JWT token for authentication.

- **Change Password**: `/api/user/change-password/`  
  Allows users to change their password.

- **Token Refresh**: `/api/user/token/refresh/`  
  Refreshes the JWT token.

- **Manage Users**: `/api/user/` [GET, PUT, PATCH, DELETE]  
  (Manager Only) Allows the manager to list, modify, or delete users.

### Task Management

- **List Tasks**: `/api/tickets/` [GET]  
  Returns a list of all tasks, with optional filters (type, status, creator, assignee).

- **Create Task**: `/api/tickets/` [POST]  
  Allows users to create a new task.

- **View Task**: `/api/tickets/{id}/` [GET]  
  Returns the details of a specific task, including blocking tasks and task history.

- **Update Task**: `/api/tickets/{id}/` [PUT, PATCH]  
  Allows users to update a task's information or change its status.

- **Delete Task**: `/api/tickets/{id}/` [DELETE]  
  (Manager Only) Allows the manager to delete a task.

- **Search Tasks**: `/api/tickets/search/`  
  Allows users to search tasks by title, description, or task number. Supports filters for type, status, creator, and assignee.

### Bonus Features

- **Subtasks and Task Blocking**: Blocking tasks can be specified when creating or updating a task.

- **Task History**: Task updates, particularly status transitions, are logged and can be viewed via the task detail endpoint.

---

## Setup

### Running with Docker

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/saamo24/bugtracker
   cd bugtracker
   ```

2. **Configure Environment Variables**:

   Create a `.env` file in the project root with the following content:

   ```
   SECRET_KEY=
   DEBUG=
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   ALLOWED_HOSTS=localhost, 127.0.0.1
   DJANGO_SETTINGS_MODULE=bugtracker.settings
   ```

3. **Build and Run the Containers**:

   ```bash
   docker-compose up --build
   ```

4. **Apply Migrations**:

   Once the containers are up, apply the migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a Superuser** (optional):

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the Application**:

   - The API will be accessible at `http://localhost:8000/api/`.
   - Swagger documentation will be accessible at `http://localhost:8000/swagger/`.

---

## Testing

- **Unit Tests**: To run unit tests, use the following command:

   ```bash
   docker-compose exec web python manage.py test
   ```

---

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger-UI
- **Containerization**: Docker, Docker Compose

---

This `README.md` provides an overview of the features, API endpoints, and setup instructions, tailored to your task-tracker project. Let me know if you need further modifications or additions!