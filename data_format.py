#data_format.py
import pandas as pd
import requests
from io import StringIO

def gather_data():
  # Fetch the data from the CoinMetrics API
  url = f'https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv'
  response = requests.get(url)
  data = pd.read_csv(StringIO(response.text), low_memory=False)
  return data

def create_report_data(data):
  # New Metrics
  data['mvrv_ratio'] = data['CapMrktCurUSD'] / data['CapRealUSD']
  data['realised_price'] = data['CapRealUSD'] / data['SplyCur']
  data['nupl'] = (data['CapMrktCurUSD'] -
                  data['CapRealUSD']) / data['CapMrktCurUSD']
  data['fear_greed_index'] = 0

  # Price Moving Averages
  data['200_day_ma_priceUSD'] = data['PriceUSD'].rolling(window=200).mean()
  data['200_week_ma_priceUSD'] = data['PriceUSD'].rolling(window=200 * 7).mean()

  # Metric Moving Averages
  data['7_day_ma_HashRate'] = data['HashRate'].rolling(window=7).mean()
  data['7_day_ma_AdrActCnt'] = data['AdrActCnt'].rolling(window=7).mean()
  data['7_day_ma_TxCnt'] = data['TxCnt'].rolling(window=7).mean()
  data['7_day_ma_TxTfrValAdjUSD'] = data['TxTfrValAdjUSD'].rolling(window=7).mean()

  # Price Multiples
  data['200_day_multiple'] = data['PriceUSD'] / data['200_day_ma_priceUSD']

  # Thermocap Multiple
  data['thermocap_multiple'] = data['CapMrktCurUSD'] / data['RevAllTimeUSD']
  data['thermocap_multiple_4'] = (4 * data['RevAllTimeUSD']) / data['SplyCur']
  data['thermocap_multiple_8'] = (8 * data['RevAllTimeUSD']) / data['SplyCur']
  data['thermocap_multiple_16'] = (16 * data['RevAllTimeUSD']) / data['SplyCur']
  data['thermocap_multiple_32'] = (32 * data['RevAllTimeUSD']) / data['SplyCur']

  # Realized Cap Multiple
  data['realizedcap_multiple_3'] = (3 * data['CapRealUSD']) / data['SplyCur']
  data['realizedcap_multiple_5'] = (5 * data['CapRealUSD']) / data['SplyCur']
  data['realizedcap_multiple_7'] = (7 * data['CapRealUSD']) / data['SplyCur']

  # --- Filter Data --- #

  # List of metric you want to filter
  list_of_metrics = [
    'time', 'PriceUSD', 'CapMrktCurUSD', 'VtyDayRet30d', 'VtyDayRet180d',
    'SplyCur', 'HashRate', '7_day_ma_HashRate', 'AdrActCnt',
    '7_day_ma_AdrActCnt', 'TxCnt', '7_day_ma_TxCnt', 'TxTfrValAdjUSD',
    '7_day_ma_TxTfrValAdjUSD', 'FeeByteMeanNtv', 'FeeTotUSD', 'RevAllTimeUSD',
    'CapRealUSD', '200_day_ma_priceUSD', 'fear_greed_index',
    '200_day_multiple', '200_week_ma_priceUSD', 'mvrv_ratio', 'realised_price',
    'nupl', 'thermocap_multiple', 'thermocap_multiple_4',
    'thermocap_multiple_8', 'thermocap_multiple_16', 'thermocap_multiple_32',
    'realizedcap_multiple_3', 'realizedcap_multiple_5',
    'realizedcap_multiple_7'
  ]

  selected_metrics = data[data.columns.intersection(list_of_metrics)]

  # Convert the time column to datetime format
  selected_metrics = selected_metrics.copy()
  selected_metrics['time'] = pd.to_datetime(selected_metrics['time'])
  return selected_metrics

def report_data_calc(date, selected_metrics):
  # Get the current values
  current_values = selected_metrics[selected_metrics['time'] == date].copy()
  # Calculate the 7 day, and 30 day changes for each metric
  for metric in current_values.columns:
    if metric != 'time':
      current_values.loc[:, f'{metric}_7_Day_Change'] = (
        (current_values[metric] - selected_metrics[selected_metrics['time'] == date - pd.Timedelta(days=7)].iloc[0][metric]) /
        selected_metrics[selected_metrics['time'] == date - pd.Timedelta(days=7)].iloc[0][metric]) * 100
      current_values.loc[:, f'{metric}_30d_change'] = (
        (current_values[metric] - selected_metrics[selected_metrics['time'] == date - pd.Timedelta(days=30)].iloc[0][metric]) /
        selected_metrics[selected_metrics['time'] == date - pd.Timedelta(days=30)].iloc[0][metric]) * 100
  return current_values
