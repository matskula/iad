from functools import partial

import pandas as pd
from dateutil.parser import parse


def time_transform(time_str: str):
    return parse(time_str).strftime('%H:%M')


def lstrip_int_transform(value: str, characters: str, output_type: type = int):
    if not isinstance(value, str):
        return value
    return output_type(value.rstrip(characters))


def preprocess_data(weather_df: pd.DataFrame):
    weather_df['day/month'] = weather_df['day/month'].astype(str) + '.2019'
    weather_df.set_index('day/month', inplace=True)
    weather_df['Time'] = weather_df['Time'].apply(time_transform)
    weather_df['Temperature'] = weather_df['Temperature'].apply(partial(lstrip_int_transform, characters=' FC'))
    weather_df['Dew Point'] = weather_df['Dew Point'].apply(partial(lstrip_int_transform, characters=' FC'))
    weather_df['Humidity'] = weather_df['Humidity'].apply(partial(lstrip_int_transform, characters=' %'))
    weather_df['Wind Speed'] = weather_df['Wind Speed'].apply(partial(lstrip_int_transform, characters=' kmph'))
    weather_df['Wind Gust'] = weather_df['Wind Gust'].apply(partial(lstrip_int_transform, characters=' kmph'))
    # uncomment for scrapped dataset
    # weather_df['Pressure'] = weather_df['Pressure'].apply(lambda x: x.replace(',', '.'))
    # weather_df['Pressure'] = weather_df['Pressure'].apply(
    #     partial(lstrip_int_transform, characters=' in', output_type=float)
    # )
    # weather_df['Precip.'] = weather_df['Precip.'].apply(lambda x: x.replace(',', '.'))
    # weather_df['Precip.'] = weather_df['Precip.'].apply(
    #     partial(lstrip_int_transform, characters=' in', output_type=float)
    # )
    # if 'Precip Accum' in weather_df.columns:
    #     weather_df['Precip Accum'] = weather_df['Precip Accum'].apply(lambda x: x.replace(',', '.'))
    #     weather_df['Precip Accum'] = weather_df['Precip Accum'].apply(
    #         partial(lstrip_int_transform, characters=' in', output_type=float)
    #     )
