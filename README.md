# ToDo App – Task Management with Django 5.2

**ToDo App** is a feature-rich, responsive web application built with Django 5.2. It began as a learning project and evolved into a multi-user platform for advanced task and team management. It includes role-based dashboards, collaborative tools, secure authentication, and a dark mode-ready modern interface.

---

## Project Goals

* Create a complete, user-friendly ToDo app for authenticated users
* Organize tasks with deadlines, priorities, descriptions, and completion status
* Implement role-based dashboards: User, Staff, Administrator
* Add collaborative features such as teams and friend connections
* Design a modern, responsive UI with Flexbox, dark mode, and animations
* Include interactive tools like FullCalendar and guided tours
* Maintain a detailed changelog and use Git professionally

---

## Tech Stack

* **Backend**: Django 5.2, Python 3.12
* **Database**: SQLite → PostgreSQL (via Neon.tech)
* **Frontend**: HTML5, custom CSS (Flexbox, dark mode), JavaScript modules, Lucide Icons
* **JS Modules**: toggle\_completed.js, auto\_dismiss.js, avatar\_dropdown.js, dark\_mode\_toggle.js
* **Tooling**: Git (branches, merges, rebase), .env, WhiteNoise, CSRF protection

---

## Project Structure

```bash
ToDo-App/
│
├── backend/
│   ├── accounts/         # user profiles, auth, settings
│   ├── tasks/            # task logic, forms, views, dashboards
│   ├── teams/            # team management and team-tasks
│   ├── static/           # CSS, JS, images (darkmode, modules)
│   ├── templates/        # role-based HTML views
│   └── settings.py       # Django project configuration
│
├── media/                # user uploads (avatars)
├── manage.py
├── requirements.txt
├── .env
```

---

## User Roles and Permissions

* **Normal User**: manage their own tasks
* **Staff**: read-only access to all tasks
* **Admin**: manage users, all tasks, stats, filters
* **Team Members**: shared task views, assignments, permissions per team

---

## Security Features

* POST-only login/logout for extra security
* Full CSRF protection on all forms and views
* Django permissions and `@login_required` decorators
* Group-based access control for dashboard segregation

---

## UI and UX Highlights

* Fully responsive layout using Flexbox
* Clean modular CSS with support for light/dark themes
* Custom switch buttons, dropdowns, and icon badges
* FullCalendar integration for task visualization
* Guided tour (Shepherd.js) with CSRF safety
* Live toggle for dark mode without reload
* Enhanced error and success messages with fade-out animations

---

## Collaborative Features

* **Team Mode**: create/join teams, assign shared tasks, manage roles
* **Friendship System**: send/accept friend requests, filter user list
* **Team Dashboard**: track member stats, visualize progress (Chart.js)
* **Shared Tasks**: team-wide assignments with completion tracking

---

## Dark Mode and Accessibility

* Toggle switch for live dark mode (user profile preference)
* Dedicated dark stylesheets for all pages (including admin views)
* Keyboard accessibility and screen-reader friendly markup
* Visual improvements and color contrast tuning

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MattiaGuazzini07/DjangoApp.git
cd DjangoApp
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your `.env` with secret key and database credentials

5. Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

---

## Development History

Every feature was developed through version-controlled Git branches. The full development timeline is documented in `Relazione progetto ToDo App.docx`, covering versions from `v0.0.1` to `v2.0.0`, including key upgrades like team collaboration, dark mode, modular JS, and graph dashboards.

---

## Future Roadmap

* Email notifications for upcoming deadlines
* Drag & Drop task reordering in calendar
* Enhanced statistics and progress charts
* Real-time team updates (WebSocket)
* Multilanguage interface (i18n)

---

## Educational Value

This project served as an in-depth exercise in Django development, frontend UI/UX, and real-world architecture. It features modular design, collaborative features, accessibility, robust security, and complete Git workflow. It reflects a comprehensive learning and building journey.

---

## Acknowledgements

* Technical guidance from ChatGPT (OpenAI)
* Libraries: FullCalendar, Shepherd.js, Chart.js, Lucide Icons
* Django documentation and open-source examples
