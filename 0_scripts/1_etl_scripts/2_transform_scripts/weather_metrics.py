import pandas as pd

# Paths
WEATHER_WISCONSIN = '1_raw/weather/weather_wisconsin.csv'
WEATHER_CALIFORNIA = '1_raw/weather/weather_california.csv'
WEATHER_FLORIDA = '1_raw/weather/weather_florida.csv'
WEATHER_RIO_DE_JANEIRO = '1_raw/weather/weather_rio_de_janeiro.csv'
WEATHER_SANTIAGO = '1_raw/weather/weather_santiago.csv'
WEATHER_BELIZE = '1_raw/weather/weather_belize.csv'

def transform_weather_data(files_and_regions):
    dfs = []
    for file, region in files_and_regions:
        df = pd.read_csv(file, skiprows=11)
        
        df_avg = df.drop(['YEAR', 'ANN'], axis=1).groupby(['PARAMETER']).mean().reset_index()
        df_avg['REGION'] = region
        
        dfs.append(df_avg)

    weather_df = pd.concat(dfs, ignore_index=True)

    replace = {
        'T2M': 'temperature',
        'WS10M': 'wind_speed',
        'RH2M': 'humidity'
    }
    weather_df['PARAMETER'] = weather_df['PARAMETER'].replace(replace)


    columns = ['REGION'] + [col for col in weather_df.columns if col != 'REGION']
    weather_df = weather_df[columns]
    weather_df.columns = [col.lower() for col in weather_df.columns]

    return weather_df

def main():
    files_and_regions = [
        (WEATHER_WISCONSIN, 'Wisconsin'),
        (WEATHER_CALIFORNIA, 'California'),
        (WEATHER_FLORIDA, 'Florida'),
        (WEATHER_RIO_DE_JANEIRO, 'Rio de Janeiro'),
        (WEATHER_SANTIAGO, 'Santiago'),
        (WEATHER_BELIZE, 'Belize')
    ]

    weather_df = transform_weather_data(files_and_regions)
    weather_df.to_csv('2_curated/weather.csv', index=False)

if __name__ == "__main__":
    main()