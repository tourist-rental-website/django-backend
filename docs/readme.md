# Backend App Development Journey

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
## 6. JWT Authentication (Login System)

### Overview

After implementing user registration, the next step in the authentication system is **JWT-based login**. This allows users to securely log in and receive tokens that are used for accessing protected API endpoints.

JWT (JSON Web Token) authentication is stateless, meaning the server does not store session data. Instead, the client stores the token and sends it with each request.

---

### Login Flow

The login process works as follows:

```text
User enters email and password
        ↓
Frontend sends POST request
        ↓
Django verifies credentials
        ↓
If valid → JWT tokens generated
        ↓
Access + Refresh tokens returned
        ↓
Frontend stores tokens
        ↓
Tokens used for protected API requests
```

---

### API Endpoint

#### Login Endpoint

```
POST /api/accounts/login/
```

---

### Request Format

```json
{
    "email": "user@example.com",
    "password": "userpassword"
}
```

## Token Types

### 1. Access Token

* Short-lived
* Used for authentication in API requests
* Sent with every request

### 2. Refresh Token

* Long-lived
* Used to generate new access tokens
* Sent only when access token expires

---

### Final Flow

```text
Login Request
     ↓
Validate Credentials
     ↓
Generate JWT Tokens
     ↓
Return to Client
     ↓
Client uses token for protected APIs
```
## 7. User Profile

### `/accounts/me/` API

This endpoint is used to get and update the currently logged-in user’s profile using JWT authentication.

It helps the frontend identify who is logged in and allows users to update their own basic information.

### Methods

### GET – Get Current User

Returns the details of the authenticated user.

#### Response

```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "9800000000",
    "role": "traveler"
}
```

---

### PATCH – Update User Profile

Allows the logged-in user to update their profile partially.

#### Request

```json
{
    "first_name": "John",
    "phone": "9812345678"
}
```

#### Response

```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "9812345678",
    "role": "traveler"
}
```

## 8. Guide Profile

After completing user authentication and profile management, the next step was to create a dedicated profile model for guides.

The purpose of the `GuideProfile` model is to store guide-specific information separately from the User model. This keeps the User model clean and allows different user roles (Traveler, Guide, Hotel) to have their own specialized data.

### Model Design

A One-to-One relationship was created between `User` and `GuideProfile`.

```text
User
  │
  └── GuideProfile
```

This ensures that:

* One user can have only one guide profile.
* Each guide profile belongs to exactly one user.


The `user` field was marked as read-only because it is assigned automatically from the authenticated user.

### Create Guide Profile

Authenticated users can create a guide profile.

#### View

```python
class GuideProfileCreateView(generics.CreateAPIView):
    serializer_class = GuideProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

### Why use `perform_create()`?

Instead of allowing clients to send a user ID, the authenticated user is automatically attached to the GuideProfile.

```python
serializer.save(user=self.request.user)
```

This ensures that users can only create guide profiles for themselves.


### List Guide Profiles

A `ListAPIView` was created to return all available guide profiles.

This endpoint will later be used by the frontend to display guides that travelers can browse and hire.

* In The same way create HotelProfile also


## 9. Hotel Profile

After implementing the GuideProfile system, a similar profile model was created for hotel providers.

The purpose of the `HotelProfile` model is to store hotel-specific information separately from the User model. This allows hotel users to maintain information related to their hotels without cluttering the core User model.

### Model Design

A One-to-One relationship was created between `User` and `HotelProfile`.

```text
User
  │
  └── HotelProfile
```

This ensures that:

* One hotel user can have only one hotel profile.
* Each hotel profile belongs to exactly one user.

### Create Hotel Profile

Authenticated hotel users can create a hotel profile.

#### View

```python
class HotelProfileCreateView(generics.CreateAPIView):
    serializer_class = HotelProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

The authenticated user is automatically attached to the profile.

### List Hotel Profiles

A `ListAPIView` was created to return all available hotel profiles.

This endpoint will later be used by travelers to browse hotels available on the platform.

---

## 10. Room Management

After creating hotel profiles, a Room model was added to allow hotels to manage individual rooms.

### Model Design

A many-to-one relationship was created between `HotelProfile` and `Room`.

```text
HotelProfile
      │
      ├── Room
      ├── Room
      └── Room
```

This ensures that:

* One hotel can have many rooms.
* Each room belongs to exactly one hotel.

### Room Fields

* room_type
* price_per_night
* capacity
* is_available
* created_at

### Create Room

Only authenticated users with the hotel role can create rooms.

#### Flow

```text
Authenticated Hotel User
          ↓
Hotel Profile
          ↓
Room Creation
          ↓
Database
```

The hotel profile is automatically attached during creation.

```python
serializer.save(hotel=hotel_profile)
```

This prevents users from creating rooms for other hotels.

### List Rooms

A public endpoint was created to allow travelers to browse all available rooms.

---

## 11. Tour Package Management

A Package model was created to allow guides to offer tourism packages to travelers.

### Model Design

A many-to-one relationship was created between `GuideProfile` and `Package`.

```text
GuideProfile
      │
      ├── Package
      ├── Package
      └── Package
```

This ensures that:

* One guide can create multiple tour packages.
* Each package belongs to exactly one guide.

### Package Fields

* title
* description
* duration_days
* price
* location
* created_at

### Create Package

Only authenticated users with the guide role can create packages.

#### Flow

```text
Authenticated Guide User
          ↓
Guide Profile
          ↓
Package Creation
          ↓
Database
```

The guide profile is automatically attached during creation.

```python
serializer.save(guide=guide_profile)
```

This prevents users from creating packages for other guides.

### List Packages

A public endpoint was created to allow travelers to browse available tour packages.

---

## 12. Role-Based Access Control

The application uses role-based access control to ensure that users can only perform actions relevant to their role.

### Traveler

Can:

* Register and login
* View guide profiles
* View hotel profiles
* View rooms
* View tour packages

### Guide

Can:

* Create and manage a guide profile
* Create tour packages
* View public listings

### Hotel

Can:

* Create and manage a hotel profile
* Create rooms
* View public listings

Role validation is performed inside the view layer before creating role-specific resources.

---

## 13. Admin Panel Configuration

All major models are registered in Django Admin for easier management and testing.

Registered models:

* User
* GuideProfile
* HotelProfile
* Room
* Package

The admin panel allows administrators to:

* View records
* Create records
* Edit records
* Delete records

without directly interacting with the database.

---

## 14. Current Database Relationships

```text
User
 ├── GuideProfile (One-to-One)
 │      └── Package (One-to-Many)
 │
 └── HotelProfile (One-to-One)
        └── Room (One-to-Many)
```

This structure separates authentication data from business-specific data while maintaining clear ownership relationships throughout the application.
