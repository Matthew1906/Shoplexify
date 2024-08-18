from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField , PasswordField, SubmitField, SelectMultipleField, SelectField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import InputRequired, URL, email, NumberRange

# Authentication
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    dob = DateField('Date of Birth', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField("Login")

# Product
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[InputRequired()])
    description = TextAreaField('Product Description', validators=[InputRequired()])
    image_url = StringField('Product Image URL', validators=[InputRequired(), URL()])
    price = IntegerField('Product Price', validators=[InputRequired(), NumberRange(min=1)])
    stock = IntegerField('Stock', validators=[InputRequired(), NumberRange(min=1)])
    categories = SelectMultipleField(
        coerce=int,
        label='Categories', 
        choices=[
            (1, 'Automotive'), (2,'Arts and Crafts'),
            (3, 'Books'), (4,'Clothing'), 
            (5, 'Electronics'), (6, 'Food and Beverages'),
            (7,'Health and Beauty'),(8, 'Home and Garden'), 
            (9, 'Office'), (10,'Sports & Outdoor Activities')
        ]
    )
    submit = SubmitField('Save Product')

# Cart
class CartForm(FlaskForm):
    count = IntegerField('Number of Products', validators=[InputRequired()])
    def __init__(self, limit=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if limit:
            self.count.validators.append(NumberRange(min=0, max=limit))
            self.count.widget = NumberInput(min=0, max=limit)

# Checkout
class TransactionForm(FlaskForm):
    address = TextAreaField('Address', validators=[InputRequired()]) 
    submit = SubmitField("Checkout")

# Product Review
class ReviewForm(FlaskForm):
    rating = IntegerField('Your Rating (1-5)', validators=[InputRequired(), NumberRange(min=1, max=5)], widget=NumberInput(min=1, max=5))
    body = TextAreaField('Review', validators=[InputRequired()])
    submit = SubmitField('Submit Review')
    