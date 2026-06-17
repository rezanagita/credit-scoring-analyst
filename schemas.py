from pydantic import BaseModel, Field

class DataDebitur(BaseModel):
    loan_amnt: float # jumlah pinjaman yang diajukan
    annual_inc: float # pendapatan tahunan peminjam
    term_months: int = Field(..., description="Pilihan tenor pinjaman: 36 atau 60 bulan")
    emp_length_years:int # lama bekerja dalam tahun
    dti : float # rasio utang terhadap pendapatan
    purpose_small_business: int # tujuan pinjaman untuk usaha kecil (1 jika ya, 0 jika tidak)
    home_ownership_rent: int # status kepemilikan rumah menyewa/kontrak (1 jika ya, 0 jika tidak)

class DataInternal(BaseModel):
    int_rate: float #penentuan suku bunga
    grade: int #kelas risiko hasil scoring awal (1=A s.d 7=G)
    total_acc: int = Field(..., description="Pilihan tenor pinjaman: 36 atau 60 bulan")
    inq_last_6mths: int #jumlah pengecekan perusahaan 6 bulan terakhir
    revol_util: float #rasio pemakaian limit kartu kredit saat ini
    installment: float #jumlah cicilan bulanan yang harus dibayar peminjam
    revol_bal: float #Total saldo tagihan kartu kredit berjalan
    open_acc: int #jumlah akun kredit terbuka yang dimiliki peminjam
    verification_status_verified: int #status verifikasi pendapatan oleh tim analis (1 jika terverifikasi, 0 jika tidak)
    home_ownership_mortgage: int #status kepemilikan rumah kpr (1 jika ya, 0 jika tidak)

class CreditScoringRequest(BaseModel):
    debitur: DataDebitur
    perusahaan : DataInternal