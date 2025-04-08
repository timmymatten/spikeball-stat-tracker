# Spikeball Stat Tracker

A Streamlit application for tracking Spikeball game statistics.

## Features

- Track game statistics for multiple players
- Record serves, sets, and hits
- View player statistics and game history
- Persistent data storage with PostgreSQL

## Setup

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spikeball-stat-tracker.git
cd spikeball-stat-tracker
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
   - Install PostgreSQL if you haven't already
   - Create a database for the application
   - Update the `.env` file with your database credentials

5. Initialize the database:
```bash
python init_db.py
```

### Running the Application

```bash
streamlit run Home.py
```

## Database Configuration

The application uses PostgreSQL for data storage. Configure your database connection in the `.env` file:

```
DB_NAME=spikeball_stats
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Replace the values with your actual database credentials.

## Usage

1. Add a new game by navigating to the "Add Game" page
2. Enter player names and track their statistics
3. View game history on the "Games" page
4. Analyze player statistics on the "Player Stats" page

## License

This project is licensed under the MIT License - see the LICENSE file for details.
