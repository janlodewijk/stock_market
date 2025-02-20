from config import TICKERS
from extract import extract_esg_data




# Run extract function
data = extract_esg_data(TICKERS)

print(data)
