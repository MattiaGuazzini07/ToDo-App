# ToDo App – Task Management with Django 5.2

**ToDo App** is a responsive web application built with Django 5.2 for advanced personal task management. It features user-role-based dashboards, interactive tools, enhanced security, and a clean, modern interface. Developed as a learning project, it now stands as a fully functional and scalable application.

---

## Project Goals

- Create a complete, user-friendly ToDo app for authenticated users
- Organize tasks with deadlines, priorities, descriptions, and completion status
- Implement role-based dashboards: User, Staff, Administrator
- Design a modern, responsive UI with Flexbox and animations
- Include interactive tools like a calendar and guided tour
- Maintain a detailed changelog and use Git professionally

---

## Tech Stack

- **Backend**: Django 5.2, Python 3.12
- **Database**: SQLite → PostgreSQL (via Neon.tech)
- **Frontend**: HTML, custom CSS, Flexbox, JavaScript, FontAwesome, Lucide
- **Tooling**: Git (branches, merges, rebase, reset), .env, WhiteNoise for static files

---

## Project Structure

```bash
ToDo-App/
│
├── backend/
│   ├── accounts/         # user and profile management
│   ├── tasks/            # task management and dashboards
│   ├── static/           # CSS, JS, images
│   ├── templates/        # HTML split by app and role
│   └── settings.py       # Django settings
│
├── media/                # avatars and user files
├── manage.py
├── requirements.txt
├── .env
```

---

## User Roles and Permissions

- **Normal User**: manage their own tasks
- **Staff**: read-only access to all tasks
- **Admin**: user management, task counters, filters, admin dashboard

---

## Security Features

- POST-only login/logout for extra security
- Full CSRF protection on all views
- Django permissions and `@login_required` decorators
- Role-specific views and access

---

## UI and UX Highlights

- Fully responsive with Flexbox
- Smooth CSS animations and transitions
- Custom user dropdown with quick actions
- FullCalendar integration for visual task overview
- Interactive guided tour with Shepherd.js (CSRF-safe)
- Accessible and consistent UI with helpful user guide

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MattiaGuazzini07/DjangoApp.git
cd DjangoApp
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up `.env` file with database and secret key settings.

5. Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

---

## Development History

Every feature was developed through clear Git commits, tracked across separate branches. The changelog (see `Relazione progetto ToDo App.docx`) documents the evolution from `v0.0.1` to the stable `v1.0.1`.

---


## Future Roadmap

- Email notifications for upcoming deadlines
- Drag & Drop functionality in the calendar
- Task statistics and progress tracking
- Multilanguage support

---

## Educational Value

This project served as a deep dive into Django and web development best practices. It includes real-world features like secure authentication, dashboard permissions, responsive design, and full Git-based version control. A complete technical and personal growth journey.

---

## Acknowledgements

- Guided support from GPT for technical and structural feedback
- FullCalendar and Shepherd.js libraries
- Django community for extensive documentation and examples
