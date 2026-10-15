import sqlite3

# Central place to configure DB filenames
DB_INSTALLATIONS = "solar_installations.db"
DB_TELEMETRY = "solar_telemetry.db"
DB_GRID = "grid_exchanges.db"


def init_installations_db():
    """
    Creates and populates the Solar Installations database
    """
    db_file = DB_INSTALLATIONS
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS installations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT NOT NULL,
            address TEXT NOT NULL,
            system_capacity_kw REAL NOT NULL,
            installation_date TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM installations")
    if cursor.fetchone()[0] == 0:
        sample_installations = [
            ("Marco Rossi", "Via Roma 12, Milano", 6.0, "2023-01-15"),
            ("Laura Bianchi", "Corso Italia 45, Torino", 4.5, "2023-03-22"),
            ("Giuseppe Verdi", "Via Dante 8, Bologna", 7.2, "2023-05-10"),
            ("Francesca Neri", "Via Garibaldi 100, Firenze", 5.0, "2023-06-18"),
            ("Alessandro Moretti", "Via Napoli 3, Roma", 8.0, "2023-08-05"),
            ("Sofia Russo", "Corso Vittorio 88, Napoli", 3.5, "2023-09-12"),
            ("Matteo Ferrari", "Via Mazzini 14, Verona", 6.5, "2023-11-01"),
            ("Elena Esposito", "Via dei Mille 27, Genova", 4.0, "2024-01-20"),
            ("Davide Romano", "Corso Francia 52, Padova", 9.0, "2024-02-14"),
            ("Chiara Colombo", "Via Milano 5, Brescia", 5.5, "2024-04-10")
        ]
        cursor.executemany("""
            INSERT INTO installations (owner_name, address, system_capacity_kw, installation_date)
            VALUES (?, ?, ?, ?)
        """, sample_installations)

    conn.commit()
    conn.close()
    print(f"Database '{db_file}' initialized with 10 records.")


def init_telemetry_db():
    """
    Creates and populates the Solar Telemetry database
    """
    db_file = DB_TELEMETRY
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            installation_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            power_output_kw REAL NOT NULL,
            efficiency_pct REAL NOT NULL,
            weather TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM telemetry_logs")
    if cursor.fetchone()[0] == 0:
        sample_telemetry = [
            # Installation 1 (6.0 kW capacity)
            (1, "2026-10-14 08:00:00", 2.1, 35.0, "Cloudy"),
            (1, "2026-10-14 10:00:00", 4.8, 80.0, "Sunny"),
            (1, "2026-10-14 12:00:00", 5.7, 95.0, "Sunny"),
            (1, "2026-10-14 14:00:00", 5.2, 86.7, "Sunny"),
            (1, "2026-10-14 16:00:00", 1.1, 18.3, "Rainy"),

            # Installation 2 (4.5 kW capacity)
            (2, "2026-10-14 08:00:00", 1.2, 26.7, "Cloudy"),
            (2, "2026-10-14 10:00:00", 3.8, 84.4, "Sunny"),
            (2, "2026-10-14 12:00:00", 4.3, 95.6, "Sunny"),
            (2, "2026-10-14 14:00:00", 2.1, 46.7, "Cloudy"),
            (2, "2026-10-14 16:00:00", 0.6, 13.3, "Rainy"),

            # Installation 3 (7.2 kW capacity)
            (3, "2026-10-14 08:00:00", 0.9, 12.5, "Rainy"),
            (3, "2026-10-14 10:00:00", 3.2, 44.4, "Cloudy"),
            (3, "2026-10-14 12:00:00", 6.8, 94.4, "Sunny"),
            (3, "2026-10-14 14:00:00", 6.5, 90.3, "Sunny"),
            (3, "2026-10-14 16:00:00", 2.8, 38.9, "Cloudy"),

            # Installation 4 (5.0 kW capacity)
            (4, "2026-10-14 08:00:00", 1.8, 36.0, "Cloudy"),
            (4, "2026-10-14 10:00:00", 4.2, 84.0, "Sunny"),
            (4, "2026-10-14 12:00:00", 4.8, 96.0, "Sunny"),
            (4, "2026-10-14 14:00:00", 0.8, 16.0, "Rainy"),
            (4, "2026-10-14 16:00:00", 0.5, 10.0, "Rainy"),

            # Installation 5 (8.0 kW capacity)
            (5, "2026-10-14 08:00:00", 3.1, 38.8, "Cloudy"),
            (5, "2026-10-14 10:00:00", 7.1, 88.8, "Sunny"),
            (5, "2026-10-14 12:00:00", 7.8, 97.5, "Sunny"),
            (5, "2026-10-14 14:00:00", 7.3, 91.3, "Sunny"),
            (5, "2026-10-14 16:00:00", 1.5, 18.8, "Rainy"),

            # Installation 6 (3.5 kW capacity)
            (6, "2026-10-14 08:00:00", 0.4, 11.4, "Rainy"),
            (6, "2026-10-14 10:00:00", 1.6, 45.7, "Cloudy"),
            (6, "2026-10-14 12:00:00", 3.3, 94.3, "Sunny"),
            (6, "2026-10-14 14:00:00", 3.1, 88.6, "Sunny"),
            (6, "2026-10-14 16:00:00", 1.2, 34.3, "Cloudy"),

            # Installation 7 (6.5 kW capacity)
            (7, "2026-10-14 08:00:00", 2.4, 36.9, "Cloudy"),
            (7, "2026-10-14 10:00:00", 5.6, 86.2, "Sunny"),
            (7, "2026-10-14 12:00:00", 6.2, 95.4, "Sunny"),
            (7, "2026-10-14 14:00:00", 2.8, 43.1, "Cloudy"),
            (7, "2026-10-14 16:00:00", 1.0, 15.4, "Rainy"),

            # Installation 8 (4.0 kW capacity)
            (8, "2026-10-14 08:00:00", 1.4, 35.0, "Cloudy"),
            (8, "2026-10-14 10:00:00", 3.5, 87.5, "Sunny"),
            (8, "2026-10-14 12:00:00", 3.8, 95.0, "Sunny"),
            (8, "2026-10-14 14:00:00", 0.7, 17.5, "Rainy"),
            (8, "2026-10-14 16:00:00", 0.4, 10.0, "Rainy"),

            # Installation 9 (9.0 kW capacity)
            (9, "2026-10-14 08:00:00", 3.5, 38.9, "Cloudy"),
            (9, "2026-10-14 10:00:00", 8.1, 90.0, "Sunny"),
            (9, "2026-10-14 12:00:00", 8.7, 96.7, "Sunny"),
            (9, "2026-10-14 14:00:00", 8.2, 91.1, "Sunny"),
            (9, "2026-10-14 16:00:00", 1.8, 20.0, "Rainy"),

            # Installation 10 (5.5 kW capacity)
            (10, "2026-10-14 08:00:00", 0.7, 12.7, "Rainy"),
            (10, "2026-10-14 10:00:00", 2.4, 43.6, "Cloudy"),
            (10, "2026-10-14 12:00:00", 5.2, 94.5, "Sunny"),
            (10, "2026-10-14 14:00:00", 4.9, 89.1, "Sunny"),
            (10, "2026-10-14 16:00:00", 1.9, 34.5, "Cloudy")
        ]
        cursor.executemany("""
            INSERT INTO telemetry_logs (installation_id, timestamp, power_output_kw, efficiency_pct, weather)
            VALUES (?, ?, ?, ?, ?)
        """, sample_telemetry)

    conn.commit()
    conn.close()
    print(f"Database '{db_file}' initialized")


def init_grid_db():
    """
    Creates and populates the Grid Exchanges database
    """
    db_file = DB_GRID
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grid_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            installation_id INTEGER NOT NULL,
            trade_date TEXT NOT NULL,
            energy_exported_kwh REAL NOT NULL,
            energy_imported_kwh REAL NOT NULL,
            battery_level_pct REAL NOT NULL,
            grid_credit_eur REAL NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM grid_trades")
    if cursor.fetchone()[0] == 0:
        sample_trades = [
            (1, "2026-10-12", 18.5, 2.3, 85.0, 2.78),
            (1, "2026-10-13", 22.0, 1.5, 92.0, 3.30),
            (2, "2026-10-12", 12.4, 4.1, 70.0, 1.86),
            (2, "2026-10-13", 14.8, 3.0, 78.0, 2.22),
            (3, "2026-10-12", 25.1, 0.8, 95.0, 3.77),
            (3, "2026-10-13", 28.4, 0.5, 98.0, 4.26),
            (4, "2026-10-12", 15.0, 3.5, 75.0, 2.25),
            (4, "2026-10-13", 11.2, 5.2, 62.0, 1.68),
            (5, "2026-10-12", 31.0, 0.0, 100.0, 4.65),
            (5, "2026-10-13", 29.5, 0.2, 96.0, 4.43),
            (6, "2026-10-12", 8.2, 6.1, 55.0, 1.23),
            (6, "2026-10-13", 10.5, 4.8, 65.0, 1.58),
            (7, "2026-10-12", 21.3, 2.0, 88.0, 3.20),
            (7, "2026-10-13", 19.8, 2.5, 82.0, 2.97),
            (8, "2026-10-12", 11.0, 4.5, 68.0, 1.65),
            (8, "2026-10-13", 9.5, 5.8, 58.0, 1.43),
            (9, "2026-10-12", 35.2, 0.0, 100.0, 5.28),
            (9, "2026-10-13", 33.8, 0.1, 99.0, 5.07),
            (10, "2026-10-12", 16.4, 3.2, 79.0, 2.46),
            (10, "2026-10-13", 17.9, 2.8, 83.0, 2.69)
        ]
        cursor.executemany("""
            INSERT INTO grid_trades (installation_id, trade_date, energy_exported_kwh, energy_imported_kwh, battery_level_pct, grid_credit_eur)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_trades)

    conn.commit()
    conn.close()
    print(f"Database '{db_file}' initialized")


if __name__ == "__main__":
    print("Initializing Smart Solar Grid SQLite databases...")
    init_installations_db()
    init_telemetry_db()
    init_grid_db()
    print("All 3 databases are initialized and ready")
