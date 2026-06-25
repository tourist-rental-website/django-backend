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

```perform_create()``` is used to automatically attach the authenticated user's hotel profile to the room being created instead of allowing the client to provide a hotel ID. This prevents users from creating rooms for other hotels.
```python
    def perform_create(self, serializer):
        if self.request.user.role != 'hotel':
            raise ValidationError("Only hotel users can create rooms.")

        try:
            hotel_profile = self.request.user.hotel_profile-->there is user column in hotel table and user.hotel_profile gets the hotel of authenticated user via reverse lookup 
        except HotelProfile.DoesNotExist:
            raise ValidationError("You must create a hotel profile before creating a room.")

        serializer.save(hotel=hotel_profile)
```
Here, serializer.save() creates and saves the Room object to the database. The hotel=hotel_profile argument sets the room's hotel foreign key to the authenticated user's hotel profile.
This ensures that rooms can only be created under the hotel profile that belongs to the logged-in user.

### List Guide Profiles

A `ListAPIView` was created to return all available guide profiles.

This endpoint will later be used by the frontend to display guides that travelers can browse and hire.

* In The same way create HotelProfile also

- Now in the same way we create review app with review create and list models. Here we need to be careful while creating rating attributes. we should restrict ratings to 1–5 using validators, so users can't submit:
```
{
    "rating": 100
}
```
so we ue 
```
from django.core.validators import MinValueValidator, MaxValueValidator

rating = models.PositiveIntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ]
)
```

# Architecture
This project uses a role-based user system built on Django REST Framework (DRF), where a single User model is extended using role-specific profile models.
```
accounts_user (Base User)
        │
        ├── GuideProfile (OneToOne)
        └── HotelProfile (OneToOne)
```
2. System Architecture
Key Idea
- User → stores authentication + common identity data
- GuideProfile → stores guide-specific information
- HotelProfile → stores hotel-specific information

This avoids duplication and keeps the system scalable.

2. Nested Fields Concept

Nested fields allow accessing related model data inside serializers using source.

Example
first_name = serializers.CharField(source='user.first_name')
phone = serializers.CharField(source='user.phone')
profile_image = serializers.ImageField(source='user.profile_image')
Meaning
These fields:
Do NOT belong to GuideProfile or HotelProfile
They Belong to User model and are accessed via relationship:
Profile → User → Field

3. Updating Nested Fields

Nested fields require explicit handling during update.

Incorrect Approach 
- instance.first_name = "John"
Correct Approach 
= instance.user.first_name = "John"
instance.user.save()

4. Handling Multi-Table Updates in Serializer

When a serializer includes both:

Profile fields
Nested User fields

We split the data manually.

Example
def update(self, instance, validated_data):
    user_data = validated_data.pop("user", {})

    # Update User table
    user = instance.user
    user.first_name = user_data.get("first_name", user.first_name)
    user.phone = user_data.get("phone", user.phone)
    user.profile_image = user_data.get("profile_image", user.profile_image)
    user.save()

    # Update Profile table
    instance.bio = validated_data.get("bio", instance.bio)
    instance.location = validated_data.get("location", instance.location)
    instance.save()

    return instance

5. super().update() vs Manual Update

- super().update()
return super().update(instance, validated_data)
Use when:
Only one model is involved
No nested relationships

- Manual Update
instance.field = validated_data.get("field", instance.field)
instance.save()
Use when:
Multiple models involved (User + Profile)
Nested fields exist
