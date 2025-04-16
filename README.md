# Receipt Processor API

This Flask application processes receipt data and calculates points based on the provided information.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # venv\Scripts\activate  # For Windows (Command Prompt)
    # venv\Scripts\Activate.ps1 # For Windows Powershell
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    ```bash
    flask init-db
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    or, with debug mode:
    ```bash
    export FLASK_DEBUG=True #Linux/macOS
    #set FLASK_DEBUG=True #windows command prompt
    #$env:FLASK_DEBUG = "True" #windows powershell
    python app.py
    ```

6.  **Docker (Optional):**

    -   Build and run the Docker container:
        ```bash
        docker-compose up --build
        ```

## API Endpoints

* **`POST /receipts/process`**: Processes a receipt and returns a receipt ID.
    * Request body: JSON receipt data.
    * Response: JSON containing the receipt ID.
* **`GET /receipts/<receipt_id>/points`**: Retrieves points for a given receipt ID.
    * Response: JSON containing the points.

## Database

* SQLite database (`receipts.db`) is used for data storage.
* Database file is stored in the `data` directory.

## Environment Variables

* `DATABASE_FOLDER`: Specifies the directory for the SQLite database. Defaults to `./data`.
* `FLASK_DEBUG`: Enables Flask debug mode when set to `True`.
