import pandas as pd

# Paths     
LISTINGS_SAN_DIEGO = 'snowbird-destinations/1_raw_layer/airbnb/listings_california_san_diego.csv'
LISTINGS_LOS_ANGELES = 'snowbird-destinations/1_raw_layer/airbnb/listings_california_los_angeles.csv'
LISTINGS_BROWARD = 'snowbird-destinations/1_raw_layer/airbnb/listings_florida_broward.csv'
LISTINGS_RIO_DE_JANEIRO = 'snowbird-destinations/1_raw_layer/airbnb/listings_brazil_rio_de_janeiro.csv'
LISTINGS_SANTIAGO = 'snowbird-destinations/1_raw_layer/airbnb/listings_chile_santiago.csv'
LISTINGS_BELIZE = 'snowbird-destinations/1_raw_layer/airbnb/listings_central_america_belize.csv'

def transform_listings_data(files_and_regions):
    dfs = []
    for file, region in files_and_regions:
        
        pd.set_option('display.max_colwidth', None)
        df = pd.read_csv(file)

        #Change types
        df['price'] = df['price'].str.replace('$', '', regex=False)
        df['price'] = df['price'].str.replace(',', '', regex=False)
        df['price'] = df['price'].astype(float)

        #Feature Engineering
        df['city'] = region
        df['location'] = df['name'].str.extract(r'in (.+?) ·')

        #Filtering
        df_filtered = df[
            ['id', 'city', 'location', 'picture_url', 'listing_url', 'room_type', 'accommodates', 'price', 'beds', 'review_scores_rating', 'number_of_reviews', 'latitude',
       'longitude']
                (df['number_of_reviews'] > 0) &
                (df['review_scores_rating'] >= 4) &
                (df['number_of_reviews'] >= 50) &
                (df['accommodates'] > 4) &
                (df['accommodates'] < 7) &
                (df['beds'] >= 4)
                ]
        
        dfs.append(df_filtered)

    listings_df = pd.concat(dfs, ignore_index=True)

    return listings_df

def main():
    files_and_regions = [
        (LISTINGS_SAN_DIEGO, 'San Diego'),
        (LISTINGS_LOS_ANGELES, 'Los Angeles'),
        (LISTINGS_BROWARD, 'Broward'),
        (LISTINGS_RIO_DE_JANEIRO, 'Rio de Janeiro'),
        (LISTINGS_SANTIAGO, 'Santiago'),
        (LISTINGS_BELIZE, 'Belize')
    ]

    listings_df = transform_listings_data(files_and_regions)
    listings_df.to_csv('snowbird-destinations/2_curated_layer/listings.csv', index=False)

if __name__ == "__main__":
    main()