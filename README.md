# TaskFlow — Task Manager App

> A full-stack task management web app built with Python Flask and vanilla JS.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Setup & Run](#setup--run)
5. [API Reference](#api-reference)
6. [UML Diagrams](#uml-diagrams)
   - [Use Case Diagram](#use-case-diagram)
   - [Class Diagram](#class-diagram)
   - [Sequence Diagrams](#sequence-diagrams)
   - [Activity Diagram](#activity-diagram)
   - [ER Diagram](#er-diagram)
7. [Test Cases](#test-cases)
8. [GitHub Project Management](#github-project-management)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [Deployment](#deployment)
11. [Scrum Meetings](#scrum-meeting-summaries)

---

## Project Overview

**TaskFlow** is a lightweight task management application that allows users to create, manage, prioritize, and track tasks across three stages: **Todo**, **In Progress**, and **Done**. Tasks can have titles, descriptions, priorities (High/Medium/Low), and due dates.

---

## Features

- ✅ Create, Read, Update, Delete (CRUD) tasks
- ✅ Kanban-style board (Todo / In Progress / Done)
- ✅ Priority levels (High / Medium / Low)
- ✅ Due date tracking with overdue highlighting
- ✅ Filter tasks by status or priority
- ✅ Live statistics dashboard
- ✅ Responsive design (mobile & desktop)
- ✅ REST API backend

---

## Tech Stack

| Layer      | Technology            |
|------------|-----------------------|
| Backend    | Python 3.11, Flask    |
| Frontend   | HTML5, CSS3, Vanilla JS |
| Storage    | JSON file (tasks.json)|
| Testing    | pytest                |
| CI/CD      | GitHub Actions        |
| Deployment | Render (via render.yaml) |

---

## Setup & Run

### Prerequisites
- Python 3.11+
- pip

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/taskflow.git
cd taskflow

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
# App runs at http://127.0.0.1:5000
```

### Run Tests

```bash
pytest tests/ -v
```

---

## API Reference

| Method | Endpoint              | Description                  |
|--------|-----------------------|------------------------------|
| GET    | `/api/tasks`          | Get all tasks (filterable)   |
| POST   | `/api/tasks`          | Create a new task            |
| GET    | `/api/tasks/<id>`     | Get single task by ID        |
| PUT    | `/api/tasks/<id>`     | Update task fields           |
| DELETE | `/api/tasks/<id>`     | Delete a task                |
| GET    | `/api/stats`          | Get task statistics          |

### Query Parameters (GET /api/tasks)
- `?status=todo|in_progress|done`
- `?priority=low|medium|high`

### Task Object Schema

```json
{
  "id": 1,
  "title": "Implement login",
  "description": "Add JWT auth",
  "priority": "high",
  "status": "todo",
  "due_date": "2025-12-31",
  "created_at": "2025-05-01T10:00:00",
  "updated_at": "2025-05-02T12:00:00"
}
```

---

## UML Diagrams

### Use Case Diagram

```
┌─────────────────────────────────────────────────────┐
│                    TaskFlow System                   │
│                                                      │
│   ┌──────────────────────────────────────────────┐  │
│   │              <<include>>                      │  │
│   │                                              │  │
│   │  (View All Tasks)◄─────────(Filter Tasks)   │  │
│   │                                              │  │
│   │  (Create Task)                               │  │
│   │                                              │  │
│   │  (Edit Task)──────────────►(Update Status)  │  │
│   │                │                             │  │
│   │                └──────────►(Change Priority) │  │
│   │                                              │  │
│   │  (Delete Task)                               │  │
│   │                                              │  │
│   │  (View Stats Dashboard)                      │  │
│   └──────────────────────────────────────────────┘  │
│                        ▲                             │
└────────────────────────┼─────────────────────────────┘
                         │
                     [  User  ]
```

**Actors:** User (single actor — no authentication in v1)

**Use Cases:**
| Use Case | Description |
|---|---|
| View All Tasks | User sees all tasks in Kanban board |
| Create Task | User fills form with title, desc, priority, due date |
| Edit Task | User updates any field of an existing task |
| Update Status | Move task between Todo → In Progress → Done |
| Delete Task | User permanently removes a task |
| Filter Tasks | User filters board by status or priority |
| View Stats Dashboard | User sees counts per status |

---

### Class Diagram

```
┌─────────────────────────────────┐
│             Task                │
├─────────────────────────────────┤
│ - id: int                       │
│ - title: str                    │
│ - description: str              │
│ - priority: str {low,medium,high}│
│ - status: str {todo,in_progress,│
│                done}            │
│ - due_date: str                 │
│ - created_at: datetime          │
│ - updated_at: datetime          │
├─────────────────────────────────┤
│ + to_dict(): dict               │
└─────────────────────────────────┘
             ▲
             │ manages (1..*)
┌─────────────────────────────────┐
│          TaskRepository         │
├─────────────────────────────────┤
│ - data_file: str                │
├─────────────────────────────────┤
│ + load_tasks(): List[Task]      │
│ + save_tasks(tasks): void       │
│ + find_by_id(id): Task|None     │
│ + next_id(tasks): int           │
└─────────────────────────────────┘
             ▲
             │ uses
┌─────────────────────────────────┐
│          FlaskApp               │
├─────────────────────────────────┤
│ - app: Flask                    │
├─────────────────────────────────┤
│ + get_tasks(): Response         │
│ + create_task(): Response       │
│ + get_task(id): Response        │
│ + update_task(id): Response     │
│ + delete_task(id): Response     │
│ + get_stats(): Response         │
└─────────────────────────────────┘
             ▲
             │ sends HTTP requests
┌─────────────────────────────────┐
│       FrontendClient            │
├─────────────────────────────────┤
│ - activeFilter: str             │
│ - editingId: int|null           │
├─────────────────────────────────┤
│ + loadTasks(): void             │
│ + renderBoard(tasks): void      │
│ + createCard(task): HTMLElement │
│ + openEdit(id): void            │
│ + deleteTask(id): void          │
│ + loadStats(): void             │
└─────────────────────────────────┘
```

---

### Sequence Diagrams

#### SD-01: Create Task

```
User          Browser           Flask API         Storage
 │                │                 │                │
 │──[Fill Form]──►│                 │                │
 │──[Click Save]──►│                │                │
 │                │──POST /api/tasks►│               │
 │                │                 │──load_tasks()──►│
 │                │                 │◄──[tasks list]──│
 │                │                 │──validate()     │
 │                │                 │──assign ID      │
 │                │                 │──save_tasks()──►│
 │                │                 │◄────[ok]────────│
 │                │◄──201 + task────│                │
 │                │──renderBoard()  │                │
 │◄───[Board updated]──│            │                │
```

#### SD-02: Update Task Status

```
User          Browser           Flask API         Storage
 │                │                 │                │
 │──[Click Edit]──►│                │                │
 │                │──GET /api/tasks/{id}──►│         │
 │                │◄──[task data]───│                │
 │                │──[Show modal]   │                │
 │──[Change Status]──►│             │                │
 │──[Save]────────►│                │                │
 │                │──PUT /api/tasks/{id}──►│         │
 │                │                 │──find_by_id()  │
 │                │                 │──update fields │
 │                │                 │──save_tasks()──►│
 │                │◄──200 + task────│                │
 │                │──moveCard()     │                │
 │◄───[Card moved]─│                │                │
```

#### SD-03: Delete Task

```
User          Browser           Flask API         Storage
 │                │                 │                │
 │──[Click Delete]►│                │                │
 │                │──[Confirm dialog]│               │
 │──[Confirm]─────►│                │                │
 │                │──DELETE /api/tasks/{id}──►│      │
 │                │                 │──filter out ID  │
 │                │                 │──save_tasks()──►│
 │                │◄──200 Deleted───│                │
 │                │──removeCard()   │                │
 │◄──[Card removed]─│               │                │
```

---

### Activity Diagram — Create Task Flow

```
     [Start]
        │
        ▼
  User clicks "+ New Task"
        │
        ▼
  Modal form opens
        │
        ▼
  User fills in fields
        │
        ▼
  User clicks "Save Task"
        │
        ▼
   ┌────┴────┐
   │ Title   │
   │ empty?  │
   └──┬──┬───┘
     Yes  No
      │    │
      ▼    ▼
  Show   POST /api/tasks
  Error       │
      │       ▼
      │  ┌────┴────┐
      │  │Validate │
      │  │ OK?     │
      │  └──┬──┬───┘
      │    Yes  No
      │     │    │
      │     ▼    ▼
      │  Save  Return
      │  Task   400
      │     │
      │     ▼
      │  Update Board
      │     │
      └────►▼
           [End]
```

---

### Entity Relationship (ER) Diagram

```
┌────────────────────────────────┐
│             TASK               │
├────────────────────────────────┤
│ PK  id          INTEGER        │
│     title       VARCHAR(255)   │
│     description TEXT           │
│     priority    ENUM(low,      │
│                 medium, high)  │
│     status      ENUM(todo,     │
│                 in_progress,   │
│                 done)          │
│     due_date    DATE           │
│     created_at  DATETIME       │
│     updated_at  DATETIME       │
└────────────────────────────────┘

Note: v1 uses JSON flat-file storage.
      This diagram represents the
      logical data model for future
      database migration.
```

---

## Test Cases

| TC ID | Test Name | Category | Input | Expected | Status |
|-------|-----------|----------|-------|----------|--------|
| TC-01 | Get tasks empty | GET /tasks | No tasks | `[]`, 200 | ✅ |
| TC-02 | Get tasks list | GET /tasks | 2 tasks | List of 2, 200 | ✅ |
| TC-03 | Filter by status | GET /tasks?status= | status=in_progress | Only in_progress tasks | ✅ |
| TC-04 | Filter by priority | GET /tasks?priority= | priority=high | Only high tasks | ✅ |
| TC-05 | Create minimal task | POST /tasks | `{title}` | 201, task with defaults | ✅ |
| TC-06 | Create full task | POST /tasks | All fields | 201, all fields saved | ✅ |
| TC-07 | Create no title | POST /tasks | `{description}` | 400 error | ✅ |
| TC-08 | Create empty title | POST /tasks | `{title: "  "}` | 400 error | ✅ |
| TC-09 | Unique IDs | POST x2 | Two tasks | Different IDs | ✅ |
| TC-10 | Get by ID | GET /tasks/1 | Valid ID | Correct task, 200 | ✅ |
| TC-11 | Get nonexistent | GET /tasks/9999 | Invalid ID | 404 error | ✅ |
| TC-12 | Update title | PUT /tasks/1 | `{title: "New"}` | Updated title, 200 | ✅ |
| TC-13 | Update status | PUT /tasks/1 | `{status:"done"}` | Updated status | ✅ |
| TC-14 | Update priority | PUT /tasks/1 | `{priority:"high"}` | Updated priority | ✅ |
| TC-15 | Update missing | PUT /tasks/9999 | Any body | 404 error | ✅ |
| TC-16 | Delete task | DELETE /tasks/1 | Valid ID | 200, task removed | ✅ |
| TC-17 | Delete missing | DELETE /tasks/9999 | Invalid ID | 404 error | ✅ |
| TC-18 | Stats empty | GET /stats | No tasks | All zeros | ✅ |
| TC-19 | Stats counts | GET /stats | Mixed tasks | Correct counts | ✅ |
| TC-20 | Homepage loads | GET / | — | 200, HTML | ✅ |

---

## GitHub Project Management

### Branch Strategy

```
main (production)
  └── develop (integration)
        ├── feature/task-crud
        ├── feature/kanban-board
        ├── feature/priority-filter
        ├── feature/stats-dashboard
        └── bugfix/overdue-highlight
```

### GitHub Issues (Backlog)

| # | Title | Label | Assignee | Sprint |
|---|-------|-------|----------|--------|
| 1 | Set up Flask project structure | setup | Dev A | Sprint 1 |
| 2 | Implement CRUD API endpoints | backend | Dev B | Sprint 1 |
| 3 | Design Kanban board UI | frontend | Dev C | Sprint 1 |
| 4 | Add priority badge system | frontend | Dev A | Sprint 2 |
| 5 | Implement filter by status | feature | Dev B | Sprint 2 |
| 6 | Add stats dashboard | feature | Dev C | Sprint 2 |
| 7 | Write pytest test suite | testing | Dev A | Sprint 2 |
| 8 | Set up GitHub Actions CI/CD | devops | Dev B | Sprint 3 |
| 9 | Deploy to Render | devops | Dev C | Sprint 3 |
| 10 | Write documentation | docs | All | Sprint 3 |

### Scrum Board Columns
- **Backlog** → **Sprint Backlog** → **In Progress** → **Review** → **Done**

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push to `main` or `develop`:

```
Push to GitHub
      │
      ▼
  ┌───────────┐    ┌──────────────┐
  │  Lint Job  │    │  Test Job    │
  │  (flake8) │    │  (pytest)    │
  └─────┬─────┘    └──────┬───────┘
        │                  │
        └──────┬───────────┘
               │ Both pass
               ▼
        ┌──────────────┐
        │  Deploy Job   │
        │ (Render Hook) │
        │ main only     │
        └──────────────┘
```

---

## Deployment

### Using Render (GitHub Student Pack — Free)

1. Sign up at [render.com](https://render.com) using your GitHub Student Pack
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**
5. Add your `RENDER_DEPLOY_HOOK_URL` as a GitHub secret for auto-deploy on push

### Environment Variables
| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |

---

## Scrum Meeting Summaries

### Sprint 1 — Week 1
**Date:** Day 1  
**Attendees:** All team members  
**What was done:**
- Set up GitHub repo, branch strategy agreed
- Flask project scaffolded
- CRUD API endpoints implemented and tested manually

**What's planned next:**
- Frontend Kanban board UI
- Priority badges and due date display

**Blockers:** None

---

### Sprint 2 — Week 2
**Date:** Day 8  
**Attendees:** All team members  
**What was done:**
- Kanban board rendered with 3 columns
- Priority filter and status filter working
- Stats dashboard added

**What's planned next:**
- Full pytest test suite
- GitHub Actions CI setup

**Blockers:** JSON file concurrency (deferred to v2)

---

### Sprint 3 — Week 3
**Date:** Day 15  
**Attendees:** All team members  
**What was done:**
- 20 test cases passing
- CI/CD pipeline green
- Deployed to Render successfully
- README and diagrams finalized

**What's planned next:**
- User authentication (v2 roadmap)
- Database migration to SQLite (v2 roadmap)

**Blockers:** None

---

## Project Structure

```
taskflow/
├── app.py                    # Flask application & API routes
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn start command
├── render.yaml               # Render deployment config
├── .gitignore
├── templates/
│   └── index.html            # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css         # Stylesheet
│   └── js/
│       └── app.js            # Frontend JavaScript
├── tests/
│   └── test_app.py           # 20 pytest test cases
└── .github/
    └── workflows/
        └── ci.yml            # GitHub Actions pipeline
```

---



*TaskFlow v1.0 — Built for Software Engineering Course*
Task CRUD feature added
