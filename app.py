from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['GET','POST'])
def get_recommendations():
    # Retrieve form inputs
    risk_tolerance = request.form.get('riskTolerance')
    investment_amount = int(request.form.get('investmentAmount'))
    investment_duration = int(request.form.get('investmentDuration'))

    # Generate investment recommendations
    recommendations = generate_investment_recommendations(risk_tolerance, investment_amount, investment_duration)

    # Generate charts
    save_folder = 'static/charts'
    os.makedirs(save_folder, exist_ok=True)

    for recommendation in recommendations:
        symbol = recommendation[0]
        chart_title = f'{symbol} Performance'

        stock = yf.Ticker(symbol)
        historical_data = stock.history(period=f"{investment_duration}d")
        historical_data = historical_data.dropna(subset=['Close', 'Volume'])

        # Bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(historical_data.index, historical_data['Close'], color='blue')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.title(chart_title)
        plt.xticks(rotation=45)
        plt.tight_layout()

        save_path_bar = os.path.join(save_folder, f'{symbol}_bar.png')
        plt.savefig(save_path_bar)
        plt.close()

        # Line chart
        plt.figure(figsize=(10, 6))
        plt.plot(historical_data.index, historical_data['Volume'], color='red')
        plt.xlabel('Date')
        plt.ylabel('Trading Volume')
        plt.title(chart_title)
        plt.xticks(rotation=45)
        plt.tight_layout()

        save_path_line = os.path.join(save_folder, f'{symbol}_line.png')
        plt.savefig(save_path_line)
        plt.close()

    # Calculate portfolio performance
    portfolio_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]  # Portfolio stocks
    portfolio_performance = calculate_portfolio_performance(portfolio_symbols, investment_duration)

    return render_template('recommendations.html', recommendations=recommendations, portfolio_performance=portfolio_performance)

def generate_investment_recommendations(risk_tolerance, investment_amount, investment_duration):
    # Define stock symbols
    stock_symbols = ["TSLA", "JPM", "V", "NVDA", "PYPL", "DIS", "NFLX", "UBER", "ADBE", "CRM", "INTC", "PFE", "MCD", "NKE", "KO", "PEP", "T", "VZ", "CSCO", "IBM", "XOM", "CVS", "WMT", "PG", "HD", "BAC", "WFC", "JNJ", "UNH", "CMCSA", "TMO", "ABT", "MRK", "GILD", "ABBV", "QCOM", "NVAX", "AMD", "BMY", "ORCL", "ZM", "GE"]
    recommendations = []

    for symbol in stock_symbols:
        try:
            # Retrieve stock data
            stock = yf.Ticker(symbol)

            # Skip if the stock's previous close is not available
            if not stock.info['regularMarketPreviousClose']:
                continue

            historical_data = stock.history(period=f"{investment_duration}d")
            historical_data = historical_data.dropna(subset=['Close', 'Volume'])

            # Calculate average return and volatility
            average_return = historical_data['Close'].pct_change().mean()
            volatility = historical_data['Close'].pct_change().std()

            symbol_name = f"{stock.info['symbol']} - {stock.info['longName']}"
            recommendation = (symbol, symbol_name, average_return)

            # Apply investment criteria based on risk tolerance, average return, volatility, and investment amount
            if risk_tolerance == 'low' and average_return > 0 and investment_amount >= 1000:
                recommendations.append(recommendation)
            elif risk_tolerance == 'medium' and average_return > 0 and volatility < 0.2 and investment_amount >= 5000:
                recommendations.append(recommendation)
            elif risk_tolerance == 'high' and average_return > 0 and volatility < 0.3 and investment_amount >= 10000:
                recommendations.append(recommendation)

        except Exception as e:
            print(f"Error retrieving data for symbol {symbol}: {str(e)}")

    # Sort and limit recommendations
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommendations = recommendations[:10]

    return recommendations

def calculate_portfolio_performance(portfolio_symbols, investment_duration):
    portfolio_performance = {}

    for symbol in portfolio_symbols:
        try:
            #Retrieve stock info
            stock = yf.Ticker(symbol)
            if not stock.info['regularMarketPreviousClose']:
                continue
            
            #Calculate historical data
            historical_data = stock.history(period=f"{investment_duration}d")
            historical_data = historical_data.dropna(subset=['Close'])

            #Calculate average return and volatility
            average_return = historical_data['Close'].pct_change().mean()
            volatility = historical_data['Close'].pct_change().std()

            symbol_name = f"{stock.info['symbol']} - {stock.info['longName']}"
            previous_close = stock.info['regularMarketPreviousClose']
            open_price = stock.info['regularMarketOpen']
            day_low = stock.info['dayLow']
            day_high = stock.info['dayHigh']

            # Store the stock's performance information in the portfolio_performance dictionary
            portfolio_performance[symbol] = {
                'Symbol': symbol,
                'Stock Name': symbol_name,
                'Average Return': average_return,
                'Volatility': volatility,
                'Previous Close': previous_close,
                'Open': open_price,
                'Day Low': day_low,
                'Day High': day_high
            }

        except Exception as e:
            print(f"Error retrieving data for symbol {symbol}: {str(e)}")

    return portfolio_performance


if __name__ == '__main__':
    app.run(debug=True)
