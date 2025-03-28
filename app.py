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
SHEET1_ID = "1cpzDf5mI1bm6U5JlfMvxolltI4Abrch2Ed4JQF4RoiA"  # Ganti dengan ID Sheet 1
SHEET2_ID = "1dqYlI9l6gKomfApHyWiWTTZK8Fb7K_yM7JHuw6dT6bM"  # Ganti dengan ID Sheet 2
SHEET1_NAME = "Sheet2"
SHEET2_NAME = "Sheet2"

@app.get("/search")
def search_data(
    query1: str = Query(None, description="Kata kunci untuk pencarian di Sheet 1"),
    query2: str = Query(None, description="Kata kunci untuk pencarian di Sheet 2")
):
    results = {}

    if query1:
        # Ambil data dari Sheet 1
        sheet1 = gc.open_by_key(SHEET1_ID).worksheet(SHEET1_NAME)
        data1 = sheet1.get_all_values()
        df1 = pd.DataFrame(data1[1:], columns=data1[0])

        # Filter pencarian berdasarkan kolom tertentu di Sheet 1
        relevant_columns1 = ["Kota Asal", "Kota Tujuan", "Tahun", "Bulan", "Provinsi Kota Asal", "Provinsi Kota Tujuan"]
        result1 = df1[df1[relevant_columns1].apply(lambda row: row.astype(str).str.contains(query1, case=False, na=False).any(), axis=1)]
        results["sheet1_results"] = result1.to_dict(orient="records")

    if query2:
        # Ambil data dari Sheet 2
        sheet2 = gc.open_by_key(SHEET2_ID).worksheet(SHEET2_NAME)
        data2 = sheet2.get_all_values()
        df2 = pd.DataFrame(data2[1:], columns=data2[0])

        # Filter pencarian berdasarkan kolom tertentu di Sheet 2
        relevant_columns2 = ["Negara", "3 Letter Code", "Nama PIC", "Nama Owner", "Nomor Owner", "Profesi Owner"]
        result2 = df2[df2[relevant_columns2].apply(lambda row: row.astype(str).str.contains(query2, case=False, na=False).any(), axis=1)]
        results["sheet2_results"] = result2.to_dict(orient="records")

    return results
