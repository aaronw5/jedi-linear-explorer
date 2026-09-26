"""Simplified additive jet-tagging formula (main result, from 641 terms / 69 quantities)
250 terms, 366 if-conditions, 39 quantities.
Each neuron: z = intercept + terms;  h = max(0, z) (then the network's fixed-point rounding);
the 16 h go through the network's own fixed last layer to 5 class scores (g, q, W, Z, t); predicted class = argmax.

Quantities (variable: meaning):
    C2                     C2
    D2                     D2
    LHA                    LHA = Σᵢ zᵢ(ΔRᵢ/0.8)^½
    centroid_offset        √((Σᵢ zᵢΔηᵢ)² + (Σᵢ zᵢΔφᵢ)²)
    dr_0                   ΔR of particle 0
    dr_7                   ΔR of particle 7
    e2                     Σᵢ<ⱼ pTᵢpTⱼ·ΔRᵢⱼ / (Σᵢ pTᵢ)²
    e2_sq                  Σᵢ<ⱼ zᵢzⱼΔRᵢⱼ²
    eccentricity           1 − λ₂/λ₁
    girth                  Σᵢ pTᵢ·ΔRᵢ / Σᵢ pTᵢ
    girth2                 Σᵢ pTᵢ·ΔRᵢ² / Σᵢ pTᵢ
    girth2_top3            Σ zΔR² of the 3 hardest particles
    lam1                   λ₁
    lam2                   λ₂
    log_sum_pt             log Σᵢ pTᵢ
    mass                   mass
    mass_over_sum_pt       m / Σᵢ pTᵢ
    max_dr                 maxᵢ ΔRᵢ
    n_dr_0_0p05            Σᵢ [0 ≤ ΔRᵢ < 0.05]
    n_dr_0p05_0p1          Σᵢ [0.05 ≤ ΔRᵢ < 0.1]
    n_dr_0p2_0p4           Σᵢ [0.2 ≤ ΔRᵢ < 0.4]
    n_pt_above_50          Σᵢ [pTᵢ > 50 GeV]
    phi_1                  Δφ of particle 1
    planar_flow            planar flow 4λ₁λ₂/(λ₁+λ₂)²
    pt_0                   pT of particle 0
    pt_7                   pT of particle 7
    sum_pt                 Σᵢ pTᵢ
    sum_pt_top2            Σ pT of the 2 hardest particles
    sum_pt_top3            Σ pT of the 3 hardest particles
    sum_pt_top5            Σ pT of the 5 hardest particles
    tau21                  τ21
    tau32                  τ32
    width                  λ₁ + λ₂
    z_4                    pT share of particle 4
    z_7                    pT share of particle 7
    z_dr_0_0p05            Σᵢ pTᵢ·[0 ≤ ΔRᵢ < 0.05] / Σᵢ pTᵢ
    z_dr_0p05_0p1          Σᵢ pTᵢ·[0.05 ≤ ΔRᵢ < 0.1] / Σᵢ pTᵢ
    z_dr_0p1_0p2           Σᵢ pTᵢ·[0.1 ≤ ΔRᵢ < 0.2] / Σᵢ pTᵢ
    z_dr_0p2_0p4           Σᵢ pTᵢ·[0.2 ≤ ΔRᵢ < 0.4] / Σᵢ pTᵢ
"""
import math

K = [[-0.15625, 0.0, 0.34375, 0.0, 0.015625], [0.390625, 0.0, -0.03125, 0.125, 0.0], [0.4296875, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, -0.5, -0.5625, 0.0625], [-0.03125, -0.09375, 0.0, 0.078125, 0.125], [-0.1875, 0.046875, 0.0, 0.015625, -0.25], [0.109375, 0.125, -0.3125, -0.375, 0.0], [0.0, 0.0, 0.21875, 0.46875, 0.0], [0.0, 0.0625, -0.25, 0.0, 0.1875], [0.171875, 0.25390625, -0.03125, -0.03125, 0.0], [0.0, -0.125, 0.0, 0.0, 0.375], [0.0, 0.0, 0.375, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, -0.5], [0.0, 0.0, 0.0703125, 0.0546875, -0.40625], [0.0, 0.0, -0.75, 0.375, 0.0], [0.0, 0.0625, -0.6875, -0.15625, 0.0]]
B = [-0.4375, 0.03125, -0.125, -0.09375, 1.34375]
INT_BITS = [3, 5, 4, 4, 5, 5, 4, 4, 3, 4, 5, 4, 5, 4, 3, 3]
FRAC_BITS = [3, 3, 4, 3, 2, 3, 3, 3, 3, 2, 4, 4, 3, 3, 4, 3]
CLASSES = ['g', 'q', 'W', 'Z', 't']


def neuron_0(D2, centroid_offset, eccentricity, girth, girth2, lam1, mass, phi_1, planar_flow, pt_7, sum_pt, sum_pt_top2, sum_pt_top5, width, z_7, z_dr_0_0p05):
    z = -0.48
    # centroid_offset
    if centroid_offset < 0.0338: z += 71 * (0.0338 - centroid_offset)
    # eccentricity
    if eccentricity > 0.997: z += 499 * (eccentricity - 0.997)
    # girth
    if girth < 0.0775: z += -56.8 * (0.0775 - girth)
    # girth2
    if girth2 < 0.0121: z += 301 * (0.0121 - girth2)
    # mass
    if mass < 22.5: z += -0.543 * (22.5 - mass)
    if mass < 71.3: z += -0.0265 * (71.3 - mass)
    # sum_pt
    if sum_pt > 895: z += -0.0276 * (sum_pt - 895)
    # width
    if width < 0.00449: z += -799 * (0.00449 - width)
    # z_dr_0_0p05
    if z_dr_0_0p05 > 0.852: z += 15.4 * (z_dr_0_0p05 - 0.852)
    # two-condition terms
    if girth2 < 0.0197 and eccentricity > 0.961: z += 3910 * (0.0197 - girth2) * (eccentricity - 0.961)
    if lam1 < 0.00645 and D2 < 0.886: z += -2060 * (0.00645 - lam1) * (0.886 - D2)
    if mass < 30 and D2 < 0.91: z += -2.9 * (30 - mass) * (0.91 - D2)
    if mass < 64.8 and centroid_offset > 0.0106: z += 2.55 * (64.8 - mass) * (centroid_offset - 0.0106)
    if mass < 29.3 and phi_1 > -0.0771: z += -4.03 * (29.3 - mass) * (phi_1 + 0.0771)
    if mass < 64.9 and pt_7 < 40.1: z += -0.0022 * (64.9 - mass) * (40.1 - pt_7)
    if planar_flow < 0.148 and sum_pt_top2 < 388: z += -0.0518 * (0.148 - planar_flow) * (388 - sum_pt_top2)
    if sum_pt > 871 and pt_7 < 27.8: z += 0.00176 * (sum_pt - 871) * (27.8 - pt_7)
    if sum_pt_top5 > 655 and z_7 > 0.0266: z += -0.514 * (sum_pt_top5 - 655) * (z_7 - 0.0266)
    return max(0.0, z)


def neuron_1(C2, centroid_offset, e2, e2_sq, eccentricity, girth2_top3, lam1, lam2, log_sum_pt, mass, max_dr, n_pt_above_50, planar_flow, pt_7, tau32, width, z_7):
    z = 1.2
    # C2
    if C2 < 0.0491: z += -23.7 * (0.0491 - C2)
    # e2_sq
    if e2_sq < 0.00775: z += 470 * (0.00775 - e2_sq)
    # log_sum_pt
    if log_sum_pt > 6.41: z += 4.58 * (log_sum_pt - 6.41)
    # max_dr
    if max_dr < 0.0455: z += -63.3 * (0.0455 - max_dr)
    # pt_7
    if pt_7 > 30.4: z += 0.115 * (pt_7 - 30.4)
    # width
    if width < 0.009: z += -657 * (0.009 - width)
    # z_7
    if z_7 < 0.0562: z += -33.7 * (0.0562 - z_7)
    # two-condition terms
    if e2 < 0.0384 and eccentricity > 0.979: z += 6000 * (0.0384 - e2) * (eccentricity - 0.979)
    if e2 > 0.031 and tau32 < 0.629: z += -82.7 * (e2 - 0.031) * (0.629 - tau32)
    if e2_sq < 0.00778 and planar_flow < 0.0847: z += -8390 * (0.00778 - e2_sq) * (0.0847 - planar_flow)
    if lam1 < 0.0083 and centroid_offset > 0.021: z += 1.43e+04 * (0.0083 - lam1) * (centroid_offset - 0.021)
    if log_sum_pt > 6.4 and centroid_offset < 0.0235: z += -235 * (log_sum_pt - 6.4) * (0.0235 - centroid_offset)
    if log_sum_pt > 6.6 and girth2_top3 < 0.0063: z += -1090 * (log_sum_pt - 6.6) * (0.0063 - girth2_top3)
    if log_sum_pt > 6.59 and lam2 < 0.0012: z += 1.03e+04 * (log_sum_pt - 6.59) * (0.0012 - lam2)
    if log_sum_pt > 6.33 and max_dr < 0.191: z += 19 * (log_sum_pt - 6.33) * (0.191 - max_dr)
    if log_sum_pt > 6.59 and n_pt_above_50 > 7.01: z += -7.05 * (log_sum_pt - 6.59) * (n_pt_above_50 - 7.01)
    if pt_7 > 32.9 and centroid_offset > 0.0144: z += 1.53 * (pt_7 - 32.9) * (centroid_offset - 0.0144)
    if pt_7 > 29.2 and mass < 97: z += -0.00155 * (pt_7 - 29.2) * (97 - mass)
    return max(0.0, z)


def neuron_2(C2, LHA, centroid_offset, girth2, lam1, log_sum_pt, max_dr, planar_flow, pt_7, sum_pt, z_7):
    z = 3.38
    # LHA
    if LHA > 0.116: z += -7.91 * (LHA - 0.116)
    # girth2
    if girth2 < 4.87e-05: z += -5.41e+04 * (4.87e-05 - girth2)
    # lam1
    if lam1 < 0.0053: z += 267 * (0.0053 - lam1)
    # log_sum_pt
    if log_sum_pt > 6.83: z += 11.4 * (log_sum_pt - 6.83)
    if log_sum_pt > 6.89: z += -13.7 * (log_sum_pt - 6.89)
    if log_sum_pt < 6.46: z += 4.86 * (6.46 - log_sum_pt)
    # planar_flow
    if planar_flow < 0.654: z += -0.791 * (0.654 - planar_flow)
    # pt_7
    if pt_7 > 30.2: z += 0.173 * (pt_7 - 30.2)
    if pt_7 < 54.2: z += -0.0503 * (54.2 - pt_7)
    # sum_pt
    if sum_pt < 788: z += 0.00563 * (788 - sum_pt)
    # z_7
    if z_7 > 0.045: z += -45.7 * (z_7 - 0.045)
    if z_7 < 0.0185: z += -303 * (0.0185 - z_7)
    # two-condition terms
    if lam1 < 0.00374 and centroid_offset < 0.00583: z += -3.21e+04 * (0.00374 - lam1) * (0.00583 - centroid_offset)
    if pt_7 > 29.6 and C2 < 0.0514: z += -1.91 * (pt_7 - 29.6) * (0.0514 - C2)
    if pt_7 > 29.2 and max_dr > 0.0755: z += -0.564 * (pt_7 - 29.2) * (max_dr - 0.0755)
    return max(0.0, z)


def neuron_3(LHA, centroid_offset, dr_7, e2, eccentricity, girth2, lam1, mass, mass_over_sum_pt, max_dr, n_dr_0_0p05, tau32, z_dr_0p1_0p2):
    z = 2.9
    # centroid_offset
    if centroid_offset > 0.0103: z += 49.3 * (centroid_offset - 0.0103)
    # e2
    if e2 > 0.0278: z += -126 * (e2 - 0.0278)
    if e2 < 0.0433: z += 179 * (0.0433 - e2)
    # girth2
    if girth2 < 0.00905: z += -833 * (0.00905 - girth2)
    if girth2 < 0.0126: z += -441 * (0.0126 - girth2)
    # mass
    if mass > 71.9: z += -0.0685 * (mass - 71.9)
    # two-condition terms
    if LHA > 0.316 and eccentricity > 0.953: z += 1090 * (LHA - 0.316) * (eccentricity - 0.953)
    if LHA > 0.308 and max_dr < 0.156: z += -1610 * (LHA - 0.308) * (0.156 - max_dr)
    if e2 < 0.0435 and z_dr_0p1_0p2 > 0.000595: z += -328 * (0.0435 - e2) * (z_dr_0p1_0p2 - 0.000595)
    if lam1 > 0.0152 and eccentricity > 0.951: z += -1.21e+04 * (lam1 - 0.0152) * (eccentricity - 0.951)
    if mass > 62 and max_dr < 0.176: z += 2.06 * (mass - 62) * (0.176 - max_dr)
    if mass_over_sum_pt > 0.0682 and dr_7 < 0.0419: z += -7530 * (mass_over_sum_pt - 0.0682) * (0.0419 - dr_7)
    if mass_over_sum_pt > 0.0909 and max_dr < 0.148: z += 9260 * (mass_over_sum_pt - 0.0909) * (0.148 - max_dr)
    if mass_over_sum_pt > 0.0616 and n_dr_0_0p05 < 5.99: z += 10.8 * (mass_over_sum_pt - 0.0616) * (5.99 - n_dr_0_0p05)
    if mass_over_sum_pt > 0.0749 and tau32 < 0.529: z += -133 * (mass_over_sum_pt - 0.0749) * (0.529 - tau32)
    return max(0.0, z)


def neuron_4(C2, lam2, mass, mass_over_sum_pt, max_dr, planar_flow, pt_7, sum_pt_top5, tau21, width):
    z = 2.33
    # C2
    if C2 > 0.00878: z += -57.4 * (C2 - 0.00878)
    # lam2
    if lam2 < 0.000389: z += -6470 * (0.000389 - lam2)
    # mass_over_sum_pt
    if mass_over_sum_pt > 0.0885: z += -174 * (mass_over_sum_pt - 0.0885)
    if mass_over_sum_pt < 0.111: z += 41.6 * (0.111 - mass_over_sum_pt)
    # sum_pt_top5
    if sum_pt_top5 < 486: z += 0.0167 * (486 - sum_pt_top5)
    # tau21
    if tau21 < 0.279: z += 15.5 * (0.279 - tau21)
    # width
    if width > 0.00219: z += 393 * (width - 0.00219)
    # two-condition terms
    if C2 > 0.0157 and pt_7 > 39.7: z += 11 * (C2 - 0.0157) * (pt_7 - 39.7)
    if max_dr > 0.109 and pt_7 > 39.2: z += -2.35 * (max_dr - 0.109) * (pt_7 - 39.2)
    if tau21 < 0.285 and mass < 66.2: z += -0.609 * (0.285 - tau21) * (66.2 - mass)
    if tau21 < 0.243 and planar_flow > 0.0325: z += 54.6 * (0.243 - tau21) * (planar_flow - 0.0325)
    if tau21 < 0.246 and pt_7 > 34.2: z += 0.67 * (0.246 - tau21) * (pt_7 - 34.2)
    return max(0.0, z)


def neuron_5(LHA, centroid_offset, dr_0, e2, girth2, girth2_top3, lam1, lam2, log_sum_pt, sum_pt, sum_pt_top2, width, z_7):
    z = 0.465
    # dr_0
    if dr_0 < 0.0238: z += -169 * (0.0238 - dr_0)
    # e2
    if e2 < 0.0374: z += 106 * (0.0374 - e2)
    # girth2
    if girth2 < 6.4e-05: z += 3.15e+04 * (6.4e-05 - girth2)
    # log_sum_pt
    if log_sum_pt > 6.89: z += -67.9 * (log_sum_pt - 6.89)
    # z_7
    if z_7 < 0.0333: z += 185 * (0.0333 - z_7)
    if z_7 < 0.0683: z += 107 * (0.0683 - z_7)
    # two-condition terms
    if LHA < 0.221 and log_sum_pt < 6.79: z += -90.9 * (0.221 - LHA) * (6.79 - log_sum_pt)
    if e2 < 0.0338 and lam2 < 7.09e-05: z += 6.85e+05 * (0.0338 - e2) * (7.09e-05 - lam2)
    if log_sum_pt > 6.6 and dr_0 < 0.0225: z += 757 * (log_sum_pt - 6.6) * (0.0225 - dr_0)
    if log_sum_pt > 6.59 and lam1 < 0.0124: z += -982 * (log_sum_pt - 6.59) * (0.0124 - lam1)
    if sum_pt_top2 < 546 and girth2_top3 < 0.00383: z += -1.79 * (546 - sum_pt_top2) * (0.00383 - girth2_top3)
    if width < 0.00267 and centroid_offset < 0.0234: z += 7.52e+04 * (0.00267 - width) * (0.0234 - centroid_offset)
    if z_7 < 0.0707 and centroid_offset < 0.0301: z += -3370 * (0.0707 - z_7) * (0.0301 - centroid_offset)
    if z_7 < 0.0684 and sum_pt < 803: z += -0.278 * (0.0684 - z_7) * (803 - sum_pt)
    return max(0.0, z)


def neuron_6(C2, centroid_offset, e2, e2_sq, girth, girth2, lam1, lam2, log_sum_pt, mass, mass_over_sum_pt, max_dr, pt_7, tau32, width, z_7, z_dr_0p05_0p1, z_dr_0p1_0p2):
    z = 6.56
    # C2
    if C2 > 0.0101: z += -20.8 * (C2 - 0.0101)
    # centroid_offset
    if centroid_offset > 0.0212: z += -59.4 * (centroid_offset - 0.0212)
    # e2
    if e2 < 0.0508: z += 85.7 * (0.0508 - e2)
    # e2_sq
    if e2_sq < 0.00328: z += 626 * (0.00328 - e2_sq)
    # girth
    if girth > 0.0868: z += 126 * (girth - 0.0868)
    # girth2
    if girth2 < 0.00862: z += -1680 * (0.00862 - girth2)
    # lam1
    if lam1 < 0.00802: z += 919 * (0.00802 - lam1)
    # lam2
    if lam2 > 0.0029: z += -1090 * (lam2 - 0.0029)
    if lam2 < 0.000518: z += -2400 * (0.000518 - lam2)
    # mass_over_sum_pt
    if mass_over_sum_pt > 0.00941: z += -53.2 * (mass_over_sum_pt - 0.00941)
    # max_dr
    if max_dr > 0.0279: z += 14.7 * (max_dr - 0.0279)
    # width
    if width < 0.0133: z += -540 * (0.0133 - width)
    # two-condition terms
    if C2 > 0.0103 and pt_7 > 32.6: z += 2.56 * (C2 - 0.0103) * (pt_7 - 32.6)
    if centroid_offset > 0.00781 and lam2 < 0.00351: z += 1.98e+04 * (centroid_offset - 0.00781) * (0.00351 - lam2)
    if e2 < 0.0502 and z_dr_0p1_0p2 > 0.159: z += 766 * (0.0502 - e2) * (z_dr_0p1_0p2 - 0.159)
    if log_sum_pt < 6.57 and pt_7 < 45.4: z += 0.343 * (6.57 - log_sum_pt) * (45.4 - pt_7)
    if log_sum_pt < 6.31 and z_7 < 0.0712: z += 1090 * (6.31 - log_sum_pt) * (0.0712 - z_7)
    if log_sum_pt < 6.71 and z_7 < 0.0492: z += 833 * (6.71 - log_sum_pt) * (0.0492 - z_7)
    if mass < 46.6 and z_dr_0p05_0p1 < 0.8: z += 0.0576 * (46.6 - mass) * (0.8 - z_dr_0p05_0p1)
    if mass_over_sum_pt > 0.0171 and tau32 < 0.53: z += -68.7 * (mass_over_sum_pt - 0.0171) * (0.53 - tau32)
    return max(0.0, z)


def neuron_7(C2, D2, centroid_offset, e2, e2_sq, eccentricity, girth, girth2, lam1, mass, mass_over_sum_pt, planar_flow, pt_0, pt_7, sum_pt, width):
    z = 4.74
    # centroid_offset
    if centroid_offset < 0.0201: z += -37.9 * (0.0201 - centroid_offset)
    # e2
    if e2 < 0.0253: z += 56.5 * (0.0253 - e2)
    if e2 < 0.0372: z += 81.6 * (0.0372 - e2)
    # e2_sq
    if e2_sq < 0.00115: z += 1320 * (0.00115 - e2_sq)
    # girth
    if girth < 0.089: z += -40.9 * (0.089 - girth)
    # girth2
    if girth2 > 0.00445: z += -765 * (girth2 - 0.00445)
    if girth2 < 0.000708: z += -2290 * (0.000708 - girth2)
    # mass
    if mass > 80.4: z += -0.206 * (mass - 80.4)
    # mass_over_sum_pt
    if mass_over_sum_pt > 0.0729: z += 183 * (mass_over_sum_pt - 0.0729)
    if mass_over_sum_pt > 0.0906: z += -185 * (mass_over_sum_pt - 0.0906)
    # planar_flow
    if planar_flow < 0.184: z += -7.43 * (0.184 - planar_flow)
    # width
    if width < 0.00564: z += -1070 * (0.00564 - width)
    # two-condition terms
    if centroid_offset < 0.0228 and C2 > 0.0245: z += 1100 * (0.0228 - centroid_offset) * (C2 - 0.0245)
    if centroid_offset > 0.0311 and pt_0 > 375: z += -8.88 * (centroid_offset - 0.0311) * (pt_0 - 375)
    if e2 < 0.0513 and D2 < 1.1: z += 120 * (0.0513 - e2) * (1.1 - D2)
    if girth2 > 0.0044 and eccentricity > 0.945: z += 1.06e+04 * (girth2 - 0.0044) * (eccentricity - 0.945)
    if lam1 < 0.00797 and D2 < 1.06: z += -754 * (0.00797 - lam1) * (1.06 - D2)
    if mass > 80.4 and eccentricity > 0.928: z += -2.23 * (mass - 80.4) * (eccentricity - 0.928)
    if planar_flow < 0.179 and sum_pt > 607: z += 0.0407 * (0.179 - planar_flow) * (sum_pt - 607)
    if planar_flow < 0.205 and width > 0.00768: z += -3780 * (0.205 - planar_flow) * (width - 0.00768)
    if pt_7 < 44.5 and planar_flow < 0.596: z += -0.0953 * (44.5 - pt_7) * (0.596 - planar_flow)
    return max(0.0, z)


def neuron_8(LHA, centroid_offset, e2, girth, girth2, lam1, lam2, log_sum_pt, mass, planar_flow, pt_7, sum_pt, width, z_dr_0p2_0p4):
    z = 0.104
    # centroid_offset
    if centroid_offset < 0.00366: z += 477 * (0.00366 - centroid_offset)
    # log_sum_pt
    if log_sum_pt > 6.71: z += -11.6 * (log_sum_pt - 6.71)
    # pt_7
    if pt_7 > 37.1: z += -0.0426 * (pt_7 - 37.1)
    # two-condition terms
    if LHA < 0.198 and lam2 < 0.000321: z += -1.69e+05 * (0.198 - LHA) * (0.000321 - lam2)
    if e2 < 0.0218 and sum_pt > 830: z += 0.561 * (0.0218 - e2) * (sum_pt - 830)
    if girth < 0.0603 and lam1 > 0.00119: z += -3.27e+04 * (0.0603 - girth) * (lam1 - 0.00119)
    if girth2 < 0.00621 and planar_flow < 0.453: z += 1240 * (0.00621 - girth2) * (0.453 - planar_flow)
    if mass < 20.2 and centroid_offset > 0.0163: z += -15.2 * (20.2 - mass) * (centroid_offset - 0.0163)
    if width < 0.00544 and centroid_offset > 0.00598: z += -7.67e+04 * (0.00544 - width) * (centroid_offset - 0.00598)
    if width < 0.00506 and z_dr_0p2_0p4 < 0.0996: z += 1.29e+04 * (0.00506 - width) * (0.0996 - z_dr_0p2_0p4)
    return max(0.0, z)


def neuron_9(centroid_offset, girth2, lam2, log_sum_pt, mass, max_dr, n_dr_0p2_0p4, pt_7, width, z_4):
    z = -2.22
    # centroid_offset
    if centroid_offset < 0.0174: z += 170 * (0.0174 - centroid_offset)
    # lam2
    if lam2 > 0.00136: z += 1500 * (lam2 - 0.00136)
    # log_sum_pt
    if log_sum_pt > 6.36: z += -4.6 * (log_sum_pt - 6.36)
    # mass
    if mass < 31.3: z += -0.136 * (31.3 - mass)
    # max_dr
    if max_dr < 0.257: z += 14.7 * (0.257 - max_dr)
    # n_dr_0p2_0p4
    if n_dr_0p2_0p4 > 1: z += 1.23 * (n_dr_0p2_0p4 - 1)
    # width
    if width < 0.00662: z += 1550 * (0.00662 - width)
    # two-condition terms
    if centroid_offset < 0.019 and z_4 > 0.031: z += -1420 * (0.019 - centroid_offset) * (z_4 - 0.031)
    if girth2 > 0.0184 and pt_7 < 29.8: z += 59.4 * (girth2 - 0.0184) * (29.8 - pt_7)
    if mass < 51.1 and centroid_offset < 0.0241: z += 5.63 * (51.1 - mass) * (0.0241 - centroid_offset)
    if mass < 49.9 and log_sum_pt < 6.79: z += 0.208 * (49.9 - mass) * (6.79 - log_sum_pt)
    if width < 0.00676 and centroid_offset > 0.00285: z += -4.34e+04 * (0.00676 - width) * (centroid_offset - 0.00285)
    return max(0.0, z)


def neuron_10(C2, LHA, e2, eccentricity, girth2, lam1, lam2, log_sum_pt, mass, mass_over_sum_pt, n_dr_0p05_0p1, n_dr_0p2_0p4, sum_pt, tau21, tau32, z_dr_0p2_0p4):
    z = 1.73
    # C2
    if C2 > 0.0596: z += 27.9 * (C2 - 0.0596)
    # e2
    if e2 > 0.0458: z += 61.3 * (e2 - 0.0458)
    if e2 < 0.0467: z += -70.6 * (0.0467 - e2)
    # girth2
    if girth2 < 0.00182: z += -1260 * (0.00182 - girth2)
    # lam2
    if lam2 > 0.000227: z += 514 * (lam2 - 0.000227)
    # log_sum_pt
    if log_sum_pt > 6.69: z += -6.91 * (log_sum_pt - 6.69)
    if log_sum_pt < 6.24: z += -3.17 * (6.24 - log_sum_pt)
    # mass
    if mass > 9.7: z += 0.0236 * (mass - 9.7)
    # mass_over_sum_pt
    if mass_over_sum_pt < 0.0966: z += 31.9 * (0.0966 - mass_over_sum_pt)
    # n_dr_0p05_0p1
    if n_dr_0p05_0p1 < 2.95: z += 0.324 * (2.95 - n_dr_0p05_0p1)
    # n_dr_0p2_0p4
    if n_dr_0p2_0p4 > 1.56: z += 0.519 * (n_dr_0p2_0p4 - 1.56)
    # tau32
    if tau32 < 0.271: z += 12.1 * (0.271 - tau32)
    # two-condition terms
    if LHA > 0.301 and tau21 < 0.699: z += -42.4 * (LHA - 0.301) * (0.699 - tau21)
    if eccentricity > 0.901 and z_dr_0p2_0p4 < 0.0539: z += 259 * (eccentricity - 0.901) * (0.0539 - z_dr_0p2_0p4)
    if lam1 < 0.004 and log_sum_pt > 6.69: z += 3650 * (0.004 - lam1) * (log_sum_pt - 6.69)
    if lam1 < 0.00395 and sum_pt > 989: z += -9.18 * (0.00395 - lam1) * (sum_pt - 989)
    if lam2 > 8.42e-05 and tau21 < 0.518: z += 2350 * (lam2 - 8.42e-05) * (0.518 - tau21)
    if tau32 < 0.29 and n_dr_0p2_0p4 < 2: z += -4.11 * (0.29 - tau32) * (2 - n_dr_0p2_0p4)
    return max(0.0, z)


def neuron_11(C2, LHA, centroid_offset, girth, log_sum_pt, mass, max_dr, n_pt_above_50, planar_flow, sum_pt_top5, width):
    z = -1.15
    # C2
    if C2 < 0.0355: z += -19.1 * (0.0355 - C2)
    # LHA
    if LHA < 0.157: z += -22.8 * (0.157 - LHA)
    # centroid_offset
    if centroid_offset > 0.0144: z += -73.1 * (centroid_offset - 0.0144)
    if centroid_offset < 0.0498: z += 101 * (0.0498 - centroid_offset)
    # girth
    if girth > 0.0766: z += -81.5 * (girth - 0.0766)
    if girth < 0.0883: z += -84.9 * (0.0883 - girth)
    # planar_flow
    if planar_flow < 0.271: z += 8.98 * (0.271 - planar_flow)
    # sum_pt_top5
    if sum_pt_top5 < 688: z += 0.00545 * (688 - sum_pt_top5)
    # width
    if width < 0.00365: z += -514 * (0.00365 - width)
    if width < 0.0087: z += 1070 * (0.0087 - width)
    # two-condition terms
    if centroid_offset < 0.0437 and log_sum_pt < 6.84: z += -101 * (0.0437 - centroid_offset) * (6.84 - log_sum_pt)
    if girth > 0.0771 and n_pt_above_50 < 7.47: z += 12.6 * (girth - 0.0771) * (7.47 - n_pt_above_50)
    if planar_flow < 0.254 and mass < 66.7: z += -0.128 * (0.254 - planar_flow) * (66.7 - mass)
    if planar_flow < 0.281 and max_dr > 0.114: z += -57.9 * (0.281 - planar_flow) * (max_dr - 0.114)
    if planar_flow < 0.217 and width > 0.0053: z += -1310 * (0.217 - planar_flow) * (width - 0.0053)
    return max(0.0, z)


def neuron_12(e2, girth2, lam2, mass, pt_7):
    z = -0.91
    # e2
    if e2 > 0.0622: z += -124 * (e2 - 0.0622)
    # girth2
    if girth2 > 0.0188: z += 220 * (girth2 - 0.0188)
    # mass
    if mass > 91.2: z += 0.0778 * (mass - 91.2)
    # two-condition terms
    if girth2 > 0.0186 and lam2 > 0.000489: z += 1.53e+04 * (girth2 - 0.0186) * (lam2 - 0.000489)
    if girth2 > 0.0197 and pt_7 > 16.1: z += 6.92 * (girth2 - 0.0197) * (pt_7 - 16.1)
    return max(0.0, z)


def neuron_13(C2, e2, girth, log_sum_pt, max_dr, n_pt_above_50, pt_0, pt_7, sum_pt, sum_pt_top5, tau21, width, z_4, z_7):
    z = 1.68
    # C2
    if C2 > 0.0664: z += -52.4 * (C2 - 0.0664)
    # e2
    if e2 < 0.0509: z += -88.6 * (0.0509 - e2)
    # girth
    if girth < 0.15: z += 67 * (0.15 - girth)
    # pt_0
    if pt_0 > 179: z += 0.0022 * (pt_0 - 179)
    # pt_7
    if pt_7 < 24.8: z += -0.246 * (24.8 - pt_7)
    # sum_pt
    if sum_pt > 998: z += -0.0241 * (sum_pt - 998)
    # width
    if width < 0.0159: z += 217 * (0.0159 - width)
    # two-condition terms
    if girth < 0.156 and log_sum_pt < 6.91: z += -41.1 * (0.156 - girth) * (6.91 - log_sum_pt)
    if girth < 0.148 and pt_7 < 39.5: z += -1.09 * (0.148 - girth) * (39.5 - pt_7)
    if sum_pt > 1070 and n_pt_above_50 > 6.01: z += 0.019 * (sum_pt - 1070) * (n_pt_above_50 - 6.01)
    if sum_pt < 764 and z_4 < 0.0379: z += 6.47 * (764 - sum_pt) * (0.0379 - z_4)
    if sum_pt_top5 > 653 and pt_7 < 42.6: z += 0.000594 * (sum_pt_top5 - 653) * (42.6 - pt_7)
    if sum_pt_top5 > 677 and z_7 > 0.0289: z += -0.566 * (sum_pt_top5 - 677) * (z_7 - 0.0289)
    if tau21 < 0.518 and max_dr > -0.0382: z += -14.9 * (0.518 - tau21) * (max_dr + 0.0382)
    return max(0.0, z)


def neuron_14(C2, D2, centroid_offset, e2, eccentricity, girth, girth2, lam1, log_sum_pt, mass, max_dr, n_dr_0p2_0p4, planar_flow, sum_pt, width, z_dr_0p05_0p1):
    z = -1.51
    # e2
    if e2 < 0.0385: z += 106 * (0.0385 - e2)
    # girth
    if girth < 0.0869: z += -80.1 * (0.0869 - girth)
    # girth2
    if girth2 < 0.0131: z += 632 * (0.0131 - girth2)
    # lam1
    if lam1 > 0.00732: z += -101 * (lam1 - 0.00732)
    # mass
    if mass > 5.61: z += 0.0187 * (mass - 5.61)
    # max_dr
    if max_dr < 0.177: z += -20.1 * (0.177 - max_dr)
    # width
    if width < 0.00741: z += -1040 * (0.00741 - width)
    # z_dr_0p05_0p1
    if z_dr_0p05_0p1 < 0.572: z += 1.85 * (0.572 - z_dr_0p05_0p1)
    # two-condition terms
    if D2 < 1.04 and centroid_offset < 0.0307: z += 38.5 * (1.04 - D2) * (0.0307 - centroid_offset)
    if e2 < 0.0382 and D2 < 0.961: z += 192 * (0.0382 - e2) * (0.961 - D2)
    if girth2 < 0.0135 and eccentricity > 0.971: z += 1.16e+04 * (0.0135 - girth2) * (eccentricity - 0.971)
    if girth2 < 0.00453 and n_dr_0p2_0p4 < 0.93: z += -486 * (0.00453 - girth2) * (0.93 - n_dr_0p2_0p4)
    if lam1 > 0.0055 and max_dr < 0.168: z += 6850 * (lam1 - 0.0055) * (0.168 - max_dr)
    if lam1 > 0.00727 and max_dr < 0.134: z += 4.3e+04 * (lam1 - 0.00727) * (0.134 - max_dr)
    if mass < 75.3 and D2 < 0.865: z += -0.0486 * (75.3 - mass) * (0.865 - D2)
    if planar_flow < 0.11 and centroid_offset > 0.00946: z += 1270 * (0.11 - planar_flow) * (centroid_offset - 0.00946)
    if planar_flow < 0.116 and centroid_offset > 0.0186: z += -1310 * (0.116 - planar_flow) * (centroid_offset - 0.0186)
    if planar_flow < 0.116 and max_dr < 0.164: z += -187 * (0.116 - planar_flow) * (0.164 - max_dr)
    if planar_flow < 0.106 and sum_pt < 740: z += -0.0507 * (0.106 - planar_flow) * (740 - sum_pt)
    if width < 0.00857 and D2 < 1.04: z += -986 * (0.00857 - width) * (1.04 - D2)
    if width < 0.00793 and log_sum_pt < 6.82: z += 381 * (0.00793 - width) * (6.82 - log_sum_pt)
    if width < 0.00758 and planar_flow < 0.109: z += -6890 * (0.00758 - width) * (0.109 - planar_flow)
    if z_dr_0p05_0p1 < 0.597 and C2 < 0.0662: z += -77 * (0.597 - z_dr_0p05_0p1) * (0.0662 - C2)
    return max(0.0, z)


def neuron_15(D2, LHA, e2, girth2_top3, lam1, log_sum_pt, mass, n_dr_0_0p05, planar_flow, sum_pt_top3, tau21, width, z_dr_0p05_0p1, z_dr_0p1_0p2, z_dr_0p2_0p4):
    z = 0.951
    # D2
    if D2 < 0.711: z += -1.98 * (0.711 - D2)
    # LHA
    if LHA > 0.342: z += -54.8 * (LHA - 0.342)
    # e2
    if e2 < 0.0244: z += 199 * (0.0244 - e2)
    if e2 < 0.041: z += 104 * (0.041 - e2)
    # girth2_top3
    if girth2_top3 < 0.00198: z += -665 * (0.00198 - girth2_top3)
    # lam1
    if lam1 < 0.00679: z += 1610 * (0.00679 - lam1)
    if lam1 < 0.00813: z += -790 * (0.00813 - lam1)
    # log_sum_pt
    if log_sum_pt > 6.9: z += 37.6 * (log_sum_pt - 6.9)
    # mass
    if mass < 37.4: z += -0.0463 * (37.4 - mass)
    # n_dr_0_0p05
    if n_dr_0_0p05 < 2.12: z += 0.454 * (2.12 - n_dr_0_0p05)
    # width
    if width < 0.00695: z += -2070 * (0.00695 - width)
    # z_dr_0p05_0p1
    if z_dr_0p05_0p1 > 0.757: z += -6.11 * (z_dr_0p05_0p1 - 0.757)
    # z_dr_0p1_0p2
    if z_dr_0p1_0p2 < 0.342: z += 3.61 * (0.342 - z_dr_0p1_0p2)
    # two-condition terms
    if LHA > 0.186 and sum_pt_top3 > 338: z += 0.0311 * (LHA - 0.186) * (sum_pt_top3 - 338)
    if mass > 80.4 and z_dr_0p2_0p4 < 0.236: z += -0.572 * (mass - 80.4) * (0.236 - z_dr_0p2_0p4)
    if tau21 < 0.26 and z_dr_0p05_0p1 < 0.513: z += -9.02 * (0.26 - tau21) * (0.513 - z_dr_0p05_0p1)
    if tau21 < 0.24 and z_dr_0p2_0p4 < 0.21: z += 62.2 * (0.24 - tau21) * (0.21 - z_dr_0p2_0p4)
    if width < 0.00788 and e2 > 0.0243: z += -3.58e+04 * (0.00788 - width) * (e2 - 0.0243)
    if width < 0.00614 and log_sum_pt > 6.9: z += -7700 * (0.00614 - width) * (log_sum_pt - 6.9)
    if width < 0.00868 and planar_flow < 0.0755: z += -3420 * (0.00868 - width) * (0.0755 - planar_flow)
    return max(0.0, z)


def rounded(h, j):
    s = 2.0 ** FRAC_BITS[j]
    return (math.floor(h * s + 0.5) / s) % (2.0 ** INT_BITS[j])


def classify(jet):
    """jet: dict quantity -> value. Returns (class index, class name)."""
    h = [
        neuron_0(jet['D2'], jet['centroid_offset'], jet['eccentricity'], jet['girth'], jet['girth2'], jet['lam1'], jet['mass'], jet['phi_1'], jet['planar_flow'], jet['pt_7'], jet['sum_pt'], jet['sum_pt_top2'], jet['sum_pt_top5'], jet['width'], jet['z_7'], jet['z_dr_0_0p05']),
        neuron_1(jet['C2'], jet['centroid_offset'], jet['e2'], jet['e2_sq'], jet['eccentricity'], jet['girth2_top3'], jet['lam1'], jet['lam2'], jet['log_sum_pt'], jet['mass'], jet['max_dr'], jet['n_pt_above_50'], jet['planar_flow'], jet['pt_7'], jet['tau32'], jet['width'], jet['z_7']),
        neuron_2(jet['C2'], jet['LHA'], jet['centroid_offset'], jet['girth2'], jet['lam1'], jet['log_sum_pt'], jet['max_dr'], jet['planar_flow'], jet['pt_7'], jet['sum_pt'], jet['z_7']),
        neuron_3(jet['LHA'], jet['centroid_offset'], jet['dr_7'], jet['e2'], jet['eccentricity'], jet['girth2'], jet['lam1'], jet['mass'], jet['mass_over_sum_pt'], jet['max_dr'], jet['n_dr_0_0p05'], jet['tau32'], jet['z_dr_0p1_0p2']),
        neuron_4(jet['C2'], jet['lam2'], jet['mass'], jet['mass_over_sum_pt'], jet['max_dr'], jet['planar_flow'], jet['pt_7'], jet['sum_pt_top5'], jet['tau21'], jet['width']),
        neuron_5(jet['LHA'], jet['centroid_offset'], jet['dr_0'], jet['e2'], jet['girth2'], jet['girth2_top3'], jet['lam1'], jet['lam2'], jet['log_sum_pt'], jet['sum_pt'], jet['sum_pt_top2'], jet['width'], jet['z_7']),
        neuron_6(jet['C2'], jet['centroid_offset'], jet['e2'], jet['e2_sq'], jet['girth'], jet['girth2'], jet['lam1'], jet['lam2'], jet['log_sum_pt'], jet['mass'], jet['mass_over_sum_pt'], jet['max_dr'], jet['pt_7'], jet['tau32'], jet['width'], jet['z_7'], jet['z_dr_0p05_0p1'], jet['z_dr_0p1_0p2']),
        neuron_7(jet['C2'], jet['D2'], jet['centroid_offset'], jet['e2'], jet['e2_sq'], jet['eccentricity'], jet['girth'], jet['girth2'], jet['lam1'], jet['mass'], jet['mass_over_sum_pt'], jet['planar_flow'], jet['pt_0'], jet['pt_7'], jet['sum_pt'], jet['width']),
        neuron_8(jet['LHA'], jet['centroid_offset'], jet['e2'], jet['girth'], jet['girth2'], jet['lam1'], jet['lam2'], jet['log_sum_pt'], jet['mass'], jet['planar_flow'], jet['pt_7'], jet['sum_pt'], jet['width'], jet['z_dr_0p2_0p4']),
        neuron_9(jet['centroid_offset'], jet['girth2'], jet['lam2'], jet['log_sum_pt'], jet['mass'], jet['max_dr'], jet['n_dr_0p2_0p4'], jet['pt_7'], jet['width'], jet['z_4']),
        neuron_10(jet['C2'], jet['LHA'], jet['e2'], jet['eccentricity'], jet['girth2'], jet['lam1'], jet['lam2'], jet['log_sum_pt'], jet['mass'], jet['mass_over_sum_pt'], jet['n_dr_0p05_0p1'], jet['n_dr_0p2_0p4'], jet['sum_pt'], jet['tau21'], jet['tau32'], jet['z_dr_0p2_0p4']),
        neuron_11(jet['C2'], jet['LHA'], jet['centroid_offset'], jet['girth'], jet['log_sum_pt'], jet['mass'], jet['max_dr'], jet['n_pt_above_50'], jet['planar_flow'], jet['sum_pt_top5'], jet['width']),
        neuron_12(jet['e2'], jet['girth2'], jet['lam2'], jet['mass'], jet['pt_7']),
        neuron_13(jet['C2'], jet['e2'], jet['girth'], jet['log_sum_pt'], jet['max_dr'], jet['n_pt_above_50'], jet['pt_0'], jet['pt_7'], jet['sum_pt'], jet['sum_pt_top5'], jet['tau21'], jet['width'], jet['z_4'], jet['z_7']),
        neuron_14(jet['C2'], jet['D2'], jet['centroid_offset'], jet['e2'], jet['eccentricity'], jet['girth'], jet['girth2'], jet['lam1'], jet['log_sum_pt'], jet['mass'], jet['max_dr'], jet['n_dr_0p2_0p4'], jet['planar_flow'], jet['sum_pt'], jet['width'], jet['z_dr_0p05_0p1']),
        neuron_15(jet['D2'], jet['LHA'], jet['e2'], jet['girth2_top3'], jet['lam1'], jet['log_sum_pt'], jet['mass'], jet['n_dr_0_0p05'], jet['planar_flow'], jet['sum_pt_top3'], jet['tau21'], jet['width'], jet['z_dr_0p05_0p1'], jet['z_dr_0p1_0p2'], jet['z_dr_0p2_0p4']),
    ]
    h = [rounded(v, j) for j, v in enumerate(h)]
    scores = [B[c] + sum(h[j] * K[j][c] for j in range(16)) for c in range(5)]
    c = max(range(5), key=lambda i: scores[i])
    return c, CLASSES[c]
