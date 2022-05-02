# Shoplexify

#### This is a simple online shop, created using Flask as the Backend Framework and Bootstrap CSS as the Frontend Framework. This project is a part of my 100 Days of Python project.

#### This project supposedly includes payment processing, but the suggested api don't really include my country and it kinda felt like fraud to me, using sandbox doesn't seem to achieve anything
#### This project's purpose is to practice by skills in backend using flask. Therefore, in terms of UI and UX, it's not great. I'll improve it from time to time.

#### My Approach toward this project
1. Create ERD and design tables
2. Build database, Create basic layout of website(navbar and footer), add categories to the database (save the block of code and comment them)
3. User Authentication (login, register, logout) and Mock data for products (taken from amazon, with a little tinkering) -> saved to .csv
4. Insert Mock Data into Database, Add product management functionality (Add new products and Update products), add Admin only decorator, and implemented template filter 
5. Add to Cart function, Pagination, and Search
6. Transaction and Checkout
7. Add Product Review, Slightly fix responsiveness
8. Restructuring the Application using Blueprints
9. Fix Responsiveness 
10. Deploy the app to Heroku

#### Steps of Deployment:
1. Clone this repository
2. Set up a virtual environment by typing 'python -m venv env' in the command line
3. Set your interpreter path to the virtual environment path
4. Download all the dependencies (modules) by typing 'python -m pip install -r requirements.txt'
5. When first deploying the app, don't forget to uncomment the create_database(app) call in __init__.py : create_app()
6. Lastly, don't forget to setup SECRET_KEY from .env file so that the program can start
7. Start the application by running the code, and then go to http://127.0.0.1:5000/
