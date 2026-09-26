"""JEDI-linear jet tagger, 8 particles, 3 features: the tuned formula (start): ONE tree of if-statements on the jet quantities and on differences of additive class scores.

Input:  the 8 hardest particles of a jet, hardest first, each (pT [GeV], Δη, Δφ) relative to the jet axis;
        empty slots have pT = 0.
Output: the class (g, q, W, Z or t).

1. quantities(): physics quantities of the particles (the same as in the formula).
2. scores():     5 class scores, each a plain sum of the formula's own terms of the quantities
                 (coef * max(0, Q.x - t): only counts when x > t;  coef * max(0, t - Q.x): only when x < t).
                 Coefficients fitted on the entire training set (595,000 jets) to reproduce the formula's
                 class probabilities.
3. decide():     one tree; each test is "quantity > threshold" or "score_c - score_d > threshold".
                 Grown on the entire training set (595,000 jets), each jet labelled with the formula's class;
                 each leaf notes the share of its training jets that the formula puts in its class.

Test set (50,000 jets): accuracy 65.52% (the formula: 65.56%); same class as the formula for 95.74% of jets.  879 leaves, depth 20.
"""

import math
from types import SimpleNamespace

CLASSES = ['g', 'q', 'W', 'Z', 't']
def quantities(pt, eta, phi):
    pt, eta, phi = [float(x) for x in pt], [float(x) for x in eta], [float(x) for x in phi]
    n = len(pt)
    P = range(n)
    real = [i for i in P if pt[i] > 0]
    tot = sum(pt)
    z = [x / tot for x in pt]
    zs = sorted(z, reverse=True)
    dr = [math.hypot(eta[i], phi[i]) for i in P]

    def dist2(i, j):
        return (eta[i] - eta[j]) ** 2 + (phi[i] - phi[j]) ** 2

    def mass_of(k):
        E = sum(pt[i] * math.cosh(eta[i]) for i in range(k))
        px = sum(pt[i] * math.cos(phi[i]) for i in range(k))
        py = sum(pt[i] * math.sin(phi[i]) for i in range(k))
        pz = sum(pt[i] * math.sinh(eta[i]) for i in range(k))
        return math.sqrt(max(E * E - px * px - py * py - pz * pz, 0.0))

    def pair_mass(i, j):
        return math.sqrt(max(2 * pt[i] * pt[j] * (math.cosh(eta[i] - eta[j]) - math.cos(phi[i] - phi[j])), 0.0))

    def tau(k):
        axes = [(eta[max(P, key=lambda i: pt[i])], phi[max(P, key=lambda i: pt[i])])]
        for _ in range(1, k):
            far = max(P, key=lambda i: pt[i] * min(math.hypot(eta[i] - a, phi[i] - b) for a, b in axes))
            axes.append((eta[far], phi[far]))
        for _ in range(6):
            nearest = [min(range(k), key=lambda j: math.hypot(eta[i] - axes[j][0], phi[i] - axes[j][1])) for i in P]
            for j in range(k):
                w = sum(pt[i] for i in P if nearest[i] == j)
                if w > 0:
                    axes[j] = (sum(pt[i] * eta[i] for i in P if nearest[i] == j) / w, sum(pt[i] * phi[i] for i in P if nearest[i] == j) / w)
        return sum(z[i] * min(math.hypot(eta[i] - a, phi[i] - b) for a, b in axes) for i in P) / 0.8

    ta = sum(z[i] * eta[i] ** 2 for i in P)
    tb = sum(z[i] * eta[i] * phi[i] for i in P)
    tc = sum(z[i] * phi[i] ** 2 for i in P)
    disc = math.sqrt(max((ta - tc) ** 2 / 4 + tb ** 2, 0.0))
    lam1, lam2 = (ta + tc) / 2 + disc, max((ta + tc) / 2 - disc, 0.0)

    hard = sorted(P, key=lambda i: -pt[i])[:24]
    R = {(i, j): math.sqrt(dist2(i, j)) for i in hard for j in hard}
    e2 = sum(z[i] * z[j] * R[i, j] for i in hard for j in hard if i < j)
    e3 = sum(z[i] * z[j] * z[k] * R[i, j] * R[i, k] * R[j, k] for i in hard for j in hard for k in hard if i < j < k)

    return SimpleNamespace(
        mass_over_sum_pt_sq=(mass_of(n) / tot) ** 2,
        z_top5=sum(zs[:5]),
        eccentricity=1 - lam2 / max(lam1, 1e-12),
        C2=e3 / max(e2 ** 2, 1e-12),
        D2=e3 / max(e2 ** 3, 1e-12),
        LHA=sum(z[i] * math.sqrt(dr[i] / 0.8) for i in P),
        log_sum_pt=math.log(tot),
        mass_over_sum_pt=mass_of(n) / tot,
        mass=mass_of(n),
        mass_top2=mass_of(2),
        mass_top3=mass_of(3),
        mass_top5=mass_of(5),
        max_pair_mass=max(pair_mass(0, 1), pair_mass(0, 2), pair_mass(1, 2)),
        max_dr=max(dr[i] for i in real),
        min_pair_mass=min(pair_mass(0, 1), pair_mass(0, 2), pair_mass(1, 2)),
        m01=pair_mass(0, 1),
        m012=math.sqrt(pair_mass(0, 1) ** 2 + pair_mass(0, 2) ** 2 + pair_mass(1, 2) ** 2),
        pt_0=pt[0],
        pt_2=pt[2],
        pt_4=pt[4],
        pt_5=pt[5],
        pt_6=pt[6],
        pt_7=pt[7],
        z_4=z[4],
        z_5=z[5],
        z_6=z[6],
        z_7=z[7],
        pt1_dr01=pt[1] * math.sqrt(dist2(0, 1)),
        planar_flow=4 * (ta * tc - tb ** 2) / max((ta + tc) ** 2, 1e-12),
        dr_0=dr[0] if pt[0] > 0 else 0.0,
        dr_2=dr[2] if pt[2] > 0 else 0.0,
        dr_3=dr[3] if pt[3] > 0 else 0.0,
        dr_6=dr[6] if pt[6] > 0 else 0.0,
        dr_7=dr[7] if pt[7] > 0 else 0.0,
        dr01=math.sqrt(dist2(0, 1)),
        eta_0=eta[0],
        phi_1=phi[1],
        phi_7=phi[7],
        sum_pt_top2=sum(pt[:2]),
        sum_pt_top3=sum(pt[:3]),
        sum_pt_top5=sum(pt[:5]),
        girth2_top2=sum(pt[i] * dr[i] ** 2 for i in range(2)) / max(sum(pt[:2]), 1e-9),
        girth2_top3=sum(pt[i] * dr[i] ** 2 for i in range(3)) / max(sum(pt[:3]), 1e-9),
        girth2_top5=sum(pt[i] * dr[i] ** 2 for i in range(5)) / max(sum(pt[:5]), 1e-9),
        n_dr_0_0p05=sum(1 for i in real if 0 <= dr[i] < 0.05),
        n_dr_0p05_0p1=sum(1 for i in real if 0.05 <= dr[i] < 0.1),
        n_dr_0p1_0p2=sum(1 for i in real if 0.1 <= dr[i] < 0.2),
        n_dr_0p2_0p4=sum(1 for i in real if 0.2 <= dr[i] < 0.4),
        n_pt_above_50=sum(1 for x in pt if x > 50),
        sum_pt=tot,
        z_dr_0_0p05=sum(z[i] for i in real if 0 <= dr[i] < 0.05),
        z_dr_0p05_0p1=sum(z[i] for i in real if 0.05 <= dr[i] < 0.1),
        z_dr_0p1_0p2=sum(z[i] for i in real if 0.1 <= dr[i] < 0.2),
        z_dr_0p2_0p4=sum(z[i] for i in real if 0.2 <= dr[i] < 0.4),
        girth=sum(z[i] * dr[i] for i in P),
        girth2=sum(z[i] * dr[i] ** 2 for i in P),
        mean_eta=sum(z[i] * eta[i] for i in P),
        mean_eta2=sum(z[i] * eta[i] ** 2 for i in P),
        mean_phi=sum(z[i] * phi[i] for i in P),
        mean_phi2=sum(z[i] * phi[i] ** 2 for i in P),
        e2=e2,
        e2_sq=sum(z[i] * z[j] * dist2(i, j) for i in P for j in P if i < j),
        lam1=lam1,
        width=ta + tc,
        lam2=lam2,
        tau21=tau(2) / max(tau(1), 1e-12),
        tau32=tau(3) / max(tau(2), 1e-12),
        centroid_offset=math.hypot(sum(z[i] * eta[i] for i in P), sum(z[i] * phi[i] for i in P)),
        pt_dispersion=math.sqrt(sum(x * x for x in z)),
    )


def score_g(Q):
    return (-0.2956
        - 1.773 * max(0.0, 0.148419710734 - Q.planar_flow)
        + 66.25 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 275.7 * max(0.0, 0.004372139331 - Q.width)
        + 382.6 * max(0.0, 0.018827652745 - Q.girth2)
        + 0.01151 * max(0.0, 64.618731689453 - Q.mass)
        + 0.06415 * max(0.0, 21.784077072144 - Q.mass)
        + 17.02 * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 133.7 * max(0.0, 0.013238675334 - Q.girth2)
        + 4.821 * max(0.0, 0.006506575659 - Q.lam1)
        - 173.2 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, 0.87567204833 - Q.D2)
        + 0.2014 * max(0.0, Q.sum_pt - 901.59375)
        + 0.008923 * max(0.0, 56.920347213745 - Q.mass)
        + 19.58 * max(0.0, 0.008678044951 - Q.width)
        + 0.0001142 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 25.578125 - Q.pt_7)
        + 0.001207 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 380.5875 - Q.sum_pt_top2)
        + 0.002513 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 0.038438041256 - Q.dr_2)
        + 0.04846 * max(0.0, 56.920347213745 - Q.mass) * max(0.0, Q.C2 - 0.023843882605)
        + 29.46 * max(0.0, 0.00832969537 - Q.girth2_top5)
        + 0.1028 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971)
        + 0.02566 * max(0.0, 29.644699859619 - Q.mass)
        - 0.03623 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.87567204833 - Q.D2)
        - 24.78 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.111761856824 - Q.max_dr)
        + 0.3239 * max(0.0, 0.087236513197 - Q.girth)
        - 0.4018 * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 3380.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.centroid_offset - 0.014379521101)
        - 0.4727 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, Q.centroid_offset - 0.012587644117)
        + 17.53 * max(0.0, 0.020459658932 - Q.e2)
        + 469.0 * max(0.0, 0.008174660116 - Q.mass_over_sum_pt_sq)
        + 44.62 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.eccentricity - 0.959856212153)
        - 8.474 * max(0.0, Q.log_sum_pt - 6.638338705138)
        + 0.001732 * max(0.0, Q.sum_pt_top5 - 687.4375)
        + 0.004542 * max(0.0, 0.007929074034 - Q.girth2_top3) * max(0.0, 35.28125 - Q.pt_6)
        + 66.08 * max(0.0, 0.00543336053 - Q.lam1)
        + 1.025 * max(0.0, Q.log_sum_pt - 6.377722943814)
        - 0.1432 * max(0.0, Q.sum_pt_top5 - 687.4375) * max(0.0, Q.z_7 - 0.023207568189)
        - 77.44 * max(0.0, 0.003952581551 - Q.girth2_top3)
        + 11.14 * max(0.0, 0.076081777364 - Q.girth)
        + 0.0003876 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, 40.040625 - Q.pt_7)
        + 1.389 * max(0.0, Q.log_sum_pt - 6.638338705138) * max(0.0, 0.093979107928 - Q.dr_7)
        + 0.0291 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, Q.phi_1 - -0.058901977539)
        + 14.37 * max(0.0, 0.004372139331 - Q.width) * max(0.0, Q.n_dr_0p1_0p2 - 1.0)
        - 30.81 * max(0.0, 0.13092863437 - Q.mass_over_sum_pt)
        - 10.03 * max(0.0, 0.012569162668 - Q.planar_flow)
        + 66.21 * max(0.0, 0.008375572068 - Q.lam1)
        + 0.0522 * max(0.0, Q.pt_7 - 34.53125)
        + 5550.0 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.centroid_offset - 0.02076709205)
        - 0.0006709 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 91.19 - Q.mass)
        - 9.288 * max(0.0, 0.035560912266 - Q.e2)
        - 18.16 * max(0.0, 0.055577157257 - Q.z_7)
        + 0.6698 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, Q.centroid_offset - 0.014379521101)
        - 3.345 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.06064 * max(0.0, 53.332374954224 - Q.mass)
        + 0.0007115 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 45.595 - Q.mass_top3)
        - 4.989 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.197968879342 - Q.max_dr)
        + 4.706 * max(0.0, Q.log_sum_pt - 6.572937922293)
        - 0.0275 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 0.553068161011 - Q.tau21)
        - 845.0 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 1400.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, Q.eccentricity - 0.978160776925)
        + 0.5757 * max(0.0, 0.083662731125 - Q.planar_flow)
        + 285.0 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.042322802544 - Q.C2)
        - 0.7897 * max(0.0, 0.197783735394 - Q.tau21)
        + 39.8 * max(0.0, 0.008168570676 - Q.e2_sq)
        + 0.01367 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 0.080507021025 - Q.max_dr)
        - 0.0005949 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 32.617988451746 - Q.mass_top3)
        - 12.38 * max(0.0, 0.042322802544 - Q.C2)
        - 0.06991 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 50.25 - Q.pt_6)
        - 338.4 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006756161242 - Q.girth2_top3)
        + 2202.0 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 9196.0 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 0.000194798295 - Q.lam2)
        + 1429.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.001130644719 - Q.lam2)
        - 51.8 * max(0.0, 0.083662731125 - Q.planar_flow) * max(0.0, 0.269169217348 - Q.tau32)
        - 0.9671 * max(0.0, 0.346713497427 - Q.LHA)
        + 13.66 * max(0.0, Q.e2 - 0.032346998155)
        + 37.03 * max(0.0, Q.mass_over_sum_pt - 0.054892207095)
        + 32.79 * max(0.0, 0.346713497427 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 59.6 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 1322.0 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 29.62 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 26.03 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.033200121667 - Q.planar_flow)
        - 1.021 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.n_pt_above_50 - 7.0)
        - 2.009 * max(0.0, 0.046566883102 - Q.max_dr)
        - 17.99 * max(0.0, Q.e2 - 0.032346998155) * max(0.0, 0.641386964917 - Q.tau32)
        - 0.2488 * max(0.0, 69.611351776123 - Q.mass)
        - 0.03361 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.068101508468 - Q.z_7)
        - 5.716 * max(0.0, Q.log_sum_pt - 6.842716632804)
        + 2.053 * max(0.0, 6.464150123592 - Q.log_sum_pt)
        - 14.22 * max(0.0, 0.028070914944 - Q.z_7)
        + 60.77 * max(0.0, 0.005954149834 - Q.lam1)
        + 17380.0 * max(0.0, 9.1213921e-05 - Q.width)
        + 0.04065 * max(0.0, Q.pt_7 - 30.484375)
        - 0.5845 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, 0.051192347892 - Q.C2)
        - 8.007 * max(0.0, Q.z_7 - 0.046240320761)
        - 4553.0 * max(0.0, 0.028070914944 - Q.z_7) * max(0.0, 0.00752008842 - Q.width)
        + 0.7086 * max(0.0, Q.LHA - 0.111565049159)
        - 1004.0 * max(0.0, 0.005954149834 - Q.lam1) * max(0.0, Q.max_dr - 0.080507021025)
        - 0.2892 * max(0.0, 0.694781820497 - Q.planar_flow)
        + 0.04045 * max(0.0, 36.229410171509 - Q.mass)
        - 7.718e-05 * max(0.0, 56.53125 - Q.pt_6) * max(0.0, Q.m012 - 32.617988451746)
        + 15.29 * max(0.0, 36.229410171509 - Q.mass) * max(0.0, 0.001130644719 - Q.lam2)
        - 0.1625 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, Q.max_dr - 0.093110798299)
        - 40.6 * max(0.0, 0.003377388461 - Q.lam1)
        - 38920.0 * max(0.0, 0.003377388461 - Q.lam1) * max(0.0, 0.006789738266 - Q.centroid_offset)
        - 50.17 * max(0.0, 8.379955863953 - Q.mass) * max(0.0, 0.010960638421 - Q.centroid_offset)
        - 53.12 * max(0.0, 0.016858545121 - Q.z_7)
        - 0.00164 * max(0.0, 687.4375 - Q.sum_pt_top5)
        + 0.04483 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.04881348081 - Q.dr_7)
        - 0.04003 * max(0.0, 53.4375 - Q.pt_7)
        + 0.0137 * max(0.0, 43.5 - Q.pt_7)
        + 0.003458 * max(0.0, 788.4484375 - Q.sum_pt)
        + 3.312 * max(0.0, Q.log_sum_pt - 6.267538488641)
        + 212.6 * max(0.0, Q.log_sum_pt - 6.896095378249)
        + 6073.0 * max(0.0, 4.8108519e-05 - Q.girth2)
        - 183.2 * max(0.0, Q.log_sum_pt - 6.804164030582)
        - 2.18 * max(0.0, 0.15984864831 - Q.max_dr)
        - 0.0007036 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, Q.max_pair_mass - 13.047927274731)
        + 2179.0 * max(0.0, 0.000172198326 - Q.width) * max(0.0, 0.222994708167 - Q.dr_7)
        + 72.29 * max(0.0, Q.mass_over_sum_pt - 0.06813910019)
        - 10.34 * max(0.0, Q.centroid_offset - 0.014379521101)
        - 4.684 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.518696343899 - Q.tau32)
        - 155.6 * max(0.0, Q.width - 0.018827653081)
        - 0.06805 * max(0.0, Q.mass - 36.229410171509)
        + 3.757 * max(0.0, Q.e2 - 0.028531698044)
        - 3.527 * max(0.0, Q.LHA - 0.312727471086)
        - 18.23 * max(0.0, 0.006679471358 - Q.width)
        - 0.5442 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.n_pt_above_50 - 3.0)
        + 9.747 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.001130644719 - Q.lam2)
        - 12.66 * max(0.0, 0.04447356835 - Q.e2)
        + 57.84 * max(0.0, 0.007330079875 - Q.lam1)
        + 0.2177 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 5.0 - Q.n_dr_0_0p05)
        + 0.003212 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 50.352200171245 - Q.mass_top3)
        + 0.258 * max(0.0, Q.mass - 69.611351776123)
        + 2.302 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, 0.964120104909 - Q.z_dr_0p05_0p1)
        + 19.58 * max(0.0, 0.008678044751 - Q.girth2)
        + 2.23 * max(0.0, Q.LHA - 0.325582223496)
        - 0.001997 * max(0.0, Q.mass - 36.229410171509) * max(0.0, Q.eccentricity - 0.620723099573)
        + 3.802 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.0)
        + 0.4619 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, Q.phi_7 - -0.041534423828)
        + 0.0001136 * max(0.0, Q.mass_top5 - 53.607658247923)
        + 0.2515 * max(0.0, -0.012844925793 - Q.mean_eta)
        + 7.879 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, -0.039672851562 - Q.eta_0)
        - 147.5 * max(0.0, Q.width - 0.018827653081) * max(0.0, 0.492494773865 - Q.pt_dispersion)
        - 0.05792 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.046481671275 - Q.dr_6)
        - 20.33 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.042151962757 - Q.dr_7)
        + 37.21 * max(0.0, Q.mass_over_sum_pt - 0.090413827016)
        + 275.7 * max(0.0, 0.004372139461 - Q.girth2)
        - 74.32 * max(0.0, Q.mass_over_sum_pt - 0.107985668755)
        + 114.8 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 0.145231109113 - Q.max_dr)
        + 5.127 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.planar_flow - 0.00804883781)
        - 21.75 * max(0.0, Q.lam1 - 0.012003726523)
        + 325.4 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 0.145231109113 - Q.max_dr)
        + 0.1819 * max(0.0, Q.mass - 69.611351776123) * max(0.0, 0.177304983139 - Q.max_dr)
        - 0.9667 * max(0.0, Q.max_dr - 0.145231109113)
        - 4.907 * max(0.0, Q.max_dr - 0.145231109113) * max(0.0, 0.04586879935 - Q.dr_3)
        - 462.7 * max(0.0, Q.lam1 - 0.016433749775) * max(0.0, Q.eccentricity - 0.959856212153)
        + 0.006033 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 68.125 - Q.pt_4)
        - 11.14 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 0.120257140434 - Q.z_4)
        - 0.3701 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 29.875 - Q.pt_5)
        + 87.69 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.959856212153)
        - 35.66 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.eccentricity - 0.959856212153)
        - 0.05522 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 56.53125 - Q.pt_6)
        - 0.3888 * max(0.0, Q.lam1 - 0.012003726523) * max(0.0, 38.25 - Q.pt_6)
        - 0.04168 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 48.71875 - Q.pt_7)
        - 3.09 * max(0.0, Q.LHA - 0.423592510895)
        - 0.0001861 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 20.125 - Q.pt_7)
        - 1.485 * max(0.0, 0.23799610585 - Q.tau21)
        + 0.05989 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 62.55 - Q.mass)
        - 58.95 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.e2_sq - 0.011657374702)
        + 569.2 * max(0.0, 0.000306123359 - Q.lam2)
        - 587.3 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.001130644719 - Q.lam2)
        + 2151.0 * max(0.0, Q.width - 0.000319370692)
        + 0.01119 * max(0.0, 763.825 - Q.sum_pt)
        + 150.3 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.067292226106 - Q.C2)
        + 810.4 * max(0.0, 0.009530300104 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.016278845848)
        - 0.9462 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.planar_flow - 0.045057236346)
        - 56.29 * max(0.0, Q.width - 0.001653836415)
        + 0.0002783 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 104.8 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        - 0.6177 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.175465903809 - Q.dr_7)
        - 0.7709 * max(0.0, Q.C2 - 0.067292226106)
        + 342.5 * max(0.0, 0.001130644719 - Q.lam2)
        - 25.51 * max(0.0, 0.005011406868 - Q.girth2_top3)
        + 14.51 * max(0.0, 0.001130644719 - Q.lam2) * max(0.0, Q.n_dr_0p1_0p2 - 2.0)
        - 8.65 * max(0.0, Q.girth - 0.101940929517)
        + 103.3 * max(0.0, 0.017162483186 - Q.e2_sq)
        - 402.2 * max(0.0, Q.girth2 - 0.013238675334)
        - 0.00171 * max(0.0, 430.75 - Q.sum_pt_top5)
        + 21.77 * max(0.0, Q.e2 - 0.063441075385)
        - 70.27 * max(0.0, Q.e2 - 0.007078157854)
        - 0.0108 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.104247858869 - Q.dr_3)
        + 16.15 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, -0.025945045147 - Q.mean_phi)
        - 0.06243 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_7 - 33.21875)
        - 18.64 * max(0.0, 0.014379521101 - Q.centroid_offset)
        - 5.672 * max(0.0, Q.max_dr - 0.102758520097)
        + 3.692 * max(0.0, Q.mass_over_sum_pt - 0.107985668755) * max(0.0, 3.885568320751 - Q.D2)
        + 3.213 * max(0.0, Q.max_dr - 0.197968879342)
        + 0.04959 * max(0.0, Q.max_dr - 0.102758520097) * max(0.0, Q.pt_7 - 37.15625)
        - 1.996 * max(0.0, Q.C2 - 0.014943876117)
        - 0.1093 * max(0.0, Q.C2 - 0.014943876117) * max(0.0, Q.pt_7 - 38.53125)
        - 0.7645 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 50.352200171245 - Q.mass_top3)
        + 11.22 * max(0.0, 0.014379521101 - Q.centroid_offset) * max(0.0, 0.674770402908 - Q.z_dr_0p05_0p1)
        - 1.033 * max(0.0, 0.047915700823 - Q.girth)
        - 0.0006215 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_2 - 73.6875)
        - 65.99 * max(0.0, 0.023780909279 - Q.e2_sq)
        + 67.16 * max(0.0, 0.001101860861 - Q.mass_over_sum_pt_sq)
        + 8.745 * max(0.0, 0.216055863061 - Q.LHA)
        - 4.637 * max(0.0, 0.049399692737 - Q.z_7)
        - 0.2181 * max(0.0, 0.049399692737 - Q.z_7) * max(0.0, 62.55 - Q.mass_top5)
        - 9.99 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 161.1 * max(0.0, 0.00528466865 - Q.e2_sq)
        - 18.61 * max(0.0, 0.028865759995 - Q.z_6)
        - 3.006 * max(0.0, 0.071488645583 - Q.z_7)
        - 745.9 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, 0.014379521101 - Q.centroid_offset)
        + 646.9 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 0.03946 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 788.4484375 - Q.sum_pt)
        - 11640.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001503553356 - Q.lam1)
        + 0.5873 * max(0.0, 0.03243272066 - Q.z_7)
        + 14.61 * max(0.0, 0.026454043164 - Q.dr_0)
        + 57.03 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 3.557 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.n_dr_0p2_0p4 - 0.0)
        - 1.848 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 84.43 * max(0.0, 0.002635417778 - Q.width)
        - 66.02 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt)
        + 28.69 * max(0.0, 0.002270363079 - Q.girth2_top5)
        - 0.002802 * max(0.0, Q.sum_pt_top5 - 752.1)
        - 4774.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.0008367 * max(0.0, 548.196875 - Q.sum_pt_top2)
        + 62.13 * max(0.0, 0.002635417778 - Q.width) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 277.6 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 0.4751 * max(0.0, 0.03243272066 - Q.z_7) * max(0.0, Q.pt_5 - 33.0265625)
        + 0.01685 * max(0.0, 24.578125 - Q.pt_5)
        + 0.004107 * max(0.0, Q.sum_pt - 868.509375)
        - 0.09492 * max(0.0, Q.sum_pt - 868.509375) * max(0.0, 0.012587644117 - Q.centroid_offset)
        + 0.1743 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, Q.mass_top3 - 28.345095968085)
        + 255.0 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.018377780003 - Q.centroid_offset)
        - 1062.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.000145482056 - Q.mean_phi2)
        - 0.1365 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.021588001063 - Q.dr_0)
        - 136.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.021588001063 - Q.dr_0)
        + 141.6 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.04118638065 - Q.dr_0)
        + 322.6 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.004331280361 - Q.mean_phi2)
        - 66.74 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.012003726523 - Q.lam1)
        - 84.97 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006299534492 - Q.girth2_top2)
        + 0.4373 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 201.8 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 9.0303693e-05 - Q.mean_eta2)
        - 0.178 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, 18.097979966098 - Q.max_pair_mass)
        + 0.2532 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.mass_top3 - 3.559569591142)
        - 7.134 * max(0.0, 0.01426135283 - Q.mean_phi2)
        - 0.1069 * max(0.0, 0.01426135283 - Q.mean_phi2) * max(0.0, 40.046952646555 - Q.max_pair_mass)
        - 134.1 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 51760.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, 7.3007261e-05 - Q.lam2)
        + 43.07 * max(0.0, 0.021588001063 - Q.dr_0)
        - 10.87 * max(0.0, Q.centroid_offset - 0.008092360237)
        + 133.7 * max(0.0, 0.013238675006 - Q.width)
        + 13.07 * max(0.0, 0.154170806525 - Q.mass_over_sum_pt)
        + 1.272 * max(0.0, 6.327378592257 - Q.log_sum_pt)
        + 3502.0 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.003408388935 - Q.lam2)
        + 11.21 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, 0.071488645583 - Q.z_7)
        + 12.0 * max(0.0, 0.050284641981 - Q.e2)
        + 10.55 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, Q.planar_flow - 0.00804883781)
        - 77.88 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.094821243733 - Q.C2)
        + 17.14 * max(0.0, Q.centroid_offset - 0.018377780003)
        - 0.02575 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, Q.pt_6 - 27.578125)
        - 6.994 * max(0.0, 6.701242202626 - Q.log_sum_pt)
        + 76.25 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 0.049399692737 - Q.z_7)
        - 0.8284 * max(0.0, Q.centroid_offset - 0.049903668404)
        + 3.841 * Q.max_dr
        + 1.124 * max(0.0, Q.C2 - 0.010539266048)
        + 197.1 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 0.008921136335 - Q.mean_phi2)
        + 26.95 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.872657364787)
        + 0.3565 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 4.0 - Q.n_dr_0p05_0p1)
        + 12.45 * max(0.0, 0.000537286005 - Q.lam2)
        + 10.96 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_phi - 0.026127964072)
        - 86.38 * max(0.0, Q.mass_over_sum_pt - 0.008374148675)
        + 7.215 * max(0.0, Q.girth2_top5 - 0.011482925368)
        - 3.997 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, Q.mean_phi - 0.009050007537)
        + 15.54 * max(0.0, Q.girth - 0.087236513197)
        - 3.227 * max(0.0, Q.mass_over_sum_pt - 0.008374148675) * max(0.0, 0.518696343899 - Q.tau32)
        - 0.008413 * max(0.0, 1.679198372364 - Q.D2)
        + 0.1084 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, Q.pt_2 - 56.5)
        + 19.8 * max(0.0, 0.007330079875 - Q.lam1) * max(0.0, 1.232133567333 - Q.D2)
        + 56.43 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.15855820179)
        + 25.09 * max(0.0, Q.lam2 - 0.003408388935)
        - 1.477 * max(0.0, 6.572937922293 - Q.log_sum_pt)
        + 0.003645 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 36.8125 - Q.pt_6)
        + 5.248 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 24.578125 - Q.pt_5)
        + 771.1 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_eta - 0.02644207105)
        - 10970.0 * max(0.0, 0.000537286005 - Q.lam2) * max(0.0, Q.mean_eta - 0.02644207105)
        + 7.781 * max(0.0, 0.003562611155 - Q.girth2)
        + 0.01842 * max(0.0, 49.668099212646 - Q.mass)
        + 7.424 * max(0.0, Q.girth2_top5 - 0.002270363079)
        - 0.0002875 * max(0.0, 1.679198372364 - Q.D2) * max(0.0, 90.625 - Q.pt_4)
        - 3.423 * max(0.0, Q.z_7 - 0.06164517166)
        + 0.04262 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 45.75 - Q.pt_7)
        + 0.06824 * max(0.0, Q.C2 - 0.010539266048) * max(0.0, Q.pt_7 - 31.859375)
        + 0.003334 * max(0.0, 49.668099212646 - Q.mass) * max(0.0, 0.750909513235 - Q.z_dr_0p05_0p1)
        - 0.2923 * max(0.0, 0.195013533663 - Q.planar_flow)
        + 69.46 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.width - 0.00752008842)
        - 66.98 * max(0.0, 0.001056655216 - Q.girth2_top2)
        - 387.2 * max(0.0, Q.girth2 - 0.007520088344)
        - 263.3 * max(0.0, Q.girth2 - 0.004372139461)
        - 0.7205 * max(0.0, Q.mass_over_sum_pt - 0.072690732432)
        + 1420.0 * max(0.0, 0.001056655216 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 56.29 * max(0.0, Q.girth2 - 0.0016538364)
        - 28.81 * max(0.0, 0.024547699839 - Q.e2)
        + 0.005833 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, 35.28125 - Q.pt_6)
        - 19.52 * max(0.0, 0.04081947431 - Q.girth)
        - 0.02418 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.mass_top3 - 23.663861485439)
        - 0.005392 * max(0.0, 48.71875 - Q.pt_7)
        + 0.001816 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.sum_pt - 615.875)
        - 13.37 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        + 137.3 * max(0.0, 0.005590288644 - Q.width)
        - 35.4 * max(0.0, 0.02076709205 - Q.centroid_offset)
        - 518.9 * max(0.0, Q.girth2 - 0.008678044751)
        + 55.15 * max(0.0, Q.mass_over_sum_pt - 0.084751611895)
        - 0.03465 * max(0.0, 0.001101266364 - Q.e2_sq)
        - 0.004195 * max(0.0, Q.mass - 80.4)
        - 285.9 * max(0.0, Q.girth2 - 0.004372139461) * max(0.0, Q.eccentricity - 0.945820652852)
        - 48.67 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, 1.122624260187 - Q.D2)
        - 3.769 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 1.122624260187 - Q.D2)
        + 18.16 * max(0.0, 0.038466955721 - Q.e2)
        - 5.657 * max(0.0, 0.02076709205 - Q.centroid_offset) * max(0.0, Q.C2 - 0.023843882605)
        + 0.08688 * max(0.0, Q.mass - 80.4) * max(0.0, Q.eccentricity - 0.927072033478)
        + 0.005113 * max(0.0, 48.71875 - Q.pt_7) * max(0.0, 0.694781820497 - Q.planar_flow)
        - 0.2313 * max(0.0, Q.centroid_offset - 0.031170772021)
        - 4.487 * max(0.0, 0.293190627853 - Q.LHA)
        - 3.276 * max(0.0, 0.005884990035 - Q.girth2_top3)
        + 1095.0 * max(0.0, 0.000561123155 - Q.width)
        + 0.08249 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_0 - 376.5)
        + 1194.0 * max(0.0, 0.001101266364 - Q.e2_sq) * max(0.0, -0.009460449219 - Q.phi_1)
        + 0.02264 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_2 - 56.5)
        - 1.198 * max(0.0, 0.197968879342 - Q.max_dr)
        - 67.61 * max(0.0, 0.005019718802 - Q.width)
        + 50.42 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.501026660204 - Q.tau21)
        + 8939.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 1.031 * max(0.0, 0.196739721581 - Q.LHA)
        - 0.613 * max(0.0, Q.log_sum_pt - 6.701242202626)
        - 42.45 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.40079469091 - Q.planar_flow)
        + 0.1355 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 248.125 - Q.sum_pt_top2)
        + 10.17 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.n_dr_0p05_0p1 - 0.0)
        - 21.84 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.mean_phi - -0.000855675264)
        + 9.609 * max(0.0, 0.061086014472 - Q.girth)
        - 0.0005755 * max(0.0, Q.sum_pt_top5 - 658.125)
        + 54.77 * max(0.0, 0.003343241496 - Q.centroid_offset)
        + 1.445 * max(0.0, 0.177304983139 - Q.max_dr)
        + 2799.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 0.1009733513 - Q.z_dr_0p2_0p4)
        + 4.34 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 1.08 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 14670.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 5418.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.lam1 - 0.00027588256)
        + 1546.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.mass_over_sum_pt_sq - 0.00012320649)
        + 3272.0 * max(0.0, 0.177304983139 - Q.max_dr) * max(0.0, 0.000194798295 - Q.lam2)
        - 151.8 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.000306123359 - Q.lam2)
        + 0.0211 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 48.71875 - Q.pt_7)
        + 268.5 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.018827652745 - Q.girth2)
        - 4920.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.00023679558 - Q.mass_over_sum_pt_sq)
        - 12.93 * max(0.0, 0.016554418951 - Q.e2)
        - 273.4 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 5.3 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 3995.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000561123155 - Q.width)
        + 38.01 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_6 - 0.02160287394)
        - 3.685 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.0168 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, Q.sum_pt - 788.4484375)
        - 5527.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.005019718802 - Q.width)
        - 1934.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.000194798295 - Q.lam2)
        + 231.4 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 175.4 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 12640.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 5070.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000306123359 - Q.lam2)
        + 0.1616 * max(0.0, 8.379955863953 - Q.mass)
        - 0.3915 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.058613700176 - Q.z_7)
        + 16.73 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_7 - 0.016858545121)
        + 0.201 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, Q.centroid_offset - 0.016278845848)
        - 827.2 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971) * max(0.0, 0.000537286005 - Q.lam2)
        + 883.6 * max(0.0, 0.000964142894 - Q.girth2)
        + 133.0 * max(0.0, 0.000222950415 - Q.girth2_top5)
        - 16.48 * max(0.0, 0.054649224505 - Q.girth)
        - 175.8 * max(0.0, Q.lam2 - 0.001130644719)
        + 1.634 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 76.55 * max(0.0, 0.006096650059 - Q.width)
        - 4.312 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.000872228216 - Q.lam1)
        - 155.6 * max(0.0, Q.girth2 - 0.018827652745)
        - 17.28 * max(0.0, 0.032346998155 - Q.e2)
        - 205.7 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.40079469091 - Q.planar_flow)
        + 57.01 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.055953954317 - Q.dr01)
        + 0.1739 * max(0.0, Q.n_dr_0p2_0p4 - 1.0)
        + 0.07295 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 6.842716632804 - Q.log_sum_pt)
        + 0.9917 * max(0.0, 0.221586732566 - Q.max_dr)
        - 1993.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.C2 - 0.030867108516)
        + 4.964 * max(0.0, Q.C2 - 0.051192347892)
        + 15.86 * max(0.0, 0.018377780003 - Q.centroid_offset)
        + 3441.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.centroid_offset - 0.003343241496)
        + 6145.0 * max(0.0, 0.000172198326 - Q.width)
        + 22.84 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_5 - 0.036727111752)
        + 150.6 * max(0.0, 0.007520088344 - Q.girth2)
        - 1.07 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.002127561159 - Q.mean_phi2)
        + 0.0931 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 0.5278 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.pt_4 - 47.34375)
        - 323.5 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_4 - 0.047491459878)
        - 215.1 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, Q.eccentricity - 0.903125533696)
        + 13.18 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.620723099573 - Q.eccentricity)
        + 0.02548 * max(0.0, 41.377904891968 - Q.mass)
        - 0.0729 * max(0.0, 41.377904891968 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        - 18.29 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        + 14.97 * max(0.0, 0.076373631775 - Q.mass_over_sum_pt)
        + 85.74 * max(0.0, 0.001503553356 - Q.lam1)
        + 1.939 * max(0.0, Q.max_dr - 0.15984864831)
        + 2.53 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 29.0421875 - Q.pt_7)
        + 0.3851 * max(0.0, Q.lam2 - 0.001130644719) * max(0.0, Q.mass_top2 - 16.308019673264)
        + 0.002133 * max(0.0, 35.5 - Q.pt_5)
        + 0.5195 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, 53.4375 - Q.pt_7)
        - 194.4 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.02644207105 - Q.mean_eta)
        - 0.001269 * max(0.0, 35.5 - Q.pt_5) * max(0.0, Q.min_pair_mass - 0.173071536962)
        - 1.702 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, Q.n_dr_0p05_0p1 - 1.0)
        + 28.62 * Q.e2
        + 196.8 * max(0.0, Q.lam2 - 0.000194798295)
        - 3.698 * max(0.0, Q.LHA - 0.303313749495)
        - 109.2 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, Q.planar_flow - 0.012569162668)
        - 2.365 * max(0.0, 6.267538488641 - Q.log_sum_pt)
        - 0.1024 * max(0.0, Q.centroid_offset - 0.00231612516) * max(0.0, 34.53125 - Q.pt_7)
        - 1.464 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 8.0 - Q.n_pt_above_50)
        - 0.06854 * max(0.0, Q.n_dr_0p2_0p4 - 2.0)
        + 76.29 * max(0.0, 0.004183811014 - Q.lam1)
        - 83.79 * max(0.0, 0.090413827016 - Q.mass_over_sum_pt)
        - 0.0117 * max(0.0, 3.0 - Q.n_dr_0p05_0p1)
        + 3.918 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 0.501026660204 - Q.tau21)
        + 0.293 * max(0.0, 0.269169217348 - Q.tau32)
        + 1.533 * max(0.0, Q.LHA - 0.303313749495) * max(0.0, 0.553068161011 - Q.tau21)
        - 0.04666 * max(0.0, 0.391541349888 - Q.tau21)
        - 38.58 * max(0.0, Q.eccentricity - 0.903125533696) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        - 0.1647 * max(0.0, 0.269169217348 - Q.tau32) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 11.21 * max(0.0, 0.002412890926 - Q.girth2_top2)
        + 0.007311 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.pt_4 - 39.8125)
        + 0.9885 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.222994708167 - Q.dr_7)
        - 10.7 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 2.055451202393 - Q.D2)
        + 11.24 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, 0.175465903809 - Q.dr_7)
        - 3.258 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.z_4 - 0.075444822386)
        + 1.267 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.sum_pt - 988.4078125)
        - 814.5 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.log_sum_pt - 6.701242202626)
        - 0.257 * max(0.0, Q.mass - 15.454033088684)
        + 0.0962 * max(0.0, Q.max_dr - 0.121680960059)
        + 0.003039 * max(0.0, Q.mass - 15.454033088684) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 404.1 * max(0.0, 0.0016538364 - Q.girth2)
        + 0.009148 * max(0.0, Q.sum_pt - 813.415625)
        - 18.23 * max(0.0, 0.006679471442 - Q.girth2)
        - 0.5866 * max(0.0, 0.253403707141 - Q.planar_flow)
        + 8.513 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.width - 0.006096650059)
        - 1.693 * max(0.0, 0.154689112391 - Q.LHA)
        + 26.24 * max(0.0, Q.girth - 0.076081777364)
        + 0.01005 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, 69.611351776123 - Q.mass)
        - 1.845 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.max_dr - 0.102758520097)
        - 0.8849 * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 0.07589 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 48.71875 - Q.pt_7)
        + 0.9164 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, Q.n_dr_0p05_0p1 - 2.0)
        + 44.13 * max(0.0, 0.006390124748 - Q.e2_sq)
        + 2.611 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 0.01128 * max(0.0, 7.0 - Q.n_dr_0_0p05)
        + 6.003 * max(0.0, 0.006390124748 - Q.e2_sq) * max(0.0, 1.332146394253 - Q.D2)
        - 0.3083 * Q.centroid_offset
        + 7.78 * max(0.0, 0.003562611091 - Q.width)
        + 0.0006992 * max(0.0, 9.257203159811 - Q.mass_top5)
        + 196.6 * max(0.0, 0.154689112391 - Q.LHA) * max(0.0, 0.028070914944 - Q.z_7)
        + 0.2331 * max(0.0, 15.454033088684 - Q.mass)
        - 0.4516 * max(0.0, Q.girth - 0.076081777364) * max(0.0, 7.0 - Q.n_pt_above_50)
        + 0.03932 * max(0.0, 29.0421875 - Q.pt_7)
        - 38.46 * max(0.0, 0.004839980301 - Q.lam1)
        + 2.108 * max(0.0, 0.035786485299 - Q.C2)
        + 3.879 * max(0.0, 0.111761856824 - Q.max_dr)
        + 0.04949 * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 0.0005711 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 22.844978847276 - Q.mass_top2)
        - 0.05244 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.pt_5 - 43.0625)
        - 0.001735 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 0.01906 * max(0.0, Q.mass - 91.19)
        - 7541.0 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.lam2 - 0.000537286005)
        - 0.1901 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.pt_7 - 15.55390625)
        + 2.465 * max(0.0, Q.mean_phi - 0.026127964072)
        + 3.105 * max(0.0, 0.148408418149 - Q.girth)
        - 1.917 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 0.1844 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 38.53125 - Q.pt_7)
        + 34.83 * max(0.0, 0.016433749775 - Q.lam1)
        + 0.1151 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, Q.z_7 - 0.023207568189)
        - 9228.0 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 8.344e-05 * max(0.0, 531.1875 - Q.sum_pt_top5)
        - 1.392e-05 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, 43.5 - Q.pt_7)
        - 0.0004619 * max(0.0, Q.sum_pt_top5 - 902.40625)
        - 0.0005334 * max(0.0, Q.sum_pt_top5 - 839.9546875)
        + 0.01575 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 56.53125 - Q.pt_6)
        + 4.318 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.pt_dispersion - 0.396830244362)
        - 0.1992 * max(0.0, 0.501026660204 - Q.tau21)
        + 191.7 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 0.037760993714 - Q.centroid_offset)
        + 0.9862 * max(0.0, 0.067272114405 - Q.z_6)
        + 9.086 * max(0.0, 0.037760993714 - Q.centroid_offset)
        - 5.8 * max(0.0, Q.LHA - 0.09323897448)
        + 0.0007842 * max(0.0, Q.sum_pt_top5 - 902.40625) * max(0.0, 3.885568320751 - Q.D2)
        + 0.00357 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.15855820179 - Q.z_dr_0p1_0p2)
        + 1.652 * max(0.0, 0.501026660204 - Q.tau21) * max(0.0, Q.max_dr - 0.015595615841)
        + 150.6 * max(0.0, 0.00752008842 - Q.width)
        - 0.02741 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 0.037477688199 - Q.z_4)
        - 0.02671 * max(0.0, 25.578125 - Q.pt_7)
        - 0.2274 * max(0.0, Q.sum_pt - 988.4078125)
        - 0.0005517 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 0.0007662 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, 3.885568320751 - Q.D2)
        - 4.247 * max(0.0, 0.111513564951 - Q.planar_flow)
        + 0.06532 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 73.98 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018377780003)
        + 4.592 * max(0.0, Q.lam1 - 0.008375572068)
        + 12.61 * max(0.0, Q.lam1 - 0.004183811014)
        + 44.49 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 0.15984864831 - Q.max_dr)
        - 0.701 * max(0.0, Q.lam1 - 0.00543336053)
        + 0.01145 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 739.5 - Q.sum_pt)
        - 4.783 * max(0.0, Q.lam1 - 0.007330079875)
        + 5.618 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 0.067292226106 - Q.C2)
        + 4731.0 * max(0.0, Q.lam1 - 0.007330079875) * max(0.0, 0.13261153996 - Q.max_dr)
        - 1.506 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235)
        - 2889.0 * max(0.0, Q.lam1 - 0.00543336053) * max(0.0, 0.15984864831 - Q.max_dr)
        - 64.71 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.009480684835)
        + 0.009245 * max(0.0, 76.655700683594 - Q.mass)
        - 11.9 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, Q.eccentricity - 0.970449631164)
        - 0.5661 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 5.87 * max(0.0, Q.lam1 - 0.005954149834)
        - 0.0381 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 121.9 * max(0.0, Q.lam1 - 0.002464291268)
        + 503.4 * max(0.0, 0.011660904657 - Q.mass_over_sum_pt_sq)
        + 0.01285 * max(0.0, 76.655700683594 - Q.mass) * max(0.0, 0.74595130682 - Q.D2)
        + 809.9 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.111513564951 - Q.planar_flow)
        - 737.6 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.eccentricity - 0.970449631164)
        + 101.6 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        + 0.3058 * max(0.0, 1.122624260187 - Q.D2)
        - 47.18 * max(0.0, 0.038466955721 - Q.e2) * max(0.0, 1.002470755577 - Q.D2)
        + 0.02776 * max(0.0, 5.0 - Q.n_dr_0p05_0p1)
        - 7.062 * max(0.0, 1.122624260187 - Q.D2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 11.26 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, Q.eccentricity - 0.984196588116)
        - 0.2598 * max(0.0, 0.74595130682 - Q.D2)
        + 157.5 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 122.9 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        + 3.138 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 1.002470755577 - Q.D2)
        + 0.5123 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 41.72 * max(0.0, 0.004372139461 - Q.girth2) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 8.225 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 0.1118 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 1.358 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.121680960059 - Q.max_dr)
        + 4.482 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        + 5000.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, Q.e2 - 0.024547699839)
        + 38.7 * max(0.0, 0.012003726523 - Q.lam1)
        - 197.3 * max(0.0, 0.011657374702 - Q.e2_sq)
        + 45.01 * max(0.0, 0.007182835724 - Q.mass_over_sum_pt_sq)
        + 0.00863 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.sum_pt_top3 - 353.0625)
        - 3.956 * max(0.0, 0.041109715588 - Q.e2)
        - 11.0 * max(0.0, 0.063441075385 - Q.e2)
        - 0.1291 * max(0.0, 0.328461505473 - Q.z_dr_0p1_0p2)
        + 1.145 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 0.02796 * max(0.0, 2.0 - Q.n_dr_0_0p05)
        + 1.798 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.m01 - 16.308019673264)
        - 1.294 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, Q.pt1_dr01 - 1.21960336377)
        - 0.01447 * max(0.0, Q.mass - 80.4) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 11.12 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.z_top5 - 0.865048766136)
        - 1020.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.log_sum_pt - 6.896095378249)
        - 0.4718 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.mass_top2 - 22.844978847276)
        + 265.5 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.061262048692 - Q.planar_flow)
        - 48.81 * max(0.0, 0.06813910019 - Q.mass_over_sum_pt)
        - 0.01363 * max(0.0, Q.n_dr_0p05_0p1 - 5.0)
        - 1.028 * max(0.0, Q.LHA - 0.346713497427)
        - 9.085 * max(0.0, Q.girth - 0.033604209498)
        + 18.49 * max(0.0, 0.002151567843 - Q.girth2_top3)
        - 3.199 * max(0.0, 0.007639643088 - Q.girth2_top2)
    )


def score_q(Q):
    return (-0.459
        - 0.7665 * max(0.0, 0.148419710734 - Q.planar_flow)
        + 22.43 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 280.3 * max(0.0, 0.004372139331 - Q.width)
        + 440.5 * max(0.0, 0.018827652745 - Q.girth2)
        + 0.003918 * max(0.0, 64.618731689453 - Q.mass)
        + 0.1413 * max(0.0, 21.784077072144 - Q.mass)
        - 7.308 * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 172.2 * max(0.0, 0.013238675334 - Q.girth2)
        + 34.89 * max(0.0, 0.006506575659 - Q.lam1)
        - 227.6 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, 0.87567204833 - Q.D2)
        + 0.01112 * max(0.0, Q.sum_pt - 901.59375)
        + 0.0003152 * max(0.0, 56.920347213745 - Q.mass)
        + 107.7 * max(0.0, 0.008678044951 - Q.width)
        - 7.753e-05 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 25.578125 - Q.pt_7)
        - 0.0005055 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 380.5875 - Q.sum_pt_top2)
        - 0.02826 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 0.038438041256 - Q.dr_2)
        + 0.2662 * max(0.0, 56.920347213745 - Q.mass) * max(0.0, Q.C2 - 0.023843882605)
        + 16.86 * max(0.0, 0.00832969537 - Q.girth2_top5)
        + 0.531 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971)
        + 0.01483 * max(0.0, 29.644699859619 - Q.mass)
        + 0.007733 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.87567204833 - Q.D2)
        - 22.35 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.111761856824 - Q.max_dr)
        - 11.72 * max(0.0, 0.087236513197 - Q.girth)
        + 1.152 * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 3059.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.centroid_offset - 0.014379521101)
        - 0.113 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, Q.centroid_offset - 0.012587644117)
        + 9.132 * max(0.0, 0.020459658932 - Q.e2)
        + 1054.0 * max(0.0, 0.008174660116 - Q.mass_over_sum_pt_sq)
        + 230.3 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.eccentricity - 0.959856212153)
        - 5.463 * max(0.0, Q.log_sum_pt - 6.638338705138)
        - 0.0001341 * max(0.0, Q.sum_pt_top5 - 687.4375)
        - 0.1209 * max(0.0, 0.007929074034 - Q.girth2_top3) * max(0.0, 35.28125 - Q.pt_6)
        + 147.6 * max(0.0, 0.00543336053 - Q.lam1)
        - 0.5536 * max(0.0, Q.log_sum_pt - 6.377722943814)
        - 0.06863 * max(0.0, Q.sum_pt_top5 - 687.4375) * max(0.0, Q.z_7 - 0.023207568189)
        - 62.94 * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 8.416 * max(0.0, 0.076081777364 - Q.girth)
        + 0.000191 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, 40.040625 - Q.pt_7)
        + 1.571 * max(0.0, Q.log_sum_pt - 6.638338705138) * max(0.0, 0.093979107928 - Q.dr_7)
        + 0.03271 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, Q.phi_1 - -0.058901977539)
        - 0.5703 * max(0.0, 0.004372139331 - Q.width) * max(0.0, Q.n_dr_0p1_0p2 - 1.0)
        - 40.77 * max(0.0, 0.13092863437 - Q.mass_over_sum_pt)
        - 0.07026 * max(0.0, 0.012569162668 - Q.planar_flow)
        + 198.8 * max(0.0, 0.008375572068 - Q.lam1)
        + 0.01076 * max(0.0, Q.pt_7 - 34.53125)
        + 104.2 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.centroid_offset - 0.02076709205)
        - 0.0001853 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 91.19 - Q.mass)
        - 0.2468 * max(0.0, 0.035560912266 - Q.e2)
        + 2.844 * max(0.0, 0.055577157257 - Q.z_7)
        + 0.2666 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, Q.centroid_offset - 0.014379521101)
        + 120.6 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.04577 * max(0.0, 53.332374954224 - Q.mass)
        + 3.727e-06 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 45.595 - Q.mass_top3)
        - 3.911 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.197968879342 - Q.max_dr)
        + 4.327 * max(0.0, Q.log_sum_pt - 6.572937922293)
        - 0.007002 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 0.553068161011 - Q.tau21)
        - 729.4 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 554.1 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, Q.eccentricity - 0.978160776925)
        - 1.675 * max(0.0, 0.083662731125 - Q.planar_flow)
        - 15.87 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.042322802544 - Q.C2)
        - 0.3095 * max(0.0, 0.197783735394 - Q.tau21)
        - 218.6 * max(0.0, 0.008168570676 - Q.e2_sq)
        - 0.02729 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 0.080507021025 - Q.max_dr)
        - 0.000166 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 32.617988451746 - Q.mass_top3)
        - 3.703 * max(0.0, 0.042322802544 - Q.C2)
        + 0.004053 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 50.25 - Q.pt_6)
        + 48.45 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006756161242 - Q.girth2_top3)
        - 253.5 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 2059.0 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 0.000194798295 - Q.lam2)
        - 1315.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.001130644719 - Q.lam2)
        - 1.254 * max(0.0, 0.083662731125 - Q.planar_flow) * max(0.0, 0.269169217348 - Q.tau32)
        - 7.824 * max(0.0, 0.346713497427 - Q.LHA)
        + 21.26 * max(0.0, Q.e2 - 0.032346998155)
        + 30.29 * max(0.0, Q.mass_over_sum_pt - 0.054892207095)
        + 15.05 * max(0.0, 0.346713497427 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 39.91 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 522.4 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 32.2 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 7.064 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.033200121667 - Q.planar_flow)
        - 0.9968 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.n_pt_above_50 - 7.0)
        + 1.773 * max(0.0, 0.046566883102 - Q.max_dr)
        + 3.72 * max(0.0, Q.e2 - 0.032346998155) * max(0.0, 0.641386964917 - Q.tau32)
        - 0.3187 * max(0.0, 69.611351776123 - Q.mass)
        + 0.02321 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.068101508468 - Q.z_7)
        - 1.125 * max(0.0, Q.log_sum_pt - 6.842716632804)
        + 0.1879 * max(0.0, 6.464150123592 - Q.log_sum_pt)
        - 22.66 * max(0.0, 0.028070914944 - Q.z_7)
        + 149.0 * max(0.0, 0.005954149834 - Q.lam1)
        + 28720.0 * max(0.0, 9.1213921e-05 - Q.width)
        - 0.02199 * max(0.0, Q.pt_7 - 30.484375)
        + 0.3306 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, 0.051192347892 - Q.C2)
        + 3.835 * max(0.0, Q.z_7 - 0.046240320761)
        + 2154.0 * max(0.0, 0.028070914944 - Q.z_7) * max(0.0, 0.00752008842 - Q.width)
        + 2.12 * max(0.0, Q.LHA - 0.111565049159)
        - 786.2 * max(0.0, 0.005954149834 - Q.lam1) * max(0.0, Q.max_dr - 0.080507021025)
        + 0.162 * max(0.0, 0.694781820497 - Q.planar_flow)
        + 0.07279 * max(0.0, 36.229410171509 - Q.mass)
        - 1.368e-05 * max(0.0, 56.53125 - Q.pt_6) * max(0.0, Q.m012 - 32.617988451746)
        + 5.625 * max(0.0, 36.229410171509 - Q.mass) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.03137 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, Q.max_dr - 0.093110798299)
        - 51.31 * max(0.0, 0.003377388461 - Q.lam1)
        - 39320.0 * max(0.0, 0.003377388461 - Q.lam1) * max(0.0, 0.006789738266 - Q.centroid_offset)
        - 89.31 * max(0.0, 8.379955863953 - Q.mass) * max(0.0, 0.010960638421 - Q.centroid_offset)
        - 6.678 * max(0.0, 0.016858545121 - Q.z_7)
        + 0.002157 * max(0.0, 687.4375 - Q.sum_pt_top5)
        - 0.01017 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.04881348081 - Q.dr_7)
        - 0.004027 * max(0.0, 53.4375 - Q.pt_7)
        - 0.001262 * max(0.0, 43.5 - Q.pt_7)
        - 0.0009691 * max(0.0, 788.4484375 - Q.sum_pt)
        + 4.043 * max(0.0, Q.log_sum_pt - 6.267538488641)
        + 4.457 * max(0.0, Q.log_sum_pt - 6.896095378249)
        + 54010.0 * max(0.0, 4.8108519e-05 - Q.girth2)
        - 9.287 * max(0.0, Q.log_sum_pt - 6.804164030582)
        - 0.511 * max(0.0, 0.15984864831 - Q.max_dr)
        - 5.329e-05 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, Q.max_pair_mass - 13.047927274731)
        + 8058.0 * max(0.0, 0.000172198326 - Q.width) * max(0.0, 0.222994708167 - Q.dr_7)
        + 106.2 * max(0.0, Q.mass_over_sum_pt - 0.06813910019)
        - 11.76 * max(0.0, Q.centroid_offset - 0.014379521101)
        - 7.359 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.518696343899 - Q.tau32)
        - 170.1 * max(0.0, Q.width - 0.018827653081)
        - 0.07217 * max(0.0, Q.mass - 36.229410171509)
        + 10.83 * max(0.0, Q.e2 - 0.028531698044)
        - 4.742 * max(0.0, Q.LHA - 0.312727471086)
        - 89.09 * max(0.0, 0.006679471358 - Q.width)
        - 0.426 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.n_pt_above_50 - 3.0)
        + 8.097 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.001130644719 - Q.lam2)
        - 7.708 * max(0.0, 0.04447356835 - Q.e2)
        + 136.2 * max(0.0, 0.007330079875 - Q.lam1)
        + 0.9153 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 5.0 - Q.n_dr_0_0p05)
        - 0.006336 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 50.352200171245 - Q.mass_top3)
        + 0.3293 * max(0.0, Q.mass - 69.611351776123)
        - 5.137 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, 0.964120104909 - Q.z_dr_0p05_0p1)
        + 107.7 * max(0.0, 0.008678044751 - Q.girth2)
        + 0.8099 * max(0.0, Q.LHA - 0.325582223496)
        + 0.00137 * max(0.0, Q.mass - 36.229410171509) * max(0.0, Q.eccentricity - 0.620723099573)
        + 14.23 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.0)
        + 0.5244 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, Q.phi_7 - -0.041534423828)
        + 0.0008227 * max(0.0, Q.mass_top5 - 53.607658247923)
        + 0.7876 * max(0.0, -0.012844925793 - Q.mean_eta)
        + 10.47 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, -0.039672851562 - Q.eta_0)
        - 147.2 * max(0.0, Q.width - 0.018827653081) * max(0.0, 0.492494773865 - Q.pt_dispersion)
        - 0.05335 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.046481671275 - Q.dr_6)
        - 18.47 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.042151962757 - Q.dr_7)
        + 27.54 * max(0.0, Q.mass_over_sum_pt - 0.090413827016)
        + 280.3 * max(0.0, 0.004372139461 - Q.girth2)
        - 135.0 * max(0.0, Q.mass_over_sum_pt - 0.107985668755)
        + 128.6 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 0.145231109113 - Q.max_dr)
        + 10.17 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.planar_flow - 0.00804883781)
        - 121.2 * max(0.0, Q.lam1 - 0.012003726523)
        + 1.923 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 0.145231109113 - Q.max_dr)
        - 0.06554 * max(0.0, Q.mass - 69.611351776123) * max(0.0, 0.177304983139 - Q.max_dr)
        - 0.1231 * max(0.0, Q.max_dr - 0.145231109113)
        + 4.224 * max(0.0, Q.max_dr - 0.145231109113) * max(0.0, 0.04586879935 - Q.dr_3)
        - 659.8 * max(0.0, Q.lam1 - 0.016433749775) * max(0.0, Q.eccentricity - 0.959856212153)
        - 0.04031 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 68.125 - Q.pt_4)
        + 3.093 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 0.120257140434 - Q.z_4)
        - 0.3934 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 29.875 - Q.pt_5)
        + 45.39 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.959856212153)
        + 84.93 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.eccentricity - 0.959856212153)
        - 0.002658 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 56.53125 - Q.pt_6)
        - 0.6339 * max(0.0, Q.lam1 - 0.012003726523) * max(0.0, 38.25 - Q.pt_6)
        + 0.02417 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 48.71875 - Q.pt_7)
        - 3.522 * max(0.0, Q.LHA - 0.423592510895)
        + 0.0002602 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 20.125 - Q.pt_7)
        - 2.817 * max(0.0, 0.23799610585 - Q.tau21)
        + 0.06129 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 62.55 - Q.mass)
        - 21.85 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.e2_sq - 0.011657374702)
        + 654.4 * max(0.0, 0.000306123359 - Q.lam2)
        + 43.63 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.001130644719 - Q.lam2)
        + 2841.0 * max(0.0, Q.width - 0.000319370692)
        + 0.004986 * max(0.0, 763.825 - Q.sum_pt)
        + 148.3 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.067292226106 - Q.C2)
        + 361.1 * max(0.0, 0.009530300104 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.016278845848)
        - 2.079 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.planar_flow - 0.045057236346)
        - 91.68 * max(0.0, Q.width - 0.001653836415)
        + 0.0006063 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 123.2 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        - 1.644 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.175465903809 - Q.dr_7)
        + 1.324 * max(0.0, Q.C2 - 0.067292226106)
        + 357.2 * max(0.0, 0.001130644719 - Q.lam2)
        - 15.87 * max(0.0, 0.005011406868 - Q.girth2_top3)
        + 36.34 * max(0.0, 0.001130644719 - Q.lam2) * max(0.0, Q.n_dr_0p1_0p2 - 2.0)
        - 9.793 * max(0.0, Q.girth - 0.101940929517)
        + 113.7 * max(0.0, 0.017162483186 - Q.e2_sq)
        - 435.7 * max(0.0, Q.girth2 - 0.013238675334)
        - 0.002623 * max(0.0, 430.75 - Q.sum_pt_top5)
        + 30.28 * max(0.0, Q.e2 - 0.063441075385)
        - 99.11 * max(0.0, Q.e2 - 0.007078157854)
        - 0.01866 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.104247858869 - Q.dr_3)
        + 35.3 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, -0.025945045147 - Q.mean_phi)
        - 0.09416 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_7 - 33.21875)
        - 16.3 * max(0.0, 0.014379521101 - Q.centroid_offset)
        - 1.242 * max(0.0, Q.max_dr - 0.102758520097)
        + 7.704 * max(0.0, Q.mass_over_sum_pt - 0.107985668755) * max(0.0, 3.885568320751 - Q.D2)
        + 2.776 * max(0.0, Q.max_dr - 0.197968879342)
        + 0.1733 * max(0.0, Q.max_dr - 0.102758520097) * max(0.0, Q.pt_7 - 37.15625)
        + 0.8482 * max(0.0, Q.C2 - 0.014943876117)
        - 0.7518 * max(0.0, Q.C2 - 0.014943876117) * max(0.0, Q.pt_7 - 38.53125)
        + 4.31 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 50.352200171245 - Q.mass_top3)
        + 23.97 * max(0.0, 0.014379521101 - Q.centroid_offset) * max(0.0, 0.674770402908 - Q.z_dr_0p05_0p1)
        - 7.743 * max(0.0, 0.047915700823 - Q.girth)
        - 0.0005048 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_2 - 73.6875)
        - 106.3 * max(0.0, 0.023780909279 - Q.e2_sq)
        + 64.38 * max(0.0, 0.001101860861 - Q.mass_over_sum_pt_sq)
        + 18.38 * max(0.0, 0.216055863061 - Q.LHA)
        + 0.06426 * max(0.0, 0.049399692737 - Q.z_7)
        + 0.04592 * max(0.0, 0.049399692737 - Q.z_7) * max(0.0, 62.55 - Q.mass_top5)
        - 31.89 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 255.5 * max(0.0, 0.00528466865 - Q.e2_sq)
        + 0.5173 * max(0.0, 0.028865759995 - Q.z_6)
        + 8.288 * max(0.0, 0.071488645583 - Q.z_7)
        - 4943.0 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, 0.014379521101 - Q.centroid_offset)
        - 205.1 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 0.01368 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 788.4484375 - Q.sum_pt)
        - 13190.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001503553356 - Q.lam1)
        + 2.968 * max(0.0, 0.03243272066 - Q.z_7)
        - 6.246 * max(0.0, 0.026454043164 - Q.dr_0)
        + 8.33 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 0.5907 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.n_dr_0p2_0p4 - 0.0)
        - 1.7 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        + 37.34 * max(0.0, 0.002635417778 - Q.width)
        - 93.33 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt)
        - 52.36 * max(0.0, 0.002270363079 - Q.girth2_top5)
        + 0.00231 * max(0.0, Q.sum_pt_top5 - 752.1)
        - 1798.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001130644719 - Q.lam2)
        - 0.0006163 * max(0.0, 548.196875 - Q.sum_pt_top2)
        + 21070.0 * max(0.0, 0.002635417778 - Q.width) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 237.5 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.centroid_offset - 0.018377780003)
        + 0.1895 * max(0.0, 0.03243272066 - Q.z_7) * max(0.0, Q.pt_5 - 33.0265625)
        - 0.002747 * max(0.0, 24.578125 - Q.pt_5)
        - 0.002701 * max(0.0, Q.sum_pt - 868.509375)
        + 0.1445 * max(0.0, Q.sum_pt - 868.509375) * max(0.0, 0.012587644117 - Q.centroid_offset)
        + 0.2625 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, Q.mass_top3 - 28.345095968085)
        - 373.8 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.018377780003 - Q.centroid_offset)
        + 3339.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.000145482056 - Q.mean_phi2)
        + 0.03311 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.021588001063 - Q.dr_0)
        + 27.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.021588001063 - Q.dr_0)
        - 51.09 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.04118638065 - Q.dr_0)
        - 89.37 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.004331280361 - Q.mean_phi2)
        - 79.51 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.012003726523 - Q.lam1)
        - 62.04 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006299534492 - Q.girth2_top2)
        + 0.06343 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.003952581551 - Q.girth2_top3)
        + 6306.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 9.0303693e-05 - Q.mean_eta2)
        - 0.005718 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, 18.097979966098 - Q.max_pair_mass)
        - 0.04062 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.mass_top3 - 3.559569591142)
        - 1.12 * max(0.0, 0.01426135283 - Q.mean_phi2)
        + 0.2168 * max(0.0, 0.01426135283 - Q.mean_phi2) * max(0.0, 40.046952646555 - Q.max_pair_mass)
        - 47.23 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 32120.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, 7.3007261e-05 - Q.lam2)
        - 8.607 * max(0.0, 0.021588001063 - Q.dr_0)
        - 13.34 * max(0.0, Q.centroid_offset - 0.008092360237)
        + 172.2 * max(0.0, 0.013238675006 - Q.width)
        + 21.63 * max(0.0, 0.154170806525 - Q.mass_over_sum_pt)
        + 1.232 * max(0.0, 6.327378592257 - Q.log_sum_pt)
        + 4445.0 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.003408388935 - Q.lam2)
        + 29.35 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, 0.071488645583 - Q.z_7)
        + 14.46 * max(0.0, 0.050284641981 - Q.e2)
        + 14.77 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, Q.planar_flow - 0.00804883781)
        - 106.2 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.094821243733 - Q.C2)
        + 19.5 * max(0.0, Q.centroid_offset - 0.018377780003)
        - 0.03346 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, Q.pt_6 - 27.578125)
        - 0.7251 * max(0.0, 6.701242202626 - Q.log_sum_pt)
        + 59.75 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 0.049399692737 - Q.z_7)
        + 3.162 * max(0.0, Q.centroid_offset - 0.049903668404)
        + 0.9997 * Q.max_dr
        - 3.753 * max(0.0, Q.C2 - 0.010539266048)
        + 267.9 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 0.008921136335 - Q.mean_phi2)
        + 36.69 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.872657364787)
        + 0.255 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 4.0 - Q.n_dr_0p05_0p1)
        + 14.2 * max(0.0, 0.000537286005 - Q.lam2)
        - 68.95 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_phi - 0.026127964072)
        - 117.8 * max(0.0, Q.mass_over_sum_pt - 0.008374148675)
        + 15.15 * max(0.0, Q.girth2_top5 - 0.011482925368)
        - 5.601 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, Q.mean_phi - 0.009050007537)
        + 24.49 * max(0.0, Q.girth - 0.087236513197)
        - 1.388 * max(0.0, Q.mass_over_sum_pt - 0.008374148675) * max(0.0, 0.518696343899 - Q.tau32)
        - 0.04446 * max(0.0, 1.679198372364 - Q.D2)
        + 0.2038 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, Q.pt_2 - 56.5)
        - 34.35 * max(0.0, 0.007330079875 - Q.lam1) * max(0.0, 1.232133567333 - Q.D2)
        + 49.76 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.15855820179)
        + 48.21 * max(0.0, Q.lam2 - 0.003408388935)
        - 3.245 * max(0.0, 6.572937922293 - Q.log_sum_pt)
        + 0.007134 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 36.8125 - Q.pt_6)
        + 5.488 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 24.578125 - Q.pt_5)
        + 799.3 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_eta - 0.02644207105)
        - 11240.0 * max(0.0, 0.000537286005 - Q.lam2) * max(0.0, Q.mean_eta - 0.02644207105)
        + 52.5 * max(0.0, 0.003562611155 - Q.girth2)
        + 0.02237 * max(0.0, 49.668099212646 - Q.mass)
        + 0.6702 * max(0.0, Q.girth2_top5 - 0.002270363079)
        - 0.0007412 * max(0.0, 1.679198372364 - Q.D2) * max(0.0, 90.625 - Q.pt_4)
        + 1.036 * max(0.0, Q.z_7 - 0.06164517166)
        + 0.0291 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 45.75 - Q.pt_7)
        + 0.3432 * max(0.0, Q.C2 - 0.010539266048) * max(0.0, Q.pt_7 - 31.859375)
        + 0.003965 * max(0.0, 49.668099212646 - Q.mass) * max(0.0, 0.750909513235 - Q.z_dr_0p05_0p1)
        - 0.6517 * max(0.0, 0.195013533663 - Q.planar_flow)
        + 260.2 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.width - 0.00752008842)
        - 43.48 * max(0.0, 0.001056655216 - Q.girth2_top2)
        - 434.6 * max(0.0, Q.girth2 - 0.007520088344)
        - 331.5 * max(0.0, Q.girth2 - 0.004372139461)
        + 22.43 * max(0.0, Q.mass_over_sum_pt - 0.072690732432)
        + 3666.0 * max(0.0, 0.001056655216 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 91.68 * max(0.0, Q.girth2 - 0.0016538364)
        - 9.884 * max(0.0, 0.024547699839 - Q.e2)
        + 0.01341 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, 35.28125 - Q.pt_6)
        - 38.61 * max(0.0, 0.04081947431 - Q.girth)
        - 0.0245 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.mass_top3 - 23.663861485439)
        + 0.005032 * max(0.0, 48.71875 - Q.pt_7)
        + 0.003944 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.sum_pt - 615.875)
        - 42.41 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        + 156.7 * max(0.0, 0.005590288644 - Q.width)
        - 43.8 * max(0.0, 0.02076709205 - Q.centroid_offset)
        - 500.2 * max(0.0, Q.girth2 - 0.008678044751)
        + 93.58 * max(0.0, Q.mass_over_sum_pt - 0.084751611895)
        + 43.21 * max(0.0, 0.001101266364 - Q.e2_sq)
        - 0.0009834 * max(0.0, Q.mass - 80.4)
        - 674.5 * max(0.0, Q.girth2 - 0.004372139461) * max(0.0, Q.eccentricity - 0.945820652852)
        - 58.54 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, 1.122624260187 - Q.D2)
        + 3.024 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 1.122624260187 - Q.D2)
        + 6.918 * max(0.0, 0.038466955721 - Q.e2)
        + 44.56 * max(0.0, 0.02076709205 - Q.centroid_offset) * max(0.0, Q.C2 - 0.023843882605)
        + 0.05384 * max(0.0, Q.mass - 80.4) * max(0.0, Q.eccentricity - 0.927072033478)
        + 0.001172 * max(0.0, 48.71875 - Q.pt_7) * max(0.0, 0.694781820497 - Q.planar_flow)
        + 1.358 * max(0.0, Q.centroid_offset - 0.031170772021)
        - 0.7482 * max(0.0, 0.293190627853 - Q.LHA)
        - 1.166 * max(0.0, 0.005884990035 - Q.girth2_top3)
        + 1201.0 * max(0.0, 0.000561123155 - Q.width)
        + 0.09184 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_0 - 376.5)
        + 1613.0 * max(0.0, 0.001101266364 - Q.e2_sq) * max(0.0, -0.009460449219 - Q.phi_1)
        - 0.07487 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_2 - 56.5)
        + 0.5395 * max(0.0, 0.197968879342 - Q.max_dr)
        + 168.9 * max(0.0, 0.005019718802 - Q.width)
        + 8.701 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.501026660204 - Q.tau21)
        + 11580.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 6.01 * max(0.0, 0.196739721581 - Q.LHA)
        + 6.62 * max(0.0, Q.log_sum_pt - 6.701242202626)
        - 1.589 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.40079469091 - Q.planar_flow)
        + 0.5213 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 248.125 - Q.sum_pt_top2)
        + 8.316 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.n_dr_0p05_0p1 - 0.0)
        - 68.33 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.mean_phi - -0.000855675264)
        + 13.68 * max(0.0, 0.061086014472 - Q.girth)
        - 0.0002258 * max(0.0, Q.sum_pt_top5 - 658.125)
        + 78.63 * max(0.0, 0.003343241496 - Q.centroid_offset)
        + 1.173 * max(0.0, 0.177304983139 - Q.max_dr)
        + 2011.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 0.1009733513 - Q.z_dr_0p2_0p4)
        - 61.53 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        - 0.6887 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 22710.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 5059.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.lam1 - 0.00027588256)
        - 9571.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.mass_over_sum_pt_sq - 0.00012320649)
        + 10130.0 * max(0.0, 0.177304983139 - Q.max_dr) * max(0.0, 0.000194798295 - Q.lam2)
        - 256.3 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.000306123359 - Q.lam2)
        - 0.03579 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 48.71875 - Q.pt_7)
        + 136.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.018827652745 - Q.girth2)
        - 11740.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.00023679558 - Q.mass_over_sum_pt_sq)
        - 6.284 * max(0.0, 0.016554418951 - Q.e2)
        - 145.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 8.649 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 4419.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000561123155 - Q.width)
        + 28.24 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_6 - 0.02160287394)
        - 2.941 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.04184 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, Q.sum_pt - 788.4484375)
        - 8019.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.005019718802 - Q.width)
        - 3730.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.000194798295 - Q.lam2)
        + 751.6 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 436.9 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 8378.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 6259.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000306123359 - Q.lam2)
        + 0.2536 * max(0.0, 8.379955863953 - Q.mass)
        - 0.04789 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.058613700176 - Q.z_7)
        + 12.73 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_7 - 0.016858545121)
        - 0.3773 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, Q.centroid_offset - 0.016278845848)
        - 1227.0 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971) * max(0.0, 0.000537286005 - Q.lam2)
        + 1126.0 * max(0.0, 0.000964142894 - Q.girth2)
        - 232.2 * max(0.0, 0.000222950415 - Q.girth2_top5)
        - 19.51 * max(0.0, 0.054649224505 - Q.girth)
        - 90.38 * max(0.0, Q.lam2 - 0.001130644719)
        + 2.358 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 127.9 * max(0.0, 0.006096650059 - Q.width)
        - 4.476 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.000872228216 - Q.lam1)
        - 170.1 * max(0.0, Q.girth2 - 0.018827652745)
        - 16.03 * max(0.0, 0.032346998155 - Q.e2)
        - 247.9 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.40079469091 - Q.planar_flow)
        + 95.91 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.055953954317 - Q.dr01)
        + 0.1499 * max(0.0, Q.n_dr_0p2_0p4 - 1.0)
        + 0.04705 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 6.842716632804 - Q.log_sum_pt)
        + 0.07207 * max(0.0, 0.221586732566 - Q.max_dr)
        - 3333.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.C2 - 0.030867108516)
        + 0.7286 * max(0.0, Q.C2 - 0.051192347892)
        + 17.3 * max(0.0, 0.018377780003 - Q.centroid_offset)
        + 3350.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.centroid_offset - 0.003343241496)
        + 8755.0 * max(0.0, 0.000172198326 - Q.width)
        - 48.02 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_5 - 0.036727111752)
        + 173.7 * max(0.0, 0.007520088344 - Q.girth2)
        - 2.031 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.002127561159 - Q.mean_phi2)
        + 0.07726 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 0.4286 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.pt_4 - 47.34375)
        - 285.6 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_4 - 0.047491459878)
        - 148.6 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, Q.eccentricity - 0.903125533696)
        + 34.52 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.620723099573 - Q.eccentricity)
        + 0.0278 * max(0.0, 41.377904891968 - Q.mass)
        - 0.0772 * max(0.0, 41.377904891968 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        - 7.922 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        + 20.1 * max(0.0, 0.076373631775 - Q.mass_over_sum_pt)
        + 128.7 * max(0.0, 0.001503553356 - Q.lam1)
        + 0.5304 * max(0.0, Q.max_dr - 0.15984864831)
        + 5.982 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 29.0421875 - Q.pt_7)
        + 0.4249 * max(0.0, Q.lam2 - 0.001130644719) * max(0.0, Q.mass_top2 - 16.308019673264)
        + 0.004291 * max(0.0, 35.5 - Q.pt_5)
        + 0.8912 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, 53.4375 - Q.pt_7)
        - 295.5 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.02644207105 - Q.mean_eta)
        - 0.002918 * max(0.0, 35.5 - Q.pt_5) * max(0.0, Q.min_pair_mass - 0.173071536962)
        - 1.443 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, Q.n_dr_0p05_0p1 - 1.0)
        + 36.36 * Q.e2
        - 436.1 * max(0.0, Q.lam2 - 0.000194798295)
        - 1.256 * max(0.0, Q.LHA - 0.303313749495)
        - 158.9 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, Q.planar_flow - 0.012569162668)
        - 3.298 * max(0.0, 6.267538488641 - Q.log_sum_pt)
        - 0.1794 * max(0.0, Q.centroid_offset - 0.00231612516) * max(0.0, 34.53125 - Q.pt_7)
        + 1.263 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 8.0 - Q.n_pt_above_50)
        - 0.06046 * max(0.0, Q.n_dr_0p2_0p4 - 2.0)
        + 198.5 * max(0.0, 0.004183811014 - Q.lam1)
        - 159.0 * max(0.0, 0.090413827016 - Q.mass_over_sum_pt)
        - 0.04048 * max(0.0, 3.0 - Q.n_dr_0p05_0p1)
        - 266.9 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 0.501026660204 - Q.tau21)
        - 1.792 * max(0.0, 0.269169217348 - Q.tau32)
        + 6.317 * max(0.0, Q.LHA - 0.303313749495) * max(0.0, 0.553068161011 - Q.tau21)
        - 0.2644 * max(0.0, 0.391541349888 - Q.tau21)
        - 51.98 * max(0.0, Q.eccentricity - 0.903125533696) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 0.58 * max(0.0, 0.269169217348 - Q.tau32) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 62.67 * max(0.0, 0.002412890926 - Q.girth2_top2)
        + 0.02066 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.pt_4 - 39.8125)
        + 0.3567 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.222994708167 - Q.dr_7)
        + 25.83 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 2.055451202393 - Q.D2)
        - 170.6 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, 0.175465903809 - Q.dr_7)
        - 13.49 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.z_4 - 0.075444822386)
        + 0.03175 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.sum_pt - 988.4078125)
        - 888.3 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.log_sum_pt - 6.701242202626)
        - 0.322 * max(0.0, Q.mass - 15.454033088684)
        + 0.6098 * max(0.0, Q.max_dr - 0.121680960059)
        + 0.002826 * max(0.0, Q.mass - 15.454033088684) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 510.5 * max(0.0, 0.0016538364 - Q.girth2)
        - 0.00618 * max(0.0, Q.sum_pt - 813.415625)
        - 89.09 * max(0.0, 0.006679471442 - Q.girth2)
        - 0.3081 * max(0.0, 0.253403707141 - Q.planar_flow)
        - 31.51 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.width - 0.006096650059)
        - 5.486 * max(0.0, 0.154689112391 - Q.LHA)
        + 27.77 * max(0.0, Q.girth - 0.076081777364)
        + 0.01046 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, 69.611351776123 - Q.mass)
        - 1.642 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.max_dr - 0.102758520097)
        + 0.8781 * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 0.0777 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 48.71875 - Q.pt_7)
        + 1.202 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, Q.n_dr_0p05_0p1 - 2.0)
        + 123.0 * max(0.0, 0.006390124748 - Q.e2_sq)
        - 2.123 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 0.009932 * max(0.0, 7.0 - Q.n_dr_0_0p05)
        + 39.57 * max(0.0, 0.006390124748 - Q.e2_sq) * max(0.0, 1.332146394253 - Q.D2)
        + 0.09194 * Q.centroid_offset
        + 52.49 * max(0.0, 0.003562611091 - Q.width)
        - 0.00175 * max(0.0, 9.257203159811 - Q.mass_top5)
        + 73.18 * max(0.0, 0.154689112391 - Q.LHA) * max(0.0, 0.028070914944 - Q.z_7)
        + 0.3152 * max(0.0, 15.454033088684 - Q.mass)
        - 0.3655 * max(0.0, Q.girth - 0.076081777364) * max(0.0, 7.0 - Q.n_pt_above_50)
        + 0.02432 * max(0.0, 29.0421875 - Q.pt_7)
        - 43.55 * max(0.0, 0.004839980301 - Q.lam1)
        + 0.7959 * max(0.0, 0.035786485299 - Q.C2)
        - 1.017 * max(0.0, 0.111761856824 - Q.max_dr)
        + 0.07687 * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 0.0002923 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 22.844978847276 - Q.mass_top2)
        - 0.05027 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.pt_5 - 43.0625)
        - 0.002656 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 0.005685 * max(0.0, Q.mass - 91.19)
        - 9157.0 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.lam2 - 0.000537286005)
        + 0.4495 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.pt_7 - 15.55390625)
        + 2.874 * max(0.0, Q.mean_phi - 0.026127964072)
        + 3.146 * max(0.0, 0.148408418149 - Q.girth)
        + 1.734 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 0.117 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 38.53125 - Q.pt_7)
        + 54.06 * max(0.0, 0.016433749775 - Q.lam1)
        + 0.09603 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, Q.z_7 - 0.023207568189)
        + 7916.0 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 0.0004541 * max(0.0, 531.1875 - Q.sum_pt_top5)
        + 6.944e-05 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, 43.5 - Q.pt_7)
        + 0.001457 * max(0.0, Q.sum_pt_top5 - 902.40625)
        - 0.0001229 * max(0.0, Q.sum_pt_top5 - 839.9546875)
        + 0.1221 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 56.53125 - Q.pt_6)
        + 4.737 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.pt_dispersion - 0.396830244362)
        - 0.01173 * max(0.0, 0.501026660204 - Q.tau21)
        - 248.3 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 0.037760993714 - Q.centroid_offset)
        - 0.6574 * max(0.0, 0.067272114405 - Q.z_6)
        + 14.22 * max(0.0, 0.037760993714 - Q.centroid_offset)
        - 9.959 * max(0.0, Q.LHA - 0.09323897448)
        - 0.0005647 * max(0.0, Q.sum_pt_top5 - 902.40625) * max(0.0, 3.885568320751 - Q.D2)
        + 0.0005518 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.15855820179 - Q.z_dr_0p1_0p2)
        - 0.2923 * max(0.0, 0.501026660204 - Q.tau21) * max(0.0, Q.max_dr - 0.015595615841)
        + 173.7 * max(0.0, 0.00752008842 - Q.width)
        + 0.06668 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 0.037477688199 - Q.z_4)
        - 0.006601 * max(0.0, 25.578125 - Q.pt_7)
        - 0.001889 * max(0.0, Q.sum_pt - 988.4078125)
        + 0.0006867 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 0.0006475 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, 3.885568320751 - Q.D2)
        - 3.546 * max(0.0, 0.111513564951 - Q.planar_flow)
        + 0.2166 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        - 18.45 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 56.18 * max(0.0, Q.lam1 - 0.008375572068)
        - 62.34 * max(0.0, Q.lam1 - 0.004183811014)
        + 19.64 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 0.15984864831 - Q.max_dr)
        - 111.8 * max(0.0, Q.lam1 - 0.00543336053)
        + 0.008191 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 739.5 - Q.sum_pt)
        - 118.9 * max(0.0, Q.lam1 - 0.007330079875)
        - 4.582 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 0.067292226106 - Q.C2)
        + 4827.0 * max(0.0, Q.lam1 - 0.007330079875) * max(0.0, 0.13261153996 - Q.max_dr)
        - 1.728 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235)
        - 2131.0 * max(0.0, Q.lam1 - 0.00543336053) * max(0.0, 0.15984864831 - Q.max_dr)
        + 6.558 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.009480684835)
        + 0.007364 * max(0.0, 76.655700683594 - Q.mass)
        - 4.868 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, Q.eccentricity - 0.970449631164)
        - 0.09857 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 108.4 * max(0.0, Q.lam1 - 0.005954149834)
        + 0.02419 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 33.82 * max(0.0, Q.lam1 - 0.002464291268)
        + 655.6 * max(0.0, 0.011660904657 - Q.mass_over_sum_pt_sq)
        + 0.01447 * max(0.0, 76.655700683594 - Q.mass) * max(0.0, 0.74595130682 - Q.D2)
        - 183.6 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.111513564951 - Q.planar_flow)
        + 1216.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.eccentricity - 0.970449631164)
        + 138.8 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        + 0.2842 * max(0.0, 1.122624260187 - Q.D2)
        - 23.54 * max(0.0, 0.038466955721 - Q.e2) * max(0.0, 1.002470755577 - Q.D2)
        + 0.02477 * max(0.0, 5.0 - Q.n_dr_0p05_0p1)
        - 4.392 * max(0.0, 1.122624260187 - Q.D2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 11.08 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, Q.eccentricity - 0.984196588116)
        - 0.3626 * max(0.0, 0.74595130682 - Q.D2)
        + 124.2 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 11.79 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        - 2.768 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 1.002470755577 - Q.D2)
        + 6.385 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 55.14 * max(0.0, 0.004372139461 - Q.girth2) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 13.27 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 0.6686 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 3.566 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.121680960059 - Q.max_dr)
        + 6.75 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        + 9119.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, Q.e2 - 0.024547699839)
        + 137.0 * max(0.0, 0.012003726523 - Q.lam1)
        - 151.4 * max(0.0, 0.011657374702 - Q.e2_sq)
        + 39.88 * max(0.0, 0.007182835724 - Q.mass_over_sum_pt_sq)
        + 0.01098 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.sum_pt_top3 - 353.0625)
        + 2.217 * max(0.0, 0.041109715588 - Q.e2)
        - 12.41 * max(0.0, 0.063441075385 - Q.e2)
        - 0.2145 * max(0.0, 0.328461505473 - Q.z_dr_0p1_0p2)
        + 0.9929 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 0.0333 * max(0.0, 2.0 - Q.n_dr_0_0p05)
        + 1.059 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.m01 - 16.308019673264)
        - 0.4988 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, Q.pt1_dr01 - 1.21960336377)
        - 0.01961 * max(0.0, Q.mass - 80.4) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 9.687 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.z_top5 - 0.865048766136)
        + 676.8 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.log_sum_pt - 6.896095378249)
        - 0.7045 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.mass_top2 - 22.844978847276)
        + 201.1 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.061262048692 - Q.planar_flow)
        - 81.15 * max(0.0, 0.06813910019 - Q.mass_over_sum_pt)
        + 0.0008437 * max(0.0, Q.n_dr_0p05_0p1 - 5.0)
        + 8.273 * max(0.0, Q.LHA - 0.346713497427)
        - 27.55 * max(0.0, Q.girth - 0.033604209498)
        + 8.428 * max(0.0, 0.002151567843 - Q.girth2_top3)
        - 1.36 * max(0.0, 0.007639643088 - Q.girth2_top2)
    )


def score_W(Q):
    return (2.598
        + 4.747 * max(0.0, 0.148419710734 - Q.planar_flow)
        + 59.98 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 472.9 * max(0.0, 0.004372139331 - Q.width)
        - 599.0 * max(0.0, 0.018827652745 - Q.girth2)
        - 0.03858 * max(0.0, 64.618731689453 - Q.mass)
        + 0.1499 * max(0.0, 21.784077072144 - Q.mass)
        - 59.6 * max(0.0, 0.007929074034 - Q.girth2_top3)
        - 321.8 * max(0.0, 0.013238675334 - Q.girth2)
        - 517.8 * max(0.0, 0.006506575659 - Q.lam1)
        - 707.6 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, 0.87567204833 - Q.D2)
        - 0.02286 * max(0.0, Q.sum_pt - 901.59375)
        - 0.03121 * max(0.0, 56.920347213745 - Q.mass)
        - 135.8 * max(0.0, 0.008678044951 - Q.width)
        + 0.0001151 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 25.578125 - Q.pt_7)
        - 0.01006 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 380.5875 - Q.sum_pt_top2)
        - 0.01142 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 0.038438041256 - Q.dr_2)
        - 0.01646 * max(0.0, 56.920347213745 - Q.mass) * max(0.0, Q.C2 - 0.023843882605)
        - 34.26 * max(0.0, 0.00832969537 - Q.girth2_top5)
        + 1.514 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971)
        - 0.04745 * max(0.0, 29.644699859619 - Q.mass)
        + 0.1218 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.87567204833 - Q.D2)
        - 52.53 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.111761856824 - Q.max_dr)
        + 58.58 * max(0.0, 0.087236513197 - Q.girth)
        + 16.66 * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 10820.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.centroid_offset - 0.014379521101)
        + 1.318 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, Q.centroid_offset - 0.012587644117)
        + 30.71 * max(0.0, 0.020459658932 - Q.e2)
        - 13570.0 * max(0.0, 0.008174660116 - Q.mass_over_sum_pt_sq)
        - 650.8 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.eccentricity - 0.959856212153)
        + 16.35 * max(0.0, Q.log_sum_pt - 6.638338705138)
        - 0.001743 * max(0.0, Q.sum_pt_top5 - 687.4375)
        - 0.2708 * max(0.0, 0.007929074034 - Q.girth2_top3) * max(0.0, 35.28125 - Q.pt_6)
        + 157.6 * max(0.0, 0.00543336053 - Q.lam1)
        - 1.388 * max(0.0, Q.log_sum_pt - 6.377722943814)
        + 0.09854 * max(0.0, Q.sum_pt_top5 - 687.4375) * max(0.0, Q.z_7 - 0.023207568189)
        + 132.9 * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 79.98 * max(0.0, 0.076081777364 - Q.girth)
        - 0.0004701 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, 40.040625 - Q.pt_7)
        - 3.533 * max(0.0, Q.log_sum_pt - 6.638338705138) * max(0.0, 0.093979107928 - Q.dr_7)
        - 0.02127 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, Q.phi_1 - -0.058901977539)
        - 163.7 * max(0.0, 0.004372139331 - Q.width) * max(0.0, Q.n_dr_0p1_0p2 - 1.0)
        - 44.97 * max(0.0, 0.13092863437 - Q.mass_over_sum_pt)
        + 28.76 * max(0.0, 0.012569162668 - Q.planar_flow)
        + 309.4 * max(0.0, 0.008375572068 - Q.lam1)
        - 0.003072 * max(0.0, Q.pt_7 - 34.53125)
        - 6050.0 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.centroid_offset - 0.02076709205)
        + 0.0002986 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 91.19 - Q.mass)
        - 21.55 * max(0.0, 0.035560912266 - Q.e2)
        - 16.71 * max(0.0, 0.055577157257 - Q.z_7)
        - 0.6891 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, Q.centroid_offset - 0.014379521101)
        - 63.7 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 0.05218 * max(0.0, 53.332374954224 - Q.mass)
        + 0.0007624 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 45.595 - Q.mass_top3)
        + 7.275 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.197968879342 - Q.max_dr)
        - 1.851 * max(0.0, Q.log_sum_pt - 6.572937922293)
        - 0.0369 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 0.553068161011 - Q.tau21)
        + 3363.0 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 222.1 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, Q.eccentricity - 0.978160776925)
        - 3.012 * max(0.0, 0.083662731125 - Q.planar_flow)
        + 168.3 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.042322802544 - Q.C2)
        - 1.324 * max(0.0, 0.197783735394 - Q.tau21)
        + 597.8 * max(0.0, 0.008168570676 - Q.e2_sq)
        - 0.149 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 0.080507021025 - Q.max_dr)
        - 0.0009196 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 32.617988451746 - Q.mass_top3)
        + 4.774 * max(0.0, 0.042322802544 - Q.C2)
        - 0.01326 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 50.25 - Q.pt_6)
        + 49.04 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006756161242 - Q.girth2_top3)
        + 1610.0 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 4872.0 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 0.000194798295 - Q.lam2)
        + 1624.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.001130644719 - Q.lam2)
        - 18.74 * max(0.0, 0.083662731125 - Q.planar_flow) * max(0.0, 0.269169217348 - Q.tau32)
        - 39.64 * max(0.0, 0.346713497427 - Q.LHA)
        - 18.33 * max(0.0, Q.e2 - 0.032346998155)
        - 23.78 * max(0.0, Q.mass_over_sum_pt - 0.054892207095)
        - 28.13 * max(0.0, 0.346713497427 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 13.62 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 1888.0 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 15.66 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 8.477 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.033200121667 - Q.planar_flow)
        + 0.07153 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.n_pt_above_50 - 7.0)
        - 4.992 * max(0.0, 0.046566883102 - Q.max_dr)
        - 30.72 * max(0.0, Q.e2 - 0.032346998155) * max(0.0, 0.641386964917 - Q.tau32)
        + 0.6642 * max(0.0, 69.611351776123 - Q.mass)
        - 0.01183 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.068101508468 - Q.z_7)
        + 2.549 * max(0.0, Q.log_sum_pt - 6.842716632804)
        - 1.361 * max(0.0, 6.464150123592 - Q.log_sum_pt)
        + 20.75 * max(0.0, 0.028070914944 - Q.z_7)
        + 155.5 * max(0.0, 0.005954149834 - Q.lam1)
        - 6018.0 * max(0.0, 9.1213921e-05 - Q.width)
        + 0.01589 * max(0.0, Q.pt_7 - 30.484375)
        - 0.1541 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, 0.051192347892 - Q.C2)
        - 7.066 * max(0.0, Q.z_7 - 0.046240320761)
        - 2228.0 * max(0.0, 0.028070914944 - Q.z_7) * max(0.0, 0.00752008842 - Q.width)
        - 0.5855 * max(0.0, Q.LHA - 0.111565049159)
        + 3373.0 * max(0.0, 0.005954149834 - Q.lam1) * max(0.0, Q.max_dr - 0.080507021025)
        - 0.05877 * max(0.0, 0.694781820497 - Q.planar_flow)
        - 0.1015 * max(0.0, 36.229410171509 - Q.mass)
        - 1.253e-05 * max(0.0, 56.53125 - Q.pt_6) * max(0.0, Q.m012 - 32.617988451746)
        + 7.191 * max(0.0, 36.229410171509 - Q.mass) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.262 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, Q.max_dr - 0.093110798299)
        + 191.2 * max(0.0, 0.003377388461 - Q.lam1)
        - 15400.0 * max(0.0, 0.003377388461 - Q.lam1) * max(0.0, 0.006789738266 - Q.centroid_offset)
        + 12.32 * max(0.0, 8.379955863953 - Q.mass) * max(0.0, 0.010960638421 - Q.centroid_offset)
        + 1.862 * max(0.0, 0.016858545121 - Q.z_7)
        + 0.002075 * max(0.0, 687.4375 - Q.sum_pt_top5)
        - 0.004582 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.04881348081 - Q.dr_7)
        + 0.005127 * max(0.0, 53.4375 - Q.pt_7)
        + 0.01085 * max(0.0, 43.5 - Q.pt_7)
        + 0.00431 * max(0.0, 788.4484375 - Q.sum_pt)
        - 0.7545 * max(0.0, Q.log_sum_pt - 6.267538488641)
        - 68.9 * max(0.0, Q.log_sum_pt - 6.896095378249)
        - 13060.0 * max(0.0, 4.8108519e-05 - Q.girth2)
        + 17.94 * max(0.0, Q.log_sum_pt - 6.804164030582)
        - 4.776 * max(0.0, 0.15984864831 - Q.max_dr)
        - 0.0003549 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, Q.max_pair_mass - 13.047927274731)
        - 10750.0 * max(0.0, 0.000172198326 - Q.width) * max(0.0, 0.222994708167 - Q.dr_7)
        - 73.77 * max(0.0, Q.mass_over_sum_pt - 0.06813910019)
        - 11.35 * max(0.0, Q.centroid_offset - 0.014379521101)
        + 43.19 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.518696343899 - Q.tau32)
        + 244.1 * max(0.0, Q.width - 0.018827653081)
        + 0.1133 * max(0.0, Q.mass - 36.229410171509)
        - 77.42 * max(0.0, Q.e2 - 0.028531698044)
        - 42.54 * max(0.0, Q.LHA - 0.312727471086)
        + 191.2 * max(0.0, 0.006679471358 - Q.width)
        - 0.2124 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.n_pt_above_50 - 3.0)
        - 31.55 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.001130644719 - Q.lam2)
        + 2.043 * max(0.0, 0.04447356835 - Q.e2)
        + 308.4 * max(0.0, 0.007330079875 - Q.lam1)
        - 6.941 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 5.0 - Q.n_dr_0_0p05)
        + 0.1213 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 50.352200171245 - Q.mass_top3)
        - 0.6484 * max(0.0, Q.mass - 69.611351776123)
        + 35.45 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, 0.964120104909 - Q.z_dr_0p05_0p1)
        - 135.9 * max(0.0, 0.008678044751 - Q.girth2)
        - 10.81 * max(0.0, Q.LHA - 0.325582223496)
        + 0.01995 * max(0.0, Q.mass - 36.229410171509) * max(0.0, Q.eccentricity - 0.620723099573)
        + 61.2 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.0)
        - 23.81 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, Q.phi_7 - -0.041534423828)
        + 0.0184 * max(0.0, Q.mass_top5 - 53.607658247923)
        - 2.536 * max(0.0, -0.012844925793 - Q.mean_eta)
        + 47.11 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, -0.039672851562 - Q.eta_0)
        + 155.1 * max(0.0, Q.width - 0.018827653081) * max(0.0, 0.492494773865 - Q.pt_dispersion)
        + 0.04564 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.046481671275 - Q.dr_6)
        + 219.7 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.042151962757 - Q.dr_7)
        + 1069.0 * max(0.0, Q.mass_over_sum_pt - 0.090413827016)
        - 472.9 * max(0.0, 0.004372139461 - Q.girth2)
        + 201.3 * max(0.0, Q.mass_over_sum_pt - 0.107985668755)
        + 1050.0 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 0.145231109113 - Q.max_dr)
        + 15.55 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.planar_flow - 0.00804883781)
        - 153.4 * max(0.0, Q.lam1 - 0.012003726523)
        - 8158.0 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 0.145231109113 - Q.max_dr)
        - 1.815 * max(0.0, Q.mass - 69.611351776123) * max(0.0, 0.177304983139 - Q.max_dr)
        - 0.1703 * max(0.0, Q.max_dr - 0.145231109113)
        + 91.69 * max(0.0, Q.max_dr - 0.145231109113) * max(0.0, 0.04586879935 - Q.dr_3)
        + 1647.0 * max(0.0, Q.lam1 - 0.016433749775) * max(0.0, Q.eccentricity - 0.959856212153)
        + 0.4621 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 68.125 - Q.pt_4)
        - 242.7 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 0.120257140434 - Q.z_4)
        - 0.9069 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 29.875 - Q.pt_5)
        - 550.3 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.959856212153)
        + 872.8 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.eccentricity - 0.959856212153)
        + 0.3034 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 56.53125 - Q.pt_6)
        + 1.096 * max(0.0, Q.lam1 - 0.012003726523) * max(0.0, 38.25 - Q.pt_6)
        + 0.8146 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 48.71875 - Q.pt_7)
        - 2.011 * max(0.0, Q.LHA - 0.423592510895)
        + 0.001423 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 20.125 - Q.pt_7)
        - 5.596 * max(0.0, 0.23799610585 - Q.tau21)
        + 0.03149 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 62.55 - Q.mass)
        + 603.0 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.e2_sq - 0.011657374702)
        + 692.1 * max(0.0, 0.000306123359 - Q.lam2)
        + 5058.0 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.001130644719 - Q.lam2)
        - 2563.0 * max(0.0, Q.width - 0.000319370692)
        - 0.02426 * max(0.0, 763.825 - Q.sum_pt)
        - 32.31 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.067292226106 - Q.C2)
        - 3978.0 * max(0.0, 0.009530300104 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.016278845848)
        + 4.417 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.planar_flow - 0.045057236346)
        + 10.45 * max(0.0, Q.width - 0.001653836415)
        + 0.0002699 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 579.7 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 3.707 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.175465903809 - Q.dr_7)
        + 10.82 * max(0.0, Q.C2 - 0.067292226106)
        - 903.6 * max(0.0, 0.001130644719 - Q.lam2)
        - 1.394 * max(0.0, 0.005011406868 - Q.girth2_top3)
        - 10.62 * max(0.0, 0.001130644719 - Q.lam2) * max(0.0, Q.n_dr_0p1_0p2 - 2.0)
        + 54.56 * max(0.0, Q.girth - 0.101940929517)
        + 59.59 * max(0.0, 0.017162483186 - Q.e2_sq)
        + 520.9 * max(0.0, Q.girth2 - 0.013238675334)
        + 0.0009041 * max(0.0, 430.75 - Q.sum_pt_top5)
        - 56.78 * max(0.0, Q.e2 - 0.063441075385)
        + 72.72 * max(0.0, Q.e2 - 0.007078157854)
        - 0.0006986 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.104247858869 - Q.dr_3)
        - 21.04 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, -0.025945045147 - Q.mean_phi)
        + 0.07787 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_7 - 33.21875)
        + 35.5 * max(0.0, 0.014379521101 - Q.centroid_offset)
        - 14.12 * max(0.0, Q.max_dr - 0.102758520097)
        + 2.818 * max(0.0, Q.mass_over_sum_pt - 0.107985668755) * max(0.0, 3.885568320751 - Q.D2)
        - 4.479 * max(0.0, Q.max_dr - 0.197968879342)
        - 0.3361 * max(0.0, Q.max_dr - 0.102758520097) * max(0.0, Q.pt_7 - 37.15625)
        - 3.004 * max(0.0, Q.C2 - 0.014943876117)
        + 0.1353 * max(0.0, Q.C2 - 0.014943876117) * max(0.0, Q.pt_7 - 38.53125)
        + 1.977 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 50.352200171245 - Q.mass_top3)
        - 1.607 * max(0.0, 0.014379521101 - Q.centroid_offset) * max(0.0, 0.674770402908 - Q.z_dr_0p05_0p1)
        - 18.4 * max(0.0, 0.047915700823 - Q.girth)
        + 0.0003192 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_2 - 73.6875)
        + 82.47 * max(0.0, 0.023780909279 - Q.e2_sq)
        + 475.9 * max(0.0, 0.001101860861 - Q.mass_over_sum_pt_sq)
        - 4.14 * max(0.0, 0.216055863061 - Q.LHA)
        - 7.123 * max(0.0, 0.049399692737 - Q.z_7)
        - 0.1474 * max(0.0, 0.049399692737 - Q.z_7) * max(0.0, 62.55 - Q.mass_top5)
        + 10.75 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 42.04 * max(0.0, 0.00528466865 - Q.e2_sq)
        - 1.207 * max(0.0, 0.028865759995 - Q.z_6)
        - 4.014 * max(0.0, 0.071488645583 - Q.z_7)
        + 22500.0 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, 0.014379521101 - Q.centroid_offset)
        + 6.86 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 0.05709 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 788.4484375 - Q.sum_pt)
        + 2836.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001503553356 - Q.lam1)
        + 3.257 * max(0.0, 0.03243272066 - Q.z_7)
        - 5.258 * max(0.0, 0.026454043164 - Q.dr_0)
        + 3.742 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 0.9355 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.n_dr_0p2_0p4 - 0.0)
        + 4.557 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 409.3 * max(0.0, 0.002635417778 - Q.width)
        - 1215.0 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt)
        + 119.1 * max(0.0, 0.002270363079 - Q.girth2_top5)
        + 0.0008007 * max(0.0, Q.sum_pt_top5 - 752.1)
        - 1521.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.0002921 * max(0.0, 548.196875 - Q.sum_pt_top2)
        - 4274.0 * max(0.0, 0.002635417778 - Q.width) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 287.4 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 0.06794 * max(0.0, 0.03243272066 - Q.z_7) * max(0.0, Q.pt_5 - 33.0265625)
        - 0.00136 * max(0.0, 24.578125 - Q.pt_5)
        + 0.0009358 * max(0.0, Q.sum_pt - 868.509375)
        - 0.07291 * max(0.0, Q.sum_pt - 868.509375) * max(0.0, 0.012587644117 - Q.centroid_offset)
        + 0.2814 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, Q.mass_top3 - 28.345095968085)
        + 172.6 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.018377780003 - Q.centroid_offset)
        - 1811.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.000145482056 - Q.mean_phi2)
        - 0.002473 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.021588001063 - Q.dr_0)
        - 70.15 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.021588001063 - Q.dr_0)
        - 128.6 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.04118638065 - Q.dr_0)
        - 9.75 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.004331280361 - Q.mean_phi2)
        - 31.51 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.012003726523 - Q.lam1)
        - 110.6 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006299534492 - Q.girth2_top2)
        - 0.06008 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 3946.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 9.0303693e-05 - Q.mean_eta2)
        - 0.00945 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, 18.097979966098 - Q.max_pair_mass)
        + 0.04917 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.mass_top3 - 3.559569591142)
        + 9.448 * max(0.0, 0.01426135283 - Q.mean_phi2)
        - 0.3187 * max(0.0, 0.01426135283 - Q.mean_phi2) * max(0.0, 40.046952646555 - Q.max_pair_mass)
        - 26.06 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 80770.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, 7.3007261e-05 - Q.lam2)
        + 15.26 * max(0.0, 0.021588001063 - Q.dr_0)
        + 4.741 * max(0.0, Q.centroid_offset - 0.008092360237)
        - 321.7 * max(0.0, 0.013238675006 - Q.width)
        - 46.91 * max(0.0, 0.154170806525 - Q.mass_over_sum_pt)
        - 1.173 * max(0.0, 6.327378592257 - Q.log_sum_pt)
        - 13170.0 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.003408388935 - Q.lam2)
        - 143.9 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, 0.071488645583 - Q.z_7)
        - 78.78 * max(0.0, 0.050284641981 - Q.e2)
        - 47.85 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, Q.planar_flow - 0.00804883781)
        + 175.0 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.094821243733 - Q.C2)
        + 19.95 * max(0.0, Q.centroid_offset - 0.018377780003)
        + 0.07712 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, Q.pt_6 - 27.578125)
        + 14.02 * max(0.0, 6.701242202626 - Q.log_sum_pt)
        - 53.95 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 0.049399692737 - Q.z_7)
        - 27.02 * max(0.0, Q.centroid_offset - 0.049903668404)
        + 4.442 * Q.max_dr
        + 0.3199 * max(0.0, Q.C2 - 0.010539266048)
        - 559.4 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 0.008921136335 - Q.mean_phi2)
        - 30.59 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.872657364787)
        + 4.571 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 4.0 - Q.n_dr_0p05_0p1)
        + 207.8 * max(0.0, 0.000537286005 - Q.lam2)
        - 625.9 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_phi - 0.026127964072)
        + 44.13 * max(0.0, Q.mass_over_sum_pt - 0.008374148675)
        - 109.0 * max(0.0, Q.girth2_top5 - 0.011482925368)
        + 9.816 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, Q.mean_phi - 0.009050007537)
        + 6.666 * max(0.0, Q.girth - 0.087236513197)
        + 9.69 * max(0.0, Q.mass_over_sum_pt - 0.008374148675) * max(0.0, 0.518696343899 - Q.tau32)
        + 0.1457 * max(0.0, 1.679198372364 - Q.D2)
        - 0.1043 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, Q.pt_2 - 56.5)
        + 263.6 * max(0.0, 0.007330079875 - Q.lam1) * max(0.0, 1.232133567333 - Q.D2)
        - 92.16 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.15855820179)
        + 511.6 * max(0.0, Q.lam2 - 0.003408388935)
        - 0.002613 * max(0.0, 6.572937922293 - Q.log_sum_pt)
        - 0.03062 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 36.8125 - Q.pt_6)
        - 17.43 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 24.578125 - Q.pt_5)
        - 2003.0 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_eta - 0.02644207105)
        + 17290.0 * max(0.0, 0.000537286005 - Q.lam2) * max(0.0, Q.mean_eta - 0.02644207105)
        - 249.8 * max(0.0, 0.003562611155 - Q.girth2)
        - 0.01239 * max(0.0, 49.668099212646 - Q.mass)
        + 28.74 * max(0.0, Q.girth2_top5 - 0.002270363079)
        + 0.0005897 * max(0.0, 1.679198372364 - Q.D2) * max(0.0, 90.625 - Q.pt_4)
        - 4.611 * max(0.0, Q.z_7 - 0.06164517166)
        - 0.09215 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 45.75 - Q.pt_7)
        - 0.5599 * max(0.0, Q.C2 - 0.010539266048) * max(0.0, Q.pt_7 - 31.859375)
        - 0.01614 * max(0.0, 49.668099212646 - Q.mass) * max(0.0, 0.750909513235 - Q.z_dr_0p05_0p1)
        + 0.2025 * max(0.0, 0.195013533663 - Q.planar_flow)
        + 569.7 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.width - 0.00752008842)
        - 414.9 * max(0.0, 0.001056655216 - Q.girth2_top2)
        + 1551.0 * max(0.0, Q.girth2 - 0.007520088344)
        + 389.3 * max(0.0, Q.girth2 - 0.004372139461)
        + 61.4 * max(0.0, Q.mass_over_sum_pt - 0.072690732432)
        + 27010.0 * max(0.0, 0.001056655216 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 10.45 * max(0.0, Q.girth2 - 0.0016538364)
        + 225.2 * max(0.0, 0.024547699839 - Q.e2)
        - 0.04123 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, 35.28125 - Q.pt_6)
        - 19.69 * max(0.0, 0.04081947431 - Q.girth)
        + 0.03228 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.mass_top3 - 23.663861485439)
        + 0.002332 * max(0.0, 48.71875 - Q.pt_7)
        + 0.005207 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.sum_pt - 615.875)
        - 96.67 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        - 1071.0 * max(0.0, 0.005590288644 - Q.width)
        + 18.01 * max(0.0, 0.02076709205 - Q.centroid_offset)
        + 688.8 * max(0.0, Q.girth2 - 0.008678044751)
        - 1354.0 * max(0.0, Q.mass_over_sum_pt - 0.084751611895)
        - 49.78 * max(0.0, 0.001101266364 - Q.e2_sq)
        + 0.02656 * max(0.0, Q.mass - 80.4)
        - 1334.0 * max(0.0, Q.girth2 - 0.004372139461) * max(0.0, Q.eccentricity - 0.945820652852)
        - 282.9 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, 1.122624260187 - Q.D2)
        + 46.56 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 1.122624260187 - Q.D2)
        - 6.698 * max(0.0, 0.038466955721 - Q.e2)
        - 186.6 * max(0.0, 0.02076709205 - Q.centroid_offset) * max(0.0, Q.C2 - 0.023843882605)
        + 0.01102 * max(0.0, Q.mass - 80.4) * max(0.0, Q.eccentricity - 0.927072033478)
        - 0.003167 * max(0.0, 48.71875 - Q.pt_7) * max(0.0, 0.694781820497 - Q.planar_flow)
        + 6.152 * max(0.0, Q.centroid_offset - 0.031170772021)
        + 12.51 * max(0.0, 0.293190627853 - Q.LHA)
        + 35.07 * max(0.0, 0.005884990035 - Q.girth2_top3)
        - 1790.0 * max(0.0, 0.000561123155 - Q.width)
        - 0.4582 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_0 - 376.5)
        - 1370.0 * max(0.0, 0.001101266364 - Q.e2_sq) * max(0.0, -0.009460449219 - Q.phi_1)
        - 0.6936 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_2 - 56.5)
        - 4.215 * max(0.0, 0.197968879342 - Q.max_dr)
        - 1068.0 * max(0.0, 0.005019718802 - Q.width)
        + 292.8 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.501026660204 - Q.tau21)
        - 17410.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 21.64 * max(0.0, 0.196739721581 - Q.LHA)
        + 11.86 * max(0.0, Q.log_sum_pt - 6.701242202626)
        - 258.4 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.40079469091 - Q.planar_flow)
        - 0.3971 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 248.125 - Q.sum_pt_top2)
        + 73.03 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.n_dr_0p05_0p1 - 0.0)
        + 137.3 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.mean_phi - -0.000855675264)
        - 146.7 * max(0.0, 0.061086014472 - Q.girth)
        + 0.003024 * max(0.0, Q.sum_pt_top5 - 658.125)
        - 94.41 * max(0.0, 0.003343241496 - Q.centroid_offset)
        + 1.907 * max(0.0, 0.177304983139 - Q.max_dr)
        - 4255.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 0.1009733513 - Q.z_dr_0p2_0p4)
        - 277.4 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        - 1.123 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        + 62610.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 46040.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.lam1 - 0.00027588256)
        - 1517.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.mass_over_sum_pt_sq - 0.00012320649)
        + 9188.0 * max(0.0, 0.177304983139 - Q.max_dr) * max(0.0, 0.000194798295 - Q.lam2)
        + 175.8 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.000306123359 - Q.lam2)
        - 0.03472 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 48.71875 - Q.pt_7)
        - 236.8 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.018827652745 - Q.girth2)
        + 1225.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.00023679558 - Q.mass_over_sum_pt_sq)
        + 9.928 * max(0.0, 0.016554418951 - Q.e2)
        + 140.5 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 5.335 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 9773.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000561123155 - Q.width)
        + 36.86 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_6 - 0.02160287394)
        + 9.023 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.08159 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, Q.sum_pt - 788.4484375)
        + 58450.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.005019718802 - Q.width)
        - 29900.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.000194798295 - Q.lam2)
        - 3590.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 1703.0 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 3254.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 3171.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000306123359 - Q.lam2)
        - 0.03561 * max(0.0, 8.379955863953 - Q.mass)
        + 0.8216 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.058613700176 - Q.z_7)
        - 74.64 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_7 - 0.016858545121)
        - 3.52 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, Q.centroid_offset - 0.016278845848)
        + 7309.0 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971) * max(0.0, 0.000537286005 - Q.lam2)
        - 1721.0 * max(0.0, 0.000964142894 - Q.girth2)
        + 1314.0 * max(0.0, 0.000222950415 - Q.girth2_top5)
        + 40.45 * max(0.0, 0.054649224505 - Q.girth)
        + 930.5 * max(0.0, Q.lam2 - 0.001130644719)
        - 1.61 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        - 803.6 * max(0.0, 0.006096650059 - Q.width)
        + 44.22 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.000872228216 - Q.lam1)
        + 244.1 * max(0.0, Q.girth2 - 0.018827652745)
        - 45.5 * max(0.0, 0.032346998155 - Q.e2)
        + 218.6 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.40079469091 - Q.planar_flow)
        - 67.3 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.055953954317 - Q.dr01)
        - 0.2827 * max(0.0, Q.n_dr_0p2_0p4 - 1.0)
        - 0.01961 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 6.842716632804 - Q.log_sum_pt)
        + 5.312 * max(0.0, 0.221586732566 - Q.max_dr)
        + 3986.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.C2 - 0.030867108516)
        - 13.31 * max(0.0, Q.C2 - 0.051192347892)
        + 33.24 * max(0.0, 0.018377780003 - Q.centroid_offset)
        + 10180.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.centroid_offset - 0.003343241496)
        - 1188.0 * max(0.0, 0.000172198326 - Q.width)
        + 23.54 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_5 - 0.036727111752)
        + 738.7 * max(0.0, 0.007520088344 - Q.girth2)
        + 2.272 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.002127561159 - Q.mean_phi2)
        - 0.136 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 0.2542 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.pt_4 - 47.34375)
        - 203.1 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_4 - 0.047491459878)
        + 109.0 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, Q.eccentricity - 0.903125533696)
        - 42.69 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.620723099573 - Q.eccentricity)
        - 0.02591 * max(0.0, 41.377904891968 - Q.mass)
        + 0.1323 * max(0.0, 41.377904891968 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 10.75 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        + 15.53 * max(0.0, 0.076373631775 - Q.mass_over_sum_pt)
        + 1038.0 * max(0.0, 0.001503553356 - Q.lam1)
        - 2.71 * max(0.0, Q.max_dr - 0.15984864831)
        - 7.378 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 29.0421875 - Q.pt_7)
        - 0.1617 * max(0.0, Q.lam2 - 0.001130644719) * max(0.0, Q.mass_top2 - 16.308019673264)
        - 0.00122 * max(0.0, 35.5 - Q.pt_5)
        - 0.9528 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, 53.4375 - Q.pt_7)
        + 149.3 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.02644207105 - Q.mean_eta)
        + 0.0004325 * max(0.0, 35.5 - Q.pt_5) * max(0.0, Q.min_pair_mass - 0.173071536962)
        + 5.429 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, Q.n_dr_0p05_0p1 - 1.0)
        + 36.03 * Q.e2
        - 1466.0 * max(0.0, Q.lam2 - 0.000194798295)
        + 44.65 * max(0.0, Q.LHA - 0.303313749495)
        - 261.7 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, Q.planar_flow - 0.012569162668)
        - 1.391 * max(0.0, 6.267538488641 - Q.log_sum_pt)
        - 0.4235 * max(0.0, Q.centroid_offset - 0.00231612516) * max(0.0, 34.53125 - Q.pt_7)
        + 8.332 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 8.0 - Q.n_pt_above_50)
        + 0.3685 * max(0.0, Q.n_dr_0p2_0p4 - 2.0)
        + 276.9 * max(0.0, 0.004183811014 - Q.lam1)
        + 1207.0 * max(0.0, 0.090413827016 - Q.mass_over_sum_pt)
        - 0.02486 * max(0.0, 3.0 - Q.n_dr_0p05_0p1)
        + 58.45 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 0.501026660204 - Q.tau21)
        - 1.192 * max(0.0, 0.269169217348 - Q.tau32)
        - 17.78 * max(0.0, Q.LHA - 0.303313749495) * max(0.0, 0.553068161011 - Q.tau21)
        + 0.5688 * max(0.0, 0.391541349888 - Q.tau21)
        + 106.0 * max(0.0, Q.eccentricity - 0.903125533696) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 0.434 * max(0.0, 0.269169217348 - Q.tau32) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 0.3684 * max(0.0, 0.002412890926 - Q.girth2_top2)
        + 0.007906 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.pt_4 - 39.8125)
        - 0.09358 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.222994708167 - Q.dr_7)
        - 103.0 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 2.055451202393 - Q.D2)
        + 229.5 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, 0.175465903809 - Q.dr_7)
        - 11.21 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.z_4 - 0.075444822386)
        - 1.774 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.sum_pt - 988.4078125)
        + 1569.0 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.log_sum_pt - 6.701242202626)
        + 0.5734 * max(0.0, Q.mass - 15.454033088684)
        - 5.887 * max(0.0, Q.max_dr - 0.121680960059)
        - 0.007553 * max(0.0, Q.mass - 15.454033088684) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 675.4 * max(0.0, 0.0016538364 - Q.girth2)
        - 0.02879 * max(0.0, Q.sum_pt - 813.415625)
        + 191.2 * max(0.0, 0.006679471442 - Q.girth2)
        + 0.4347 * max(0.0, 0.253403707141 - Q.planar_flow)
        - 169.2 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.width - 0.006096650059)
        - 8.765 * max(0.0, 0.154689112391 - Q.LHA)
        - 138.5 * max(0.0, Q.girth - 0.076081777364)
        - 0.008425 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, 69.611351776123 - Q.mass)
        + 1.071 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.max_dr - 0.102758520097)
        + 1.393 * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 0.3143 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 48.71875 - Q.pt_7)
        - 0.3764 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, Q.n_dr_0p05_0p1 - 2.0)
        - 527.7 * max(0.0, 0.006390124748 - Q.e2_sq)
        - 8.806 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 0.1128 * max(0.0, 7.0 - Q.n_dr_0_0p05)
        - 223.3 * max(0.0, 0.006390124748 - Q.e2_sq) * max(0.0, 1.332146394253 - Q.D2)
        - 12.5 * Q.centroid_offset
        - 249.8 * max(0.0, 0.003562611091 - Q.width)
        + 0.01199 * max(0.0, 9.257203159811 - Q.mass_top5)
        + 129.3 * max(0.0, 0.154689112391 - Q.LHA) * max(0.0, 0.028070914944 - Q.z_7)
        - 0.5961 * max(0.0, 15.454033088684 - Q.mass)
        - 0.6039 * max(0.0, Q.girth - 0.076081777364) * max(0.0, 7.0 - Q.n_pt_above_50)
        - 0.04698 * max(0.0, 29.0421875 - Q.pt_7)
        + 181.7 * max(0.0, 0.004839980301 - Q.lam1)
        - 19.81 * max(0.0, 0.035786485299 - Q.C2)
        + 7.611 * max(0.0, 0.111761856824 - Q.max_dr)
        - 0.3496 * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 0.0008231 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 22.844978847276 - Q.mass_top2)
        - 0.09373 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.pt_5 - 43.0625)
        - 0.01136 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 0.04001 * max(0.0, Q.mass - 91.19)
        - 5145.0 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.lam2 - 0.000537286005)
        + 1.965 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.pt_7 - 15.55390625)
        - 8.333 * max(0.0, Q.mean_phi - 0.026127964072)
        + 22.86 * max(0.0, 0.148408418149 - Q.girth)
        + 15.79 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 0.2029 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 38.53125 - Q.pt_7)
        + 0.8371 * max(0.0, 0.016433749775 - Q.lam1)
        - 0.1845 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, Q.z_7 - 0.023207568189)
        - 9398.0 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 0.0001526 * max(0.0, 531.1875 - Q.sum_pt_top5)
        - 4.876e-07 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, 43.5 - Q.pt_7)
        - 0.0004759 * max(0.0, Q.sum_pt_top5 - 902.40625)
        + 0.000343 * max(0.0, Q.sum_pt_top5 - 839.9546875)
        + 0.3197 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 56.53125 - Q.pt_6)
        + 4.853 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.pt_dispersion - 0.396830244362)
        + 0.01288 * max(0.0, 0.501026660204 - Q.tau21)
        - 0.3324 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 0.037760993714 - Q.centroid_offset)
        - 2.397 * max(0.0, 0.067272114405 - Q.z_6)
        - 52.83 * max(0.0, 0.037760993714 - Q.centroid_offset)
        + 5.335 * max(0.0, Q.LHA - 0.09323897448)
        - 0.0002892 * max(0.0, Q.sum_pt_top5 - 902.40625) * max(0.0, 3.885568320751 - Q.D2)
        + 0.004676 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.15855820179 - Q.z_dr_0p1_0p2)
        - 4.73 * max(0.0, 0.501026660204 - Q.tau21) * max(0.0, Q.max_dr - 0.015595615841)
        + 738.8 * max(0.0, 0.00752008842 - Q.width)
        + 0.3695 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 0.037477688199 - Q.z_4)
        - 0.01214 * max(0.0, 25.578125 - Q.pt_7)
        + 0.05097 * max(0.0, Q.sum_pt - 988.4078125)
        + 0.00124 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 0.0001245 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, 3.885568320751 - Q.D2)
        + 2.434 * max(0.0, 0.111513564951 - Q.planar_flow)
        - 0.5409 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 248.4 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 214.9 * max(0.0, Q.lam1 - 0.008375572068)
        - 212.6 * max(0.0, Q.lam1 - 0.004183811014)
        + 1.348 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 0.15984864831 - Q.max_dr)
        - 311.8 * max(0.0, Q.lam1 - 0.00543336053)
        + 0.0005162 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 739.5 - Q.sum_pt)
        - 226.4 * max(0.0, Q.lam1 - 0.007330079875)
        - 4.092 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 0.067292226106 - Q.C2)
        - 58590.0 * max(0.0, Q.lam1 - 0.007330079875) * max(0.0, 0.13261153996 - Q.max_dr)
        + 6.152 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235)
        + 9621.0 * max(0.0, Q.lam1 - 0.00543336053) * max(0.0, 0.15984864831 - Q.max_dr)
        - 86.89 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.009480684835)
        - 0.01343 * max(0.0, 76.655700683594 - Q.mass)
        - 2.926 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, Q.eccentricity - 0.970449631164)
        - 3.748 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 333.7 * max(0.0, Q.lam1 - 0.005954149834)
        - 0.1386 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 743.6 * max(0.0, Q.lam1 - 0.002464291268)
        - 778.7 * max(0.0, 0.011660904657 - Q.mass_over_sum_pt_sq)
        - 0.001427 * max(0.0, 76.655700683594 - Q.mass) * max(0.0, 0.74595130682 - Q.D2)
        + 435.8 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.111513564951 - Q.planar_flow)
        - 1639.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.eccentricity - 0.970449631164)
        - 1316.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        - 0.9754 * max(0.0, 1.122624260187 - Q.D2)
        + 58.64 * max(0.0, 0.038466955721 - Q.e2) * max(0.0, 1.002470755577 - Q.D2)
        + 0.01322 * max(0.0, 5.0 - Q.n_dr_0p05_0p1)
        - 6.677 * max(0.0, 1.122624260187 - Q.D2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 32.3 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, Q.eccentricity - 0.984196588116)
        + 0.6846 * max(0.0, 0.74595130682 - Q.D2)
        - 629.1 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 1260.0 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        - 57.36 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 1.002470755577 - Q.D2)
        - 77.81 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 26.78 * max(0.0, 0.004372139461 - Q.girth2) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        + 47.02 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 5.75 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 44.51 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.121680960059 - Q.max_dr)
        - 24.23 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 82980.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, Q.e2 - 0.024547699839)
        + 372.0 * max(0.0, 0.012003726523 - Q.lam1)
        + 94.21 * max(0.0, 0.011657374702 - Q.e2_sq)
        + 14910.0 * max(0.0, 0.007182835724 - Q.mass_over_sum_pt_sq)
        - 0.01461 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.sum_pt_top3 - 353.0625)
        - 114.1 * max(0.0, 0.041109715588 - Q.e2)
        - 41.55 * max(0.0, 0.063441075385 - Q.e2)
        - 0.06851 * max(0.0, 0.328461505473 - Q.z_dr_0p1_0p2)
        - 0.4727 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 0.012 * max(0.0, 2.0 - Q.n_dr_0_0p05)
        + 3.552 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.m01 - 16.308019673264)
        - 4.102 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, Q.pt1_dr01 - 1.21960336377)
        + 0.2615 * max(0.0, Q.mass - 80.4) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        + 28.76 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.z_top5 - 0.865048766136)
        + 5230.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.log_sum_pt - 6.896095378249)
        + 0.6241 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.mass_top2 - 22.844978847276)
        + 572.7 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.061262048692 - Q.planar_flow)
        + 68.77 * max(0.0, 0.06813910019 - Q.mass_over_sum_pt)
        - 0.04028 * max(0.0, Q.n_dr_0p05_0p1 - 5.0)
        + 71.58 * max(0.0, Q.LHA - 0.346713497427)
        - 57.51 * max(0.0, Q.girth - 0.033604209498)
        + 3.611 * max(0.0, 0.002151567843 - Q.girth2_top3)
        + 8.567 * max(0.0, 0.007639643088 - Q.girth2_top2)
    )


def score_Z(Q):
    return (0.09546
        - 0.03211 * max(0.0, 0.148419710734 - Q.planar_flow)
        + 152.7 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 246.1 * max(0.0, 0.004372139331 - Q.width)
        - 60.69 * max(0.0, 0.018827652745 - Q.girth2)
        - 0.0194 * max(0.0, 64.618731689453 - Q.mass)
        + 0.01244 * max(0.0, 21.784077072144 - Q.mass)
        - 10.72 * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 267.8 * max(0.0, 0.013238675334 - Q.girth2)
        + 66.65 * max(0.0, 0.006506575659 - Q.lam1)
        + 365.2 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, 0.87567204833 - Q.D2)
        - 0.03107 * max(0.0, Q.sum_pt - 901.59375)
        + 0.002332 * max(0.0, 56.920347213745 - Q.mass)
        + 604.3 * max(0.0, 0.008678044951 - Q.width)
        - 2.681e-05 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 25.578125 - Q.pt_7)
        + 0.001909 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 380.5875 - Q.sum_pt_top2)
        - 0.007098 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 0.038438041256 - Q.dr_2)
        - 0.2431 * max(0.0, 56.920347213745 - Q.mass) * max(0.0, Q.C2 - 0.023843882605)
        + 52.83 * max(0.0, 0.00832969537 - Q.girth2_top5)
        - 0.2749 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971)
        + 0.01629 * max(0.0, 29.644699859619 - Q.mass)
        - 0.06602 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.87567204833 - Q.D2)
        + 66.75 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.111761856824 - Q.max_dr)
        - 36.42 * max(0.0, 0.087236513197 - Q.girth)
        - 8.202 * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 10060.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.centroid_offset - 0.014379521101)
        + 0.8706 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, Q.centroid_offset - 0.012587644117)
        + 74.65 * max(0.0, 0.020459658932 - Q.e2)
        - 5683.0 * max(0.0, 0.008174660116 - Q.mass_over_sum_pt_sq)
        - 1266.0 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.eccentricity - 0.959856212153)
        + 19.97 * max(0.0, Q.log_sum_pt - 6.638338705138)
        - 0.00204 * max(0.0, Q.sum_pt_top5 - 687.4375)
        + 0.02763 * max(0.0, 0.007929074034 - Q.girth2_top3) * max(0.0, 35.28125 - Q.pt_6)
        + 12.47 * max(0.0, 0.00543336053 - Q.lam1)
        - 0.4821 * max(0.0, Q.log_sum_pt - 6.377722943814)
        + 0.09759 * max(0.0, Q.sum_pt_top5 - 687.4375) * max(0.0, Q.z_7 - 0.023207568189)
        + 46.72 * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 5.992 * max(0.0, 0.076081777364 - Q.girth)
        + 0.0004427 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, 40.040625 - Q.pt_7)
        - 6.443 * max(0.0, Q.log_sum_pt - 6.638338705138) * max(0.0, 0.093979107928 - Q.dr_7)
        - 0.01372 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, Q.phi_1 - -0.058901977539)
        + 151.2 * max(0.0, 0.004372139331 - Q.width) * max(0.0, Q.n_dr_0p1_0p2 - 1.0)
        + 74.63 * max(0.0, 0.13092863437 - Q.mass_over_sum_pt)
        - 1.494 * max(0.0, 0.012569162668 - Q.planar_flow)
        - 140.1 * max(0.0, 0.008375572068 - Q.lam1)
        + 0.03153 * max(0.0, Q.pt_7 - 34.53125)
        - 1162.0 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.centroid_offset - 0.02076709205)
        - 0.0003099 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 91.19 - Q.mass)
        - 48.31 * max(0.0, 0.035560912266 - Q.e2)
        - 10.77 * max(0.0, 0.055577157257 - Q.z_7)
        - 0.2283 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, Q.centroid_offset - 0.014379521101)
        - 114.0 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 0.02229 * max(0.0, 53.332374954224 - Q.mass)
        + 0.00181 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 45.595 - Q.mass_top3)
        + 1.619 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.197968879342 - Q.max_dr)
        - 6.01 * max(0.0, Q.log_sum_pt - 6.572937922293)
        - 0.06076 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 0.553068161011 - Q.tau21)
        + 708.6 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 1315.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, Q.eccentricity - 0.978160776925)
        + 2.771 * max(0.0, 0.083662731125 - Q.planar_flow)
        + 185.4 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.042322802544 - Q.C2)
        + 0.3433 * max(0.0, 0.197783735394 - Q.tau21)
        - 415.6 * max(0.0, 0.008168570676 - Q.e2_sq)
        - 0.147 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 0.080507021025 - Q.max_dr)
        - 0.00195 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 32.617988451746 - Q.mass_top3)
        - 6.49 * max(0.0, 0.042322802544 - Q.C2)
        - 0.02012 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 50.25 - Q.pt_6)
        - 150.2 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006756161242 - Q.girth2_top3)
        + 518.5 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.007929074034 - Q.girth2_top3)
        - 6.652 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 0.000194798295 - Q.lam2)
        + 1469.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.001130644719 - Q.lam2)
        - 13.67 * max(0.0, 0.083662731125 - Q.planar_flow) * max(0.0, 0.269169217348 - Q.tau32)
        - 27.34 * max(0.0, 0.346713497427 - Q.LHA)
        + 5.306 * max(0.0, Q.e2 - 0.032346998155)
        - 39.95 * max(0.0, Q.mass_over_sum_pt - 0.054892207095)
        - 24.01 * max(0.0, 0.346713497427 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 13.06 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 1514.0 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 25.43 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 14.99 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.033200121667 - Q.planar_flow)
        - 0.7179 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.n_pt_above_50 - 7.0)
        + 2.913 * max(0.0, 0.046566883102 - Q.max_dr)
        - 35.47 * max(0.0, Q.e2 - 0.032346998155) * max(0.0, 0.641386964917 - Q.tau32)
        + 0.1506 * max(0.0, 69.611351776123 - Q.mass)
        + 0.06072 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.068101508468 - Q.z_7)
        + 0.8135 * max(0.0, Q.log_sum_pt - 6.842716632804)
        - 1.455 * max(0.0, 6.464150123592 - Q.log_sum_pt)
        - 7.999 * max(0.0, 0.028070914944 - Q.z_7)
        + 53.75 * max(0.0, 0.005954149834 - Q.lam1)
        - 1813.0 * max(0.0, 9.1213921e-05 - Q.width)
        + 0.03156 * max(0.0, Q.pt_7 - 30.484375)
        - 0.5827 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, 0.051192347892 - Q.C2)
        - 5.274 * max(0.0, Q.z_7 - 0.046240320761)
        + 2681.0 * max(0.0, 0.028070914944 - Q.z_7) * max(0.0, 0.00752008842 - Q.width)
        + 1.065 * max(0.0, Q.LHA - 0.111565049159)
        + 53.46 * max(0.0, 0.005954149834 - Q.lam1) * max(0.0, Q.max_dr - 0.080507021025)
        + 0.05684 * max(0.0, 0.694781820497 - Q.planar_flow)
        + 0.01125 * max(0.0, 36.229410171509 - Q.mass)
        - 0.0001435 * max(0.0, 56.53125 - Q.pt_6) * max(0.0, Q.m012 - 32.617988451746)
        - 9.341 * max(0.0, 36.229410171509 - Q.mass) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.1665 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, Q.max_dr - 0.093110798299)
        + 258.6 * max(0.0, 0.003377388461 - Q.lam1)
        - 5990.0 * max(0.0, 0.003377388461 - Q.lam1) * max(0.0, 0.006789738266 - Q.centroid_offset)
        + 4.759 * max(0.0, 8.379955863953 - Q.mass) * max(0.0, 0.010960638421 - Q.centroid_offset)
        + 5.376 * max(0.0, 0.016858545121 - Q.z_7)
        - 0.0007326 * max(0.0, 687.4375 - Q.sum_pt_top5)
        - 0.003061 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.04881348081 - Q.dr_7)
        + 0.00262 * max(0.0, 53.4375 - Q.pt_7)
        + 0.009963 * max(0.0, 43.5 - Q.pt_7)
        + 0.002852 * max(0.0, 788.4484375 - Q.sum_pt)
        - 4.686 * max(0.0, Q.log_sum_pt - 6.267538488641)
        - 43.86 * max(0.0, Q.log_sum_pt - 6.896095378249)
        - 3635.0 * max(0.0, 4.8108519e-05 - Q.girth2)
        + 30.54 * max(0.0, Q.log_sum_pt - 6.804164030582)
        + 4.579 * max(0.0, 0.15984864831 - Q.max_dr)
        - 9.559e-05 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, Q.max_pair_mass - 13.047927274731)
        - 4370.0 * max(0.0, 0.000172198326 - Q.width) * max(0.0, 0.222994708167 - Q.dr_7)
        + 1.696 * max(0.0, Q.mass_over_sum_pt - 0.06813910019)
        + 27.59 * max(0.0, Q.centroid_offset - 0.014379521101)
        + 65.12 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.518696343899 - Q.tau32)
        + 54.7 * max(0.0, Q.width - 0.018827653081)
        + 0.02519 * max(0.0, Q.mass - 36.229410171509)
        - 52.72 * max(0.0, Q.e2 - 0.028531698044)
        - 1.872 * max(0.0, Q.LHA - 0.312727471086)
        - 263.2 * max(0.0, 0.006679471358 - Q.width)
        - 0.4313 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.n_pt_above_50 - 3.0)
        - 14.45 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.001130644719 - Q.lam2)
        + 31.77 * max(0.0, 0.04447356835 - Q.e2)
        - 251.4 * max(0.0, 0.007330079875 - Q.lam1)
        - 2.837 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 5.0 - Q.n_dr_0_0p05)
        + 0.129 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 50.352200171245 - Q.mass_top3)
        - 0.1208 * max(0.0, Q.mass - 69.611351776123)
        + 10.91 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, 0.964120104909 - Q.z_dr_0p05_0p1)
        + 604.2 * max(0.0, 0.008678044751 - Q.girth2)
        - 8.472 * max(0.0, Q.LHA - 0.325582223496)
        - 0.01175 * max(0.0, Q.mass - 36.229410171509) * max(0.0, Q.eccentricity - 0.620723099573)
        + 151.8 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.0)
        - 23.74 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, Q.phi_7 - -0.041534423828)
        + 0.02023 * max(0.0, Q.mass_top5 - 53.607658247923)
        - 3.403 * max(0.0, -0.012844925793 - Q.mean_eta)
        + 65.15 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, -0.039672851562 - Q.eta_0)
        - 114.7 * max(0.0, Q.width - 0.018827653081) * max(0.0, 0.492494773865 - Q.pt_dispersion)
        + 0.09678 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.046481671275 - Q.dr_6)
        + 382.8 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.042151962757 - Q.dr_7)
        + 462.2 * max(0.0, Q.mass_over_sum_pt - 0.090413827016)
        - 246.1 * max(0.0, 0.004372139461 - Q.girth2)
        - 134.5 * max(0.0, Q.mass_over_sum_pt - 0.107985668755)
        + 473.4 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 0.145231109113 - Q.max_dr)
        + 3.821 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.planar_flow - 0.00804883781)
        + 95.47 * max(0.0, Q.lam1 - 0.012003726523)
        - 3444.0 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 0.145231109113 - Q.max_dr)
        - 1.047 * max(0.0, Q.mass - 69.611351776123) * max(0.0, 0.177304983139 - Q.max_dr)
        - 3.671 * max(0.0, Q.max_dr - 0.145231109113)
        + 96.13 * max(0.0, Q.max_dr - 0.145231109113) * max(0.0, 0.04586879935 - Q.dr_3)
        + 3934.0 * max(0.0, Q.lam1 - 0.016433749775) * max(0.0, Q.eccentricity - 0.959856212153)
        + 0.6437 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 68.125 - Q.pt_4)
        - 324.0 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 0.120257140434 - Q.z_4)
        + 0.2246 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 29.875 - Q.pt_5)
        - 319.7 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.959856212153)
        - 156.1 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.eccentricity - 0.959856212153)
        + 0.184 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 56.53125 - Q.pt_6)
        + 0.5602 * max(0.0, Q.lam1 - 0.012003726523) * max(0.0, 38.25 - Q.pt_6)
        + 0.568 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 48.71875 - Q.pt_7)
        + 1.441 * max(0.0, Q.LHA - 0.423592510895)
        + 0.0008013 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 20.125 - Q.pt_7)
        - 2.567 * max(0.0, 0.23799610585 - Q.tau21)
        - 0.001368 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 62.55 - Q.mass)
        + 1425.0 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.e2_sq - 0.011657374702)
        + 748.8 * max(0.0, 0.000306123359 - Q.lam2)
        + 526.9 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.001130644719 - Q.lam2)
        - 526.4 * max(0.0, Q.width - 0.000319370692)
        - 0.02678 * max(0.0, 763.825 - Q.sum_pt)
        - 805.2 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.067292226106 - Q.C2)
        - 1420.0 * max(0.0, 0.009530300104 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.016278845848)
        + 3.589 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.planar_flow - 0.045057236346)
        + 110.9 * max(0.0, Q.width - 0.001653836415)
        - 0.0002073 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        + 316.6 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 5.633 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.175465903809 - Q.dr_7)
        - 6.681 * max(0.0, Q.C2 - 0.067292226106)
        + 55.64 * max(0.0, 0.001130644719 - Q.lam2)
        - 13.37 * max(0.0, 0.005011406868 - Q.girth2_top3)
        - 57.27 * max(0.0, 0.001130644719 - Q.lam2) * max(0.0, Q.n_dr_0p1_0p2 - 2.0)
        + 81.12 * max(0.0, Q.girth - 0.101940929517)
        - 354.9 * max(0.0, 0.017162483186 - Q.e2_sq)
        + 300.6 * max(0.0, Q.girth2 - 0.013238675334)
        + 0.001959 * max(0.0, 430.75 - Q.sum_pt_top5)
        + 4.779 * max(0.0, Q.e2 - 0.063441075385)
        - 3.608 * max(0.0, Q.e2 - 0.007078157854)
        + 0.01147 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.104247858869 - Q.dr_3)
        - 46.22 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, -0.025945045147 - Q.mean_phi)
        + 0.06308 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_7 - 33.21875)
        + 45.22 * max(0.0, 0.014379521101 - Q.centroid_offset)
        + 9.346 * max(0.0, Q.max_dr - 0.102758520097)
        + 4.472 * max(0.0, Q.mass_over_sum_pt - 0.107985668755) * max(0.0, 3.885568320751 - Q.D2)
        - 7.72 * max(0.0, Q.max_dr - 0.197968879342)
        - 0.3751 * max(0.0, Q.max_dr - 0.102758520097) * max(0.0, Q.pt_7 - 37.15625)
        + 5.58 * max(0.0, Q.C2 - 0.014943876117)
        + 0.9491 * max(0.0, Q.C2 - 0.014943876117) * max(0.0, Q.pt_7 - 38.53125)
        - 3.019 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 50.352200171245 - Q.mass_top3)
        - 22.13 * max(0.0, 0.014379521101 - Q.centroid_offset) * max(0.0, 0.674770402908 - Q.z_dr_0p05_0p1)
        - 5.589 * max(0.0, 0.047915700823 - Q.girth)
        + 0.002985 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_2 - 73.6875)
        + 131.6 * max(0.0, 0.023780909279 - Q.e2_sq)
        + 143.6 * max(0.0, 0.001101860861 - Q.mass_over_sum_pt_sq)
        + 0.8425 * max(0.0, 0.216055863061 - Q.LHA)
        - 9.951 * max(0.0, 0.049399692737 - Q.z_7)
        - 0.03643 * max(0.0, 0.049399692737 - Q.z_7) * max(0.0, 62.55 - Q.mass_top5)
        + 9.362 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 3.929 * max(0.0, 0.00528466865 - Q.e2_sq)
        + 0.1262 * max(0.0, 0.028865759995 - Q.z_6)
        + 3.658 * max(0.0, 0.071488645583 - Q.z_7)
        + 18840.0 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, 0.014379521101 - Q.centroid_offset)
        - 4.474 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 0.06281 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 788.4484375 - Q.sum_pt)
        + 2447.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001503553356 - Q.lam1)
        + 0.8055 * max(0.0, 0.03243272066 - Q.z_7)
        - 4.742 * max(0.0, 0.026454043164 - Q.dr_0)
        - 15.72 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 2.723 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.n_dr_0p2_0p4 - 0.0)
        + 0.8327 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        + 431.5 * max(0.0, 0.002635417778 - Q.width)
        - 462.4 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt)
        - 31.89 * max(0.0, 0.002270363079 - Q.girth2_top5)
        - 2.019e-05 * max(0.0, Q.sum_pt_top5 - 752.1)
        - 4871.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.0004381 * max(0.0, 548.196875 - Q.sum_pt_top2)
        - 13960.0 * max(0.0, 0.002635417778 - Q.width) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 106.8 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.centroid_offset - 0.018377780003)
        + 0.03785 * max(0.0, 0.03243272066 - Q.z_7) * max(0.0, Q.pt_5 - 33.0265625)
        - 4.615e-05 * max(0.0, 24.578125 - Q.pt_5)
        + 0.0004685 * max(0.0, Q.sum_pt - 868.509375)
        + 0.05552 * max(0.0, Q.sum_pt - 868.509375) * max(0.0, 0.012587644117 - Q.centroid_offset)
        - 0.08038 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, Q.mass_top3 - 28.345095968085)
        + 91.72 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.018377780003 - Q.centroid_offset)
        - 1626.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.000145482056 - Q.mean_phi2)
        + 0.006953 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.021588001063 - Q.dr_0)
        - 30.59 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.021588001063 - Q.dr_0)
        + 15.94 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.04118638065 - Q.dr_0)
        + 53.19 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.004331280361 - Q.mean_phi2)
        + 84.32 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.012003726523 - Q.lam1)
        - 16.58 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006299534492 - Q.girth2_top2)
        - 0.09739 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 3494.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 9.0303693e-05 - Q.mean_eta2)
        + 0.06201 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, 18.097979966098 - Q.max_pair_mass)
        + 0.06989 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.mass_top3 - 3.559569591142)
        + 5.857 * max(0.0, 0.01426135283 - Q.mean_phi2)
        - 0.08921 * max(0.0, 0.01426135283 - Q.mean_phi2) * max(0.0, 40.046952646555 - Q.max_pair_mass)
        - 20.85 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 40040.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, 7.3007261e-05 - Q.lam2)
        + 8.799 * max(0.0, 0.021588001063 - Q.dr_0)
        - 4.407 * max(0.0, Q.centroid_offset - 0.008092360237)
        + 267.8 * max(0.0, 0.013238675006 - Q.width)
        - 73.95 * max(0.0, 0.154170806525 - Q.mass_over_sum_pt)
        - 1.788 * max(0.0, 6.327378592257 - Q.log_sum_pt)
        - 4279.0 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.003408388935 - Q.lam2)
        - 173.4 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, 0.071488645583 - Q.z_7)
        - 145.7 * max(0.0, 0.050284641981 - Q.e2)
        - 21.07 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, Q.planar_flow - 0.00804883781)
        + 47.05 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.094821243733 - Q.C2)
        - 13.03 * max(0.0, Q.centroid_offset - 0.018377780003)
        + 0.07279 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, Q.pt_6 - 27.578125)
        + 9.669 * max(0.0, 6.701242202626 - Q.log_sum_pt)
        - 89.71 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 0.049399692737 - Q.z_7)
        - 5.615 * max(0.0, Q.centroid_offset - 0.049903668404)
        - 6.804 * Q.max_dr
        - 4.073 * max(0.0, Q.C2 - 0.010539266048)
        - 889.4 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 0.008921136335 - Q.mean_phi2)
        - 31.88 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.872657364787)
        + 2.98 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 4.0 - Q.n_dr_0p05_0p1)
        + 124.5 * max(0.0, 0.000537286005 - Q.lam2)
        - 1359.0 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_phi - 0.026127964072)
        + 9.52 * max(0.0, Q.mass_over_sum_pt - 0.008374148675)
        - 121.4 * max(0.0, Q.girth2_top5 - 0.011482925368)
        + 14.46 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, Q.mean_phi - 0.009050007537)
        - 73.41 * max(0.0, Q.girth - 0.087236513197)
        + 12.13 * max(0.0, Q.mass_over_sum_pt - 0.008374148675) * max(0.0, 0.518696343899 - Q.tau32)
        - 0.07718 * max(0.0, 1.679198372364 - Q.D2)
        - 0.1196 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, Q.pt_2 - 56.5)
        - 164.5 * max(0.0, 0.007330079875 - Q.lam1) * max(0.0, 1.232133567333 - Q.D2)
        - 62.22 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.15855820179)
        + 272.2 * max(0.0, Q.lam2 - 0.003408388935)
        + 3.311 * max(0.0, 6.572937922293 - Q.log_sum_pt)
        - 0.05502 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 36.8125 - Q.pt_6)
        - 18.0 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 24.578125 - Q.pt_5)
        - 2939.0 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_eta - 0.02644207105)
        + 39710.0 * max(0.0, 0.000537286005 - Q.lam2) * max(0.0, Q.mean_eta - 0.02644207105)
        - 4.613 * max(0.0, 0.003562611155 - Q.girth2)
        + 0.01347 * max(0.0, 49.668099212646 - Q.mass)
        + 67.27 * max(0.0, Q.girth2_top5 - 0.002270363079)
        + 0.002141 * max(0.0, 1.679198372364 - Q.D2) * max(0.0, 90.625 - Q.pt_4)
        - 3.718 * max(0.0, Q.z_7 - 0.06164517166)
        - 0.1049 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 45.75 - Q.pt_7)
        - 1.411 * max(0.0, Q.C2 - 0.010539266048) * max(0.0, Q.pt_7 - 31.859375)
        - 0.02266 * max(0.0, 49.668099212646 - Q.mass) * max(0.0, 0.750909513235 - Q.z_dr_0p05_0p1)
        - 2.855 * max(0.0, 0.195013533663 - Q.planar_flow)
        - 2381.0 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.width - 0.00752008842)
        - 316.2 * max(0.0, 0.001056655216 - Q.girth2_top2)
        - 300.4 * max(0.0, Q.girth2 - 0.007520088344)
        - 168.3 * max(0.0, Q.girth2 - 0.004372139461)
        + 44.4 * max(0.0, Q.mass_over_sum_pt - 0.072690732432)
        + 21950.0 * max(0.0, 0.001056655216 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 110.9 * max(0.0, Q.girth2 - 0.0016538364)
        + 153.8 * max(0.0, 0.024547699839 - Q.e2)
        - 0.07851 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, 35.28125 - Q.pt_6)
        - 13.61 * max(0.0, 0.04081947431 - Q.girth)
        + 0.06501 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.mass_top3 - 23.663861485439)
        - 0.01059 * max(0.0, 48.71875 - Q.pt_7)
        + 0.01023 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.sum_pt - 615.875)
        - 54.24 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        - 684.3 * max(0.0, 0.005590288644 - Q.width)
        + 7.659 * max(0.0, 0.02076709205 - Q.centroid_offset)
        + 677.0 * max(0.0, Q.girth2 - 0.008678044751)
        - 447.7 * max(0.0, Q.mass_over_sum_pt - 0.084751611895)
        + 6.657 * max(0.0, 0.001101266364 - Q.e2_sq)
        - 0.05116 * max(0.0, Q.mass - 80.4)
        + 7181.0 * max(0.0, Q.girth2 - 0.004372139461) * max(0.0, Q.eccentricity - 0.945820652852)
        - 417.3 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, 1.122624260187 - Q.D2)
        + 108.4 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 1.122624260187 - Q.D2)
        + 93.48 * max(0.0, 0.038466955721 - Q.e2)
        + 465.0 * max(0.0, 0.02076709205 - Q.centroid_offset) * max(0.0, Q.C2 - 0.023843882605)
        - 0.4267 * max(0.0, Q.mass - 80.4) * max(0.0, Q.eccentricity - 0.927072033478)
        - 0.00655 * max(0.0, 48.71875 - Q.pt_7) * max(0.0, 0.694781820497 - Q.planar_flow)
        - 6.424 * max(0.0, Q.centroid_offset - 0.031170772021)
        + 18.65 * max(0.0, 0.293190627853 - Q.LHA)
        + 83.0 * max(0.0, 0.005884990035 - Q.girth2_top3)
        - 43.03 * max(0.0, 0.000561123155 - Q.width)
        - 1.462 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_0 - 376.5)
        - 3660.0 * max(0.0, 0.001101266364 - Q.e2_sq) * max(0.0, -0.009460449219 - Q.phi_1)
        - 0.6449 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_2 - 56.5)
        + 0.9849 * max(0.0, 0.197968879342 - Q.max_dr)
        - 406.2 * max(0.0, 0.005019718802 - Q.width)
        - 71.67 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.501026660204 - Q.tau21)
        - 4550.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 5.738 * max(0.0, 0.196739721581 - Q.LHA)
        - 0.01071 * max(0.0, Q.log_sum_pt - 6.701242202626)
        + 87.97 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.40079469091 - Q.planar_flow)
        - 0.4099 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 248.125 - Q.sum_pt_top2)
        + 12.2 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.n_dr_0p05_0p1 - 0.0)
        + 2.31 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.mean_phi - -0.000855675264)
        - 46.46 * max(0.0, 0.061086014472 - Q.girth)
        + 0.001837 * max(0.0, Q.sum_pt_top5 - 658.125)
        - 13.43 * max(0.0, 0.003343241496 - Q.centroid_offset)
        - 8.941 * max(0.0, 0.177304983139 - Q.max_dr)
        + 585.4 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 0.1009733513 - Q.z_dr_0p2_0p4)
        - 342.8 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 3.958 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        + 11800.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 10230.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.lam1 - 0.00027588256)
        + 5288.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.mass_over_sum_pt_sq - 0.00012320649)
        - 6393.0 * max(0.0, 0.177304983139 - Q.max_dr) * max(0.0, 0.000194798295 - Q.lam2)
        - 11.49 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.000306123359 - Q.lam2)
        - 0.0873 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 48.71875 - Q.pt_7)
        - 220.4 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.018827652745 - Q.girth2)
        - 3237.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.00023679558 - Q.mass_over_sum_pt_sq)
        - 11.5 * max(0.0, 0.016554418951 - Q.e2)
        - 10.47 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.8803 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        - 7284.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000561123155 - Q.width)
        + 7.389 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_6 - 0.02160287394)
        + 2.061 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 0.08684 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, Q.sum_pt - 788.4484375)
        + 20310.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.005019718802 - Q.width)
        + 6367.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.000194798295 - Q.lam2)
        - 43.25 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 1766.0 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 25510.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.centroid_offset - 0.018377780003)
        + 4199.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000306123359 - Q.lam2)
        + 0.02222 * max(0.0, 8.379955863953 - Q.mass)
        - 0.878 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.058613700176 - Q.z_7)
        - 58.48 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_7 - 0.016858545121)
        - 0.5105 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, Q.centroid_offset - 0.016278845848)
        + 456.9 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971) * max(0.0, 0.000537286005 - Q.lam2)
        - 843.8 * max(0.0, 0.000964142894 - Q.girth2)
        - 192.1 * max(0.0, 0.000222950415 - Q.girth2_top5)
        + 6.905 * max(0.0, 0.054649224505 - Q.girth)
        + 90.57 * max(0.0, Q.lam2 - 0.001130644719)
        + 0.4904 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        - 197.8 * max(0.0, 0.006096650059 - Q.width)
        + 19.87 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.000872228216 - Q.lam1)
        + 54.69 * max(0.0, Q.girth2 - 0.018827652745)
        - 52.13 * max(0.0, 0.032346998155 - Q.e2)
        + 62.06 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.40079469091 - Q.planar_flow)
        + 81.06 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.055953954317 - Q.dr01)
        - 0.2392 * max(0.0, Q.n_dr_0p2_0p4 - 1.0)
        - 0.03129 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 6.842716632804 - Q.log_sum_pt)
        + 2.326 * max(0.0, 0.221586732566 - Q.max_dr)
        + 504.8 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.C2 - 0.030867108516)
        + 8.397 * max(0.0, Q.C2 - 0.051192347892)
        - 4.085 * max(0.0, 0.018377780003 - Q.centroid_offset)
        - 898.7 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.centroid_offset - 0.003343241496)
        + 467.3 * max(0.0, 0.000172198326 - Q.width)
        + 19.5 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_5 - 0.036727111752)
        - 379.5 * max(0.0, 0.007520088344 - Q.girth2)
        - 0.02309 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.002127561159 - Q.mean_phi2)
        - 0.06996 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 0.2709 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.pt_4 - 47.34375)
        - 189.9 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_4 - 0.047491459878)
        - 195.1 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, Q.eccentricity - 0.903125533696)
        - 10.99 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.620723099573 - Q.eccentricity)
        - 0.01472 * max(0.0, 41.377904891968 - Q.mass)
        + 0.09501 * max(0.0, 41.377904891968 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 48.05 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        - 23.02 * max(0.0, 0.076373631775 - Q.mass_over_sum_pt)
        - 89.6 * max(0.0, 0.001503553356 - Q.lam1)
        - 0.4832 * max(0.0, Q.max_dr - 0.15984864831)
        - 6.464 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 29.0421875 - Q.pt_7)
        - 0.2162 * max(0.0, Q.lam2 - 0.001130644719) * max(0.0, Q.mass_top2 - 16.308019673264)
        - 0.001472 * max(0.0, 35.5 - Q.pt_5)
        - 1.613 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, 53.4375 - Q.pt_7)
        + 90.77 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.02644207105 - Q.mean_eta)
        + 0.0001412 * max(0.0, 35.5 - Q.pt_5) * max(0.0, Q.min_pair_mass - 0.173071536962)
        - 1.759 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, Q.n_dr_0p05_0p1 - 1.0)
        + 65.89 * Q.e2
        + 235.0 * max(0.0, Q.lam2 - 0.000194798295)
        + 8.927 * max(0.0, Q.LHA - 0.303313749495)
        - 450.4 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, Q.planar_flow - 0.012569162668)
        + 2.33 * max(0.0, 6.267538488641 - Q.log_sum_pt)
        - 0.009365 * max(0.0, Q.centroid_offset - 0.00231612516) * max(0.0, 34.53125 - Q.pt_7)
        + 9.552 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 8.0 - Q.n_pt_above_50)
        + 0.2163 * max(0.0, Q.n_dr_0p2_0p4 - 2.0)
        - 31.42 * max(0.0, 0.004183811014 - Q.lam1)
        + 445.0 * max(0.0, 0.090413827016 - Q.mass_over_sum_pt)
        - 0.01817 * max(0.0, 3.0 - Q.n_dr_0p05_0p1)
        + 180.1 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 0.501026660204 - Q.tau21)
        - 0.5754 * max(0.0, 0.269169217348 - Q.tau32)
        - 13.93 * max(0.0, Q.LHA - 0.303313749495) * max(0.0, 0.553068161011 - Q.tau21)
        + 0.3009 * max(0.0, 0.391541349888 - Q.tau21)
        + 6.848 * max(0.0, Q.eccentricity - 0.903125533696) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 0.1083 * max(0.0, 0.269169217348 - Q.tau32) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 12.59 * max(0.0, 0.002412890926 - Q.girth2_top2)
        + 0.006629 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.pt_4 - 39.8125)
        - 7.704 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.222994708167 - Q.dr_7)
        - 62.64 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 2.055451202393 - Q.D2)
        + 245.8 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, 0.175465903809 - Q.dr_7)
        - 8.234 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.z_4 - 0.075444822386)
        - 1.088 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.sum_pt - 988.4078125)
        + 182.6 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.log_sum_pt - 6.701242202626)
        + 0.117 * max(0.0, Q.mass - 15.454033088684)
        - 0.3404 * max(0.0, Q.max_dr - 0.121680960059)
        - 0.003143 * max(0.0, Q.mass - 15.454033088684) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 81.06 * max(0.0, 0.0016538364 - Q.girth2)
        - 0.006365 * max(0.0, Q.sum_pt - 813.415625)
        - 263.2 * max(0.0, 0.006679471442 - Q.girth2)
        + 0.05738 * max(0.0, 0.253403707141 - Q.planar_flow)
        + 216.4 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.width - 0.006096650059)
        + 2.295 * max(0.0, 0.154689112391 - Q.LHA)
        - 28.06 * max(0.0, Q.girth - 0.076081777364)
        + 0.003448 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, 69.611351776123 - Q.mass)
        + 7.543 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.max_dr - 0.102758520097)
        - 8.166 * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 0.4506 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 48.71875 - Q.pt_7)
        + 0.1522 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, Q.n_dr_0p05_0p1 - 2.0)
        + 211.6 * max(0.0, 0.006390124748 - Q.e2_sq)
        + 14.67 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 0.04252 * max(0.0, 7.0 - Q.n_dr_0_0p05)
        + 124.0 * max(0.0, 0.006390124748 - Q.e2_sq) * max(0.0, 1.332146394253 - Q.D2)
        - 0.08074 * Q.centroid_offset
        - 4.608 * max(0.0, 0.003562611091 - Q.width)
        + 0.001945 * max(0.0, 9.257203159811 - Q.mass_top5)
        - 46.63 * max(0.0, 0.154689112391 - Q.LHA) * max(0.0, 0.028070914944 - Q.z_7)
        - 0.08449 * max(0.0, 15.454033088684 - Q.mass)
        - 1.604 * max(0.0, Q.girth - 0.076081777364) * max(0.0, 7.0 - Q.n_pt_above_50)
        - 0.02133 * max(0.0, 29.0421875 - Q.pt_7)
        + 71.65 * max(0.0, 0.004839980301 - Q.lam1)
        + 8.928 * max(0.0, 0.035786485299 - Q.C2)
        - 7.533 * max(0.0, 0.111761856824 - Q.max_dr)
        - 0.1765 * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 0.0003459 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 22.844978847276 - Q.mass_top2)
        - 0.01028 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.pt_5 - 43.0625)
        - 0.00803 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 0.05311 * max(0.0, Q.mass - 91.19)
        - 3604.0 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.lam2 - 0.000537286005)
        + 0.7954 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.pt_7 - 15.55390625)
        - 6.983 * max(0.0, Q.mean_phi - 0.026127964072)
        + 51.77 * max(0.0, 0.148408418149 - Q.girth)
        - 14.54 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 0.04242 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 38.53125 - Q.pt_7)
        + 44.05 * max(0.0, 0.016433749775 - Q.lam1)
        - 0.1379 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, Q.z_7 - 0.023207568189)
        - 46310.0 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 7.356e-05 * max(0.0, 531.1875 - Q.sum_pt_top5)
        + 4.586e-05 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, 43.5 - Q.pt_7)
        + 0.002114 * max(0.0, Q.sum_pt_top5 - 902.40625)
        + 0.0005694 * max(0.0, Q.sum_pt_top5 - 839.9546875)
        + 0.08724 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 56.53125 - Q.pt_6)
        + 10.27 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.pt_dispersion - 0.396830244362)
        + 0.7229 * max(0.0, 0.501026660204 - Q.tau21)
        - 3365.0 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 0.037760993714 - Q.centroid_offset)
        + 0.761 * max(0.0, 0.067272114405 - Q.z_6)
        - 3.631 * max(0.0, 0.037760993714 - Q.centroid_offset)
        + 1.768 * max(0.0, Q.LHA - 0.09323897448)
        - 0.0002176 * max(0.0, Q.sum_pt_top5 - 902.40625) * max(0.0, 3.885568320751 - Q.D2)
        - 0.002327 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.15855820179 - Q.z_dr_0p1_0p2)
        - 3.388 * max(0.0, 0.501026660204 - Q.tau21) * max(0.0, Q.max_dr - 0.015595615841)
        - 379.5 * max(0.0, 0.00752008842 - Q.width)
        + 0.5174 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 0.037477688199 - Q.z_4)
        - 0.002825 * max(0.0, 25.578125 - Q.pt_7)
        + 0.03529 * max(0.0, Q.sum_pt - 988.4078125)
        + 0.0001397 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 0.0003976 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, 3.885568320751 - Q.D2)
        + 0.2152 * max(0.0, 0.111513564951 - Q.planar_flow)
        + 0.1441 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        - 341.7 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 147.2 * max(0.0, Q.lam1 - 0.008375572068)
        - 14.59 * max(0.0, Q.lam1 - 0.004183811014)
        - 53.21 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 0.15984864831 - Q.max_dr)
        + 28.55 * max(0.0, Q.lam1 - 0.00543336053)
        - 0.01339 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 739.5 - Q.sum_pt)
        - 243.2 * max(0.0, Q.lam1 - 0.007330079875)
        - 11.59 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 0.067292226106 - Q.C2)
        + 33670.0 * max(0.0, Q.lam1 - 0.007330079875) * max(0.0, 0.13261153996 - Q.max_dr)
        - 3.853 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235)
        + 1717.0 * max(0.0, Q.lam1 - 0.00543336053) * max(0.0, 0.15984864831 - Q.max_dr)
        + 413.6 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.009480684835)
        - 0.05098 * max(0.0, 76.655700683594 - Q.mass)
        - 2.927 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, Q.eccentricity - 0.970449631164)
        + 5.237 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        + 62.77 * max(0.0, Q.lam1 - 0.005954149834)
        + 0.2187 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 47.55 * max(0.0, Q.lam1 - 0.002464291268)
        + 188.1 * max(0.0, 0.011660904657 - Q.mass_over_sum_pt_sq)
        - 0.02198 * max(0.0, 76.655700683594 - Q.mass) * max(0.0, 0.74595130682 - Q.D2)
        - 765.8 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.111513564951 - Q.planar_flow)
        + 1820.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.eccentricity - 0.970449631164)
        + 939.2 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        - 1.146 * max(0.0, 1.122624260187 - Q.D2)
        - 38.11 * max(0.0, 0.038466955721 - Q.e2) * max(0.0, 1.002470755577 - Q.D2)
        - 0.002777 * max(0.0, 5.0 - Q.n_dr_0p05_0p1)
        + 16.62 * max(0.0, 1.122624260187 - Q.D2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 14.26 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, Q.eccentricity - 0.984196588116)
        + 0.7736 * max(0.0, 0.74595130682 - Q.D2)
        + 167.5 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 1210.0 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        + 264.1 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 1.002470755577 - Q.D2)
        + 99.71 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 131.7 * max(0.0, 0.004372139461 - Q.girth2) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 9.29 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 1.219 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 19.95 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.121680960059 - Q.max_dr)
        - 3.861 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 54570.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, Q.e2 - 0.024547699839)
        + 108.8 * max(0.0, 0.012003726523 - Q.lam1)
        + 331.4 * max(0.0, 0.011657374702 - Q.e2_sq)
        + 6054.0 * max(0.0, 0.007182835724 - Q.mass_over_sum_pt_sq)
        - 0.001787 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.sum_pt_top3 - 353.0625)
        + 10.71 * max(0.0, 0.041109715588 - Q.e2)
        - 54.11 * max(0.0, 0.063441075385 - Q.e2)
        + 1.514 * max(0.0, 0.328461505473 - Q.z_dr_0p1_0p2)
        - 0.5416 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 0.03858 * max(0.0, 2.0 - Q.n_dr_0_0p05)
        + 0.05883 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.m01 - 16.308019673264)
        + 1.2 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, Q.pt1_dr01 - 1.21960336377)
        - 0.05806 * max(0.0, Q.mass - 80.4) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 3.543 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.z_top5 - 0.865048766136)
        + 1774.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.log_sum_pt - 6.896095378249)
        + 0.321 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.mass_top2 - 22.844978847276)
        - 421.2 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.061262048692 - Q.planar_flow)
        - 16.65 * max(0.0, 0.06813910019 - Q.mass_over_sum_pt)
        - 0.04721 * max(0.0, Q.n_dr_0p05_0p1 - 5.0)
        + 24.26 * max(0.0, Q.LHA - 0.346713497427)
        - 9.139 * max(0.0, Q.girth - 0.033604209498)
        - 39.43 * max(0.0, 0.002151567843 - Q.girth2_top3)
        + 10.0 * max(0.0, 0.007639643088 - Q.girth2_top2)
    )


def score_t(Q):
    return (-0.4157
        - 0.9688 * max(0.0, 0.148419710734 - Q.planar_flow)
        + 45.16 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 24.19 * max(0.0, 0.004372139331 - Q.width)
        - 55.78 * max(0.0, 0.018827652745 - Q.girth2)
        + 0.01063 * max(0.0, 64.618731689453 - Q.mass)
        - 0.003357 * max(0.0, 21.784077072144 - Q.mass)
        - 1.148 * max(0.0, 0.007929074034 - Q.girth2_top3)
        - 33.13 * max(0.0, 0.013238675334 - Q.girth2)
        - 168.9 * max(0.0, 0.006506575659 - Q.lam1)
        - 158.1 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, 0.87567204833 - Q.D2)
        + 0.13 * max(0.0, Q.sum_pt - 901.59375)
        + 0.01919 * max(0.0, 56.920347213745 - Q.mass)
        - 28.91 * max(0.0, 0.008678044951 - Q.width)
        + 5.669e-05 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 25.578125 - Q.pt_7)
        - 0.002373 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 380.5875 - Q.sum_pt_top2)
        + 0.06341 * max(0.0, Q.sum_pt - 901.59375) * max(0.0, 0.038438041256 - Q.dr_2)
        - 0.1553 * max(0.0, 56.920347213745 - Q.mass) * max(0.0, Q.C2 - 0.023843882605)
        - 6.68 * max(0.0, 0.00832969537 - Q.girth2_top5)
        + 0.2664 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971)
        - 0.008277 * max(0.0, 29.644699859619 - Q.mass)
        - 0.02798 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.87567204833 - Q.D2)
        - 5.37 * max(0.0, 0.148419710734 - Q.planar_flow) * max(0.0, 0.111761856824 - Q.max_dr)
        + 21.43 * max(0.0, 0.087236513197 - Q.girth)
        - 4.926 * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 1154.0 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.centroid_offset - 0.014379521101)
        - 0.1554 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, Q.centroid_offset - 0.012587644117)
        + 7.592 * max(0.0, 0.020459658932 - Q.e2)
        + 654.4 * max(0.0, 0.008174660116 - Q.mass_over_sum_pt_sq)
        + 6.116 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.eccentricity - 0.959856212153)
        - 7.251 * max(0.0, Q.log_sum_pt - 6.638338705138)
        + 0.003541 * max(0.0, Q.sum_pt_top5 - 687.4375)
        - 0.2533 * max(0.0, 0.007929074034 - Q.girth2_top3) * max(0.0, 35.28125 - Q.pt_6)
        - 22.72 * max(0.0, 0.00543336053 - Q.lam1)
        - 0.06785 * max(0.0, Q.log_sum_pt - 6.377722943814)
        - 0.1416 * max(0.0, Q.sum_pt_top5 - 687.4375) * max(0.0, Q.z_7 - 0.023207568189)
        - 6.487 * max(0.0, 0.003952581551 - Q.girth2_top3)
        + 26.83 * max(0.0, 0.076081777364 - Q.girth)
        + 8.168e-05 * max(0.0, 64.618731689453 - Q.mass) * max(0.0, 40.040625 - Q.pt_7)
        - 2.065 * max(0.0, Q.log_sum_pt - 6.638338705138) * max(0.0, 0.093979107928 - Q.dr_7)
        - 0.0286 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, Q.phi_1 - -0.058901977539)
        + 11.6 * max(0.0, 0.004372139331 - Q.width) * max(0.0, Q.n_dr_0p1_0p2 - 1.0)
        - 37.86 * max(0.0, 0.13092863437 - Q.mass_over_sum_pt)
        + 1.913 * max(0.0, 0.012569162668 - Q.planar_flow)
        - 47.07 * max(0.0, 0.008375572068 - Q.lam1)
        - 0.005078 * max(0.0, Q.pt_7 - 34.53125)
        + 156.9 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.centroid_offset - 0.02076709205)
        - 0.0001223 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 91.19 - Q.mass)
        - 2.76 * max(0.0, 0.035560912266 - Q.e2)
        - 0.7932 * max(0.0, 0.055577157257 - Q.z_7)
        + 0.09042 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, Q.centroid_offset - 0.014379521101)
        + 32.68 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 0.02001 * max(0.0, 53.332374954224 - Q.mass)
        + 0.0002381 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 45.595 - Q.mass_top3)
        + 0.2312 * max(0.0, Q.log_sum_pt - 6.377722943814) * max(0.0, 0.197968879342 - Q.max_dr)
        - 0.02674 * max(0.0, Q.log_sum_pt - 6.572937922293)
        - 0.007721 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 0.553068161011 - Q.tau21)
        - 198.8 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 328.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, Q.eccentricity - 0.978160776925)
        - 1.015 * max(0.0, 0.083662731125 - Q.planar_flow)
        + 27.45 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.042322802544 - Q.C2)
        + 0.5104 * max(0.0, 0.197783735394 - Q.tau21)
        + 148.6 * max(0.0, 0.008168570676 - Q.e2_sq)
        - 0.1982 * max(0.0, Q.pt_7 - 34.53125) * max(0.0, 0.080507021025 - Q.max_dr)
        - 0.0002778 * max(0.0, Q.pt_7 - 53.4375) * max(0.0, 32.617988451746 - Q.mass_top3)
        - 0.4647 * max(0.0, 0.042322802544 - Q.C2)
        + 0.002689 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 50.25 - Q.pt_6)
        - 36.37 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006756161242 - Q.girth2_top3)
        - 388.4 * max(0.0, 0.055577157257 - Q.z_7) * max(0.0, 0.007929074034 - Q.girth2_top3)
        + 1428.0 * max(0.0, 0.197783735394 - Q.tau21) * max(0.0, 0.000194798295 - Q.lam2)
        + 141.7 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.001130644719 - Q.lam2)
        + 17.75 * max(0.0, 0.083662731125 - Q.planar_flow) * max(0.0, 0.269169217348 - Q.tau32)
        + 7.336 * max(0.0, 0.346713497427 - Q.LHA)
        + 8.184 * max(0.0, Q.e2 - 0.032346998155)
        - 6.032 * max(0.0, Q.mass_over_sum_pt - 0.054892207095)
        + 11.65 * max(0.0, 0.346713497427 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 5.022 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 746.5 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, 0.083662731125 - Q.planar_flow)
        + 16.72 * max(0.0, 0.008168570676 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 7.164 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.033200121667 - Q.planar_flow)
        + 0.5018 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.n_pt_above_50 - 7.0)
        + 1.609 * max(0.0, 0.046566883102 - Q.max_dr)
        + 0.9243 * max(0.0, Q.e2 - 0.032346998155) * max(0.0, 0.641386964917 - Q.tau32)
        + 0.1513 * max(0.0, 69.611351776123 - Q.mass)
        + 0.04513 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.068101508468 - Q.z_7)
        - 6.159 * max(0.0, Q.log_sum_pt - 6.842716632804)
        + 0.0554 * max(0.0, 6.464150123592 - Q.log_sum_pt)
        + 33.42 * max(0.0, 0.028070914944 - Q.z_7)
        - 37.52 * max(0.0, 0.005954149834 - Q.lam1)
        + 4046.0 * max(0.0, 9.1213921e-05 - Q.width)
        + 0.02234 * max(0.0, Q.pt_7 - 30.484375)
        - 0.2179 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, 0.051192347892 - Q.C2)
        + 0.5746 * max(0.0, Q.z_7 - 0.046240320761)
        - 1093.0 * max(0.0, 0.028070914944 - Q.z_7) * max(0.0, 0.00752008842 - Q.width)
        + 0.7235 * max(0.0, Q.LHA - 0.111565049159)
        - 613.1 * max(0.0, 0.005954149834 - Q.lam1) * max(0.0, Q.max_dr - 0.080507021025)
        - 0.04007 * max(0.0, 0.694781820497 - Q.planar_flow)
        - 0.005882 * max(0.0, 36.229410171509 - Q.mass)
        - 5.402e-06 * max(0.0, 56.53125 - Q.pt_6) * max(0.0, Q.m012 - 32.617988451746)
        - 6.506 * max(0.0, 36.229410171509 - Q.mass) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.03771 * max(0.0, Q.pt_7 - 30.484375) * max(0.0, Q.max_dr - 0.093110798299)
        - 13.66 * max(0.0, 0.003377388461 - Q.lam1)
        - 6065.0 * max(0.0, 0.003377388461 - Q.lam1) * max(0.0, 0.006789738266 - Q.centroid_offset)
        - 11.97 * max(0.0, 8.379955863953 - Q.mass) * max(0.0, 0.010960638421 - Q.centroid_offset)
        - 3.235 * max(0.0, 0.016858545121 - Q.z_7)
        - 0.0008824 * max(0.0, 687.4375 - Q.sum_pt_top5)
        + 0.004463 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.04881348081 - Q.dr_7)
        + 0.002354 * max(0.0, 53.4375 - Q.pt_7)
        - 0.000812 * max(0.0, 43.5 - Q.pt_7)
        - 0.000749 * max(0.0, 788.4484375 - Q.sum_pt)
        - 1.097 * max(0.0, Q.log_sum_pt - 6.267538488641)
        + 163.4 * max(0.0, Q.log_sum_pt - 6.896095378249)
        + 1251.0 * max(0.0, 4.8108519e-05 - Q.girth2)
        - 118.8 * max(0.0, Q.log_sum_pt - 6.804164030582)
        - 0.3317 * max(0.0, 0.15984864831 - Q.max_dr)
        + 3.163e-05 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, Q.max_pair_mass - 13.047927274731)
        + 4122.0 * max(0.0, 0.000172198326 - Q.width) * max(0.0, 0.222994708167 - Q.dr_7)
        - 12.36 * max(0.0, Q.mass_over_sum_pt - 0.06813910019)
        + 10.21 * max(0.0, Q.centroid_offset - 0.014379521101)
        - 2.598 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.518696343899 - Q.tau32)
        - 0.1727 * max(0.0, Q.width - 0.018827653081)
        + 0.01561 * max(0.0, Q.mass - 36.229410171509)
        + 3.628 * max(0.0, Q.e2 - 0.028531698044)
        + 0.1491 * max(0.0, Q.LHA - 0.312727471086)
        + 38.7 * max(0.0, 0.006679471358 - Q.width)
        + 0.3824 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.n_pt_above_50 - 3.0)
        + 2.336 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.001130644719 - Q.lam2)
        + 1.565 * max(0.0, 0.04447356835 - Q.e2)
        - 42.62 * max(0.0, 0.007330079875 - Q.lam1)
        + 0.643 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 5.0 - Q.n_dr_0_0p05)
        - 0.02108 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 50.352200171245 - Q.mass_top3)
        - 0.1603 * max(0.0, Q.mass - 69.611351776123)
        + 1.147 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, 0.964120104909 - Q.z_dr_0p05_0p1)
        - 28.9 * max(0.0, 0.008678044751 - Q.girth2)
        - 0.085 * max(0.0, Q.LHA - 0.325582223496)
        - 0.01567 * max(0.0, Q.mass - 36.229410171509) * max(0.0, Q.eccentricity - 0.620723099573)
        + 30.99 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.0)
        + 2.371 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, Q.phi_7 - -0.041534423828)
        - 0.004875 * max(0.0, Q.mass_top5 - 53.607658247923)
        - 0.422 * max(0.0, -0.012844925793 - Q.mean_eta)
        - 3.445 * max(0.0, Q.centroid_offset - 0.014379521101) * max(0.0, -0.039672851562 - Q.eta_0)
        + 181.8 * max(0.0, Q.width - 0.018827653081) * max(0.0, 0.492494773865 - Q.pt_dispersion)
        - 0.04209 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 0.046481671275 - Q.dr_6)
        - 37.73 * max(0.0, Q.mass_over_sum_pt - 0.06813910019) * max(0.0, 0.042151962757 - Q.dr_7)
        - 95.31 * max(0.0, Q.mass_over_sum_pt - 0.090413827016)
        - 24.19 * max(0.0, 0.004372139461 - Q.girth2)
        + 117.8 * max(0.0, Q.mass_over_sum_pt - 0.107985668755)
        - 44.67 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 0.145231109113 - Q.max_dr)
        - 1.311 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.planar_flow - 0.00804883781)
        + 28.06 * max(0.0, Q.lam1 - 0.012003726523)
        + 1144.0 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 0.145231109113 - Q.max_dr)
        + 0.09129 * max(0.0, Q.mass - 69.611351776123) * max(0.0, 0.177304983139 - Q.max_dr)
        + 0.632 * max(0.0, Q.max_dr - 0.145231109113)
        - 5.994 * max(0.0, Q.max_dr - 0.145231109113) * max(0.0, 0.04586879935 - Q.dr_3)
        + 138.7 * max(0.0, Q.lam1 - 0.016433749775) * max(0.0, Q.eccentricity - 0.959856212153)
        - 0.02573 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 68.125 - Q.pt_4)
        + 19.06 * max(0.0, -0.012844925793 - Q.mean_eta) * max(0.0, 0.120257140434 - Q.z_4)
        + 0.1477 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, 29.875 - Q.pt_5)
        + 59.37 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.959856212153)
        - 77.0 * max(0.0, Q.e2 - 0.028531698044) * max(0.0, Q.eccentricity - 0.959856212153)
        - 0.04598 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 56.53125 - Q.pt_6)
        + 1.192 * max(0.0, Q.lam1 - 0.012003726523) * max(0.0, 38.25 - Q.pt_6)
        + 0.009186 * max(0.0, Q.mass_over_sum_pt - 0.090413827016) * max(0.0, 48.71875 - Q.pt_7)
        + 19.04 * max(0.0, Q.LHA - 0.423592510895)
        - 0.0004851 * max(0.0, Q.mass - 36.229410171509) * max(0.0, 20.125 - Q.pt_7)
        + 3.593 * max(0.0, 0.23799610585 - Q.tau21)
        - 0.09633 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 62.55 - Q.mass)
        - 319.8 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.e2_sq - 0.011657374702)
        - 1470.0 * max(0.0, 0.000306123359 - Q.lam2)
        - 2419.0 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.001130644719 - Q.lam2)
        - 189.7 * max(0.0, Q.width - 0.000319370692)
        + 0.01151 * max(0.0, 763.825 - Q.sum_pt)
        + 5.29 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.067292226106 - Q.C2)
        + 2333.0 * max(0.0, 0.009530300104 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.016278845848)
        + 3.195 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.planar_flow - 0.045057236346)
        - 138.1 * max(0.0, Q.width - 0.001653836415)
        - 0.0001286 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 136.4 * max(0.0, Q.width - 0.000319370692) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 2.965 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.175465903809 - Q.dr_7)
        + 22.78 * max(0.0, Q.C2 - 0.067292226106)
        + 91.7 * max(0.0, 0.001130644719 - Q.lam2)
        + 58.85 * max(0.0, 0.005011406868 - Q.girth2_top3)
        - 31.72 * max(0.0, 0.001130644719 - Q.lam2) * max(0.0, Q.n_dr_0p1_0p2 - 2.0)
        - 7.665 * max(0.0, Q.girth - 0.101940929517)
        + 230.6 * max(0.0, 0.017162483186 - Q.e2_sq)
        + 22.97 * max(0.0, Q.girth2 - 0.013238675334)
        + 0.0009221 * max(0.0, 430.75 - Q.sum_pt_top5)
        + 23.11 * max(0.0, Q.e2 - 0.063441075385)
        + 0.7279 * max(0.0, Q.e2 - 0.007078157854)
        + 0.01332 * max(0.0, 69.611351776123 - Q.mass) * max(0.0, 0.104247858869 - Q.dr_3)
        - 57.91 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, -0.025945045147 - Q.mean_phi)
        + 0.06818 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_7 - 33.21875)
        - 2.982 * max(0.0, 0.014379521101 - Q.centroid_offset)
        + 0.4094 * max(0.0, Q.max_dr - 0.102758520097)
        + 5.593 * max(0.0, Q.mass_over_sum_pt - 0.107985668755) * max(0.0, 3.885568320751 - Q.D2)
        - 0.7114 * max(0.0, Q.max_dr - 0.197968879342)
        - 0.2831 * max(0.0, Q.max_dr - 0.102758520097) * max(0.0, Q.pt_7 - 37.15625)
        - 2.223 * max(0.0, Q.C2 - 0.014943876117)
        + 0.875 * max(0.0, Q.C2 - 0.014943876117) * max(0.0, Q.pt_7 - 38.53125)
        - 10.69 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 50.352200171245 - Q.mass_top3)
        - 20.89 * max(0.0, 0.014379521101 - Q.centroid_offset) * max(0.0, 0.674770402908 - Q.z_dr_0p05_0p1)
        + 12.12 * max(0.0, 0.047915700823 - Q.girth)
        + 0.003569 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, Q.pt_2 - 73.6875)
        - 107.0 * max(0.0, 0.023780909279 - Q.e2_sq)
        + 48.45 * max(0.0, 0.001101860861 - Q.mass_over_sum_pt_sq)
        - 10.77 * max(0.0, 0.216055863061 - Q.LHA)
        - 8.657 * max(0.0, 0.049399692737 - Q.z_7)
        - 0.2524 * max(0.0, 0.049399692737 - Q.z_7) * max(0.0, 62.55 - Q.mass_top5)
        + 7.139 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 74.5 * max(0.0, 0.00528466865 - Q.e2_sq)
        - 28.78 * max(0.0, 0.028865759995 - Q.z_6)
        - 9.946 * max(0.0, 0.071488645583 - Q.z_7)
        + 7814.0 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, 0.014379521101 - Q.centroid_offset)
        + 809.5 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.031170772021 - Q.centroid_offset)
        + 0.0149 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 788.4484375 - Q.sum_pt)
        + 4570.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001503553356 - Q.lam1)
        - 28.14 * max(0.0, 0.03243272066 - Q.z_7)
        + 22.27 * max(0.0, 0.026454043164 - Q.dr_0)
        - 10.04 * max(0.0, 0.00528466865 - Q.e2_sq) * max(0.0, Q.n_pt_above_50 - 6.0)
        + 4.331 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.n_dr_0p2_0p4 - 0.0)
        - 3.991 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 84.83 * max(0.0, 0.002635417778 - Q.width)
        + 55.83 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt)
        + 103.4 * max(0.0, 0.002270363079 - Q.girth2_top5)
        - 0.004105 * max(0.0, Q.sum_pt_top5 - 752.1)
        - 2845.0 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.001130644719 - Q.lam2)
        + 0.0008768 * max(0.0, 548.196875 - Q.sum_pt_top2)
        - 4086.0 * max(0.0, 0.002635417778 - Q.width) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 205.4 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 0.562 * max(0.0, 0.03243272066 - Q.z_7) * max(0.0, Q.pt_5 - 33.0265625)
        + 0.01486 * max(0.0, 24.578125 - Q.pt_5)
        + 0.00541 * max(0.0, Q.sum_pt - 868.509375)
        - 0.2413 * max(0.0, Q.sum_pt - 868.509375) * max(0.0, 0.012587644117 - Q.centroid_offset)
        + 0.7917 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, Q.mass_top3 - 28.345095968085)
        + 505.2 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.018377780003 - Q.centroid_offset)
        - 5678.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.000145482056 - Q.mean_phi2)
        - 0.1983 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.021588001063 - Q.dr_0)
        - 192.8 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.021588001063 - Q.dr_0)
        + 236.2 * max(0.0, Q.log_sum_pt - 6.896095378249) * max(0.0, 0.04118638065 - Q.dr_0)
        + 508.4 * max(0.0, 0.071488645583 - Q.z_7) * max(0.0, 0.004331280361 - Q.mean_phi2)
        - 29.21 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.012003726523 - Q.lam1)
        - 39.26 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 0.006299534492 - Q.girth2_top2)
        + 0.38 * max(0.0, 548.196875 - Q.sum_pt_top2) * max(0.0, 0.003952581551 - Q.girth2_top3)
        - 10030.0 * max(0.0, Q.log_sum_pt - 6.572937922293) * max(0.0, 9.0303693e-05 - Q.mean_eta2)
        - 0.08309 * max(0.0, 0.084751611895 - Q.mass_over_sum_pt) * max(0.0, 18.097979966098 - Q.max_pair_mass)
        + 0.2582 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, Q.mass_top3 - 3.559569591142)
        - 9.993 * max(0.0, 0.01426135283 - Q.mean_phi2)
        - 0.3145 * max(0.0, 0.01426135283 - Q.mean_phi2) * max(0.0, 40.046952646555 - Q.max_pair_mass)
        - 97.19 * max(0.0, 0.216055863061 - Q.LHA) * max(0.0, 0.083662731125 - Q.planar_flow)
        - 63910.0 * max(0.0, 0.035560912266 - Q.e2) * max(0.0, 7.3007261e-05 - Q.lam2)
        + 52.71 * max(0.0, 0.021588001063 - Q.dr_0)
        - 16.77 * max(0.0, Q.centroid_offset - 0.008092360237)
        - 33.16 * max(0.0, 0.013238675006 - Q.width)
        + 37.96 * max(0.0, 0.154170806525 - Q.mass_over_sum_pt)
        - 0.1215 * max(0.0, 6.327378592257 - Q.log_sum_pt)
        + 3502.0 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.003408388935 - Q.lam2)
        + 14.37 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, 0.071488645583 - Q.z_7)
        + 17.61 * max(0.0, 0.050284641981 - Q.e2)
        + 15.45 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, Q.planar_flow - 0.00804883781)
        + 83.06 * max(0.0, Q.centroid_offset - 0.008092360237) * max(0.0, 0.094821243733 - Q.C2)
        + 2.469 * max(0.0, Q.centroid_offset - 0.018377780003)
        - 0.00637 * max(0.0, 6.327378592257 - Q.log_sum_pt) * max(0.0, Q.pt_6 - 27.578125)
        - 9.492 * max(0.0, 6.701242202626 - Q.log_sum_pt)
        + 26.13 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 0.049399692737 - Q.z_7)
        + 5.283 * max(0.0, Q.centroid_offset - 0.049903668404)
        + 0.5367 * Q.max_dr
        - 2.481 * max(0.0, Q.C2 - 0.010539266048)
        - 0.4484 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 0.008921136335 - Q.mean_phi2)
        + 3.436 * max(0.0, Q.LHA - 0.312727471086) * max(0.0, Q.eccentricity - 0.872657364787)
        + 0.05678 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 4.0 - Q.n_dr_0p05_0p1)
        + 119.8 * max(0.0, 0.000537286005 - Q.lam2)
        + 539.5 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_phi - 0.026127964072)
        + 6.212 * max(0.0, Q.mass_over_sum_pt - 0.008374148675)
        + 9.768 * max(0.0, Q.girth2_top5 - 0.011482925368)
        - 0.8966 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, Q.mean_phi - 0.009050007537)
        - 25.53 * max(0.0, Q.girth - 0.087236513197)
        + 1.027 * max(0.0, Q.mass_over_sum_pt - 0.008374148675) * max(0.0, 0.518696343899 - Q.tau32)
        - 0.02387 * max(0.0, 1.679198372364 - Q.D2)
        - 0.03514 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, Q.pt_2 - 56.5)
        + 45.22 * max(0.0, 0.007330079875 - Q.lam1) * max(0.0, 1.232133567333 - Q.D2)
        + 35.25 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.15855820179)
        - 44.43 * max(0.0, Q.lam2 - 0.003408388935)
        + 1.52 * max(0.0, 6.572937922293 - Q.log_sum_pt)
        - 0.008297 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 36.8125 - Q.pt_6)
        + 4.339 * max(0.0, Q.centroid_offset - 0.018377780003) * max(0.0, 24.578125 - Q.pt_5)
        + 75.36 * max(0.0, 0.013238675006 - Q.width) * max(0.0, Q.mean_eta - 0.02644207105)
        - 5433.0 * max(0.0, 0.000537286005 - Q.lam2) * max(0.0, Q.mean_eta - 0.02644207105)
        + 50.68 * max(0.0, 0.003562611155 - Q.girth2)
        + 0.003709 * max(0.0, 49.668099212646 - Q.mass)
        - 2.576 * max(0.0, Q.girth2_top5 - 0.002270363079)
        + 0.001131 * max(0.0, 1.679198372364 - Q.D2) * max(0.0, 90.625 - Q.pt_4)
        + 1.249 * max(0.0, Q.z_7 - 0.06164517166)
        - 0.005035 * max(0.0, 6.701242202626 - Q.log_sum_pt) * max(0.0, 45.75 - Q.pt_7)
        - 0.1012 * max(0.0, Q.C2 - 0.010539266048) * max(0.0, Q.pt_7 - 31.859375)
        - 0.006333 * max(0.0, 49.668099212646 - Q.mass) * max(0.0, 0.750909513235 - Q.z_dr_0p05_0p1)
        - 0.05155 * max(0.0, 0.195013533663 - Q.planar_flow)
        - 49.28 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.width - 0.00752008842)
        - 7.87 * max(0.0, 0.001056655216 - Q.girth2_top2)
        + 71.1 * max(0.0, Q.girth2 - 0.007520088344)
        + 42.46 * max(0.0, Q.girth2 - 0.004372139461)
        - 4.142 * max(0.0, Q.mass_over_sum_pt - 0.072690732432)
        - 994.8 * max(0.0, 0.001056655216 - Q.girth2_top2) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 138.1 * max(0.0, Q.girth2 - 0.0016538364)
        - 13.33 * max(0.0, 0.024547699839 - Q.e2)
        + 0.04082 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, 35.28125 - Q.pt_6)
        + 29.66 * max(0.0, 0.04081947431 - Q.girth)
        - 0.02138 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.mass_top3 - 23.663861485439)
        + 0.0001534 * max(0.0, 48.71875 - Q.pt_7)
        + 0.0005462 * max(0.0, 0.195013533663 - Q.planar_flow) * max(0.0, Q.sum_pt - 615.875)
        - 27.98 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        + 27.66 * max(0.0, 0.005590288644 - Q.width)
        - 1.142 * max(0.0, 0.02076709205 - Q.centroid_offset)
        + 29.18 * max(0.0, Q.girth2 - 0.008678044751)
        + 29.03 * max(0.0, Q.mass_over_sum_pt - 0.084751611895)
        - 110.4 * max(0.0, 0.001101266364 - Q.e2_sq)
        + 0.01679 * max(0.0, Q.mass - 80.4)
        + 34.15 * max(0.0, Q.girth2 - 0.004372139461) * max(0.0, Q.eccentricity - 0.945820652852)
        - 74.21 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, 1.122624260187 - Q.D2)
        - 7.633 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, 1.122624260187 - Q.D2)
        + 1.901 * max(0.0, 0.038466955721 - Q.e2)
        - 62.75 * max(0.0, 0.02076709205 - Q.centroid_offset) * max(0.0, Q.C2 - 0.023843882605)
        + 0.01034 * max(0.0, Q.mass - 80.4) * max(0.0, Q.eccentricity - 0.927072033478)
        + 0.003043 * max(0.0, 48.71875 - Q.pt_7) * max(0.0, 0.694781820497 - Q.planar_flow)
        - 2.039 * max(0.0, Q.centroid_offset - 0.031170772021)
        - 1.863 * max(0.0, 0.293190627853 - Q.LHA)
        - 11.76 * max(0.0, 0.005884990035 - Q.girth2_top3)
        - 221.9 * max(0.0, 0.000561123155 - Q.width)
        + 0.14 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_0 - 376.5)
        - 1028.0 * max(0.0, 0.001101266364 - Q.e2_sq) * max(0.0, -0.009460449219 - Q.phi_1)
        + 0.1321 * max(0.0, Q.centroid_offset - 0.031170772021) * max(0.0, Q.pt_2 - 56.5)
        - 1.951 * max(0.0, 0.197968879342 - Q.max_dr)
        + 180.0 * max(0.0, 0.005019718802 - Q.width)
        - 113.8 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.501026660204 - Q.tau21)
        + 4273.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.023554160423 - Q.centroid_offset)
        - 9.761 * max(0.0, 0.196739721581 - Q.LHA)
        - 10.19 * max(0.0, Q.log_sum_pt - 6.701242202626)
        + 86.63 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, 0.40079469091 - Q.planar_flow)
        + 0.5009 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 248.125 - Q.sum_pt_top2)
        - 1.709 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.n_dr_0p05_0p1 - 0.0)
        - 69.75 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.mean_phi - -0.000855675264)
        - 5.241 * max(0.0, 0.061086014472 - Q.girth)
        - 0.001445 * max(0.0, Q.sum_pt_top5 - 658.125)
        + 23.5 * max(0.0, 0.003343241496 - Q.centroid_offset)
        + 0.5126 * max(0.0, 0.177304983139 - Q.max_dr)
        + 450.8 * max(0.0, 0.005019718802 - Q.width) * max(0.0, 0.1009733513 - Q.z_dr_0p2_0p4)
        + 52.89 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        + 0.08635 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 10510.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.centroid_offset - 0.006789738266)
        - 2926.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.lam1 - 0.00027588256)
        - 2264.0 * max(0.0, 0.005019718802 - Q.width) * max(0.0, Q.mass_over_sum_pt_sq - 0.00012320649)
        + 4868.0 * max(0.0, 0.177304983139 - Q.max_dr) * max(0.0, 0.000194798295 - Q.lam2)
        - 53.38 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.000306123359 - Q.lam2)
        + 0.04676 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 48.71875 - Q.pt_7)
        + 127.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.018827652745 - Q.girth2)
        + 7417.0 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.00023679558 - Q.mass_over_sum_pt_sq)
        + 3.615 * max(0.0, 0.016554418951 - Q.e2)
        - 232.3 * max(0.0, Q.log_sum_pt - 6.701242202626) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 0.9742 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 3472.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000561123155 - Q.width)
        - 35.78 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_6 - 0.02160287394)
        - 0.5214 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.023554160423 - Q.centroid_offset)
        + 0.02484 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, Q.sum_pt - 788.4484375)
        - 9226.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.005019718802 - Q.width)
        + 21170.0 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, 0.000194798295 - Q.lam2)
        + 905.7 * max(0.0, 0.061086014472 - Q.girth) * max(0.0, Q.centroid_offset - 0.006789738266)
        + 266.6 * max(0.0, 0.024547699839 - Q.e2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 2090.0 * max(0.0, 0.006679471442 - Q.girth2) * max(0.0, Q.centroid_offset - 0.018377780003)
        - 8286.0 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, 0.000306123359 - Q.lam2)
        - 0.01227 * max(0.0, 8.379955863953 - Q.mass)
        - 0.7031 * max(0.0, 15.454033088684 - Q.mass) * max(0.0, 0.058613700176 - Q.z_7)
        + 158.4 * max(0.0, 0.196739721581 - Q.LHA) * max(0.0, Q.z_7 - 0.016858545121)
        + 0.09683 * max(0.0, 21.784077072144 - Q.mass) * max(0.0, Q.centroid_offset - 0.016278845848)
        - 2769.0 * max(0.0, Q.z_dr_0_0p05 - 0.847731333971) * max(0.0, 0.000537286005 - Q.lam2)
        + 146.6 * max(0.0, 0.000964142894 - Q.girth2)
        - 1576.0 * max(0.0, 0.000222950415 - Q.girth2_top5)
        + 4.531 * max(0.0, 0.054649224505 - Q.girth)
        + 15.95 * max(0.0, Q.lam2 - 0.001130644719)
        + 0.3225 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.026856224803 - Q.centroid_offset)
        + 2.557 * max(0.0, 0.006096650059 - Q.width)
        - 6.869 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.000872228216 - Q.lam1)
        - 0.1584 * max(0.0, Q.girth2 - 0.018827652745)
        - 3.603 * max(0.0, 0.032346998155 - Q.e2)
        - 51.45 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.40079469091 - Q.planar_flow)
        - 49.47 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.055953954317 - Q.dr01)
        + 0.08429 * max(0.0, Q.n_dr_0p2_0p4 - 1.0)
        + 0.05741 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 6.842716632804 - Q.log_sum_pt)
        + 1.166 * max(0.0, 0.221586732566 - Q.max_dr)
        - 588.8 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.C2 - 0.030867108516)
        + 8.849 * max(0.0, Q.C2 - 0.051192347892)
        - 1.275 * max(0.0, 0.018377780003 - Q.centroid_offset)
        + 1796.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.centroid_offset - 0.003343241496)
        - 323.8 * max(0.0, 0.000172198326 - Q.width)
        + 13.95 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_5 - 0.036727111752)
        + 5.484 * max(0.0, 0.007520088344 - Q.girth2)
        - 0.1505 * max(0.0, 29.644699859619 - Q.mass) * max(0.0, 0.002127561159 - Q.mean_phi2)
        - 0.004831 * max(0.0, 53.332374954224 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        - 0.03901 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.pt_4 - 47.34375)
        + 2.233 * max(0.0, 0.018377780003 - Q.centroid_offset) * max(0.0, Q.z_4 - 0.047491459878)
        - 54.79 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, Q.eccentricity - 0.903125533696)
        + 6.147 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.620723099573 - Q.eccentricity)
        - 0.0001914 * max(0.0, 41.377904891968 - Q.mass)
        + 0.004643 * max(0.0, 41.377904891968 - Q.mass) * max(0.0, 0.322073846732 - Q.planar_flow)
        + 27.76 * max(0.0, 0.032346998155 - Q.e2) * max(0.0, 0.446608647704 - Q.tau21)
        - 1.068 * max(0.0, 0.076373631775 - Q.mass_over_sum_pt)
        - 34.82 * max(0.0, 0.001503553356 - Q.lam1)
        + 0.1107 * max(0.0, Q.max_dr - 0.15984864831)
        - 1.62 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 29.0421875 - Q.pt_7)
        + 0.146 * max(0.0, Q.lam2 - 0.001130644719) * max(0.0, Q.mass_top2 - 16.308019673264)
        - 0.001025 * max(0.0, 35.5 - Q.pt_5)
        - 0.2307 * max(0.0, 0.020459658932 - Q.e2) * max(0.0, 53.4375 - Q.pt_7)
        - 14.71 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, 0.02644207105 - Q.mean_eta)
        + 0.0009689 * max(0.0, 35.5 - Q.pt_5) * max(0.0, Q.min_pair_mass - 0.173071536962)
        - 0.7828 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, Q.n_dr_0p05_0p1 - 1.0)
        + 12.47 * Q.e2
        + 725.7 * max(0.0, Q.lam2 - 0.000194798295)
        - 4.529 * max(0.0, Q.LHA - 0.303313749495)
        - 204.1 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, Q.planar_flow - 0.012569162668)
        + 0.846 * max(0.0, 6.267538488641 - Q.log_sum_pt)
        + 0.5145 * max(0.0, Q.centroid_offset - 0.00231612516) * max(0.0, 34.53125 - Q.pt_7)
        - 16.58 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 8.0 - Q.n_pt_above_50)
        + 0.0341 * max(0.0, Q.n_dr_0p2_0p4 - 2.0)
        - 109.1 * max(0.0, 0.004183811014 - Q.lam1)
        - 68.3 * max(0.0, 0.090413827016 - Q.mass_over_sum_pt)
        + 0.09018 * max(0.0, 3.0 - Q.n_dr_0p05_0p1)
        + 679.9 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 0.501026660204 - Q.tau21)
        + 4.52 * max(0.0, 0.269169217348 - Q.tau32)
        - 14.35 * max(0.0, Q.LHA - 0.303313749495) * max(0.0, 0.553068161011 - Q.tau21)
        + 0.4403 * max(0.0, 0.391541349888 - Q.tau21)
        + 49.59 * max(0.0, Q.eccentricity - 0.903125533696) * max(0.0, 0.05643851608 - Q.z_dr_0p2_0p4)
        - 1.64 * max(0.0, 0.269169217348 - Q.tau32) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        + 214.7 * max(0.0, 0.002412890926 - Q.girth2_top2)
        - 0.02969 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.pt_4 - 39.8125)
        - 9.653 * max(0.0, Q.C2 - 0.051192347892) * max(0.0, 0.222994708167 - Q.dr_7)
        - 64.13 * max(0.0, Q.lam2 - 0.000194798295) * max(0.0, 2.055451202393 - Q.D2)
        + 385.7 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, 0.175465903809 - Q.dr_7)
        + 32.71 * max(0.0, 0.391541349888 - Q.tau21) * max(0.0, Q.z_4 - 0.075444822386)
        + 0.7527 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.sum_pt - 988.4078125)
        + 803.9 * max(0.0, 0.004183811014 - Q.lam1) * max(0.0, Q.log_sum_pt - 6.701242202626)
        + 0.1268 * max(0.0, Q.mass - 15.454033088684)
        - 1.248 * max(0.0, Q.max_dr - 0.121680960059)
        + 0.001117 * max(0.0, Q.mass - 15.454033088684) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 235.7 * max(0.0, 0.0016538364 - Q.girth2)
        + 0.01921 * max(0.0, Q.sum_pt - 813.415625)
        + 38.7 * max(0.0, 0.006679471442 - Q.girth2)
        - 0.4872 * max(0.0, 0.253403707141 - Q.planar_flow)
        + 22.55 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.width - 0.006096650059)
        + 3.259 * max(0.0, 0.154689112391 - Q.LHA)
        - 19.48 * max(0.0, Q.girth - 0.076081777364)
        + 0.02492 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, 69.611351776123 - Q.mass)
        - 0.8526 * max(0.0, 0.253403707141 - Q.planar_flow) * max(0.0, Q.max_dr - 0.102758520097)
        + 0.08477 * max(0.0, 0.049903668404 - Q.centroid_offset)
        + 0.06911 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 48.71875 - Q.pt_7)
        + 0.3909 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, Q.n_dr_0p05_0p1 - 2.0)
        + 1.24 * max(0.0, 0.006390124748 - Q.e2_sq)
        - 3.293 * max(0.0, 0.049903668404 - Q.centroid_offset) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 0.00519 * max(0.0, 7.0 - Q.n_dr_0_0p05)
        - 26.86 * max(0.0, 0.006390124748 - Q.e2_sq) * max(0.0, 1.332146394253 - Q.D2)
        + 3.632 * Q.centroid_offset
        + 50.67 * max(0.0, 0.003562611091 - Q.width)
        + 0.00297 * max(0.0, 9.257203159811 - Q.mass_top5)
        + 213.2 * max(0.0, 0.154689112391 - Q.LHA) * max(0.0, 0.028070914944 - Q.z_7)
        - 0.08482 * max(0.0, 15.454033088684 - Q.mass)
        + 0.4371 * max(0.0, Q.girth - 0.076081777364) * max(0.0, 7.0 - Q.n_pt_above_50)
        - 0.0368 * max(0.0, 29.0421875 - Q.pt_7)
        + 2.84 * max(0.0, 0.004839980301 - Q.lam1)
        - 0.1089 * max(0.0, 0.035786485299 - Q.C2)
        + 0.6425 * max(0.0, 0.111761856824 - Q.max_dr)
        + 0.02008 * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 7.013e-06 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 22.844978847276 - Q.mass_top2)
        + 0.06532 * max(0.0, 0.04447356835 - Q.e2) * max(0.0, Q.pt_5 - 43.0625)
        + 0.008183 * max(0.0, 29.0421875 - Q.pt_7) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 0.02825 * max(0.0, Q.mass - 91.19)
        - 10630.0 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.lam2 - 0.000537286005)
        - 3.568 * max(0.0, Q.girth2 - 0.018827652745) * max(0.0, Q.pt_7 - 15.55390625)
        - 4.967 * max(0.0, Q.mean_phi - 0.026127964072)
        - 55.68 * max(0.0, 0.148408418149 - Q.girth)
        + 9.137 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        + 0.529 * max(0.0, 0.148408418149 - Q.girth) * max(0.0, 38.53125 - Q.pt_7)
        - 84.4 * max(0.0, 0.016433749775 - Q.lam1)
        + 0.2206 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, Q.z_7 - 0.023207568189)
        + 34140.0 * max(0.0, 0.000306123359 - Q.lam2) * max(0.0, 0.049903668404 - Q.centroid_offset)
        - 0.001595 * max(0.0, 531.1875 - Q.sum_pt_top5)
        - 0.0001907 * max(0.0, Q.sum_pt_top5 - 658.125) * max(0.0, 43.5 - Q.pt_7)
        + 0.0004979 * max(0.0, Q.sum_pt_top5 - 902.40625)
        - 0.007538 * max(0.0, Q.sum_pt_top5 - 839.9546875)
        + 0.5063 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 56.53125 - Q.pt_6)
        - 50.71 * max(0.0, 0.050284641981 - Q.e2) * max(0.0, Q.pt_dispersion - 0.396830244362)
        + 0.692 * max(0.0, 0.501026660204 - Q.tau21)
        + 951.9 * max(0.0, 0.016433749775 - Q.lam1) * max(0.0, 0.037760993714 - Q.centroid_offset)
        - 7.96 * max(0.0, 0.067272114405 - Q.z_6)
        - 5.175 * max(0.0, 0.037760993714 - Q.centroid_offset)
        + 2.139 * max(0.0, Q.LHA - 0.09323897448)
        - 0.001002 * max(0.0, Q.sum_pt_top5 - 902.40625) * max(0.0, 3.885568320751 - Q.D2)
        - 0.005928 * max(0.0, Q.sum_pt_top5 - 839.9546875) * max(0.0, 0.15855820179 - Q.z_dr_0p1_0p2)
        + 3.505 * max(0.0, 0.501026660204 - Q.tau21) * max(0.0, Q.max_dr - 0.015595615841)
        + 5.481 * max(0.0, 0.00752008842 - Q.width)
        - 1.639 * max(0.0, 763.825 - Q.sum_pt) * max(0.0, 0.037477688199 - Q.z_4)
        + 0.09102 * max(0.0, 25.578125 - Q.pt_7)
        - 0.1524 * max(0.0, Q.sum_pt - 988.4078125)
        - 0.006252 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, Q.n_pt_above_50 - 6.0)
        - 0.0002839 * max(0.0, Q.sum_pt - 988.4078125) * max(0.0, 3.885568320751 - Q.D2)
        - 0.5267 * max(0.0, 0.111513564951 - Q.planar_flow)
        + 0.09606 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 15.78 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018377780003)
        + 34.28 * max(0.0, Q.lam1 - 0.008375572068)
        - 26.28 * max(0.0, Q.lam1 - 0.004183811014)
        + 19.52 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 0.15984864831 - Q.max_dr)
        + 54.03 * max(0.0, Q.lam1 - 0.00543336053)
        + 0.0045 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, 739.5 - Q.sum_pt)
        + 49.61 * max(0.0, Q.lam1 - 0.007330079875)
        - 0.9796 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 0.067292226106 - Q.C2)
        + 3476.0 * max(0.0, Q.lam1 - 0.007330079875) * max(0.0, 0.13261153996 - Q.max_dr)
        - 0.6354 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235)
        - 1801.0 * max(0.0, Q.lam1 - 0.00543336053) * max(0.0, 0.15984864831 - Q.max_dr)
        - 34.72 * max(0.0, 0.111513564951 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.009480684835)
        - 0.005648 * max(0.0, 76.655700683594 - Q.mass)
        - 2.383 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, Q.eccentricity - 0.970449631164)
        + 0.07969 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        + 41.05 * max(0.0, Q.lam1 - 0.005954149834)
        - 0.01387 * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        - 15.39 * max(0.0, Q.lam1 - 0.002464291268)
        - 359.7 * max(0.0, 0.011660904657 - Q.mass_over_sum_pt_sq)
        + 0.009715 * max(0.0, 76.655700683594 - Q.mass) * max(0.0, 0.74595130682 - Q.D2)
        + 73.36 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.111513564951 - Q.planar_flow)
        - 597.5 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, Q.eccentricity - 0.970449631164)
        + 105.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        + 0.2424 * max(0.0, 1.122624260187 - Q.D2)
        + 5.775 * max(0.0, 0.038466955721 - Q.e2) * max(0.0, 1.002470755577 - Q.D2)
        + 0.01285 * max(0.0, 5.0 - Q.n_dr_0p05_0p1)
        + 3.618 * max(0.0, 1.122624260187 - Q.D2) * max(0.0, 0.031170772021 - Q.centroid_offset)
        - 6.005 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, Q.eccentricity - 0.984196588116)
        + 0.01574 * max(0.0, 0.74595130682 - Q.D2)
        + 43.61 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 6.804164030582 - Q.log_sum_pt)
        - 45.07 * max(0.0, 0.008678044951 - Q.width) * max(0.0, 1.002470755577 - Q.D2)
        - 15.2 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 1.002470755577 - Q.D2)
        - 3.006 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 37.11 * max(0.0, 0.004372139461 - Q.girth2) * max(0.0, 1.0 - Q.n_dr_0p2_0p4)
        - 0.6738 * max(0.0, 0.013238675334 - Q.girth2) * max(0.0, 3.0 - Q.n_dr_0p1_0p2)
        + 0.6929 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.588259786367 - Q.z_dr_0p05_0p1)
        + 14.51 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.121680960059 - Q.max_dr)
        + 1.892 * max(0.0, 0.23799610585 - Q.tau21) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        + 5427.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, Q.e2 - 0.024547699839)
        - 57.56 * max(0.0, 0.012003726523 - Q.lam1)
        - 216.1 * max(0.0, 0.011657374702 - Q.e2_sq)
        - 546.9 * max(0.0, 0.007182835724 - Q.mass_over_sum_pt_sq)
        + 0.003781 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.sum_pt_top3 - 353.0625)
        + 4.909 * max(0.0, 0.041109715588 - Q.e2)
        + 6.437 * max(0.0, 0.063441075385 - Q.e2)
        + 0.05599 * max(0.0, 0.328461505473 - Q.z_dr_0p1_0p2)
        + 0.4202 * max(0.0, Q.z_dr_0p05_0p1 - 0.750909513235) * max(0.0, 2.0 - Q.n_dr_0p2_0p4)
        - 9.104e-05 * max(0.0, 2.0 - Q.n_dr_0_0p05)
        + 1.196 * max(0.0, 0.008375572068 - Q.lam1) * max(0.0, Q.m01 - 16.308019673264)
        - 1.788 * max(0.0, 0.006506575659 - Q.lam1) * max(0.0, Q.pt1_dr01 - 1.21960336377)
        + 0.03157 * max(0.0, Q.mass - 80.4) * max(0.0, 0.20552001074 - Q.z_dr_0p2_0p4)
        - 34.1 * max(0.0, Q.LHA - 0.176724128067) * max(0.0, Q.z_top5 - 0.865048766136)
        - 2282.0 * max(0.0, 0.006096650059 - Q.width) * max(0.0, Q.log_sum_pt - 6.896095378249)
        - 0.2085 * max(0.0, 0.018827652745 - Q.girth2) * max(0.0, Q.mass_top2 - 22.844978847276)
        + 19.0 * max(0.0, 0.00752008842 - Q.width) * max(0.0, 0.061262048692 - Q.planar_flow)
        + 14.01 * max(0.0, 0.06813910019 - Q.mass_over_sum_pt)
        - 0.02736 * max(0.0, Q.n_dr_0p05_0p1 - 5.0)
        - 6.834 * max(0.0, Q.LHA - 0.346713497427)
        + 26.46 * max(0.0, Q.girth - 0.033604209498)
        - 50.18 * max(0.0, 0.002151567843 - Q.girth2_top3)
        - 1.886 * max(0.0, 0.007639643088 - Q.girth2_top2)
    )


def scores(Q):
    return {c: f(Q) for c, f in zip(CLASSES, (score_g, score_q, score_W, score_Z, score_t))}


def decide(Q, s):
    if Q.width > 0.009197441395372152:
        if s['g'] - s['t'] > -0.15487468242645264:
            if s['g'] - s['t'] > 0.008620239794254303:
                if s['g'] - s['q'] > -0.06517927907407284:
                    if s['g'] - s['Z'] > -0.02077453676611185:
                        if s['g'] - s['t'] > 0.3740038275718689:
                            if Q.e2 > 0.10193249955773354:
                                if Q.pt_4 > 51.234375:
                                    return 'g'   # 92% of the training jets here get this class from the formula
                                else:
                                    if Q.girth2_top3 > 0.0555100291967392:
                                        return 'g'   # 77% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 61% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['Z'] > 8.340018272399902:
                                    if s['g'] - s['t'] > 1.169784963130951:
                                        return 'g'   # 99% of the training jets here get this class from the formula
                                    else:
                                        if Q.centroid_offset > 0.03260336257517338:
                                            return 'g'   # 83% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['W'] > 12.1140456199646:
                                                return 'g'   # 65% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 82% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 98% of the training jets here get this class from the formula
                        else:
                            if s['q'] - s['Z'] > 7.619341135025024:
                                if Q.pt_6 > 24.7890625:
                                    if Q.girth2_top3 > 0.009323391597718:
                                        if s['q'] - s['W'] > 10.534032344818115:
                                            return 't'   # 72% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['t'] > -0.6956802010536194:
                                                return 't'   # 59% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 79% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 89% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 66% of the training jets here get this class from the formula
                            else:
                                if Q.e2 > 0.09830567985773087:
                                    if Q.pt_7 > 36.515625:
                                        return 'g'   # 69% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 74% of the training jets here get this class from the formula
                                else:
                                    if Q.mass_over_sum_pt > 0.0632023811340332:
                                        if s['Z'] - s['t'] > -3.151324987411499:
                                            return 'g'   # 93% of the training jets here get this class from the formula
                                        else:
                                            if Q.tau32 > 0.1586519405245781:
                                                return 'g'   # 86% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 52% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 50% of the training jets here get this class from the formula
                    else:
                        if Q.mass_top5 > 49.753984451293945:
                            return 'g'   # 64% of the training jets here get this class from the formula
                        else:
                            return 'Z'   # 87% of the training jets here get this class from the formula
                else:
                    if s['g'] - s['q'] > -0.2610173970460892:
                        if Q.girth2_top2 > 0.019542424008250237:
                            return 'g'   # 60% of the training jets here get this class from the formula
                        else:
                            return 'q'   # 78% of the training jets here get this class from the formula
                    else:
                        return 'q'   # 93% of the training jets here get this class from the formula
            else:
                if s['Z'] - s['t'] > -0.14467672258615494:
                    return 'Z'   # 85% of the training jets here get this class from the formula
                else:
                    if s['g'] - s['q'] > -0.2815948873758316:
                        if s['g'] - s['t'] > -0.07579886168241501:
                            if s['q'] - s['Z'] > 6.970127582550049:
                                if Q.z_dr_0p05_0p1 > 0.0894029252231121:
                                    if Q.phi_7 > 0.038543701171875:
                                        return 't'   # 67% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 80% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 81% of the training jets here get this class from the formula
                            else:
                                if Q.n_pt_above_50 > 1.5:
                                    if Q.pt_6 > 37.171875:
                                        if Q.tau32 > 0.6324963569641113:
                                            return 'g'   # 84% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['t'] > -1.726602554321289:
                                                return 'g'   # 70% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 60% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['W'] > 3.0908336639404297:
                                            if Q.phi_7 > -0.0015132427215576172:
                                                return 't'   # 57% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 70% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 83% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 88% of the training jets here get this class from the formula
                        else:
                            if Q.mass > 49.22847938537598:
                                if Q.mass > 94.51290512084961:
                                    if s['Z'] - s['t'] > -7.068643093109131:
                                        if Q.centroid_offset > 0.01728248316794634:
                                            return 'g'   # 72% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 70% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 96% of the training jets here get this class from the formula
                                else:
                                    if Q.D2 > 1.843755066394806:
                                        return 't'   # 67% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 62% of the training jets here get this class from the formula
                            else:
                                if Q.C2 > 0.08197004720568657:
                                    return 'g'   # 70% of the training jets here get this class from the formula
                                else:
                                    if Q.eta_0 > 0.074981689453125:
                                        if Q.max_pair_mass > 13.244242191314697:
                                            return 't'   # 64% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 81% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 74% of the training jets here get this class from the formula
                    else:
                        return 'q'   # 88% of the training jets here get this class from the formula
        else:
            if s['Z'] - s['t'] > -0.1370302066206932:
                if s['Z'] - s['t'] > 0.1374722346663475:
                    if Q.sum_pt > 748.203125:
                        if s['Z'] - s['t'] > 0.4915202260017395:
                            return 'Z'   # 95% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['W'] > 4.00553572177887:
                                return 't'   # 68% of the training jets here get this class from the formula
                            else:
                                return 'Z'   # 77% of the training jets here get this class from the formula
                    else:
                        return 'Z'   # 98% of the training jets here get this class from the formula
                else:
                    if Q.sum_pt > 633.546875:
                        if Q.D2 > 0.30910588800907135:
                            if Q.sum_pt_top2 > 308.90625:
                                return 't'   # 62% of the training jets here get this class from the formula
                            else:
                                return 'Z'   # 70% of the training jets here get this class from the formula
                        else:
                            return 't'   # 88% of the training jets here get this class from the formula
                    else:
                        if Q.centroid_offset > 0.026496989652514458:
                            return 't'   # 56% of the training jets here get this class from the formula
                        else:
                            return 'Z'   # 83% of the training jets here get this class from the formula
            else:
                if s['q'] - s['t'] > -0.1338217779994011:
                    if s['q'] - s['t'] > 0.09301432222127914:
                        return 'q'   # 83% of the training jets here get this class from the formula
                    else:
                        if Q.pt_dispersion > 0.43434880673885345:
                            if s['W'] - s['t'] > -5.559607982635498:
                                return 't'   # 82% of the training jets here get this class from the formula
                            else:
                                if Q.m012 > 4.268625974655151:
                                    return 'q'   # 67% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 65% of the training jets here get this class from the formula
                        else:
                            if Q.lam2 > 0.00010362618559156545:
                                return 'q'   # 84% of the training jets here get this class from the formula
                            else:
                                return 't'   # 57% of the training jets here get this class from the formula
                else:
                    if s['g'] - s['t'] > -0.3931789994239807:
                        if Q.width > 0.026639237999916077:
                            if Q.centroid_offset > 0.029343734495341778:
                                if Q.pt_7 > 27.6328125:
                                    if Q.max_dr > 0.269146129488945:
                                        return 'g'   # 82% of the training jets here get this class from the formula
                                    else:
                                        if Q.z_dr_0p05_0p1 > 0.06013109162449837:
                                            return 't'   # 76% of the training jets here get this class from the formula
                                        else:
                                            if Q.eta_0 > 0.02387237548828125:
                                                if Q.mean_eta > 0.03243500180542469:
                                                    return 'g'   # 72% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 80% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 79% of the training jets here get this class from the formula
                                else:
                                    if Q.D2 > 0.8295169770717621:
                                        return 'g'   # 62% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 89% of the training jets here get this class from the formula
                            else:
                                return 't'   # 76% of the training jets here get this class from the formula
                        else:
                            if Q.C2 > 0.07706456258893013:
                                if Q.pt_7 > 24.625:
                                    if s['q'] - s['Z'] > 3.5009654760360718:
                                        return 't'   # 81% of the training jets here get this class from the formula
                                    else:
                                        if Q.mean_phi > 0.007275065174326301:
                                            return 't'   # 80% of the training jets here get this class from the formula
                                        else:
                                            if Q.pt_6 > 42.21875:
                                                return 'g'   # 82% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 62% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 67% of the training jets here get this class from the formula
                            else:
                                if Q.centroid_offset > 0.052014170214533806:
                                    if Q.z_dr_0p1_0p2 > 0.19072063267230988:
                                        if Q.dr_0 > 0.11780570074915886:
                                            return 't'   # 78% of the training jets here get this class from the formula
                                        else:
                                            if Q.tau21 > 0.3210374414920807:
                                                return 't'   # 76% of the training jets here get this class from the formula
                                            else:
                                                if Q.phi_1 > 0.041748046875:
                                                    return 't'   # 67% of the training jets here get this class from the formula
                                                else:
                                                    if Q.e2 > 0.03631100058555603:
                                                        return 'g'   # 75% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 58% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 88% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['t'] > -0.2351740300655365:
                                        if Q.e2 > 0.0685371607542038:
                                            return 'g'   # 52% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 81% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 92% of the training jets here get this class from the formula
                    else:
                        if s['Z'] - s['t'] > -0.518286406993866:
                            if s['W'] - s['t'] > -4.398602724075317:
                                if Q.centroid_offset > 0.007874831324443221:
                                    if Q.lam2 > 0.0002027922309935093:
                                        if Q.dr_3 > 0.06825930997729301:
                                            return 'Z'   # 56% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 90% of the training jets here get this class from the formula
                                    else:
                                        return 'Z'   # 71% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 78% of the training jets here get this class from the formula
                            else:
                                return 't'   # 91% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['t'] > -0.6671048402786255:
                                if Q.lam1 > 0.034212928265333176:
                                    if Q.mean_phi > 0.04936755262315273:
                                        return 'g'   # 76% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_4 > 51.03125:
                                            return 'g'   # 56% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 78% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 95% of the training jets here get this class from the formula
                            else:
                                return 't'   # 100% of the training jets here get this class from the formula
    else:
        if s['q'] - s['Z'] > 0.17603666335344315:
            if s['g'] - s['q'] > 0.06651259958744049:
                if s['g'] - s['t'] > -0.050770772621035576:
                    if s['g'] - s['W'] > 0.06107725948095322:
                        if s['g'] - s['q'] > 0.1760062724351883:
                            if s['g'] - s['t'] > 0.229898601770401:
                                if s['g'] - s['q'] > 0.29413631558418274:
                                    if s['g'] - s['W'] > 0.37635183334350586:
                                        if Q.z_7 > 0.0137370596639812:
                                            if Q.LHA > 0.05418029800057411:
                                                if s['q'] - s['Z'] > 5.116793394088745:
                                                    if s['g'] - s['t'] > 1.3649688959121704:
                                                        return 'g'   # 98% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.z_7 > 0.04486602544784546:
                                                            return 'g'   # 92% of the training jets here get this class from the formula
                                                        else:
                                                            if s['g'] - s['q'] > 1.2752330303192139:
                                                                return 'g'   # 90% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.pt_7 > 18.34375:
                                                                    return 'g'   # 79% of the training jets here get this class from the formula
                                                                else:
                                                                    return 't'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.0018900777213275433:
                                                        return 'g'   # 100% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['q'] > 0.3723166733980179:
                                                            return 'g'   # 98% of the training jets here get this class from the formula
                                                        else:
                                                            if s['q'] - s['Z'] > 1.986541748046875:
                                                                return 'g'   # 91% of the training jets here get this class from the formula
                                                            else:
                                                                if s['q'] - s['t'] > 3.1107375621795654:
                                                                    return 'q'   # 55% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 86% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 61% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > 0.8559941351413727:
                                                return 'g'   # 73% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 85% of the training jets here get this class from the formula
                                    else:
                                        if Q.e2 > 0.030619241297245026:
                                            if Q.mass > 29.920292854309082:
                                                if s['Z'] - s['t'] > -0.5721572935581207:
                                                    return 'W'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 71% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 95% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['Z'] > 1.2443513870239258:
                                                return 'g'   # 97% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt1_dr01 > 11.041543960571289:
                                                    return 'W'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    if s['Z'] - s['t'] > 2.3277684450149536:
                                                        if s['q'] - s['W'] > -0.18095549941062927:
                                                            return 'g'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.mass_top3 > 2.373353362083435:
                                                                return 'W'   # 67% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 66% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.mass > 12.331191062927246:
                                                            if Q.pt_7 > 35.515625:
                                                                return 'g'   # 88% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.pt_dispersion > 0.412533164024353:
                                                                    return 'g'   # 78% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 53% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 96% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.004893647972494364:
                                        if s['q'] - s['W'] > 0.0038090345915406942:
                                            if Q.z_7 > 0.03589611314237118:
                                                return 'g'   # 97% of the training jets here get this class from the formula
                                            else:
                                                if Q.max_dr > 0.017864340916275978:
                                                    return 'g'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 63% of the training jets here get this class from the formula
                                        else:
                                            if Q.pt1_dr01 > 0.7924483120441437:
                                                if Q.girth > 0.02126309648156166:
                                                    return 'g'   # 74% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 60% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 86% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['Z'] > 2.393101453781128:
                                            if Q.sum_pt > 1207.90625:
                                                return 'q'   # 77% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt_7 > 28.3359375:
                                                    return 'g'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    if s['Z'] - s['t'] > -0.8033650815486908:
                                                        return 'g'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 38% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['t'] > 3.0956305265426636:
                                                if Q.centroid_offset > 0.0033056626562029123:
                                                    if Q.pt_2 > 83.625:
                                                        return 'g'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 67% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt > 768.140625:
                                                        return 'g'   # 71% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.e2 > 0.0031318238470703363:
                                                            return 'q'   # 80% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 64% of the training jets here get this class from the formula
                                            else:
                                                if Q.girth2_top5 > 0.0007569092267658561:
                                                    return 'g'   # 92% of the training jets here get this class from the formula
                                                else:
                                                    if Q.pt1_dr01 > 1.237074375152588:
                                                        if Q.mean_eta > -0.0012420174316503108:
                                                            return 'g'   # 63% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 73% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 80% of the training jets here get this class from the formula
                            else:
                                if Q.centroid_offset > 0.046813324093818665:
                                    if Q.pt_7 > 36.34375:
                                        return 'g'   # 86% of the training jets here get this class from the formula
                                    else:
                                        if Q.log_sum_pt > 6.160745859146118:
                                            if s['g'] - s['t'] > 0.08522964268922806:
                                                if Q.pt_7 > 26.9765625:
                                                    return 'g'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 82% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 73% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > 4.6133880615234375:
                                                return 't'   # 64% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 81% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['W'] > 0.4224880784749985:
                                        if s['g'] - s['t'] > 0.058750689029693604:
                                            return 'g'   # 87% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_dr_0p2_0p4 > 0.0768810547888279:
                                                return 't'   # 54% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 79% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['Z'] > 0.8178276121616364:
                                            return 'g'   # 88% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 52% of the training jets here get this class from the formula
                        else:
                            if Q.centroid_offset > 0.005309609696269035:
                                if s['W'] - s['t'] > 3.3924137353897095:
                                    if Q.max_dr > 0.03868534602224827:
                                        return 'g'   # 66% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt_top3 > 548.5:
                                            return 'q'   # 80% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 67% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 0.11724848300218582:
                                        if s['q'] - s['Z'] > 0.6786807775497437:
                                            if Q.pt_5 > 38.109375:
                                                if Q.z_top5 > 0.8009546101093292:
                                                    if s['W'] - s['Z'] > 0.012797909788787365:
                                                        return 'g'   # 90% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.sum_pt > 744.671875:
                                                            return 'g'   # 90% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.mass > 10.355444431304932:
                                                                return 'g'   # 88% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 96% of the training jets here get this class from the formula
                                            else:
                                                if Q.girth2_top5 > 0.000128271130961366:
                                                    if s['q'] - s['W'] > 2.198489546775818:
                                                        if Q.C2 > 0.01649019867181778:
                                                            return 'g'   # 74% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 51% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 89% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 68% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass_over_sum_pt > 0.021384836174547672:
                                                return 'W'   # 45% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 69% of the training jets here get this class from the formula
                                    else:
                                        if Q.z_top5 > 0.8249510824680328:
                                            if Q.width > 0.00010483511505299248:
                                                if Q.LHA > 0.17602885514497757:
                                                    if Q.max_dr > 0.08844960108399391:
                                                        if Q.mass > 25.377931594848633:
                                                            return 'g'   # 79% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 53% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.C2 > 0.012184428051114082:
                                                            return 'q'   # 76% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 58% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam2 > 6.460424629040062e-05:
                                                        return 'g'   # 88% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.mass > 7.323447227478027:
                                                            if Q.e2 > 0.007939279545098543:
                                                                return 'g'   # 84% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.LHA > 0.1139712706208229:
                                                                    return 'q'   # 73% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 66% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 80% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 72% of the training jets here get this class from the formula
                                        else:
                                            if s['W'] - s['Z'] > -0.107828538864851:
                                                return 'g'   # 81% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt_2 > 97.53125:
                                                    return 'g'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 63% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['Z'] > 2.506723403930664:
                                    if s['g'] - s['q'] > 0.1051509752869606:
                                        if Q.pt_7 > 30.1953125:
                                            if Q.log_sum_pt > 6.709285259246826:
                                                return 'g'   # 92% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 17.40459442138672:
                                                    return 'g'   # 89% of the training jets here get this class from the formula
                                                else:
                                                    if Q.dr_0 > 0.020657670684158802:
                                                        return 'q'   # 72% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['Z'] > 2.7183960676193237:
                                                            return 'g'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.pt_7 > 45.71875:
                                                                if Q.z_5 > 0.08700526505708694:
                                                                    return 'g'   # 73% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'q'   # 70% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 90% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 51% of the training jets here get this class from the formula
                                    else:
                                        if Q.log_sum_pt > 6.72690749168396:
                                            return 'g'   # 78% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.0025837059365585446:
                                                if Q.pt_5 > 67.84375:
                                                    return 'g'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['Z'] > 0.08256538584828377:
                                                        return 'g'   # 71% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 61% of the training jets here get this class from the formula
                                            else:
                                                if Q.tau21 > 0.35960546135902405:
                                                    return 'q'   # 89% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 70% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['t'] > 2.3391016721725464:
                                        if Q.sum_pt > 842.234375:
                                            if Q.girth2_top2 > 8.221172538469546e-05:
                                                return 'g'   # 84% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_7 > 0.05258130095899105:
                                                    return 'g'   # 74% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt > 1014.171875:
                                                        if Q.sum_pt > 1140.90625:
                                                            return 'q'   # 64% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 88% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 81% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['Z'] > 1.7011982798576355:
                                                if Q.mass > 11.408508777618408:
                                                    if Q.sum_pt > 671.21875:
                                                        if s['g'] - s['q'] > 0.11809816211462021:
                                                            return 'g'   # 90% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 59% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    if Q.pt_5 > 37.203125:
                                                        if Q.centroid_offset > 0.004267754731699824:
                                                            if s['g'] - s['Z'] > 2.2794939279556274:
                                                                return 'g'   # 59% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 62% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt_5 > 50.90625:
                                                    return 'q'   # 56% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if Q.LHA > 0.22272314131259918:
                                            return 'g'   # 92% of the training jets here get this class from the formula
                                        else:
                                            if Q.lam1 > 0.00020183972810627893:
                                                if s['g'] - s['q'] > 0.10556597262620926:
                                                    if Q.pt_7 > 31.1171875:
                                                        if Q.pt_4 > 61.671875:
                                                            return 'q'   # 59% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 64% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 74% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 89% of the training jets here get this class from the formula
                    else:
                        if s['g'] - s['W'] > -0.428615927696228:
                            if s['g'] - s['Z'] > 0.9978578686714172:
                                if Q.e2 > 0.028585005551576614:
                                    if s['g'] - s['Z'] > 1.474596917629242:
                                        if Q.planar_flow > 0.03452811576426029:
                                            if Q.mass > 31.81063175201416:
                                                return 'W'   # 73% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 62% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 89% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 75% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['W'] > -0.1917937994003296:
                                        if Q.dr_3 > 0.11205435544252396:
                                            return 'W'   # 54% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 82% of the training jets here get this class from the formula
                                    else:
                                        if Q.n_dr_0_0p05 > 6.5:
                                            if Q.mass > 27.921642303466797:
                                                return 'W'   # 79% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 62% of the training jets here get this class from the formula
                                        else:
                                            if Q.max_pair_mass > 13.820130825042725:
                                                return 'W'   # 66% of the training jets here get this class from the formula
                                            else:
                                                if Q.girth2_top3 > 0.0012227247352711856:
                                                    if Q.log_sum_pt > 6.390512704849243:
                                                        return 'W'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 85% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 88% of the training jets here get this class from the formula
                            else:
                                if Q.girth > 0.04671783372759819:
                                    return 'W'   # 93% of the training jets here get this class from the formula
                                else:
                                    if s['Z'] - s['t'] > 2.7048304080963135:
                                        return 'W'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_0 > 343.875:
                                            return 'g'   # 69% of the training jets here get this class from the formula
                                        else:
                                            if Q.lam2 > 5.4323292715707794e-05:
                                                return 'W'   # 80% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['Z'] > 0.5601967871189117:
                                                    return 'g'   # 56% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 73% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['Z'] > 1.2318024039268494:
                                if Q.sum_pt_top5 > 666.59375:
                                    return 'g'   # 56% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 86% of the training jets here get this class from the formula
                            else:
                                return 'W'   # 96% of the training jets here get this class from the formula
                else:
                    if s['W'] - s['t'] > -0.02925233729183674:
                        if s['W'] - s['t'] > 0.34429319202899933:
                            return 'W'   # 97% of the training jets here get this class from the formula
                        else:
                            if Q.n_dr_0p1_0p2 > 1.5:
                                return 't'   # 60% of the training jets here get this class from the formula
                            else:
                                return 'W'   # 83% of the training jets here get this class from the formula
                    else:
                        if s['g'] - s['t'] > -0.2529173046350479:
                            if Q.sum_pt > 493.7734375:
                                if Q.tau21 > 0.11148727685213089:
                                    if Q.C2 > 0.07635469734668732:
                                        if Q.D2 > 3.0357041358947754:
                                            return 't'   # 82% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 86% of the training jets here get this class from the formula
                                    else:
                                        if Q.log_sum_pt > 6.4421045780181885:
                                            if s['g'] - s['t'] > -0.1578751653432846:
                                                return 'g'   # 58% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 89% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 84% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 60% of the training jets here get this class from the formula
                            else:
                                if Q.z_dr_0p2_0p4 > 0.0655292496085167:
                                    return 't'   # 86% of the training jets here get this class from the formula
                                else:
                                    if Q.pt_5 > 32.671875:
                                        if s['g'] - s['t'] > -0.10012470558285713:
                                            return 'g'   # 80% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > 1.4737749695777893:
                                                return 'g'   # 69% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 65% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 84% of the training jets here get this class from the formula
                        else:
                            if Q.girth > 0.02913726679980755:
                                if s['g'] - s['t'] > -0.470483735203743:
                                    if Q.D2 > 1.0737341046333313:
                                        return 't'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_6 > 27.1015625:
                                            return 't'   # 79% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 60% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 99% of the training jets here get this class from the formula
                            else:
                                return 'g'   # 42% of the training jets here get this class from the formula
            else:
                if s['q'] - s['W'] > -0.03641217015683651:
                    if s['q'] - s['t'] > -0.0418864656239748:
                        if s['g'] - s['q'] > -0.025541121140122414:
                            if Q.planar_flow > 0.050336096435785294:
                                if Q.sum_pt > 1023.1171875:
                                    if Q.sum_pt > 1168.765625:
                                        return 'q'   # 77% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 86% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 0.024697977118194103:
                                        if s['W'] - s['Z'] > 0.05761439725756645:
                                            if s['W'] - s['t'] > 3.033355712890625:
                                                if Q.pt_dispersion > 0.3989757299423218:
                                                    if Q.mass_over_sum_pt_sq > 0.00011616930714808404:
                                                        return 'g'   # 46% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 90% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 60% of the training jets here get this class from the formula
                                            else:
                                                if Q.C2 > 0.010563920717686415:
                                                    if Q.e2 > 0.006684274412691593:
                                                        if Q.planar_flow > 0.7509517669677734:
                                                            return 'g'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.centroid_offset > 0.011047384701669216:
                                                                if Q.eccentricity > 0.9716574549674988:
                                                                    return 'g'   # 55% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'q'   # 75% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.mass > 14.746253967285156:
                                                                    if Q.log_sum_pt > 6.481229543685913:
                                                                        if Q.centroid_offset > 0.00454063736833632:
                                                                            return 'g'   # 80% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'q'   # 52% of the training jets here get this class from the formula
                                                                    else:
                                                                        if s['W'] - s['Z'] > 0.2467297539114952:
                                                                            return 'g'   # 55% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'q'   # 83% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'q'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 67% of the training jets here get this class from the formula
                                        else:
                                            if Q.max_dr > 0.07179470732808113:
                                                if Q.sum_pt > 654.875:
                                                    return 'g'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 63% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['Z'] > 1.7192410230636597:
                                                    if Q.pt_2 > 123.46875:
                                                        if Q.z_5 > 0.07988724485039711:
                                                            return 'g'   # 67% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.girth2_top5 > 0.00011411161176511087:
                                                                return 'g'   # 54% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 80% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt_top2 > 329.8125:
                                                        return 'g'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 70% of the training jets here get this class from the formula
                                    else:
                                        if Q.girth2 > 0.00011019750672858208:
                                            if Q.pt_5 > 74.3125:
                                                if Q.dr_0 > 0.010231981053948402:
                                                    return 'q'   # 68% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 74% of the training jets here get this class from the formula
                                            else:
                                                if Q.C2 > 0.03940070606768131:
                                                    return 'g'   # 62% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['W'] > 0.3373755216598511:
                                                        if Q.C2 > 0.007467588176950812:
                                                            if Q.sum_pt_top3 > 619.8125:
                                                                if Q.girth2_top5 > 0.00020682081958511844:
                                                                    return 'g'   # 67% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'q'   # 80% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.girth2_top2 > 2.190793111367384e-05:
                                                                    if s['W'] - s['Z'] > 0.48488958179950714:
                                                                        if Q.planar_flow > 0.07010249048471451:
                                                                            return 'q'   # 77% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'g'   # 65% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'q'   # 86% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.z_6 > 0.05669274181127548:
                                                                if s['Z'] - s['t'] > 2.4512147903442383:
                                                                    return 'q'   # 76% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.sum_pt > 735.375:
                                                                        return 'g'   # 90% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'q'   # 65% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.lam2 > 8.112618525046855e-05:
                                                            return 'W'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 63% of the training jets here get this class from the formula
                                        else:
                                            if Q.log_sum_pt > 6.571320533752441:
                                                return 'q'   # 93% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 52% of the training jets here get this class from the formula
                            else:
                                if s['W'] - s['Z'] > 0.2794150412082672:
                                    if Q.z_top5 > 0.7964917719364166:
                                        if s['W'] - s['Z'] > 0.7876971065998077:
                                            return 'g'   # 77% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 62% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 90% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['Z'] > -2.6740505695343018:
                                        return 'q'   # 65% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 77% of the training jets here get this class from the formula
                        else:
                            if s['q'] - s['W'] > 0.22528216242790222:
                                if s['g'] - s['q'] > -0.11657501384615898:
                                    if Q.sum_pt_top3 > 671.5:
                                        if Q.log_sum_pt > 7.056336879730225:
                                            return 'q'   # 87% of the training jets here get this class from the formula
                                        else:
                                            if Q.sum_pt > 1060.609375:
                                                return 'g'   # 82% of the training jets here get this class from the formula
                                            else:
                                                if Q.e2_sq > 0.00015969778905855492:
                                                    return 'g'   # 69% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 88% of the training jets here get this class from the formula
                                    else:
                                        if Q.eccentricity > 0.9910659492015839:
                                            if Q.C2 > 0.01106460252776742:
                                                return 'g'   # 60% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 67% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth2 > 3.213423224224243e-05:
                                                if Q.z_7 > 0.03138778358697891:
                                                    if Q.lam1 > 0.0020186053588986397:
                                                        return 'q'   # 72% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.centroid_offset > 0.002003390691243112:
                                                            return 'q'   # 96% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.pt_4 > 51.359375:
                                                                return 'q'   # 90% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    if Q.girth2_top2 > 5.113090082886629e-05:
                                                        return 'q'   # 81% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 75% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['Z'] > 1.719170093536377:
                                                    return 'q'   # 88% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 82% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['Z'] > -0.26615066826343536:
                                        if s['q'] - s['t'] > 0.974924772977829:
                                            if s['q'] - s['Z'] > 0.5390777885913849:
                                                if s['g'] - s['q'] > -0.39220382273197174:
                                                    if Q.sum_pt > 1040.359375:
                                                        if Q.sum_pt > 1173.859375:
                                                            return 'q'   # 96% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.sum_pt > 1078.859375:
                                                                if Q.z_7 > 0.030246944166719913:
                                                                    return 'g'   # 73% of the training jets here get this class from the formula
                                                                else:
                                                                    if s['W'] - s['t'] > 2.4338951110839844:
                                                                        return 'g'   # 54% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'q'   # 89% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.girth2 > 0.0001685564493527636:
                                                                    return 'g'   # 55% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'q'   # 93% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.pt_7 > 17.765625:
                                                            return 'q'   # 99% of the training jets here get this class from the formula
                                                        else:
                                                            if s['W'] - s['Z'] > 0.029632597230374813:
                                                                return 'q'   # 97% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 58% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 100% of the training jets here get this class from the formula
                                            else:
                                                if Q.e2 > 0.005391850369051099:
                                                    if Q.girth2_top3 > 0.00041964770935010165:
                                                        return 'q'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 97% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth2 > 0.0006257706845644861:
                                                return 'q'   # 88% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 69% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['W'] > 2.3965734243392944:
                                            if s['q'] - s['t'] > 0.12314491346478462:
                                                if Q.pt_5 > 34.921875:
                                                    return 'q'   # 99% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam1 > 9.8041749879485e-05:
                                                        return 'q'   # 96% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.centroid_offset > 0.0020306509686633945:
                                                            return 'q'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.sum_pt > 809.546875:
                                                                if Q.pt_5 > 20.0625:
                                                                    if s['q'] - s['Z'] > 2.447053074836731:
                                                                        return 'q'   # 96% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.pt_4 > 35.15625:
                                                                            return 'q'   # 81% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'Z'   # 68% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 52% of the training jets here get this class from the formula
                                                            else:
                                                                if s['q'] - s['t'] > 2.780988097190857:
                                                                    return 'Z'   # 75% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'q'   # 74% of the training jets here get this class from the formula
                                            else:
                                                if Q.sum_pt_top5 > 558.0625:
                                                    return 'q'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 63% of the training jets here get this class from the formula
                                        else:
                                            if Q.lam1 > 3.28901569446316e-05:
                                                if Q.centroid_offset > 0.0018252914305776358:
                                                    return 'q'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    if Q.pt_5 > 44.375:
                                                        return 'q'   # 90% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.log_sum_pt > 6.651950120925903:
                                                            return 'q'   # 85% of the training jets here get this class from the formula
                                                        else:
                                                            if s['W'] - s['t'] > 0.9488333165645599:
                                                                return 'Z'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 52% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['t'] > 3.8808562755584717:
                                                    if Q.pt_4 > 51.453125:
                                                        return 'q'   # 98% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    if Q.pt_4 > 78.15625:
                                                        return 'q'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        if s['W'] - s['t'] > 0.7005959451198578:
                                                            return 'Z'   # 80% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 52% of the training jets here get this class from the formula
                            else:
                                if Q.girth2 > 0.002147036953829229:
                                    if s['q'] - s['Z'] > 1.0637547373771667:
                                        if Q.e2 > 0.026992528699338436:
                                            return 'W'   # 66% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 78% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 72% of the training jets here get this class from the formula
                                else:
                                    if Q.C2 > 0.06364477798342705:
                                        if Q.LHA > 0.14331483095884323:
                                            return 'W'   # 72% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 77% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['Z'] > 0.5833749175071716:
                                            if Q.lam2 > 5.596087248704862e-05:
                                                if Q.max_dr > 0.12514539808034897:
                                                    if s['q'] - s['Z'] > 0.7134610712528229:
                                                        return 'q'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 92% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 94% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth2 > 0.00035271779051981866:
                                                if Q.LHA > 0.15986944735050201:
                                                    if Q.C2 > 0.020293031819164753:
                                                        if Q.mass > 18.156840324401855:
                                                            if Q.mass > 25.90733528137207:
                                                                return 'W'   # 58% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 89% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 76% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 89% of the training jets here get this class from the formula
                                                else:
                                                    if Q.min_pair_mass > 0.5132643282413483:
                                                        return 'W'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 59% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 96% of the training jets here get this class from the formula
                    else:
                        if s['q'] - s['t'] > -0.3808138519525528:
                            if Q.D2 > 0.5991449058055878:
                                if Q.pt_5 > 21.8515625:
                                    return 't'   # 80% of the training jets here get this class from the formula
                                else:
                                    return 'q'   # 55% of the training jets here get this class from the formula
                            else:
                                return 'W'   # 55% of the training jets here get this class from the formula
                        else:
                            return 't'   # 97% of the training jets here get this class from the formula
                else:
                    if s['q'] - s['W'] > -0.39719824492931366:
                        if s['q'] - s['Z'] > 0.8748576939105988:
                            if Q.girth > 0.04558306746184826:
                                if Q.girth > 0.05426567606627941:
                                    return 'W'   # 86% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > -0.06744405627250671:
                                        return 'g'   # 56% of the training jets here get this class from the formula
                                    else:
                                        if Q.eccentricity > 0.9898533523082733:
                                            return 'q'   # 60% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 68% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['q'] > -0.1207842119038105:
                                    return 'g'   # 43% of the training jets here get this class from the formula
                                else:
                                    if Q.max_dr > 0.2556522339582443:
                                        return 'W'   # 58% of the training jets here get this class from the formula
                                    else:
                                        return 'q'   # 80% of the training jets here get this class from the formula
                        else:
                            if s['q'] - s['W'] > -0.12773296982049942:
                                if Q.girth > 0.018301931209862232:
                                    if Q.lam1 > 0.0020836694166064262:
                                        return 'W'   # 86% of the training jets here get this class from the formula
                                    else:
                                        if s['Z'] - s['t'] > 2.1653246879577637:
                                            if Q.C2 > 0.009952094405889511:
                                                if s['q'] - s['Z'] > 0.47379952669143677:
                                                    return 'q'   # 61% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 74% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 100% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass > 31.257763862609863:
                                                return 'W'   # 60% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_top5 > 0.8464375436306:
                                                    return 'q'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 54% of the training jets here get this class from the formula
                                else:
                                    return 'q'   # 69% of the training jets here get this class from the formula
                            else:
                                if Q.width > 0.002055217162705958:
                                    return 'W'   # 86% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['Z'] > 0.8801224529743195:
                                        if Q.eccentricity > 0.858977735042572:
                                            return 'q'   # 66% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 79% of the training jets here get this class from the formula
                                    else:
                                        if Q.girth2_top2 > 0.0006343194690998644:
                                            if Q.mean_eta2 > 0.00039114859828259796:
                                                return 'W'   # 72% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 63% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth > 0.01811805833131075:
                                                return 'W'   # 84% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['t'] > 3.1598308086395264:
                                                    return 'W'   # 89% of the training jets here get this class from the formula
                                                else:
                                                    if Q.C2 > 0.007688478566706181:
                                                        return 'q'   # 58% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.max_dr > 0.021408473141491413:
                                                            return 'W'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 62% of the training jets here get this class from the formula
                    else:
                        if s['W'] - s['t'] > -0.16732945293188095:
                            if s['q'] - s['Z'] > 0.9360299706459045:
                                if Q.sum_pt_top5 > 664.671875:
                                    if Q.girth > 0.047737833112478256:
                                        return 'W'   # 92% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['W'] > -0.6997597515583038:
                                            return 'q'   # 71% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 58% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 88% of the training jets here get this class from the formula
                            else:
                                if Q.width > 0.0019322876469232142:
                                    return 'W'   # 98% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['t'] > 3.1450403928756714:
                                        return 'W'   # 94% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['W'] > -0.6649230122566223:
                                            if Q.eccentricity > 0.9706512689590454:
                                                if Q.girth2_top2 > 0.0005740120250266045:
                                                    return 'q'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 69% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 85% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 92% of the training jets here get this class from the formula
                        else:
                            return 't'   # 84% of the training jets here get this class from the formula
        else:
            if s['W'] - s['Z'] > 0.026637978851795197:
                if s['g'] - s['W'] > 0.04005148261785507:
                    if s['g'] - s['W'] > 0.2689172327518463:
                        if s['g'] - s['t'] > -0.07147495821118355:
                            if Q.mass > 52.468828201293945:
                                if Q.D2 > 0.5329417884349823:
                                    return 'g'   # 78% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 71% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['W'] > 0.396686315536499:
                                    if Q.mass > 28.427733421325684:
                                        if s['g'] - s['W'] > 0.7354211211204529:
                                            return 'g'   # 98% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.008058912586420774:
                                                return 'g'   # 90% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_4 > 0.10328696668148041:
                                                    return 'W'   # 62% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 80% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 99% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.00548038468696177:
                                        if Q.tau21 > 0.11342733725905418:
                                            if Q.centroid_offset > 0.020625798031687737:
                                                return 'g'   # 93% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['q'] > 1.0744790434837341:
                                                    return 'g'   # 88% of the training jets here get this class from the formula
                                                else:
                                                    if Q.girth2 > 0.0003580924967536703:
                                                        if s['g'] - s['Z'] > 0.9232453405857086:
                                                            return 'g'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 51% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 95% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 60% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 72% of the training jets here get this class from the formula
                        else:
                            return 't'   # 95% of the training jets here get this class from the formula
                    else:
                        if s['q'] - s['t'] > 1.486577033996582:
                            if s['g'] - s['W'] > 0.13984449952840805:
                                if Q.pt_7 > 42.640625:
                                    if s['W'] - s['Z'] > 0.4818410873413086:
                                        if s['q'] - s['W'] > -0.9040324985980988:
                                            return 'W'   # 53% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 91% of the training jets here get this class from the formula
                                    else:
                                        if Q.e2_sq > 8.398190766456537e-05:
                                            return 'g'   # 74% of the training jets here get this class from the formula
                                        else:
                                            if Q.pt_2 > 96.09375:
                                                return 'W'   # 81% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 59% of the training jets here get this class from the formula
                                else:
                                    if Q.mass > 11.128814697265625:
                                        if Q.sum_pt > 901.421875:
                                            return 'g'   # 85% of the training jets here get this class from the formula
                                        else:
                                            if Q.e2 > 0.009933839552104473:
                                                return 'g'   # 67% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 72% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 83% of the training jets here get this class from the formula
                            else:
                                if Q.z_7 > 0.053746387362480164:
                                    if s['q'] - s['W'] > -1.3947017788887024:
                                        return 'W'   # 88% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 55% of the training jets here get this class from the formula
                                else:
                                    if Q.mass > 4.709384918212891:
                                        if Q.max_dr > 0.03175518848001957:
                                            if Q.eta_0 > -0.0177764892578125:
                                                if s['g'] - s['q'] > 1.0346501469612122:
                                                    return 'g'   # 85% of the training jets here get this class from the formula
                                                else:
                                                    if Q.mass > 11.035985946655273:
                                                        return 'W'   # 71% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 69% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 85% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 84% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 80% of the training jets here get this class from the formula
                        else:
                            if Q.mass > 28.430347442626953:
                                if s['g'] - s['t'] > -0.06770136393606663:
                                    if s['g'] - s['t'] > 2.2378426790237427:
                                        return 'g'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if Q.D2 > 0.5363918244838715:
                                            if Q.mass_over_sum_pt > 0.05800768546760082:
                                                if s['g'] - s['t'] > 0.7033359408378601:
                                                    if Q.z_5 > 0.08519335091114044:
                                                        return 'W'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 55% of the training jets here get this class from the formula
                                                else:
                                                    if Q.girth > 0.05784754268825054:
                                                        return 'g'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 60% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_7 > 0.053154245018959045:
                                                    return 'g'   # 75% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 56% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 88% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 89% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['Z'] > 0.39561422169208527:
                                    return 'g'   # 86% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['W'] > -1.9006134271621704:
                                        if Q.pt_6 > 50.796875:
                                            if Q.lam2 > 2.9906938834756147e-05:
                                                return 'g'   # 41% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 79% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['Z'] > 0.26171164214611053:
                                                return 'g'   # 74% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 43% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 90% of the training jets here get this class from the formula
                else:
                    if s['W'] - s['Z'] > 0.22067313641309738:
                        if s['g'] - s['W'] > -0.3722715377807617:
                            if s['g'] - s['t'] > -0.1262553259730339:
                                if s['g'] - s['q'] > 1.1193780899047852:
                                    if Q.mass_over_sum_pt_sq > 0.0030916351824998856:
                                        if Q.mass > 28.079474449157715:
                                            return 'W'   # 88% of the training jets here get this class from the formula
                                        else:
                                            if s['Z'] - s['t'] > 0.21547650545835495:
                                                if Q.phi_1 > 0.0167236328125:
                                                    return 'g'   # 63% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 81% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 84% of the training jets here get this class from the formula
                                    else:
                                        if Q.C2 > 0.014476768672466278:
                                            if Q.eccentricity > 0.9796976149082184:
                                                if s['g'] - s['q'] > 1.735702931880951:
                                                    if Q.mass > 42.27568244934082:
                                                        return 'W'   # 74% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 64% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 81% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_dr_0p1_0p2 > 0.06147386133670807:
                                                    if Q.mass > 29.300637245178223:
                                                        if s['g'] - s['Z'] > 1.1737569570541382:
                                                            return 'g'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 76% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['q'] > 1.549379050731659:
                                                            return 'g'   # 79% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.lam2 > 0.0001724924150039442:
                                                                return 'g'   # 60% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 90% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['Z'] > 0.47943438589572906:
                                                        return 'g'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['q'] > 1.3849610090255737:
                                                            return 'g'   # 70% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 65% of the training jets here get this class from the formula
                                        else:
                                            if Q.pt_7 > 30.296875:
                                                if Q.log_sum_pt > 6.468814134597778:
                                                    if s['g'] - s['q'] > 1.8628092408180237:
                                                        if Q.eccentricity > 0.9821124374866486:
                                                            return 'W'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 69% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.C2 > 0.008297720458358526:
                                                            if s['q'] - s['Z'] > -1.3297259211540222:
                                                                if s['g'] - s['W'] > -0.11999531835317612:
                                                                    if Q.min_pair_mass > 0.5778475701808929:
                                                                        return 'W'   # 77% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'g'   # 64% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 89% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 44% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam1 > 0.0011152058141306043:
                                                        if s['g'] - s['Z'] > 0.4085191935300827:
                                                            return 'g'   # 62% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 93% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 82% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['W'] > -0.1032402478158474:
                                        if Q.pt_7 > 32.703125:
                                            if Q.sum_pt > 663.359375:
                                                if Q.max_dr > 0.0449515413492918:
                                                    if s['g'] - s['Z'] > 0.4988355189561844:
                                                        return 'g'   # 50% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 88% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 92% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_dr_0_0p05 > 0.9416386187076569:
                                                    if Q.log_sum_pt > 6.471693992614746:
                                                        return 'W'   # 68% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['Z'] > 0.9445068836212158:
                                                        return 'g'   # 49% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 93% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass > 12.805385112762451:
                                                if s['g'] - s['q'] > 0.7379094064235687:
                                                    if Q.C2 > 0.039979616180062294:
                                                        return 'W'   # 70% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 69% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 87% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 73% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['Z'] > 0.6603683531284332:
                                            if Q.max_dr > 0.06414783000946045:
                                                return 'W'   # 81% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 59% of the training jets here get this class from the formula
                                        else:
                                            if Q.sum_pt_top5 > 930.203125:
                                                return 'g'   # 53% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 93% of the training jets here get this class from the formula
                            else:
                                return 't'   # 84% of the training jets here get this class from the formula
                        else:
                            if s['W'] - s['t'] > -0.01209290325641632:
                                if s['W'] - s['Z'] > 0.37163206934928894:
                                    if s['g'] - s['W'] > -0.7380642592906952:
                                        if s['g'] - s['q'] > 1.378185510635376:
                                            if Q.mass_over_sum_pt > 0.04449912905693054:
                                                if s['W'] - s['t'] > 0.5209825932979584:
                                                    if s['g'] - s['t'] > 2.248891830444336:
                                                        return 'W'   # 61% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.mass > 29.665539741516113:
                                                            return 'W'   # 98% of the training jets here get this class from the formula
                                                        else:
                                                            if s['W'] - s['Z'] > 1.2198882102966309:
                                                                return 'g'   # 56% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 44% of the training jets here get this class from the formula
                                            else:
                                                if Q.lam2 > 3.047753853024915e-05:
                                                    if s['g'] - s['Z'] > 0.19972878694534302:
                                                        return 'g'   # 66% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 64% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 86% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['t'] > -1.3090546131134033:
                                                if Q.sum_pt > 1007.5390625:
                                                    if Q.max_dr > 0.06001468375325203:
                                                        return 'W'   # 90% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 95% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 64% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['t'] > 0.49663953483104706:
                                            return 'W'   # 100% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_dr_0p05_0p1 > 0.19610107690095901:
                                                return 'W'   # 97% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['Z'] > 0.018937858752906322:
                                                    return 't'   # 56% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 85% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 1.1093494892120361:
                                        if Q.centroid_offset > 0.033478306606411934:
                                            if Q.max_dr > 0.08958233892917633:
                                                return 'W'   # 80% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 73% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 84% of the training jets here get this class from the formula
                                    else:
                                        if Q.lam1 > 0.0007058207702357322:
                                            if s['W'] - s['Z'] > 0.29279300570487976:
                                                return 'W'   # 94% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['t'] > 1.7063658833503723:
                                                    return 'W'   # 73% of the training jets here get this class from the formula
                                                else:
                                                    if Q.C2 > 0.04979691095650196:
                                                        if Q.sum_pt_top5 > 853.5546875:
                                                            if Q.girth > 0.031469373032450676:
                                                                return 'Z'   # 64% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 77% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.LHA > 0.20085058361291885:
                                                                if Q.planar_flow > 0.048844294622540474:
                                                                    return 'W'   # 82% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 58% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 95% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 91% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 97% of the training jets here get this class from the formula
                            else:
                                if s['W'] - s['t'] > -0.26704439520835876:
                                    if Q.n_dr_0p05_0p1 > 4.5:
                                        return 'W'   # 69% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 68% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 91% of the training jets here get this class from the formula
                    else:
                        if Q.girth > 0.024931428022682667:
                            if s['W'] - s['Z'] > 0.1395210400223732:
                                if s['Z'] - s['t'] > -0.1790095716714859:
                                    if s['g'] - s['q'] > 0.9934217929840088:
                                        if Q.girth2_top2 > 0.001301172305829823:
                                            if Q.centroid_offset > 0.013697025366127491:
                                                if Q.mass > 25.321358680725098:
                                                    return 'W'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['Z'] > -0.1177532710134983:
                                                        return 'W'   # 61% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 68% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['t'] > -0.46202731132507324:
                                                    if Q.lam1 > 0.004689516965299845:
                                                        return 'Z'   # 60% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 80% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 86% of the training jets here get this class from the formula
                                        else:
                                            if Q.LHA > 0.18124902248382568:
                                                return 'Z'   # 51% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 88% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['W'] > -0.18140850216150284:
                                            return 'W'   # 48% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_5 > 0.016718421131372452:
                                                if Q.lam2 > 6.948134569029207e-06:
                                                    if Q.max_dr > 0.15709882974624634:
                                                        if Q.sum_pt_top5 > 622.453125:
                                                            if Q.centroid_offset > 0.011093112174421549:
                                                                if Q.mass > 47.01471710205078:
                                                                    if Q.D2 > 3.860640287399292:
                                                                        return 'Z'   # 68% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.girth2_top3 > 0.0016260690754279494:
                                                                            if Q.z_dr_0p1_0p2 > 0.12759823352098465:
                                                                                return 'W'   # 86% of the training jets here get this class from the formula
                                                                            else:
                                                                                return 'Z'   # 65% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'W'   # 82% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 84% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 90% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.lam2 > 9.738136941450648e-05:
                                                                return 'W'   # 79% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.tau21 > 0.13121438771486282:
                                                                    if Q.centroid_offset > 0.01384958066046238:
                                                                        return 'Z'   # 71% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 76% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 79% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.sum_pt_top2 > 365.8125:
                                                            if s['g'] - s['t'] > -2.5830382108688354:
                                                                if Q.centroid_offset > 0.026374281384050846:
                                                                    if s['g'] - s['t'] > 2.0031466484069824:
                                                                        return 'Z'   # 73% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 77% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.centroid_offset > 0.0058634113520383835:
                                                                        return 'W'   # 88% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.e2 > 0.03944040462374687:
                                                                            return 'Z'   # 61% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'W'   # 89% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 52% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.lam2 > 0.00022256311785895377:
                                                                if Q.eta_0 > 0.015350341796875:
                                                                    return 'W'   # 90% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.sum_pt_top2 > 296.3125:
                                                                        return 'W'   # 80% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 55% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 91% of the training jets here get this class from the formula
                                                else:
                                                    if Q.mass > 3.5394190549850464:
                                                        return 'W'   # 70% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 68% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 61% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 58% of the training jets here get this class from the formula
                            else:
                                if Q.z_dr_0_0p05 > 0.9475665390491486:
                                    if s['q'] - s['Z'] > -0.926494687795639:
                                        if Q.eccentricity > 0.9906933903694153:
                                            return 'Z'   # 67% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > -0.024502288084477186:
                                                return 'q'   # 67% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass_over_sum_pt > 0.043124448508024216:
                                                    return 'Z'   # 55% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.025801248848438263:
                                                        if Q.eccentricity > 0.9631415903568268:
                                                            return 'W'   # 84% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.girth2_top2 > 0.0008412378665525466:
                                                                return 'W'   # 63% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 89% of the training jets here get this class from the formula
                                    else:
                                        if Q.centroid_offset > 0.026338830590248108:
                                            if Q.D2 > 3.0536540746688843:
                                                return 'W'   # 79% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 81% of the training jets here get this class from the formula
                                        else:
                                            if Q.D2 > 1.2918824553489685:
                                                if Q.z_dr_0p1_0p2 > 0.017598354257643223:
                                                    return 'W'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    if Q.dr_7 > 0.023792637512087822:
                                                        if s['W'] - s['Z'] > 0.09652187302708626:
                                                            return 'W'   # 50% of the training jets here get this class from the formula
                                                        else:
                                                            if s['q'] - s['Z'] > -1.1330690383911133:
                                                                return 'W'   # 56% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.C2 > 0.01169340219348669:
                                                                    if Q.e2 > 0.009056118782609701:
                                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 71% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 91% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 59% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 80% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['t'] > -0.016677438747137785:
                                        if Q.max_dr > 0.1577567383646965:
                                            if Q.sum_pt_top3 > 447.6875:
                                                if Q.planar_flow > 0.08103286102414131:
                                                    if Q.mass_top5 > 39.34586715698242:
                                                        if Q.mean_phi > -0.005461256252601743:
                                                            return 'Z'   # 54% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.012647971510887146:
                                                        if Q.pt_5 > 60.703125:
                                                            return 'W'   # 72% of the training jets here get this class from the formula
                                                        else:
                                                            if s['W'] - s['Z'] > 0.096778254956007:
                                                                return 'W'   # 52% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.width > 0.003294603666290641:
                                                                    return 'Z'   # 76% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 54% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['t'] > 0.4937331825494766:
                                                            return 'Z'   # 71% of the training jets here get this class from the formula
                                                        else:
                                                            if s['g'] - s['t'] > -2.4064853191375732:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 73% of the training jets here get this class from the formula
                                            else:
                                                if s['Z'] - s['t'] > 0.8540021777153015:
                                                    if Q.lam2 > 6.18970807408914e-05:
                                                        if Q.log_sum_pt > 6.434634208679199:
                                                            if Q.centroid_offset > 0.014095238409936428:
                                                                return 'W'   # 76% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 59% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.m01 > 5.238145351409912:
                                                                return 'W'   # 62% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 73% of the training jets here get this class from the formula
                                                else:
                                                    if Q.mass > 37.27558135986328:
                                                        return 'W'   # 71% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 40% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.016036249697208405:
                                                if s['g'] - s['Z'] > -0.4395096153020859:
                                                    if s['q'] - s['W'] > -1.360560119152069:
                                                        return 'W'   # 75% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.C2 > 0.04068353213369846:
                                                            return 'W'   # 84% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 44% of the training jets here get this class from the formula
                                                else:
                                                    if Q.LHA > 0.29199738800525665:
                                                        return 'W'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.z_dr_0p05_0p1 > 0.8957187533378601:
                                                            if Q.pt_5 > 50.0625:
                                                                return 'Z'   # 70% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 72% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 81% of the training jets here get this class from the formula
                                            else:
                                                if Q.lam1 > 0.006718594813719392:
                                                    if Q.sum_pt_top3 > 481.078125:
                                                        return 'Z'   # 64% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    if Q.max_dr > 0.10129605233669281:
                                                        if Q.z_dr_0p05_0p1 > 0.3185413032770157:
                                                            if Q.min_pair_mass > 0.5508710741996765:
                                                                if s['W'] - s['t'] > 2.22704017162323:
                                                                    return 'W'   # 50% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.phi_7 > 0.057464599609375:
                                                                        return 'W'   # 51% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 78% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 58% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 72% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 82% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 68% of the training jets here get this class from the formula
                        else:
                            if Q.sum_pt > 1046.99609375:
                                return 'g'   # 40% of the training jets here get this class from the formula
                            else:
                                return 'W'   # 92% of the training jets here get this class from the formula
            else:
                if s['g'] - s['Z'] > -0.0531108807772398:
                    if s['g'] - s['t'] > -0.07635051384568214:
                        if s['g'] - s['Z'] > 0.22620027512311935:
                            if s['g'] - s['Z'] > 0.3933802545070648:
                                if s['g'] - s['t'] > 0.11795227229595184:
                                    return 'g'   # 98% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 1.210996925830841:
                                        return 'g'   # 77% of the training jets here get this class from the formula
                                    else:
                                        if Q.mass_over_sum_pt_sq > 0.005970794474706054:
                                            return 'g'   # 76% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass > 30.13521671295166:
                                                return 't'   # 83% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 62% of the training jets here get this class from the formula
                            else:
                                if Q.e2_sq > 0.00034913951822090894:
                                    if Q.eccentricity > 0.971128523349762:
                                        if s['W'] - s['t'] > -2.9092363119125366:
                                            if Q.centroid_offset > 0.0401003323495388:
                                                return 'Z'   # 63% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 34.26426696777344:
                                                    return 'Z'   # 50% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 72% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 76% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['t'] > 0.11865604296326637:
                                            if Q.C2 > 0.01689105946570635:
                                                return 'g'   # 85% of the training jets here get this class from the formula
                                            else:
                                                if Q.centroid_offset > 0.03807198256254196:
                                                    return 'Z'   # 51% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 68% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 50% of the training jets here get this class from the formula
                                else:
                                    if Q.pt_0 > 122.4375:
                                        return 'g'   # 91% of the training jets here get this class from the formula
                                    else:
                                        if Q.mass_over_sum_pt > 0.01086984109133482:
                                            return 'g'   # 92% of the training jets here get this class from the formula
                                        else:
                                            if Q.eccentricity > 0.9687760174274445:
                                                return 'g'   # 68% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 69% of the training jets here get this class from the formula
                        else:
                            if Q.sum_pt > 670.3671875:
                                if s['g'] - s['W'] > 0.3105045557022095:
                                    if Q.mass > 34.742998123168945:
                                        if s['g'] - s['W'] > 3.213138222694397:
                                            return 'g'   # 77% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 56% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['q'] > 0.15579868853092194:
                                            if s['q'] - s['t'] > 0.4306930601596832:
                                                if Q.log_sum_pt > 6.5576653480529785:
                                                    return 'g'   # 92% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 72% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 98% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 40% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.024494532495737076:
                                        if s['q'] - s['W'] > -1.9045048952102661:
                                            if Q.z_top5 > 0.8149221539497375:
                                                return 'g'   # 37% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 84% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 73% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['Z'] > -0.07061299681663513:
                                            return 'W'   # 76% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 69% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['Z'] > 0.12547928094863892:
                                    if s['W'] - s['Z'] > -0.02649408672004938:
                                        return 'W'   # 47% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['t'] > -0.004946038243360817:
                                            if Q.D2 > 1.5120041966438293:
                                                if Q.centroid_offset > 0.023880161345005035:
                                                    return 'g'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 57% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt_2 > 66.78125:
                                                    if Q.z_dr_0p05_0p1 > 0.31704311072826385:
                                                        return 'Z'   # 73% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.girth2_top2 > 0.001768330461345613:
                                                            return 'g'   # 76% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.pt_6 > 48.390625:
                                                                return 'Z'   # 77% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 56% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 67% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 50% of the training jets here get this class from the formula
                                else:
                                    if Q.mass > 18.598644256591797:
                                        if Q.sum_pt_top5 > 268.25:
                                            if s['g'] - s['W'] > 0.1476311758160591:
                                                if Q.tau32 > 0.2586299926042557:
                                                    if Q.dr_6 > 0.061361437663435936:
                                                        if Q.n_pt_above_50 > 3.5:
                                                            return 'Z'   # 68% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 57% of the training jets here get this class from the formula
                                                    else:
                                                        if s['Z'] - s['t'] > 0.38833776116371155:
                                                            if Q.z_dr_0p05_0p1 > 0.2863183617591858:
                                                                if Q.pt_2 > 70.15625:
                                                                    return 'Z'   # 84% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 51% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 60% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 84% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 42% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if Q.LHA > 0.1997031345963478:
                                            if Q.centroid_offset > 0.044140493497252464:
                                                if Q.D2 > 1.4410406351089478:
                                                    return 'g'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 73% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['q'] > 1.5805070400238037:
                                                    if Q.tau21 > 0.44991785287857056:
                                                        return 'g'   # 54% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 83% of the training jets here get this class from the formula
                                        else:
                                            if Q.planar_flow > 0.1238895133137703:
                                                return 'Z'   # 62% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 77% of the training jets here get this class from the formula
                    else:
                        if s['g'] - s['t'] > -0.18441350013017654:
                            if Q.log_sum_pt > 6.426108121871948:
                                return 'g'   # 65% of the training jets here get this class from the formula
                            else:
                                if Q.max_pair_mass > 11.920351505279541:
                                    return 't'   # 84% of the training jets here get this class from the formula
                                else:
                                    if Q.log_sum_pt > 6.0905492305755615:
                                        if Q.mass > 42.54539489746094:
                                            return 'g'   # 53% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['t'] > -0.10062967240810394:
                                                return 'g'   # 44% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 82% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 59% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['t'] > -0.41190506517887115:
                                if Q.C2 > 0.07834212854504585:
                                    return 'g'   # 53% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 87% of the training jets here get this class from the formula
                            else:
                                return 't'   # 99% of the training jets here get this class from the formula
                else:
                    if s['Z'] - s['t'] > 0.013403811492025852:
                        if s['W'] - s['Z'] > -0.20206943154335022:
                            if Q.girth > 0.02471283543854952:
                                if Q.z_dr_0_0p05 > 0.9384433627128601:
                                    if Q.centroid_offset > 0.025852431543171406:
                                        if Q.mass > 17.638710975646973:
                                            if s['q'] - s['t'] > 0.6694166660308838:
                                                if Q.lam2 > 3.7250709283398464e-05:
                                                    return 'Z'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 80% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > -0.38221175968647003:
                                                if s['q'] - s['Z'] > -0.026944559067487717:
                                                    return 'q'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 70% of the training jets here get this class from the formula
                                            else:
                                                if s['W'] - s['Z'] > -0.03661062754690647:
                                                    if s['q'] - s['Z'] > -1.2515283823013306:
                                                        if Q.sum_pt_top3 > 405.9375:
                                                            return 'Z'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.LHA > 0.19913088530302048:
                                                                return 'Z'   # 84% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 66% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 96% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 97% of the training jets here get this class from the formula
                                    else:
                                        if Q.lam1 > 0.002144438214600086:
                                            if Q.centroid_offset > 0.013016424141824245:
                                                if Q.max_dr > 0.19574104994535446:
                                                    return 'Z'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 56% of the training jets here get this class from the formula
                                            else:
                                                if Q.LHA > 0.19687070697546005:
                                                    return 'W'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    if Q.tau32 > 0.43362459540367126:
                                                        return 'Z'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 60% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass > 12.768070697784424:
                                                if s['q'] - s['W'] > -0.1811339184641838:
                                                    return 'q'   # 45% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 75% of the training jets here get this class from the formula
                                            else:
                                                if Q.sum_pt > 839.4375:
                                                    return 'Z'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.girth > 0.02551064547151327:
                                                        if s['g'] - s['t'] > 2.0343018770217896:
                                                            return 'Z'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 52% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['t'] > 2.3197779655456543:
                                                            return 'Z'   # 52% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 86% of the training jets here get this class from the formula
                                else:
                                    if Q.max_dr > 0.11992919817566872:
                                        if s['W'] - s['Z'] > -0.05686246603727341:
                                            if s['q'] - s['t'] > 0.02173346746712923:
                                                if Q.z_dr_0p1_0p2 > 0.04371585696935654:
                                                    return 'W'   # 73% of the training jets here get this class from the formula
                                                else:
                                                    if Q.planar_flow > 0.025808468461036682:
                                                        if Q.tau21 > 0.33898232877254486:
                                                            return 'W'   # 60% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 74% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 76% of the training jets here get this class from the formula
                                            else:
                                                if Q.centroid_offset > 0.028427762910723686:
                                                    return 'W'   # 74% of the training jets here get this class from the formula
                                                else:
                                                    if Q.girth2_top2 > 0.0008230918901972473:
                                                        if Q.D2 > 1.3540594577789307:
                                                            if Q.eccentricity > 0.9772657752037048:
                                                                return 'Z'   # 90% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.sum_pt_top5 > 523.4375:
                                                                    if Q.mass_over_sum_pt > 0.06335319206118584:
                                                                        return 'Z'   # 60% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 74% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 84% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.z_dr_0p05_0p1 > 0.39743049442768097:
                                                                if Q.mass > 50.88765525817871:
                                                                    return 'Z'   # 82% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.max_dr > 0.14441519975662231:
                                                                        return 'Z'   # 97% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.pt_2 > 69.03125:
                                                                            return 'W'   # 70% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'Z'   # 70% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.max_dr > 0.1519239991903305:
                                                                    if Q.centroid_offset > 0.011910602916032076:
                                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.z_dr_0p05_0p1 > 0.055711496621370316:
                                                                            return 'Z'   # 77% of the training jets here get this class from the formula
                                                                        else:
                                                                            if Q.pt1_dr01 > 0.7229156196117401:
                                                                                return 'W'   # 75% of the training jets here get this class from the formula
                                                                            else:
                                                                                return 'Z'   # 61% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.mass_top5 > 49.11003303527832:
                                                                        return 'Z'   # 53% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.pt_0 > 251.125:
                                                            return 'W'   # 84% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 51% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.02820505015552044:
                                                if Q.z_7 > 0.06702465564012527:
                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    if Q.C2 > 0.041598349809646606:
                                                        return 'W'   # 62% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.sum_pt > 726.546875:
                                                            return 'W'   # 64% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 74% of the training jets here get this class from the formula
                                            else:
                                                if Q.lam1 > 0.006694400683045387:
                                                    if Q.LHA > 0.298184797167778:
                                                        return 'Z'   # 64% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 80% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam1 > 0.0028530251001939178:
                                                        if s['W'] - s['Z'] > -0.12614744156599045:
                                                            if s['q'] - s['t'] > 0.10641225427389145:
                                                                if Q.e2 > 0.018066665157675743:
                                                                    if Q.mass_over_sum_pt > 0.06047982536256313:
                                                                        if Q.max_dr > 0.20955249667167664:
                                                                            return 'W'   # 62% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'Z'   # 84% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 79% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 78% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.z_4 > 0.09796744585037231:
                                                                    if Q.D2 > 1.1679781079292297:
                                                                        return 'Z'   # 78% of the training jets here get this class from the formula
                                                                    else:
                                                                        if s['g'] - s['W'] > -2.7015336751937866:
                                                                            return 'W'   # 60% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'Z'   # 81% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.max_dr > 0.2194223329424858:
                                                                        return 'W'   # 50% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 80% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.z_dr_0p1_0p2 > 0.07624435052275658:
                                                            return 'W'   # 85% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 62% of the training jets here get this class from the formula
                                    else:
                                        if Q.mass_top5 > 45.87975311279297:
                                            if Q.centroid_offset > 0.00537285185419023:
                                                if Q.dr_0 > 0.07526162639260292:
                                                    if Q.dr_0 > 0.08962121605873108:
                                                        if Q.pt_0 > 209.0625:
                                                            return 'W'   # 62% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.min_pair_mass > 1.189920961856842:
                                                            return 'Z'   # 52% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 86% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam1 > 0.0060819576028734446:
                                                        return 'Z'   # 85% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['Z'] > -2.7328449487686157:
                                                            return 'Z'   # 78% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 74% of the training jets here get this class from the formula
                                            else:
                                                if Q.max_dr > 0.089454285800457:
                                                    return 'Z'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 56% of the training jets here get this class from the formula
                                        else:
                                            if Q.planar_flow > 0.07868412882089615:
                                                if Q.C2 > 0.023290611803531647:
                                                    if Q.e2_sq > 0.006288266973569989:
                                                        if Q.z_dr_0p05_0p1 > 0.9103898704051971:
                                                            return 'W'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 76% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.girth2 > 0.0042065707966685295:
                                                            return 'W'   # 85% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.centroid_offset > 0.032190343365073204:
                                                                return 'Z'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 69% of the training jets here get this class from the formula
                                                else:
                                                    if Q.pt_7 > 31.578125:
                                                        if s['W'] - s['Z'] > -0.02098577283322811:
                                                            if Q.centroid_offset > 0.027942704036831856:
                                                                return 'Z'   # 73% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 67% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.LHA > 0.24668684601783752:
                                                            return 'Z'   # 60% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 74% of the training jets here get this class from the formula
                                            else:
                                                if Q.sum_pt_top5 > 544.90625:
                                                    if Q.e2_sq > 0.005564053310081363:
                                                        if Q.max_dr > 0.09878723323345184:
                                                            return 'Z'   # 87% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.centroid_offset > 0.03349321149289608:
                                                            return 'Z'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    if Q.width > 0.004138357471674681:
                                                        return 'W'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 64% of the training jets here get this class from the formula
                            else:
                                if Q.max_dr > 0.036229534074664116:
                                    if Q.sum_pt > 849.390625:
                                        if Q.z_dr_0_0p05 > 0.977851152420044:
                                            return 'Z'   # 73% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 59% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 71% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['Z'] > -1.663218915462494:
                                        if Q.eccentricity > 0.9701389670372009:
                                            return 'W'   # 95% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_7 > 0.027131357230246067:
                                                return 'W'   # 96% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 52% of the training jets here get this class from the formula
                                    else:
                                        if Q.girth > 0.023551386781036854:
                                            if s['W'] - s['Z'] > -0.11640099063515663:
                                                return 'W'   # 63% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 86% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 83% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['Z'] > -0.36789292097091675:
                                if Q.log_sum_pt > 6.528996706008911:
                                    if s['g'] - s['W'] > 0.3045271039009094:
                                        if Q.pt_7 > 29.4140625:
                                            if Q.centroid_offset > 0.013512490317225456:
                                                if s['g'] - s['Z'] > -0.2247096449136734:
                                                    return 'g'   # 81% of the training jets here get this class from the formula
                                                else:
                                                    if Q.max_dr > 0.20683623105287552:
                                                        return 'g'   # 88% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.mass_over_sum_pt_sq > 0.0001325896300841123:
                                                            if Q.sum_pt_top2 > 404.03125:
                                                                return 'g'   # 64% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 84% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 68% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 70% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > -0.0896940529346466:
                                                return 'Z'   # 72% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 59% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['q'] > 1.9004867672920227:
                                            if Q.planar_flow > 0.05692688561975956:
                                                if Q.mean_eta2 > 0.0004393351264297962:
                                                    return 'Z'   # 55% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 71% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 88% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > -0.009822537656873465:
                                                return 'Z'   # 85% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 42% of the training jets here get this class from the formula
                                else:
                                    if Q.girth2 > 0.0018812348134815693:
                                        if Q.log_sum_pt > 6.475047588348389:
                                            if s['W'] - s['t'] > 0.25522930920124054:
                                                return 'Z'   # 77% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 57% of the training jets here get this class from the formula
                                        else:
                                            if Q.sum_pt_top2 > 123.109375:
                                                return 'Z'   # 82% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 71% of the training jets here get this class from the formula
                                    else:
                                        return 'Z'   # 95% of the training jets here get this class from the formula
                            else:
                                if s['Z'] - s['t'] > 0.28869597613811493:
                                    if s['q'] - s['Z'] > -0.31877903640270233:
                                        if s['q'] - s['W'] > 2.024377703666687:
                                            if Q.e2 > 0.021590126678347588:
                                                return 'Z'   # 54% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 85% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > 0.048522504046559334:
                                                return 'q'   # 73% of the training jets here get this class from the formula
                                            else:
                                                if s['W'] - s['t'] > 0.3423160910606384:
                                                    if Q.centroid_offset > 0.02471670974045992:
                                                        return 'Z'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.z_dr_0p2_0p4 > 0.010878493078052998:
                                                            return 'Z'   # 79% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 57% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['Z'] > -0.18273234367370605:
                                                        return 'q'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 71% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['Z'] > -0.4080776870250702:
                                            if Q.dr_0 > 0.058807481080293655:
                                                if Q.mass > 57.48923873901367:
                                                    return 'Z'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    if Q.max_dr > 0.10340021550655365:
                                                        if Q.eccentricity > 0.9933585822582245:
                                                            if Q.sum_pt_top3 > 340.875:
                                                                if Q.girth > 0.07256478443741798:
                                                                    return 'Z'   # 95% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 50% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.girth2 > 0.006763514596968889:
                                                                    return 'W'   # 93% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 62% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.width > 0.0044776019640266895:
                                                                return 'Z'   # 84% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 62% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.planar_flow > 0.08132646232843399:
                                                            if Q.lam2 > 0.0007268510235007852:
                                                                return 'W'   # 65% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 77% of the training jets here get this class from the formula
                                                        else:
                                                            if s['g'] - s['q'] > 0.15909051895141602:
                                                                if Q.pt_0 > 109.9375:
                                                                    if Q.z_dr_0p05_0p1 > 0.9154789447784424:
                                                                        return 'W'   # 74% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 66% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 97% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 65% of the training jets here get this class from the formula
                                            else:
                                                if Q.lam1 > 0.0065904175862669945:
                                                    if s['g'] - s['W'] > -3.1296130418777466:
                                                        if Q.tau21 > 0.11227024719119072:
                                                            return 'Z'   # 65% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 77% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.planar_flow > 0.1466393917798996:
                                                        if Q.mass > 12.267364978790283:
                                                            if Q.lam2 > 0.00010570455197012052:
                                                                if Q.n_dr_0p1_0p2 > 1.5:
                                                                    if Q.D2 > 2.6737172603607178:
                                                                        return 'W'   # 63% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.centroid_offset > 0.017522905953228474:
                                                                            if s['W'] - s['t'] > 1.577512800693512:
                                                                                if s['g'] - s['q'] > 0.17780641466379166:
                                                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                                                                else:
                                                                                    return 'Z'   # 81% of the training jets here get this class from the formula
                                                                            else:
                                                                                return 'Z'   # 82% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'Z'   # 92% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 88% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.centroid_offset > 0.028950669802725315:
                                                                    return 'Z'   # 86% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 70% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 98% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.girth > 0.02473573014140129:
                                                            return 'Z'   # 95% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.log_sum_pt > 6.764638185501099:
                                                                return 'Z'   # 75% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 68% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['W'] > 4.764723777770996:
                                                if Q.e2 > 0.021442475728690624:
                                                    if s['Z'] - s['t'] > 0.6080337166786194:
                                                        if s['g'] - s['Z'] > -0.7382376790046692:
                                                            return 'g'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 93% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 48% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['q'] > -0.164058156311512:
                                                        return 'g'   # 54% of the training jets here get this class from the formula
                                                    else:
                                                        if s['Z'] - s['t'] > 1.9578841924667358:
                                                            return 'Z'   # 80% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 67% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['Z'] > -0.7686829268932343:
                                                    if s['g'] - s['q'] > 2.032541275024414:
                                                        if s['g'] - s['W'] > 3.809423804283142:
                                                            return 'g'   # 52% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['Z'] > -0.6622767150402069:
                                                        if Q.lam1 > 0.006944303633645177:
                                                            if s['g'] - s['Z'] > -3.5119001865386963:
                                                                if Q.dr_2 > 0.05755884200334549:
                                                                    if Q.mass_top5 > 35.351240158081055:
                                                                        return 'Z'   # 85% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 58% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 99% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 97% of the training jets here get this class from the formula
                                                    else:
                                                        if s['q'] - s['Z'] > -0.7952040135860443:
                                                            if s['W'] - s['t'] > -1.7989481687545776:
                                                                return 'Z'   # 96% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.e2 > 0.020351934246718884:
                                                                    return 'Z'   # 85% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.e2_sq > 0.003799562808126211:
                                                                        return 'q'   # 69% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 64% of the training jets here get this class from the formula
                                                        else:
                                                            if s['Z'] - s['t'] > 0.5369385182857513:
                                                                return 'Z'   # 100% of the training jets here get this class from the formula
                                                            else:
                                                                if s['q'] - s['W'] > 2.9944180250167847:
                                                                    if Q.LHA > 0.3285272866487503:
                                                                        return 'Z'   # 96% of the training jets here get this class from the formula
                                                                    else:
                                                                        if Q.lam1 > 0.007890125270932913:
                                                                            return 't'   # 76% of the training jets here get this class from the formula
                                                                        else:
                                                                            return 'Z'   # 76% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 96% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['W'] > 3.6398775577545166:
                                        if Q.max_dr > 0.11837000399827957:
                                            if s['q'] - s['t'] > -0.23634764552116394:
                                                return 'q'   # 56% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 75% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 77% of the training jets here get this class from the formula
                                    else:
                                        if s['Z'] - s['t'] > 0.17080078274011612:
                                            if s['W'] - s['t'] > -0.21476194262504578:
                                                if Q.z_7 > 0.05472840368747711:
                                                    return 'W'   # 57% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 83% of the training jets here get this class from the formula
                                            else:
                                                if Q.e2 > 0.019381356425583363:
                                                    if s['W'] - s['t'] > -4.947565078735352:
                                                        return 'Z'   # 88% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 54% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['Z'] > -1.8756940960884094:
                                                        return 'Z'   # 75% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 52% of the training jets here get this class from the formula
                                        else:
                                            if Q.e2 > 0.023223948664963245:
                                                if Q.tau32 > 0.44264766573905945:
                                                    if Q.z_dr_0p1_0p2 > 0.16825546324253082:
                                                        if Q.e2 > 0.041853273287415504:
                                                            return 'Z'   # 72% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.z_4 > 0.06945043802261353:
                                                                return 't'   # 55% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 70% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 86% of the training jets here get this class from the formula
                                            else:
                                                if Q.planar_flow > 0.0863359346985817:
                                                    return 't'   # 71% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 60% of the training jets here get this class from the formula
                    else:
                        if s['Z'] - s['t'] > -0.1986590251326561:
                            if Q.e2 > 0.03979584388434887:
                                if Q.z_dr_0p1_0p2 > 0.40377581119537354:
                                    return 't'   # 75% of the training jets here get this class from the formula
                                else:
                                    if Q.z_7 > 0.07280585542321205:
                                        return 'Z'   # 78% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_0 > 116.21875:
                                            if Q.lam2 > 0.00039366127748508006:
                                                return 'Z'   # 81% of the training jets here get this class from the formula
                                            else:
                                                if s['W'] - s['Z'] > -0.8608101010322571:
                                                    return 'Z'   # 54% of the training jets here get this class from the formula
                                                else:
                                                    if Q.eta_0 > -0.0615234375:
                                                        return 't'   # 58% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 75% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['W'] > 1.7975582480430603:
                                    if Q.dr_7 > 0.03574621304869652:
                                        if s['q'] - s['t'] > -0.3213927298784256:
                                            return 'q'   # 46% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 83% of the training jets here get this class from the formula
                                    else:
                                        return 'Z'   # 72% of the training jets here get this class from the formula
                                else:
                                    if Q.z_dr_0p1_0p2 > 0.19032569974660873:
                                        return 't'   # 78% of the training jets here get this class from the formula
                                    else:
                                        if Q.e2_sq > 0.0049927425570786:
                                            if Q.girth2_top3 > 0.003280209260992706:
                                                if Q.mean_eta2 > 0.005103335017338395:
                                                    return 't'   # 51% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 84% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_dr_0p2_0p4 > 0.06017386540770531:
                                                    return 'Z'   # 66% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 76% of the training jets here get this class from the formula
                                        else:
                                            if s['W'] - s['t'] > -0.38939036428928375:
                                                return 'W'   # 37% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_7 > 0.057401563972234726:
                                                    return 't'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    if s['Z'] - s['t'] > -0.0314232986420393:
                                                        return 'Z'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 62% of the training jets here get this class from the formula
                        else:
                            if s['Z'] - s['t'] > -0.4064643234014511:
                                if s['g'] - s['q'] > 0.8814189732074738:
                                    if Q.tau32 > 0.41086266934871674:
                                        return 't'   # 77% of the training jets here get this class from the formula
                                    else:
                                        return 'Z'   # 49% of the training jets here get this class from the formula
                                else:
                                    if Q.z_dr_0p05_0p1 > 0.9489601254463196:
                                        if Q.centroid_offset > 0.03501993417739868:
                                            return 't'   # 96% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 46% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 90% of the training jets here get this class from the formula
                            else:
                                return 't'   # 97% of the training jets here get this class from the formula


def classify(pt, eta, phi):
    Q = quantities(pt, eta, phi)
    return decide(Q, scores(Q))


if __name__ == '__main__':
    pt = [412.0, 230.5, 101.2, 40.3, 22.8, 10.1, 6.4, 3.3]
    eta = [0.01, -0.12, 0.25, 0.05, -0.31, 0.2, -0.05, 0.4]
    phi = [-0.02, 0.18, -0.1, 0.33, 0.07, -0.25, 0.12, -0.36]
    print('class:', classify(pt, eta, phi))
