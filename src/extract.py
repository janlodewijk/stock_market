import yfinance as yf
import time  # To handle API rate limiting
import logging  # For logging missing data or errors
import pandas as pd

# Configure logging to track missing data or issues
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_esg_data(tickers, save_path: str = None) -> dict:
    """
    Extract ESG scores and stock price data for given tickers using Yahoo Finance.
    
    Args:
        tickers (list): List of stock ticker symbols (e.g., ["AAPL", "TSLA", "MSFT"]).
        save_path (str, optional): Path to save extracted data as a JSON or CSV file.
    
    Returns:
        dict: Extracted ESG and stock data.
    """
    
    # Initialize a dictionary to store extracted data
    extracted_data = {}

    for ticker in tickers:
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)

        # Extract ESG data
        esg = stock.sustainability
        
        # ✅ Check if ESG data is available
        if esg is None:  # <- Condition to check if ESG data is None or empty
            logging.warning(f"ESG data missing for {ticker}")
            esg = None  # Or choose how you want to handle it

        # Extract stock price data (latest 1-day history)
        price = stock.history(period="1d")

        # ✅ Check if stock price data is available
        if price is None:  # <- Condition to check if price data is empty
            logging.warning(f"Stock price data missing for {ticker}")
            price = None  # Or choose how you want to handle it

        # ✅ Store only if at least one of the two is available
        if esg is not None or price is not None:
            extracted_data[ticker] = {
                "esg": pd.DataFrame(esg),  # <- Convert ESG DataFrame to a dictionary if needed
                "price": price  # <- Extract relevant stock price info
            }

        # ✅ Rate limiting to prevent API blocking
        time.sleep(1)  # Pause for 1 second before the next request

    return extracted_data
