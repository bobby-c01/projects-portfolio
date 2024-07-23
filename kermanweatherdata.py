import matplotlib.pyplot as plt
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
params = {
    "latitude": 36.7236,
    "longitude": -120.0599,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "minutely_15": "temperature_2m",
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "ms",
    "precipitation_unit": "inch",
    "timezone": "America/Los_Angeles"
}
responses = openmeteo.weather_api(url, params=params)

response = responses[0]

minutely_15 = response.Minutely15()
minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()

minutely_15_data = {"date": pd.date_range(
    start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
    end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=minutely_15.Interval()),
    inclusive="left"
), "temperature_2m": minutely_15_temperature_2m}

minutely_15_dataframe = pd.DataFrame(data=minutely_15_data)

daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=daily.Interval()),
    inclusive="left"
), "temperature_2m_max": daily_temperature_2m_max, "temperature_2m_min": daily_temperature_2m_min}

daily_dataframe = pd.DataFrame(data=daily_data)


plt.figure(figsize=(14, 7))


plt.subplot(2, 1, 1)
plt.plot(minutely_15_dataframe['date'], minutely_15_dataframe['temperature_2m'], label='Minutely Temperature 2m', color='blue')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.title('15 Minute Temperature Data')
plt.legend()
plt.grid()


plt.subplot(2, 1, 2)
plt.plot(daily_dataframe['date'], daily_dataframe['temperature_2m_max'], label='Daily Max Temperature 2m', color='red')
plt.plot(daily_dataframe['date'], daily_dataframe['temperature_2m_min'], label='Daily Min Temperature 2m', color='green')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.title('Daily Temperature Data')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


if __name__ == "__main__":
    plot_temperature_forecast_trends()

