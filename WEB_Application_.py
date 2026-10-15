import sqlite3
import pandas as pd
import streamlit as st

# Configure the Streamlit page layout and title
st.set_page_config(page_title="Solar Grid Manager", layout="wide")

st.title("Data-Intensive Systems - Assignment 2")

# Map sidebar names to SQLite database files, table names, and column schemas
DB_CONFIG = {
    "Solar Installations DB": {
        "file": "solar_installations.db",
        "table": "installations",
        "columns": ["owner_name", "address", "system_capacity_kw", "installation_date"]
    },
    "Solar Telemetry DB": {
        "file": "solar_telemetry.db",
        "table": "telemetry_logs",
        "columns": ["installation_id", "timestamp", "power_output_kw", "efficiency_pct", "weather"]
    },
    "Grid Exchanges DB": {
        "file": "grid_exchanges.db",
        "table": "grid_trades",
        "columns": ["installation_id", "trade_date", "energy_exported_kwh", "energy_imported_kwh", "battery_level_pct", "grid_credit_eur"]
    }
}

# Sidebar widget allowing the user to select which database to inspect or modify
st.sidebar.header("Database Selector")
selected_db_name = st.sidebar.selectbox("Choose a database:", list(DB_CONFIG.keys()))
db_info = DB_CONFIG[selected_db_name]

def get_connection(db_file):
    # Utility helper function to establish a connection to an SQLite database file
    return sqlite3.connect(db_file)

st.header(f"{selected_db_name}")

# --- SECTION 1: READ RECORDS & INLINE CELL EDITING ---
st.subheader("1. Table (View and Edit)")

df = pd.DataFrame()
try:
    # Connect to the active SQLite database file and load records into a Pandas DataFrame
    conn = get_connection(db_info["file"])
    df = pd.read_sql_query(f"SELECT * FROM {db_info['table']}", conn)
    conn.close()

    if df.empty:
        st.info("No records found in this database table")
    else:
        # Data editor component allowing direct cell modification
        edited_df = st.data_editor(
            df,
            disabled=["id"],  # Keep primary key 'id' column read-only to prevent corruption
            use_container_width=True,
            key=f"editor_{selected_db_name}"
        )

        # Button to commit modified table cells back to the SQLite database
        if st.button("Save Table Changes", type="primary"):
            try:
                conn = get_connection(db_info["file"])
                cursor = conn.cursor()

                # Iterate over edited rows and execute SQL UPDATE queries for modified records
                for index, row in edited_df.iterrows():
                    row_id = row["id"]
                    update_cols = [col for col in db_info["columns"] if col in row]
                    set_clause = ", ".join([f"{col} = ?" for col in update_cols])
                    values = [row[col] for col in update_cols] + [row_id]

                    query = f"UPDATE {db_info['table']} SET {set_clause} WHERE id = ?"
                    cursor.execute(query, values)

                conn.commit()
                conn.close()

                st.success("Changes saved successfully to the database!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to update database: {e}")

except Exception as e:
    st.error(
        f"Could not load data from '{db_info['file']}'. Make sure you ran 'init_db.py' first.\nDetails: {e}"
    )

# --- SECTION 2: ADD NEW RECORD ---
st.subheader("2. Add New Record")

with st.form(key="add_record_form"):
    inputs = {}

    # Input controls specific to the active database table schema
    if selected_db_name == "Solar Installations DB":
        inputs["owner_name"] = st.text_input("Owner Name (e.g. Marco Rossi)")
        inputs["address"] = st.text_input("Address (e.g. Via Roma 12, Milano)")
        inputs["system_capacity_kw"] = st.number_input("System Capacity (kW)", min_value=0.5, max_value=100.0, step=0.5, value=6.0)
        inputs["installation_date"] = st.text_input("Installation Date (YYYY-MM-DD)", value="2026-10-14")

    elif selected_db_name == "Solar Telemetry DB":
        inputs["installation_id"] = st.number_input("Installation ID", min_value=1, step=1, value=1)
        inputs["timestamp"] = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value="2026-10-14 14:00:00")
        inputs["power_output_kw"] = st.number_input("Power Output (kW)", min_value=0.0, step=0.1, value=4.5)
        inputs["efficiency_pct"] = st.number_input("Efficiency (%)", min_value=0.0, max_value=100.0, step=0.5, value=92.5)
        inputs["weather"] = st.selectbox("Weather Condition", ["Sunny", "Partly Cloudy", "Cloudy", "Rainy"])

    elif selected_db_name == "Grid Exchanges DB":
        inputs["installation_id"] = st.number_input("Installation ID", min_value=1, step=1, value=1)
        inputs["trade_date"] = st.text_input("Trade Date (YYYY-MM-DD)", value="2026-10-14")
        inputs["energy_exported_kwh"] = st.number_input("Energy Exported (kWh)", min_value=0.0, step=0.5, value=15.0)
        inputs["energy_imported_kwh"] = st.number_input("Energy Imported (kWh)", min_value=0.0, step=0.5, value=2.0)
        inputs["battery_level_pct"] = st.number_input("Battery Level (%)", min_value=0.0, max_value=100.0, step=1.0, value=85.0)
        inputs["grid_credit_eur"] = st.number_input("Grid Credit (€)", min_value=0.0, step=0.10, value=2.25)

    submit_button = st.form_submit_button(label="Insert Record")

if submit_button:
    # Input validation for empty required text fields
    validation_errors = []
    for key, value in inputs.items():
        if isinstance(value, str) and not value.strip():
            validation_errors.append(f"Field '{key.replace('_', ' ').title()}' cannot be empty")

    if validation_errors:
        for err in validation_errors:
            st.warning(err)
    else:
        try:
            # Construct and execute dynamic SQL INSERT statement
            conn = get_connection(db_info["file"])
            cursor = conn.cursor()

            cols = ", ".join(inputs.keys())
            placeholders = ", ".join(["?"] * len(inputs))
            values = tuple(inputs.values())

            query = f"INSERT INTO {db_info['table']} ({cols}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()
            conn.close()

            st.success("New record added successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to insert record: {e}")

# --- SECTION 3: DELETE RECORD ---
st.subheader("3. Delete Record")

if not df.empty and "id" in df.columns:
    record_ids = df["id"].tolist()
    selected_id = st.selectbox("Select Record ID to delete:", record_ids)

    if st.button("Delete Record", type="primary"):
        try:
            # Execute SQL DELETE query for the selected record ID
            conn = get_connection(db_info["file"])
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {db_info['table']} WHERE id = ?", (selected_id,))
            conn.commit()
            conn.close()

            st.success(f"Record with ID {selected_id} deleted successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to delete record: {e}")
else:
    st.info("No records available to delete")
