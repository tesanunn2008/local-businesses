from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Change this in real apps

def get_db():
    return sqlite3.connect("business_app.db", check_same_thread=False)


# ---------------------------
# LOGIN PAGE
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, first FROM user WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            session["first"] = user[1]
            return redirect("/businesses")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")


# ---------------------------
# BUSINESSES PAGE
# ---------------------------
@app.route("/businesses")
def businesses():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, address, category, website, phone
        FROM business
    """)

    rows = cur.fetchall()

    return render_template("businesses.html", name=session["first"], businesses=rows)



# ---------------------------
# RATE BUSINESS
# ---------------------------
@app.route("/rate/<int:bus_id>/<int:rating>")
def rate(bus_id, rating):
    if "user_id" not in session:
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_rating (user_id, business_id, rating)
        VALUES (?, ?, ?)
    """, (session["user_id"], bus_id, rating))

    conn.commit()
    return redirect("/businesses")


# ---------------------------
# FAVORITE BUSINESS
# ---------------------------
@app.route("/favorite/<int:bus_id>")
def favorite(bus_id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_favorite (user_id, business_id)
        VALUES (?, ?)
    """, (session["user_id"], bus_id))

    conn.commit()
    return redirect("/businesses")


# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)