# Shoplexify

#### This is a simple multi-page online shop application, created using [Flask](https://flask.palletsprojects.com/en/2.1.x/) as the Backend Framework and [Bootstrap CSS](https://getbootstrap.com/) as the Frontend Framework. The project premise came from my [100 Days of Python Udemy course](https://github.com/Matthew1906/100DaysOfPython).

#### This project's purpose is to practice by skills in backend using [Flask](https://flask.palletsprojects.com/en/2.1.x/). Therefore, in terms of UI and UX, it's not great. However, I might improve it from time to time.

#### I also implemented a bit of payment processing using [midtrans sandbox](https://docs.midtrans.com/en/technical-reference/sandbox-test). Please take note that the payment process itself is indeed fake

#### Languages and Tools: 
[![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) 
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.1.x/) 
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://www.w3schools.com/html/) 
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://www.w3schools.com/css/)
[![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](https://www.javascript.com/) 
[![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
[![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)](https://dashboard.heroku.com/) 
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
10. Add Sandbox Payment Processing using Midtrans
11. Deploy the app to Heroku
