
# ClanZenit

## Description

ClanZenit is a Flask-based application designed to manage people and their associated roles. The project allows users to:

- Add, edit, and remove people.
- Define and manage roles.
- Rotate roles among people.
- Change a person’s role dynamically.

This tool is ideal for organizations, clubs, or teams requiring efficient role management.

---

## Installation

Follow the steps below to set up the ClanZenit project:

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ClanZenit
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
    set these environment variables in the activate file in `.venv/bin/activate`
   ```env
   dbUser=<your-database-username>
   dbPassword=<your-database-password>
   keySession=<your-secret-session-key>
   ```

   Replace `<your-database-username>`, `<your-database-password>`, and `<your-secret-session-key>` with your actual values.

5. Set database infomation in `site/db.py`
    ```python
     __init__(self, host="<your-host>", user="", password="", database="<your-database>"):
    ```

    Replace `<your-host>` and `<your-database>` with your actual values.

6. Start the development server:
   ```bash
   python3 app.py
   ```

   The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Database Structure

### Tables

1. **User**:
   - `id` (Primary Key, Integer, Auto_Increment)
   - `name` (String, required, unique)
   - `role` (Foreign Key, references `Role.id`)

2. **Role**:
   - `id` (Primary Key, Integer, Auto_Increment)
   - `role_name` (String, unique, required)

3. **Admin**:
   - `id` (Primary Key, Integer)
   - `username` (String, unique, required)
   - `password` (String 512, required)
   - `session_id` (String 512, required)
   - `session_expire` (datetime, required)

---

## Configuration

### Environment Variables
Ensure the following environment variables are set in your `.env` file:
- `dbUser`: Database username
- `dbPassword`: Database password
- `keySession`: A secure key for Flask sessions

---

## Author

**Giacomo Marconi**  
Email: [your-email@example.com]

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.