# Financial Asset Portfolio Backtester

Welcome to the **Financial Asset Portfolio Backtester** project! This **web application** allows users to **perform backtests** on stocks using a ranking system and fundamental indicators such as EBIT/EV and ROIC. The core features of this application include generating new asset portfolios every month based on a provided dataset, creating a **ranking system** using fundamental indicators, and performing **web scraping** to gather data from a financial website. The project primarily focuses on **full-stack development**, incorporating technologies such as **HTML, CSS, JavaScript, Bootstrap, user authentication, database management, Python, Flask, and data visualization**.

This project encompasses two core functionalities:

### Part 1 - Financial Asset Backtesting:

<img src="https://github.com/felipecacique/PortfolioBacktester/blob/main/img/backtest-page.png" />

This component of the application empowers users to perform backtests on financial assets. The backtesting simulation revolves around a dynamically updated monthly portfolio. This portfolio is meticulously constructed based on a ranking system driven by fundamental indicators sourced from a dataset generously provided by [Varos](https://www.youtube.com/@varos-programacao). As a powerful feature, it generates performance graphs comparing the model's performance against the Ibovespa (IBOV) index over the past seven years. This part enables users to gain insights into the historical performance of their portfolios in real-world scenarios.

### Part 2 - Real-Time Data Acquisition and Ranking:

<img src="https://github.com/felipecacique/PortfolioBacktester/blob/main/img/ranking-page.png" />

The second component of the application excels in web scraping, extracting real-time financial data from [Fundamentus](https://www.fundamentus.com.br/resultado.php) on a daily basis. Leveraging this timely data, the backend of the application dynamically generates a ranking system. This ranking system is then elegantly presented in a table format, showcasing the best assets to consider for investment. The criteria used in this ranking system are defined in Part 1. The top-ranked assets serve as the building blocks of the user's portfolio. Should the user desire to create new portfolios on a monthly basis, Part 2 equips them with the essential data and insights needed to make informed investment decisions.

Together, these two parts offer a comprehensive solution for financial asset analysis and portfolio management, providing users with a powerful toolset to make data-driven investment choices.

## Project Overview

- **Backtesting Engine:** The application leverages a provided dataset (date, asset, price, EBIT/EV, ROIC) to create and manage portfolios. It calculates rankings using the fundamental indicators and selects the top assets to form a portfolio.

- **Web Scraping:** A web scraping module fetches data from the [Fundamentus](https://www.fundamentus.com.br/resultado.php) website daily. This data is used to generate a ranking of assets, which aids in portfolio creation.

- **User Authentication:** Users can create accounts, log in, and maintain sessions to access the app's features securely.

  <img src="https://github.com/felipecacique/PortfolioBacktester/blob/main/img/login-page.png" />

- **Database Integration:** The application integrates with a SQL database to store user data, portfolios, and other relevant information.

- **Data Visualization:** The app includes interactive data visualization elements such as time-series line graphs, tables displaying ranking results, and a doughnut chart representing the portfolio's assets.

## Usage

To run the Financial Portfolio Backtester locally, follow these steps:

1. **Clone the Repository:** Clone this GitHub repository to your local machine.


- `https://github.com/yourusername/FinancialAssetPortfolioBacktester.git`

2. **Set Up the Environment:** Install the required dependencies and configure the database connection.

3. **Run the Application:** Start the Flask application, and access it through a web browser.

- `python app.py`

4. **Access the application:** Through your web browser at `http://localhost:5000`.

5. **User Registration:** Create a user account to access the backtesting and ranking features.

6. **Perform Backtests:** Use the app to perform backtests on stocks, generate portfolios, and analyze results.

7. **Real-Time Ranking:** Create a real-time portfolio every month based on a ranking system.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Python, Flask
- **Database:** SQL (configured with SQLite)
- **Data Visualization:** Chart.js
- **Web Scraping:** BeautifulSoup
- **User Authentication:** Flask-Login
- **Version Control:** Git and GitHub

## Project Structure

The project is structured as follows:

- **app.py:** The main Flask application file. Contains the application routes and requests for both the **Backend** and **Frontend**.
  
### Frontend:
  
- **templates/:** HTML templates for rendering web pages.
- **templates/index.html:** Defines forms for user registration and login.
- **templates/dashboard.html:** Create the dashboard page, containing a sidebar navigation, parameters form, buttons, charts, and table.
- **static/:** Static assets (CSS, JavaScript, images).
- **static/index-script.js:** JavaScript functionality of the login page.
- **static/dashboard-script.js:** JavaScript functionality of the dashboard page.
- **static/styles.css:** Define the visual styles and layout of a web page.

### Backend: 

- **CriandoUmModeloDeInvestimento.py:** Performs backtesting of a monthly generated stock portfolio based on financial indicators and ranking system.
- **PegarSitesEmSitesAutomatizarCarteira.py:** Web scraping module to collect financial data and create a ranking.
- **database.sqlite:** Defines the user database using SQL-Lite.
- **tabela.pickle:** Stores the fundamentus.com data.
- **dados_empresa.csv:** Historical dataset with date, asset, price, and financial indicators provided by Varos.
- **ibov.csv:** Ibov historical data.



## Data Sources

The application uses two primary data sources:

1. **Varos Dataset:** A dataset provided by [Varos](https://www.youtube.com/@varos-programacao) containing fundamental financial indicators such as EBIT/EV and ROIC for various financial assets.
   
2. **Fundamentus Web Scraping:** Daily web scraping of financial data from [Fundamentus](https://www.fundamentus.com.br/resultado.php) to obtain real-time information on assets.

### Disclaimer:

This project is intended for educational and learning purposes only. The financial simulations, backtesting, and ranking systems implemented within this application are not indicative of or meant to provide financial or investment advice. Users should exercise caution and conduct thorough research and analysis before making any real-world investment decisions. The data, rankings, and portfolio simulations generated by this application are purely hypothetical and do not represent actual investment recommendations. Always consult with a qualified financial advisor or professional before making any financial decisions or investments.

## Acknowledgments

* This project was inspired by a bootcamp provided by Varos, a YouTube channel, which included the dataset and code to get started.

* This project was made possible with the assistance of [ChatGPT 3.5](https://chat.openai.com/), which provided valuable guidance, generated code snippets, and offered helpful tips during the development process. We are grateful for the support and insights provided by this AI-powered model. Additionally, this README was created with the assistance of ChatGPT to provide comprehensive project documentation.

## Deployment

You can try our app on [https://wood-lemon-clam.glitch.me](https://wood-lemon-clam.glitch.me). Not all features are fuctional in this [Glitch](https://glitch.com/) free web server, such as registering a new user and doing the web-scraping with selenium. For a better experience, open it on the desktop.

