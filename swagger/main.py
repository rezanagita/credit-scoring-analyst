from fastapi import FastAPI, HTTPException
from schemas import CreditScoringRequest
import pandas as pd
import numpy as np
import joblib
import os 

app = FastAPI(
    title="Lending Loan Credit Scoring API",
    description="API untuk memprediksi risiko gagal bayar (bad loan) menggunakan Logistic Regression",
    version="1.0.0"
)

try:
    model = joblib.load('model/model_lr.joblib')
    scaler = joblib.load('model/robust_scaling.joblib')
except Exception as e:
    raise RuntimeError(f"Error loading model or scaler: {e}")

# fitur default
fitur_sistem_backend ={
    'initial_list_status_w': 1, # pinjaman dibayari oleh 1 investor
    'initial_list_status_f': 0 # pinjaman didanai oleh banyak investor
}

@app.get("/")
def read_root():
    return{"status": "Aman", "message":"API Credit Scoring"}

@app.post("/predict")
def predict_credit(payload: CreditScoringRequest):
    try:
        data_debitur = payload.debitur.model_dump()
        data_company = payload.perusahaan.model_dump()

        # validasi input tenor
        if data_debitur['term_months'] not in [36,60]:
            raise HTTPException(status_code=400, detail="Tenor pinjaman harus 36 atau 60 bulan")
        #kembalikan jdul filter ke fotmat asli 
        data_debitur['purpose_small business'] = data_debitur.pop('purpose_small_business')

        #menggabungkan semua fitur
        combined_data = {**data_debitur, **data_company, **fitur_sistem_backend}
        data_input = pd.DataFrame([combined_data])

        # pastikan urutan fitur sesuai dengan yang digunakan saat pelatihan model
        urutan_kolom = [
            'int_rate', 'grade', 'annual_inc', 'inq_last_6mths', 'dti', 'revol_util', 'installment', 
            'revol_bal', 'term_months', 'loan_amnt', 'total_acc', 'initial_list_status_w', 
            'initial_list_status_f', 'open_acc', 'verification_status_verified', 'home_ownership_rent', 
            'home_ownership_mortgage', 'purpose_small business', 'emp_length_years'
        ]
        data_input = data_input[urutan_kolom]
        data_scaled = scaler.transform(data_input)

        # peluang prediksi
        peluang_gagal_bayar = float(model.predict_proba(data_scaled)[0][1])
        status_prediksi = int(model.predict(data_scaled)[0])

        return {
            "peluang_gagal_bayar(%)": round(peluang_gagal_bayar * 100, 2),
            "status_kode": status_prediksi,
            "rekomendasi_sistem": "TOLAK PINJAMAN" if status_prediksi ==1 else "TERIMA PINJAMAN"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses prediksi: {str(e)}")