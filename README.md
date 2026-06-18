#  End-to-End Credit Risk Scoring Analysis & System

Aplikasi berbasis Machine Learning (Logistic Regression) yang dirancang untuk membantu *Credit Officer* (Internal Bank) dalam memprediksi risiko kelayakan kredit calon nasabah secara *real-time*, dilengkapi dengan dashboard analisis historis portofolio kredit.

---

## 📌 1. Deskripsi Proyek
Proyek ini menyelesaikan tantangan bisnis di sektor finansial peminjaman peer to peer dengan memitigasi risiko gagal bayar (*Non-Performing Loan/Bad Rate*). Sistem ini mengintegrasikan dua pendekatan utama:
1. **Analisis Historis (Descriptive Analytics):** Menggunakan Power BI Dashboard untuk mengaudit tren risiko dan performa pinjaman masa lalu.
2. **Sistem Prediksi Real-Time (Predictive Analytics):** Model Machine Learning yang dideploy ke platform cloud untuk membantu pengambilan keputusan kredit yang taktis.

---

## 🚀 2. Live Demo Aplikasi
Aplikasi ini di-deploy secara terpisah ke dalam dua arsitektur sistem (Backend Engine & Frontend Portal) pada Hugging Face Spaces:

* **💻 Interactive Web Portal (Streamlit UI):** [Link Portal UI Streamlit](https://credit-scoring-analyst.streamlit.app/) *(Dioptimalkan untuk kebutuhan bisnis dan operasional staf internal bank).*
* **⚙️ Production API Engine (FastAPI Swagger UI):** [Link API Swagger docs](https://rezanagit20-credit-scoring-api.hf.space/docs) *(Disediakan untuk kebutuhan integrasi sistem/B2B Developer via REST API).*
* **📊 Dashboard <img width="1799" height="1018" alt="Screenshot 2026-06-18 153230" src="https://github.com/user-attachments/assets/328340e0-ec44-4099-95f3-8523f05206f3" />**

---

## 📊 3. Dataset
Dataset yang digunakan dalam proyek ini berisikan data historis portofolio pinjaman yang mencakup profil personal keuangan serta parameter kebijakan internal perusahaan peminjaman. 

### **Fitur Utama yang Digunakan (19 Variabel):**
* **Profil Finansial Debitur:** `annual_inc` (Pendapatan Tahunan), `dti` (Rasio Utang terhadap Pendapatan), `home_ownership` (Status Rumah: Rent/Mortgage/Own), `emp_length_years` (Lama Bekerja), dan `purpose` (Tujuan Pinjaman).
* **Parameter Finansial & Kebijakan Bank:** `loan_amnt` (Nominal Pinjaman), `installment` (Angsuran Bulanan), `int_rate` (Suku Bunga), `term_months` (Tenor 36/60 Bulan), `grade` (Screning Awal Risiko), `verification_status` (Status Verifikasi), dan metadata transaksi lainnya (`revol_bal`, `revol_util`, `open_acc`, `total_acc`, `inq_last_6mths`, `initial_list_status`).

---

## 🛠️ 4. Informasi Struktur Repository
Repositori ini dikelola dengan struktur folder yang bersih untuk memisahkan logika pemrosesan data, penyimpanan model, dan antarmuka web:

```text
├── model/
│   ├── model_lr.joblib            # File binary model Logistic Regression teratih
│   └── robust_scaling.joblib       # File binary untuk normalisasi fitur numerik
├── app.py                         # File utama Web Portal menggunakan Streamlit SDK
├── main.py                        # File utama REST API menggunakan FastAPI Framework
├── requirements.txt               # Daftar dependensi pustaka Python yang dibutuhkan
├── swagger/
│   ├── main.py            # file utama aplikasi
│   └── schemas.py       # file data inputan
│   └──  Dockerfile      # Konfigurasi containerization untuk deployment cloud
```

---

## 📈 5. Hasil & Evaluasi Komparasi Model
Pengembangan model dilakukan dengan menguji 6 algoritma Machine Learning yang berbeda untuk menemukan model terbaik yang paling sensitif dalam mendeteksi nasabah berisiko gagal bayar (*Bad Loan*). 

Berikut adalah hasil evaluasi komparasi seluruh model berdasarkan data pengujian (*test set*):

| Nama Model | Accuracy | Recall (Bad Loan) | Precision (Bad Loan) | F1-Score (Bad Loan) | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **Logistic Regression** | **63.00%** | **63.00%** | **17.00%** | **27.00%** | **0.68** |
| 🌲 Random Forest | 71.00% | 48.00% | 19.00% | 27.00% | 0.67 |
| 🚀 XGBoost | 86.00% | 12.00% | 24.00% | 16.00% | 0.66 |
| 🌌 Naive Bayes | 58.00% | 66.00% | 16.00% | 26.00% | 0.66 |
| 📈 AdaBoost | 58.00% | 64.00% | 16.00% | 25.00% | 0.65 |
| 🌿 Decision Tree | 74.00% | 39.00% | 18.00% | 25.00% | 0.64 |

### **💡 Justifikasi Pemilihan Model Utama:**
Meskipun model kompleks seperti *XGBoost* menghasilkan nilai akurasi paling tinggi (86.00%), model tersebut memiliki nilai **Recall Bad Loan yang sangat rendah (12.00%)**, yang berarti ia meloloskan 88% nasabah yang berisiko macet. 

Dalam bisnis manajemen risiko kredit (*credit risk management*), meminimalkan kerugian akibat nasabah gagal bayar jauh lebih krusial daripada sekadar mengejar akurasi tinggi. Oleh karena itu, **Logistic Regression dipilih sebagai model produksi utama** karena berhasil memberikan performa paling optimal dan seimbang:
1. Memiliki **ROC-AUC tertinggi (0.68)** yang menunjukkan kemampuan pemisahan kelas risiko terbaik.
2. Memiliki **Recall (Bad Loan) sebesar 63.00%**, menjadikannya model yang jauh lebih aman dalam menyaring dan mengamankan portofolio kredit perusahaan dari potensi *Non-Performing Loan* (NPL).



