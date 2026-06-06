# Accounts App Development Journey

## 1. Creating a Custom User Model

The first step was to create a custom User model. Django provides a default User model that uses a username for authentication. However, for this project, email-based authentication was chosen because it provides a better user experience and removes the need for users to remember a separate username.

The User model extends Django's `AbstractUser` class, which already provides common authentication-related fields and functionality such as:

* password
* first_name
* last_name
* is_active
* is_staff
* is_superuser
* permissions

Since email authentication is being used, the default username field was removed and email was configured as the unique identifier for authentication.

Additional project-specific fields were also added:

* role (traveler, guide, hotel)
* phone number

The User model is responsible for defining the structure of the user data stored in the database.

---

## 2. Creating a Custom User Manager

After creating the custom User model, a custom UserManager was implemented.

Normally, Django's default UserManager assumes that users are created using a username. Since this project uses email authentication, a custom manager is required to define how users and superusers are created.

The custom manager contains two important methods:

### create_user()

This method is responsible for creating normal users.

Responsibilities:

* Ensure an email is provided.
* Normalize the email address.
* Hash the password using Django's built-in password hashing system.
* Save the user to the database.

Using `set_password()` is important because passwords should never be stored as plain text.

### create_superuser()

This method is responsible for creating administrators.

Responsibilities:

* Set `is_staff=True`
* Set `is_superuser=True`
* Set `is_active=True`
* Reuse the `create_user()` method to avoid code duplication

The UserManager acts as the factory responsible for creating User objects correctly.

---

## 3. Database Migration

After creating the User model and UserManager, migrations were generated and applied.

Commands used:

```bash
python manage.py makemigrations
python manage.py migrate
```

This created the necessary database tables for authentication and the custom User model.

---

## 4. Creating the Register Serializer

After the database structure was ready, the next step was to create a serializer using Django REST Framework.

A serializer acts as the bridge between incoming API requests and Django models.

Responsibilities of the RegisterSerializer:

* Receive incoming registration data.
* Validate the data.
* Convert JSON data into Python objects.
* Create a new user in the database.
* Return serialized user data in the API response.

Example registration request:

```json
{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "traveler"
}
```

The serializer validates the request and then calls:

```python
User.objects.create_user(...)
```

which delegates the actual user creation process to the custom UserManager.

This separation keeps validation logic and database creation logic organized.

Flow:

```text
Request Data
      ↓
Serializer Validation
      ↓
UserManager
      ↓
Database
```

---

## 5. Creating the Register View

After creating the serializer, a registration endpoint was implemented using Django REST Framework's `CreateAPIView`.

The RegisterView is responsible for handling HTTP requests related to user registration.

Responsibilities:

* Accept POST requests.
* Pass request data to the serializer.
* Trigger validation.
* Save the user if validation succeeds.
* Return an appropriate response.

The view does not directly interact with the database. Instead, it delegates validation and object creation to the serializer.

Flow:

```text
Client Request
      ↓
RegisterView
      ↓
RegisterSerializer
      ↓
UserManager
      ↓
Database
```

Using `CreateAPIView` reduces boilerplate code because Django REST Framework already provides the common logic required for creating new objects.

---

## Summary

At this stage, the authentication system consists of:

1. Custom User Model
2. Custom User Manager
3. PostgreSQL Database Integration
4. Register Serializer
5. Register API View

Current Registration Flow:

```text
POST /accounts/register/
         ↓
RegisterView
         ↓
RegisterSerializer
         ↓
Validation
         ↓
UserManager.create_user()
         ↓
Password Hashing
         ↓
Database Save
         ↓
Response Returned
```

This establishes the foundation for future authentication features such as login, JWT authentication, profile management, password reset, and role-based permissions.
