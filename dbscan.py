import seaborn as sns
import pandas as pd
import math
import pandas as pd

# cekirdek veri noktasini bulacak fonksiyon


def cekirdek_bul(renk):
    for n in range(0, len(renk)):
        # eger noise veri noktasiysa cekirdek olamaz
        if renk[n] == -1:
            continue
        # eger renk degeri verilmemisse cekirdek olabilir
        if renk[n] == 0:
            return n
    return -1


def dbscan2D(dizi, cap, min_nokta):

    uzunluk = dizi['x'].count()
    # renk degerlerini belirten array
    renk = [0 for k in range(0, uzunluk)]
    # cekirdek veri noktasinin kontrol edilip edilmedigini gosteren array
    kontrol_edildi = [0 for k in range(0, uzunluk)]
    # veri noktasinin cekirdek veri noktasi olup olmadigini belirten array
    cekirdek_degil = [False for k in range(0, uzunluk)]
    # baslangictaki renk degeri
    bas_renk = 1

    # noise veri noktalarini bulup -1 renk degeriyle isaretleyip cekirdek
    # veri noktasi olmadigini isaretleyen dongu
    for n in range(0, uzunluk):

        # belirtilen cap verisiyle  n indeksli noktanin etrafinda
        # olan veri noktalarinin sayisini tutan degisken

        sayac = 0

        # n noktasinin etrafindaki degerleri sayan dongu
        # metrik olarak oklidyen uzaklik kullanilmistir
        for k in range(0, uzunluk):
            # x uzakligi
            uzaklik_x = dizi['x'][n] - dizi['x'][k]
            # y uzakligi
            uzaklik_y = dizi['y'][n] - dizi['y'][k]
            # oklidyen uzaklik
            nokta_uzaklik = math.sqrt(
                uzaklik_x*uzaklik_x + uzaklik_y*uzaklik_y)
            # eger uzaklik captan kucukse etrafinda demektir
            if nokta_uzaklik <= cap:
                # etrafindaki nokta sayisi 1 arttirilir
                sayac = sayac + 1
        # n indeksli noktanin etrafindaki nokta sayisi minimum nokta
        # parametresinden kucukse nokta cekirdek veri noktasi olamaz ayrica
        # simdilik noise noktasi olarak -1 renk degeri verilir
        if sayac < min_nokta:
            cekirdek_degil[n] = True
            renk[n] = -1

    # cekirdek veri noktalariyla kumeleme yapacak dongu
    while 1:
        # cekirdek indeksi degiskene atanir
        cekirdek_indeksi = cekirdek_bul(renk)
        # eger cekirdek bulunamadiysa kumeleme tamamlanmistir
        if cekirdek_indeksi < 0:
            break
        # dongu dizisi basta secilen cekirdek degerin etrafindaki degerleri
        # belirtir ve anlamsal olarak onlar da birer cekirdek noktasidir

        # simdilik baslangic noktasi olarak secilen cekirdek noktasinin indeksi
        # secilir
        dongu_dizisi = [cekirdek_indeksi]
        # noktanin kontrol edilip edilmedigini belirten dizi
        kontrol_edildi[cekirdek_indeksi] = 1
        # renk degeri baslangic renk degeri olarak verilir
        renk[cekirdek_indeksi] = bas_renk
        # dongu cekirdek belirli kume dahilindeki cekirdek noktalari
        # var oldugu surece doner, eger cekirdek nokta yoksa baska bir kumeye gecer
        while len(dongu_dizisi) > 0:
            # dongu dizisi dahilindeki degerler cekirdek noktasi olup
            # bu degerlerin de etrafindaki degerler kontrol edilir
            for m in dongu_dizisi:
                dongu_dizisi = []
                for k in range(uzunluk):
                    # eger deger kontrol edildiyse yani dongu dizisinin icine girdiyse bir daha
                    # kontrol edilmez
                    if kontrol_edildi[k] != 1:
                        uzaklik_x = dizi['x'][m] - dizi['x'][k]
                        uzaklik_y = dizi['y'][m] - dizi['y'][k]
                        nokta_uzaklik = math.sqrt(
                            uzaklik_x*uzaklik_x + uzaklik_y*uzaklik_y)
                        # eger nokta uzaklik captan kucuk ve 0 a esit degilse yani kendisi degilse
                        if nokta_uzaklik <= cap and nokta_uzaklik != 0:
                            # bu noktanin rengi cekirdek noktasinin rengi olur
                            renk[k] = bas_renk
                            # eger cekirdek noktasi olup kontrol edilmediyse
                            if not cekirdek_degil[k] and kontrol_edildi[k] != 1:
                                # kontrol edildi olarak isaretlenir
                                kontrol_edildi[k] = 1
                                # dongu dizisine eklenir
                                dongu_dizisi.append(k)
        # baska bir kumeye gecildigi icin renk degeri 1 arttirilir
        bas_renk = bas_renk+1
    return renk


# csv dosyasi okunur
url = './2Dcluster.csv'
df = pd.read_csv(url)
# color sutunu silinir
features = df.drop(['color'], axis=1)


results = features.copy()
results['Clusters'] = dbscan2D(features, 60, 37)

print(results['Clusters'])


# kumeleme seabor kutuphanesi yardimiyla gorsellestirilir
sns.pairplot(results, hue='Clusters', palette='Dark2')
