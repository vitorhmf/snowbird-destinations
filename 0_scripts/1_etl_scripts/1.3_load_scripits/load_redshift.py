import psycopg2

# Conexão ao Redshift
conn = psycopg2.connect(
    dbname='your_dbname', 
    user='your_user', 
    password='your_password', 
    port='your_port', 
    host='your_cluster_endpoint'
)
cur = conn.cursor()

# Truncate das tabelas (opcional)
cur.execute("TRUNCATE TABLE weather;")
cur.execute("TRUNCATE TABLE cities_metrics;")
cur.execute("TRUNCATE TABLE countries_metrics;")
cur.execute("TRUNCATE TABLE listings;")

# Comandos COPY para carregar os dados do S3
copy_sql = """
COPY {} FROM 's3://your_bucket_name/{}' 
CREDENTIALS 'aws_iam_role=your_iam_role' 
CSV IGNOREHEADER 1;
"""
tables_files = [
    ("weather", "weather.csv"),
    ("cities_metrics", "cities_metrics.csv"),
    ("countries_metrics", "countries_metrics.csv"),
    ("listings", "listings.csv")
]

for table, file in tables_files:
    cur.execute(copy_sql.format(table, file))

# Fechar a conexão
conn.commit()
cur.close()
conn.close()
