from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB (create table if not exists)
def init_db():
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_date TEXT NOT NULL,
            booking_time TEXT CHECK(booking_time IN ('Morning','Evening')),
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # check if delete action
        if "delete_id" in request.form:
            delete_id = request.form["delete_id"]
            conn = sqlite3.connect("bookings.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id = ?", (delete_id,))
            conn.commit()
            conn.close()
        else:
            # Insert new booking
            booking_date = request.form["booking_date"]
            booking_time = request.form["booking_time"]
            name = request.form["name"]

            conn = sqlite3.connect("bookings.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bookings (booking_date, booking_time, name) VALUES (?, ?, ?)",
                (booking_date, booking_time, name),
            )
            conn.commit()
            conn.close()

        return redirect(url_for("home"))

    # Fetch all bookings (include ID for delete)
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, booking_date, booking_time, name FROM bookings ORDER BY booking_date"
    )
    rows = cursor.fetchall()
    conn.close()

    return render_template("form.html", bookings=rows)


if __name__ == "__main__":
    app.run(debug=True)
