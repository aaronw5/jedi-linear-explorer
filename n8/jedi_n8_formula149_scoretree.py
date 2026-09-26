"""JEDI-linear jet tagger, 8 particles, 3 features: the simpler version of the simplified formula: ONE tree of if-statements on the jet quantities and on differences of additive class scores.

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

Test set (50,000 jets): accuracy 64.63% (the formula: 64.64%); same class as the formula for 95.83% of jets.  872 leaves, depth 17.
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
        eccentricity=1 - lam2 / max(lam1, 1e-12),
        C2=e3 / max(e2 ** 2, 1e-12),
        D2=e3 / max(e2 ** 3, 1e-12),
        LHA=sum(z[i] * math.sqrt(dr[i] / 0.8) for i in P),
        log_sum_pt=math.log(tot),
        mass_over_sum_pt=mass_of(n) / tot,
        mass=mass_of(n),
        max_dr=max(dr[i] for i in real),
        pt_0=pt[0],
        pt_7=pt[7],
        z_7=z[7],
        planar_flow=4 * (ta * tc - tb ** 2) / max((ta + tc) ** 2, 1e-12),
        sum_pt_top5=sum(pt[:5]),
        n_dr_0p2_0p4=sum(1 for i in real if 0.2 <= dr[i] < 0.4),
        sum_pt=tot,
        z_dr_0p05_0p1=sum(z[i] for i in real if 0.05 <= dr[i] < 0.1),
        z_dr_0p1_0p2=sum(z[i] for i in real if 0.1 <= dr[i] < 0.2),
        z_dr_0p2_0p4=sum(z[i] for i in real if 0.2 <= dr[i] < 0.4),
        girth=sum(z[i] * dr[i] for i in P),
        girth2=sum(z[i] * dr[i] ** 2 for i in P),
        e2=e2,
        e2_sq=sum(z[i] * z[j] * dist2(i, j) for i in P for j in P if i < j),
        lam1=lam1,
        width=ta + tc,
        lam2=lam2,
        tau21=tau(2) / max(tau(1), 1e-12),
        tau32=tau(3) / max(tau(2), 1e-12),
        centroid_offset=math.hypot(sum(z[i] * eta[i] for i in P), sum(z[i] * phi[i] for i in P)),
    )


def score_g(Q):
    return (6.009
        + 17.92 * max(0.0, 0.033 - Q.centroid_offset)
        - 9.538 * max(0.0, 0.013 - Q.girth2)
        + 0.04327 * max(0.0, 29.0 - Q.mass)
        + 0.01949 * max(0.0, 74.0 - Q.mass)
        + 0.003057 * max(0.0, Q.sum_pt - 880.0)
        + 303.1 * max(0.0, 0.005 - Q.width)
        - 2103.0 * max(0.0, 0.018 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 266.6 * max(0.0, 0.0062 - Q.lam1) * max(0.0, 0.95 - Q.D2)
        - 1.336 * max(0.0, 65.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.008)
        + 0.0001839 * max(0.0, 66.0 - Q.mass) * max(0.0, 39.0 - Q.pt_7)
        + 8.115e-05 * max(0.0, Q.sum_pt - 860.0) * max(0.0, 33.0 - Q.pt_7)
        + 0.07177 * max(0.0, Q.pt_7 - 32.0)
        - 61.72 * max(0.0, 0.01 - Q.width)
        + 6530.0 * max(0.0, 0.012 - Q.lam1) * max(0.0, Q.centroid_offset - 0.018)
        - 59.2 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.028 - Q.centroid_offset)
        + 1100.0 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.0015 - Q.lam2)
        - 0.0005202 * max(0.0, Q.pt_7 - 34.0) * max(0.0, 98.0 - Q.mass)
        - 10.8 * max(0.0, Q.LHA - 0.13)
        + 42.6 * max(0.0, 0.005 - Q.lam1)
        + 1.644 * max(0.0, 6.4 - Q.log_sum_pt)
        + 0.05691 * max(0.0, Q.pt_7 - 28.0)
        + 0.0037 * max(0.0, 780.0 - Q.sum_pt)
        - 19.93 * max(0.0, Q.z_7 - 0.047)
        - 112.5 * max(0.0, 0.018 - Q.z_7)
        - 0.7342 * max(0.0, Q.pt_7 - 28.0) * max(0.0, 0.054 - Q.C2)
        - 0.2499 * max(0.0, Q.pt_7 - 28.0) * max(0.0, Q.max_dr - 0.07)
        + 2.858 * max(0.0, Q.LHA - 0.27)
        - 17.41 * max(0.0, Q.centroid_offset - 0.013)
        + 1.382 * max(0.0, 0.047 - Q.e2)
        - 61.72 * max(0.0, 0.01 - Q.girth2)
        - 13.83 * max(0.0, Q.lam1 - 0.016)
        - 6.223 * max(0.0, Q.mass_over_sum_pt - 0.071) * max(0.0, 0.55 - Q.tau32)
        - 7.575 * max(0.0, Q.C2 - 0.063)
        + 684.5 * max(0.0, 0.00042 - Q.lam2)
        + 0.003529 * max(0.0, 55.0 - Q.mass)
        - 13.09 * max(0.0, Q.mass_over_sum_pt - 0.086)
        - 0.3729 * max(0.0, 0.27 - Q.tau21)
        + 56.99 * max(0.0, Q.width - 0.0016)
        + 0.01919 * max(0.0, Q.C2 - -0.00087) * max(0.0, Q.pt_7 - 38.0)
        + 0.005342 * max(0.0, 0.26 - Q.tau21) * max(0.0, 57.0 - Q.mass)
        + 7.958 * max(0.0, 0.04 - Q.e2)
        + 20.95 * max(0.0, Q.log_sum_pt - 6.9)
        - 27.31 * max(0.0, 0.035 - Q.z_7)
        - 19.33 * max(0.0, 0.066 - Q.z_7)
        - 10.5 * max(0.0, 0.22 - Q.LHA) * max(0.0, 6.8 - Q.log_sum_pt)
        - 102100.0 * max(0.0, 0.025 - Q.e2) * max(0.0, 9.2e-05 - Q.lam2)
        - 32070.0 * max(0.0, 0.0026 - Q.width) * max(0.0, 0.021 - Q.centroid_offset)
        + 673.7 * max(0.0, 0.072 - Q.z_7) * max(0.0, 0.032 - Q.centroid_offset)
        + 23.81 * max(0.0, Q.girth - 0.09)
        + 136.1 * max(0.0, Q.lam2 - 0.0027)
        - 291.8 * max(0.0, 0.00066 - Q.lam2)
        - 44.15 * max(0.0, Q.mass_over_sum_pt - 0.0089)
        + 2.193 * Q.max_dr
        - 168.2 * max(0.0, 0.012 - Q.width)
        + 764.0 * max(0.0, Q.centroid_offset - 0.0059) * max(0.0, 0.0026 - Q.lam2)
        + 55.38 * max(0.0, 0.049 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.18)
        + 0.01526 * max(0.0, 6.5 - Q.log_sum_pt) * max(0.0, 44.0 - Q.pt_7)
        + 88.1 * max(0.0, 6.3 - Q.log_sum_pt) * max(0.0, 0.071 - Q.z_7)
        + 122.3 * max(0.0, 6.7 - Q.log_sum_pt) * max(0.0, 0.049 - Q.z_7)
        + 0.007506 * max(0.0, 42.0 - Q.mass) * max(0.0, 0.94 - Q.z_dr_0p05_0p1)
        - 3.265 * max(0.0, Q.mass_over_sum_pt - 0.015) * max(0.0, 0.55 - Q.tau32)
        - 16.23 * max(0.0, 0.038 - Q.e2)
        - 431.2 * max(0.0, 0.0011 - Q.e2_sq)
        + 18.99 * max(0.0, 0.087 - Q.girth)
        + 41.54 * max(0.0, Q.girth2 - 0.0046)
        + 0.008322 * max(0.0, Q.mass - 80.4)
        + 6.604 * max(0.0, Q.mass_over_sum_pt - 0.073)
        + 14.96 * max(0.0, Q.mass_over_sum_pt - 0.09)
        - 1.243 * max(0.0, 0.19 - Q.planar_flow)
        - 588.3 * max(0.0, 0.00069 - Q.width)
        + 187.4 * max(0.0, 0.0056 - Q.width)
        + 0.9937 * max(0.0, Q.centroid_offset - 0.031) * max(0.0, Q.pt_0 - 370.0)
        - 48.56 * max(0.0, Q.girth2 - 0.0047) * max(0.0, Q.eccentricity - 0.94)
        + 0.006324 * max(0.0, 0.18 - Q.planar_flow) * max(0.0, Q.sum_pt - 590.0)
        + 57.96 * max(0.0, 0.22 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        + 0.001694 * max(0.0, 45.0 - Q.pt_7) * max(0.0, 0.6 - Q.planar_flow)
        - 16.02 * max(0.0, 0.063 - Q.girth)
        - 56.87 * max(0.0, 0.0049 - Q.width)
        + 12210.0 * max(0.0, 0.17 - Q.LHA) * max(0.0, 0.00039 - Q.lam2)
        - 77.4 * max(0.0, 0.0051 - Q.girth2) * max(0.0, 0.54 - Q.planar_flow)
        + 1.187 * max(0.0, 20.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.015)
        - 9294.0 * max(0.0, 0.0051 - Q.width) * max(0.0, Q.centroid_offset - 0.0014)
        - 4.386 * max(0.0, 0.019 - Q.centroid_offset)
        + 217.9 * max(0.0, Q.lam2 - 0.0015)
        - 0.5442 * max(0.0, Q.log_sum_pt - 6.3)
        - 0.0642 * max(0.0, 25.0 - Q.mass)
        + 0.1152 * max(0.0, Q.n_dr_0p2_0p4 - 1.5)
        - 339.3 * max(0.0, 0.00029 - Q.width)
        + 340.4 * max(0.0, 0.0065 - Q.width)
        + 0.6075 * max(0.0, Q.girth2 - 0.019) * max(0.0, 30.0 - Q.pt_7)
        + 0.07216 * max(0.0, 56.0 - Q.mass) * max(0.0, 6.8 - Q.log_sum_pt)
        - 2003.0 * max(0.0, 0.0091 - Q.width) * max(0.0, Q.C2 - 0.026)
        - 8873.0 * max(0.0, 0.0061 - Q.width) * max(0.0, Q.centroid_offset - 0.0016)
        + 8.446 * max(0.0, Q.C2 - 0.059)
        + 4.182 * max(0.0, Q.e2 - 0.037)
        - 7.486 * max(0.0, 0.037 - Q.e2)
        - 183.6 * max(0.0, 0.0018 - Q.girth2)
        - 227.9 * max(0.0, Q.lam2 - 0.00016)
        - 0.04313 * max(0.0, 6.3 - Q.log_sum_pt)
        - 0.05573 * max(0.0, 0.34 - Q.z_dr_0p05_0p1)
        + 0.6173 * max(0.0, Q.LHA - 0.29) * max(0.0, 0.69 - Q.tau21)
        + 11.93 * max(0.0, Q.eccentricity - 0.9) * max(0.0, 0.041 - Q.z_dr_0p2_0p4)
        - 28.65 * max(0.0, Q.lam2 - 0.00022) * max(0.0, 0.52 - Q.tau21)
        + 0.9774 * max(0.0, 0.15 - Q.LHA)
        - 28.68 * max(0.0, 0.05 - Q.centroid_offset)
        + 3.4 * max(0.0, Q.girth - 0.074)
        - 15.76 * max(0.0, 0.088 - Q.girth)
        - 166.2 * max(0.0, 0.0038 - Q.width)
        - 157.9 * max(0.0, 0.0088 - Q.width)
        - 101.9 * max(0.0, 0.39 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        + 7.365 * max(0.0, Q.e2 - 0.062)
        + 0.001891 * max(0.0, Q.mass - 91.2)
        - 4.294 * max(0.0, Q.width - 0.018)
        - 7189.0 * max(0.0, Q.girth2 - 0.019) * max(0.0, Q.lam2 - 0.0016)
        - 1.545 * max(0.0, Q.C2 - 0.065)
        + 4.485 * max(0.0, 0.14 - Q.girth)
        - 0.01687 * max(0.0, Q.sum_pt - 980.0)
        - 25.08 * max(0.0, 0.15 - Q.girth) * max(0.0, 6.7 - Q.log_sum_pt)
        - 0.2567 * max(0.0, 0.15 - Q.girth) * max(0.0, 35.0 - Q.pt_7)
        - 1.816e-06 * max(0.0, Q.sum_pt_top5 - 660.0) * max(0.0, 48.0 - Q.pt_7)
        - 0.2908 * max(0.0, 0.52 - Q.tau21) * max(0.0, Q.max_dr - 0.031)
        - 2.216 * max(0.0, 0.091 - Q.girth)
        - 45.33 * max(0.0, 0.014 - Q.girth2)
        + 3.411 * max(0.0, Q.lam1 - 0.0075)
        - 0.005924 * max(0.0, 80.4 - Q.mass)
        - 0.4198 * max(0.0, 0.18 - Q.max_dr)
        + 1.722 * max(0.0, 0.0075 - Q.width)
        - 0.04158 * max(0.0, 0.64 - Q.z_dr_0p05_0p1)
        + 1426.0 * max(0.0, 0.014 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 395.2 * max(0.0, Q.lam1 - 0.0064) * max(0.0, 0.16 - Q.max_dr)
        + 33.37 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.011)
        + 23.11 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018)
        + 30.0 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, 0.17 - Q.max_dr)
        + 193.0 * max(0.0, 0.0087 - Q.width) * max(0.0, 1.0 - Q.D2)
        + 112.2 * max(0.0, 0.0083 - Q.width) * max(0.0, 6.9 - Q.log_sum_pt)
        + 247.7 * max(0.0, 0.0078 - Q.width) * max(0.0, 0.097 - Q.planar_flow)
        + 0.3963 * max(0.0, 0.63 - Q.z_dr_0p05_0p1) * max(0.0, 0.067 - Q.C2)
        - 3.673 * max(0.0, Q.LHA - 0.34)
        - 17.51 * max(0.0, 0.041 - Q.e2)
        + 136.6 * max(0.0, 0.0065 - Q.lam1)
        + 64.73 * max(0.0, 0.0081 - Q.lam1)
        - 113.9 * max(0.0, 0.0069 - Q.width)
        + 0.4985 * max(0.0, 0.31 - Q.tau21) * max(0.0, 0.68 - Q.z_dr_0p05_0p1)
        - 4.424 * max(0.0, 0.29 - Q.tau21) * max(0.0, 0.2 - Q.z_dr_0p2_0p4)
        + 279.7 * max(0.0, 0.0065 - Q.width) * max(0.0, Q.log_sum_pt - 6.9)
    )


def score_q(Q):
    return (7.082
        + 15.84 * max(0.0, 0.033 - Q.centroid_offset)
        + 3.494 * max(0.0, 0.013 - Q.girth2)
        + 0.007493 * max(0.0, 29.0 - Q.mass)
        + 0.01389 * max(0.0, 74.0 - Q.mass)
        - 0.0001133 * max(0.0, Q.sum_pt - 880.0)
        + 375.4 * max(0.0, 0.005 - Q.width)
        - 2181.0 * max(0.0, 0.018 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 145.9 * max(0.0, 0.0062 - Q.lam1) * max(0.0, 0.95 - Q.D2)
        - 1.315 * max(0.0, 65.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.008)
        + 0.0002302 * max(0.0, 66.0 - Q.mass) * max(0.0, 39.0 - Q.pt_7)
        - 5.319e-06 * max(0.0, Q.sum_pt - 860.0) * max(0.0, 33.0 - Q.pt_7)
        + 0.0347 * max(0.0, Q.pt_7 - 32.0)
        - 9.574 * max(0.0, 0.01 - Q.width)
        + 4313.0 * max(0.0, 0.012 - Q.lam1) * max(0.0, Q.centroid_offset - 0.018)
        + 107.3 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.028 - Q.centroid_offset)
        - 808.2 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.0015 - Q.lam2)
        - 0.000146 * max(0.0, Q.pt_7 - 34.0) * max(0.0, 98.0 - Q.mass)
        - 10.08 * max(0.0, Q.LHA - 0.13)
        - 62.83 * max(0.0, 0.005 - Q.lam1)
        + 0.2042 * max(0.0, 6.4 - Q.log_sum_pt)
        - 0.01599 * max(0.0, Q.pt_7 - 28.0)
        - 0.001644 * max(0.0, 780.0 - Q.sum_pt)
        - 7.023 * max(0.0, Q.z_7 - 0.047)
        + 10.1 * max(0.0, 0.018 - Q.z_7)
        - 0.07104 * max(0.0, Q.pt_7 - 28.0) * max(0.0, 0.054 - Q.C2)
        - 0.1087 * max(0.0, Q.pt_7 - 28.0) * max(0.0, Q.max_dr - 0.07)
        - 3.012 * max(0.0, Q.LHA - 0.27)
        - 18.15 * max(0.0, Q.centroid_offset - 0.013)
        + 4.287 * max(0.0, 0.047 - Q.e2)
        - 9.574 * max(0.0, 0.01 - Q.girth2)
        - 52.61 * max(0.0, Q.lam1 - 0.016)
        - 7.252 * max(0.0, Q.mass_over_sum_pt - 0.071) * max(0.0, 0.55 - Q.tau32)
        + 8.164 * max(0.0, Q.C2 - 0.063)
        + 1355.0 * max(0.0, 0.00042 - Q.lam2)
        - 0.003159 * max(0.0, 55.0 - Q.mass)
        - 4.09 * max(0.0, Q.mass_over_sum_pt - 0.086)
        - 2.139 * max(0.0, 0.27 - Q.tau21)
        - 108.4 * max(0.0, Q.width - 0.0016)
        - 0.1113 * max(0.0, Q.C2 - -0.00087) * max(0.0, Q.pt_7 - 38.0)
        + 0.05536 * max(0.0, 0.26 - Q.tau21) * max(0.0, 57.0 - Q.mass)
        - 3.855 * max(0.0, 0.04 - Q.e2)
        - 4.359 * max(0.0, Q.log_sum_pt - 6.9)
        + 28.78 * max(0.0, 0.035 - Q.z_7)
        + 4.128 * max(0.0, 0.066 - Q.z_7)
        - 44.54 * max(0.0, 0.22 - Q.LHA) * max(0.0, 6.8 - Q.log_sum_pt)
        + 49040.0 * max(0.0, 0.025 - Q.e2) * max(0.0, 9.2e-05 - Q.lam2)
        - 16720.0 * max(0.0, 0.0026 - Q.width) * max(0.0, 0.021 - Q.centroid_offset)
        - 103.9 * max(0.0, 0.072 - Q.z_7) * max(0.0, 0.032 - Q.centroid_offset)
        + 39.88 * max(0.0, Q.girth - 0.09)
        + 268.4 * max(0.0, Q.lam2 - 0.0027)
        - 467.9 * max(0.0, 0.00066 - Q.lam2)
        - 34.83 * max(0.0, Q.mass_over_sum_pt - 0.0089)
        + 2.432 * Q.max_dr
        - 193.3 * max(0.0, 0.012 - Q.width)
        - 1683.0 * max(0.0, Q.centroid_offset - 0.0059) * max(0.0, 0.0026 - Q.lam2)
        + 72.29 * max(0.0, 0.049 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.18)
        + 0.009857 * max(0.0, 6.5 - Q.log_sum_pt) * max(0.0, 44.0 - Q.pt_7)
        + 90.36 * max(0.0, 6.3 - Q.log_sum_pt) * max(0.0, 0.071 - Q.z_7)
        + 113.4 * max(0.0, 6.7 - Q.log_sum_pt) * max(0.0, 0.049 - Q.z_7)
        + 0.01101 * max(0.0, 42.0 - Q.mass) * max(0.0, 0.94 - Q.z_dr_0p05_0p1)
        - 3.388 * max(0.0, Q.mass_over_sum_pt - 0.015) * max(0.0, 0.55 - Q.tau32)
        - 15.36 * max(0.0, 0.038 - Q.e2)
        - 580.1 * max(0.0, 0.0011 - Q.e2_sq)
        + 16.18 * max(0.0, 0.087 - Q.girth)
        + 78.39 * max(0.0, Q.girth2 - 0.0046)
        - 0.0009891 * max(0.0, Q.mass - 80.4)
        - 7.304 * max(0.0, Q.mass_over_sum_pt - 0.073)
        + 18.0 * max(0.0, Q.mass_over_sum_pt - 0.09)
        - 1.092 * max(0.0, 0.19 - Q.planar_flow)
        - 470.1 * max(0.0, 0.00069 - Q.width)
        + 233.4 * max(0.0, 0.0056 - Q.width)
        + 0.9492 * max(0.0, Q.centroid_offset - 0.031) * max(0.0, Q.pt_0 - 370.0)
        - 64.98 * max(0.0, Q.girth2 - 0.0047) * max(0.0, Q.eccentricity - 0.94)
        + 0.003348 * max(0.0, 0.18 - Q.planar_flow) * max(0.0, Q.sum_pt - 590.0)
        + 48.9 * max(0.0, 0.22 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        - 0.005799 * max(0.0, 45.0 - Q.pt_7) * max(0.0, 0.6 - Q.planar_flow)
        - 12.11 * max(0.0, 0.063 - Q.girth)
        - 157.1 * max(0.0, 0.0049 - Q.width)
        - 1022.0 * max(0.0, 0.17 - Q.LHA) * max(0.0, 0.00039 - Q.lam2)
        + 9.28 * max(0.0, 0.0051 - Q.girth2) * max(0.0, 0.54 - Q.planar_flow)
        + 1.387 * max(0.0, 20.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.015)
        - 11730.0 * max(0.0, 0.0051 - Q.width) * max(0.0, Q.centroid_offset - 0.0014)
        + 6.516 * max(0.0, 0.019 - Q.centroid_offset)
        + 243.1 * max(0.0, Q.lam2 - 0.0015)
        - 1.696 * max(0.0, Q.log_sum_pt - 6.3)
        - 0.03885 * max(0.0, 25.0 - Q.mass)
        + 0.07922 * max(0.0, Q.n_dr_0p2_0p4 - 1.5)
        + 32.79 * max(0.0, 0.00029 - Q.width)
        + 324.9 * max(0.0, 0.0065 - Q.width)
        + 3.388 * max(0.0, Q.girth2 - 0.019) * max(0.0, 30.0 - Q.pt_7)
        + 0.06828 * max(0.0, 56.0 - Q.mass) * max(0.0, 6.8 - Q.log_sum_pt)
        - 3095.0 * max(0.0, 0.0091 - Q.width) * max(0.0, Q.C2 - 0.026)
        - 10950.0 * max(0.0, 0.0061 - Q.width) * max(0.0, Q.centroid_offset - 0.0016)
        + 5.349 * max(0.0, Q.C2 - 0.059)
        - 10.82 * max(0.0, Q.e2 - 0.037)
        + 8.856 * max(0.0, 0.037 - Q.e2)
        + 213.9 * max(0.0, 0.0018 - Q.girth2)
        - 258.3 * max(0.0, Q.lam2 - 0.00016)
        + 1.246 * max(0.0, 6.3 - Q.log_sum_pt)
        - 0.4389 * max(0.0, 0.34 - Q.z_dr_0p05_0p1)
        + 9.113 * max(0.0, Q.LHA - 0.29) * max(0.0, 0.69 - Q.tau21)
        - 30.45 * max(0.0, Q.eccentricity - 0.9) * max(0.0, 0.041 - Q.z_dr_0p2_0p4)
        - 474.3 * max(0.0, Q.lam2 - 0.00022) * max(0.0, 0.52 - Q.tau21)
        + 2.985 * max(0.0, 0.15 - Q.LHA)
        - 28.83 * max(0.0, 0.05 - Q.centroid_offset)
        + 8.188 * max(0.0, Q.girth - 0.074)
        - 20.83 * max(0.0, 0.088 - Q.girth)
        - 16.68 * max(0.0, 0.0038 - Q.width)
        - 157.5 * max(0.0, 0.0088 - Q.width)
        - 117.2 * max(0.0, 0.39 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        + 7.165 * max(0.0, Q.e2 - 0.062)
        - 0.001053 * max(0.0, Q.mass - 91.2)
        + 39.1 * max(0.0, Q.width - 0.018)
        - 9338.0 * max(0.0, Q.girth2 - 0.019) * max(0.0, Q.lam2 - 0.0016)
        - 17.78 * max(0.0, Q.C2 - 0.065)
        + 2.026 * max(0.0, 0.14 - Q.girth)
        + 0.005206 * max(0.0, Q.sum_pt - 980.0)
        - 17.77 * max(0.0, 0.15 - Q.girth) * max(0.0, 6.7 - Q.log_sum_pt)
        - 0.2887 * max(0.0, 0.15 - Q.girth) * max(0.0, 35.0 - Q.pt_7)
        - 2.26e-06 * max(0.0, Q.sum_pt_top5 - 660.0) * max(0.0, 48.0 - Q.pt_7)
        - 0.4338 * max(0.0, 0.52 - Q.tau21) * max(0.0, Q.max_dr - 0.031)
        - 7.93 * max(0.0, 0.091 - Q.girth)
        - 46.89 * max(0.0, 0.014 - Q.girth2)
        + 123.4 * max(0.0, Q.lam1 - 0.0075)
        + 0.005571 * max(0.0, 80.4 - Q.mass)
        + 0.3864 * max(0.0, 0.18 - Q.max_dr)
        - 50.26 * max(0.0, 0.0075 - Q.width)
        - 0.0413 * max(0.0, 0.64 - Q.z_dr_0p05_0p1)
        + 3066.0 * max(0.0, 0.014 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 278.5 * max(0.0, Q.lam1 - 0.0064) * max(0.0, 0.16 - Q.max_dr)
        + 140.3 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.011)
        - 71.22 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018)
        + 9.588 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, 0.17 - Q.max_dr)
        + 142.8 * max(0.0, 0.0087 - Q.width) * max(0.0, 1.0 - Q.D2)
        + 217.5 * max(0.0, 0.0083 - Q.width) * max(0.0, 6.9 - Q.log_sum_pt)
        - 178.9 * max(0.0, 0.0078 - Q.width) * max(0.0, 0.097 - Q.planar_flow)
        + 0.4951 * max(0.0, 0.63 - Q.z_dr_0p05_0p1) * max(0.0, 0.067 - Q.C2)
        - 5.5 * max(0.0, Q.LHA - 0.34)
        + 9.839 * max(0.0, 0.041 - Q.e2)
        + 156.6 * max(0.0, 0.0065 - Q.lam1)
        - 82.92 * max(0.0, 0.0081 - Q.lam1)
        - 183.5 * max(0.0, 0.0069 - Q.width)
        + 0.3581 * max(0.0, 0.31 - Q.tau21) * max(0.0, 0.68 - Q.z_dr_0p05_0p1)
        - 4.068 * max(0.0, 0.29 - Q.tau21) * max(0.0, 0.2 - Q.z_dr_0p2_0p4)
        - 609.7 * max(0.0, 0.0065 - Q.width) * max(0.0, Q.log_sum_pt - 6.9)
    )


def score_W(Q):
    return (-10.81
        - 73.55 * max(0.0, 0.033 - Q.centroid_offset)
        - 98.84 * max(0.0, 0.013 - Q.girth2)
        - 0.02696 * max(0.0, 29.0 - Q.mass)
        - 0.05611 * max(0.0, 74.0 - Q.mass)
        - 0.004569 * max(0.0, Q.sum_pt - 880.0)
        - 1011.0 * max(0.0, 0.005 - Q.width)
        + 2146.0 * max(0.0, 0.018 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 1602.0 * max(0.0, 0.0062 - Q.lam1) * max(0.0, 0.95 - Q.D2)
        + 2.02 * max(0.0, 65.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.008)
        - 0.0005109 * max(0.0, 66.0 - Q.mass) * max(0.0, 39.0 - Q.pt_7)
        + 5.051e-05 * max(0.0, Q.sum_pt - 860.0) * max(0.0, 33.0 - Q.pt_7)
        - 0.03066 * max(0.0, Q.pt_7 - 32.0)
        + 402.2 * max(0.0, 0.01 - Q.width)
        - 11270.0 * max(0.0, 0.012 - Q.lam1) * max(0.0, Q.centroid_offset - 0.018)
        - 67.81 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.028 - Q.centroid_offset)
        + 500.4 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.0015 - Q.lam2)
        - 6.36e-05 * max(0.0, Q.pt_7 - 34.0) * max(0.0, 98.0 - Q.mass)
        - 2.842 * max(0.0, Q.LHA - 0.13)
        + 165.8 * max(0.0, 0.005 - Q.lam1)
        + 0.6156 * max(0.0, 6.4 - Q.log_sum_pt)
        + 0.03204 * max(0.0, Q.pt_7 - 28.0)
        - 0.001254 * max(0.0, 780.0 - Q.sum_pt)
        + 5.497 * max(0.0, Q.z_7 - 0.047)
        + 6.825 * max(0.0, 0.018 - Q.z_7)
        - 0.09884 * max(0.0, Q.pt_7 - 28.0) * max(0.0, 0.054 - Q.C2)
        + 0.1506 * max(0.0, Q.pt_7 - 28.0) * max(0.0, Q.max_dr - 0.07)
        + 34.36 * max(0.0, Q.LHA - 0.27)
        + 11.35 * max(0.0, Q.centroid_offset - 0.013)
        - 90.52 * max(0.0, 0.047 - Q.e2)
        + 402.2 * max(0.0, 0.01 - Q.girth2)
        + 131.9 * max(0.0, Q.lam1 - 0.016)
        + 43.87 * max(0.0, Q.mass_over_sum_pt - 0.071) * max(0.0, 0.55 - Q.tau32)
        + 129.8 * max(0.0, Q.C2 - 0.063)
        + 249.9 * max(0.0, 0.00042 - Q.lam2)
        - 0.03194 * max(0.0, 55.0 - Q.mass)
        + 16.2 * max(0.0, Q.mass_over_sum_pt - 0.086)
        - 0.4056 * max(0.0, 0.27 - Q.tau21)
        + 441.4 * max(0.0, Q.width - 0.0016)
        - 0.4573 * max(0.0, Q.C2 - -0.00087) * max(0.0, Q.pt_7 - 38.0)
        + 0.09825 * max(0.0, 0.26 - Q.tau21) * max(0.0, 57.0 - Q.mass)
        + 139.9 * max(0.0, 0.04 - Q.e2)
        - 18.02 * max(0.0, Q.log_sum_pt - 6.9)
        - 22.83 * max(0.0, 0.035 - Q.z_7)
        - 9.589 * max(0.0, 0.066 - Q.z_7)
        + 20.18 * max(0.0, 0.22 - Q.LHA) * max(0.0, 6.8 - Q.log_sum_pt)
        + 367800.0 * max(0.0, 0.025 - Q.e2) * max(0.0, 9.2e-05 - Q.lam2)
        + 9182.0 * max(0.0, 0.0026 - Q.width) * max(0.0, 0.021 - Q.centroid_offset)
        + 386.7 * max(0.0, 0.072 - Q.z_7) * max(0.0, 0.032 - Q.centroid_offset)
        - 116.5 * max(0.0, Q.girth - 0.09)
        + 279.8 * max(0.0, Q.lam2 - 0.0027)
        + 345.3 * max(0.0, 0.00066 - Q.lam2)
        + 67.01 * max(0.0, Q.mass_over_sum_pt - 0.0089)
        - 9.938 * Q.max_dr
        + 395.8 * max(0.0, 0.012 - Q.width)
        - 3719.0 * max(0.0, Q.centroid_offset - 0.0059) * max(0.0, 0.0026 - Q.lam2)
        - 39.77 * max(0.0, 0.049 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.18)
        - 0.08769 * max(0.0, 6.5 - Q.log_sum_pt) * max(0.0, 44.0 - Q.pt_7)
        - 300.9 * max(0.0, 6.3 - Q.log_sum_pt) * max(0.0, 0.071 - Q.z_7)
        - 245.6 * max(0.0, 6.7 - Q.log_sum_pt) * max(0.0, 0.049 - Q.z_7)
        - 0.01436 * max(0.0, 42.0 - Q.mass) * max(0.0, 0.94 - Q.z_dr_0p05_0p1)
        + 11.64 * max(0.0, Q.mass_over_sum_pt - 0.015) * max(0.0, 0.55 - Q.tau32)
        - 67.17 * max(0.0, 0.038 - Q.e2)
        + 314.2 * max(0.0, 0.0011 - Q.e2_sq)
        - 69.32 * max(0.0, 0.087 - Q.girth)
        - 312.6 * max(0.0, Q.girth2 - 0.0046)
        + 0.03278 * max(0.0, Q.mass - 80.4)
        + 44.53 * max(0.0, Q.mass_over_sum_pt - 0.073)
        - 71.27 * max(0.0, Q.mass_over_sum_pt - 0.09)
        - 2.061 * max(0.0, 0.19 - Q.planar_flow)
        + 455.9 * max(0.0, 0.00069 - Q.width)
        - 649.1 * max(0.0, 0.0056 - Q.width)
        - 0.9169 * max(0.0, Q.centroid_offset - 0.031) * max(0.0, Q.pt_0 - 370.0)
        + 323.3 * max(0.0, Q.girth2 - 0.0047) * max(0.0, Q.eccentricity - 0.94)
        + 0.00334 * max(0.0, 0.18 - Q.planar_flow) * max(0.0, Q.sum_pt - 590.0)
        + 143.4 * max(0.0, 0.22 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        + 0.001963 * max(0.0, 45.0 - Q.pt_7) * max(0.0, 0.6 - Q.planar_flow)
        - 37.56 * max(0.0, 0.063 - Q.girth)
        + 675.9 * max(0.0, 0.0049 - Q.width)
        + 19850.0 * max(0.0, 0.17 - Q.LHA) * max(0.0, 0.00039 - Q.lam2)
        - 420.7 * max(0.0, 0.0051 - Q.girth2) * max(0.0, 0.54 - Q.planar_flow)
        - 1.971 * max(0.0, 20.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.015)
        + 8807.0 * max(0.0, 0.0051 - Q.width) * max(0.0, Q.centroid_offset - 0.0014)
        + 76.25 * max(0.0, 0.019 - Q.centroid_offset)
        - 147.6 * max(0.0, Q.lam2 - 0.0015)
        - 2.523 * max(0.0, Q.log_sum_pt - 6.3)
        + 0.0694 * max(0.0, 25.0 - Q.mass)
        + 0.007448 * max(0.0, Q.n_dr_0p2_0p4 - 1.5)
        + 665.0 * max(0.0, 0.00029 - Q.width)
        - 679.2 * max(0.0, 0.0065 - Q.width)
        + 9.762 * max(0.0, Q.girth2 - 0.019) * max(0.0, 30.0 - Q.pt_7)
        - 0.02903 * max(0.0, 56.0 - Q.mass) * max(0.0, 6.8 - Q.log_sum_pt)
        + 2722.0 * max(0.0, 0.0091 - Q.width) * max(0.0, Q.C2 - 0.026)
        + 21230.0 * max(0.0, 0.0061 - Q.width) * max(0.0, Q.centroid_offset - 0.0016)
        - 59.06 * max(0.0, Q.C2 - 0.059)
        - 17.11 * max(0.0, Q.e2 - 0.037)
        + 137.7 * max(0.0, 0.037 - Q.e2)
        + 98.52 * max(0.0, 0.0018 - Q.girth2)
        + 86.3 * max(0.0, Q.lam2 - 0.00016)
        + 2.079 * max(0.0, 6.3 - Q.log_sum_pt)
        + 0.2686 * max(0.0, 0.34 - Q.z_dr_0p05_0p1)
        - 14.72 * max(0.0, Q.LHA - 0.29) * max(0.0, 0.69 - Q.tau21)
        + 53.22 * max(0.0, Q.eccentricity - 0.9) * max(0.0, 0.041 - Q.z_dr_0p2_0p4)
        + 577.0 * max(0.0, Q.lam2 - 0.00022) * max(0.0, 0.52 - Q.tau21)
        - 4.684 * max(0.0, 0.15 - Q.LHA)
        + 74.75 * max(0.0, 0.05 - Q.centroid_offset)
        - 39.99 * max(0.0, Q.girth - 0.074)
        - 68.06 * max(0.0, 0.088 - Q.girth)
        - 340.6 * max(0.0, 0.0038 - Q.width)
        + 434.0 * max(0.0, 0.0088 - Q.width)
        - 39.37 * max(0.0, 0.39 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        - 57.89 * max(0.0, Q.e2 - 0.062)
        - 0.01569 * max(0.0, Q.mass - 91.2)
        + 3.845 * max(0.0, Q.width - 0.018)
        - 4365.0 * max(0.0, Q.girth2 - 0.019) * max(0.0, Q.lam2 - 0.0016)
        - 75.91 * max(0.0, Q.C2 - 0.065)
        - 18.3 * max(0.0, 0.14 - Q.girth)
        + 0.0008322 * max(0.0, Q.sum_pt - 980.0)
        + 15.58 * max(0.0, 0.15 - Q.girth) * max(0.0, 6.7 - Q.log_sum_pt)
        + 0.286 * max(0.0, 0.15 - Q.girth) * max(0.0, 35.0 - Q.pt_7)
        + 4.499e-05 * max(0.0, Q.sum_pt_top5 - 660.0) * max(0.0, 48.0 - Q.pt_7)
        - 1.364 * max(0.0, 0.52 - Q.tau21) * max(0.0, Q.max_dr - 0.031)
        + 158.4 * max(0.0, 0.091 - Q.girth)
        - 24.16 * max(0.0, 0.014 - Q.girth2)
        - 125.2 * max(0.0, Q.lam1 - 0.0075)
        + 0.02058 * max(0.0, 80.4 - Q.mass)
        - 5.707 * max(0.0, 0.18 - Q.max_dr)
        + 1067.0 * max(0.0, 0.0075 - Q.width)
        - 0.03391 * max(0.0, 0.64 - Q.z_dr_0p05_0p1)
        - 1643.0 * max(0.0, 0.014 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 3686.0 * max(0.0, Q.lam1 - 0.0064) * max(0.0, 0.16 - Q.max_dr)
        - 326.7 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.011)
        + 106.3 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018)
        + 12.24 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, 0.17 - Q.max_dr)
        + 550.9 * max(0.0, 0.0087 - Q.width) * max(0.0, 1.0 - Q.D2)
        - 568.7 * max(0.0, 0.0083 - Q.width) * max(0.0, 6.9 - Q.log_sum_pt)
        + 264.1 * max(0.0, 0.0078 - Q.width) * max(0.0, 0.097 - Q.planar_flow)
        - 3.183 * max(0.0, 0.63 - Q.z_dr_0p05_0p1) * max(0.0, 0.067 - Q.C2)
        + 26.49 * max(0.0, Q.LHA - 0.34)
        - 203.2 * max(0.0, 0.041 - Q.e2)
        - 1671.0 * max(0.0, 0.0065 - Q.lam1)
        + 1033.0 * max(0.0, 0.0081 - Q.lam1)
        + 1306.0 * max(0.0, 0.0069 - Q.width)
        + 6.394 * max(0.0, 0.31 - Q.tau21) * max(0.0, 0.68 - Q.z_dr_0p05_0p1)
        - 15.49 * max(0.0, 0.29 - Q.tau21) * max(0.0, 0.2 - Q.z_dr_0p2_0p4)
        + 3894.0 * max(0.0, 0.0065 - Q.width) * max(0.0, Q.log_sum_pt - 6.9)
    )


def score_Z(Q):
    return (-10.34
        - 36.93 * max(0.0, 0.033 - Q.centroid_offset)
        - 32.89 * max(0.0, 0.013 - Q.girth2)
        + 0.04743 * max(0.0, 29.0 - Q.mass)
        - 0.03915 * max(0.0, 74.0 - Q.mass)
        + 0.001372 * max(0.0, Q.sum_pt - 880.0)
        + 1122.0 * max(0.0, 0.005 - Q.width)
        - 4944.0 * max(0.0, 0.018 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        + 426.8 * max(0.0, 0.0062 - Q.lam1) * max(0.0, 0.95 - Q.D2)
        + 0.4938 * max(0.0, 65.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.008)
        - 6.82e-05 * max(0.0, 66.0 - Q.mass) * max(0.0, 39.0 - Q.pt_7)
        - 4.846e-05 * max(0.0, Q.sum_pt - 860.0) * max(0.0, 33.0 - Q.pt_7)
        - 0.003189 * max(0.0, Q.pt_7 - 32.0)
        + 282.3 * max(0.0, 0.01 - Q.width)
        + 1420.0 * max(0.0, 0.012 - Q.lam1) * max(0.0, Q.centroid_offset - 0.018)
        - 97.82 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.028 - Q.centroid_offset)
        + 737.9 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.0015 - Q.lam2)
        - 0.0001484 * max(0.0, Q.pt_7 - 34.0) * max(0.0, 98.0 - Q.mass)
        + 5.896 * max(0.0, Q.LHA - 0.13)
        + 77.52 * max(0.0, 0.005 - Q.lam1)
        + 1.015 * max(0.0, 6.4 - Q.log_sum_pt)
        + 0.003435 * max(0.0, Q.pt_7 - 28.0)
        + 0.0005231 * max(0.0, 780.0 - Q.sum_pt)
        + 3.565 * max(0.0, Q.z_7 - 0.047)
        - 4.384 * max(0.0, 0.018 - Q.z_7)
        + 0.2057 * max(0.0, Q.pt_7 - 28.0) * max(0.0, 0.054 - Q.C2)
        + 0.08874 * max(0.0, Q.pt_7 - 28.0) * max(0.0, Q.max_dr - 0.07)
        - 7.561 * max(0.0, Q.LHA - 0.27)
        + 0.5711 * max(0.0, Q.centroid_offset - 0.013)
        - 90.84 * max(0.0, 0.047 - Q.e2)
        + 282.3 * max(0.0, 0.01 - Q.girth2)
        + 126.6 * max(0.0, Q.lam1 - 0.016)
        + 55.66 * max(0.0, Q.mass_over_sum_pt - 0.071) * max(0.0, 0.55 - Q.tau32)
        + 4.946 * max(0.0, Q.C2 - 0.063)
        - 1096.0 * max(0.0, 0.00042 - Q.lam2)
        + 0.02338 * max(0.0, 55.0 - Q.mass)
        + 85.34 * max(0.0, Q.mass_over_sum_pt - 0.086)
        + 0.4929 * max(0.0, 0.27 - Q.tau21)
        + 33.76 * max(0.0, Q.width - 0.0016)
        + 0.1098 * max(0.0, Q.C2 - -0.00087) * max(0.0, Q.pt_7 - 38.0)
        - 0.02414 * max(0.0, 0.26 - Q.tau21) * max(0.0, 57.0 - Q.mass)
        - 66.9 * max(0.0, 0.04 - Q.e2)
        - 8.347 * max(0.0, Q.log_sum_pt - 6.9)
        - 9.044 * max(0.0, 0.035 - Q.z_7)
        - 2.434 * max(0.0, 0.066 - Q.z_7)
        + 7.584 * max(0.0, 0.22 - Q.LHA) * max(0.0, 6.8 - Q.log_sum_pt)
        + 64860.0 * max(0.0, 0.025 - Q.e2) * max(0.0, 9.2e-05 - Q.lam2)
        + 23860.0 * max(0.0, 0.0026 - Q.width) * max(0.0, 0.021 - Q.centroid_offset)
        + 146.5 * max(0.0, 0.072 - Q.z_7) * max(0.0, 0.032 - Q.centroid_offset)
        - 79.36 * max(0.0, Q.girth - 0.09)
        + 50.23 * max(0.0, Q.lam2 - 0.0027)
        + 741.2 * max(0.0, 0.00066 - Q.lam2)
        + 61.09 * max(0.0, Q.mass_over_sum_pt - 0.0089)
        - 6.972 * Q.max_dr
        + 610.3 * max(0.0, 0.012 - Q.width)
        - 3634.0 * max(0.0, Q.centroid_offset - 0.0059) * max(0.0, 0.0026 - Q.lam2)
        - 89.22 * max(0.0, 0.049 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.18)
        - 0.1082 * max(0.0, 6.5 - Q.log_sum_pt) * max(0.0, 44.0 - Q.pt_7)
        - 314.0 * max(0.0, 6.3 - Q.log_sum_pt) * max(0.0, 0.071 - Q.z_7)
        - 282.5 * max(0.0, 6.7 - Q.log_sum_pt) * max(0.0, 0.049 - Q.z_7)
        - 0.003751 * max(0.0, 42.0 - Q.mass) * max(0.0, 0.94 - Q.z_dr_0p05_0p1)
        + 13.2 * max(0.0, Q.mass_over_sum_pt - 0.015) * max(0.0, 0.55 - Q.tau32)
        + 96.38 * max(0.0, 0.038 - Q.e2)
        + 1183.0 * max(0.0, 0.0011 - Q.e2_sq)
        - 14.2 * max(0.0, 0.087 - Q.girth)
        + 160.0 * max(0.0, Q.girth2 - 0.0046)
        - 0.07691 * max(0.0, Q.mass - 80.4)
        + 68.06 * max(0.0, Q.mass_over_sum_pt - 0.073)
        - 180.4 * max(0.0, Q.mass_over_sum_pt - 0.09)
        - 2.861 * max(0.0, 0.19 - Q.planar_flow)
        - 687.1 * max(0.0, 0.00069 - Q.width)
        - 628.3 * max(0.0, 0.0056 - Q.width)
        - 1.68 * max(0.0, Q.centroid_offset - 0.031) * max(0.0, Q.pt_0 - 370.0)
        + 6857.0 * max(0.0, Q.girth2 - 0.0047) * max(0.0, Q.eccentricity - 0.94)
        + 0.01276 * max(0.0, 0.18 - Q.planar_flow) * max(0.0, Q.sum_pt - 590.0)
        - 1938.0 * max(0.0, 0.22 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        - 0.02482 * max(0.0, 45.0 - Q.pt_7) * max(0.0, 0.6 - Q.planar_flow)
        + 20.98 * max(0.0, 0.063 - Q.girth)
        - 1351.0 * max(0.0, 0.0049 - Q.width)
        - 3528.0 * max(0.0, 0.17 - Q.LHA) * max(0.0, 0.00039 - Q.lam2)
        + 48.33 * max(0.0, 0.0051 - Q.girth2) * max(0.0, 0.54 - Q.planar_flow)
        - 1.882 * max(0.0, 20.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.015)
        - 11120.0 * max(0.0, 0.0051 - Q.width) * max(0.0, Q.centroid_offset - 0.0014)
        + 1.159 * max(0.0, 0.019 - Q.centroid_offset)
        + 50.98 * max(0.0, Q.lam2 - 0.0015)
        - 0.6621 * max(0.0, Q.log_sum_pt - 6.3)
        + 0.00989 * max(0.0, 25.0 - Q.mass)
        - 0.005099 * max(0.0, Q.n_dr_0p2_0p4 - 1.5)
        + 369.8 * max(0.0, 0.00029 - Q.width)
        - 242.0 * max(0.0, 0.0065 - Q.width)
        + 11.23 * max(0.0, Q.girth2 - 0.019) * max(0.0, 30.0 - Q.pt_7)
        - 0.03497 * max(0.0, 56.0 - Q.mass) * max(0.0, 6.8 - Q.log_sum_pt)
        + 860.3 * max(0.0, 0.0091 - Q.width) * max(0.0, Q.C2 - 0.026)
        + 16410.0 * max(0.0, 0.0061 - Q.width) * max(0.0, Q.centroid_offset - 0.0016)
        + 21.73 * max(0.0, Q.C2 - 0.059)
        + 2.634 * max(0.0, Q.e2 - 0.037)
        - 26.37 * max(0.0, 0.037 - Q.e2)
        + 191.0 * max(0.0, 0.0018 - Q.girth2)
        - 13.99 * max(0.0, Q.lam2 - 0.00016)
        + 0.505 * max(0.0, 6.3 - Q.log_sum_pt)
        + 0.1875 * max(0.0, 0.34 - Q.z_dr_0p05_0p1)
        - 6.64 * max(0.0, Q.LHA - 0.29) * max(0.0, 0.69 - Q.tau21)
        - 32.86 * max(0.0, Q.eccentricity - 0.9) * max(0.0, 0.041 - Q.z_dr_0p2_0p4)
        - 17.84 * max(0.0, Q.lam2 - 0.00022) * max(0.0, 0.52 - Q.tau21)
        - 1.32 * max(0.0, 0.15 - Q.LHA)
        + 33.81 * max(0.0, 0.05 - Q.centroid_offset)
        + 15.6 * max(0.0, Q.girth - 0.074)
        - 12.31 * max(0.0, 0.088 - Q.girth)
        + 130.0 * max(0.0, 0.0038 - Q.width)
        + 274.8 * max(0.0, 0.0088 - Q.width)
        + 26.16 * max(0.0, 0.39 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        - 92.64 * max(0.0, Q.e2 - 0.062)
        + 0.09175 * max(0.0, Q.mass - 91.2)
        + 162.5 * max(0.0, Q.width - 0.018)
        - 7827.0 * max(0.0, Q.girth2 - 0.019) * max(0.0, Q.lam2 - 0.0016)
        - 34.15 * max(0.0, Q.C2 - 0.065)
        + 18.87 * max(0.0, 0.14 - Q.girth)
        - 0.0007989 * max(0.0, Q.sum_pt - 980.0)
        - 1.435 * max(0.0, 0.15 - Q.girth) * max(0.0, 6.7 - Q.log_sum_pt)
        + 0.03185 * max(0.0, 0.15 - Q.girth) * max(0.0, 35.0 - Q.pt_7)
        + 3.017e-05 * max(0.0, Q.sum_pt_top5 - 660.0) * max(0.0, 48.0 - Q.pt_7)
        - 0.2306 * max(0.0, 0.52 - Q.tau21) * max(0.0, Q.max_dr - 0.031)
        - 18.31 * max(0.0, 0.091 - Q.girth)
        + 406.5 * max(0.0, 0.014 - Q.girth2)
        - 315.7 * max(0.0, Q.lam1 - 0.0075)
        - 0.01744 * max(0.0, 80.4 - Q.mass)
        - 8.161 * max(0.0, 0.18 - Q.max_dr)
        - 630.7 * max(0.0, 0.0075 - Q.width)
        + 0.06037 * max(0.0, 0.64 - Q.z_dr_0p05_0p1)
        + 10520.0 * max(0.0, 0.014 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        + 5805.0 * max(0.0, Q.lam1 - 0.0064) * max(0.0, 0.16 - Q.max_dr)
        + 364.0 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.011)
        - 508.9 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018)
        - 45.91 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, 0.17 - Q.max_dr)
        - 198.1 * max(0.0, 0.0087 - Q.width) * max(0.0, 1.0 - Q.D2)
        - 12.96 * max(0.0, 0.0083 - Q.width) * max(0.0, 6.9 - Q.log_sum_pt)
        - 1839.0 * max(0.0, 0.0078 - Q.width) * max(0.0, 0.097 - Q.planar_flow)
        - 11.02 * max(0.0, 0.63 - Q.z_dr_0p05_0p1) * max(0.0, 0.067 - Q.C2)
        + 19.98 * max(0.0, Q.LHA - 0.34)
        + 106.3 * max(0.0, 0.041 - Q.e2)
        - 318.8 * max(0.0, 0.0065 - Q.lam1)
        + 162.0 * max(0.0, 0.0081 - Q.lam1)
        + 291.8 * max(0.0, 0.0069 - Q.width)
        + 0.3279 * max(0.0, 0.31 - Q.tau21) * max(0.0, 0.68 - Q.z_dr_0p05_0p1)
        + 2.849 * max(0.0, 0.29 - Q.tau21) * max(0.0, 0.2 - Q.z_dr_0p2_0p4)
        + 1592.0 * max(0.0, 0.0065 - Q.width) * max(0.0, Q.log_sum_pt - 6.9)
    )


def score_t(Q):
    return (0.9954
        + 16.71 * max(0.0, 0.033 - Q.centroid_offset)
        - 65.37 * max(0.0, 0.013 - Q.girth2)
        - 0.01552 * max(0.0, 29.0 - Q.mass)
        - 0.005166 * max(0.0, 74.0 - Q.mass)
        + 0.00293 * max(0.0, Q.sum_pt - 880.0)
        + 164.6 * max(0.0, 0.005 - Q.width)
        - 757.5 * max(0.0, 0.018 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 81.29 * max(0.0, 0.0062 - Q.lam1) * max(0.0, 0.95 - Q.D2)
        - 0.5549 * max(0.0, 65.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.008)
        + 0.0001496 * max(0.0, 66.0 - Q.mass) * max(0.0, 39.0 - Q.pt_7)
        + 0.0001002 * max(0.0, Q.sum_pt - 860.0) * max(0.0, 33.0 - Q.pt_7)
        + 0.0007616 * max(0.0, Q.pt_7 - 32.0)
        - 23.46 * max(0.0, 0.01 - Q.width)
        + 2387.0 * max(0.0, 0.012 - Q.lam1) * max(0.0, Q.centroid_offset - 0.018)
        - 14.37 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.028 - Q.centroid_offset)
        - 552.1 * max(0.0, Q.log_sum_pt - 6.5) * max(0.0, 0.0015 - Q.lam2)
        + 9.592e-05 * max(0.0, Q.pt_7 - 34.0) * max(0.0, 98.0 - Q.mass)
        - 3.481 * max(0.0, Q.LHA - 0.13)
        + 72.23 * max(0.0, 0.005 - Q.lam1)
        + 0.025 * max(0.0, 6.4 - Q.log_sum_pt)
        - 0.003973 * max(0.0, Q.pt_7 - 28.0)
        + 0.0008694 * max(0.0, 780.0 - Q.sum_pt)
        + 4.41 * max(0.0, Q.z_7 - 0.047)
        - 3.654 * max(0.0, 0.018 - Q.z_7)
        - 0.06516 * max(0.0, Q.pt_7 - 28.0) * max(0.0, 0.054 - Q.C2)
        + 0.005016 * max(0.0, Q.pt_7 - 28.0) * max(0.0, Q.max_dr - 0.07)
        - 4.269 * max(0.0, Q.LHA - 0.27)
        + 2.913 * max(0.0, Q.centroid_offset - 0.013)
        + 23.03 * max(0.0, 0.047 - Q.e2)
        - 23.46 * max(0.0, 0.01 - Q.girth2)
        - 39.58 * max(0.0, Q.lam1 - 0.016)
        + 6.891 * max(0.0, Q.mass_over_sum_pt - 0.071) * max(0.0, 0.55 - Q.tau32)
        - 3.51 * max(0.0, Q.C2 - 0.063)
        - 801.4 * max(0.0, 0.00042 - Q.lam2)
        + 0.00865 * max(0.0, 55.0 - Q.mass)
        - 46.48 * max(0.0, Q.mass_over_sum_pt - 0.086)
        + 3.755 * max(0.0, 0.27 - Q.tau21)
        - 167.4 * max(0.0, Q.width - 0.0016)
        + 0.1712 * max(0.0, Q.C2 - -0.00087) * max(0.0, Q.pt_7 - 38.0)
        - 0.08655 * max(0.0, 0.26 - Q.tau21) * max(0.0, 57.0 - Q.mass)
        - 20.45 * max(0.0, 0.04 - Q.e2)
        + 32.67 * max(0.0, Q.log_sum_pt - 6.9)
        - 36.64 * max(0.0, 0.035 - Q.z_7)
        - 22.7 * max(0.0, 0.066 - Q.z_7)
        + 15.74 * max(0.0, 0.22 - Q.LHA) * max(0.0, 6.8 - Q.log_sum_pt)
        - 117500.0 * max(0.0, 0.025 - Q.e2) * max(0.0, 9.2e-05 - Q.lam2)
        + 12680.0 * max(0.0, 0.0026 - Q.width) * max(0.0, 0.021 - Q.centroid_offset)
        + 729.4 * max(0.0, 0.072 - Q.z_7) * max(0.0, 0.032 - Q.centroid_offset)
        + 20.0 * max(0.0, Q.girth - 0.09)
        + 13.27 * max(0.0, Q.lam2 - 0.0027)
        + 9.872 * max(0.0, 0.00066 - Q.lam2)
        + 18.57 * max(0.0, Q.mass_over_sum_pt - 0.0089)
        + 0.4774 * Q.max_dr
        + 4.205 * max(0.0, 0.012 - Q.width)
        + 2199.0 * max(0.0, Q.centroid_offset - 0.0059) * max(0.0, 0.0026 - Q.lam2)
        + 85.24 * max(0.0, 0.049 - Q.e2) * max(0.0, Q.z_dr_0p1_0p2 - 0.18)
        + 0.007734 * max(0.0, 6.5 - Q.log_sum_pt) * max(0.0, 44.0 - Q.pt_7)
        + 64.6 * max(0.0, 6.3 - Q.log_sum_pt) * max(0.0, 0.071 - Q.z_7)
        + 47.64 * max(0.0, 6.7 - Q.log_sum_pt) * max(0.0, 0.049 - Q.z_7)
        + 0.001416 * max(0.0, 42.0 - Q.mass) * max(0.0, 0.94 - Q.z_dr_0p05_0p1)
        - 3.924 * max(0.0, Q.mass_over_sum_pt - 0.015) * max(0.0, 0.55 - Q.tau32)
        + 6.371 * max(0.0, 0.038 - Q.e2)
        + 36.76 * max(0.0, 0.0011 - Q.e2_sq)
        + 5.08 * max(0.0, 0.087 - Q.girth)
        + 132.0 * max(0.0, Q.girth2 - 0.0046)
        + 0.009142 * max(0.0, Q.mass - 80.4)
        + 4.179 * max(0.0, Q.mass_over_sum_pt - 0.073)
        + 20.88 * max(0.0, Q.mass_over_sum_pt - 0.09)
        - 0.1797 * max(0.0, 0.19 - Q.planar_flow)
        - 189.5 * max(0.0, 0.00069 - Q.width)
        - 0.6954 * max(0.0, 0.0056 - Q.width)
        + 0.8788 * max(0.0, Q.centroid_offset - 0.031) * max(0.0, Q.pt_0 - 370.0)
        + 155.4 * max(0.0, Q.girth2 - 0.0047) * max(0.0, Q.eccentricity - 0.94)
        + 0.001081 * max(0.0, 0.18 - Q.planar_flow) * max(0.0, Q.sum_pt - 590.0)
        - 11.47 * max(0.0, 0.22 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        + 0.00912 * max(0.0, 45.0 - Q.pt_7) * max(0.0, 0.6 - Q.planar_flow)
        - 2.578 * max(0.0, 0.063 - Q.girth)
        - 172.0 * max(0.0, 0.0049 - Q.width)
        - 40600.0 * max(0.0, 0.17 - Q.LHA) * max(0.0, 0.00039 - Q.lam2)
        + 61.38 * max(0.0, 0.0051 - Q.girth2) * max(0.0, 0.54 - Q.planar_flow)
        + 0.1794 * max(0.0, 20.0 - Q.mass) * max(0.0, Q.centroid_offset - 0.015)
        - 3689.0 * max(0.0, 0.0051 - Q.width) * max(0.0, Q.centroid_offset - 0.0014)
        - 6.826 * max(0.0, 0.019 - Q.centroid_offset)
        + 4.114 * max(0.0, Q.lam2 - 0.0015)
        + 1.297 * max(0.0, Q.log_sum_pt - 6.3)
        + 0.02256 * max(0.0, 25.0 - Q.mass)
        + 0.2228 * max(0.0, Q.n_dr_0p2_0p4 - 1.5)
        + 285.7 * max(0.0, 0.00029 - Q.width)
        + 35.39 * max(0.0, 0.0065 - Q.width)
        - 1.171 * max(0.0, Q.girth2 - 0.019) * max(0.0, 30.0 - Q.pt_7)
        + 0.05596 * max(0.0, 56.0 - Q.mass) * max(0.0, 6.8 - Q.log_sum_pt)
        - 682.1 * max(0.0, 0.0091 - Q.width) * max(0.0, Q.C2 - 0.026)
        - 2418.0 * max(0.0, 0.0061 - Q.width) * max(0.0, Q.centroid_offset - 0.0016)
        + 6.336 * max(0.0, Q.C2 - 0.059)
        + 23.71 * max(0.0, Q.e2 - 0.037)
        - 13.86 * max(0.0, 0.037 - Q.e2)
        - 450.5 * max(0.0, 0.0018 - Q.girth2)
        + 225.7 * max(0.0, Q.lam2 - 0.00016)
        - 3.649 * max(0.0, 6.3 - Q.log_sum_pt)
        + 1.041 * max(0.0, 0.34 - Q.z_dr_0p05_0p1)
        - 15.33 * max(0.0, Q.LHA - 0.29) * max(0.0, 0.69 - Q.tau21)
        + 109.5 * max(0.0, Q.eccentricity - 0.9) * max(0.0, 0.041 - Q.z_dr_0p2_0p4)
        + 932.0 * max(0.0, Q.lam2 - 0.00022) * max(0.0, 0.52 - Q.tau21)
        + 6.051 * max(0.0, 0.15 - Q.LHA)
        - 7.112 * max(0.0, 0.05 - Q.centroid_offset)
        + 2.594 * max(0.0, Q.girth - 0.074)
        - 8.711 * max(0.0, 0.088 - Q.girth)
        - 28.38 * max(0.0, 0.0038 - Q.width)
        - 85.8 * max(0.0, 0.0088 - Q.width)
        - 37.8 * max(0.0, 0.39 - Q.planar_flow) * max(0.0, Q.width - 0.0078)
        + 49.2 * max(0.0, Q.e2 - 0.062)
        - 0.04827 * max(0.0, Q.mass - 91.2)
        - 114.7 * max(0.0, Q.width - 0.018)
        - 11020.0 * max(0.0, Q.girth2 - 0.019) * max(0.0, Q.lam2 - 0.0016)
        + 27.57 * max(0.0, Q.C2 - 0.065)
        - 24.63 * max(0.0, 0.14 - Q.girth)
        - 0.02125 * max(0.0, Q.sum_pt - 980.0)
        - 1.534 * max(0.0, 0.15 - Q.girth) * max(0.0, 6.7 - Q.log_sum_pt)
        + 0.4847 * max(0.0, 0.15 - Q.girth) * max(0.0, 35.0 - Q.pt_7)
        - 0.0001828 * max(0.0, Q.sum_pt_top5 - 660.0) * max(0.0, 48.0 - Q.pt_7)
        + 8.295 * max(0.0, 0.52 - Q.tau21) * max(0.0, Q.max_dr - 0.031)
        - 10.09 * max(0.0, 0.091 - Q.girth)
        + 59.21 * max(0.0, 0.014 - Q.girth2)
        + 56.43 * max(0.0, Q.lam1 - 0.0075)
        + 0.0203 * max(0.0, 80.4 - Q.mass)
        + 1.196 * max(0.0, 0.18 - Q.max_dr)
        - 15.27 * max(0.0, 0.0075 - Q.width)
        - 0.1348 * max(0.0, 0.64 - Q.z_dr_0p05_0p1)
        + 764.8 * max(0.0, 0.014 - Q.girth2) * max(0.0, Q.eccentricity - 0.97)
        - 104.8 * max(0.0, Q.lam1 - 0.0064) * max(0.0, 0.16 - Q.max_dr)
        - 30.22 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.011)
        + 58.65 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, Q.centroid_offset - 0.018)
        + 4.026 * max(0.0, 0.12 - Q.planar_flow) * max(0.0, 0.17 - Q.max_dr)
        + 80.54 * max(0.0, 0.0087 - Q.width) * max(0.0, 1.0 - Q.D2)
        + 114.6 * max(0.0, 0.0083 - Q.width) * max(0.0, 6.9 - Q.log_sum_pt)
        + 66.7 * max(0.0, 0.0078 - Q.width) * max(0.0, 0.097 - Q.planar_flow)
        + 0.7821 * max(0.0, 0.63 - Q.z_dr_0p05_0p1) * max(0.0, 0.067 - Q.C2)
        - 0.5149 * max(0.0, Q.LHA - 0.34)
        + 10.06 * max(0.0, 0.041 - Q.e2)
        - 6.359 * max(0.0, 0.0065 - Q.lam1)
        + 2.448 * max(0.0, 0.0081 - Q.lam1)
        + 25.79 * max(0.0, 0.0069 - Q.width)
        - 0.2407 * max(0.0, 0.31 - Q.tau21) * max(0.0, 0.68 - Q.z_dr_0p05_0p1)
        - 2.342 * max(0.0, 0.29 - Q.tau21) * max(0.0, 0.2 - Q.z_dr_0p2_0p4)
        + 513.5 * max(0.0, 0.0065 - Q.width) * max(0.0, Q.log_sum_pt - 6.9)
    )


def scores(Q):
    return {c: f(Q) for c, f in zip(CLASSES, (score_g, score_q, score_W, score_Z, score_t))}


def decide(Q, s):
    if s['W'] - s['t'] > -3.8279107809066772:
        if s['q'] - s['Z'] > 0.24022626131772995:
            if s['g'] - s['q'] > -0.0037683285772800446:
                if s['g'] - s['W'] > 0.10579106956720352:
                    if s['g'] - s['t'] > -0.11503813043236732:
                        if s['g'] - s['q'] > 0.12615393102169037:
                            if s['g'] - s['W'] > 0.35529178380966187:
                                if Q.z_7 > 0.015656876377761364:
                                    if s['g'] - s['q'] > 0.20380205661058426:
                                        if s['g'] - s['t'] > 0.10932128503918648:
                                            return 'g'   # 100% of the training jets here get this class from the formula
                                        else:
                                            if Q.e2 > 0.050341662019491196:
                                                return 't'   # 52% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 84% of the training jets here get this class from the formula
                                    else:
                                        if Q.centroid_offset > 0.004962526028975844:
                                            if Q.sum_pt > 922.09375:
                                                if Q.sum_pt > 987.0625:
                                                    return 'g'   # 98% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 78% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 97% of the training jets here get this class from the formula
                                        else:
                                            if Q.sum_pt > 713.453125:
                                                if s['g'] - s['Z'] > 2.067168354988098:
                                                    return 'g'   # 96% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.0022936806781217456:
                                                        if Q.sum_pt > 730.546875:
                                                            return 'g'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 61% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 99% of the training jets here get this class from the formula
                                            else:
                                                if Q.eccentricity > 0.9741584360599518:
                                                    return 'g'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam1 > 0.00013679912080988288:
                                                        if s['g'] - s['q'] > 0.15849114209413528:
                                                            if Q.centroid_offset > 0.003981532528996468:
                                                                return 'g'   # 89% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.sum_pt > 689.75:
                                                                    return 'g'   # 84% of the training jets here get this class from the formula
                                                                else:
                                                                    if s['Z'] - s['t'] > -0.6209993958473206:
                                                                        return 'q'   # 61% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'g'   # 72% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.sum_pt_top5 > 454.9375:
                                                                return 'q'   # 75% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 63% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.centroid_offset > 0.0030473960796371102:
                                                            if s['g'] - s['t'] > 3.7350085973739624:
                                                                return 'q'   # 87% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 53% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 96% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['Z'] > 1.1549567580223083:
                                        return 'q'   # 85% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 56% of the training jets here get this class from the formula
                            else:
                                if Q.z_7 > 0.04620402492582798:
                                    if s['g'] - s['Z'] > 1.1123083233833313:
                                        if Q.mass_over_sum_pt > 0.06049175001680851:
                                            if Q.D2 > 1.0624821186065674:
                                                if Q.tau21 > 0.3783019185066223:
                                                    return 'g'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 87% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 96% of the training jets here get this class from the formula
                                    else:
                                        if Q.LHA > 0.21527913957834244:
                                            if Q.planar_flow > 0.10179683938622475:
                                                return 'W'   # 78% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 64% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.018526473082602024:
                                                if Q.sum_pt_top5 > 612.40625:
                                                    return 'W'   # 68% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 81% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 93% of the training jets here get this class from the formula
                                else:
                                    if s['Z'] - s['t'] > 2.5338157415390015:
                                        if s['q'] - s['W'] > 0.0773206576704979:
                                            return 'g'   # 65% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 82% of the training jets here get this class from the formula
                                    else:
                                        if Q.centroid_offset > 0.019246895797550678:
                                            if s['g'] - s['Z'] > 0.6895578503608704:
                                                if Q.LHA > 0.18943990021944046:
                                                    return 'W'   # 68% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 84% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 78% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 90% of the training jets here get this class from the formula
                        else:
                            if Q.centroid_offset > 0.007028921507298946:
                                if Q.sum_pt > 891.890625:
                                    if Q.sum_pt > 993.3671875:
                                        return 'g'   # 95% of the training jets here get this class from the formula
                                    else:
                                        return 'q'   # 84% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['Z'] > 0.6884278953075409:
                                        if s['g'] - s['q'] > 0.029761606827378273:
                                            if s['q'] - s['Z'] > 2.5261073112487793:
                                                if Q.girth > 0.02103497087955475:
                                                    return 'g'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 73% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 94% of the training jets here get this class from the formula
                                        else:
                                            if Q.LHA > 0.1148146353662014:
                                                if s['q'] - s['W'] > 1.9512340426445007:
                                                    if Q.sum_pt > 696.5625:
                                                        return 'g'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 69% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['t'] > 3.411763548851013:
                                                        return 'q'   # 70% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 88% of the training jets here get this class from the formula
                                            else:
                                                if s['Z'] - s['t'] > 2.402332067489624:
                                                    return 'g'   # 67% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 89% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['W'] > 0.36503277719020844:
                                            return 'q'   # 53% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_7 > 0.04208240285515785:
                                                return 'g'   # 57% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 74% of the training jets here get this class from the formula
                            else:
                                if Q.sum_pt > 755.578125:
                                    if Q.log_sum_pt > 6.818582534790039:
                                        if Q.log_sum_pt > 6.897799015045166:
                                            if Q.z_7 > 0.017749479971826077:
                                                return 'g'   # 98% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 88% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['Z'] > 2.670207977294922:
                                                return 'g'   # 72% of the training jets here get this class from the formula
                                            else:
                                                if Q.log_sum_pt > 6.836007356643677:
                                                    return 'q'   # 91% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 50% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt > 771.0:
                                            if s['g'] - s['q'] > 0.007997105363756418:
                                                return 'g'   # 98% of the training jets here get this class from the formula
                                            else:
                                                if Q.C2 > 0.008323690854012966:
                                                    return 'g'   # 98% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['W'] > 2.1204711198806763:
                                                        return 'g'   # 74% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 76% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth > 0.00799313560128212:
                                                return 'g'   # 94% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['q'] > 0.07758897170424461:
                                                    return 'g'   # 92% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 83% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.0019997863564640284:
                                        if s['g'] - s['q'] > 0.06513987109065056:
                                            if Q.centroid_offset > 0.005198847968131304:
                                                if Q.LHA > 0.10505644604563713:
                                                    return 'g'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt > 724.59375:
                                                        return 'g'   # 58% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 90% of the training jets here get this class from the formula
                                            else:
                                                if Q.C2 > 0.009639175608754158:
                                                    if Q.log_sum_pt > 6.571408033370972:
                                                        return 'g'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.D2 > 0.7229395806789398:
                                                            if Q.planar_flow > 0.5696807503700256:
                                                                return 'g'   # 52% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 80% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.002900391351431608:
                                                        return 'q'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.z_7 > 0.059100428596138954:
                                                            return 'q'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 71% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['W'] > 1.4005587697029114:
                                                if Q.max_dr > 0.055058758705854416:
                                                    if Q.sum_pt > 697.359375:
                                                        return 'g'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.0028291005874052644:
                                                        return 'q'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.pt_7 > 36.8125:
                                                            return 'q'   # 90% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 67% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 76% of the training jets here get this class from the formula
                                    else:
                                        if Q.mass > 8.944921493530273:
                                            if Q.log_sum_pt > 6.466678857803345:
                                                if Q.log_sum_pt > 6.591652154922485:
                                                    return 'g'   # 61% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 86% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 16.456817626953125:
                                                    return 'q'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 95% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 93% of the training jets here get this class from the formula
                    else:
                        if s['g'] - s['t'] > -0.41756175458431244:
                            if Q.width > 0.0062230974435806274:
                                if Q.girth > 0.16753090918064117:
                                    return 'g'   # 52% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 88% of the training jets here get this class from the formula
                            else:
                                if s['Z'] - s['t'] > -2.6344796419143677:
                                    if s['g'] - s['t'] > -0.22260448336601257:
                                        if Q.e2_sq > 0.0036150235682725906:
                                            return 'g'   # 85% of the training jets here get this class from the formula
                                        else:
                                            if Q.max_dr > 0.0816338062286377:
                                                return 't'   # 84% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 68% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 76% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 96% of the training jets here get this class from the formula
                        else:
                            return 't'   # 98% of the training jets here get this class from the formula
                else:
                    if s['g'] - s['W'] > -0.36228179931640625:
                        if s['g'] - s['Z'] > 1.0580397844314575:
                            if Q.mass_over_sum_pt > 0.05952820926904678:
                                if s['g'] - s['t'] > -0.27277161180973053:
                                    if Q.C2 > 0.022332909516990185:
                                        if s['g'] - s['q'] > 0.8896949589252472:
                                            if Q.centroid_offset > 0.01393819972872734:
                                                return 'g'   # 85% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 61% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 85% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['t'] > 0.15867769718170166:
                                            return 'g'   # 93% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 50% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 88% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['Z'] > 1.3343374133110046:
                                    if Q.max_dr > 0.09826997295022011:
                                        if Q.pt_7 > 48.78125:
                                            return 'W'   # 69% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 77% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 93% of the training jets here get this class from the formula
                                else:
                                    if Q.lam2 > 0.0002141009535989724:
                                        if Q.LHA > 0.21107187122106552:
                                            return 'W'   # 71% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 68% of the training jets here get this class from the formula
                                    else:
                                        if Q.max_dr > 0.11900508403778076:
                                            if Q.eccentricity > 0.9754983484745026:
                                                return 'W'   # 69% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 74% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['W'] > -0.9637890458106995:
                                                return 'g'   # 80% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 60% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['Z'] > 0.811908632516861:
                                if Q.e2 > 0.013364769984036684:
                                    if Q.D2 > 2.291933298110962:
                                        return 'g'   # 63% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_7 > 36.34375:
                                            if Q.e2_sq > 0.0027654418954625726:
                                                return 'W'   # 97% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_7 > 0.059960510581731796:
                                                    return 'g'   # 80% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 69% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 86% of the training jets here get this class from the formula
                                else:
                                    if Q.sum_pt_top5 > 621.3125:
                                        return 'W'   # 59% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 85% of the training jets here get this class from the formula
                            else:
                                if Q.pt_7 > 26.03125:
                                    if Q.z_7 > 0.047594066709280014:
                                        if Q.e2 > 0.013156128581613302:
                                            return 'W'   # 91% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 60% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 92% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 52% of the training jets here get this class from the formula
                    else:
                        if s['W'] - s['t'] > 0.037867105565965176:
                            if s['g'] - s['W'] > -0.5996963679790497:
                                if s['g'] - s['Z'] > 0.9829657077789307:
                                    if Q.width > 0.003270673449151218:
                                        return 'W'   # 85% of the training jets here get this class from the formula
                                    else:
                                        if Q.z_dr_0p05_0p1 > 0.18347203731536865:
                                            return 'g'   # 62% of the training jets here get this class from the formula
                                        else:
                                            if Q.C2 > 0.01678588893264532:
                                                return 'W'   # 80% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 60% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 94% of the training jets here get this class from the formula
                            else:
                                return 'W'   # 96% of the training jets here get this class from the formula
                        else:
                            return 't'   # 83% of the training jets here get this class from the formula
            else:
                if s['q'] - s['W'] > 0.25032998621463776:
                    if s['g'] - s['q'] > -0.09552823379635811:
                        if Q.log_sum_pt > 6.909207344055176:
                            if Q.z_7 > 0.016304880380630493:
                                return 'g'   # 93% of the training jets here get this class from the formula
                            else:
                                return 'q'   # 79% of the training jets here get this class from the formula
                        else:
                            if Q.centroid_offset > 0.012992383446544409:
                                if s['g'] - s['t'] > -0.15411539375782013:
                                    if Q.e2 > 0.006742503959685564:
                                        if Q.pt_7 > 23.9609375:
                                            if s['g'] - s['q'] > -0.07377742230892181:
                                                return 'g'   # 83% of the training jets here get this class from the formula
                                            else:
                                                if Q.log_sum_pt > 6.518937110900879:
                                                    return 'q'   # 67% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 68% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 55% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['q'] > -0.03797489404678345:
                                            if s['Z'] - s['t'] > 2.7913901805877686:
                                                return 'q'   # 76% of the training jets here get this class from the formula
                                            else:
                                                if Q.LHA > 0.17915970087051392:
                                                    return 'q'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 80% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 75% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 83% of the training jets here get this class from the formula
                            else:
                                if Q.centroid_offset > 0.002089264919050038:
                                    if Q.mass > 26.791635513305664:
                                        if Q.lam1 > 0.0028875397983938456:
                                            return 't'   # 60% of the training jets here get this class from the formula
                                        else:
                                            if s['Z'] - s['t'] > -0.5660611689090729:
                                                if Q.z_7 > 0.04477275535464287:
                                                    return 'g'   # 71% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 60% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 70% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt_top5 > 620.203125:
                                            if Q.mass > 8.316360473632812:
                                                if Q.sum_pt_top5 > 724.15625:
                                                    return 'q'   # 91% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['q'] > -0.06825223192572594:
                                                        if s['W'] - s['Z'] > 0.4766934812068939:
                                                            return 'q'   # 72% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.lam2 > 4.6291987018776126e-05:
                                                                return 'g'   # 87% of the training jets here get this class from the formula
                                                            else:
                                                                if s['g'] - s['W'] > 2.312211751937866:
                                                                    return 'g'   # 86% of the training jets here get this class from the formula
                                                                else:
                                                                    if s['g'] - s['q'] > -0.03947591409087181:
                                                                        return 'g'   # 64% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'q'   # 74% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.D2 > 2.2120426893234253:
                                                            if Q.z_7 > 0.047886377200484276:
                                                                return 'g'   # 68% of the training jets here get this class from the formula
                                                            else:
                                                                return 'q'   # 79% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 87% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt_7 > 62.953125:
                                                    return 'g'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['q'] > -0.03050007950514555:
                                                        if Q.lam2 > 3.244430627091788e-05:
                                                            return 'g'   # 63% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 94% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.00992330489680171:
                                                if s['g'] - s['q'] > -0.04577258042991161:
                                                    if Q.z_7 > 0.042344531044363976:
                                                        return 'g'   # 76% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 83% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 92% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['Z'] > 2.067908525466919:
                                        if Q.z_7 > 0.04607752151787281:
                                            if Q.sum_pt_top5 > 617.078125:
                                                if Q.sum_pt > 917.65625:
                                                    return 'q'   # 81% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 75% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 83% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 79% of the training jets here get this class from the formula
                                    else:
                                        if Q.z_7 > 0.06432487443089485:
                                            if s['g'] - s['W'] > 1.9702812433242798:
                                                return 'q'   # 75% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 57% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 79% of the training jets here get this class from the formula
                    else:
                        if Q.mass > 39.697731018066406:
                            if s['q'] - s['t'] > 0.38902783393859863:
                                if s['q'] - s['W'] > 1.2084119319915771:
                                    return 'q'   # 90% of the training jets here get this class from the formula
                                else:
                                    if Q.max_dr > 0.253810852766037:
                                        if Q.LHA > 0.12503038346767426:
                                            if s['W'] - s['t'] > 1.0978858470916748:
                                                return 'W'   # 92% of the training jets here get this class from the formula
                                            else:
                                                if Q.tau21 > 0.2437506914138794:
                                                    return 'W'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 56% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass > 42.72229194641113:
                                                if Q.lam2 > 4.925140456180088e-05:
                                                    return 'q'   # 59% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 92% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 71% of the training jets here get this class from the formula
                                    else:
                                        if Q.lam1 > 0.0021483462769538164:
                                            return 'W'   # 56% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 90% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['t'] > -0.32000987231731415:
                                    if Q.lam2 > 0.00016743363812565804:
                                        return 'q'   # 74% of the training jets here get this class from the formula
                                    else:
                                        if Q.log_sum_pt > 6.6724560260772705:
                                            return 't'   # 91% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 50% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 96% of the training jets here get this class from the formula
                        else:
                            if Q.log_sum_pt > 6.991500377655029:
                                if s['g'] - s['q'] > -0.5807864367961884:
                                    if Q.z_7 > 0.01698392629623413:
                                        if s['Z'] - s['t'] > 1.5872096419334412:
                                            return 'g'   # 93% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > -0.3622780293226242:
                                                return 'g'   # 67% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 84% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt_top5 > 1093.296875:
                                            return 'q'   # 98% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 57% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['W'] > 1.6999986171722412:
                                        if Q.max_dr > 0.018848628737032413:
                                            return 'q'   # 90% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 61% of the training jets here get this class from the formula
                                    else:
                                        return 'q'   # 99% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['t'] > -0.08192676678299904:
                                    if s['q'] - s['Z'] > 0.6674122214317322:
                                        if Q.sum_pt > 752.640625:
                                            if s['g'] - s['W'] > 2.48014497756958:
                                                if Q.sum_pt > 1011.421875:
                                                    if s['g'] - s['q'] > -0.23847707360982895:
                                                        return 'g'   # 95% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 54% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 97% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['Z'] > 0.8774930238723755:
                                                    if Q.sum_pt > 1052.21484375:
                                                        if s['g'] - s['q'] > -0.38504624366760254:
                                                            return 'g'   # 91% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 99% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 100% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam2 > 4.6934957936173305e-05:
                                                        if Q.width > 0.0011909509194083512:
                                                            return 'W'   # 71% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.girth2 > 0.00036074177478440106:
                                                                return 'q'   # 90% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 77% of the training jets here get this class from the formula
                                                    else:
                                                        return 'q'   # 97% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth > 0.007132587255910039:
                                                if Q.centroid_offset > 0.0019061132334172726:
                                                    return 'q'   # 97% of the training jets here get this class from the formula
                                                else:
                                                    if Q.mass > 8.089913368225098:
                                                        return 'q'   # 96% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.log_sum_pt > 6.580660820007324:
                                                            if Q.pt_7 > 38.828125:
                                                                return 'q'   # 69% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.max_dr > 0.018603501841425896:
                                                                    return 'q'   # 50% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 80% of the training jets here get this class from the formula
                                            else:
                                                if Q.centroid_offset > 0.0022419107845053077:
                                                    if Q.sum_pt > 714.484375:
                                                        return 'q'   # 96% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.centroid_offset > 0.003732205484993756:
                                                            return 'q'   # 97% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.D2 > 2.6935527324676514:
                                                                return 'q'   # 68% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt > 730.078125:
                                                        if s['q'] - s['W'] > 2.7089688777923584:
                                                            return 'q'   # 80% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.centroid_offset > 0.001916632812935859:
                                                                return 'q'   # 65% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.planar_flow > 0.49148766696453094:
                                                                    return 'W'   # 94% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 36% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.z_7 > 0.015330298338085413:
                                                            return 'g'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 100% of the training jets here get this class from the formula
                                    else:
                                        if Q.planar_flow > 0.4018712490797043:
                                            if Q.C2 > 0.03193008899688721:
                                                return 'q'   # 54% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 89% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['t'] > 3.05367374420166:
                                                return 'q'   # 99% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['W'] > 0.4446510523557663:
                                                    return 'q'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    if Q.C2 > 0.01261212257668376:
                                                        return 'q'   # 62% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 83% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 78% of the training jets here get this class from the formula
                else:
                    if s['q'] - s['Z'] > 0.9465512931346893:
                        if Q.width > 0.002489391015842557:
                            if s['W'] - s['t'] > -0.15483789891004562:
                                if s['q'] - s['Z'] > 1.5315864086151123:
                                    if Q.girth2 > 0.0028953772271052003:
                                        return 'W'   # 84% of the training jets here get this class from the formula
                                    else:
                                        return 'q'   # 74% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 88% of the training jets here get this class from the formula
                            else:
                                return 't'   # 79% of the training jets here get this class from the formula
                        else:
                            if Q.centroid_offset > 0.015537379309535027:
                                if Q.width > 0.0014878867659717798:
                                    return 'W'   # 86% of the training jets here get this class from the formula
                                else:
                                    if Q.planar_flow > 0.11991298198699951:
                                        return 'W'   # 64% of the training jets here get this class from the formula
                                    else:
                                        return 'q'   # 69% of the training jets here get this class from the formula
                            else:
                                if Q.max_dr > 0.22947604209184647:
                                    return 'W'   # 77% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['t'] > 1.29762202501297:
                                        if s['g'] - s['q'] > -0.07738030329346657:
                                            return 'q'   # 40% of the training jets here get this class from the formula
                                        else:
                                            if Q.lam2 > 0.00019621593673946336:
                                                if Q.centroid_offset > 0.010462709236890078:
                                                    return 'W'   # 71% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 85% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['Z'] > 1.2298660278320312:
                                            if s['g'] - s['q'] > -0.15445271879434586:
                                                return 'g'   # 50% of the training jets here get this class from the formula
                                            else:
                                                return 'q'   # 75% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 73% of the training jets here get this class from the formula
                    else:
                        if s['q'] - s['W'] > 0.07177114859223366:
                            if Q.max_dr > 0.24212562292814255:
                                if s['g'] - s['t'] > -0.20412447303533554:
                                    return 'W'   # 95% of the training jets here get this class from the formula
                                else:
                                    return 'q'   # 42% of the training jets here get this class from the formula
                            else:
                                if Q.centroid_offset > 0.01878995541483164:
                                    return 'W'   # 82% of the training jets here get this class from the formula
                                else:
                                    if Q.eccentricity > 0.9062459170818329:
                                        if Q.e2_sq > 0.0017718981252983212:
                                            return 'W'   # 58% of the training jets here get this class from the formula
                                        else:
                                            return 'q'   # 84% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['Z'] > 0.6222279667854309:
                                            return 'q'   # 60% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 78% of the training jets here get this class from the formula
                        else:
                            if Q.girth2 > 0.002207112149335444:
                                if s['W'] - s['t'] > -0.1558440923690796:
                                    return 'W'   # 97% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 86% of the training jets here get this class from the formula
                            else:
                                if Q.centroid_offset > 0.015220357105135918:
                                    if Q.eccentricity > 0.9264200627803802:
                                        if Q.centroid_offset > 0.016941212117671967:
                                            return 'W'   # 91% of the training jets here get this class from the formula
                                        else:
                                            if Q.mass_over_sum_pt > 0.009506105445325375:
                                                if Q.mass > 27.291622161865234:
                                                    return 'W'   # 91% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 77% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 90% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 98% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['Z'] > 0.7354980409145355:
                                        if Q.sum_pt > 818.2734375:
                                            return 'q'   # 82% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 89% of the training jets here get this class from the formula
                                    else:
                                        if Q.lam2 > 9.217425758833997e-05:
                                            return 'W'   # 96% of the training jets here get this class from the formula
                                        else:
                                            if Q.max_dr > 0.2404305562376976:
                                                return 'W'   # 97% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['t'] > 1.738067865371704:
                                                    if Q.planar_flow > 0.28806017339229584:
                                                        return 'W'   # 93% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.lam1 > 0.0017140787676908076:
                                                            if s['q'] - s['Z'] > 0.5163258612155914:
                                                                return 'q'   # 68% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            return 'q'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 83% of the training jets here get this class from the formula
        else:
            if s['W'] - s['Z'] > -0.03962830640375614:
                if s['g'] - s['W'] > 0.16783524304628372:
                    if s['g'] - s['Z'] > 0.646447092294693:
                        if s['g'] - s['t'] > -0.12977824732661247:
                            if s['g'] - s['W'] > 0.4299886226654053:
                                if Q.D2 > 0.7229246497154236:
                                    if s['Z'] - s['t'] > 2.6072189807891846:
                                        if s['g'] - s['W'] > 0.6260449588298798:
                                            return 'g'   # 98% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.019989820197224617:
                                                if s['g'] - s['q'] > 1.5505208373069763:
                                                    return 'g'   # 96% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt_top5 > 631.65625:
                                                        return 'W'   # 88% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 64% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 88% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 100% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['Z'] > 1.0104705095291138:
                                        return 'g'   # 96% of the training jets here get this class from the formula
                                    else:
                                        if Q.planar_flow > 0.22115660458803177:
                                            return 'W'   # 53% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 87% of the training jets here get this class from the formula
                            else:
                                if s['Z'] - s['t'] > 2.7161648273468018:
                                    if Q.centroid_offset > 0.018493029288947582:
                                        return 'W'   # 86% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['t'] > 3.720907688140869:
                                            return 'W'   # 60% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 98% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 1.2000786066055298:
                                        return 'g'   # 94% of the training jets here get this class from the formula
                                    else:
                                        if Q.D2 > 0.84942227602005:
                                            if Q.sum_pt_top5 > 609.5:
                                                if Q.centroid_offset > 0.019442083314061165:
                                                    return 'W'   # 81% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 88% of the training jets here get this class from the formula
                                            else:
                                                if Q.LHA > 0.20873714983463287:
                                                    if Q.sum_pt > 584.1953125:
                                                        return 'W'   # 66% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 93% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['Z'] > 1.0010147094726562:
                                                return 'g'   # 82% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 65% of the training jets here get this class from the formula
                        else:
                            return 't'   # 88% of the training jets here get this class from the formula
                    else:
                        if Q.sum_pt_top5 > 572.21875:
                            if Q.sum_pt > 981.203125:
                                return 'g'   # 80% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['Z'] > 0.5027133822441101:
                                    if s['Z'] - s['t'] > 2.536502242088318:
                                        if Q.girth2 > 0.0003796661621890962:
                                            if s['q'] - s['t'] > 2.07948100566864:
                                                return 'W'   # 95% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 50% of the training jets here get this class from the formula
                                        else:
                                            if Q.tau21 > 0.6920114159584045:
                                                return 'g'   # 92% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 56% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 62% of the training jets here get this class from the formula
                                else:
                                    if s['q'] - s['Z'] > -1.0152002573013306:
                                        return 'W'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if Q.width > 0.0007276593532878906:
                                            return 'g'   # 44% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 72% of the training jets here get this class from the formula
                        else:
                            if s['W'] - s['t'] > -0.20666977018117905:
                                if Q.D2 > 0.7467233538627625:
                                    if s['g'] - s['W'] > 0.33841556310653687:
                                        return 'g'   # 91% of the training jets here get this class from the formula
                                    else:
                                        if Q.e2 > 0.006199629977345467:
                                            if Q.centroid_offset > 0.03689023479819298:
                                                return 'Z'   # 40% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 15.895688533782959:
                                                    if s['q'] - s['t'] > 0.32097165286540985:
                                                        return 'W'   # 73% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 91% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['t'] > 0.9857484698295593:
                                                if s['W'] - s['t'] > 1.9280138611793518:
                                                    return 'W'   # 82% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 49% of the training jets here get this class from the formula
                                            else:
                                                if Q.centroid_offset > 0.03140249103307724:
                                                    return 'Z'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 53% of the training jets here get this class from the formula
                                else:
                                    return 'W'   # 74% of the training jets here get this class from the formula
                            else:
                                return 't'   # 71% of the training jets here get this class from the formula
                else:
                    if s['W'] - s['Z'] > 0.18042009323835373:
                        if s['g'] - s['W'] > -0.22038759291172028:
                            if s['g'] - s['q'] > 1.1155695915222168:
                                if s['g'] - s['Z'] > 0.9131478667259216:
                                    if Q.lam2 > 0.0005851544847246259:
                                        if Q.mass > 28.37814712524414:
                                            return 'W'   # 70% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 73% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 80% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 1.45563542842865:
                                        if s['g'] - s['W'] > -0.04621455259621143:
                                            if s['q'] - s['t'] > 1.058471143245697:
                                                return 'W'   # 58% of the training jets here get this class from the formula
                                            else:
                                                if Q.LHA > 0.2116849645972252:
                                                    if Q.sum_pt > 586.828125:
                                                        if s['q'] - s['W'] > -1.9399433135986328:
                                                            return 'W'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 77% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 81% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 93% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['W'] > -2.1632230281829834:
                                                if Q.pt_7 > 45.703125:
                                                    return 'W'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['Z'] > 0.4166675806045532:
                                                        return 'g'   # 74% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 52% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_7 > 41.859375:
                                            if s['g'] - s['q'] > 1.3193594813346863:
                                                if Q.mass > 17.655454635620117:
                                                    return 'W'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 50% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 87% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['W'] > -0.03253598138689995:
                                                if Q.lam2 > 0.0005158364947419614:
                                                    return 'W'   # 64% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 75% of the training jets here get this class from the formula
                                            else:
                                                if Q.LHA > 0.1935158148407936:
                                                    return 'W'   # 69% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 80% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['Z'] > 0.6863387823104858:
                                    if Q.pt_7 > 33.375:
                                        if s['g'] - s['Z'] > 1.0268301367759705:
                                            return 'g'   # 59% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth > 0.03652854263782501:
                                                return 'W'   # 82% of the training jets here get this class from the formula
                                            else:
                                                if Q.log_sum_pt > 6.590150594711304:
                                                    return 'W'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 79% of the training jets here get this class from the formula
                                    else:
                                        if Q.planar_flow > 0.6033943593502045:
                                            return 'W'   # 69% of the training jets here get this class from the formula
                                        else:
                                            if Q.tau21 > 0.2610696852207184:
                                                return 'g'   # 89% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 44% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['t'] > -0.20654889196157455:
                                        if Q.sum_pt > 1010.734375:
                                            return 'g'   # 78% of the training jets here get this class from the formula
                                        else:
                                            if Q.log_sum_pt > 6.541886329650879:
                                                return 'W'   # 96% of the training jets here get this class from the formula
                                            else:
                                                if Q.LHA > 0.19761501252651215:
                                                    if Q.sum_pt > 565.8828125:
                                                        return 'W'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['W'] > -0.0015754812629893422:
                                                            if Q.D2 > 1.3206177949905396:
                                                                return 'g'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 73% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 81% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt > 669.4609375:
                                                        return 'W'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 72% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 94% of the training jets here get this class from the formula
                        else:
                            if s['W'] - s['t'] > 0.1610332429409027:
                                if s['W'] - s['Z'] > 0.38308659195899963:
                                    if s['g'] - s['Z'] > 0.91417396068573:
                                        if Q.girth > 0.03954074718058109:
                                            if Q.log_sum_pt > 6.78125262260437:
                                                return 'g'   # 73% of the training jets here get this class from the formula
                                            else:
                                                if Q.centroid_offset > 0.01592219341546297:
                                                    if s['g'] - s['W'] > -0.4347890019416809:
                                                        if Q.planar_flow > 0.34218698740005493:
                                                            return 'W'   # 76% of the training jets here get this class from the formula
                                                        else:
                                                            if s['q'] - s['W'] > -1.543021321296692:
                                                                return 'W'   # 56% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 80% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 94% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > 1.5875188112258911:
                                                return 'g'   # 94% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 33.25420379638672:
                                                    return 'W'   # 72% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 67% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['W'] > -0.566604346036911:
                                            if Q.log_sum_pt > 6.816906929016113:
                                                if s['q'] - s['t'] > 1.8743690848350525:
                                                    return 'W'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['t'] > 1.706508457660675:
                                                        return 'g'   # 79% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 67% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['q'] > 1.4328007102012634:
                                                    if Q.mass > 26.978073120117188:
                                                        return 'W'   # 92% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.pt_0 > 127.96875:
                                                            return 'W'   # 71% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 69% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['Z'] > 0.8103291094303131:
                                                        if Q.tau21 > 0.4841887205839157:
                                                            return 'g'   # 56% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 95% of the training jets here get this class from the formula
                                        else:
                                            if s['W'] - s['Z'] > 0.5632520616054535:
                                                if s['W'] - s['t'] > 0.38183924555778503:
                                                    return 'W'   # 100% of the training jets here get this class from the formula
                                                else:
                                                    if Q.z_dr_0p1_0p2 > 0.2637655735015869:
                                                        return 't'   # 56% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 92% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 98% of the training jets here get this class from the formula
                                else:
                                    if Q.max_dr > 0.16500529646873474:
                                        if Q.girth2 > 0.0034189592115581036:
                                            if Q.centroid_offset > 0.015718940645456314:
                                                if Q.lam1 > 0.003900569397956133:
                                                    if Q.lam2 > 0.00012388690083753318:
                                                        if Q.D2 > 2.084856152534485:
                                                            return 'Z'   # 66% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.max_dr > 0.17455267906188965:
                                                            return 'Z'   # 88% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.log_sum_pt > 6.552060604095459:
                                                                if s['W'] - s['Z'] > 0.25045034289360046:
                                                                    return 'W'   # 84% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 59% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 88% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.02325025387108326:
                                                        if Q.max_dr > 0.1769418716430664:
                                                            return 'Z'   # 89% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 52% of the training jets here get this class from the formula
                                                    else:
                                                        if s['W'] - s['Z'] > 0.25551433861255646:
                                                            return 'W'   # 78% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.z_dr_0p2_0p4 > 0.04768459498882294:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.max_dr > 0.18080630898475647:
                                                                    return 'Z'   # 73% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 72% of the training jets here get this class from the formula
                                            else:
                                                if Q.C2 > 0.045649681240320206:
                                                    if s['g'] - s['t'] > 0.01200864277780056:
                                                        if Q.eccentricity > 0.9859735369682312:
                                                            if Q.e2_sq > 0.003964449046179652:
                                                                return 'Z'   # 67% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 81% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 91% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.planar_flow > 0.0879785604774952:
                                                            if Q.lam1 > 0.003759061684831977:
                                                                return 'W'   # 73% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 63% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.e2 > 0.015438146889209747:
                                                                return 'Z'   # 82% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 53% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['t'] > -1.528842031955719:
                                                        if Q.centroid_offset > 0.013304037507623434:
                                                            if s['g'] - s['q'] > -1.02716863155365:
                                                                return 'W'   # 88% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 57% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 96% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['q'] > -0.2189907655119896:
                                                            return 'W'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 63% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 96% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt > 991.40625:
                                            if s['q'] - s['t'] > -1.3526520729064941:
                                                return 'W'   # 77% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 79% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.029840567149221897:
                                                if Q.max_dr > 0.05878339894115925:
                                                    if s['g'] - s['t'] > 1.5805611610412598:
                                                        return 'Z'   # 50% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['Z'] > -1.5084295272827148:
                                                        if Q.C2 > 0.011780120432376862:
                                                            return 'W'   # 72% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 95% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 95% of the training jets here get this class from the formula
                            else:
                                if s['W'] - s['t'] > -0.11761908605694771:
                                    if Q.z_dr_0p05_0p1 > 0.05776963196694851:
                                        if s['q'] - s['W'] > -1.815471351146698:
                                            if s['g'] - s['q'] > 0.6966279447078705:
                                                return 't'   # 50% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 88% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 68% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 60% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 86% of the training jets here get this class from the formula
                    else:
                        if Q.max_dr > 0.16152845323085785:
                            if Q.width > 0.0032723640324547887:
                                if Q.centroid_offset > 0.013197563122957945:
                                    if Q.LHA > 0.2230273261666298:
                                        if Q.lam2 > 0.00014108754112385213:
                                            if Q.D2 > 2.0941717624664307:
                                                if Q.girth2 > 0.003754008677788079:
                                                    return 'Z'   # 88% of the training jets here get this class from the formula
                                                else:
                                                    if Q.D2 > 2.868187427520752:
                                                        return 'Z'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 69% of the training jets here get this class from the formula
                                            else:
                                                if Q.tau21 > 0.4724958539009094:
                                                    return 'W'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    if Q.C2 > 0.03821946494281292:
                                                        return 'Z'   # 70% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 72% of the training jets here get this class from the formula
                                        else:
                                            if s['Z'] - s['t'] > 0.08747573569417:
                                                if s['W'] - s['Z'] > 0.130096435546875:
                                                    if Q.max_dr > 0.17315994203090668:
                                                        if Q.girth > 0.04695654660463333:
                                                            return 'Z'   # 96% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 54% of the training jets here get this class from the formula
                                                    else:
                                                        if s['q'] - s['Z'] > -2.33799409866333:
                                                            return 'Z'   # 64% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 90% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 92% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 60% of the training jets here get this class from the formula
                                    else:
                                        if Q.C2 > 0.041489411145448685:
                                            if s['g'] - s['Z'] > -1.308912992477417:
                                                if s['g'] - s['t'] > 0.2128773108124733:
                                                    if Q.girth2 > 0.0035393371945247054:
                                                        return 'Z'   # 52% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 96% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 69% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 84% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['t'] > 0.05681146867573261:
                                                return 'W'   # 84% of the training jets here get this class from the formula
                                            else:
                                                if Q.C2 > 0.03524821065366268:
                                                    return 'Z'   # 73% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 67% of the training jets here get this class from the formula
                                else:
                                    if s['Z'] - s['t'] > 0.006042810273356736:
                                        if Q.C2 > 0.04395356588065624:
                                            if Q.eccentricity > 0.9775417149066925:
                                                if Q.lam1 > 0.003744843532331288:
                                                    return 'Z'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.D2 > 4.489556312561035:
                                                        return 'Z'   # 90% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 85% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['t'] > -0.17973150312900543:
                                                    return 'W'   # 75% of the training jets here get this class from the formula
                                                else:
                                                    if Q.z_dr_0p05_0p1 > 0.08501585945487022:
                                                        return 'W'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 79% of the training jets here get this class from the formula
                                        else:
                                            if Q.sum_pt > 903.88671875:
                                                if Q.n_dr_0p2_0p4 > 0.5:
                                                    return 'W'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['Z'] > 0.1039045937359333:
                                                        return 'W'   # 90% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['t'] > -0.9634232819080353:
                                                            return 'Z'   # 65% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 78% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['t'] > -1.3825573325157166:
                                                    if Q.D2 > 1.7052454948425293:
                                                        if Q.lam1 > 0.004383517196401954:
                                                            return 'Z'   # 90% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 89% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.LHA > 0.2259414866566658:
                                                            if Q.max_dr > 0.16979342699050903:
                                                                if s['W'] - s['Z'] > 0.06844272091984749:
                                                                    return 'W'   # 68% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 62% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 92% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 92% of the training jets here get this class from the formula
                                                else:
                                                    if Q.max_dr > 0.17064651101827621:
                                                        return 'Z'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.planar_flow > 0.02627034019678831:
                                                            return 'W'   # 79% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 64% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 91% of the training jets here get this class from the formula
                            else:
                                if Q.LHA > 0.22076043486595154:
                                    if Q.max_dr > 0.17520925402641296:
                                        if s['W'] - s['Z'] > 0.0821412205696106:
                                            return 'W'   # 66% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.02405739389359951:
                                                return 'Z'   # 79% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 58% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt > 698.3125:
                                            return 'W'   # 91% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 55% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['t'] > -0.30585676431655884:
                                        if s['g'] - s['W'] > -0.2255592718720436:
                                            return 'g'   # 52% of the training jets here get this class from the formula
                                        else:
                                            if Q.width > 0.0026162891881540418:
                                                if s['W'] - s['Z'] > 0.0013947252300567925:
                                                    if s['g'] - s['Z'] > -2.2790852785110474:
                                                        return 'W'   # 92% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.D2 > 4.387287139892578:
                                                            return 'Z'   # 76% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.z_dr_0p2_0p4 > 0.03686434030532837:
                                                        return 'W'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 65% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 96% of the training jets here get this class from the formula
                                    else:
                                        if Q.C2 > 0.055844008922576904:
                                            return 'Z'   # 81% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 68% of the training jets here get this class from the formula
                        else:
                            if Q.max_dr > 0.06495814770460129:
                                if s['W'] - s['t'] > 0.005788545357063413:
                                    if s['g'] - s['t'] > -1.270478367805481:
                                        if Q.log_sum_pt > 6.879114627838135:
                                            if s['q'] - s['t'] > -1.2505109310150146:
                                                if Q.lam2 > 1.14173653855687e-05:
                                                    return 'W'   # 74% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 59% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 75% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.03086940571665764:
                                                if s['g'] - s['t'] > 1.049023985862732:
                                                    if s['g'] - s['q'] > 1.2080600261688232:
                                                        return 'Z'   # 61% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 53% of the training jets here get this class from the formula
                                                else:
                                                    if Q.C2 > 0.019311961717903614:
                                                        return 'W'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.lam2 > 6.960048995097168e-05:
                                                            return 'Z'   # 73% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 88% of the training jets here get this class from the formula
                                            else:
                                                if s['W'] - s['Z'] > 0.043021298944950104:
                                                    return 'W'   # 92% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.009958837646991014:
                                                        if Q.max_dr > 0.15655890852212906:
                                                            return 'W'   # 54% of the training jets here get this class from the formula
                                                        else:
                                                            if s['Z'] - s['t'] > 0.5594019889831543:
                                                                return 'W'   # 88% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.tau32 > 0.6223526298999786:
                                                                    return 'Z'   # 51% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.max_dr > 0.10674167051911354:
                                                            if Q.LHA > 0.2988881468772888:
                                                                return 'Z'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 90% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 92% of the training jets here get this class from the formula
                                    else:
                                        if Q.max_dr > 0.10464214161038399:
                                            if s['q'] - s['t'] > -1.6284051537513733:
                                                if Q.D2 > 0.323819175362587:
                                                    return 'W'   # 80% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 56% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_dr_0p05_0p1 > 0.19221039861440659:
                                                    if s['W'] - s['Z'] > 0.05699976719915867:
                                                        if Q.max_dr > 0.11425026878714561:
                                                            if Q.z_dr_0p05_0p1 > 0.5862816572189331:
                                                                if Q.max_dr > 0.12805218249559402:
                                                                    return 'Z'   # 84% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 51% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 71% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.centroid_offset > 0.004796778317540884:
                                                                return 'W'   # 94% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 56% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 87% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 90% of the training jets here get this class from the formula
                                else:
                                    if Q.max_dr > 0.10081162676215172:
                                        return 't'   # 75% of the training jets here get this class from the formula
                                    else:
                                        return 'W'   # 49% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['Z'] > -0.904914915561676:
                                    if Q.planar_flow > 0.04178392514586449:
                                        if Q.planar_flow > 0.05560809373855591:
                                            return 'W'   # 96% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > -0.693242758512497:
                                                return 'W'   # 86% of the training jets here get this class from the formula
                                            else:
                                                if Q.sum_pt_top5 > 694.421875:
                                                    return 'W'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 96% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['Z'] > -0.5104126334190369:
                                            if Q.centroid_offset > 0.02981366030871868:
                                                return 'Z'   # 89% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 80% of the training jets here get this class from the formula
                                        else:
                                            if Q.planar_flow > 0.033579859882593155:
                                                if s['W'] - s['Z'] > 0.06546306237578392:
                                                    return 'W'   # 64% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 94% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 98% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.022955610416829586:
                                        if Q.eccentricity > 0.982343316078186:
                                            return 'Z'   # 98% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > -1.13508540391922:
                                                if Q.D2 > 1.6341639757156372:
                                                    return 'W'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    if s['W'] - s['Z'] > 0.0765199325978756:
                                                        return 'W'   # 66% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if Q.planar_flow > 0.06354067474603653:
                                            return 'W'   # 83% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 85% of the training jets here get this class from the formula
            else:
                if s['g'] - s['Z'] > 0.1209823340177536:
                    if s['g'] - s['t'] > 0.019957855343818665:
                        if s['g'] - s['Z'] > 0.39850880205631256:
                            if s['g'] - s['t'] > 0.15147841721773148:
                                if s['g'] - s['Z'] > 0.5617084205150604:
                                    return 'g'   # 98% of the training jets here get this class from the formula
                                else:
                                    if s['W'] - s['t'] > 2.462747097015381:
                                        if s['g'] - s['q'] > 1.9055005311965942:
                                            return 'g'   # 85% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 58% of the training jets here get this class from the formula
                                    else:
                                        if Q.lam1 > 0.00124847557162866:
                                            if s['W'] - s['t'] > -0.07000169157981873:
                                                if Q.centroid_offset > 0.04060600325465202:
                                                    return 'Z'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt > 599.328125:
                                                        if Q.tau21 > 0.26434819400310516:
                                                            if Q.pt_0 > 147.875:
                                                                return 'Z'   # 61% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 74% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 62% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 90% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 89% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 99% of the training jets here get this class from the formula
                            else:
                                if Q.mass > 21.875595092773438:
                                    if Q.log_sum_pt > 6.196028470993042:
                                        return 't'   # 58% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 70% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 100% of the training jets here get this class from the formula
                        else:
                            if s['q'] - s['t'] > 1.4074439406394958:
                                if s['q'] - s['Z'] > -1.0510644912719727:
                                    if Q.C2 > 0.010838910937309265:
                                        return 'g'   # 69% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['Z'] > 0.2878127098083496:
                                            if Q.sum_pt_top5 > 576.640625:
                                                return 'W'   # 88% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 59% of the training jets here get this class from the formula
                                        else:
                                            return 'W'   # 89% of the training jets here get this class from the formula
                                else:
                                    return 'Z'   # 71% of the training jets here get this class from the formula
                            else:
                                if s['W'] - s['t'] > -0.01753606926649809:
                                    if Q.centroid_offset > 0.033306779339909554:
                                        if Q.max_dr > 0.0998011901974678:
                                            return 'g'   # 82% of the training jets here get this class from the formula
                                        else:
                                            if Q.log_sum_pt > 6.533334493637085:
                                                return 'g'   # 71% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['Z'] > 0.25673985481262207:
                                                    if Q.centroid_offset > 0.03466638922691345:
                                                        if s['Z'] - s['t'] > 0.8453521728515625:
                                                            if Q.C2 > 0.009758605156093836:
                                                                if Q.z_dr_0p05_0p1 > 0.25433872640132904:
                                                                    return 'Z'   # 78% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 61% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 94% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 56% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 74% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['Z'] > 0.23054056614637375:
                                            if Q.D2 > 0.6421391069889069:
                                                if s['W'] - s['t'] > 2.0424941778182983:
                                                    if s['g'] - s['q'] > 1.8143072128295898:
                                                        return 'g'   # 77% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 87% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 83% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_7 > 0.05753649026155472:
                                                if Q.e2_sq > 0.00021279850625433028:
                                                    return 'g'   # 53% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 79% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['Z'] > -0.20916727930307388:
                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 72% of the training jets here get this class from the formula
                                else:
                                    if Q.e2 > 0.009705619420856237:
                                        if Q.log_sum_pt > 6.207362651824951:
                                            if Q.mass > 24.77659320831299:
                                                if s['W'] - s['Z'] > -0.6301596164703369:
                                                    return 'g'   # 37% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['Z'] > -2.0203882455825806:
                                                        return 'Z'   # 65% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 66% of the training jets here get this class from the formula
                                            else:
                                                if Q.max_dr > 0.06596669554710388:
                                                    return 'g'   # 78% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 71% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 76% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 90% of the training jets here get this class from the formula
                    else:
                        if s['g'] - s['t'] > -0.1531439647078514:
                            if Q.mass_over_sum_pt > 0.030452982522547245:
                                if s['q'] - s['W'] > 0.21195346117019653:
                                    return 't'   # 70% of the training jets here get this class from the formula
                                else:
                                    return 'g'   # 43% of the training jets here get this class from the formula
                            else:
                                return 'g'   # 100% of the training jets here get this class from the formula
                        else:
                            if Q.C2 > 0.008920400403439999:
                                return 't'   # 96% of the training jets here get this class from the formula
                            else:
                                return 'Z'   # 41% of the training jets here get this class from the formula
                else:
                    if s['Z'] - s['t'] > 0.03433539718389511:
                        if s['W'] - s['Z'] > -0.24207814037799835:
                            if Q.LHA > 0.2626188099384308:
                                if s['g'] - s['t'] > -1.0602632761001587:
                                    if Q.max_dr > 0.1603684350848198:
                                        if Q.e2 > 0.03331614285707474:
                                            if Q.LHA > 0.2754798084497452:
                                                return 'Z'   # 80% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 84% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['Z'] > -0.16021107137203217:
                                            if Q.log_sum_pt > 6.478605508804321:
                                                if Q.sum_pt > 990.4140625:
                                                    return 'Z'   # 61% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['t'] > -0.7581509351730347:
                                                        return 'W'   # 90% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.centroid_offset > 0.0191199854016304:
                                                            return 'W'   # 88% of the training jets here get this class from the formula
                                                        else:
                                                            if s['g'] - s['W'] > -2.694578528404236:
                                                                return 'Z'   # 64% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 76% of the training jets here get this class from the formula
                                            else:
                                                if Q.max_dr > 0.11964813992381096:
                                                    if Q.LHA > 0.28966274857521057:
                                                        return 'Z'   # 75% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.e2 > 0.034207360818982124:
                                                            return 'W'   # 96% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.planar_flow > 0.22151515632867813:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.D2 > 1.1219325065612793:
                                                                    return 'Z'   # 71% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 71% of the training jets here get this class from the formula
                                                else:
                                                    if Q.planar_flow > 0.06320425122976303:
                                                        if Q.eccentricity > 0.9256001114845276:
                                                            if Q.z_dr_0p05_0p1 > 0.770937979221344:
                                                                if Q.mass > 39.862064361572266:
                                                                    return 'W'   # 66% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 74% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 78% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 89% of the training jets here get this class from the formula
                                        else:
                                            if Q.girth2 > 0.005110297817736864:
                                                if Q.max_dr > 0.11772669479250908:
                                                    if Q.z_dr_0p05_0p1 > 0.5708751976490021:
                                                        return 'Z'   # 82% of the training jets here get this class from the formula
                                                    else:
                                                        if s['g'] - s['Z'] > -1.919761598110199:
                                                            return 'W'   # 70% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 70% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['t'] > -1.4421705603599548:
                                                        return 'W'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.eccentricity > 0.9881392121315002:
                                                            if Q.sum_pt_top5 > 637.78125:
                                                                return 'Z'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 74% of the training jets here get this class from the formula
                                            else:
                                                if Q.log_sum_pt > 6.454067707061768:
                                                    if Q.max_dr > 0.1439816877245903:
                                                        return 'Z'   # 64% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 86% of the training jets here get this class from the formula
                                                else:
                                                    if Q.e2 > 0.027139109559357166:
                                                        return 'W'   # 69% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 70% of the training jets here get this class from the formula
                                else:
                                    if Q.max_dr > 0.10133268684148788:
                                        if Q.centroid_offset > 0.018878419883549213:
                                            if s['W'] - s['t'] > 0.5871478915214539:
                                                if Q.max_dr > 0.15140295773744583:
                                                    return 'Z'   # 83% of the training jets here get this class from the formula
                                                else:
                                                    if Q.e2_sq > 0.005071715218946338:
                                                        if Q.e2 > 0.034004827961325645:
                                                            return 'W'   # 77% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 86% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 81% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 73% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_dr_0p05_0p1 > 0.46439166367053986:
                                                if s['W'] - s['Z'] > -0.07094752416014671:
                                                    if Q.max_dr > 0.11213334277272224:
                                                        return 'Z'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 90% of the training jets here get this class from the formula
                                            else:
                                                if Q.e2 > 0.03488345444202423:
                                                    return 'W'   # 72% of the training jets here get this class from the formula
                                                else:
                                                    if Q.lam2 > 6.414120434783399e-05:
                                                        if Q.centroid_offset > 0.012609853409230709:
                                                            return 'Z'   # 76% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 75% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 88% of the training jets here get this class from the formula
                                    else:
                                        if Q.planar_flow > 0.09949289634823799:
                                            return 'Z'   # 81% of the training jets here get this class from the formula
                                        else:
                                            if Q.max_dr > 0.0972302220761776:
                                                if s['W'] - s['Z'] > -0.12962836772203445:
                                                    return 'W'   # 85% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 62% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 90% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['Z'] > -0.8769606947898865:
                                    if Q.planar_flow > 0.06919309496879578:
                                        if Q.width > 0.00303023646119982:
                                            if s['g'] - s['t'] > 0.1397135928273201:
                                                return 'W'   # 50% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 80% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.029653185978531837:
                                                if Q.D2 > 2.3939855098724365:
                                                    return 'W'   # 77% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 75% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['Z'] > -0.7338502109050751:
                                                    return 'W'   # 89% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.024771127849817276:
                                                        if Q.z_7 > 0.04797929897904396:
                                                            return 'W'   # 77% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.e2 > 0.004318527411669493:
                                                                return 'W'   # 68% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 87% of the training jets here get this class from the formula
                                    else:
                                        if s['q'] - s['t'] > 1.4562053084373474:
                                            if Q.centroid_offset > 0.025630122050642967:
                                                if s['q'] - s['W'] > -0.5314581990242004:
                                                    return 'W'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 100% of the training jets here get this class from the formula
                                            else:
                                                if Q.max_dr > 0.30415481328964233:
                                                    return 'Z'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 76% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_dr_0p1_0p2 > 0.006375353317707777:
                                                if Q.max_dr > 0.16094526648521423:
                                                    return 'Z'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 68% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 83% of the training jets here get this class from the formula
                                else:
                                    if Q.D2 > 3.704772710800171:
                                        if Q.girth2 > 0.0026324900100007653:
                                            if Q.girth2 > 0.002887316979467869:
                                                return 'Z'   # 94% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_dr_0p2_0p4 > 0.027486003935337067:
                                                    if Q.pt_7 > 22.9375:
                                                        return 'W'   # 71% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 85% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 96% of the training jets here get this class from the formula
                                        else:
                                            if Q.e2_sq > 0.000450610852567479:
                                                if Q.girth2 > 0.0022938286419957876:
                                                    if Q.pt_7 > 22.921875:
                                                        return 'W'   # 80% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['q'] > 0.06352286785840988:
                                                        return 'Z'   # 44% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 89% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 71% of the training jets here get this class from the formula
                                    else:
                                        if Q.mass > 14.576708793640137:
                                            if Q.max_dr > 0.16421034187078476:
                                                if Q.LHA > 0.21704255789518356:
                                                    if Q.centroid_offset > 0.012610387988388538:
                                                        if Q.e2 > 0.027076696045696735:
                                                            if Q.z_dr_0p1_0p2 > 0.07649414241313934:
                                                                return 'Z'   # 83% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 57% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 97% of the training jets here get this class from the formula
                                                    else:
                                                        if s['W'] - s['Z'] > -0.07178198546171188:
                                                            return 'Z'   # 54% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.e2 > 0.034631961956620216:
                                                                return 'W'   # 55% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.z_7 > 0.01444898871704936:
                                                                    return 'Z'   # 87% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 55% of the training jets here get this class from the formula
                                                else:
                                                    if Q.max_dr > 0.23715825378894806:
                                                        if Q.C2 > 0.03165440261363983:
                                                            if s['W'] - s['Z'] > -0.12774298340082169:
                                                                if Q.pt_0 > 507.375:
                                                                    return 'W'   # 58% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 87% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 98% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 52% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.C2 > 0.044723669067025185:
                                                            return 'Z'   # 74% of the training jets here get this class from the formula
                                                        else:
                                                            if s['g'] - s['q'] > 0.35100172460079193:
                                                                return 'Z'   # 59% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.max_dr > 0.21939228475093842:
                                                                    if Q.LHA > 0.21061506122350693:
                                                                        return 'Z'   # 69% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 83% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 90% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 25.873957633972168:
                                                    if Q.max_dr > 0.15012642741203308:
                                                        if s['W'] - s['t'] > 1.7471108436584473:
                                                            if Q.z_dr_0p1_0p2 > 0.11774158850312233:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                            else:
                                                                if s['W'] - s['Z'] > -0.11130602285265923:
                                                                    return 'W'   # 62% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 74% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        if s['q'] - s['t'] > -1.0980448722839355:
                                                            if Q.lam2 > 6.371160998241976e-05:
                                                                if Q.e2 > 0.019006232731044292:
                                                                    return 'W'   # 79% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 68% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.029223360121250153:
                                                        if Q.max_dr > 0.11093220114707947:
                                                            return 'g'   # 37% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 87% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 59% of the training jets here get this class from the formula
                                        else:
                                            if Q.centroid_offset > 0.02408561483025551:
                                                if s['g'] - s['q'] > 2.018781304359436:
                                                    return 'g'   # 54% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['Z'] > -1.0071192383766174:
                                                        if Q.centroid_offset > 0.024912647902965546:
                                                            return 'Z'   # 91% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 54% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 99% of the training jets here get this class from the formula
                                            else:
                                                if s['q'] - s['W'] > -0.9854938983917236:
                                                    return 'W'   # 65% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 88% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['Z'] > -0.4747016131877899:
                                if Q.centroid_offset > 0.04206143133342266:
                                    if Q.e2 > 0.013702691998332739:
                                        return 'Z'   # 87% of the training jets here get this class from the formula
                                    else:
                                        if s['W'] - s['Z'] > -1.6000466346740723:
                                            if Q.z_dr_0p05_0p1 > 0.25879234075546265:
                                                if s['g'] - s['W'] > 1.0134735107421875:
                                                    if Q.log_sum_pt > 6.533175468444824:
                                                        return 'g'   # 74% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 68% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 88% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 88% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 92% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['q'] > 2.182267189025879:
                                        if s['Z'] - s['t'] > 1.1826080679893494:
                                            if Q.max_dr > 0.03292000666260719:
                                                return 'g'   # 86% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 56% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_7 > 29.0234375:
                                            if Q.lam1 > 0.0015611646231263876:
                                                if Q.mass > 4.835028171539307:
                                                    if s['g'] - s['Z'] > -0.10450104251503944:
                                                        if Q.centroid_offset > 0.03758665360510349:
                                                            return 'Z'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.centroid_offset > 0.01924626249819994:
                                                                if Q.max_dr > 0.1064607985317707:
                                                                    if Q.z_dr_0p05_0p1 > 0.4593840390443802:
                                                                        return 'Z'   # 54% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'g'   # 80% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 52% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 71% of the training jets here get this class from the formula
                                                    else:
                                                        if s['W'] - s['Z'] > -0.5098027586936951:
                                                            if Q.pt_7 > 44.71875:
                                                                return 'W'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.z_dr_0p1_0p2 > 0.14397016167640686:
                                                                    return 'W'   # 47% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 78% of the training jets here get this class from the formula
                                                        else:
                                                            if s['Z'] - s['t'] > 0.23531320691108704:
                                                                return 'Z'   # 91% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.sum_pt > 518.546875:
                                                                    return 'Z'   # 90% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.D2 > 1.2458652257919312:
                                                                        return 't'   # 44% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['t'] > 0.16048698127269745:
                                                        return 'Z'   # 76% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 91% of the training jets here get this class from the formula
                                            else:
                                                if Q.mass > 15.398066520690918:
                                                    return 'W'   # 56% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['t'] > -0.09869606047868729:
                                                        if s['q'] - s['Z'] > -0.7910111248493195:
                                                            if Q.width > 0.000951393652940169:
                                                                return 'Z'   # 95% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 74% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 98% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 59% of the training jets here get this class from the formula
                                        else:
                                            if s['g'] - s['q'] > 0.04501577094197273:
                                                if Q.D2 > 2.716844081878662:
                                                    if Q.z_7 > 0.031848061829805374:
                                                        if s['W'] - s['t'] > 0.25889623165130615:
                                                            return 'W'   # 64% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 36% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 67% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 70% of the training jets here get this class from the formula
                                            else:
                                                if Q.pt_7 > 24.6484375:
                                                    return 'W'   # 56% of the training jets here get this class from the formula
                                                else:
                                                    return 'q'   # 70% of the training jets here get this class from the formula
                            else:
                                if s['W'] - s['Z'] > -0.4057809114456177:
                                    if Q.z_dr_0p05_0p1 > 0.181174635887146:
                                        if s['g'] - s['t'] > -0.7816236019134521:
                                            if Q.planar_flow > 0.03830554150044918:
                                                if Q.max_dr > 0.11882564797997475:
                                                    if Q.z_dr_0p05_0p1 > 0.6980754137039185:
                                                        return 'Z'   # 92% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.e2 > 0.030868371948599815:
                                                            if Q.LHA > 0.28192394971847534:
                                                                return 'Z'   # 85% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.max_dr > 0.15812288969755173:
                                                                    return 'Z'   # 60% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'W'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.max_dr > 0.14567720144987106:
                                                                return 'Z'   # 94% of the training jets here get this class from the formula
                                                            else:
                                                                if s['q'] - s['t'] > -0.7010699510574341:
                                                                    return 'W'   # 62% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 85% of the training jets here get this class from the formula
                                                else:
                                                    if s['q'] - s['t'] > -1.4428375363349915:
                                                        if Q.centroid_offset > 0.0328183826059103:
                                                            return 'Z'   # 74% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 70% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 80% of the training jets here get this class from the formula
                                            else:
                                                if Q.max_dr > 0.14292936772108078:
                                                    return 'Z'   # 93% of the training jets here get this class from the formula
                                                else:
                                                    if Q.mass > 66.74995040893555:
                                                        return 'Z'   # 97% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.width > 0.00496425642631948:
                                                            if Q.max_dr > 0.12020351737737656:
                                                                return 'Z'   # 68% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 70% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 85% of the training jets here get this class from the formula
                                        else:
                                            if Q.max_dr > 0.0925341434776783:
                                                if Q.max_dr > 0.10112891718745232:
                                                    if Q.e2_sq > 0.004617553437128663:
                                                        if Q.z_dr_0p05_0p1 > 0.33635464310646057:
                                                            return 'Z'   # 96% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.max_dr > 0.14523440599441528:
                                                                return 'Z'   # 92% of the training jets here get this class from the formula
                                                            else:
                                                                return 'W'   # 56% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 74% of the training jets here get this class from the formula
                                                else:
                                                    if Q.LHA > 0.31600813567638397:
                                                        return 'Z'   # 83% of the training jets here get this class from the formula
                                                    else:
                                                        return 'W'   # 51% of the training jets here get this class from the formula
                                            else:
                                                if Q.lam2 > 6.838285844423808e-05:
                                                    return 'Z'   # 66% of the training jets here get this class from the formula
                                                else:
                                                    return 'W'   # 82% of the training jets here get this class from the formula
                                    else:
                                        if Q.e2 > 0.034392986446619034:
                                            if Q.D2 > 1.129055678844452:
                                                return 'Z'   # 77% of the training jets here get this class from the formula
                                            else:
                                                return 'W'   # 71% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > -0.25246091932058334:
                                                return 'q'   # 39% of the training jets here get this class from the formula
                                            else:
                                                if Q.D2 > 4.313555955886841:
                                                    if Q.girth2 > 0.0020952806808054447:
                                                        return 'Z'   # 94% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.max_dr > 0.09101896360516548:
                                                            return 'W'   # 59% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 76% of the training jets here get this class from the formula
                                                else:
                                                    return 'Z'   # 96% of the training jets here get this class from the formula
                                else:
                                    if s['Z'] - s['t'] > 0.22937515377998352:
                                        if Q.centroid_offset > 0.053093595430254936:
                                            if s['g'] - s['W'] > 1.171772837638855:
                                                return 'g'   # 86% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 68% of the training jets here get this class from the formula
                                        else:
                                            if s['q'] - s['Z'] > -0.7295087277889252:
                                                if Q.pt_7 > 22.6953125:
                                                    return 'Z'   # 79% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.025647971779108047:
                                                        if Q.D2 > 2.9098923206329346:
                                                            return 'q'   # 83% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 62% of the training jets here get this class from the formula
                                                    else:
                                                        return 'Z'   # 77% of the training jets here get this class from the formula
                                            else:
                                                if Q.lam1 > 0.0027587009826675057:
                                                    if s['W'] - s['Z'] > -0.6172426044940948:
                                                        if Q.max_dr > 0.13233152776956558:
                                                            if Q.e2 > 0.03407170996069908:
                                                                if Q.LHA > 0.2793106436729431:
                                                                    return 'Z'   # 96% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.D2 > 1.0274816155433655:
                                                                        return 'Z'   # 82% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'W'   # 60% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 99% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.LHA > 0.28010785579681396:
                                                                return 'Z'   # 92% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.e2 > 0.022534526884555817:
                                                                    return 'W'   # 60% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'Z'   # 68% of the training jets here get this class from the formula
                                                    else:
                                                        if s['Z'] - s['t'] > 0.34634803235530853:
                                                            return 'Z'   # 100% of the training jets here get this class from the formula
                                                        else:
                                                            if Q.max_dr > 0.2741706371307373:
                                                                return 't'   # 59% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 94% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['W'] > 0.23255415260791779:
                                                        if Q.sum_pt > 765.5625:
                                                            if Q.z_dr_0p05_0p1 > 0.5365045368671417:
                                                                return 'Z'   # 68% of the training jets here get this class from the formula
                                                            else:
                                                                return 'g'   # 82% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.D2 > 0.5987531244754791:
                                                            if s['g'] - s['q'] > 1.91787451505661:
                                                                if s['q'] - s['t'] > -0.20418541133403778:
                                                                    return 'Z'   # 90% of the training jets here get this class from the formula
                                                                else:
                                                                    return 'g'   # 62% of the training jets here get this class from the formula
                                                            else:
                                                                if s['g'] - s['t'] > -0.085416030138731:
                                                                    return 'Z'   # 97% of the training jets here get this class from the formula
                                                                else:
                                                                    if s['q'] - s['W'] > -0.49513572454452515:
                                                                        return 'q'   # 58% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 'Z'   # 96% of the training jets here get this class from the formula
                                                        else:
                                                            return 'W'   # 91% of the training jets here get this class from the formula
                                    else:
                                        if Q.girth > 0.05483083985745907:
                                            if Q.sum_pt > 526.6328125:
                                                if s['Z'] - s['t'] > 0.1034148558974266:
                                                    return 'Z'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.e2 > 0.024854418821632862:
                                                        if Q.tau32 > 0.6437283754348755:
                                                            if Q.max_dr > 0.11738737672567368:
                                                                if Q.e2_sq > 0.006795764900743961:
                                                                    return 'Z'   # 70% of the training jets here get this class from the formula
                                                                else:
                                                                    return 't'   # 75% of the training jets here get this class from the formula
                                                            else:
                                                                return 'Z'   # 86% of the training jets here get this class from the formula
                                                        else:
                                                            return 'Z'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 56% of the training jets here get this class from the formula
                                            else:
                                                if s['g'] - s['t'] > -0.47915682196617126:
                                                    return 'Z'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    if Q.mass > 40.50704002380371:
                                                        return 'Z'   # 67% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 73% of the training jets here get this class from the formula
                                        else:
                                            if Q.e2 > 0.023297986015677452:
                                                return 'Z'   # 60% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 69% of the training jets here get this class from the formula
                    else:
                        if s['Z'] - s['t'] > -0.21532460302114487:
                            if s['Z'] - s['t'] > -0.03891191631555557:
                                if s['W'] - s['Z'] > -1.4565135836601257:
                                    return 'Z'   # 58% of the training jets here get this class from the formula
                                else:
                                    if Q.mass_over_sum_pt > 0.09493579715490341:
                                        return 'Z'   # 94% of the training jets here get this class from the formula
                                    else:
                                        if Q.tau32 > 0.3422307223081589:
                                            return 't'   # 67% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 69% of the training jets here get this class from the formula
                            else:
                                if Q.max_dr > 0.10014265775680542:
                                    if Q.e2_sq > 0.008854246232658625:
                                        if Q.tau21 > 0.169514998793602:
                                            return 'Z'   # 88% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 65% of the training jets here get this class from the formula
                                    else:
                                        if Q.log_sum_pt > 6.652732610702515:
                                            return 'Z'   # 68% of the training jets here get this class from the formula
                                        else:
                                            if Q.tau32 > 0.29355235397815704:
                                                if s['q'] - s['t'] > -0.31993870437145233:
                                                    return 't'   # 41% of the training jets here get this class from the formula
                                                else:
                                                    if Q.centroid_offset > 0.03692712262272835:
                                                        if Q.girth > 0.07328140363097191:
                                                            return 'Z'   # 58% of the training jets here get this class from the formula
                                                        else:
                                                            return 't'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 't'   # 83% of the training jets here get this class from the formula
                                            else:
                                                return 'Z'   # 50% of the training jets here get this class from the formula
                                else:
                                    if Q.lam1 > 0.006438653450459242:
                                        return 't'   # 88% of the training jets here get this class from the formula
                                    else:
                                        if Q.e2 > 0.020649366080760956:
                                            return 'Z'   # 76% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 30% of the training jets here get this class from the formula
                        else:
                            if Q.log_sum_pt > 7.015718460083008:
                                return 'Z'   # 62% of the training jets here get this class from the formula
                            else:
                                return 't'   # 94% of the training jets here get this class from the formula
    else:
        if s['g'] - s['t'] > -0.06091710366308689:
            if s['g'] - s['t'] > 0.16277549415826797:
                if s['g'] - s['q'] > 0.02637570071965456:
                    if s['g'] - s['Z'] > -0.0870656780898571:
                        if s['Z'] - s['t'] > -7.50035548210144:
                            return 'g'   # 95% of the training jets here get this class from the formula
                        else:
                            if s['g'] - s['t'] > 0.7547788918018341:
                                return 'g'   # 92% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['W'] > 7.346055746078491:
                                    if s['g'] - s['q'] > 1.6631883382797241:
                                        return 'g'   # 80% of the training jets here get this class from the formula
                                    else:
                                        if Q.z_dr_0p05_0p1 > 0.6313211619853973:
                                            return 'g'   # 65% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 67% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.07142635807394981:
                                        if Q.z_7 > 0.08060980960726738:
                                            return 'g'   # 56% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 85% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 91% of the training jets here get this class from the formula
                    else:
                        if Q.sum_pt > 979.65625:
                            return 'g'   # 50% of the training jets here get this class from the formula
                        else:
                            return 'Z'   # 88% of the training jets here get this class from the formula
                else:
                    if s['g'] - s['q'] > -0.25794871151447296:
                        if Q.mass > 116.97656631469727:
                            return 'g'   # 66% of the training jets here get this class from the formula
                        else:
                            return 'q'   # 54% of the training jets here get this class from the formula
                    else:
                        return 'q'   # 83% of the training jets here get this class from the formula
            else:
                if s['g'] - s['q'] > 0.029904807917773724:
                    if s['g'] - s['Z'] > -0.33704210817813873:
                        if s['g'] - s['t'] > 0.07095565646886826:
                            if s['q'] - s['Z'] > 7.818294048309326:
                                if Q.z_7 > 0.06579259037971497:
                                    return 'g'   # 64% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 82% of the training jets here get this class from the formula
                            else:
                                if Q.centroid_offset > 0.020249015651643276:
                                    if Q.lam2 > 0.0004328741488279775:
                                        if s['g'] - s['W'] > 8.18980598449707:
                                            return 't'   # 62% of the training jets here get this class from the formula
                                        else:
                                            if s['W'] - s['Z'] > -3.692482352256775:
                                                return 'g'   # 77% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 57% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 84% of the training jets here get this class from the formula
                                else:
                                    if Q.pt_0 > 197.6875:
                                        return 't'   # 69% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 65% of the training jets here get this class from the formula
                        else:
                            if Q.centroid_offset > 0.02724515739828348:
                                if Q.mass > 72.19687271118164:
                                    return 'g'   # 80% of the training jets here get this class from the formula
                                else:
                                    if Q.C2 > 0.07052838429808617:
                                        if Q.LHA > 0.423587366938591:
                                            return 't'   # 62% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 82% of the training jets here get this class from the formula
                                    else:
                                        if s['g'] - s['t'] > 0.011417543049901724:
                                            if Q.sum_pt > 380.4765625:
                                                if Q.LHA > 0.327801913022995:
                                                    if Q.D2 > 1.3519429564476013:
                                                        return 't'   # 85% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 52% of the training jets here get this class from the formula
                                                else:
                                                    if Q.sum_pt_top5 > 384.328125:
                                                        if Q.max_dr > 0.09288674220442772:
                                                            return 't'   # 57% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 84% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 86% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 82% of the training jets here get this class from the formula
                                        else:
                                            if Q.z_dr_0p1_0p2 > 0.2089633047580719:
                                                if Q.tau21 > 0.13181693851947784:
                                                    if s['q'] - s['t'] > -1.1451266407966614:
                                                        return 'g'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        if Q.lam1 > 0.008176551200449467:
                                                            if Q.lam1 > 0.015065548475831747:
                                                                return 'g'   # 72% of the training jets here get this class from the formula
                                                            else:
                                                                if Q.girth2 > 0.011805255431681871:
                                                                    return 't'   # 88% of the training jets here get this class from the formula
                                                                else:
                                                                    if Q.z_dr_0p1_0p2 > 0.4934607148170471:
                                                                        return 'g'   # 72% of the training jets here get this class from the formula
                                                                    else:
                                                                        return 't'   # 69% of the training jets here get this class from the formula
                                                        else:
                                                            return 'g'   # 84% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 70% of the training jets here get this class from the formula
                                            else:
                                                if s['W'] - s['Z'] > -1.7758476734161377:
                                                    return 'g'   # 67% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 73% of the training jets here get this class from the formula
                            else:
                                if Q.max_dr > 0.16739771515130997:
                                    if s['W'] - s['Z'] > 0.470873698592186:
                                        return 'g'   # 76% of the training jets here get this class from the formula
                                    else:
                                        if Q.tau21 > 0.40261565148830414:
                                            return 'g'   # 72% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 63% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 78% of the training jets here get this class from the formula
                    else:
                        return 'Z'   # 88% of the training jets here get this class from the formula
                else:
                    if Q.z_dr_0p1_0p2 > 0.7597302496433258:
                        return 't'   # 47% of the training jets here get this class from the formula
                    else:
                        return 'q'   # 82% of the training jets here get this class from the formula
        else:
            if s['Z'] - s['t'] > 0.059636274352669716:
                if s['Z'] - s['t'] > 0.3628961145877838:
                    if s['q'] - s['Z'] > -0.7186550796031952:
                        return 'q'   # 51% of the training jets here get this class from the formula
                    else:
                        if Q.mass > 93.33248138427734:
                            return 't'   # 48% of the training jets here get this class from the formula
                        else:
                            if s['Z'] - s['t'] > 0.5671212673187256:
                                return 'Z'   # 99% of the training jets here get this class from the formula
                            else:
                                if Q.e2 > 0.02916307281702757:
                                    return 'Z'   # 98% of the training jets here get this class from the formula
                                else:
                                    if Q.mass_over_sum_pt > 0.07556186243891716:
                                        if Q.tau32 > 0.551476925611496:
                                            return 't'   # 73% of the training jets here get this class from the formula
                                        else:
                                            return 'Z'   # 68% of the training jets here get this class from the formula
                                    else:
                                        return 'Z'   # 92% of the training jets here get this class from the formula
                else:
                    if Q.e2 > 0.038916485384106636:
                        if s['Z'] - s['t'] > 0.1516643762588501:
                            return 'Z'   # 92% of the training jets here get this class from the formula
                        else:
                            if Q.mass_over_sum_pt > 0.09320113435387611:
                                return 'Z'   # 90% of the training jets here get this class from the formula
                            else:
                                if Q.mass_over_sum_pt > 0.08860282599925995:
                                    return 't'   # 67% of the training jets here get this class from the formula
                                else:
                                    return 'Z'   # 86% of the training jets here get this class from the formula
                    else:
                        if Q.e2_sq > 0.005765512818470597:
                            if Q.tau32 > 0.3607374131679535:
                                if Q.z_dr_0p2_0p4 > 0.11247017234563828:
                                    return 'Z'   # 64% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 80% of the training jets here get this class from the formula
                            else:
                                return 'Z'   # 77% of the training jets here get this class from the formula
                        else:
                            return 'Z'   # 57% of the training jets here get this class from the formula
            else:
                if s['q'] - s['t'] > -0.21943733841180801:
                    if s['q'] - s['t'] > -0.031279406510293484:
                        if Q.centroid_offset > 0.015758533962070942:
                            if Q.centroid_offset > 0.0779746025800705:
                                return 't'   # 60% of the training jets here get this class from the formula
                            else:
                                if s['q'] - s['t'] > 0.22960522770881653:
                                    return 'q'   # 96% of the training jets here get this class from the formula
                                else:
                                    if s['g'] - s['Z'] > 8.273499488830566:
                                        return 't'   # 62% of the training jets here get this class from the formula
                                    else:
                                        return 'q'   # 82% of the training jets here get this class from the formula
                        else:
                            if Q.sum_pt_top5 > 692.875:
                                return 't'   # 66% of the training jets here get this class from the formula
                            else:
                                return 'q'   # 88% of the training jets here get this class from the formula
                    else:
                        if s['g'] - s['Z'] > 0.14660563319921494:
                            if Q.lam1 > 0.02371290884912014:
                                if s['g'] - s['q'] > -0.18221943080425262:
                                    return 't'   # 42% of the training jets here get this class from the formula
                                else:
                                    return 'q'   # 76% of the training jets here get this class from the formula
                            else:
                                if Q.lam1 > 0.007877558469772339:
                                    return 't'   # 79% of the training jets here get this class from the formula
                                else:
                                    return 'q'   # 50% of the training jets here get this class from the formula
                        else:
                            return 'q'   # 79% of the training jets here get this class from the formula
                else:
                    if s['g'] - s['t'] > -0.312762975692749:
                        if Q.pt_7 > 26.5234375:
                            if Q.lam1 > 0.030120261013507843:
                                if Q.mass > 90.97009658813477:
                                    return 'g'   # 65% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.07143991068005562:
                                        if Q.tau32 > 0.49641256034374237:
                                            return 't'   # 80% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 95% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 78% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['t'] > -0.1592186763882637:
                                    if Q.max_dr > 0.21377886831760406:
                                        if Q.girth > 0.06903312355279922:
                                            if Q.planar_flow > 0.10068545490503311:
                                                if Q.C2 > 0.08400218188762665:
                                                    return 'g'   # 61% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 82% of the training jets here get this class from the formula
                                            else:
                                                if Q.planar_flow > 0.033704377710819244:
                                                    return 'g'   # 61% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 65% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 83% of the training jets here get this class from the formula
                                    else:
                                        if Q.sum_pt_top5 > 257.328125:
                                            if s['W'] - s['t'] > -8.310046195983887:
                                                return 't'   # 86% of the training jets here get this class from the formula
                                            else:
                                                if Q.z_dr_0p1_0p2 > 0.3087252825498581:
                                                    return 'g'   # 60% of the training jets here get this class from the formula
                                                else:
                                                    return 't'   # 84% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 54% of the training jets here get this class from the formula
                                else:
                                    if Q.centroid_offset > 0.056880950927734375:
                                        if Q.z_dr_0p1_0p2 > 0.28048698604106903:
                                            if Q.e2 > 0.050084253773093224:
                                                return 't'   # 79% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 57% of the training jets here get this class from the formula
                                        else:
                                            return 't'   # 93% of the training jets here get this class from the formula
                                    else:
                                        if Q.z_7 > 0.0551341250538826:
                                            if Q.C2 > 0.08017579466104507:
                                                if Q.eccentricity > 0.8500913977622986:
                                                    return 't'   # 87% of the training jets here get this class from the formula
                                                else:
                                                    return 'g'   # 52% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 94% of the training jets here get this class from the formula
                                        else:
                                            if s['W'] - s['Z'] > -4.048353910446167:
                                                return 't'   # 84% of the training jets here get this class from the formula
                                            else:
                                                return 'g'   # 51% of the training jets here get this class from the formula
                        else:
                            if Q.z_dr_0p1_0p2 > 0.7041775584220886:
                                return 't'   # 70% of the training jets here get this class from the formula
                            else:
                                if Q.sum_pt_top5 > 391.171875:
                                    return 't'   # 64% of the training jets here get this class from the formula
                                else:
                                    if Q.LHA > 0.3382560759782791:
                                        if Q.pt_0 > 65.625:
                                            return 't'   # 51% of the training jets here get this class from the formula
                                        else:
                                            return 'g'   # 89% of the training jets here get this class from the formula
                                    else:
                                        return 'g'   # 80% of the training jets here get this class from the formula
                    else:
                        if s['Z'] - s['t'] > -0.1997908428311348:
                            if Q.tau32 > 0.38075074553489685:
                                if s['Z'] - s['t'] > -0.014163178391754627:
                                    if Q.centroid_offset > 0.014316588640213013:
                                        return 't'   # 76% of the training jets here get this class from the formula
                                    else:
                                        return 'Z'   # 62% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 90% of the training jets here get this class from the formula
                            else:
                                if Q.e2 > 0.04000072367489338:
                                    return 'Z'   # 85% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 63% of the training jets here get this class from the formula
                        else:
                            if s['q'] - s['t'] > -0.5036320090293884:
                                if Q.width > 0.0247202105820179:
                                    if Q.max_dr > 0.25101786851882935:
                                        return 'q'   # 60% of the training jets here get this class from the formula
                                    else:
                                        if Q.pt_7 > 28.8984375:
                                            return 't'   # 100% of the training jets here get this class from the formula
                                        else:
                                            if s['W'] - s['t'] > -7.332305669784546:
                                                return 'q'   # 70% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 85% of the training jets here get this class from the formula
                                else:
                                    if Q.D2 > 4.07715368270874:
                                        return 'q'   # 61% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 91% of the training jets here get this class from the formula
                            else:
                                if s['g'] - s['t'] > -0.5108265578746796:
                                    if Q.log_sum_pt > 5.779560089111328:
                                        if Q.girth2 > 0.03754151239991188:
                                            if Q.centroid_offset > 0.04958784766495228:
                                                return 'g'   # 53% of the training jets here get this class from the formula
                                            else:
                                                return 't'   # 80% of the training jets here get this class from the formula
                                        else:
                                            if Q.pt_7 > 25.3984375:
                                                return 't'   # 96% of the training jets here get this class from the formula
                                            else:
                                                if Q.log_sum_pt > 6.102523565292358:
                                                    return 't'   # 91% of the training jets here get this class from the formula
                                                else:
                                                    if s['g'] - s['W'] > 6.614777088165283:
                                                        return 't'   # 78% of the training jets here get this class from the formula
                                                    else:
                                                        return 'g'   # 68% of the training jets here get this class from the formula
                                    else:
                                        return 't'   # 54% of the training jets here get this class from the formula
                                else:
                                    return 't'   # 100% of the training jets here get this class from the formula


def classify(pt, eta, phi):
    Q = quantities(pt, eta, phi)
    return decide(Q, scores(Q))


if __name__ == '__main__':
    pt = [412.0, 230.5, 101.2, 40.3, 22.8, 10.1, 6.4, 3.3]
    eta = [0.01, -0.12, 0.25, 0.05, -0.31, 0.2, -0.05, 0.4]
    phi = [-0.02, 0.18, -0.1, 0.33, 0.07, -0.25, 0.12, -0.36]
    print('class:', classify(pt, eta, phi))
