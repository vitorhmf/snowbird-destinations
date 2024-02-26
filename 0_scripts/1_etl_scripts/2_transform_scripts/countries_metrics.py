import pandas as pd

BETTER_LIFE_INDEX = '1_raw/cities_metrics/better_life_index.csv'

def assign_group(indicator):
    if indicator in ['Feeling safe walking alone at night', 'Homicide rate']:
        return 'security'
    elif indicator in ['Air pollution', 'Water quality']:
        return 'environment'
    else:
        return 'people'

def transform_cities_metrics(filepath):
    df = pd.read_csv(filepath)

    # Filters
    indicators = (
        (df['Inequality'] == 'Total') &
        ~(df['Indicator'].isin([
            'Stakeholder engagement for developing regulations',
            'Rooms per person',
            'Housing expenditure',
            'Household net adjusted disposable income',
            'Personal earnings',
            'Student skills',
            'Years in education',
            'Employees working very long hours',
            'Long-term unemployment rate',
            'Quality of support network',
            'Voter turnout',
            'Dwellings without basic facilities',
            'Household net wealth',
            'Time devoted to leisure and personal care',
            'Self-reported health',
            'Labour market insecurity'
        ]))
    )

    countries = (
        df['Country'].isin(['Mexico', 'Brazil', 'Chile', 'United States'])
    )

    filters = indicators & countries

    df_filtered = df[['Country', 'Indicator', 'Unit', 'Value']][filters].reset_index(drop=True)
    df_filtered.columns = [col.lower() for col in df_filtered.columns]
    
    # Feature Engineer

    # Group Indicators
    df_filtered['group'] = df_filtered['indicator'].apply(assign_group)

    # Country Ranking
    df_filtered['rank'] = df_filtered.groupby('indicator')['value'].rank(method='dense', ascending=False)

    df_final = df_filtered[['group', 'indicator', 'country', 'unit', 'value', 'rank']]

    return df_final

def main():
    df_final = transform_cities_metrics(BETTER_LIFE_INDEX)
    df_final.to_csv('2_curated/cities_metrics.csv', index=False)

if __name__ == "__main__":
    main()
