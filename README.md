# FaundaTrek Backend API

A Django REST Framework backend for the FaundaTrek social e-commerce platform, built with modern web technologies and best practices.

## 🚀 Features

- **User Management**: Multi-role user system (Entrepreneur, Investor, Donor, Admin)
- **Social Stories**: Text, image, and video posts with likes and comments
- **Pitch Platform**: Entrepreneurs can upload business pitches with funding goals
- **Donation System**: Support for monetary and material donations with tracking
- **Messaging**: 1-on-1 chat system between users
- **JWT Authentication**: Secure token-based authentication
- **RESTful API**: Clean, consistent API design
- **File Uploads**: Support for images, videos, and documents
- **Search & Filtering**: Advanced search and filtering capabilities
- **Pagination**: Efficient data pagination for large datasets

## 🛠️ Tech Stack

- **Backend**: Django 5.2.5 + Django REST Framework 3.16.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT with djangorestframework-simplejwt
- **File Storage**: Local storage (dev) / AWS S3/DO Spaces (prod)
- **CORS**: django-cors-headers for frontend integration
- **Deployment**: Ready for Heroku, Railway, AWS, or any cloud platform

## 📋 Requirements

- Python 3.8+
- Django 5.2.5+
- PostgreSQL (for production)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Fundatrek
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=fundatrek_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Database Setup

```bash
# For development (SQLite - default)
python manage.py migrate

# For production (PostgreSQL)
# Update settings.py to use PostgreSQL
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login

### Profiles
- `GET /api/profile/{id}/` - Get user profile
- `PUT /api/profile/{id}/` - Update user profile

### Stories
- `GET /api/stories/` - List all stories
- `POST /api/stories/` - Create new story
- `GET /api/stories/{id}/` - Get story details
- `PUT /api/stories/{id}/` - Update story
- `DELETE /api/stories/{id}/` - Delete story
- `POST /api/stories/{id}/like/` - Like/unlike story
- `POST /api/stories/{id}/comment/` - Add comment to story

### Pitches
- `GET /api/pitches/` - List all pitches
- `POST /api/pitches/` - Create new pitch
- `GET /api/pitches/{id}/` - Get pitch details
- `PUT /api/pitches/{id}/` - Update pitch
- `DELETE /api/pitches/{id}/` - Delete pitch

### Donations
- `GET /api/donations/` - List all donations
- `POST /api/donations/` - Create new donation
- `GET /api/donations/{id}/` - Get donation details
- `PUT /api/donations/{id}/` - Update donation
- `DELETE /api/donations/{id}/` - Delete donation
- `POST /api/donations/{id}/contribute/` - Contribute to donation

### Messages
- `GET /api/messages/` - List user's messages
- `POST /api/messages/` - Send new message
- `GET /api/messages/{user_id}/` - Get conversation with specific user
- `POST /api/messages/{id}/read/` - Mark message as read

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

### Token Endpoints
- **Access Token**: Valid for 5 hours (configurable)
- **Refresh Token**: Valid for 1 day (configurable)
- **Auto-rotation**: Refresh tokens are automatically rotated

## 📁 File Uploads

The API supports file uploads for:
- Profile pictures
- Story images and videos
- Pitch documents (PDFs, videos)
- Any other file types

Files are stored in the `media/` directory during development and can be configured for cloud storage in production.

## 🔍 Search & Filtering

All list endpoints support:
- **Search**: Text search across relevant fields
- **Filtering**: Filter by various criteria
- **Ordering**: Sort by different fields
- **Pagination**: 20 items per page (configurable)

### Example Queries
```
GET /api/stories/?search=entrepreneurship&ordering=-created_at
GET /api/pitches/?search=tech&ordering=funding_goal
GET /api/donations/?search=education&ordering=deadline
```

## 🚀 Deployment

### Heroku
```bash
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key

# Deploy
git push heroku main
```

### Railway
```bash
# Connect your GitHub repository
# Railway will automatically detect Django and set up the environment
```

### AWS/DigitalOcean
- Use RDS for PostgreSQL
- Use S3/Spaces for file storage
- Deploy to EC2/Droplet or use container services

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage:
- Users and profiles
- Stories and content
- Pitches and funding
- Donations and contributions
- Messages and conversations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Changelog

### v1.0.0
- Initial release
- Complete user management system
- Social stories with media support
- Pitch platform with funding tracking
- Donation system with contribution tracking
- Messaging system
- JWT authentication
- RESTful API design
- Admin interface
- File upload support
- Search and filtering
- Pagination
- CORS support for frontend integration
