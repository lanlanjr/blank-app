# streamlit_app.py
from dotenv import load_dotenv
import os
import streamlit as st
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
db_config = {
    'dialect': os.getenv('dialect'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
    'database': os.getenv('database'),
    # 'username': os.getenv('username'),
    'username': 'root',
    'password': os.getenv('password')
}

st.write(db_config)

# Create database connection string
connection_string = f"{db_config['dialect']}://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Initialize SQLAlchemy engine
engine = create_engine(connection_string)

# Initialize Streamlit connection
conn = st.connection('mysql', type='sql', url=connection_string)

# Perform query
df = conn.query('SELECT * from mytable;', ttl=600)

# Print results
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")