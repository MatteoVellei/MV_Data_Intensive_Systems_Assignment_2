# Solar Grid Multi-Database Management System

This project is a multi-database management web application developed for Assignment 2 of the Data-Intensive Systems course. It models an IoT solar grid monitoring platform using three separate SQLite databases that can be inspected, edited, and managed through a Streamlit interface.

## Overview

The repository includes:

- `Create_DBs.py` — creates and populates the SQLite databases with realistic sample data
- `WEB_Application_.py` — Streamlit dashboard for interacting with the databases
- `requirements.txt` — Python dependencies
- three generated SQLite databases:
  - `solar_installations.db`
  - `solar_telemetry.db`
  - `grid_exchanges.db`

## Database Architecture

1. `solar_installations.db` — Master solar installations database
   - Table: `installations`
   - Fields: `id`, `owner_name`, `address`, `system_capacity_kw`, `installation_date`
   - Sample data: 10 installation records

2. `solar_telemetry.db` — Telemetry database for inverter production logs
   - Table: `telemetry_logs`
   - Fields: `id`, `installation_id`, `timestamp`, `power_output_kw`, `efficiency_pct`, `weather`
   - Sample data: 50 telemetry entries

3. `grid_exchanges.db` — Grid interaction and battery status database
   - Table: `grid_trades`
   - Fields: `id`, `installation_id`, `trade_date`, `energy_exported_kwh`, `energy_imported_kwh`, `battery_level_pct`, `grid_credit_eur`
   - Sample data: 20 trade records

## Features

The Streamlit app provides:

- Database selection from the sidebar;
- Reading/viewing table contents in a Pandas data editor;
- Inline editing and saving changes back to SQLite;
- Inserting new records using;
- Deleting existing records;
- Validating inputs before inserting data.

## How to Run the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Initialize the SQLite databases

```
python Create_DBs.py
```

This script creates the three database files and fills them with sample data if they are empty.

### 3. Launch the Streamlit app

```
streamlit run WEB_Application_.py
```

Once the app starts, use the sidebar to select which database table to view or modify.

## Notes

- The application is focused on CRUD-style management for a small distributed energy monitoring scenario.
- The generated SQLite databases are local files in the project folder.
