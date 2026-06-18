import streamlit as st
import joblib
import pandas as pd
import numpy as np

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Credit Scoring System", 
    page_icon="💳", 
    layout="centered"
)

# ==============================================================================
# 2. LOAD COMPONENT MACHINE LEARNING
# ==============================================================================
@st.cache_resource
def load_models():
    try:
        model = joblib.load('model/model_lr.joblib')
        scaler = joblib.load('model/robust_scaling.joblib')
        return model, scaler
    except Exception as e:
        st.error(f"Gagal memuat model/scaler: {e}")
        return None, None

model, scaler = load_models()

# ==============================================================================
# 3. HEADER APLIKASI (PORTAL PETUGAS BANK)
# ==============================================================================
st.title("💳 Credit Risk Scoring Portal")
st.markdown("### Internal Credit Officer Dashboard")
st.markdown("Formulir penilaian kelayakan kredit calon nasabah untuk petugas analisis risiko.")
st.divider()

# ==============================================================================
# 4. FORMULIR INPUT SINGLE-PAGE (DIBAGI 2 KOLOM KIRI-KANAN)
# ==============================================================================
col1, col2 = st.columns(2)

# ==============================================================================
# 4. FORMULIR INPUT SINGLE-PAGE (SUDAH DIKOREKSI LOGIKANYA)
# ==============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 👤 Profil & Finansial Nasabah")
    loan_amnt = st.number_input("Nominal Pinjaman yang Diajukan ($)", min_value=0, value=15000, step=500)
    annual_inc = st.number_input("Pendapatan Tahunan ($)", min_value=0, value=55000, step=1000)
    dti = st.number_input("Rasio Utang terhadap Pendapatan (DTI %)", min_value=0.0, max_value=100.0, value=15.0, step=0.1)
    home_ownership = st.selectbox("Status Kepemilikan Rumah", options=["RENT", "MORTGAGE", "OWN"])
    purpose = st.selectbox("Tujuan Utama Pinjaman", options=["debt_consolidation", "credit_card", "home_improvement", "other"])
    emp_length_years = st.slider("Lama Bekerja (Tahun)", min_value=0, max_value=10, value=5)

with col2:
    st.markdown("#### 🏢 Parameter Internal Bank")
    installment = st.number_input("Nilai Angsuran Bulanan ($)", min_value=0, value=350, step=10)
    int_rate = st.slider("Tingkat Suku Bunga Pinjaman (%)", min_value=0.0, max_value=30.0, value=12.5, step=0.1)
    term_months = st.selectbox("Tenor Pinjaman", options=[36, 60], format_func=lambda x: f"{x} Bulan")
    grade_input = st.selectbox("Grade Risiko Hasil Screening Awal", options=["A", "B", "C", "D", "E", "F", "G"])
    list_status = st.selectbox("Initial List Status", options=["F", "W"])
    verification_status = st.selectbox("Status Verifikasi Berkas", options=["Verified", "Not Verified"])

# ==============================================================================
# 5. TOMBOL SUBMIT TUNGGAL (DI PALING BAWAH HALAMAN)
# ==============================================================================
st.divider()

if st.button("📊 Hitung Kelayakan & Skor Kredit", type="primary", use_container_width=True):
    if model is not None and scaler is not None:
        
        # --- MAPPING DATA KATEGORIKAL ---
        home_rent = 1 if home_ownership == "RENT" else 0
        home_mortgage = 1 if home_ownership == "MORTGAGE" else 0
        
        mapping_grade = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}
        grade_angka = mapping_grade.get(grade_input, 4)
        
        initial_list_status_w = 1 if list_status == "W" else 0
        initial_list_status_f = 1 if list_status == "F" else 0
        is_verified = 1 if verification_status == "Verified" else 0

        # --- PENYUSUNAN 19 FITUR EKSURAN MODEL ---
        combined_data = {
            'int_rate': int_rate,
            'grade': grade_angka,
            'annual_inc': annual_inc,
            'inq_last_6mths': 1,  
            'dti': dti,
            'revol_util': 40.0,   
            'installment': installment,
            'revol_bal': 5000.0,  
            'term_months': term_months,
            'loan_amnt': loan_amnt,
            'total_acc': 15,      
            'initial_list_status_w': initial_list_status_w,
            'initial_list_status_f': initial_list_status_f,
            'open_acc': 8,         
            'verification_status_verified': is_verified,
            'home_ownership_rent': home_rent,
            'home_ownership_mortgage': home_mortgage,
            'purpose_small business': 1 if purpose == "other" else 0,
            'emp_length_years': emp_length_years
        }
        
        # Transformasi ke Dataframe dan kunci urutan kolom
        data_input = pd.DataFrame([combined_data])
        urutan_kolom = [
            'int_rate', 'grade', 'annual_inc', 'inq_last_6mths', 'dti', 'revol_util', 'installment', 
            'revol_bal', 'term_months', 'loan_amnt', 'total_acc', 'initial_list_status_w', 
            'initial_list_status_f', 'open_acc', 'verification_status_verified', 'home_ownership_rent', 
            'home_ownership_mortgage', 'purpose_small business', 'emp_length_years'
        ]
        data_input = data_input[urutan_kolom]
        
        # Robust Scaling dan Prediksi Risiko
        data_scaled = scaler.transform(data_input)
        probabilitas_gagal = float(model.predict_proba(data_scaled)[0][1])
        prediksi_kelas = int(model.predict(data_scaled)[0])
        
        # --- OUTPUT VISUALISASI HASIL ---
        st.subheader("📢 Hasil Analisis Risiko Aplikasi Kredit")
        st.metric(label="Probabilitas Gagal Bayar (Risk Score)", value=f"{probabilitas_gagal * 100:.2f}%")
        
        if prediksi_kelas == 1 or probabilitas_gagal > 0.45:  
            st.error("🚨 KEPUTUSAN: PINJAMAN DITOLAK (High Risk)")
            st.markdown("Kombinasi data finansial nasabah dan parameter internal dinilai **terlalu berisiko** bagi portofolio bank.")
        else:
            st.success("✅ KEPUTUSAN: PINJAMAN DISETUJUI (Low Risk)")
            st.markdown("Aplikasi memenuhi standar mitigasi risiko perusahaan dan layak diberikan pembiayaan.")
            
    else:
        st.error("Sistem error: Komponen Machine Learning gagal dimuat.")