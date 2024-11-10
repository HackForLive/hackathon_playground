import pathlib

from genai_hackathon.services.sqlite_db_service import FinancialReportDbManager
from genai_hackathon import vector_db_path

root_dir = pathlib.Path(__file__).parent.parent
vector_db_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    db_manager = FinancialReportDbManager(sqlite_db_path=vector_db_path)
    
    companies = [
        ('Goldman Sachs', 'Finance'),
        ('Pfizer', 'Pharmacy'),
        ('ExxonMobil', 'Oil and Gas'),
        ('Toyota', 'Manufacturing'),
        ('Walmart', 'Retail'),
        ('Intel', 'Technology'),
        ('NVidia', 'Technology'),
        ('AMD', 'Technology'),
    ]
    for name, sector in companies:
        db_manager.upsert_company(company_name=name, sector=sector)
    
    print(db_manager.get_all_companies())
