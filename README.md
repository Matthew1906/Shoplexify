# Shoplexify

#### This is a simple online shop, created using Flask as the Backend Framework. This project is a part of my 100 Days of Python project.

#### This project supposedly includes payment processing, but the suggested api don't really include my country and it kinda felt like fraud to me, using sandbox doesn't seem to achieve anything
#### Please take note that this website is not responsive at all:v, This project's purpose is to practice by skills in backend using flask. I'll improve it from time to time tho.

#### My Approach toward this project
1. Create Flowchart and ERD, design tables
2. Build database, Create basic layout of website(navbar and footer), add categories to the database (save the block of code into ./init/init.txt)
3. User Authentication (login, register, logout) and Mock data for products (taken from amazon, with a little tinkering) -> saved to csv file
4. Insert Mock Data into Database, Add product management functionality (Add new products and Update products), add decorators, and implemented template filters
5. Add to Cart function, Pagination, and Search
6. Transaction and Checkout
7. Add Product Review, Slightly fix responsiveness
8. Restructuring the Application using Blueprints
9. Add session feature so that user can add products to cart without login
10. Deploy the app to Heroku

#### Steps of Deployment:
1. Clone this repository
2. Set up a virtual environment by typing 'python -m venv env' in the command line
3. Set your interpreter path to the virtual environment path
4. Download all the dependencies (modules) by typing 'python -m pip install -r requirements.txt'
5. When first deploying the app, don't forget to uncomment the create_database(app) call in __init__.py : create_app()
6. Lastly, don't forget to setup SECRET_KEY from .env file so that the program can start
7. Start the application by running the code, and then go to http://127.0.0.1:5000/

#### Todo:
- Clear cart function (cart.py, cart.html)
- Remove order from cart (cart.py, cart.html)
- Improve frontend
