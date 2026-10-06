"""Hafta 4 · İş, Enerji ve Momentum — Ders 4.1–4.4 (4.4 bitirme).
  python hafta4.py   → ekran/4.x/*.txt + *.png, OLCUMLER.json (d4_*), cikti/bitirme_raporu.csv"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from ortak import LAB, kayit, yumusat, olc, oturum, sekil, g


def ders_4_1():
    """İş ve kinetik enerji ilkesi: yayla itilen, sürtünmeli yüzeyde kayan blok (ÖRNEK)."""
    ns = oturum("4.1", "is-enerji", """
import numpy as np
g = 9.81
k, x0, m, mu = 400.0, 0.10, 0.5, 0.3
x = np.linspace(-x0, 0, 1001)
W_yay = np.trapezoid(-k * x, x)
W_surt = -mu * m * g * x0
round(W_yay, 4), round(W_surt, 4)
v1 = np.sqrt(2 * (W_yay + W_surt) / m)
round(v1, 3)
d = v1**2 / (2 * mu * g)
round(d, 3), round(x0 + d, 3)
""")
    ns = oturum("4.1", "sayisal-sinama", """
from scipy.integrate import solve_ivp
def denklem(t, s):
    x, v = s
    F_yay = -k * x if x < 0 else 0.0
    return [v, (F_yay - mu * m * g) / m]
durdu = lambda t, s: s[1] if t > 0.01 else 1.0
durdu.terminal = True
cozum = solve_ivp(denklem, [0, 3], [-x0, 0], events=durdu, max_step=1e-4)
round(cozum.y_events[0][0][0] + x0, 3)
""", ns)
    k, x0 = 400.0, 0.10
    x = np.linspace(-x0, 0, 200)
    fig, ax = plt.subplots()
    ax.plot(x * 1000, -k * x, color="#1D4ED8", label="yay kuvveti  −k x")
    ax.fill_between(x * 1000, -k * x, color="#1D4ED8", alpha=0.18)
    ax.axhline(0.3 * 0.5 * 9.81, color="#C2410C", ls="--", label=f"sürtünme kuvveti  μ m g = {0.3 * 0.5 * 9.81:.2f} N")
    ax.text(-75, 12, f"alan = yayın işi\n{ns['W_yay']:.2f} J", fontsize=26, color="#1D4ED8")
    ax.set_xlabel("yayın sıkışması x (mm)"); ax.set_ylabel("kuvvet (N)"); ax.legend(loc="upper right")
    ax.set_title("İş = kuvvet–yol eğrisinin altındaki alan · 400 N/m, 0,5 kg, μ 0,3 (ÖRNEK)")
    sekil("4.1", "kuvvet-yol")
    olc(d4_1_W_yay=ns["W_yay"], d4_1_W_surt=ns["W_surt"], d4_1_v1=ns["v1"], d4_1_d=ns["d"], d4_1_toplam=ns["x0"] + ns["d"],
        d4_1_sayisal=ns["cozum"].y_events[0][0][0] + ns["x0"])


def ders_4_2():
    """Enerjinin korunumu ve güç: sarkaçta enerji, dirseğin gücü ve işi, bardağın potansiyel enerjisi."""
    ns = oturum("4.2", "enerji-korunumu", """
import numpy as np
from scipy.integrate import solve_ivp
g, m, L = 9.81, 0.5, 1.0
th0 = np.radians(60)
cozum = solve_ivp(lambda t, s: [s[1], -g / L * np.sin(s[0])], [0, 20], [th0, 0],
                  max_step=0.001, rtol=1e-9, atol=1e-9)
th, th_n = cozum.y
E = 0.5 * m * L**2 * th_n**2 + m * g * L * (1 - np.cos(th))
round(E[0], 4), f"{np.abs(E - E[0]).max() / E[0]:.1e}"
""")
    ns = oturum("4.2", "dirsek-gucu", """
from ortak import kayit, yumusat
k = kayit()
t, q, w = k["zaman_s"], k["dirsek_rad"], k["dirsek_hiz_rad_s"]
m3 = t > 3
tau = 0.0976 * np.gradient(yumusat(w), t) - (-2.998 * np.cos(q) + 0.145 * np.sin(q))
P = tau * w
round(np.abs(P[m3]).max(), 3)
dt = t[1] - t[0]
W_arti = (P[m3] * (P[m3] > 0)).sum() * dt
W_eksi = (P[m3] * (P[m3] < 0)).sum() * dt
round(W_arti, 3), round(W_eksi, 3)
z = k["bardak_z_m"]
dE_bardak = 0.2 * g * (z.max() - z[0])
round(z.max() - z[0], 3), round(dE_bardak, 3)
""", ns)
    t, P, m3 = ns["t"], ns["P"], ns["m3"]
    fig, ax = plt.subplots()
    ax.fill_between(t[m3], P[m3], where=P[m3] > 0, color="#0F766E", alpha=0.6, label=f"motor iş yapıyor  +{ns['W_arti']:.2f} J")
    ax.fill_between(t[m3], P[m3], where=P[m3] < 0, color="#C2410C", alpha=0.6, label=f"motor frenliyor  {ns['W_eksi']:.2f} J")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("güç  τ ω  (W)"); ax.legend(loc="upper left")
    ax.set_title("Dirseğin gücü · benzetim kaydı · basitleştirilmiş tork modeli (Ders 3.4)")
    sekil("4.2", "dirsek-gucu-grafik")
    E = ns["E"]
    olc(d4_2_E0=E[0], d4_2_sapma=float(np.abs(E - E[0]).max() / E[0]), d4_2_P_max=np.abs(P[m3]).max(),
        d4_2_W_arti=ns["W_arti"], d4_2_W_eksi=ns["W_eksi"], d4_2_dz=ns["z"].max() - ns["z"][0], d4_2_dE_bardak=ns["dE_bardak"])


def ders_4_3():
    """İmpuls, momentum ve çarpışma: geri sıçrama katsayısı (ÖRNEK) ve bardağın masaya konması (benzetim kaydı)."""
    ns = oturum("4.3", "carpisma", """
import numpy as np
m1, v1, m2, v2 = 1.0, 2.0, 2.0, 0.0
e = 0.6
v1_s = (m1 * v1 + m2 * v2 - m2 * e * (v1 - v2)) / (m1 + m2)
v2_s = (m1 * v1 + m2 * v2 + m1 * e * (v1 - v2)) / (m1 + m2)
round(v1_s, 4), round(v2_s, 4)
round(m1 * v1 + m2 * v2, 4), round(m1 * v1_s + m2 * v2_s, 4)
E_once = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
E_sonra = 0.5 * m1 * v1_s**2 + 0.5 * m2 * v2_s**2
round(E_once, 3), round(E_sonra, 3), round(1 - E_sonra / E_once, 3)
""")
    ns = oturum("4.3", "bardak-konma", """
from ortak import kayit
k = kayit()
t, z = k["zaman_s"], k["bardak_z_m"]
v_z = np.gradient(z, t)
j = np.flatnonzero((t > 85) & (z < 0.77))[0]
round(t[j], 2), round(v_z[j], 3)
m_b = 0.2
J_konma = m_b * abs(v_z[j])
J_dusme = m_b * np.sqrt(2 * 9.81 * 0.05)
round(J_konma, 4), round(J_dusme, 4), round(J_dusme / J_konma, 1)
""", ns)
    ee = np.linspace(0, 1, 101)
    kayip = []
    for e in ee:
        a = (2 - 2 * e * 2) / 3; b = (2 + e * 2) / 3
        kayip.append(1 - (0.5 * a ** 2 + b ** 2) / 2)
    fig, ax = plt.subplots()
    ax.plot(ee, 100 * np.array(kayip), color="#7E22CE")
    ax.plot(0.6, 100 * ns["E_sonra"] * 0 + 100 * (1 - ns["E_sonra"] / ns["E_once"]), "o", color="#C2410C", ms=18,
            label=f"e = 0,6  →  enerjinin %{100 * (1 - ns['E_sonra'] / ns['E_once']):.0f}'ü kayıp")
    ax.set_xlabel("geri sıçrama katsayısı e"); ax.set_ylabel("kaybolan kinetik enerji (%)"); ax.legend(loc="upper right")
    ax.set_title("Çarpışmada enerji kaybı · 1 kg, 2 m/s → duran 2 kg (ÖRNEK) · momentum her e için korunur")
    sekil("4.3", "enerji-kaybi")
    olc(d4_3_v1s=ns["v1_s"], d4_3_v2s=ns["v2_s"], d4_3_p=ns["m1"] * ns["v1"], d4_3_kayip=1 - ns["E_sonra"] / ns["E_once"],
        d4_3_t_konma=ns["t"][ns["j"]], d4_3_vz=ns["v_z"][ns["j"]], d4_3_J_konma=ns["J_konma"], d4_3_J_dusme=ns["J_dusme"])


def bardak_raporu(mu_tepsi=0.2, hiz_olcut=1.0, konma_olcut=0.1, tork_siniri=25.0):
    """Bitirme: bardağın yolculuğunu dört ölçütle sınar. Ölçütler ÖRNEK, tork sınırı eklem kartından."""
    k = kayit()
    t = k["zaman_s"]
    p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"], k["bardak_z_m"]]))
    v = np.gradient(p, t, axis=0)
    a = np.gradient(v, t, axis=0)
    mu = np.hypot(a[:, 0], a[:, 1]) / (g + a[:, 2])
    m3 = t > 3
    w, q = k["dirsek_hiz_rad_s"], k["dirsek_rad"]
    tau = 0.0976 * np.gradient(yumusat(w), t) - (-2.998 * np.cos(q) + 0.145 * np.sin(q))
    z = k["bardak_z_m"]
    j = np.flatnonzero((t > 85) & (z < 0.77))[0]
    v_konma = abs(np.gradient(z, t)[j])
    satir = [("bardağın en büyük hızı (m/s)", np.linalg.norm(v, axis=1).max(), hiz_olcut),
             ("gereken sürtünme katsayısı", mu.max(), mu_tepsi),
             ("dirseğin en büyük torku (N·m)", np.abs(tau[m3]).max(), tork_siniri),
             ("masaya konma hızı (m/s)", v_konma, konma_olcut)]
    return [(ad, round(float(d), 3), s, "GEÇTİ" if d < s else "KALDI") for ad, d, s in satir]


def ders_4_4():
    ns = oturum("4.4", "bitirme-raporu", """
from hafta4 import bardak_raporu
rapor = bardak_raporu()
for ad, deger, olcut, sonuc in rapor:
    print(f"{ad:32s} {deger:7.3f}  < {olcut:5.2f}   {sonuc}")
all(s == "GEÇTİ" for *_, s in rapor)
""")
    ns = oturum("4.4", "olcut-degisimi", """
rapor = bardak_raporu(mu_tepsi=0.1)
[(ad, sonuc) for ad, _, _, sonuc in rapor if sonuc == "KALDI"]
""", ns)
    rapor = bardak_raporu()
    (LAB / "cikti").mkdir(exist_ok=True)
    (LAB / "cikti/bitirme_raporu.csv").write_text("olcu,deger,olcut,sonuc\n" + "".join(f"{a},{d},{s},{r}\n" for a, d, s, r in rapor), encoding="utf-8")
    fig, ax = plt.subplots()
    oran = [d / s for _, d, s, _ in rapor]
    ax.barh([r[0] for r in rapor], oran, color=["#0F766E" if r[3] == "GEÇTİ" else "#C2410C" for r in rapor])
    ax.axvline(1, color="k", ls="--", lw=2); ax.text(1.02, -0.45, "ölçüt", fontsize=22)
    for k_, (r, o) in enumerate(zip(rapor, oran)):
        ax.text(max(o, 1) + 0.03, k_, f"{r[1]:g} / {r[2]:g}  {r[3]}", va="center")
    ax.set_xlim(0, 1.6); ax.invert_yaxis(); ax.set_xlabel("değer / ölçüt")
    ax.set_title("Bitirme · bardağın yolculuğu · ölçütler ÖRNEK, tork sınırı eklem kartından")
    sekil("4.4", "bitirme-ozet")
    olc(d4_4_rapor=[list(r) for r in rapor], d4_4_mu01=[a for a, _, _, s in bardak_raporu(mu_tepsi=0.1) if s == "KALDI"])


if __name__ == "__main__":
    for f in (ders_4_1, ders_4_2, ders_4_3, ders_4_4):
        f(); print(f.__name__, "tamam")
