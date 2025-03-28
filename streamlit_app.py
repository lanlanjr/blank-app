# streamlit_app.py  
# from dotenv import load_dotenv      # for local dev
import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# Load environment variables from .env file
# load_dotenv()   # for local dev

# Get database credentials from environment variables
db_config = {
    'dialect': st.secrets['database']['dialect'],
    'host': st.secrets['database']['host'],
    'port': st.secrets['database']['port'],
    'database': st.secrets['database']['database'],
    'username': st.secrets['database']['username'],
    'password': st.secrets['database']['password']
}



# # Get database credentials from environment variables
# db_config = {
#     'dialect': os.getenv('dialect'),
#     'host': os.getenv('host'),
#     'port': os.getenv('port'),
#     'database': os.getenv('database'),
#     # 'username': os.getenv('username'),
#     'username': 'root',
#     'password': os.getenv('password')
# }

st.write(db_config)

# Create database connection string
connection_string = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Initialize SQLAlchemy engine
engine = create_engine(connection_string)

# Initialize Streamlit connection
conn = st.connection('mysql', type='sql', url=connection_string)

# Perform query
try:
    with engine.connect() as connection:
        # Use text() for SQLAlchemy queries
        query = text("SELECT * FROM mytable")
        result = connection.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        if not df.empty:
            for row in df.itertuples():
                st.write(f"{row.name} has a :{row.pet}:")
        else:
            st.warning("No data found in the table")
except Exception as e:
    st.error(f"Error executing query: {str(e)}")