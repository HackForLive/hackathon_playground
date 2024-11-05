import sqlite3
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).parent
sql_db_dir = base_dir.parent / 'db' / 'sqlite_db'

excel_path = base_dir.parent / 'excel_data' / 'Global-Oil-and-Gas-Extraction-Tracker-March-2024.xlsx'

if __name__ == "__main__":
    conn = sqlite3.connect('database.db')

    main_df = pd.read_excel(excel_path, sheet_name='Main data')
    reserves_df = pd.read_excel(excel_path, sheet_name='Production & reserves')
    # Load data from Excel and save it in the SQLite database
    main_df.to_sql('global_oil_and_gas_main', conn, if_exists='replace', index=False)
    reserves_df.to_sql('global_oil_and_gas_reserves', conn, if_exists='replace', index=False)
    conn.close()