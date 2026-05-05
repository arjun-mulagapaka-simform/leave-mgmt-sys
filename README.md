# Leave Management System

## Overview

Leave Management System is a Django-based employee leave management application with a REST API, JWT authentication, role-based approval workflows, leave balance tracking, and a small frontend for interaction.

The project includes:
- `user_mgmt`: employee, department, and role management
- `leavemanagement`: leave requests, leave policies, approvals, and business rules
- `common`: role/permission and employee scope utilities
- `frontend`: HTML + JavaScript pages for login, dashboard, leave request, leave history, and pending approvals
- `leave_mgmt_sys`: Django project configuration, JWT auth, and URL routing

## Key Features

- JWT authentication for secure API access
- Custom `Employee` user model with email login
- Role-based access control for employees, reporting managers, managers, and HR
- Leave request creation with overlapping-date prevention
- Leave approval and rejection workflow
- Leave balance computation based on approved leaves and policy rules
- Email notification tasks using Celery
- Basic frontend pages for users to request and review leaves

## Architecture

### Apps

- `user_mgmt`
  - Models: `Employee`, `Department`, `Role`
  - Serializers: `EmployeeSerializer`
  - Views: employee list, retrieve/update, current user details
  - URLs: auth, employee endpoints, `api/me`

- `leavemanagement`
  - Models: `LeaveLog`, `LeavePolicy`, `LeaveTypeEnum`
  - Serializers: `LeaveLogSerializer`
  - Views: leave CRUD, pending leaves, approval, balance retrieval
  - Services: `LeaveBalance`
  - Tasks: Celery email notifications for leave request and approval/rejection
  - URLs: leave and approval endpoints

- `common`
  - Permissions: `IsEmployee`, `IsReportingManager`, `IsManager`, `IsHR`, and combined role permissions
  - Scope service: `ScopeOfEmployee` for employee visibility and reporting hierarchy

- `frontend`
  - Views: page renderers for dashboard, login, leave request, leave history, pending leaves, and leave detail
  - Templates: HTML files under `templates/frontend`
  - Static assets: front-end JavaScript and CSS files

## Database Models

### `Employee`
- `email` (unique)
- `first_name`, `last_name`
- `department` (FK to `Department`)
- `reporting_manager` (self-referencing FK)
- `role` (FK to `Role`)
- `is_staff`

### `Department`
- `name`
- `manager` (OneToOne to `Employee`)
- `hr` (OneToOne to `Employee`)

### `Role`
- `name`

### `LeaveLog`
- `employee` (FK to `Employee`)
- `leave_type` (`paid`, `unpaid`, `compensation`, `incident`)
- `start_date`, `end_date`
- `status` (`pen`, `apr`, `rej`)
- `reason`
- `actioned_by` (FK to `Employee`)
- `rejection_reason`

### `LeavePolicy`
- `name`
- `given_days`
- `leave_type`

## API Endpoints

### Authentication
- `POST /user/api/token/` — obtain access and refresh tokens
- `POST /user/api/token/refresh/` — refresh access token
- `POST /user/api/logout/` — blacklist refresh token

### User Management
- `GET /user/api/me` — current authenticated user details
- `GET /user/employees/` — list employees within current user scope
- `GET /user/employees/<id>/` — retrieve employee by id
- `PUT /user/employees/<id>/` — update employee (manager-only for updates)
- `PATCH /user/employees/<id>/` — partial employee update

### Leave Management
- `GET /leaves/` — list leave requests for authenticated employee
- `POST /leaves/` — create a new leave request
- `GET /leaves/<id>/` — retrieve leave request
- `PUT /leaves/<id>/` — update leave request
- `PATCH /leaves/<id>/` — partially update leave request
- `GET /leaves/pending/` — list pending leave requests for manager/HR scope
- `PUT /leaves/<id>/approve/` — approve or reject a leave request
- `GET /leaves/balance/` — retrieve current leave balance for authenticated user

> Note: The exact URL patterns for approval and balance endpoints are implied by the `leavemanagement` app and may depend on routing definitions.

## Frontend Pages

- `/` — dashboard
- `/login` — login page
- `/leaves/request` — leave request form
- `/leaves/all` — leave history page
- `/leaves/<id>` — leave detail page
- `/leaves/pending` — pending leaves review page

## Setup

1. Activate the existing virtual environment:
   ```bash
   source leave_m_s_env/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in a `.env` file, including `secret_key` and `database_pass`.
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start Django development server:
   ```bash
   python manage.py runserver
   ```
6. Start Celery worker if email tasks are required:
   ```bash
   celery -A leave_mgmt_sys worker --loglevel=info
   ```

## Notes

- The project uses PostgreSQL as configured in `leave_mgmt_sys/settings.py`.
- JWT authentication is enabled by `rest_framework_simplejwt`.
- Leave balance is calculated from approved leaves and configured leave policies.
- The `common` app defines role-based scopes and permissions for manager/HR workflows.

## Project Status

This is a completed leave management backend with role-aware approval workflows, leave validation, and frontend page stubs. Ongoing work may include enhanced UI integration, complete admin management, and production-ready deployment configuration.