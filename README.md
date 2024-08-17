```markdown
# FastAPI Application
## Prerequisites

- Python 3.7 or later
- pip (Python package installer)

## Setting Up the Project

1. **Clone the Repository**

   ```bash
   git clone https://github.com/snython/courses_backend.git
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Command Prompt**:
     ```bash
     venv\Scripts\activate
     ```

   - **PowerShell**:
     ```bash
     .\venv\Scripts\Activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirement.txt
   ```

## Running the Application

1. **Navigate to the Project Directory**

   Ensure you are in the directory where your `main.py` file is located.

2. **Run the Application Using Uvicorn**

   ```bash
   -uvicorn app.main:app --reload
   ```

   - `main:app` refers to the `main.py` file and the `app` FastAPI instance within it.
   - `--host 0.0.0.0` allows external access.
   - `--port 8000` runs the app on port 8000.
   - `--reload` enables auto-reloading for development.

3. **Access the Application**

   Open your web browser and navigate to:

   ```
   http://localhost:8000
   ```

   You can also view the API documentation at:

   - **Swagger UI**: `http://localhost:8000/docs`
   - **ReDoc**: `http://localhost:8000/redoc`

## Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

- **Command Not Found**: Ensure you have activated the virtual environment.
- **Port Conflict**: If port 8000 is in use, change the port number in the `uvicorn` command.



Run the create_env.py script to create the .env file with default environment variable

-python app/db/create_env.py

run the applicatioon using the command

-uvicorn app.main:app --reload

Url to have access to the swagger API documentation
--http://ip:8000/docs