"""Hafta 3 · Katı Cismin Kinematiği ve Kinetiği — Ders 3.1–3.4.
  python hafta3.py   → ekran/3.x/*.txt + *.png, OLCUMLER.json (d3_*)
Dirsek verisi benzetim kaydından; kütle ve uzaklıklar G1 sağ kol tablosundan (veri/g1_sag_kol_kutle.csv; el kütlesi VARSAYIM)."""
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, yumusat, olc, oturum, sekil, g


def ders_3_1():
    """Sabit eksen etrafında dönme: dirseğin açısal hızı ve elin hızı, teğetsel ve normal ivmesi."""
    ns = oturum("3.1", "dirsek-donmesi", """
import numpy as np
from ortak import kayit, yumusat
k = kayit()
t = k["zaman_s"]
q = k["dirsek_rad"]
w = k["dirsek_hiz_rad_s"]
w_turev = np.gradient(q, t)
round(np.abs(w - w_turev).mean(), 4)
m = t > 3
i = np.flatnonzero(m)[np.abs(w[m]).argmax()]
round(t[i], 2), round(w[i], 3)
""")
    ns = oturum("3.1", "elin-hizi", """
r = 0.30
v_el = np.abs(w) * r
round(v_el[i], 3)
alfa = np.gradient(yumusat(w), t)
a_t = alfa * r
a_n = w**2 * r
round(np.abs(a_t[m]).max(), 3), round(a_n[m].max(), 3)
""", ns)
    t, q, w, wt, m, i = (ns[k] for k in ("t", "q", "w", "w_turev", "m", "i"))
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(t[m], np.degrees(q[m]), color="#0F766E"); ax[0].set_ylabel("dirsek açısı (°)")
    ax[0].set_title("Dirsek · benzetim kaydı (Isaac) · ilk 3 saniye başlangıç oturması, çıkarıldı")
    ax[1].plot(t[m], w[m], color="#7E22CE", label="kayıttaki açısal hız")
    ax[1].plot(t[m], wt[m], "--", color="#C2410C", lw=1.5, label="açıdan türevle")
    ax[1].annotate(f"{w[i]:.2f} rad/s", (t[i], w[i]), xytext=(t[i] - 30, w[i]), arrowprops=dict(arrowstyle="->"))
    ax[1].set_ylabel("açısal hız (rad/s)"); ax[1].set_xlabel("zaman (s)"); ax[1].legend(loc="upper left")
    sekil("3.1", "aci-ve-hiz")
    fig, ax = plt.subplots()
    ax.plot(t[m], ns["a_t"][m], color="#1D4ED8", label="teğetsel ivme  α r")
    ax.plot(t[m], ns["a_n"][m], color="#C2410C", label="normal ivme  ω² r")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("ivme (m/s²)"); ax.legend(loc="upper left")
    ax.set_title("Elin dirseğe göre ivmesi · el dirsekten 0,30 m uzakta (robot modeli)")
    sekil("3.1", "el-ivmesi")
    olc(d3_1_fark=np.abs(w - wt).mean(), d3_1_t=t[i], d3_1_w=w[i], d3_1_v_el=ns["v_el"][i],
        d3_1_at_max=np.abs(ns["a_t"][m]).max(), d3_1_an_max=ns["a_n"][m].max())


def ders_3_2():
    """Genel düzlemsel hareket: krank–biyel mekanizması, ani dönme merkezi (ÖRNEK)."""
    ns = oturum("3.2", "krank-biyel", """
import numpy as np
r, l, w = 0.05, 0.15, 20.0
th = np.radians(60)
A = r * np.array([np.cos(th), np.sin(th)])
phi = np.arcsin(r * np.sin(th) / l)
B = np.array([A[0] + l * np.cos(phi), 0.0])
w_AB = r * w * np.cos(th) / (l * np.cos(phi))
round(w_AB, 3)
v_B = -r * w * np.sin(th) - l * w_AB * np.sin(phi)
round(v_B, 4)
""")
    ns = oturum("3.2", "ani-donme-merkezi", """
IC = np.array([B[0], B[0] * np.tan(th)])
d_A = np.linalg.norm(IC - A)
d_B = np.linalg.norm(IC - B)
w_AB_ic = r * w / d_A
round(w_AB_ic, 3), round(-w_AB_ic * d_B, 4)
""", ns)
    r, l, w = 0.05, 0.15, 20.0
    th = np.linspace(0, 2 * np.pi, 3601)
    x = r * np.cos(th) + np.sqrt(l ** 2 - (r * np.sin(th)) ** 2)
    v = np.gradient(x, th) * w
    a = np.gradient(v, th) * w
    fig = plt.figure()
    a1 = fig.add_subplot(1, 2, 1)
    A, B, IC = ns["A"], ns["B"], ns["IC"]
    a1.plot([0, A[0]], [0, A[1]], color="#0F766E", lw=8, label="krank (OA)")
    a1.plot([A[0], B[0]], [A[1], B[1]], color="#7E22CE", lw=8, label="biyel (AB)")
    a1.plot([0, IC[0]], [0, IC[1]], ":", color="#555555"); a1.plot([B[0], IC[0]], [B[1], IC[1]], ":", color="#555555")
    a1.plot(*IC, "*", color="#C2410C", ms=28, label="ani dönme merkezi")
    a1.add_patch(plt.Rectangle((B[0] - 0.015, -0.012), 0.03, 0.024, color="#1D4ED8"))
    a1.set_aspect("equal"); a1.set_xlabel("x (m)"); a1.set_ylabel("y (m)"); a1.legend(loc="upper left", fontsize=17)
    a1.set_title("θ = 60°")
    a2 = fig.add_subplot(2, 2, 2); a2.plot(np.degrees(th), v, color="#1D4ED8"); a2.set_ylabel("piston hızı (m/s)")
    a2.set_title("krank 50 mm, biyel 150 mm, 20 rad/s (ÖRNEK)", fontsize=20)
    a3 = fig.add_subplot(2, 2, 4); a3.plot(np.degrees(th), a, color="#C2410C"); a3.set_ylabel("piston ivmesi (m/s²)")
    a3.set_xlabel("krank açısı (°)")
    sekil("3.2", "mekanizma")
    olc(d3_2_w_AB=ns["w_AB"], d3_2_v_B=ns["v_B"], d3_2_w_AB_ic=ns["w_AB_ic"], d3_2_v_max=np.abs(v).max(),
        d3_2_a_max=np.abs(a).max())


def ders_3_3():
    """Kütle eylemsizlik momenti: dirseğin taşıdığı parçalar, paralel eksen teoremi."""
    ns = oturum("3.3", "eylemsizlik", """
import numpy as np
T = np.genfromtxt("veri/g1_sag_kol_kutle.csv", delimiter=",", names=True,
                  dtype=None, encoding="utf-8")
dis = T[T["uzaklik_dirsek_m"] > 0]
for s in dis:
    print(f"{s[0]:20s} {s[1]:.3f} kg  {s[-1]:.3f} m  {s[1] * s[-1]**2:.5f}")
I_parca = (dis["kutle_kg"] * dis["uzaklik_dirsek_m"]**2).sum()
round(I_parca, 4)
I_dirsek = I_parca + 0.03
round(I_dirsek, 4)
""")
    ns = oturum("3.3", "paralel-eksen", """
m_c, L_c = 0.6, 0.2
n = 100000
x = (np.arange(n) + 0.5) / n * L_c
I_uc = (m_c / n * x**2).sum()
round(I_uc, 6), round(m_c * L_c**2 / 3, 6)
I_G = m_c * L_c**2 / 12
round(I_G + m_c * (L_c / 2)**2, 6)
""", ns)
    dis = ns["dis"]
    pay = dis["kutle_kg"] * dis["uzaklik_dirsek_m"] ** 2
    fig, ax = plt.subplots()
    ad = [s.replace(" parçası", "") for s in dis["parca"]]
    ax.barh(ad, pay, color=["#0F766E", "#1D4ED8", "#1D4ED8", "#1D4ED8", "#C2410C"])
    for k_, v in enumerate(pay):
        ax.text(v + 0.0005, k_, f"{v:.4f}  (%{100 * v / pay.sum():.0f})", va="center")
    ax.set_xlabel("m d²  (kg·m²)"); ax.invert_yaxis(); ax.set_xlim(0, pay.max() * 1.35)
    ax.set_title(f"Dirseğe göre eylemsizlik payları · toplam {pay.sum():.4f} kg·m² · el kütlesi VARSAYIM")
    sekil("3.3", "eylemsizlik-paylari")
    olc(d3_3_I_parca=ns["I_parca"], d3_3_I_dirsek=ns["I_dirsek"], d3_3_el_pay=pay[-1] / pay.sum(),
        d3_3_I_uc=ns["I_uc"], d3_3_I_uc_formul=0.6 * 0.2 ** 2 / 3)


def ders_3_4():
    """Dönme hareketinin kinetiği: M = I α ile dirsek torku, yerçekimi torku, sınırla karşılaştırma."""
    ns = oturum("3.4", "dirsek-torku", """
import numpy as np
from ortak import kayit, yumusat
k = kayit()
t, q, w = k["zaman_s"], k["dirsek_rad"], k["dirsek_hiz_rad_s"]
m = t > 3
I = 0.0976
alfa = np.gradient(yumusat(w), t)
tau_atalet = I * alfa
G = -2.998 * np.cos(q) + 0.145 * np.sin(q)
tau = tau_atalet - G
round(np.abs(tau_atalet[m]).max(), 3)
round(np.abs(G[m]).max(), 3)
round(np.abs(tau[m]).max(), 3), 25.0
""")
    t, m = ns["t"], ns["m"]
    fig, ax = plt.subplots()
    ax.plot(t[m], ns["tau"][m], color="#7E22CE", lw=4, label="motorun vermesi gereken tork  I α − G")
    ax.plot(t[m], -ns["G"][m], "--", color="#0F766E", label="yerçekimini karşılamak için  −G")
    ax.plot(t[m], ns["tau_atalet"][m], color="#C2410C", lw=2, label="açısal ivme için  I α")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("tork (N·m)"); ax.set_ylim(-0.6, 4.7); ax.legend(loc="upper right", ncol=1)
    ax.set_title("Dirsek torku · benzetim kaydı · basitleştirilmiş: omuzun hareketi hesaba katılmıyor · sınır 25 N·m")
    sekil("3.4", "tork-bilesenleri")
    olc(d3_4_atalet_max=np.abs(ns["tau_atalet"][m]).max(), d3_4_G_max=np.abs(ns["G"][m]).max(),
        d3_4_tau_max=np.abs(ns["tau"][m]).max(), d3_4_alfa_max=np.abs(ns["alfa"][m]).max())


if __name__ == "__main__":
    for f in (ders_3_1, ders_3_2, ders_3_3, ders_3_4):
        f(); print(f.__name__, "tamam")
