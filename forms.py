from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, PasswordField, BooleanField, IntegerField, DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class browse_form(FlaskForm):
    type = SelectField("Type")
    brand = SelectField("Brand")
    price_range = SelectField("Price Range")
    sort_by = SelectField("Sort By")
    
    submit = SubmitField("Submit")


class login_form(FlaskForm):
    username = StringField("Username",
        validators = [InputRequired()])
    password = PasswordField("Password",
        validators = [InputRequired()])
    login_button = SubmitField("Login")


class register_form(FlaskForm):
    name = StringField("Name",
        validators = [InputRequired()])
    username = StringField("Username",
        validators = [InputRequired()])
    password = PasswordField("Password",
        validators = [InputRequired()])
    re_password = PasswordField("Re-enter Password",
        validators = [InputRequired()])
    admin = BooleanField("Admin?")
    admin_code = PasswordField("", render_kw={"placeholder": "Admin Code", "disabled": "True"})
    register_button = SubmitField("Register")

class edit_user_details(FlaskForm):
    updated_name = StringField("Name")
    updated_username = StringField("Username")
    updated_password = PasswordField("Password", render_kw={"placeholder": "Unchanged"})
    current_password = PasswordField("", render_kw={"placeholder": "Current Password", "disabled": "True"}, validators = [InputRequired()])
    save_changes = SubmitField("Save Changes", render_kw={"disabled":"True"})

class checkout_form(FlaskForm):
    place_order = SubmitField("Place Order")

class entry_form(FlaskForm):
    type_name = StringField("Type")
    brand_name = StringField("Brand")
    model = StringField("Model")
    engine_size = DecimalField("Engine Size (L)")
    production_year = IntegerField("Production Year", validators = [NumberRange(1900, 2023)])
    market_value = IntegerField("Market Value (€)")

    image = FileField("Upload Image", validators=[FileRequired(), FileAllowed(['webp'], "Please upload a '.webp' file")])

    add = SubmitField("Add New Entry")
    edit = SubmitField("Edit Entry")