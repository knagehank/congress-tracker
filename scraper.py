import requests

# Eksempel-URL (House Disclosure)
HOUSE_URL = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure"

def get_latest_files():
    # Hent og parse den side, der indeholder link til PDF/tekst
    # Returner evt. en liste af URL'er til nye filer

def parse_file(file_url):
    # Download PDF/tekst
    # Udpak data med fx pdfplumber
    # Gem i en liste af dicts, fx:
    # [{"name": "John Doe", "date": "2024-01-01", "ticker": "AAPL", "action": "BUY", "amount": 10000}, ...]

def update_csv(parsed_data):
    # Læg parsed data i en CSV-fil
    # Tjek om poster allerede findes i CSV for at undgå dubletter

if __name__ == "__main__":
    file_list = get_latest_files()
    for f_url in file_list:
        data = parse_file(f_url)
        update_csv(data)
