import sqlite3
import os


def main():
    # drop database if exists
    os.remove("business_app.db")

    # Connect to SQLite
    conn = sqlite3.connect("business_app.db")
    cur = conn.cursor()

    # Create user table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first TEXT NOT NULL,
            last TEXT NOT NULL,
            phone INTEGER NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    users = [
        ("admin", "admin", 7270000000, "admin", "admin"),
        ("John", "Smith", 7270000001, "john.smith@tesabiz.com", "john1"),
        ("Jane", "Doe", 7270000002, "jane.doe@tesabiz.com", "joe1")
    ]

    cur.executemany(
        "INSERT INTO user (first, last, phone, email, password) VALUES (?, ?, ?, ?, ?)",
        users
    )


    # Create business table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS business (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            category INTEGER NOT NULL,
            phone TEXT NOT NULL,
            website TEXT NOT NULL,
            deal TEXT
        )
    """)

    businesses = [
        ("Mike's Pizza", "123 Pizza Blvd. Trinity FL 34655", "Restaurant", "7271000001", "mikspizza.tesabiz.com", "10% off your first order!"),
        ("Jose's Tacos", "123 Taco Blvd. Trinity FL 34655", "Restaurant", "7271000002", "josestacos.tesabiz.com", "Free drink with purchase of 3 tacos!"),
        ("Sally's Salon", "456 Beauty St. Trinity FL 34655", "Salon", "7272000001", "sallyssalon.tesabiz.com", ""),
        ("Pete's Plumbing", "789 Fixit Ave. Trinity FL 34655", "Home Services", "7273000001", "petesplumbing.tesabiz.com", "Free estimates on all jobs!")
    ]

    cur.executemany(
        "INSERT INTO business (name, address, category, phone, website, deal) VALUES (?, ?, ?, ?, ?, ?)",
        businesses
    )


    # Create user_favorite table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_favorite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            business_id INTEGER NOT NULL,
            UNIQUE(user_id, business_id)
        )
    """)

    # Create business_rating table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS business_rating (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            user_id INTEGER NOT NULL,                
            UNIQUE(user_id, business_id)
        )
    """)






    # Save and close
    conn.commit()
    conn.close()

    print("Database created and sample data inserted!")

if __name__ == "__main__":
    main()