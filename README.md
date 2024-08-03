# IT Company Task Manager

A simple task management application for an IT company built with Django.

## Features

### Task Management
- **Create, Update, Delete Tasks**: Easily manage tasks with CRUD operations.
- **View All Tasks**: Access a list of all tasks.
- **View Task Details**: Access detailed information about each task.
- **Assign Workers to Tasks**: Track which workers are assigned to specific tasks.
- **Filter by Completion Status**: Filter tasks by completed, not completed, or all.
- **Sort Tasks**: Sort tasks by name or deadline.

### Worker Management
- **Create, Update, Delete Workers**: Manage workers with CRUD operations.
- **View All Workers**: Access a list of all workers.
- **View Worker Details**: Access detailed information about each worker.
- **Task Assignment**: See which tasks a worker is assigned to.

### Task Type Management
- **Create, Update, Delete Task Types**: Manage task types with CRUD operations.
- **View All Task Types**: Access a list of all task types.

### Position Management
- **Create, Update, Delete Positions**: Manage positions within the organization.
- **View All Positions**: Access a list of all positions.

### Additional Features
- **Search Functionality**: Search by name within tasks, workers, task types, and positions.
- **User Authentication**: Secure login and logout for users.

## How to Launch the Project

### 1. Clone the Repository

```
git clone https://github.com/Meksim-fesh/it-company-task-manager.git
cd django-task-manager
```

### 2. Create and Activate Virtual Environment

```
python -m venv venv # Or python3 -m venv venv
source venv\Scripts\activate # Or source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Rename the `.env.example` file to `.env` and set your environment variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Apply Migrations

```
python manage.py migrate
```

### 6. Create a Superuser

```
python manage.py createsuperuser
```

### 7. Run the Server

```
python manage.py runserver
```

# Check It Out

The project deployed to Render: [https://it-company-task-manager-rek7.onrender.com](https://it-company-task-manager-rek7.onrender.com)


Test credentials

**Login**: test_user
**Password**: pass123word

## License

This project is licensed under the MIT License.
