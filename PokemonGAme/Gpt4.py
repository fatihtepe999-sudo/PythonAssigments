import pandas as pd

# Kullanıcıdan veri girişi alma
isimler = []
yaslar = []
meslekler = []

while True:
    isim = input("İsim (Çıkmak için 'q' ya da 'Q' tuşuna basın): ")
    if isim.lower() == 'q':
        break
    yas = int(input("Yaş: "))
    meslek = input("Meslek: ")

    isimler.append(isim)
    yaslar.append(yas)
    meslekler.append(meslek)

# Veri oluşturma
veri = {
    'Isim': isimler,
    'Yas': yaslar,
    'Meslek': meslekler
}

# Veri çerçevesini oluşturma
df = pd.DataFrame(veri)

# Veri çerçevesini ekrana yazdırma
print("\nOluşturulan Veri Çerçevesi:")
print(df)

# Veri çerçevesini CSV dosyasına kaydetme
dosya_adi = "veri.csv"
df.to_csv(dosya_adi, index=False)

print(f"\n'{dosya_adi}' adlı CSV dosyasına veriler kaydedildi.")
