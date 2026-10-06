"""Hafta 1 · Parçacığın Kinematiği — Ders 1.1–1.4.
  python hafta1.py   → ekran/1.x/*.txt + *.png, OLCUMLER.json (d1_*)"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, yumusat, olc, oturum, sekil, g


def ders_1_1():
    """Konum, hız ve ivme: bardağın konumundan sayısal türevle hız ve ivme."""
    ns = oturum("1.1", "kaydi-acmak", """
import numpy as np
from ortak import kayit, yumusat
k = kayit()
t = k["zaman_s"]
p = np.column_stack([k["bardak_x_m"], k["bardak_y_m"], k["bardak_z_m"]])
p.shape
t[-1]
p[0]
p[-1]
""")
    t, p = ns["t"], ns["p"]
    ns = oturum("1.1", "hiz-ivme", """
v = np.gradient(p, t, axis=0)
hiz = np.linalg.norm(v, axis=1)
round(hiz.max(), 3), round(t[hiz.argmax()], 2)
a = np.gradient(v, t, axis=0)
round(np.linalg.norm(a, axis=1).max(), 2)
hiz_y = np.linalg.norm(np.gradient(yumusat(p), t, axis=0), axis=1)
round(hiz_y.max(), 3)
a_y = np.gradient(np.gradient(yumusat(p), t, axis=0), t, axis=0)
round(np.linalg.norm(a_y, axis=1).max(), 2)
yol = np.linalg.norm(np.diff(yumusat(p), axis=0), axis=1).sum()
round(yol, 2)
""", ns)
    v, hiz, a, a_y = ns["v"], ns["hiz"], ns["a"], ns["a_y"]
    fig, ax = plt.subplots(2, 1, sharex=True)
    for i, (ad, r) in enumerate([("x", "#C2410C"), ("y", "#1D4ED8"), ("z", "#0F766E")]):
        ax[0].plot(t, p[:, i] - p[0, i], color=r, label=f"{ad} − {ad}₀")
    ax[0].set_ylabel("konum farkı (m)"); ax[0].legend(loc="upper left"); ax[0].set_title("Bardağın konumu ve hızı · benzetim kaydı (Isaac)")
    ax[1].plot(t, hiz, color="#bbbbbb", lw=1.5, label=f"doğrudan türev · en büyük {hiz.max():.2f} m/s")
    ax[1].plot(t, ns["hiz_y"], color="#7E22CE", label=f"yarım saniye yumuşatıp türev · en büyük {ns['hiz_y'].max():.2f} m/s")
    ax[1].set_ylabel("hız (m/s)"); ax[1].set_xlabel("zaman (s)"); ax[1].legend(loc="upper left")
    sekil("1.1", "konum-hiz")
    fig, ax = plt.subplots()
    ax.plot(t, np.linalg.norm(a, axis=1), color="#bbbbbb", lw=1.5, label="doğrudan iki kez türev")
    ax.plot(t, np.linalg.norm(a_y, axis=1), color="#C2410C", label="önce yarım saniye yumuşatıp türev")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("ivme büyüklüğü (m/s²)"); ax.legend(loc="upper left")
    ax.set_title("Türev gürültüyü büyütür: ivme")
    sekil("1.1", "ivme-gurultu")
    olc(d1_1_sure_s=t[-1], d1_1_ornek=len(t), d1_1_bas=p[0], d1_1_son=p[-1], d1_1_hiz_max=hiz.max(), d1_1_hiz_max_t=t[hiz.argmax()], d1_1_hiz_max_yumusak=ns["hiz_y"].max(),
        d1_1_ivme_max_ham=np.linalg.norm(a, axis=1).max(), d1_1_ivme_max_yumusak=np.linalg.norm(a_y, axis=1).max(),
        d1_1_yol_m=ns["yol"])


def ders_1_2():
    """Sabit ivme: masadan yatay hızla düşen bardak — kapalı çözüm ve adım adım (Euler) çözüm."""
    ns = oturum("1.2", "kapali-cozum", """
import numpy as np
g = 9.81
h = 0.76
v0 = 0.5
t_dus = np.sqrt(2 * h / g)
round(t_dus, 3)
x_dus = v0 * t_dus
round(x_dus, 3)
v_carpma = np.hypot(v0, g * t_dus)
round(v_carpma, 2)
""")
    ns = oturum("1.2", "adim-adim", """
def euler(dt):
    x, y, vx, vy, t = 0.0, h, v0, 0.0, 0.0
    while y > 0:
        x, y = x + vx * dt, y + vy * dt
        vy = vy - g * dt
        t = t + dt
    return round(t, 3), round(x, 3)
euler(0.05)
euler(0.01)
euler(0.001)
""", ns)
    h, v0, t_dus = ns["h"], ns["v0"], ns["t_dus"]
    fig, ax = plt.subplots()
    tt = np.linspace(0, t_dus, 200)
    ax.plot(v0 * tt, h - g * tt ** 2 / 2, color="#C2410C", lw=4, label="kapalı çözüm")
    for dt, r in [(0.05, "#1D4ED8"), (0.01, "#0F766E")]:
        xs, ys = [0.0], [h]; x, y, vx, vy = 0.0, h, v0, 0.0
        while y > 0:
            x, y = x + vx * dt, y + vy * dt; vy -= g * dt; xs.append(x); ys.append(y)
        ax.plot(xs, ys, "o--", color=r, ms=7, lw=1.5, label=f"Euler, adım {dt} s")
    ax.axhline(0, color="k", lw=1); ax.set_xlabel("yatay uzaklık (m)"); ax.set_ylabel("yükseklik (m)")
    ax.set_title("Masadan düşen bardak · masa 0,76 m (benzetim kaydı) · ilk hız 0,5 m/s (ÖRNEK)"); ax.legend()
    sekil("1.2", "yorunge")
    olc(d1_2_h=h, d1_2_v0=v0, d1_2_t=t_dus, d1_2_x=ns["x_dus"], d1_2_v_carpma=ns["v_carpma"],
        d1_2_euler=[ns["euler"](0.05), ns["euler"](0.01), ns["euler"](0.001)])


def ders_1_3():
    """Eğrisel hareket: bardağın yatay yolunda teğetsel ve normal ivme, eğrilik yarıçapı."""
    ns = oturum("1.3", "tegetsel-normal", """
import numpy as np
from ortak import kayit, yumusat
k = kayit()
t = k["zaman_s"]
r = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"]]), 50)
v = np.gradient(r, t, axis=0)
a = np.gradient(v, t, axis=0)
hiz = np.linalg.norm(v, axis=1)
a_t = (v * a).sum(axis=1) / np.maximum(hiz, 1e-9)
a_n = np.abs(v[:, 0] * a[:, 1] - v[:, 1] * a[:, 0]) / np.maximum(hiz, 1e-9)
hareket = hiz > 0.2
i = np.flatnonzero(hareket)[a_n[hareket].argmax()]
round(t[i], 2), round(hiz[i], 3), round(a_n[i], 3)
rho = hiz[i] ** 2 / a_n[i]
round(rho, 2)
""")
    t, r, hiz, a_t, a_n, i, hareket = (ns[k] for k in ("t", "r", "hiz", "a_t", "a_n", "i", "hareket"))
    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    sc = ax.scatter(r[:, 0], r[:, 1], c=hiz, cmap="viridis", s=10)
    fig.colorbar(sc, ax=ax, label="hız (m/s)")
    ax.plot(*r[0], "s", color="#0F766E", ms=18, label="başlangıç masası"); ax.plot(*r[-1], "*", color="#C2410C", ms=26, label="servis masası")
    ax.plot(*r[i], "o", mfc="none", mec="#C2410C", ms=40, mew=3, label=f"en büyük normal ivme · t = {t[i]:.1f} s")
    ax.set_aspect("equal"); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.legend(loc="lower right")
    ax.set_title("Bardağın yatay yolu · benzetim kaydı (bir saniye yumuşatıldı)")
    sekil("1.3", "yatay-yol")
    fig, ax = plt.subplots()
    ax.plot(t, np.where(hareket, a_t, np.nan), color="#1D4ED8", label="teğetsel ivme  (hız değişimi)")
    ax.plot(t, np.where(hareket, a_n, np.nan), color="#C2410C", label="normal ivme  (yön değişimi)")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("ivme (m/s²)"); ax.legend(loc="upper left")
    ax.set_title("Teğetsel ve normal ivme · yalnız hız 0,2 m/s'yi aşınca")
    sekil("1.3", "tegetsel-normal-grafik")
    olc(d1_3_t=t[i], d1_3_hiz=hiz[i], d1_3_an=a_n[i], d1_3_rho=ns["rho"], d1_3_at_max=np.abs(a_t[hareket]).max(),
        d1_3_an_max=a_n[hareket].max())


def ders_1_4():
    """Kutupsal koordinatlar: dönen kolda kayan bilezik (ÖRNEK)."""
    ns = oturum("1.4", "kutupsal", """
import numpy as np
r = lambda t: 0.2 + 0.15 * t**2
r_n = lambda t: 0.3 * t
r_nn = 0.3
th_n = 1.5
t = 1.0
v_r, v_th = r_n(t), r(t) * th_n
round(v_r, 3), round(v_th, 3)
a_r = r_nn - r(t) * th_n**2
a_th = 2 * r_n(t) * th_n
round(a_r, 4), round(a_th, 4)
""")
    ns = oturum("1.4", "kartezyen-sinama", """
tt = np.linspace(0, 2, 20001)
x = r(tt) * np.cos(th_n * tt)
y = r(tt) * np.sin(th_n * tt)
ax_ = np.gradient(np.gradient(x, tt), tt)
ay_ = np.gradient(np.gradient(y, tt), tt)
j = 10000
th = th_n * tt[j]
a_r_say = ax_[j] * np.cos(th) + ay_[j] * np.sin(th)
a_th_say = -ax_[j] * np.sin(th) + ay_[j] * np.cos(th)
round(a_r_say, 4), round(a_th_say, 4)
""", ns)
    tt = np.linspace(0, 2, 400); rr = 0.2 + 0.15 * tt ** 2; th = 1.5 * tt
    fig, ax = plt.subplots()
    ax.plot(rr * np.cos(th), rr * np.sin(th), color="#7E22CE", label="bileziğin yolu")
    T = 1.0; R = 0.2 + 0.15; TH = 1.5
    p = np.array([R * np.cos(TH), R * np.sin(TH)]); er = p / R; et = np.array([-er[1], er[0]])
    ax.plot([0, 0.95 * np.cos(TH)], [0, 0.95 * np.sin(TH)], color="#555555", lw=6, alpha=0.5, label="dönen kol (t = 1 s)")
    s = 0.25
    ax.annotate("", p + s * ns["a_r"] * er, p, arrowprops=dict(arrowstyle="->", color="#C2410C", lw=4))
    ax.annotate("", p + s * ns["a_th"] * et, p, arrowprops=dict(arrowstyle="->", color="#1D4ED8", lw=4))
    ax.text(*(p + s * ns["a_r"] * er + [-0.12, -0.05]), f"a_r = {ns['a_r']:.4f}", color="#C2410C")
    ax.text(*(p + s * ns["a_th"] * et + [-0.05, 0.03]), f"a_θ = {ns['a_th']:.2f}", color="#1D4ED8")
    ax.plot(*p, "o", color="k", ms=14); ax.plot(0, 0, "ks", ms=14)
    ax.set_aspect("equal"); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.legend(loc="lower left")
    ax.set_title("Dönen kolda kayan bilezik · r = 0,2 + 0,15 t², θ̇ = 1,5 rad/s (ÖRNEK)")
    sekil("1.4", "bilezik-yolu")
    olc(d1_4_vr=ns["v_r"], d1_4_vth=ns["v_th"], d1_4_ar=ns["a_r"], d1_4_ath=ns["a_th"],
        d1_4_ar_say=ns["a_r_say"], d1_4_ath_say=ns["a_th_say"])


if __name__ == "__main__":
    for f in (ders_1_1, ders_1_2, ders_1_3, ders_1_4):
        f(); print(f.__name__, "tamam")
