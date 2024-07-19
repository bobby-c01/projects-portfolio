import requests
import urllib.parse
import plotly.graph_objects as go


api_key = ${{ secrets.API_KEY }}
location = 'kerman'
units = 'imperial'
timesteps = ['1d']

weather_forecast_data = {
    'apikey': api_key,
    'location': location,
    'units': units,
    'timesteps': ','.join(timesteps)
}
query_string = urllib.parse.urlencode(weather_forecast_data)

get_weather_forecast_url = "https://api.tomorrow.io/v4/weather/forecast"
url = f"{get_weather_forecast_url}?{query_string}"
headers = {'accept': 'application/json'}


def plot_temperature_forecast_trends():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        weather_forecast_res = response.json()

        daily_weather_forecast_data = weather_forecast_res.get('timelines', {}).get('daily', [])
        temperature_plots = convert_data_into_temp_plots(daily_weather_forecast_data)

        layout = {
            'title': 'Kerman Temperature Trends Over the Next 5 Days',
            'xaxis': {'title': 'Date', 'type': 'date'},
            'yaxis': {'title': f'Temperature ({units})', 'type': 'linear'},
            'showlegend': True,
            'hovermode': 'x unified'
        }
        fig = go.Figure(data=temperature_plots, layout=layout)
        fig.show()

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def convert_data_into_temp_plots(raw_data):
    max_temperatures = []
    min_temperatures = []
    avg_temperatures = []
    time_stamps = []

    for day in raw_data:
        time_stamps.append(day.get('time', ''))
        max_temperatures.append(day.get('values', {}).get('temperatureMax', None))
        min_temperatures.append(day.get('values', {}).get('temperatureMin', None))
        avg_temperatures.append(day.get('values', {}).get('temperatureAvg', None))

    return [
        go.Scatter(
            x=time_stamps,
            y=max_temperatures,
            mode='lines+markers',
            name='Max Temp',
            hoverinfo='text+x+y'
        ),
        go.Scatter(
            x=time_stamps,
            y=min_temperatures,
            mode='lines+markers',
            name='Min Temp',
            hoverinfo='text+x+y'
        ),
        go.Scatter(
            x=time_stamps,
            y=avg_temperatures,
            mode='lines+markers',
            name='Avg Temp',
            hoverinfo='text+x+y'
        )
    ]


if __name__ == "__main__":
    plot_temperature_forecast_trends()

