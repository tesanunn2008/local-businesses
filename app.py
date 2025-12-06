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
def verify():
    if request.method == "POST":
        selected_color = request.form.get("traffic_light")
        expected_color = session.get("expected_color")
        
        if selected_color == expected_color:
            # Verification successful, redirect to login
            return redirect("/login")
        else:
            # Verification failed, try again
            return redirect("/")
    
    # Generate a random traffic light color for verification
    import random
    colors = ["red", "yellow", "green"]
    expected_color = random.choice(colors)
    session["expected_color"] = expected_color
    
    return render_template("verify.html", expected_color=expected_color)

@app.route("/login", methods=["GET", "POST"])
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
        SELECT b.id, b.name, b.address, b.category, b.website, b.phone,
               CASE WHEN uf.id IS NOT NULL THEN 1 ELSE 0 END as is_favorite,
               COALESCE(br.rating, 0) as user_rating, b.deal
        FROM business b
        LEFT JOIN user_favorite uf ON b.id = uf.business_id AND uf.user_id = ?
        LEFT JOIN business_rating br ON b.id = br.business_id AND br.user_id = ?
    """, (session["user_id"],session["user_id"],))


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

    # Check if rating already exists
    cur.execute("""
        SELECT id FROM business_rating
        WHERE business_id = ?
        AND user_id = ?
    """, (bus_id, session["user_id"]))
    
    existing_rating = cur.fetchone()
    
    if existing_rating:
        # Update existing rating
        cur.execute("""
            UPDATE business_rating
            SET rating = ?
            WHERE business_id = ?
            AND user_id = ?
        """, (rating, bus_id, session["user_id"]))
    else:
        # Insert new rating
        cur.execute("""
            INSERT INTO business_rating (business_id, rating)
            VALUES (?, ?)
            AND user_id = ?
        """, (bus_id, rating, session["user_id"]))

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

    # Check if favorite already exists
    cur.execute("""
        SELECT id FROM user_favorite
        WHERE user_id = ? AND business_id = ?
    """, (session["user_id"], bus_id))
    
    favorite = cur.fetchone()
    
    if favorite:
        # Remove favorite if it exists
        cur.execute("""
            DELETE FROM user_favorite
            WHERE user_id = ? AND business_id = ?
        """, (session["user_id"], bus_id))
    else:
        # Add favorite if it doesn't exist
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
