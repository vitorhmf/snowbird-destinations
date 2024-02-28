import pandas as pd

# Paths     
CITIES = 'snowbird-destinations/1_raw_layer/cities_metrics/world_city_population.csv'


def transform_cities_metrics(filepath):
    df = pd.read_csv(filepath)

    # Filter
    df_filtered = df[
        ['country', 'city', 'pop2024']
        ][
            (df['city'].isin([
                'San Diego',
                'Los Angeles',
                'Broward',
                'Rio de Janeiro',
                'Santiago',
                'Belize'          
            ]))
        ]

    # Edit Columns
    df_final = df_filtered.rename(columns={'pop2024': 'population'})

    # Feature Engineering
    # City Size
    df_final['size'] = df_final['population'].apply(
        lambda x: 'big' if x>10000000 
        else 'medium' if x>5000000 
        else 'small' if x>1000000 
        else 'tiny'
        )

    # Currency
    df_final['currency'] = df_final['country'].apply(
        lambda x: 'BRL' if x=='Brazil'
        else 'USD' if x=='United States'
        else 'CLP' if x=='Chile'
        else 'BZD'
        )
    
    #Quote
    df_final['usd_quote'] = df_final['currency'].apply(
        lambda x: 4.99 if x=='BRL'
        else 1.0 if x=='USD'
        else 980.39 if x=='CLP'
        else 2.02
        )
    

    return df_final
    
def main():
    df_final = transform_cities_metrics(CITIES)
    df_final.to_csv('snowbird-destinations/2_curated_layer/cities_metrics.csv', index=False)

if __name__ == "__main__":
    main()