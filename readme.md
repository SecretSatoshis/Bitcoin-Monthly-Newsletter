# Secret Satoshis Newsletter

Welcome to the repository of Secret Satoshis Newsletter, an automated newsletter generator that curates Bitcoin data and content. The application is built using Python, with Streamlit for the web interface, and runs in Replit, an online integrated development environment (IDE).

## Project Overview

This project provides an automated system for generating a comprehensive newsletter. It uses Streamlit, a Python library that allows you to create custom web applications for machine learning and data science. The application is designed to accept various inputs about Bitcoin and output a curated newsletter complete with up-to-date bitcoin metrics and relevant content such as news stories, podcast episodes, tweets, and books.

The newsletter generator is composed of three main Python files:

- `data_format.py`: Fetches and processes data from CoinMetrics. It calculates a variety of metrics and their changes over 7-day and 30-day periods.
- `content_format.py`: Fetches and processes the headlines of the curated content for the newsletter and generates a detailed and interpretive analysis based on the data provided.
- `streamlist_app.py`: This is the main Streamlit application where user input is collected, and the final newsletter is generated and displayed.

These scripts use several libraries, such as pandas, Streamlit, and openai, to fetch and process data, scrape web content, and generate a natural language summary using OpenAI's GPT-4 model.

## How to Run the Application in Replit

To run this application in Replit, follow these steps:

1. Set your OpenAI API key as an environment variable. Code: `openai.api_key = os.getenv("MY_SECRET")`
2. Click the 'Run' button at the top of Replit interfance.

## Interacting with the Streamlit Application

When you run the application, you'll find various input fields:

- Report date: Here, you input the date for which you want the report to be generated.
- Support and Resistance Levels: You can input the support and resistance price levels for the given date, along with their contexts.
- Content URLs: Here, you can input comma-separated URLs for various content types, such as News Stories, Podcasts, Tweets, and Books.

Once all inputs are filled, click the "Submit" button. The application will then generate the newsletter, display it in the Streamlit app.

## License
This project is licensed under the terms of the GPLv3 license.
