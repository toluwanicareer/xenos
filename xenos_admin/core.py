def bitcoin_dollar_rate():
	client=get_coinbase_client()
	rates=client.get_exchange_rates(currency='BTC')
	return rates.rates.USD

def convert_to_dollar(amount):
	rate=bitcoin_dollar_rate()
	return float(rate)*float(amount)