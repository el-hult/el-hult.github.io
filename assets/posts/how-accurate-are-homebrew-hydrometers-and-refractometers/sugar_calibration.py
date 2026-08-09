"""
Generate calibration plots for the sugar measurement blog post.
Run from repo root: python _scripts/sugar_calibration.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "posts" / "how-accurate-are-homebrew-hydrometers-and-refractometers"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────
# Two series of cumulative sugar additions to tap water.
# Columns: temp_C, chinese_sg, american_sg, refracto_sg, german_sg,
#           old_batch_g, added_sugar_g

data_A = np.array([
    # Series A (9 samples, starting batch: 178 g tap water)
    [25.0, 0.994, 1.004, 1.000, 1.002, 178.0,  0.0],
    [22.9, 0.998, 1.008, 1.003, 1.007, 178.0,  2.3],
    [23.7, 1.007, 1.016, 1.010, 1.015, 176.5,  3.2],
    [24.4, 1.012, 1.020, 1.016, 1.021, 178.0,  2.9],
    [25.3, 1.020, 1.025, 1.022, 1.028, 177.0,  3.0],
    [25.7, 1.028, 1.034, 1.032, 1.037, 179.5,  4.8],
    [25.6, 1.048, 1.052, 1.051, 1.054, 181.0,  9.5],
    [25.0, 1.076, 1.080, 1.080, 1.084, 187.5, 15.4],
    [24.9, 1.102, 1.106, 1.105, 1.109, 122.0,  9.7],
])

data_B = np.array([
    # Series B (4 samples, starting batch: 265.5 g tap water)
    [21.3, 0.996, 1.005, 1.000, 1.003, 265.5,  0.0],
    [24.8, 1.036, 1.042, 1.040, 1.048, 106.5, 12.4],
    [25.6, 1.069, 1.072, 1.073, 1.075, 113.5, 10.5],
    [25.7, 1.098, 1.102, 1.104, 1.108, 122.5, 11.5],
])

data = np.vstack([data_A, data_B])
series_labels = ["A"] * len(data_A) + ["B"] * len(data_B)

temp       = data[:, 0]
chinese    = data[:, 1]
american   = data[:, 2]
refracto   = data[:, 3]
german     = data[:, 4]

# ── Compute Brix from batch masses and sugar additions ───────────────────────
# Each row records old_batch_g (mass of solution before adding sugar) and
# added_sugar_g.  The sugar already in solution is old_batch_g × prev_brix/100.
# Brix = 100 × sugar_in_solution / total_solution_mass.

def compute_brix(series_data):
    """Compute Brix recursively for one series."""
    bx = np.zeros(len(series_data))
    prev = 0.0
    for i in range(len(series_data)):
        old_batch = series_data[i, 5]
        added = series_data[i, 6]
        sugar_in = old_batch * prev / 100.0 + added
        total = old_batch + added
        prev = 100.0 * sugar_in / total
        bx[i] = prev
    return bx

brix = np.concatenate([compute_brix(data_A), compute_brix(data_B)])

# ── NBS reference table ──────────────────────────────────────────────────────
# Apparent specific gravity at 20°C/20°C of sucrose solutions (column 3).
# Source: NBS Circular 440, Table 114 (Bates et al., 1942).
# Values at integer Brix, accurate to ±1 in the fifth decimal.

NBS_BRIX = np.arange(0, 31, dtype=float)
NBS_SG = np.array([
    1.00000, 1.00390, 1.00780, 1.01173, 1.01569,  # 0–4
    1.01968, 1.02369, 1.02773, 1.03180, 1.03590,  # 5–9
    1.04003, 1.04418, 1.04837, 1.05259, 1.05683,  # 10–14
    1.06111, 1.06542, 1.06976, 1.07413, 1.07853,  # 15–19
    1.08297, 1.08744, 1.09194, 1.09647, 1.10104,  # 20–24
    1.10564, 1.11027, 1.11493, 1.11963, 1.12436,  # 25–29
    1.12913,                                        # 30
])

brix_to_sg = interp1d(NBS_BRIX, NBS_SG, kind="cubic")
ref_sg = brix_to_sg(brix)

# ── Water density model ───────────────────────────────────────────────────────
# Polynomial for air-free water density (g/mL) at 1 atm, valid 5–40°C on ITS-90.
# Jones & Harris (1992), J. Res. Natl. Inst. Stand. Technol. 97(3), 335-340.
def rho_water(T_celsius):
    """Water density in g/mL at temperature T (°C), 1 atm."""
    t = np.asarray(T_celsius, dtype=float)
    return (999.84847 + 6.337563e-2 * t - 8.523829e-3 * t**2
            + 6.943248e-5 * t**3 - 3.821216e-7 * t**4) / 1000.0


# ── Physics-based temperature corrections ─────────────────────────────────────
# A hydrometer calibrated at T_cal, used at T, reads ρ_sample(T)/ρ_water(T_cal).
# True SG at 20/20°C = ρ_sample(20°C)/ρ_water(20°C).
# Assuming the sample expands like water:
#   corrected = reading × ρ_water(T_cal) / ρ_water(T)
#
# This converts the reading to SG(T_cal/T), then the water-like-expansion
# assumption converts to SG(20/20).

T_CAL_CHINESE = 15.556   # 60°F
T_CAL_AMERICAN = 20.0
T_CAL_GERMAN = 20.0

chinese_corr = chinese * rho_water(T_CAL_CHINESE) / rho_water(temp)
german_corr  = german  * rho_water(T_CAL_GERMAN)  / rho_water(temp)

# American hydrometer: also apply the manufacturer's additive correction table
# for comparison, in addition to the physics-based approach.
corr_temps = np.array([10.0, 15.0, 20.0, 25.0, 30.0])
corr_vals  = np.array([-0.0025, -0.0014, 0.0, 0.0028, 0.0046])
correction_fn = interp1d(corr_temps, corr_vals, kind="linear", fill_value="extrapolate")

american_table_corr   = american + correction_fn(temp)
american_physics_corr = american * rho_water(T_CAL_AMERICAN) / rho_water(temp)

# ── Plot styling ──────────────────────────────────────────────────────────────
COLORS = {
    "Chinese":     "#e41a1c",
    "American":    "#377eb8",
    "Refractometer": "#4daf4a",
    "German":      "#984ea3",
}
MARKERS = {"A": "o", "B": "s"}
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150, "figure.figsize": (8, 5.5)})

series_mask_A = np.array([sl == "A" for sl in series_labels])
series_mask_B = np.array([sl == "B" for sl in series_labels])


def add_trend_line(ax, x, y, color):
    """Add linear regression trend line."""
    coeffs = np.polyfit(x, y, 1)
    x_fit = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_fit, np.polyval(coeffs, x_fit), color=color, lw=1, ls="-", alpha=0.5)


def sg_formatter(x, _):
    """Format SG with 3 decimal places so Oechsle values are readable."""
    return f"{x:.3f}"


# ── Plot 1: Raw SG readings vs reference ──────────────────────────────────────
fig, ax = plt.subplots()
sg_range = np.array([0.990, 1.120])
ax.plot(sg_range, sg_range, "k--", lw=0.8, label="Perfect agreement")

for label, vals, color in [
    ("Chinese (60/60°F raw)", chinese, COLORS["Chinese"]),
    ("American (20°C raw)", american, COLORS["American"]),
    ("Refractometer (ATC)", refracto, COLORS["Refractometer"]),
    ("German (20°C raw)", german, COLORS["German"]),
]:
    ax.scatter(ref_sg[series_mask_A], vals[series_mask_A], c=color, marker="o",
               s=30, label=f"{label} (○ A)", alpha=0.8, edgecolors="none")
    ax.scatter(ref_sg[series_mask_B], vals[series_mask_B], c=color, marker="s",
               s=30, label=f"{label} (□ B)", alpha=0.8, edgecolors="none")
    add_trend_line(ax, ref_sg, vals, color)

ax.set_xlabel("Reference SG (20/20°C)")
ax.set_ylabel("Measured SG")
ax.set_title("Raw instrument readings vs reference")
ax.xaxis.set_major_formatter(plt.FuncFormatter(sg_formatter))
ax.yaxis.set_major_formatter(plt.FuncFormatter(sg_formatter))
ax.legend(fontsize=6, loc="upper left", ncol=2)
ax.set_aspect("equal")
ax.set_xlim(sg_range)
ax.set_ylim(sg_range)
fig.tight_layout()
fig.savefig(OUT_DIR / "raw_readings.png")
plt.close(fig)

# ── Plot 2: Residuals (raw) ──────────────────────────────────────────────────
fig, ax = plt.subplots()
ax.axhline(0, color="k", lw=0.8, ls="--")

for label, vals, color in [
    ("Chinese (60/60°F)", chinese, COLORS["Chinese"]),
    ("American (20°C)", american, COLORS["American"]),
    ("Refractometer", refracto, COLORS["Refractometer"]),
    ("German (20°C)", german, COLORS["German"]),
]:
    residuals = vals - ref_sg
    ax.scatter(ref_sg[series_mask_A], residuals[series_mask_A], c=color, marker="o",
               s=30, label=f"{label} (○ A)", alpha=0.8, edgecolors="none")
    ax.scatter(ref_sg[series_mask_B], residuals[series_mask_B], c=color, marker="s",
               s=30, label=f"{label} (□ B)", alpha=0.8, edgecolors="none")
    add_trend_line(ax, ref_sg, residuals, color)

ax.set_xlabel("Reference SG (20/20°C)")
ax.set_ylabel("Measured − Reference SG")
ax.set_title("Residuals — raw readings (no temperature correction)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(sg_formatter))
ax.legend(fontsize=6, loc="lower left", ncol=2)
fig.tight_layout()
fig.savefig(OUT_DIR / "residuals_raw.png")
plt.close(fig)

# ── Plot 3: Residuals after temperature corrections ──────────────────────────
fig, ax = plt.subplots()
ax.axhline(0, color="k", lw=0.8, ls="--")

for label, vals, color in [
    ("Chinese (physics-corr.)", chinese_corr, COLORS["Chinese"]),
    ("American (physics-corr.)", american_physics_corr, COLORS["American"]),
    ("Refractometer (ATC)", refracto, COLORS["Refractometer"]),
    ("German (physics-corr.)", german_corr, COLORS["German"]),
]:
    residuals = vals - ref_sg
    ax.scatter(ref_sg[series_mask_A], residuals[series_mask_A], c=color, marker="o",
               s=30, label=f"{label} (○ A)", alpha=0.8, edgecolors="none")
    ax.scatter(ref_sg[series_mask_B], residuals[series_mask_B], c=color, marker="s",
               s=30, label=f"{label} (□ B)", alpha=0.8, edgecolors="none")
    add_trend_line(ax, ref_sg, residuals, color)

ax.set_xlabel("Reference SG (20/20°C)")
ax.set_ylabel("Measured − Reference SG")
ax.set_title("Residuals — after available temperature corrections")
ax.xaxis.set_major_formatter(plt.FuncFormatter(sg_formatter))
ax.legend(fontsize=6, loc="lower left", ncol=2)
fig.tight_layout()
fig.savefig(OUT_DIR / "residuals_corrected.png")
plt.close(fig)

# ── Summary statistics ────────────────────────────────────────────────────────
print("=== Summary statistics (measured - reference SG) ===\n")

instruments = {
    "Chinese (raw 60/60°F)":       chinese,
    "Chinese (physics-corr.)":     chinese_corr,
    "American (raw 20°C)":         american,
    "American (table-corr.)":      american_table_corr,
    "American (physics-corr.)":    american_physics_corr,
    "Refractometer (ATC)":         refracto,
    "German (raw 20°C)":           german,
    "German (physics-corr.)":      german_corr,
}

for name, vals in instruments.items():
    res = vals - ref_sg
    print(f"{name:35s}  mean={res.mean():+.4f}  std={res.std():.4f}  "
          f"max|err|={np.abs(res).max():.4f}")

# ── ABV error propagation ────────────────────────────────────────────────────
print("\n=== ABV error propagation (ABV = 131.25 * (OG - FG)) ===\n")
print("If both OG and FG are measured with the SAME instrument,")
print("systematic bias cancels.  ABV error ≈ 131.25 × √(2) × σ")
print("where σ is the std dev (random scatter), not RMSE.\n")

for name, vals in instruments.items():
    res = vals - ref_sg
    rmse = np.sqrt(np.mean(res**2))
    std = res.std()
    abv_rmse = 131.25 * np.sqrt(2) * rmse
    abv_std = 131.25 * np.sqrt(2) * std
    print(f"{name:35s}  RMSE={rmse:.4f}  std={std:.4f}  "
          f"ABV(RMSE)=±{abv_rmse:.1f}%  ABV(std)=±{abv_std:.1f}%")

# ── Temperature correction magnitude ─────────────────────────────────────────
print("\n=== Physics-based correction factors (ρ_water(T_cal)/ρ_water(T)) ===\n")
print(f"Measurement temps: {temp.min():.1f}–{temp.max():.1f}°C")
for name, t_cal in [("Chinese (15.6°C)", T_CAL_CHINESE), ("American/German (20°C)", T_CAL_AMERICAN)]:
    factors = rho_water(t_cal) / rho_water(temp)
    print(f"  {name}: factor range {factors.min():.5f}–{factors.max():.5f}")

# ── American correction table vs physics model ────────────────────────────────
print("\n=== American correction table vs physics model ===\n")
# The table gives additive corrections. The physics model gives a multiplicative
# factor ρ_water(20)/ρ_water(T). For SG≈1 the additive equivalent is factor-1.
print(f"{'Temp':>6s}  {'Table':>8s}  {'Physics':>8s}  {'Ratio':>6s}")
for t in [10, 15, 20, 25, 30]:
    table_corr = dict(zip(corr_temps, corr_vals))[t]
    physics_corr = rho_water(20.0) / rho_water(float(t)) - 1.0
    ratio = table_corr / physics_corr if abs(physics_corr) > 1e-8 else float('inf')
    print(f"{t:5.0f}°C  {table_corr:+8.4f}  {physics_corr:+8.4f}  {ratio:6.2f}×")

print(f"\nPlots saved to {OUT_DIR}")
