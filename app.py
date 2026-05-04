import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, FancyBboxPatch
import random

# =============================================
# ⚖️ THE MIZAN – النسخة المتكاملة النهائية
# دمج: الهالة الملحمية + المدارات الديناميكية + الألوان الحقيقية
# Author: Ali Adel Alatifi | علي عادل العاطفي
# =============================================

# ---------- Divine Constants ----------
ق = 100; ن = 50; ص = 90; ك = 20
G_norm = 6.67; c_norm = 3.0; h_norm = 6.63; alpha_norm = 0.73
PHI_RATIO = ق / G_norm

fig = plt.figure(figsize=(24, 16), facecolor='#020010')
ax = fig.add_axes([0, 0, 1, 1], facecolor='#020010')
ax.set_xlim(0, 24); ax.set_ylim(0, 16)
ax.axis('off')

# =============================================
# ١. THE THRONE + AUTHOR NAME + SMALL MIZAN
# =============================================
ax.text(12, 15.6, '⚖️  S = W × B  |  Q = 100  |  Theory of Everything  ⚖️',
        color='#FFD700', fontsize=20, ha='center', fontweight='bold')
ax.text(12, 15.1, 'Scientific Proof: S (Gold=Stability) ALWAYS leads E (Cyan=Empowerment) – Quranic Istidraj',
        color='#00FFFF', fontsize=8, ha='center')
ax.text(12, 14.7, 'علي عادل العاطفي  |  Ali Adel Alatifi',
        color='#FFD700', fontsize=11, ha='center', fontweight='bold', alpha=0.9)

# --- Small Mizan under author ---
mizan_center_x, mizan_center_y = 12, 13.8
beam, = ax.plot([mizan_center_x-1.2, mizan_center_x+1.2], [mizan_center_y, mizan_center_y],
                color='#FFD700', lw=1.5, alpha=0.7, zorder=6)
ax.scatter([mizan_center_x], [mizan_center_y+0.3], s=60, c='white', alpha=0.6, zorder=7, edgecolors='#FFD700', lw=1)
chain_L, = ax.plot([mizan_center_x-1.2, mizan_center_x-1.2], [mizan_center_y, mizan_center_y-0.7],
                   color='#FFD700', lw=0.8, alpha=0.5, zorder=5)
chain_R, = ax.plot([mizan_center_x+1.2, mizan_center_x+1.2], [mizan_center_y, mizan_center_y-0.7],
                   color='#FFD700', lw=0.8, alpha=0.5, zorder=5)
pan_L = FancyBboxPatch((mizan_center_x-1.8, mizan_center_y-1.2), 1.2, 0.5, boxstyle="round,pad=0.05",
                       color='white', alpha=0.25, zorder=4, ec='white', lw=0.7)
pan_R = FancyBboxPatch((mizan_center_x+0.6, mizan_center_y-1.2), 1.2, 0.5, boxstyle="round,pad=0.05",
                       color='#220000', alpha=0.25, zorder=4, ec='#FF3333', lw=0.7)
ax.add_patch(pan_L); ax.add_patch(pan_R)
good_val = ax.text(mizan_center_x-1.2, mizan_center_y-0.95, '0', color='white', fontsize=6, ha='center', fontweight='bold', alpha=0.6)
bad_val = ax.text(mizan_center_x+1.2, mizan_center_y-0.95, '0', color='#FF3333', fontsize=6, ha='center', fontweight='bold', alpha=0.6)

# =============================================
# ٢. THE VISIBLE WORLD – دمج التصميمين
# =============================================
center_x, center_y = 12, 7.5
N_SOULS = 400

# خلفية نجوم ثابتة
bg_stars_x = np.random.uniform(0, 24, 800)
bg_stars_y = np.random.uniform(2, 14, 800)
ax.scatter(bg_stars_x, bg_stars_y, s=np.random.uniform(0.5, 2, 800), c='white', alpha=0.15, zorder=0)

# ===== Sun S – ذهبي = الثبات =====
sun = Circle((center_x, center_y), 1.0, color='#FFFFFF', alpha=0.95, zorder=12)
sun_glow1 = Circle((center_x, center_y), 1.8, color='#FFD700', alpha=0.2, zorder=11)
sun_glow2 = Circle((center_x, center_y), 2.8, color='#FFD700', alpha=0.08, zorder=10)
sun_glow3 = Circle((center_x, center_y), 4.5, color='#FFD700', alpha=0.03, zorder=9)
ax.add_patch(sun); ax.add_patch(sun_glow1); ax.add_patch(sun_glow2); ax.add_patch(sun_glow3)
ax.text(center_x, center_y, 'S', color='#3a2000', fontsize=12, ha='center', va='center', fontweight='bold', zorder=13)

# ===== Epic E Halo – سماوي = التمكين (يتأخر عن S) =====
halo = Circle((center_x, center_y), 0.8, color='#00FFFF', alpha=0.2, zorder=8)
ax.add_patch(halo)
ax.text(center_x, center_y - 2.5, 'E (Empowerment & Istidraj) – Always Lags Behind S', color='#00FFFF', fontsize=8, ha='center', alpha=0.7)

# ===== مدارات ديناميكية للكواكب =====
orbit_W_circle = Circle((center_x, center_y), 5, fill=False, color='#FFD700', lw=0.8, alpha=0.15, zorder=1)
orbit_B_circle = Circle((center_x, center_y), 5, fill=False, color='#FF3333', lw=0.8, alpha=0.15, zorder=1)
ax.add_patch(orbit_W_circle); ax.add_patch(orbit_B_circle)

# ===== Planet W – أبيض/ذهبي = الولاء =====
planet_W = Circle((0,0), 0.4, color='#FFFFFF', alpha=0.95, zorder=15, ec='#FFD700', lw=1.5)
ax.add_patch(planet_W)
label_W = ax.text(0, 0, 'W (Al-Walaa)', color='#FFD700', fontsize=9, ha='center', fontweight='bold', zorder=16)
trail_W, = ax.plot([], [], color='#FFD700', lw=0.4, alpha=0.2, zorder=2)

# ===== Planet B – أحمر = البراءة =====
planet_B = Circle((0,0), 0.4, color='#FF3333', alpha=0.95, zorder=15, ec='#FF6666', lw=1.5)
ax.add_patch(planet_B)
label_B = ax.text(0, 0, 'B (Al-Baraa)', color='#FF3333', fontsize=9, ha='center', fontweight='bold', zorder=16)
trail_B, = ax.plot([], [], color='#FF3333', lw=0.4, alpha=0.2, zorder=2)

# ===== نجوم النور (ذهبية) والظلام (حمراء) =====
stars_gold = ax.scatter([], [], s=[], c='#FFD700', alpha=0.5, zorder=3)
stars_red = ax.scatter([], [], s=[], c='#FF2222', alpha=0.5, zorder=3)

# ===== ATOM & CELL =====
atom_nucleus = Circle((3, 4.5), 0.4, color='#4488FF', alpha=0.7, zorder=5)
atom_electron = Circle((3, 4.5), 0.06, color='white', alpha=0.9, zorder=6)
ax.add_patch(atom_nucleus); ax.add_patch(atom_electron)
ax.text(3, 3.5, 'Atom (Physics)\nSame Law – S = W × B', color='#4488FF', fontsize=7, ha='center', alpha=0.7)

cell_membrane = Circle((21, 4.5), 0.5, color='#00FF88', alpha=0.5, zorder=5)
cell_nucleus = Circle((21, 4.5), 0.15, color='white', alpha=0.8, zorder=6)
ax.add_patch(cell_membrane); ax.add_patch(cell_nucleus)
ax.text(21, 3.5, 'Cell (Biology)\nSame Law – S = W × B', color='#00FF88', fontsize=7, ha='center', alpha=0.7)

# =============================================
# THE LIVING SPIRAL
# =============================================
np.random.seed(42)
types_init = np.random.choice(['believer', 'disbeliever', 'hypocrite'], N_SOULS, p=[0.4, 0.3, 0.3])

spiral_W = np.zeros(N_SOULS)
spiral_B = np.zeros(N_SOULS)

for i in range(N_SOULS):
    if types_init[i] == 'believer':
        spiral_W[i] = np.random.uniform(0.7, 1.0)
        spiral_B[i] = np.random.uniform(0.7, 1.0)
    elif types_init[i] == 'disbeliever':
        spiral_W[i] = np.random.uniform(0.01, 0.2)
        spiral_B[i] = np.random.uniform(0.01, 0.2)
    else:
        spiral_W[i] = np.random.uniform(0.4, 0.7)
        spiral_B[i] = np.random.uniform(0.1, 0.4)

angles_init = np.linspace(0, 8*np.pi, N_SOULS)
radii_init = (angles_init * 0.35) + np.random.uniform(0, 1.5, N_SOULS)
spiral_x = center_x + radii_init * np.cos(angles_init + np.random.uniform(-0.3, 0.3, N_SOULS))
spiral_y = center_y + radii_init * np.sin(angles_init + np.random.uniform(-0.3, 0.3, N_SOULS)) * 0.4
spiral_x = np.clip(spiral_x, 0.5, 23.5)
spiral_y = np.clip(spiral_y, 2.5, 14.0)

soul_angles = np.random.uniform(0, 2*np.pi, N_SOULS)
soul_speeds = np.random.uniform(0.005, 0.02, N_SOULS)
soul_orbits = radii_init.copy()

lines = []
for i in range(N_SOULS):
    distances = np.sqrt((spiral_x[i] - spiral_x)**2 + (spiral_y[i] - spiral_y)**2)
    nearest = np.argsort(distances)[1:3]
    for j in nearest:
        if j > i:
            line, = ax.plot([], [], color='white', lw=0.3, alpha=0.1, zorder=1)
            lines.append((i, j, line))

UNIFORM_SIZE = 55
spiral_scatter = ax.scatter(spiral_x, spiral_y, s=UNIFORM_SIZE, c='white', alpha=0.9, zorder=10, edgecolors='white', linewidths=0.5)

stream_gold = ax.scatter([], [], s=[], c='#FFD700', alpha=0.8, zorder=20)
stream_red = ax.scatter([], [], s=[], c='#FF2222', alpha=0.8, zorder=20)

phase_text = ax.text(12, 3.8, '', color='white', fontsize=12, ha='center', fontweight='bold')

# =============================================
# BATTLE HEATMAP + PROOF PANEL
# =============================================
ax_heat = fig.add_axes([0.02, 0.02, 0.35, 0.12], facecolor='#0a0a1a')
ax_heat.set_title('Collective Vibration Heatmap', color='white', fontsize=7, pad=2)
ax_heat.tick_params(colors='white', labelsize=4)

ax_counters = fig.add_axes([0.38, 0.02, 0.15, 0.12], facecolor='#0a0a1a')
ax_counters.set_xlim(0, 10); ax_counters.set_ylim(0, 6); ax_counters.axis('off')

ax_proof = fig.add_axes([0.55, 0.02, 0.43, 0.12], facecolor='#0a0a1a')
ax_proof.set_title('Proof: S (GOLD=Stability) leads E (CYAN=Empowerment) – Istidraj', color='white', fontsize=7, pad=2)
ax_proof.set_xlim(0, 200); ax_proof.set_ylim(0, 1)
ax_proof.tick_params(colors='white', labelsize=4)
proof_S_line, = ax_proof.plot([], [], color='#FFD700', lw=2, label='S (Stability)')
proof_E_line, = ax_proof.plot([], [], color='#00FFFF', lw=2, label='E (Empowerment)')
ax_proof.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=5)
ax_proof.grid(True, alpha=0.2)
proof_data_S, proof_data_E, proof_x = [], [], []

# ---------- Simulation Variables ----------
W_val, B_val, E_val = 0.9, 0.9, 0.1
ك_val, حسنات, سيئات = 0.2, 0.0, 0.0
phase = 'Balance'
aW, aB, aE_angle = 0.0, np.pi, 0.0
tWx, tWy, tBx, tBy = [], [], [], []
hdata = []
proof_counter = 0

def update(frame):
    global W_val, B_val, E_val, ك_val, حسنات, سيئات, phase, aW, aB, aE_angle
    global spiral_W, spiral_B, spiral_x, spiral_y, soul_angles, soul_orbits
    global proof_data_S, proof_data_E, proof_x, proof_counter
    global tWx, tWy, tBx, tBy
    
    # ===== Stars drive everything =====
    avg_W_stars = np.mean(spiral_W)
    avg_B_stars = np.mean(spiral_B)
    
    W_val = W_val + (avg_W_stars - W_val) * 0.01
    B_val = B_val + (avg_B_stars - B_val) * 0.01
    W_val = max(0.01, min(1.0, W_val))
    B_val = max(0.01, min(1.0, B_val))
    
    S = W_val * B_val
    E_val = E_val + 0.03 * (S - E_val)
    
    # Events
    if random.random() < 0.004: B_val *= random.uniform(0.3, 0.6); phase = 'Shock'
    if random.random() < 0.002: W_val = min(1.0, W_val * random.uniform(1.3, 2.0)); phase = 'Awakening'
    if S < 0.1 and random.random() < 0.15: W_val, B_val = random.uniform(0.5, 0.9), random.uniform(0.5, 0.9); phase = 'Rebirth'
    if ك_val > 1.3 and random.random() < 0.01: W_val *= 0.3; B_val *= 0.3; phase = 'Collapse'
    if ك_val < 0.3 and W_val > 0.7: phase = 'Renaissance'
    elif 0.3 <= ك_val <= 0.7: phase = 'Balance'
    elif ك_val > 0.7 and S < 0.4: phase = 'Istidraj'
    
    W_val = W_val - 0.015 * E_val + 0.03 / (S + 0.1) - 0.008 * (1 - B_val)
    B_val = B_val - 0.015 * E_val + 0.008 * (1 - B_val) * W_val * (1 - W_val)
    W_val = max(0.01, min(1.0, W_val)); B_val = max(0.01, min(1.0, B_val))
    ك_val = max(0.01, min(2.0, ك_val + 0.015 * (S - ك_val)))
    حسنات += W_val * 0.1; سيئات += (1 - B_val) * 0.1; ميزان = حسنات - سيئات
    
    # Proof data
    proof_counter += 1
    if proof_counter % 3 == 0:
        proof_data_S.append(S)
        proof_data_E.append(E_val)
        proof_x.append(len(proof_x))
        if len(proof_x) > 200:
            proof_data_S.pop(0); proof_data_E.pop(0); proof_x.pop(0)
        proof_S_line.set_data(proof_x, proof_data_S)
        proof_E_line.set_data(proof_x, proof_data_E)
    
    # ===== Planetary Motion – مدارات ديناميكية =====
    # W: كلما زاد W، صغر نصف القطر وزادت السرعة
    orbit_W = 8.0 - 3.0 * W_val
    base_speed_W = 0.018 + 0.04 * W_val
    noise_W = random.uniform(-0.015, 0.015) * (1 - W_val)**2
    aW += base_speed_W + noise_W
    wx = center_x + orbit_W * np.cos(aW)
    wy = center_y + orbit_W * np.sin(aW) * 0.6
    
    # B: كلما زاد B، صغر نصف القطر وزادت السرعة
    orbit_B = 5.5 - 2.0 * B_val
    base_speed_B = 0.018 + 0.04 * B_val
    noise_B = random.uniform(-0.015, 0.015) * (1 - B_val)**2
    aB -= (base_speed_B + noise_B)
    bx = center_x + orbit_B * np.cos(aB)
    by = center_y + orbit_B * np.sin(aB) * 0.6
    
    planet_W.center = (wx, wy); planet_B.center = (bx, by)
    label_W.set_position((wx, wy + 1.2)); label_B.set_position((bx, by + 1.2))
    planet_W.set_radius(0.3 + 0.8 * W_val)
    planet_B.set_radius(0.3 + 0.8 * B_val)
    
    # تحديث أفلاك المدار
    orbit_W_circle.set_radius(orbit_W)
    orbit_B_circle.set_radius(orbit_B)
    orbit_W_circle.set_alpha(0.08 + 0.15 * W_val)
    orbit_B_circle.set_alpha(0.08 + 0.15 * B_val)
    
    # ذيول المسار
    tWx.append(wx); tWy.append(wy); tBx.append(bx); tBy.append(by)
    if len(tWx) > 300: tWx.pop(0); tWy.pop(0); tBx.pop(0); tBy.pop(0)
    trail_W.set_data(tWx, tWy); trail_B.set_data(tBx, tBy)
    
    # Sun
    sun.set_radius(1.0 + 2.5 * S)
    sun_glow1.set_radius(1.5 + 3.5 * S)
    sun_glow2.set_radius(2.5 + 5.0 * S)
    sun_glow3.set_radius(4.0 + 7.0 * S)
    
    # Epic E Halo
    max_halo_radius = 14.0
    halo.set_radius(0.8 + max_halo_radius * E_val)
    halo.set_alpha(0.05 + 0.20 * E_val)
    
    # Atom & Cell
    aE_angle += 0.1; electron_r = 0.5 + 0.4 * S
    atom_electron.center = (3 + electron_r * np.cos(aE_angle), 4.5 + electron_r * np.sin(aE_angle))
    atom_nucleus.set_radius(0.2 + 0.3 * S)
    cell_membrane.set_radius(0.3 + 0.4 * S); cell_nucleus.set_radius(0.08 + 0.15 * S)
    
    # ===== نجوم النور والظلام (تعتمد على S) =====
    S_safe = max(0.01, S)
    n_gold = int(60 + 120 * S_safe)
    gx = np.random.uniform(0, 24, n_gold); gy = np.random.uniform(2, 14, n_gold)
    gs = np.random.uniform(2, 7, n_gold)
    g_alpha = 0.15 + 0.6 * S_safe
    stars_gold.set_offsets(np.c_[gx, gy]); stars_gold.set_sizes(gs); stars_gold.set_alpha(g_alpha)

    n_red = int(60 + 120 * (1 - S_safe))
    rx = np.random.uniform(0, 24, n_red); ry = np.random.uniform(2, 14, n_red)
    rs = np.random.uniform(2, 7, n_red)
    r_alpha = 0.15 + 0.6 * (1 - S_safe)
    stars_red.set_offsets(np.c_[rx, ry]); stars_red.set_sizes(rs); stars_red.set_alpha(r_alpha)
    
    # ===== Moral Interconnectedness =====
    new_W = np.copy(spiral_W)
    new_B = np.copy(spiral_B)
    
    for i in range(N_SOULS):
        distances = np.sqrt((spiral_x[i] - spiral_x)**2 + (spiral_y[i] - spiral_y)**2)
        neighbors = np.where(distances < 2.0)[0]
        neighbors = neighbors[neighbors != i]
        if len(neighbors) > 0:
            avg_W = np.mean(spiral_W[neighbors])
            avg_B = np.mean(spiral_B[neighbors])
            new_W[i] += (avg_W - spiral_W[i]) * 0.02
            new_B[i] += (avg_B - spiral_B[i]) * 0.02
    
    new_W += (W_val - new_W) * 0.005
    new_B += (B_val - new_B) * 0.005
    
    spiral_W = np.clip(new_W, 0.01, 1.0)
    spiral_B = np.clip(new_B, 0.01, 1.0)
    
    if frame % 150 == 0 and random.random() < 0.3:
        affected = np.random.choice(N_SOULS, size=40, replace=False)
        spiral_B[affected] *= random.uniform(0.4, 0.7)
    
    stability_factor = W_val * B_val
    for i in range(N_SOULS):
        soul_speed = soul_speeds[i] * (0.3 + 0.7 * stability_factor)
        soul_angles[i] += soul_speed
        orbit_radius = soul_orbits[i] * (0.8 + 0.4 * stability_factor)
        spiral_x[i] = center_x + orbit_radius * np.cos(soul_angles[i])
        spiral_y[i] = center_y + orbit_radius * np.sin(soul_angles[i]) * 0.4
    
    instability = 1 - stability_factor
    spiral_x += np.random.uniform(-0.05, 0.05, N_SOULS) * instability
    spiral_y += np.random.uniform(-0.05, 0.05, N_SOULS) * instability
    spiral_x = np.clip(spiral_x, 0.5, 23.5)
    spiral_y = np.clip(spiral_y, 2.5, 14.0)
    
    for (i, j, line) in lines:
        line.set_data([spiral_x[i], spiral_x[j]], [spiral_y[i], spiral_y[j]])
        avg_S_pair = (spiral_W[i]*spiral_B[i] + spiral_W[j]*spiral_B[j]) / 2
        line.set_alpha(0.03 + 0.3 * avg_S_pair)
        line.set_color('white' if avg_S_pair > 0.5 else '#FFD700' if avg_S_pair > 0.3 else '#FF4444')
        line.set_linewidth(0.1 + 0.6 * avg_S_pair)
    
    # ============================================
    # 🎨 نِظَامُ الألْوَان الْحَقِيقِيَّة – S = W × B
    # ============================================
    colors, edge_colors, edge_widths = [], [], []
    n_believers = n_disbelievers = n_hypocrites = 0
    
    for i in range(N_SOULS):
        w, b = spiral_W[i], spiral_B[i]
        s = w * b
        
        if s >= 0.85:
            colors.append('#FFFFFF'); edge_colors.append('#FFD700'); edge_widths.append(0.3)
            n_believers += 1
        elif s >= 0.70:
            colors.append('#FFF8DC'); edge_colors.append('#FFD700'); edge_widths.append(0.5)
            n_believers += 1
        elif s >= 0.55:
            colors.append('#FFD700'); edge_colors.append('#DAA520'); edge_widths.append(0.8)
            n_hypocrites += 1
        elif s >= 0.38:
            colors.append('#FFBF00'); edge_colors.append('#FF8C00'); edge_widths.append(1.1)
            n_hypocrites += 1
        elif s >= 0.22:
            colors.append('#FF7F00'); edge_colors.append('#FF4500'); edge_widths.append(1.5)
            n_disbelievers += 1
        elif s >= 0.10:
            colors.append('#DC143C'); edge_colors.append('#8B0000'); edge_widths.append(2.0)
            n_disbelievers += 1
        elif s >= 0.03:
            colors.append('#8B0000'); edge_colors.append('#4a0000'); edge_widths.append(2.4)
            n_disbelievers += 1
        else:
            colors.append('#1a0000'); edge_colors.append('#0a0000'); edge_widths.append(2.8)
            n_disbelievers += 1
    
    spiral_scatter.set_offsets(np.c_[spiral_x, spiral_y])
    spiral_scatter.set_color(colors)
    spiral_scatter.set_edgecolor(edge_colors)
    spiral_scatter.set_linewidths(edge_widths)
    spiral_scatter.set_alpha(0.88)
    
    # Collective effects
    total = N_SOULS
    believer_ratio = n_believers / total
    sun_brightness = 0.5 + believer_ratio * 0.5
    sun.set_alpha(sun_brightness)
    sun_glow1.set_alpha(0.1 + believer_ratio * 0.3)
    sun_glow2.set_alpha(0.03 + believer_ratio * 0.1)
    
    halo_instability = (n_hypocrites / total) * 2
    halo.set_alpha(0.05 + 0.20 * E_val + halo_instability * 0.15)
    
    # Streams
    good_n = int(avg_W_stars * 30)
    good_x = np.random.uniform(1, 16, good_n); good_y = np.random.uniform(4, 12, good_n)
    stream_gold.set_offsets(np.c_[good_x, good_y]); stream_gold.set_sizes(np.random.uniform(1, 3, good_n))
    
    bad_n = int((1-avg_B_stars) * 30)
    bad_x = np.random.uniform(8, 23, bad_n); bad_y = np.random.uniform(4, 12, bad_n)
    stream_red.set_offsets(np.c_[bad_x, bad_y]); stream_red.set_sizes(np.random.uniform(1, 3, bad_n))
    
    # Mizan Update
    good_val.set_text(f'{حسنات:.1f}'); bad_val.set_text(f'{سيئات:.1f}')
    pLy = 13.8 - 1.2 + min(حسنات/20, 0.6)
    pRy = 13.8 - 1.2 + min(سيئات/20, 0.6)
    pan_L.set_y(pLy); pan_R.set_y(pRy)
    good_val.set_y(pLy + 0.25); bad_val.set_y(pRy + 0.25)
    diff = max(-0.4, min(0.4, (سيئات-حسنات)/30))
    beam.set_ydata([13.8-diff, 13.8+diff])
    chain_L.set_ydata([13.8-diff, pLy+0.35])
    chain_R.set_ydata([13.8+diff, pRy+0.35])
    
    phase_text.set_text(f'{phase} | Believers={n_believers} Disbelievers={n_disbelievers} Hypocrites={n_hypocrites}')
    
    avg_W = np.mean(spiral_W); avg_B = np.mean(spiral_B); avg_S = avg_W * avg_B
    
    hdata.append([avg_W, avg_B, avg_S, E_val, ك_val, حسنات/100, سيئات/100, ميزان/100])
    if len(hdata) > 300: hdata.pop(0)
    if len(hdata) > 1:
        ax_heat.clear(); ax_heat.imshow(np.array(hdata).T, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1)
        ax_heat.set_yticks(range(8)); ax_heat.set_yticklabels(['W','B','S','E','ك','ح','س','م'], color='white', fontsize=5)
        ax_heat.set_xticks([]); ax_heat.set_title('Collective Vibration Heatmap', color='white', fontsize=7, pad=2)
    
    ax_counters.clear(); ax_counters.set_facecolor('#0a0a1a')
    ax_counters.set_xlim(0, 10); ax_counters.set_ylim(0, 6); ax_counters.axis('off')
    ax_counters.text(5, 5.5, 'Real Values (S = W × B)', color='white', fontsize=7, ha='center', fontweight='bold')
    ax_counters.text(5, 4.2, f'W = {avg_W:.2f} (White=Walaa)', color='#FFFFFF', fontsize=8, ha='center', fontweight='bold')
    ax_counters.text(5, 3.0, f'B = {avg_B:.2f} (Red=Baraa)', color='#FF3333', fontsize=8, ha='center', fontweight='bold')
    ax_counters.text(5, 1.8, f'S = {avg_S:.2f} (Gold=Thabat)', color='#FFD700', fontsize=8, ha='center', fontweight='bold')
    ax_counters.text(5, 0.6, f'E = {E_val:.2f} (Cyan=Tamkeen)', color='#00FFFF', fontsize=8, ha='center', fontweight='bold')
    
    return_tuple = (sun, planet_W, planet_B, halo, stars_gold, stars_red, spiral_scatter, 
                    stream_gold, stream_red, beam, chain_L, chain_R, pan_L, pan_R, 
                    good_val, bad_val, atom_electron, atom_nucleus, cell_membrane, cell_nucleus, 
                    proof_S_line, proof_E_line, orbit_W_circle, orbit_B_circle, trail_W, trail_B)
    line_artists = tuple(l[2] for l in lines)
    return return_tuple + line_artists

ani = FuncAnimation(fig, update, frames=8000, interval=22, repeat=True)
plt.show()
