# Ollama Chat

Ollama Chat is a chat application built using FastAPI, which allows users to communicate in real-time. This project leverages several key technologies to deliver a robust and scalable chat experience.

## Features

- Real-time messaging with WebSocket support
- User authentication and management
- Scalable architecture with PostgreSQL database
- RESTful API for integration

## Requirements

- Python 3.x
- PostgreSQL database
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ollama-chat.git
   cd ollama-chat
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Create a PostgreSQL database 
   - Configure your `.env` file with database credentials

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

- Open your browser and navigate to `http://localhost:8000` to access the chat application.

## Contributing

We welcome contributions! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

