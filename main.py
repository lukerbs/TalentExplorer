from dotenv import load_dotenv
import os

from src.util import build_driver, wait

# Initialize Chrome Driver
driver = build_driver()

# Load LinkedIn Username and Password
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# link to the "People" tab of company profile page 
COMPANY_PROFILE_URL = "https://www.linkedin.com/company/endavanorthamerica/people/"