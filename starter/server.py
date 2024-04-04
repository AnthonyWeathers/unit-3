from flask import Flask, render_template, redirect, flash, request, session, url_for
import jinja2
import melons
from forms import LoginForm, NumOfMelonsForm
import customers

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined # for debugging purposes

### Flask Routes go here. ###
cart = []

@app.route("/")
def homepage():
    return render_template("base.html")

@app.route("/melons")
def all_melons():
    """Should get list of all melon objects"""
    # return render_template("melons.html", melons=all_melons())
    return render_template("melons.html", melons=melons.all_melons())

@app.route("/melon/<melon_id>", methods=["GET", "POST"])
def melon(melon_id):
    """Should get melon object by id and send it to page to access its details"""
    # return render_template("melon.html",melon=get_by_id(melon_id))

    form = NumOfMelonsForm(request.form)

    if form.validate_on_submit():
        number = form.number.data

        return redirect(url_for('add_many_to_cart', melon_id=melon_id, number=number))
    
    return render_template("melon.html", melon=melons.get_by_id(melon_id), form=form)

@app.route("/add_to_cart<melon_id>")
def add_to_cart(melon_id):
    """ Add melon via its melon_id to cart if user is logged in"""

    if 'username' not in session:
        return redirect("/login")

    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']

    cart[melon_id] = cart.get(melon_id, 0) + 1

    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(session['cart'])
    return redirect("/cart")

@app.route("/add_many_to_cart<melon_id><number>")
def add_many_to_cart(melon_id,number):
    """ Add melon via its melon_id to cart if user is logged in"""

    if 'username' not in session:
        return redirect("/login")

    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']

    cart[melon_id] = cart.get(melon_id, 0) + int(number)

    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(session['cart'])
    return redirect("/cart")

@app.route("/cart")
def cart():
    """ Shows contents of cart if a user is logged in"""

    if 'username' not in session:
        return redirect("/login")

    order_total = 0
    cart_melons = []

    # Get cart dict from session (or an empty one if none exists yet)
    cart = session.get("cart", {})
    for melon_id, qty in cart.items():
        melon = melons.get_by_id(melon_id)

        # Calculate cost of watermelon type and quantity
        cost_total = qty * melon.price
        order_total += cost_total

        # add quantity and total cost to the melon object
        melon.qty = qty
        melon.total_cost = cost_total

        cart_melons.append(melon)

    return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)

@app.route("/empty-cart")
def empty_cart():
    session['cart'] = {}
    return redirect("/cart")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user into site."""
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check to see if a registered user exists with this username
        user = customers.get_by_username(username)

        if not user or user['password'] != password:
                flash("Invalid username or password")
                return redirect('/login')

        # Store username in session to keep track of logged in user
        session["username"] = user['username']
        flash("Logged in.")
        return redirect("/melons")

    # Form has not been submitted or data was not valid
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Log user out."""

    del session["username"]
    flash("Logged out.")
    return redirect("/login")

@app.errorhandler(404)
def error_404(e):
   return render_template("404.html")

if __name__ == "__main__":
   app.env = "development"
   app.run(debug = True, port = 8000, host = "localhost")