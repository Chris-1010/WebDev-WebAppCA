from flask import Flask, render_template, redirect, session, url_for, request, g
from forms import browse_form, login_form, register_form, edit_user_details, checkout_form, entry_form
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os, random

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config['SECRET_KEY'] = 'key'
app.config['SESSION_PERMANENT'] = 'False'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.before_request
def logged_in():
    if request.url != 'login' and request.url != 'register':
        session['previous_page'] = request.url
    g.user = session.get("username", None)  # checks if user is logged in. .get method works as follows: tries to get "user_id" first, if it can't, it returns None
    g.name = session.get("name", None)  # finds the name of the user if logged in
    g.admin = session.get("admin", "false")
    g.random = random.randint(1,8)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.admin == "false":
            return redirect(url_for("account", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/", methods=["GET", "POST"])
def browse():
    form = browse_form()

    db = get_db()
    choices = db.execute("""SELECT type, brand, market_value FROM vehicles;""").fetchall()

    types=["Type"]
    brands=['Brand']
    market_values=['Price Range', '15k-20k', '20k-25k', '25k-30k', '>30k']
    sort_by_choices = ["Price", "Year", "Alphabetical"]

    for dictionary in choices:
        if dictionary['type'] not in types:
            types.append(dictionary['type'])
        if dictionary['brand'] not in brands:
            brands.append(dictionary['brand'])
    form.type.choices = types
    form.brand.choices = brands
    form.price_range.choices = market_values
    form.sort_by.choices = sort_by_choices
    
    if form.validate_on_submit():
        query_parts = []

        if form.type.data != "Type":
            query_parts.append(f"type = '{form.type.data}'")

        if form.brand.data != "Brand":
            query_parts.append(f"brand = '{form.brand.data}'")

        if form.price_range.data != "Price Range":  # MARKET VALUE BETWEEN ...
            if form.price_range.data == '15k-20k':
                start_range = 15000
                end_range = 20000
            elif form.price_range.data == '20k-25k':
                start_range = 20000
                end_range = 25000
            elif form.price_range.data == '25k-30k':
                start_range = 25000
                end_range = 30000
            elif form.price_range.data == '>30k':
                start_range = 30000
                end_range = 500000
            
            query_parts.append(f"market_value BETWEEN {str(start_range)} AND {str(end_range)}")

        sort_by = form.sort_by.data
        if sort_by == "Price":
            sort_by = "market_value"
        elif sort_by == "Alphabetical":
            sort_by = "model"
        elif sort_by == "Year":
            sort_by = "production_year"


        if query_parts:
            query = f"SELECT * FROM vehicles WHERE {' AND '.join(query_parts)} ORDER BY {sort_by};"
        else:
            query = f"SELECT * FROM vehicles ORDER BY {sort_by};"

        db = get_db()
        model_choices = db.execute(query).fetchall()

        entries = []
        for dictionary in model_choices:  # <sqlite3.Row object at 0x0000019F0FFF1510>...
            details = {"id":dictionary["id"],
                       "brand":dictionary["brand"],
                       "model":dictionary["model"],
                       "engine_size":dictionary["engine_size"],
                       "production_year":dictionary["production_year"],
                       "market_value":dictionary["market_value"]}
            entries.append(details)
        return render_template("browse.html", form=form, entries=entries)
    
        
    return render_template("browse.html", form=form)


@app.route("/details/<int:id>", methods=["GET", "POST"])
def vehicle_details(id):

    db = get_db()
    details = db.execute("SELECT * FROM vehicles WHERE id=?;", (id,)).fetchone()
    
    watchlist_details = {'watchlist':""}
    if 'username' in session:
        watchlist_details = db.execute("SELECT watchlist FROM credentials WHERE username = ?", (session['username'],)).fetchone()
    
    if 'recently_viewed' not in session:
        session["recently_viewed"] = {f"{id} details":{"id":details["id"], "brand":details["brand"], "model":details["model"], "url":request.url}}

    else:
        session['recently_viewed'][f"{id} details"] = {"id":details["id"], "brand":details["brand"], "model":details["model"], "url":request.url}

        if len(session['recently_viewed']) > 3:

            # My Method
            keys = session['recently_viewed'].keys()
            first_key = ""
            while first_key == "":
                for key in keys:
                    first_key = key
                    break

            
            session['recently_viewed'].pop(first_key)  # Pop it
        
    return render_template("details.html", details=details, watchlist_details=watchlist_details)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = register_form()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data
        # re_password = form.re_password.data
        admin_code = form.admin_code.data
        if admin_code == "3q5h9":
            admin = "true"
        else:
            admin = "false"
        db = get_db()
        check_existing_user = db.execute("SELECT * FROM credentials WHERE username = ?;", (username,)).fetchone()
        if check_existing_user is not None:
            form.username.errors.append("Username already taken")
        else:
            db.execute("INSERT INTO credentials (name, username, password, admin) VALUES (?, ?, ?, ?);", (name, username, generate_password_hash(password), admin))
            db.commit()  # Save the database
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = login_form()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db = get_db()
        corresponding_user = db.execute("SELECT * FROM credentials WHERE username = ?;", (username,)).fetchone()

        if corresponding_user is None:  # User not found
            form.username.errors.append("User not found")

        elif not check_password_hash(corresponding_user['password'], password):  # Incorrect Password
            form.password.errors.append("Incorrect Password")

        else:  # login successful
            session["username"] = username  # a way of knowing that the user is logged in
            session["name"] = corresponding_user["name"]
            session['admin'] = corresponding_user['admin']

            # retrieve watchlist from database and put it in session
            if corresponding_user["watchlist"]:
                session['watchlist'] = {}
                watchlist_ids = corresponding_user['watchlist'].split('-')
                for id in watchlist_ids:
                    details = db.execute("SELECT * FROM vehicles WHERE id=?;", (id,)).fetchone()
                    session["watchlist"][f"{id} details"] = {"id":details["id"], "type":details["type"], "brand":details["brand"], "model":details["model"], "engine_size":details["engine_size"], "production_year":details["production_year"], "market_value":details["market_value"]}

            
            next_page = request.args.get("next")
            if not next_page:
                try:
                    next_page = url_for(session['previous_page'])
                except:
                    next_page = url_for("browse")
            return redirect(next_page)  # returns you to the page you were on before logging in
    return render_template("login.html", form=form)
    
@app.route("/logout")
@login_required
def logout():
    
    if "watchlist" in session:
        # Attempt to save watchlist for login next time
        stored_watchlist_ids = ""  # what will be stored in the database: a string of ids, concatenated together. For example, 123 will have the vehicles with the ids 1, 2, and 3 in the watchlist
        
        for key in session["watchlist"]:  # "1 details", "2 details", "3 details"
            partition = key.split(" ")
            stored_watchlist_ids += partition[0] + '-'
        stored_watchlist_ids = stored_watchlist_ids[:-1]
        db = get_db()
        db.execute("UPDATE credentials SET watchlist = ? WHERE username = ?;", (stored_watchlist_ids, session["username"]))
        db.commit()
        session.pop("watchlist")
    session.pop("username")
    session.pop("name")
    session.pop("admin")
    next_page = request.args.get("next")
    if not next_page:
        try:
            next_page = url_for(session['previous_page'])
        except:
            next_page = url_for("browse")
    return redirect(next_page)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = edit_user_details()
    db = get_db()
    user = db.execute("SELECT * from credentials WHERE username = ?;", (session['username'],)).fetchone()
    order_information = db.execute("""SELECT orders.order_id, vehicles.id, vehicles.brand, vehicles.model, orders.date
                                    FROM vehicles
                                    JOIN orders
                                    ON vehicles.id = orders.vehicle_id
                                    WHERE orders.username = ?;""", (session['username'],)).fetchall()

    if form.validate_on_submit():
        current_password = form.current_password.data
        if check_password_hash(user['password'], current_password):
            updated_name = form.updated_name.data
            updated_username = form.updated_username.data
            updated_password = form.updated_password.data

            if updated_name is None or updated_name == "":
                updated_name = user['name']

            if updated_password is None or updated_password == "":
                updated_password = user['password']
            else:
                updated_password = generate_password_hash(updated_password)

            if updated_username is None:
                updated_username = user['username']
            else:
                check_existing_user = db.execute("SELECT * FROM credentials WHERE username = ?;", (updated_username,)).fetchone()
                if check_existing_user is not None:
                    form.updated_username.errors.append("Username already taken")
                    updated_username = user['username']
            
            db.execute("UPDATE credentials SET name = ?, username = ?, password = ? WHERE username = ?;", (updated_name, updated_username, updated_password, user['username']))
            # Update orders table also
            db.execute("UPDATE orders SET username = ? WHERE username = ?;", (updated_username, user['username']))
            db.commit()

            user = db.execute("SELECT * from credentials WHERE username = ?;", (updated_username,)).fetchone()
            order_information = db.execute("""SELECT orders.order_id, vehicles.id, vehicles.brand, vehicles.model, orders.date
                                FROM vehicles
                                JOIN orders
                                ON vehicles.id = orders.vehicle_id
                                WHERE orders.username = ?;""", (updated_username,)).fetchall()
            session['name'] = updated_name
            session['username'] = updated_username
        else:
            form.current_password.errors.append("Incorrect Password")
            
    name = user['name']
    username = user['username']
    admin = user['admin']
    return render_template("account.html", form=form, order_information=order_information, name=name, username=username, admin=admin)




@app.route("/watchlist")
@login_required
def watchlist():
    return render_template("watchlist.html")

@app.route("/add_to_watchlist/<int:id>")
@login_required
def add_to_watchlist(id):

    db = get_db()
    details = db.execute("SELECT * FROM vehicles WHERE id=?;", (id,)).fetchone()

    if "watchlist" not in session:
        session["watchlist"] = {f"{id} details":{"id":details["id"], "type":details["type"], "brand":details["brand"], "model":details["model"], "engine_size":details["engine_size"], "production_year":details["production_year"], "market_value":details["market_value"]}}
    else:
        session["watchlist"][f"{id} details"] = {"id":details["id"], "type":details["type"], "brand":details["brand"], "model":details["model"], "engine_size":details["engine_size"], "production_year":details["production_year"], "market_value":details["market_value"]}

    save_watchlist()

    return redirect(url_for("vehicle_details", id=id))

@app.route("/remove_from_watchlist/<int:id>")
@login_required
def remove_from_watchlist(id):

    session["watchlist"].pop(f"{id} details")

    save_watchlist()

    return redirect(url_for("watchlist"))

def save_watchlist():
    stored_watchlist_ids = ""  # what will be stored in the database: a string of ids, concatenated together. For example, 123 will have the vehicles with the ids 1, 2, and 3 in the watchlist
        
    for key in session["watchlist"]:  # "1 details", "2 details", "3 details"
        partition = key.split(" ")
        stored_watchlist_ids += partition[0] + '-'
    stored_watchlist_ids = stored_watchlist_ids[:-1]
    db = get_db()
    db.execute("UPDATE credentials SET watchlist = ? WHERE username = ?;", (stored_watchlist_ids, session["username"]))
    db.commit()
    return render_template("watchlist.html")


@app.route("/checkout/<int:id>", methods=["GET", "POST"])
@login_required
def checkout(id):
    form = checkout_form()
    ordered = False
    db = get_db()
    vehicle = db.execute("SELECT * FROM vehicles WHERE id=?;", (id,)).fetchone()
    if form.validate_on_submit():
        db.execute("INSERT INTO orders (username, vehicle_id, date) VALUES (?, ?, ?);", (session["username"], id, datetime.now().strftime("%d/%m/%Y")))
        db.commit()
        ordered = True

    return render_template("checkout.html", form=form, vehicle=vehicle, ordered=ordered)


@app.route("/admin/view_orders", methods=["GET", "POST"])
@admin_required
def view_orders():
    db = get_db()
    order_information = db.execute("""SELECT orders.order_id, vehicles.id, vehicles.brand, vehicles.model, orders.date
                                    FROM vehicles
                                    JOIN orders
                                    ON vehicles.id = orders.vehicle_id;""").fetchall()

    return render_template("orders.html", order_information=order_information)


@app.route("/admin/<mode>_entries", methods=["GET", "POST"])
@admin_required
def edit_entries(mode):
    form = entry_form()
    db = get_db()


    if request.method == "POST":
        if request.form.get("add_entry"):
            type = form.type.data
            brand = form.brand.data
            model = form.brand.data
            engine_size = form.brand.data
            engine_size += "L"
            production_year = form.production_year.data
            market_value = form.market_value.data

            image = form.image.data
            image.filename = model
            image.save(os.path.join(app.root_path, 'static', image.filename))

            db.execute("INSERT INTO vehicles (type, brand, model, engine_size, production_year, market_value) VALUES (?, ?, ?, ?, ?, ?);", (type, brand, model, engine_size, production_year, market_value))

        elif request.form.get("edit_entry"):
            id = request.form.get('vehicle_id')  # Gets the id of the submit button that was clicked (example: edit_vehicle1, edit_vehicle2, ...). The [-1] gets the last character in the string: the id number
            original_details = db.execute("SELECT * FROM vehicles WHERE id = ?;", (id,)).fetchone()

            updated_type = form.type_name.data
            if updated_type is None or updated_type == "":
                updated_type = original_details['type']

            updated_brand = form.brand_name.data
            if updated_brand is None or updated_brand == "" :
                updated_brand = original_details['brand']

            updated_model = form.model.data
            if updated_model is None or updated_model == "":
                updated_model = original_details['model']
            else:  # change the name of the image associated with the model name
                os.rename(os.path.join(app.root_path, 'static', original_details['model']), os.path.join(app.root_path, 'static', updated_model))


            updated_engine_size = form.engine_size.data
            if updated_engine_size is None or updated_engine_size == "":
                updated_engine_size = original_details['engine_size']
            else:
                updated_engine_size = str(updated_engine_size)
                updated_engine_size += "L"

            updated_production_year = form.production_year.data
            if updated_production_year is None or updated_production_year == "":
                updated_production_year = original_details['production_year']
            
            updated_market_value = form.market_value.data
            if updated_market_value is None or updated_market_value == "":
                updated_market_value = original_details['market_value']

            db.execute("UPDATE vehicles SET type = ?, brand = ?, model = ?, engine_size = ?, production_year = ?, market_value = ? WHERE id = ?;", (updated_type, updated_brand, updated_model, updated_engine_size, updated_production_year, updated_market_value, id))
            db.commit()
    entries = db.execute("SELECT * FROM vehicles ORDER BY id DESC;").fetchall()

    return render_template("entries.html", form=form, mode=mode, entries=entries)