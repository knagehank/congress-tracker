import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import pdfplumber  # pip install pdfplumber

HOUSE_URL = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure"

def get_latest_files():
    """ Finder links til seneste PDF-rapporter. """
    resp = requests.get(HOUSE_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')

    pdf_links = []

    # (Eksempel) Finder alle <a> tags med .pdf i linket
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith('.pdf'):
            # Bygger fuld URL, hvis linket er relativt
            if not href.startswith('http'):
                full_url = "https://disclosures-clerk.house.gov" + href
            else:
                full_url = href

            pdf_links.append(full_url)

    # Returnerer en liste af PDF-links (i praksis kan du filtrere yderligere)
    return pdf_links

def parse_file(file_url):
    """ Downloader en PDF og udtrækker handler (pseudo-kode). """
    # 1) Download PDF'en
    pdf_content = requests.get(file_url).content

    trades = []
    # 2) Åbn PDF'en med pdfplumber
    with pdfplumber.open(bytearray(pdf_content)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # 3) Gennemgå text, find linjer med aktiehandler
            # F.eks. noget med Ticker, "Purchase/Sale", beløb, datoer
            for line in text.split('\n'):
                # Her skal du definere en logik, der finder det, du har brug for
                if "BUY" in line or "PURCHASE" in line or "SELL" in line:
                    # Eksempel: parse evt. ticker og beløb
                    trades.append({
                        "url": file_url,
                        "line": line
                    })

    return trades

def update_csv(parsed_data):
    """ Gem de nye fund i data.csv (uden dubletter). """
    import csv
    import os

    csv_file = "data.csv"
    # Opret fil, hvis den ikke findes, og skriv header
    file_exists = os.path.isfile(csv_file)

    # Vi åbner CSV i append-mode
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Hvis filen ikke fandtes i forvejen, så skriv header
        if not file_exists:
            writer.writerow(["url", "line"])  # Tilpas kolonner

        # Lægger data ind
        for row in parsed_data:
            writer.writerow([row["url"], row["line"]])

def main():
    # 1) Hent liste af seneste PDF-links
    pdf_links = get_latest_files()

    # 2) For hvert link, parse og udtræk handler
    for link in pdf_links:
        trades = parse_file(link)
        # 3) Gem resultatet
        update_csv(trades)

if __name__ == "__main__":
    main()
