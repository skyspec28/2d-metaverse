# 2D Metaverse

A virtual world platform where users can interact, customize their avatars, and explore different spaces.

## Features

- User authentication and registration
- Avatar customization
- Real-time movement and interaction
- Multiple customizable spaces
- Interactive elements
- WebSocket-based communication
- Admin dashboard

## Tech Stack

### Backend
- Django
- Django REST Framework
- Channels (WebSockets)
- PostgreSQL
- Redis

### Frontend
- React
- TypeScript
- Phaser.js
- Material-UI

## Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL
- Redis

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Running the Application

1. Start the backend server:
```bash
python manage.py runserver
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the application at `http://localhost:3000`

## API Documentation

### Authentication
- POST `/api/auth/register/` - Register a new user
- POST `/api/auth/login/` - Login and get JWT tokens

### Spaces
- GET `/api/spaces/all/` - List all spaces
- POST `/api/spaces/new/` - Create a new space
- DELETE `/api/spaces/delete/<id>/` - Delete a space

### Avatars
- GET `/api/avatars/<id>/` - Get avatar details
- POST `/api/admin/avatar/new/` - Create a new avatar (admin only)

### Elements
- POST `/api/admin/element/new/` - Create a new element (admin only)
- PUT `/api/admin/element/update/<id>/` - Update an element (admin only)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m '✨ feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.