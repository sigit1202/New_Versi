from fastapi import FastAPI, Query
import pandas as pd
import gspread
from google.oauth2 import service_account

app = FastAPI()

# Autentikasi Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "service_account.json"  # Ganti dengan file JSON autentikasi Google

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

# ID Google Sheets (Ganti dengan ID sebenarnya)
SHEET1_ID = "your_sheet1_id"  # Ganti dengan ID Sheet 1
SHEET2_ID = "your_sheet2_id"  # Ganti dengan ID Sheet 2
SHEET1_NAME = "Sheet1"
SHEET2_NAME = "Sheet2"

@app.get("/search")
def search_data(query: str = Query(..., description="Masukkan kata kunci untuk pencarian")):
    # Ambil data dari Sheet 1 (Sheet ID 1)
    sheet1 = gc.open_by_key(SHEET1_ID).worksheet(SHEET1_NAME)
    data1 = sheet1.get_all_values()
    df1 = pd.DataFrame(data1[1:], columns=data1[0])

    # Ambil data dari Sheet 2 (Sheet ID 2)
    sheet2 = gc.open_by_key(SHEET2_ID).worksheet(SHEET2_NAME)
    data2 = sheet2.get_all_values()
    df2 = pd.DataFrame(data2[1:], columns=data2[0])

    # Filter data berdasarkan query (Pencarian di semua kolom)
    result1 = df1[df1.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]
    result2 = df2[df2.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]

    return {
        "sheet1_results": result1.to_dict(orient="records"),
        "sheet2_results": result2.to_dict(orient="records")
    }
