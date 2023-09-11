# Financial Asset Portfolio Backtester

Welcome to the Financial Asset Portfolio Backtester project! This web application allows users to perform backtests on stocks using a ranking system and fundamental indicators such as EBIT/EV and ROE. The core features of this application include generating new asset portfolios every month based on a provided dataset, creating a ranking system using fundamental indicators, and performing web scraping to gather data from a financial website. The project primarily focuses on full-stack development, incorporating technologies such as HTML, CSS, JavaScript, Bootstrap, user authentication, database management, Python, Flask, and data visualization.

## Project Overview
- Backtesting Engine: The application leverages a provided dataset (date, asset, price, EBIT/EV, ROE) to create and manage portfolios. It calculates rankings using the fundamental indicators and selects the top assets to form a portfolio.

- Web Scraping: A web scraping module fetches data from the website fundamentus.com daily. This data is used to generate a ranking of assets, which aids in portfolio creation.

- User Authentication: Users can create accounts, log in, and maintain sessions to access the app's features securely.

- Database Integration: The application integrates with a SQL database to store user data, portfolios, and other relevant information.

- Data Visualization: The app includes interactive data visualization elements such as time-series line graphs, tables displaying ranking results, and a doughnut chart representing the portfolio's assets.

## Usage

To use the Financial Asset Portfolio Backtester:

1. Clone the Repository: Clone this GitHub repository to your local machine.

git clone https://github.com/your-username/financial-portfolio-backtester.git

2. Set Up the Environment: Install the required dependencies and configure the database connection.

3. Run the Application: Start the app.py Flask application, and access it through a web browser.

4. User Registration: Create a user account to access the backtesting and ranking features.

5. Perform Backtests: Use the app to perform backtests on stocks, generate portfolios, and analyze results.

## Technologies Used
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Python, Flask
- Database: SQL (configured with Flask-SQLAlchemy)
- Data Visualization: Chart.js
- Web Scraping: BeautifulSoup
- User Authentication: Flask-Login
- Version Control: Git and GitHub

## Project Structure

The project is structured as follows:

- app.py: The main Flask application file.
- templates/: HTML templates for rendering web pages.
- static/: Static assets (CSS, JavaScript, images).
- models.py: Defines the database models using SQLAlchemy.
- routes.py: Contains the application routes and view functions.
- forms.py: Defines forms for user registration and login.
- scraper.py: Web scraping module to collect financial data.
- charts.py: Contains functions for plotting charts using Chart.js.
- config.py: Configuration settings for the application.

## Contributing

Contributions to the Financial Asset Portfolio Backtester project are welcome! You can contribute by reporting issues, suggesting improvements, or creating pull requests. Feel free to fork the repository and submit your contributions.

## Acknowledgments

This project was inspired by a bootcamp provided by Varos, a YouTube channel, which included the dataset and code to get started.

## License

This project is licensed under the MIT License.
