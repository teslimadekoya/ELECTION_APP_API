# Election Management System

## Project Overview
The Election Management System is a Django REST Framework-based application that provides a comprehensive solution for managing elections, candidates, and voter participation. The system ensures secure voting through JWT authentication and enforces election rules through robust data models.

## Key Features
- **User Management**: Custom user model with voter/admin roles and unique voter IDs
- **Election Management**: Create and manage elections with status tracking (upcoming/ongoing/completed)
- **Candidate Registration**: Register candidates for elections with party affiliation
- **Voting System**: Secure voting mechanism with one-vote-per-user-per-election enforcement
- **Real-time Statistics**: Track candidate votes and election results
- **REST API**: Comprehensive API endpoints for all operations
- **JWT Authentication**: Secure access to all endpoints

## Technology Stack
- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (default), compatible with other Django-supported databases
- **API Documentation**: DRF built-in browsable API

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/election-management-system.git
   cd election-management-system
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

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Authentication
- **POST /api/token/**: Obtain JWT tokens (access and refresh)
- **POST /api/token/refresh/**: Refresh access token

### Users
- **POST /api/register/**: Register a new user
- **GET /api/users/**: List all users (admin only)
- **GET /api/users/{id}/**: Get user details

### Elections
- **POST /api/elections/**: Create a new election (admin only)
- **GET /api/elections/**: List all elections
- **GET /api/elections/{id}/**: Get election details

### Candidates
- **POST /api/candidates/**: Register a new candidate (admin only)
- **GET /api/candidates/**: List all candidates
- **GET /api/candidates/{id}/**: Get candidate details

### Voting
- **POST /api/vote/**: Cast a vote (Authenticated users only)
   - Request Body: { "election": <election_id>, "candidate": <candidate_id> }
   - Returns: 201 Created on success
   - Errors: 
     - 400 Bad Request if user already voted in this election
     - 400 Bad Request if invalid election/candidate IDs
     - 401 Unauthorized if not authenticated

- **GET /api/votes/**: List all votes
   - Returns: 200 OK with list of all votes
   - Note: Currently accessible to all users

- **GET /api/votes/{id}/**: Get specific vote details
   - Returns: 200 OK with vote details
   - Errors: 404 Not Found if vote doesn't exist

- **DELETE /api/votes/{id}/**: Delete a vote (Admin only)
   - Returns: 204 No Content on success
   - Errors: 404 Not Found if vote doesn't exist

### Election Results
- **GET /api/elections/{id}/results/**: View election results
   - Returns: 200 OK with election results
   - Accessible to both voters and admins

- **POST /api/elections/{id}/results/**: Publish election results (Admin only)
   - Returns: 201 Created with published results
   - Errors: 403 Forbidden if not admin

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
