# Note Project

This is a Django project that provides a RESTful API for creating, managing, and sharing notes. The API allows users to perform CRUD operations on notes, share notes with other users, and search for notes based on keywords.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Throttling](#throttling)
- [Security](#security)
- [Testing](#testing)
- [Search Functionality](#search-functionality)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create, read, update, and delete notes
- Share notes with other users
- Search for notes based on keywords
- Authentication and authorization mechanisms
- Rate limiting and request throttling
- Unit, integration, and end-to-end tests

## Getting Started

### Prerequisites

- Python (>=3.6)
- Django (>=3.0)
- Django REST Framework (>=3.11)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JathinShyam/note_project.git
   cd note_project
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
## Configuration

1. Apply database migrations:

   ```bash
   python manage.py migrate
2. Create a superuser for administrative access:

   ```bash
   python manage.py createsuperuser
Follow the prompts to create a superuser account.

3. Run the development server:

   ```bash
   python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

## API Endpoints
### Authentication Endpoints:

- (POST) **/api/auth/signup:** Create a new user account.
- (POST) **/api/auth/login:** Log in to an existing user account and receive an access token.

### Note Endpoints:

- (GET) **/api/notes:** Get a list of all notes for the authenticated user.
- (GET) **/api/notes/:id:** Get a note by ID for the authenticated user.
- (POST) **/api/notes:** Create a new note for the authenticated user.
- (PUT) **/api/notes/:id:** Update an existing note by ID for the authenticated user.
- (DELETE) **/api/notes/:id:** Delete a note by ID for the authenticated user.
- (POST) **/api/notes/:id/share:** Share a note with another user for the authenticated user.
- (GET) **/api/search?q=:query:** Search for notes based on keywords for the authenticated user.

## Throttling

The project uses rate limiting and request throttling to handle high traffic. Default rates can be configured in the settings.py file.

## Security

The code implements secure authentication and authorization mechanisms, including the use of Token Authentication and session authentication.

## Testing

The project includes unit tests, integration tests, and end-to-end tests for all endpoints. You can run the tests using:
1. Testing
   ```bash
   python manage.py test
## Search Functionality

The code implements text indexing and search functionality using PostgreSQL's Full Text Search. Users can search for notes based on keywords efficiently.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.