# Hareketin Hesabı: Mühendislik Dinamiği — kurs dosyaları

Forenly AI Academy'deki **Hareketin Hesabı: Mühendislik Dinamiği** kursunun laboratuvar dosyaları. Derslerde ekranda gördüğünüz her Python oturumu ve grafik bu betiklerle üretildi.

## Gerekenler

- **Python 3.10 veya üstü**, ve `numpy` (2.0 ya da üstü), `scipy`, `matplotlib`. Hepsi ücretsizdir.
- Kurulum: `python -m pip install -r requirements.txt`
- Bilgisayarınıza kurmak istemezseniz tarayıcıda çalışan bir not defterine (ör. Google Colab) bu klasörü yükleyip aynı betikleri çalıştırabilirsiniz.

## Nasıl çalıştırılır

1. Bu depoyu indirin (Code → Download ZIP) ve klasörde bir terminal açın.
2. Bir haftayı çalıştırın: `python hafta1.py` (`hafta2.py`, `hafta3.py`, `hafta4.py`). Her hafta bağımsızdır.
3. Betikler çalışınca `ekran/<ders>/` klasöründe grafikler (`.png`) ve Python oturum kayıtları (`.txt`), kökte de ölçülen sayılar (`OLCUMLER.json`) oluşur. Ders 4.4 ayrıca `cikti/bitirme_raporu.csv` yazar.
4. İsteğe bağlı: `python komut_ciz.py` oturum kayıtlarını derslerdeki gibi resme çizer.

Derslerdeki komutları kendiniz yazmak isterseniz `python` yazıp etkileşimli oturumu açın ve `ekran/<ders>/*.txt` dosyalarındaki satırları sırayla girin.

## Sonucunuzu karşılaştırın

`beklenen/OLCUMLER.json` ekibimizin 2026-10-06 koşumunda ölçtüğü sayılardır; `beklenen/ekran/` aynı koşumun grafikleri ve oturum kayıtlarıdır. Kendi `OLCUMLER.json` dosyanızla karşılaştırın. `beklenen/bitirme_raporu.csv` Ders 4.4'teki raporun ölçütleriyle sonucudur.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ortak.py` | Kaydı okuma (`kayit`), yumuşatma (`yumusat`), ölçüm yazma, oturum kaydı ve grafik kaydetme |
| `hafta1.py` | Parçacığın kinematiği: sayısal türev, sabit ivme ve Euler, teğetsel ve normal ivme, kutupsal koordinatlar |
| `hafta2.py` | Parçacığın kinetiği: gereken sürtünme, hava dirençli düşüş, yay–kütle–sönüm, sarkaçta ip gerilmesi |
| `hafta3.py` | Katı cisim: dirseğin dönmesi, krank–biyel, eylemsizlik momenti, dirsek torku |
| `hafta4.py` | İş, enerji ve momentum: iş–enerji ilkesi, enerjinin korunumu ve güç, çarpışma ve impuls, bitirme raporu (`bardak_raporu`) |
| `komut_ciz.py` | Oturum kayıtlarını resme çizer (isteğe bağlı, Pillow gerekir) |
| `veri/cay_servisi_kaydi.csv` | Çay servisi benzetim kaydı: zaman, omuz ve dirsek açıları, dirseğin açısal hızı, bardağın konumu × 5666 örnek (saniyede 50) |
| `veri/g1_sag_kol_kutle.csv` | Kolun parçaları: kütle ve eklemlere uzaklık (el kütlesi VARSAYIM) |
| `veri/g1_sag_kol_parametre.csv` | Eklem kartı: kazançlar, tork sınırı, yerçekimi katsayıları |

## Veri hakkında

Robot verisinin tamamı **benzetim kaydıdır**, gerçek robot ölçümü değildir. Kayıt, Forenly AI'nin [kafe projesinde](https://forenly.ai/work/cafe) Unitree G1 insansı robotunun çay servisini benzetimde yaptığı bir bölümden alınmıştır. Dirsek torku modeli basitleştirilmiştir: omuzun hareketi hesaba katılmaz. Kayıttan ya da robot tablolarından gelmeyen değerler (top, yay, sarkaç, krank, arabalar, bardak kütlesi, ölçütler) betiklerde ve derslerde **ÖRNEK** diye işaretlidir.

Dosyalar yalnız eğitim amacıyla paylaşılmıştır. © Forenly AI
