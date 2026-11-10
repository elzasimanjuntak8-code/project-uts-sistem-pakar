import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Sistem Pakar Penyakit Demam",
    page_icon="🩺",
    layout="wide"
)

# ============================================================
# BASIS PENGETAHUAN: 30 GEJALA SESUAI SOAL UTS
# ============================================================
GEJALA = {
    "G01": "Demam",
    "G02": "Demam tinggi",
    "G03": "Demam naik turun",
    "G04": "Menggigil",
    "G05": "Berkeringat berlebihan",
    "G06": "Sakit kepala",
    "G07": "Nyeri di belakang mata",
    "G08": "Nyeri otot",
    "G09": "Nyeri sendi",
    "G10": "Tubuh terasa lemas",
    "G11": "Nafsu makan menurun",
    "G12": "Mual",
    "G13": "Muntah berulang",
    "G14": "Nyeri perut hebat",
    "G15": "Diare",
    "G16": "Sembelit",
    "G17": "Batuk",
    "G18": "Pilek",
    "G19": "Sakit tenggorokan",
    "G20": "Sesak nafas berat",
    "G21": "Nyeri dada",
    "G22": "Ruam merah pada kulit",
    "G23": "Mata merah",
    "G24": "Bintik putih dalam mulut",
    "G25": "Nyeri saat buang air kecil",
    "G26": "Sering buang air kecil",
    "G27": "Nyeri pinggang",
    "G28": "Hilang penciuman/pengecapan",
    "G29": "Pendarahan dari hidung/gusi",
    "G30": "Penurunan kesadaran",
}

# Format aturan: kode, nama kesimpulan, daftar fakta/gejala, kode kesimpulan
ATURAN = [
    ("R01", "Influenza", ["G01", "G06", "G08", "G17"], "indikasi_influenza"),
    ("R02", "Influenza", ["G01", "G17", "G18", "G19"], "indikasi_influenza"),
    ("R03", "COVID-19", ["G01", "G17", "G19", "G28"], "indikasi_covid19"),
    ("R04", "COVID-19", ["G01", "G08", "G10", "G28"], "indikasi_covid19"),
    ("R05", "DBD", ["G02", "G06", "G07", "G08"], "indikasi_dbd"),
    ("R06", "DBD", ["G02", "G09", "G12", "G22"], "indikasi_dbd"),
    ("R07", "DBD", ["G01", "G07", "G09", "G22"], "indikasi_dbd"),
    ("R08", "Demam tifoid", ["G01", "G06", "G10", "G11", "G14"], "indikasi_tifoid"),
    ("R09", "Demam tifoid", ["G01", "G12", "G14", "G15"], "indikasi_tifoid"),
    ("R10", "Demam tifoid", ["G01", "G11", "G14", "G16"], "indikasi_tifoid"),
    ("R11", "Malaria", ["G01", "G04", "G05", "G06"], "indikasi_malaria"),
    ("R12", "Malaria", ["G03", "G04", "G05", "G08"], "indikasi_malaria"),
    ("R13", "ISK", ["G01", "G25", "G26"], "indikasi_isk"),
    ("R14", "ISK", ["G01", "G25", "G27", "G10"], "indikasi_isk"),
    ("R15", "Pneumonia", ["G01", "G17", "G20", "G21"], "indikasi_pneumonia"),
    ("R16", "Pneumonia", ["G02", "G17", "G20", "G10"], "indikasi_pneumonia"),
    ("R17", "Campak", ["G01", "G17", "G18", "G22", "G23"], "indikasi_campak"),
    ("R18", "Campak", ["G01", "G22", "G23", "G24"], "indikasi_campak"),
    ("R19", "Peringatan perdarahan", ["G01", "G29"], "peringatan_perdarahan"),
    ("R20", "Peringatan tanda bahaya", ["G01", "G13", "G14"], "peringatan_tanda_bahaya"),
    ("R21", "Peringatan darurat", ["G01", "G30"], "peringatan_darurat"),
    ("R22", "Peringatan darurat", ["G01", "G20"], "peringatan_darurat"),
]

# Tiga skenario wajib untuk pengujian/demonstrasi
SKENARIO = {
    "Skenario 1 — Influenza": ["G01", "G06", "G08", "G17"],
    "Skenario 2 — DBD": ["G02", "G06", "G07", "G08"],
    "Skenario 3 — Malaria": ["G01", "G04", "G05", "G06"],
}

def forward_chaining(fakta_awal):
    """
    Mesin inferensi Forward Chaining.
    Fakta awal adalah gejala yang dipilih pengguna.
    Aturan dijalankan jika seluruh premis/IF ada dalam kumpulan fakta.
    Kesimpulan/THEN ditambahkan sebagai fakta baru.
    Proses diulang sampai tidak ada fakta baru.
    """
    fakta = set(fakta_awal)
    aturan_terpenuhi = []
    kesimpulan = set()
    langkah = []
    iterasi = 1

    while True:
        ada_fakta_baru = False
        langkah.append(f"Iterasi {iterasi}: memeriksa basis aturan.")
        for kode, nama, premis, hasil in ATURAN:
            if set(premis).issubset(fakta) and kode not in [x[0] for x in aturan_terpenuhi]:
                aturan_terpenuhi.append((kode, nama, premis, hasil))
                langkah.append(
                    f"{kode} terpenuhi karena semua gejala "
                    f"{', '.join(premis)} tersedia. THEN: {hasil}."
                )
                if hasil not in fakta:
                    fakta.add(hasil)
                    kesimpulan.add(nama)
                    ada_fakta_baru = True
                    langkah.append(f"Fakta baru ditambahkan: {hasil}.")
                else:
                    kesimpulan.add(nama)
        if not ada_fakta_baru:
            langkah.append("Tidak ada fakta baru; proses inferensi berhenti.")
            break
        iterasi += 1

    return aturan_terpenuhi, sorted(kesimpulan), langkah

def format_gejala(kode_list):
    return [f"{kode} — {GEJALA[kode]}" for kode in kode_list if kode in GEJALA]

st.title("🩺 Sistem Pakar Identifikasi Penyakit dengan Gejala Demam")
st.caption("Implementasi Python + Streamlit menggunakan algoritma Forward Chaining")
st.warning(
    "Catatan: aplikasi ini merupakan simulasi akademik berdasarkan aturan pada soal UTS, "
    "bukan alat diagnosis medis. Hasilnya hanya indikasi awal dan tidak menggantikan pemeriksaan tenaga kesehatan."
)

with st.sidebar:
    st.header("Pengaturan Pengujian")
    mode = st.radio("Pilih mode input", ["Pilih skenario pengujian", "Pilih gejala manual"])
    st.markdown("---")
    st.write("**Algoritma:** Forward Chaining")
    st.write(f"**Jumlah gejala:** {len(GEJALA)}")
    st.write(f"**Jumlah aturan:** {len(ATURAN)}")

st.subheader("1. Input gejala")
if mode == "Pilih skenario pengujian":
    pilihan_skenario = st.selectbox("Pilih salah satu skenario", list(SKENARIO.keys()))
    gejala_terpilih = SKENARIO[pilihan_skenario]
    st.info("Gejala pada skenario ini telah dipilih otomatis. Kamu juga dapat melihat rinciannya di bawah.")
    st.write("**Gejala terpilih:**")
    for item in format_gejala(gejala_terpilih):
        st.write(f"- {item}")
else:
    st.write("Pilih semua gejala yang dialami. Kamu dapat memilih lebih dari satu.")
    opsi = [f"{kode} — {nama}" for kode, nama in GEJALA.items()]
    pilihan = st.multiselect("Daftar gejala", opsi, placeholder="Ketik kode atau nama gejala...")
    gejala_terpilih = [item.split(" — ")[0] for item in pilihan]

if st.button("🔍 Proses Forward Chaining", type="primary", use_container_width=True):
    if not gejala_terpilih:
        st.error("Pilih minimal satu gejala terlebih dahulu.")
    else:
        aturan_terpenuhi, hasil, langkah = forward_chaining(gejala_terpilih)
        st.session_state["hasil_inferensi"] = {
            "gejala": gejala_terpilih,
            "aturan": aturan_terpenuhi,
            "hasil": hasil,
            "langkah": langkah,
        }

if "hasil_inferensi" in st.session_state:
    data = st.session_state["hasil_inferensi"]
    st.markdown("---")
    st.subheader("2. Gejala yang dipilih")
    st.write(", ".join(format_gejala(data["gejala"])))

    st.subheader("3. Aturan yang berhasil dipenuhi")
    if data["aturan"]:
        for kode, nama, premis, hasil in data["aturan"]:
            with st.expander(f"{kode} — {nama}", expanded=True):
                st.write("**IF:** " + " AND ".join(premis))
                st.write("**Gejala:** " + ", ".join(GEJALA[g] for g in premis))
                st.write(f"**THEN:** `{hasil}`")
    else:
        st.info("Tidak ada aturan yang seluruh gejalanya terpenuhi. Sistem belum dapat menghasilkan kesimpulan berdasarkan basis aturan.")

    st.subheader("4. Hasil kesimpulan sistem")
    if data["hasil"]:
        for nama in data["hasil"]:
            if nama.startswith("Peringatan"):
                st.error(f"⚠️ {nama}")
            else:
                st.success(f"Indikasi: **{nama}**")
    else:
        st.info("Belum ditemukan indikasi penyakit dari aturan yang tersedia.")

    st.subheader("5. Tahapan proses inferensi (Forward Chaining)")
    for nomor, tahap in enumerate(data["langkah"], start=1):
        st.write(f"{nomor}. {tahap}")

    with st.expander("Lihat fakta akhir sistem"):
        st.write("Fakta awal (gejala):", ", ".join(data["gejala"]))
        st.write("Aturan aktif:", ", ".join(x[0] for x in data["aturan"]) or "Tidak ada")
        st.write("Kesimpulan:", ", ".join(data["hasil"]) or "Tidak ada")

st.markdown("---")
st.subheader("Informasi metode")
st.markdown(
    """
    **Forward Chaining** adalah metode penalaran yang dimulai dari fakta awal
    (gejala yang dipilih pengguna), kemudian memeriksa aturan IF–THEN.
    Jika seluruh kondisi IF pada suatu aturan terpenuhi, bagian THEN menjadi
    fakta/kesimpulan baru. Proses diulang sampai tidak ada fakta baru yang dapat ditambahkan.
    """
)
st.caption("Basis pengetahuan dan aturan R01–R22 mengikuti dokumen UTS Praktik Artificial Intelligence.")
