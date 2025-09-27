# Contributing to yt-dlp Web UI

Thank you for your interest in contributing to yt-dlp Web UI! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/ytdlp-webui.git
   cd ytdlp-webui
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

## Development Workflow

### Running the Application

1. **Start backend**
   ```bash
   cd backend
   source venv/bin/activate
   python -m src.main
   ```

2. **Start frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Code Style

#### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Use Black for formatting: `black .`
- Use isort for imports: `isort .`

#### JavaScript/React (Frontend)
- Use ESLint configuration provided
- Use Prettier for formatting: `npm run format`
- Follow React best practices
- Use functional components with hooks

### Testing

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write tests for new functionality
   - Update documentation if needed
   - Ensure all tests pass

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots for UI changes

## Issue Reporting

When reporting issues, please include:

- **Environment**: OS, Python version, Node.js version
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Relevant error messages

## Feature Requests

For feature requests, please:

- Check existing issues first
- Provide a clear use case
- Explain the expected behavior
- Consider implementation complexity

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks or political discussions
- Spam or off-topic discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

Feel free to open an issue for questions about contributing or the development process.

