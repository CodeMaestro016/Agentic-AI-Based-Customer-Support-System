# Agentic-AI-Based-Customer-Support-System

An intelligent customer support system powered by AI agents that provides automated assistance through natural language processing and contextual understanding.

## Features

- 🤖 Multiple specialized AI agents for different tasks
- 📝 Document summarization and RAG (Retrieval-Augmented Generation)
- 🩺 Medical workflow support
- 💬 Dynamic chat system with follow-up capability
- 🔐 User authentication and admin dashboard
- 📊 MongoDB integration for data persistence
- 🎯 Query classification for routing requests
- 🔄 Solution generation with context awareness

## Prerequisites

- Python 3.9+
- MongoDB
- Streamlit (for frontend development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeMaestro016/Agentic-AI-Based-Customer-Support-System.git
cd Agentic-AI-Based-Customer-Support-System
```

2. Create and activate a virtual environment:
```bash
python -m venv env
.\env\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
# MongoDB Configuration
MONGODB_URL=your_mongodb_url
DB_NAME=your_database_name

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (if needed)
OPENAI_API_KEY=your_openai_api_key
```

## Project Structure

```
backend/
├── agents/         # Specialized AI agents
├── core/           # Core configurations
├── database/       # Database connections
├── routes/         # API endpoints
├── schemas/        # Data models
└── utils/          # Utility functions

frontend/
├── pages/          # Streamlit pages
└── image/          # UI assets
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend application:
```bash
cd frontend
streamlit run streamlit_app.py
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:8501

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage

1. **User Registration/Login**
   - Navigate to the signup page to create a new account
   - Login with your credentials

2. **Starting a Chat**
   - Go to the chat interface
   - Type your query in natural language
   - The system will automatically:
     - Classify your query
     - Route to appropriate agent
     - Generate contextual responses

3. **Admin Dashboard**
   - Access administrative features
   - Monitor system usage
   - Manage users and settings

### Common Issues

1. **ModuleNotFoundError**:
   - Ensure you're in the virtual environment
   - Verify all dependencies are installed
   - Check if you're running commands from the correct directory

2. **MongoDB Connection Issues**:
   - Verify MongoDB is running
   - Check connection string in `.env`
   - Ensure network connectivity

3. **Environment Variables**:
   - Confirm `.env` file exists
   - Verify all required variables are set
   - Check for typos in variable names

### Getting Help

If you encounter any issues:
1. Check the existing issues on GitHub
2. Review the documentation
3. Open a new issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages
   - System information
