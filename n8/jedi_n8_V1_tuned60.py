"""JEDI-linear jet tagger, 8 particles, 3 features, written as a formula (V1, 60 terms per neuron, all coefficients tuned together on the classification).

Input:  the 8 hardest particles of a jet, hardest first, each (pT [GeV], Δη, Δφ) relative to the jet axis;
        empty slots have pT = 0.
Output: the class (g, q, W, Z or t), the 5 logits and the 5 probabilities.

1. quantities():  physics quantities of the particles.
2. jet_layer_4(): the 16 neurons of the network's last hidden layer, each max(0, z) with z built from if-statements.
3. logits():      the network's own last layer: each neuron is rounded to the network's fixed-point grid
                  (round to a multiple of 2^-f, then wrap modulo 2^i), multiplied by the weights, plus the biases.
4. classify():    softmax of the logits; the class is the largest logit.

Test set (50,000 jets of the hls4ml LHC jet dataset, test file): accuracy 65.8% (the network: 65.8%); same class as the network for 88.1% of jets.

Quantities:
  Q.mass_over_sum_pt_sq    (jet mass / total pT) squared
  Q.z_top5                 pT share of the 5 largest
  Q.eccentricity           1 − λ2/λ1 of the pT-weighted (Δη, Δφ) tensor
  Q.C2                     energy correlation ratio e3/e2²
  Q.D2                     energy correlation ratio e3/e2³
  Q.LHA                    Les Houches angularity
  Q.log_sum_pt             natural log of the total pT
  Q.mass_over_sum_pt       jet mass / total pT
  Q.mass                   invariant mass of all particles (massless four-vectors) [GeV]
  Q.mass_top2              mass of the 2 hardest particles [GeV]
  Q.mass_top3              mass of the 3 hardest particles [GeV]
  Q.mass_top5              mass of the 5 hardest particles [GeV]
  Q.max_pair_mass          largest pair mass among particles 0, 1, 2 [GeV]
  Q.max_dr                 largest distance ΔR of a particle from the jet axis
  Q.min_pair_mass          smallest pair mass among particles 0, 1, 2 [GeV]
  Q.pt_balance01           min(pT0, pT1) / (pT0 + pT1)
  Q.m01                    mass of particles 0 and 1 [GeV]
  Q.m012                   mass of particles 0, 1 and 2 [GeV]
  Q.pt_0                   pT of particle 0 [GeV]
  Q.pt_1                   pT of particle 1 [GeV]
  Q.pt_2                   pT of particle 2 [GeV]
  Q.pt_3                   pT of particle 3 [GeV]
  Q.pt_4                   pT of particle 4 [GeV]
  Q.pt_5                   pT of particle 5 [GeV]
  Q.pt_6                   pT of particle 6 [GeV]
  Q.pt_7                   pT of particle 7 [GeV]
  Q.z_2                    pT of particle 2 / total pT
  Q.z_3                    pT of particle 3 / total pT
  Q.z_4                    pT of particle 4 / total pT
  Q.z_5                    pT of particle 5 / total pT
  Q.z_6                    pT of particle 6 / total pT
  Q.z_7                    pT of particle 7 / total pT
  Q.z_top2_slots           pT share of the 2 hardest particles
  Q.z_top5_slots           pT share of the 5 hardest particles
  Q.z_1st                  largest pT share
  Q.pt1_over_pt0           pT1 / pT0
  Q.z_2nd                  2nd-largest pT share
  Q.pt1_dr01               pT1 · ΔR01
  Q.z_3rd                  3rd-largest pT share
  Q.planar_flow            planar flow of the pT-weighted (Δη, Δφ) tensor
  Q.dr_0                   ΔR of particle 0 from the jet axis
  Q.dr_2                   ΔR of particle 2 from the jet axis
  Q.dr_3                   ΔR of particle 3 from the jet axis
  Q.dr_4                   ΔR of particle 4 from the jet axis
  Q.dr_5                   ΔR of particle 5 from the jet axis
  Q.dr_6                   ΔR of particle 6 from the jet axis
  Q.dr_7                   ΔR of particle 7 from the jet axis
  Q.dr01                   ΔR between particles 0 and 1
  Q.eta_0                  Δη of particle 0
  Q.eta_1                  Δη of particle 1
  Q.eta_2                  Δη of particle 2
  Q.eta_3                  Δη of particle 3
  Q.eta_4                  Δη of particle 4
  Q.eta_5                  Δη of particle 5
  Q.eta_6                  Δη of particle 6
  Q.eta_7                  Δη of particle 7
  Q.phi_0                  Δφ of particle 0
  Q.phi_1                  Δφ of particle 1
  Q.phi_2                  Δφ of particle 2
  Q.phi_5                  Δφ of particle 5
  Q.phi_6                  Δφ of particle 6
  Q.phi_7                  Δφ of particle 7
  Q.sum_pt_top2            total pT of the 2 hardest particles [GeV]
  Q.sum_pt_top3            total pT of the 3 hardest particles [GeV]
  Q.sum_pt_top5            total pT of the 5 hardest particles [GeV]
  Q.girth2_top2            pT-weighted mean ΔR² of the 2 hardest particles
  Q.girth2_top3            pT-weighted mean ΔR² of the 3 hardest particles
  Q.girth2_top5            pT-weighted mean ΔR² of the 5 hardest particles
  Q.n_dr_0_0p05            number of particles with 0 ≤ ΔR < 0.05
  Q.n_dr_0p05_0p1          number of particles with 0.05 ≤ ΔR < 0.1
  Q.n_dr_0p1_0p2           number of particles with 0.1 ≤ ΔR < 0.2
  Q.n_dr_0p2_0p4           number of particles with 0.2 ≤ ΔR < 0.4
  Q.n_pt_above_50          number of particles with pT > 50 GeV
  Q.sum_pt                 total pT of the particles [GeV]
  Q.z_dr_0_0p05            pT share of the particles with 0 ≤ ΔR < 0.05
  Q.z_dr_0p05_0p1          pT share of the particles with 0.05 ≤ ΔR < 0.1
  Q.z_dr_0p1_0p2           pT share of the particles with 0.1 ≤ ΔR < 0.2
  Q.z_dr_0p2_0p4           pT share of the particles with 0.2 ≤ ΔR < 0.4
  Q.girth                  pT-weighted mean ΔR
  Q.girth2                 pT-weighted mean ΔR²
  Q.mean_eta               pT-weighted mean Δη
  Q.mean_eta2              pT-weighted mean Δη²
  Q.mean_phi               pT-weighted mean Δφ
  Q.mean_phi2              pT-weighted mean Δφ²
  Q.e2                     energy correlation e2 = Σ_{i<j} zᵢzⱼΔRᵢⱼ
  Q.e2_sq                  Σ_{i<j} zᵢzⱼΔRᵢⱼ²
  Q.lam1                   larger eigenvalue of the pT-weighted (Δη, Δφ) tensor
  Q.width                  λ1 + λ2 of the pT-weighted (Δη, Δφ) tensor
  Q.lam2                   smaller eigenvalue of the pT-weighted (Δη, Δφ) tensor
  Q.tau21                  N-subjettiness τ2/τ1 (axes from pT-weighted k-means)
  Q.tau32                  N-subjettiness τ3/τ2
  Q.centroid_offset        distance of the pT centroid from the jet axis
  Q.pt_dispersion          √(Σ pTᵢ²) / Σ pTᵢ
"""
import math
from types import SimpleNamespace

CLASSES = ['g', 'q', 'W', 'Z', 't']
W = [[-0.15625, 0.0, 0.34375, 0.0, 0.015625], [0.390625, 0.0, -0.03125, 0.125, 0.0], [0.4296875, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, -0.5, -0.5625, 0.0625], [-0.03125, -0.09375, 0.0, 0.078125, 0.125], [-0.1875, 0.046875, 0.0, 0.015625, -0.25], [0.109375, 0.125, -0.3125, -0.375, 0.0], [0.0, 0.0, 0.21875, 0.46875, 0.0], [0.0, 0.0625, -0.25, 0.0, 0.1875], [0.171875, 0.25390625, -0.03125, -0.03125, 0.0], [0.0, -0.125, 0.0, 0.0, 0.375], [0.0, 0.0, 0.375, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, -0.5], [0.0, 0.0, 0.0703125, 0.0546875, -0.40625], [0.0, 0.0, -0.75, 0.375, 0.0], [0.0, 0.0625, -0.6875, -0.15625, 0.0]]
B = [-0.4375, 0.03125, -0.125, -0.09375, 1.34375]
INT_BITS = [3, 5, 4, 4, 5, 5, 4, 4, 3, 4, 5, 4, 5, 4, 3, 3]
FRAC_BITS = [3, 3, 4, 3, 2, 3, 3, 3, 3, 2, 4, 4, 3, 3, 4, 3]


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
        pt_balance01=min(pt[0], pt[1]) / max(pt[0] + pt[1], 1e-9),
        m01=pair_mass(0, 1),
        m012=math.sqrt(pair_mass(0, 1) ** 2 + pair_mass(0, 2) ** 2 + pair_mass(1, 2) ** 2),
        pt_0=pt[0],
        pt_1=pt[1],
        pt_2=pt[2],
        pt_3=pt[3],
        pt_4=pt[4],
        pt_5=pt[5],
        pt_6=pt[6],
        pt_7=pt[7],
        z_2=z[2],
        z_3=z[3],
        z_4=z[4],
        z_5=z[5],
        z_6=z[6],
        z_7=z[7],
        z_top2_slots=sum(pt[:2]) / tot,
        z_top5_slots=sum(pt[:5]) / tot,
        z_1st=zs[0],
        pt1_over_pt0=pt[1] / max(pt[0], 1e-9),
        z_2nd=zs[1],
        pt1_dr01=pt[1] * math.sqrt(dist2(0, 1)),
        z_3rd=zs[2],
        planar_flow=4 * (ta * tc - tb ** 2) / max((ta + tc) ** 2, 1e-12),
        dr_0=dr[0] if pt[0] > 0 else 0.0,
        dr_2=dr[2] if pt[2] > 0 else 0.0,
        dr_3=dr[3] if pt[3] > 0 else 0.0,
        dr_4=dr[4] if pt[4] > 0 else 0.0,
        dr_5=dr[5] if pt[5] > 0 else 0.0,
        dr_6=dr[6] if pt[6] > 0 else 0.0,
        dr_7=dr[7] if pt[7] > 0 else 0.0,
        dr01=math.sqrt(dist2(0, 1)),
        eta_0=eta[0],
        eta_1=eta[1],
        eta_2=eta[2],
        eta_3=eta[3],
        eta_4=eta[4],
        eta_5=eta[5],
        eta_6=eta[6],
        eta_7=eta[7],
        phi_0=phi[0],
        phi_1=phi[1],
        phi_2=phi[2],
        phi_5=phi[5],
        phi_6=phi[6],
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


def neuron_0(Q):
    z = -0.668329656124115
    if Q.planar_flow < 0.012569162668:
        z += -100.42595982551575 * Q.planar_flow + 1.7537515035819622
    if 0.012569162668 <= Q.planar_flow < 0.148419710734:
        z += -3.6178085803985596 * Q.planar_flow + 0.5369541029937375
    if Q.width < 0.004372139331:
        z += -214.67156982421875 * Q.width + 4.192483868482949
    if 0.004372139331 <= Q.width < 0.008678044951:
        z += -755.6853637695312 * Q.width + 6.5578715556047795
    if Q.girth2 < 0.013238675334:
        z += -469.75325775146484 * Q.girth2 + 6.556384905405782
    if 0.013238675334 <= Q.girth2 < 0.018827652745:
        z += -60.38207244873047 * Q.girth2 + 1.136852692088129
    if Q.mass < 21.784077072144:
        z += 0.3208375871181488 * Q.mass - 9.13278003842438
    if 21.784077072144 <= Q.mass < 29.644699859619:
        z += 0.11075383424758911 * Q.mass - 4.556299374286854
    if 29.644699859619 <= Q.mass < 56.920347213745:
        z += 0.04057645797729492 * Q.mass - 2.4759121178184342
    if 56.920347213745 <= Q.mass < 64.618731689453:
        z += 0.02160012163221836 * Q.mass - 1.3957724642118678
    if Q.girth2_top3 < 0.003952581551:
        z += -158.9435272216797 * Q.girth2_top3 + 0.12140660088181665
    if 0.003952581551 <= Q.girth2_top3 < 0.007929074034:
        z += 127.45671081542969 * Q.girth2_top3 - 1.0106136961856704
    if Q.lam1 < 0.000504949057:
        z += 321.4055404663086 * Q.lam1 - 1.6690384769546898
    if 0.000504949057 <= Q.lam1 < 0.00543336053:
        z += 205.0260467529297 * Q.lam1 - 1.6102727613499817
    if 0.00543336053 <= Q.lam1 < 0.006506575659:
        z += 20.130569458007812 * Q.lam1 - 0.6056689728402418
    if 0.006506575659 <= Q.lam1 < 0.008375572068:
        z += 253.9801025390625 * Q.lam1 - 2.1272286526539474
    if Q.sum_pt >= 901.59375:
        z += -0.02735385112464428 * Q.sum_pt + 24.662061212409753
    if Q.girth2_top5 < 0.00832969537:
        z += 119.30717468261719 * Q.girth2_top5 - 0.9937924205615775
    if Q.z_dr_0_0p05 >= 0.847731333971:
        z += 15.553894996643066 * Q.z_dr_0_0p05 - 13.185524153949089
    if Q.girth < 0.076081777364:
        z += 70.80416107177734 * Q.girth - 5.682472664370334
    if 0.076081777364 <= Q.girth < 0.087236513197:
        z += 26.496929168701172 * Q.girth - 2.311499711105374
    if Q.centroid_offset < 0.031170772021:
        z += -43.17546081542969 * Q.centroid_offset + 1.3458124459793774
    if Q.e2 < 0.020459658932:
        z += 39.96731185913086 * Q.e2 - 0.8177175690666962
    if Q.mass_over_sum_pt_sq < 0.008174660116:
        z += 336.0888977050781 * Q.mass_over_sum_pt_sq - 2.747412507500106
    if 6.377722943814 <= Q.log_sum_pt < 6.638338705138:
        z += 0.7071569561958313 * Q.log_sum_pt - 4.510051144407825
    if Q.log_sum_pt >= 6.638338705138:
        z += -4.167714297771454 * Q.log_sum_pt + 27.850995383367817
    if Q.sum_pt_top5 >= 687.4375:
        z += 0.008367556147277355 * Q.sum_pt_top5 - 5.752171878993977
    if Q.mass_over_sum_pt < 0.13092863437:
        z += 23.31473159790039 * Q.mass_over_sum_pt - 3.052565968816186
    if Q.z_dr_0p05_0p1 >= 0.846033477783:
        z += -0.21791306138038635 * Q.z_dr_0p05_0p1 + 0.1843617451739886
    if Q.planar_flow < 0.148419710734 and Q.centroid_offset < 0.049903668404:
        z += 119.89995574951172 * (0.148419710734 - Q.planar_flow) * (0.049903668404 - Q.centroid_offset)
    if Q.width < 0.004372139331 and Q.D2 < 0.74595130682:
        z += -2966.149658203125 * (0.004372139331 - Q.width) * (0.74595130682 - Q.D2)
    if Q.lam1 < 0.006506575659 and Q.D2 < 0.87567204833:
        z += -1872.092529296875 * (0.006506575659 - Q.lam1) * (0.87567204833 - Q.D2)
    if Q.girth2 < 0.013238675334 and Q.D2 < 1.002470755577:
        z += -14.82368278503418 * (0.013238675334 - Q.girth2) * (1.002470755577 - Q.D2)
    if Q.sum_pt > 901.59375 and Q.pt_7 < 25.578125:
        z += 0.0016177577199414372 * (Q.sum_pt - 901.59375) * (25.578125 - Q.pt_7)
    if Q.girth2 < 0.013238675334 and Q.mean_phi < -0.001813532785:
        z += 322.5538330078125 * (0.013238675334 - Q.girth2) * (-0.001813532785 - Q.mean_phi)
    if Q.planar_flow < 0.148419710734 and Q.sum_pt_top2 < 380.5875:
        z += -0.044908422976732254 * (0.148419710734 - Q.planar_flow) * (380.5875 - Q.sum_pt_top2)
    if Q.planar_flow < 0.148419710734 and Q.dr_2 < 0.027807975573:
        z += -406.9549255371094 * (0.148419710734 - Q.planar_flow) * (0.027807975573 - Q.dr_2)
    if Q.sum_pt > 901.59375 and Q.dr_2 < 0.038438041256:
        z += 0.09785108268260956 * (Q.sum_pt - 901.59375) * (0.038438041256 - Q.dr_2)
    if Q.girth2 < 0.018827652745 and Q.mass_top2 > 28.78966323496:
        z += 3.530254602432251 * (0.018827652745 - Q.girth2) * (Q.mass_top2 - 28.78966323496)
    if Q.mass < 56.920347213745 and Q.C2 > 0.023843882605:
        z += 0.8602447509765625 * (56.920347213745 - Q.mass) * (Q.C2 - 0.023843882605)
    if Q.mass < 29.644699859619 and Q.D2 < 0.87567204833:
        z += -2.0144217014312744 * (29.644699859619 - Q.mass) * (0.87567204833 - Q.D2)
    if Q.planar_flow < 0.148419710734 and Q.max_dr < 0.111761856824:
        z += -193.76817321777344 * (0.148419710734 - Q.planar_flow) * (0.111761856824 - Q.max_dr)
    if Q.girth2 < 0.013238675334 and Q.centroid_offset > 0.014379521101:
        z += -2130.78564453125 * (0.013238675334 - Q.girth2) * (Q.centroid_offset - 0.014379521101)
    if Q.mass < 64.618731689453 and Q.centroid_offset > 0.012587644117:
        z += 2.9854695796966553 * (64.618731689453 - Q.mass) * (Q.centroid_offset - 0.012587644117)
    if Q.girth2 < 0.018827652745 and Q.phi_0 > 0.021438598633:
        z += 276.26654052734375 * (0.018827652745 - Q.girth2) * (Q.phi_0 - 0.021438598633)
    if Q.girth2 < 0.018827652745 and Q.eccentricity > 0.959856212153:
        z += 2616.547119140625 * (0.018827652745 - Q.girth2) * (Q.eccentricity - 0.959856212153)
    if Q.sum_pt > 901.59375 and Q.pt_7 > 29.0421875:
        z += -0.0005090510239824653 * (Q.sum_pt - 901.59375) * (Q.pt_7 - 29.0421875)
    if Q.girth2_top3 < 0.007929074034 and Q.pt_6 < 35.28125:
        z += -2.884523630142212 * (0.007929074034 - Q.girth2_top3) * (35.28125 - Q.pt_6)
    if Q.log_sum_pt > 6.638338705138 and Q.dr_4 < 0.072321663733:
        z += 9.768698692321777 * (Q.log_sum_pt - 6.638338705138) * (0.072321663733 - Q.dr_4)
    if Q.sum_pt_top5 > 687.4375 and Q.phi_2 > 0.064147949219:
        z += 0.06283409148454666 * (Q.sum_pt_top5 - 687.4375) * (Q.phi_2 - 0.064147949219)
    if Q.girth2_top3 < 0.007929074034 and Q.phi_1 < -0.002475547791:
        z += -1062.6795654296875 * (0.007929074034 - Q.girth2_top3) * (-0.002475547791 - Q.phi_1)
    if Q.sum_pt_top5 > 687.4375 and Q.eta_6 > 0.076599121094:
        z += -0.026224788278341293 * (Q.sum_pt_top5 - 687.4375) * (Q.eta_6 - 0.076599121094)
    if Q.sum_pt_top5 > 687.4375 and Q.z_7 > 0.023207568189:
        z += -0.5725680589675903 * (Q.sum_pt_top5 - 687.4375) * (Q.z_7 - 0.023207568189)
    if Q.mass < 64.618731689453 and Q.pt_7 < 40.040625:
        z += -0.0019723318982869387 * (64.618731689453 - Q.mass) * (40.040625 - Q.pt_7)
    if Q.log_sum_pt > 6.638338705138 and Q.dr_7 < 0.093979107928:
        z += 21.979841232299805 * (Q.log_sum_pt - 6.638338705138) * (0.093979107928 - Q.dr_7)
    if Q.mass_over_sum_pt_sq < 0.008174660116 and Q.eta_7 > 0.020645141602:
        z += -171.5435333251953 * (0.008174660116 - Q.mass_over_sum_pt_sq) * (Q.eta_7 - 0.020645141602)
    if Q.mass < 29.644699859619 and Q.phi_1 > -0.058901977539:
        z += -2.4983315467834473 * (29.644699859619 - Q.mass) * (Q.phi_1 - -0.058901977539)
    if Q.planar_flow < 0.148419710734 and Q.pt_1 > 159.25:
        z += -0.020307209342718124 * (0.148419710734 - Q.planar_flow) * (Q.pt_1 - 159.25)
    if Q.width < 0.004372139331 and Q.n_dr_0p1_0p2 > 1.0:
        z += -393.5710754394531 * (0.004372139331 - Q.width) * (Q.n_dr_0p1_0p2 - 1.0)
    if Q.z_dr_0_0p05 > 0.847731333971 and Q.n_dr_0p2_0p4 > 2.0:
        z += 12.650705337524414 * (Q.z_dr_0_0p05 - 0.847731333971) * (Q.n_dr_0p2_0p4 - 2.0)
    return max(0.0, z)


def neuron_1(Q):
    z = 0.8257313370704651
    if Q.lam1 < 0.008375572068:
        z += 134.67144775390625 * Q.lam1 - 1.1279504161647385
    if 34.53125 <= Q.pt_7 < 53.4375:
        z += 0.11733510345220566 * Q.pt_7 - 4.051727791083977
    if Q.pt_7 >= 53.4375:
        z += 0.10850251279771328 * Q.pt_7 - 3.57973622798454
    if Q.e2 < 0.032346998155:
        z += -7.749777793884277 * Q.e2 + 0.27558916820931384
    if 0.032346998155 <= Q.e2 < 0.035560912266:
        z += -39.946722984313965 * Q.e2 + 1.3170636948807792
    if Q.e2 >= 0.035560912266:
        z += -32.19694519042969 * Q.e2 + 1.0414745266714653
    if 6.377722943814 <= Q.log_sum_pt < 6.572937922293:
        z += 2.9595494270324707 * Q.log_sum_pt - 18.875186284136564
    if Q.log_sum_pt >= 6.572937922293:
        z += 9.302843570709229 * Q.log_sum_pt - 60.56926491336863
    if Q.z_7 < 0.043044721986:
        z += 87.1691746711731 * Q.z_7 - 4.778858744005293
    if 0.043044721986 <= Q.z_7 < 0.055577157257:
        z += 81.92229461669922 * Q.z_7 - 4.553008250766577
    if Q.girth < 0.076081777364:
        z += -18.801443099975586 * Q.girth + 1.4304472080542565
    if Q.mass < 53.332374954224:
        z += 0.011390185914933681 * Q.mass - 0.6074656660135641
    if Q.width < 0.008678044951:
        z += 482.528076171875 * Q.width - 4.187400335139084
    if Q.planar_flow < 0.083662731125:
        z += -6.096721172332764 * Q.planar_flow + 0.5100683441849708
    if Q.tau21 < 0.197783735394:
        z += 4.014367580413818 * Q.tau21 - 0.7939766152988186
    if Q.e2_sq < 0.008168570676:
        z += -454.9080810546875 * Q.e2_sq + 3.7159488111787518
    if Q.C2 < 0.042322802544:
        z += 26.923494338989258 * Q.C2 - 1.139477734703544
    if Q.LHA < 0.346713497427:
        z += 3.466859817504883 * Q.LHA - 1.2020070924162487
    if Q.mass_over_sum_pt >= 0.054892207095:
        z += 21.766462326049805 * Q.mass_over_sum_pt - 1.1948091577270412
    if Q.n_pt_above_50 >= 6.0:
        z += 0.19365496933460236 * Q.n_pt_above_50 - 1.1619298160076141
    if Q.max_dr < 0.046566883102:
        z += 70.4786148071289 * Q.max_dr - 3.281969416914458
    if Q.lam1 < 0.008375572068 and Q.centroid_offset > 0.02076709205:
        z += 13355.525390625 * (0.008375572068 - Q.lam1) * (Q.centroid_offset - 0.02076709205)
    if Q.lam1 < 0.008375572068 and Q.z_7 > 0.039784489456:
        z += -1241.6859130859375 * (0.008375572068 - Q.lam1) * (Q.z_7 - 0.039784489456)
    if Q.pt_7 > 34.53125 and Q.mass < 91.19:
        z += -0.0014630791265517473 * (Q.pt_7 - 34.53125) * (91.19 - Q.mass)
    if Q.log_sum_pt > 6.377722943814 and Q.z_dr_0_0p05 < 0.90085350275:
        z += 0.426740437746048 * (Q.log_sum_pt - 6.377722943814) * (0.90085350275 - Q.z_dr_0_0p05)
    if Q.lam1 < 0.008375572068 and Q.lam2 < 0.000537286005:
        z += -8520.9990234375 * (0.008375572068 - Q.lam1) * (0.000537286005 - Q.lam2)
    if Q.z_7 < 0.055577157257 and Q.lam2 < 0.003408388935:
        z += 529.1622924804688 * (0.055577157257 - Q.z_7) * (0.003408388935 - Q.lam2)
    if Q.pt_7 > 34.53125 and Q.C2 > 0.004836016125:
        z += -0.06623619794845581 * (Q.pt_7 - 34.53125) * (Q.C2 - 0.004836016125)
    if Q.pt_7 > 34.53125 and Q.centroid_offset > 0.014379521101:
        z += 1.7930684089660645 * (Q.pt_7 - 34.53125) * (Q.centroid_offset - 0.014379521101)
    if Q.log_sum_pt > 6.377722943814 and Q.centroid_offset < 0.023554160423:
        z += -206.771728515625 * (Q.log_sum_pt - 6.377722943814) * (0.023554160423 - Q.centroid_offset)
    if Q.pt_7 > 53.4375 and Q.mass_top3 < 45.595:
        z += 0.005119578912854195 * (Q.pt_7 - 53.4375) * (45.595 - Q.mass_top3)
    if Q.log_sum_pt > 6.377722943814 and Q.max_dr < 0.197968879342:
        z += 11.92992115020752 * (Q.log_sum_pt - 6.377722943814) * (0.197968879342 - Q.max_dr)
    if Q.pt_7 > 34.53125 and Q.pt_6 < 52.90625:
        z += 0.0017021873500198126 * (Q.pt_7 - 34.53125) * (52.90625 - Q.pt_6)
    if Q.z_7 < 0.055577157257 and Q.dr01 > 0.055953954317:
        z += 53.26193618774414 * (0.055577157257 - Q.z_7) * (Q.dr01 - 0.055953954317)
    if Q.pt_7 > 53.4375 and Q.tau21 < 0.553068161011:
        z += -0.2563510835170746 * (Q.pt_7 - 53.4375) * (0.553068161011 - Q.tau21)
    if Q.log_sum_pt > 6.572937922293 and Q.D2 < 1.232133567333:
        z += 1.5201126337051392 * (Q.log_sum_pt - 6.572937922293) * (1.232133567333 - Q.D2)
    if Q.width < 0.008678044951 and Q.planar_flow < 0.083662731125:
        z += -1852.335205078125 * (0.008678044951 - Q.width) * (0.083662731125 - Q.planar_flow)
    if Q.e2 < 0.035560912266 and Q.eccentricity > 0.978160776925:
        z += 6066.12939453125 * (0.035560912266 - Q.e2) * (Q.eccentricity - 0.978160776925)
    if Q.z_7 < 0.055577157257 and Q.tau21 < 0.163363117725:
        z += 30.07939338684082 * (0.055577157257 - Q.z_7) * (0.163363117725 - Q.tau21)
    if Q.z_7 < 0.055577157257 and Q.C2 < 0.042322802544:
        z += 612.7081298828125 * (0.055577157257 - Q.z_7) * (0.042322802544 - Q.C2)
    if Q.e2 < 0.035560912266 and Q.mean_phi > 0.001618889696:
        z += -161.67185974121094 * (0.035560912266 - Q.e2) * (Q.mean_phi - 0.001618889696)
    if Q.pt_7 > 34.53125 and Q.max_dr < 0.080507021025:
        z += 0.8225708603858948 * (Q.pt_7 - 34.53125) * (0.080507021025 - Q.max_dr)
    if Q.pt_7 > 53.4375 and Q.mass_top3 < 32.617988451746:
        z += -0.0034427763894200325 * (Q.pt_7 - 53.4375) * (32.617988451746 - Q.mass_top3)
    if Q.log_sum_pt > 6.572937922293 and Q.max_dr < 0.290267042816:
        z += 0.2859514057636261 * (Q.log_sum_pt - 6.572937922293) * (0.290267042816 - Q.max_dr)
    if Q.tau21 < 0.197783735394 and Q.pt_6 < 50.25:
        z += -0.164889857172966 * (0.197783735394 - Q.tau21) * (50.25 - Q.pt_6)
    if Q.log_sum_pt > 6.572937922293 and Q.girth2_top3 < 0.006756161242:
        z += -1285.290283203125 * (Q.log_sum_pt - 6.572937922293) * (0.006756161242 - Q.girth2_top3)
    if Q.z_7 < 0.055577157257 and Q.girth2_top3 < 0.007929074034:
        z += 7193.83203125 * (0.055577157257 - Q.z_7) * (0.007929074034 - Q.girth2_top3)
    if Q.tau21 < 0.197783735394 and Q.lam2 < 0.000194798295:
        z += 21455.80859375 * (0.197783735394 - Q.tau21) * (0.000194798295 - Q.lam2)
    if Q.log_sum_pt > 6.572937922293 and Q.lam2 < 0.001130644719:
        z += 5814.5205078125 * (Q.log_sum_pt - 6.572937922293) * (0.001130644719 - Q.lam2)
    if Q.planar_flow < 0.083662731125 and Q.tau32 < 0.269169217348:
        z += -211.29396057128906 * (0.083662731125 - Q.planar_flow) * (0.269169217348 - Q.tau32)
    if Q.mass < 53.332374954224 and Q.mass_top3 > 23.663861485439:
        z += -0.001155233127065003 * (53.332374954224 - Q.mass) * (Q.mass_top3 - 23.663861485439)
    if Q.log_sum_pt > 6.572937922293 and Q.n_dr_0p1_0p2 > 1.0:
        z += -0.13354025781154633 * (Q.log_sum_pt - 6.572937922293) * (Q.n_dr_0p1_0p2 - 1.0)
    if Q.LHA < 0.346713497427 and Q.planar_flow < 0.083662731125:
        z += -80.38643646240234 * (0.346713497427 - Q.LHA) * (0.083662731125 - Q.planar_flow)
    if Q.lam1 < 0.008375572068 and Q.n_pt_above_50 > 6.0:
        z += -94.01914978027344 * (0.008375572068 - Q.lam1) * (Q.n_pt_above_50 - 6.0)
    if Q.e2_sq < 0.008168570676 and Q.planar_flow < 0.083662731125:
        z += -5841.3232421875 * (0.008168570676 - Q.e2_sq) * (0.083662731125 - Q.planar_flow)
    if Q.e2_sq < 0.008168570676 and Q.n_pt_above_50 > 6.0:
        z += 35.86458206176758 * (0.008168570676 - Q.e2_sq) * (Q.n_pt_above_50 - 6.0)
    if Q.log_sum_pt > 6.572937922293 and Q.planar_flow < 0.033200121667:
        z += 84.66653442382812 * (Q.log_sum_pt - 6.572937922293) * (0.033200121667 - Q.planar_flow)
    if Q.log_sum_pt > 6.572937922293 and Q.n_pt_above_50 > 7.0:
        z += -6.833393573760986 * (Q.log_sum_pt - 6.572937922293) * (Q.n_pt_above_50 - 7.0)
    if Q.log_sum_pt > 6.377722943814 and Q.n_pt_above_50 > 7.0:
        z += 0.11944511532783508 * (Q.log_sum_pt - 6.377722943814) * (Q.n_pt_above_50 - 7.0)
    if Q.planar_flow < 0.083662731125 and Q.mean_eta < 6.2888237e-05:
        z += 39.06167984008789 * (0.083662731125 - Q.planar_flow) * (6.2888237e-05 - Q.mean_eta)
    if Q.e2 > 0.032346998155 and Q.tau32 < 0.641386964917:
        z += -85.08639526367188 * (Q.e2 - 0.032346998155) * (0.641386964917 - Q.tau32)
    return max(0.0, z)


def neuron_2(Q):
    z = 2.8122711181640625
    if Q.mass < 8.379955863953:
        z += 0.07438577990978956 * Q.mass - 1.6168824039064842
    if 8.379955863953 <= Q.mass < 36.229410171509:
        z += 0.060785263776779175 * Q.mass - 1.5029106789848765
    if 36.229410171509 <= Q.mass < 69.611351776123:
        z += -0.020948559045791626 * Q.mass + 1.4582575129394846
    if Q.log_sum_pt < 6.267538488641:
        z += -3.6994175035506487 * Q.log_sum_pt + 23.98514330094026
    if 6.267538488641 <= Q.log_sum_pt < 6.464150123592:
        z += -2.7828805167227983 * Q.log_sum_pt + 18.240712459733658
    if 6.464150123592 <= Q.log_sum_pt < 6.572937922293:
        z += 0.2726090233772993 * Q.log_sum_pt - 1.510430628538452
    if 6.572937922293 <= Q.log_sum_pt < 6.638338705138:
        z += 0.893575755879283 * Q.log_sum_pt - 5.592006413083113
    if 6.638338705138 <= Q.log_sum_pt < 6.804164030582:
        z += 0.9165369868278503 * Q.log_sum_pt - 5.744430841206601
    if 6.804164030582 <= Q.log_sum_pt < 6.842716632804:
        z += 4.89373105764389 * Q.log_sum_pt - 32.805911680497104
    if 6.842716632804 <= Q.log_sum_pt < 6.896095378249:
        z += 12.75815862417221 * Q.log_sum_pt - 86.61996099746273
    if Q.log_sum_pt >= 6.896095378249:
        z += -1.7052136063575745 * Q.log_sum_pt + 13.120833395388662
    if Q.z_7 < 0.016858545121:
        z += 25.129531860351562 * Q.z_7 + 0.34650615494165393
    if 0.016858545121 <= Q.z_7 < 0.028070914944:
        z += -68.6878433227539 * Q.z_7 + 1.9281306075998232
    if Q.z_7 >= 0.046240320761:
        z += -32.80953598022461 * Q.z_7 + 1.5171234677451566
    if Q.lam1 < 0.003377388461:
        z += -461.0514373779297 * Q.lam1 + 2.311602934407239
    if 0.003377388461 <= Q.lam1 < 0.005954149834:
        z += -292.7912292480469 * Q.lam1 + 1.743322849023914
    if Q.width < 9.1213921e-05:
        z += 9085.396484375 * Q.width - 0.6758072228701621
    if 9.1213921e-05 <= Q.width < 0.000172198326:
        z += -1888.109375 * Q.width + 0.32512927367990624
    if Q.pt_7 < 15.55390625:
        z += 0.09389831125736237 * Q.pt_7 - 2.987445288867457
    if 15.55390625 <= Q.pt_7 < 30.484375:
        z += 0.028365395963191986 * Q.pt_7 - 1.9681524680927396
    if 30.484375 <= Q.pt_7 < 43.5:
        z += 0.18131949752569199 * Q.pt_7 - 6.6308626579120755
    if 43.5 <= Q.pt_7 < 53.4375:
        z += 0.22684167325496674 * Q.pt_7 - 8.611077302135527
    if Q.pt_7 >= 53.4375:
        z += 0.1529541015625 * Q.pt_7 - 4.662710189819336
    if Q.LHA >= 0.111565049159:
        z += -5.748402118682861 * Q.LHA + 0.6413207649565531
    if Q.planar_flow < 0.694781820497:
        z += 1.00908625125885 * Q.planar_flow - 0.701094782688117
    if Q.pt_6 < 56.53125:
        z += 0.005651099141687155 * Q.pt_6 - 0.31946369835350197
    if Q.sum_pt_top5 < 687.4375:
        z += 0.006341209169477224 * Q.sum_pt_top5 - 4.359184978442499
    if Q.sum_pt_top5 >= 839.9546875:
        z += -0.0017134201480075717 * Q.sum_pt_top5 + 1.4391952849759035
    if Q.sum_pt < 788.4484375:
        z += -0.011279389262199402 * Q.sum_pt + 8.893216839735397
    if Q.girth2 < 4.8108519e-05:
        z += 58616.33984375 * Q.girth2 - 2.819945299083504
    if Q.tau21 < 0.335550022125:
        z += -0.4259081482887268 * Q.tau21 + 0.14291348858150008
    if Q.girth2_top2 < 3.8495183e-05:
        z += -12147.5810546875 * Q.girth2_top2 + 0.4676233557075283
    if Q.max_dr < 0.15984864831:
        z += 2.388078212738037 * Q.max_dr - 0.38173107436473586
    if Q.mass < 69.611351776123 and Q.z_7 < 0.068101508468:
        z += -0.2727755606174469 * (69.611351776123 - Q.mass) * (0.068101508468 - Q.z_7)
    if Q.mass < 69.611351776123 and Q.centroid_offset > 0.010960638421:
        z += -0.019393285736441612 * (69.611351776123 - Q.mass) * (Q.centroid_offset - 0.010960638421)
    if Q.pt_7 > 30.484375 and Q.dr_0 > 0.031288303462:
        z += 0.08112535625696182 * (Q.pt_7 - 30.484375) * (Q.dr_0 - 0.031288303462)
    if Q.pt_7 > 30.484375 and Q.C2 < 0.051192347892:
        z += -1.9097871780395508 * (Q.pt_7 - 30.484375) * (0.051192347892 - Q.C2)
    if Q.z_7 < 0.028070914944 and Q.width < 0.00752008842:
        z += -18020.98828125 * (0.028070914944 - Q.z_7) * (0.00752008842 - Q.width)
    if Q.lam1 < 0.005954149834 and Q.max_dr > 0.080507021025:
        z += -1900.70361328125 * (0.005954149834 - Q.lam1) * (Q.max_dr - 0.080507021025)
    if Q.log_sum_pt > 6.842716632804 and Q.dr01 > 0.141033647649:
        z += 69.00959014892578 * (Q.log_sum_pt - 6.842716632804) * (Q.dr01 - 0.141033647649)
    if Q.pt_6 < 56.53125 and Q.m012 > 32.617988451746:
        z += -0.0009184412774629891 * (56.53125 - Q.pt_6) * (Q.m012 - 32.617988451746)
    if Q.mass < 36.229410171509 and Q.lam2 < 0.001130644719:
        z += 49.69545364379883 * (36.229410171509 - Q.mass) * (0.001130644719 - Q.lam2)
    if Q.pt_7 > 30.484375 and Q.max_dr > 0.093110798299:
        z += -0.5839080214500427 * (Q.pt_7 - 30.484375) * (Q.max_dr - 0.093110798299)
    if Q.log_sum_pt > 6.842716632804 and Q.n_pt_above_50 > 5.0:
        z += -0.9447485208511353 * (Q.log_sum_pt - 6.842716632804) * (Q.n_pt_above_50 - 5.0)
    if Q.mass < 36.229410171509 and Q.pt_4 < 55.65625:
        z += -4.084295505890623e-05 * (36.229410171509 - Q.mass) * (55.65625 - Q.pt_4)
    if Q.lam1 < 0.003377388461 and Q.centroid_offset < 0.006789738266:
        z += -46020.27734375 * (0.003377388461 - Q.lam1) * (0.006789738266 - Q.centroid_offset)
    if Q.mass < 8.379955863953 and Q.centroid_offset < 0.010960638421:
        z += 26.942678451538086 * (8.379955863953 - Q.mass) * (0.010960638421 - Q.centroid_offset)
    if Q.pt_7 > 30.484375 and Q.centroid_offset > 0.012587644117:
        z += -0.9793556332588196 * (Q.pt_7 - 30.484375) * (Q.centroid_offset - 0.012587644117)
    if Q.sum_pt_top5 > 839.9546875 and Q.dr_7 < 0.04881348081:
        z += 0.15877099335193634 * (Q.sum_pt_top5 - 839.9546875) * (0.04881348081 - Q.dr_7)
    if Q.width < 9.1213921e-05 and Q.pt_2 < 154.25:
        z += 58.409481048583984 * (9.1213921e-05 - Q.width) * (154.25 - Q.pt_2)
    if Q.pt_6 < 56.53125 and Q.lam2 > 0.000306123359:
        z += 2.0102460384368896 * (56.53125 - Q.pt_6) * (Q.lam2 - 0.000306123359)
    if Q.log_sum_pt > 6.842716632804 and Q.z_3rd < 0.073680565134:
        z += 112.98939514160156 * (Q.log_sum_pt - 6.842716632804) * (0.073680565134 - Q.z_3rd)
    if Q.mass < 8.379955863953 and Q.z_2 < 0.181856399189:
        z += 0.38553953170776367 * (8.379955863953 - Q.mass) * (0.181856399189 - Q.z_2)
    if Q.mass < 36.229410171509 and Q.mean_phi < -0.003096654534:
        z += 0.40444329380989075 * (36.229410171509 - Q.mass) * (-0.003096654534 - Q.mean_phi)
    if Q.log_sum_pt < 6.464150123592 and Q.eta_0 > 0.029803466797:
        z += -0.8472163081169128 * (6.464150123592 - Q.log_sum_pt) * (Q.eta_0 - 0.029803466797)
    if Q.pt_7 > 30.484375 and Q.z_dr_0p05_0p1 < 0.750909513235:
        z += -0.012145488522946835 * (Q.pt_7 - 30.484375) * (0.750909513235 - Q.z_dr_0p05_0p1)
    if Q.mass < 69.611351776123 and Q.max_pair_mass > 13.047927274731:
        z += -0.001830283203162253 * (69.611351776123 - Q.mass) * (Q.max_pair_mass - 13.047927274731)
    if Q.log_sum_pt > 6.267538488641 and Q.phi_0 < 0.004838562012:
        z += 3.187058448791504 * (Q.log_sum_pt - 6.267538488641) * (0.004838562012 - Q.phi_0)
    if Q.log_sum_pt < 6.572937922293 and Q.eccentricity > 0.779212655895:
        z += 3.5319325923919678 * (6.572937922293 - Q.log_sum_pt) * (Q.eccentricity - 0.779212655895)
    if Q.width < 0.000172198326 and Q.dr_7 < 0.222994708167:
        z += -32001.51953125 * (0.000172198326 - Q.width) * (0.222994708167 - Q.dr_7)
    if Q.log_sum_pt < 6.464150123592 and Q.dr_7 < 0.072549472237:
        z += 17.240314483642578 * (6.464150123592 - Q.log_sum_pt) * (0.072549472237 - Q.dr_7)
    if Q.sum_pt < 788.4484375 and Q.dr_7 < 0.063966271204:
        z += -0.021203413605690002 * (788.4484375 - Q.sum_pt) * (0.063966271204 - Q.dr_7)
    return max(0.0, z)


def neuron_3(Q):
    z = 3.261817455291748
    if 0.06813910019 <= Q.mass_over_sum_pt < 0.090413827016:
        z += -51.058284759521484 * Q.mass_over_sum_pt + 3.479065580758584
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += -3.4567031860351562 * Q.mass_over_sum_pt - 0.8247755813146216
    if Q.mass_over_sum_pt >= 0.107985668755:
        z += -35.53750991821289 * Q.mass_over_sum_pt + 2.6394917878594972
    if Q.centroid_offset >= 0.014379521101:
        z += 56.415706634521484 * Q.centroid_offset - 0.8112308439789273
    if Q.width < 0.006679471358:
        z += -138.06686401367188 * Q.width + 0.9222136636682021
    if Q.width >= 0.018827653081:
        z += 100.99311065673828 * Q.width - 1.9014632510161127
    if 36.229410171509 <= Q.mass < 69.611351776123:
        z += -0.02750324457883835 * Q.mass + 0.9964263288940659
    if Q.mass >= 69.611351776123:
        z += -0.05303528346121311 * Q.mass + 2.7737460690967057
    if Q.e2 < 0.028531698044:
        z += -137.70591843128204 * Q.e2 + 6.133462579255209
    if 0.028531698044 <= Q.e2 < 0.038466955721:
        z += -181.23672592639923 * Q.e2 + 7.375470434317385
    if 0.038466955721 <= Q.e2 < 0.04447356835:
        z += -182.76654052734375 * Q.e2 + 7.4343177448332565
    if Q.e2 >= 0.04447356835:
        z += -43.53080749511719 * Q.e2 + 1.2420078550621756
    if 0.312727471086 <= Q.LHA < 0.325582223496:
        z += 18.363731384277344 * Q.LHA - 5.742843275507664
    if 0.325582223496 <= Q.LHA < 0.423592510895:
        z += 30.95234966278076 * Q.LHA - 9.841473605365195
    if Q.LHA >= 0.423592510895:
        z += 13.464982032775879 * Q.LHA - 2.433955642027481
    if Q.girth2 < 0.004372139461:
        z += 1120.3692932128906 * Q.girth2 - 13.989169789706041
    if 0.004372139461 <= Q.girth2 < 0.008678044751:
        z += 1638.5450744628906 * Q.girth2 - 16.25470657064367
    if 0.008678044751 <= Q.girth2 < 0.013238675334:
        z += 446.2845764160156 * Q.girth2 - 5.908216613743344
    if Q.lam1 < 0.007330079875:
        z += -301.8611755371094 * Q.lam1 + 2.2126665278484077
    if 0.012003726523 <= Q.lam1 < 0.016433749775:
        z += -281.65789794921875 * Q.lam1 + 3.3809443800254644
    if Q.lam1 >= 0.016433749775:
        z += -229.93856048583984 * Q.lam1 + 2.531001729623512
    if Q.mass_top5 >= 53.607658247923:
        z += -0.06864731013774872 * Q.mass_top5 + 3.680021541503613
    if Q.mean_eta < -0.012844925793:
        z += -13.843114852905273 * Q.mean_eta - 0.17781378302954437
    if Q.z_dr_0p1_0p2 < 0.468445876241:
        z += 0.4213344156742096 * Q.z_dr_0p1_0p2 - 0.19737236954099482
    if Q.max_dr >= 0.145231109113:
        z += 14.268226623535156 * Q.max_dr - 2.072190377611646
    if Q.C2 >= 0.094821243733:
        z += 71.6023178100586 * Q.C2 - 6.789420828915293
    if Q.mass_over_sum_pt > 0.06813910019 and Q.tau32 < 0.518696343899:
        z += -78.85592651367188 * (Q.mass_over_sum_pt - 0.06813910019) * (0.518696343899 - Q.tau32)
    if Q.e2 > 0.028531698044 and Q.n_pt_above_50 > 3.0:
        z += -4.116652488708496 * (Q.e2 - 0.028531698044) * (Q.n_pt_above_50 - 3.0)
    if Q.mass > 36.229410171509 and Q.lam2 < 0.001130644719:
        z += 28.254682540893555 * (Q.mass - 36.229410171509) * (0.001130644719 - Q.lam2)
    if Q.mass_over_sum_pt > 0.06813910019 and Q.n_dr_0_0p05 < 5.0:
        z += 11.216885566711426 * (Q.mass_over_sum_pt - 0.06813910019) * (5.0 - Q.n_dr_0_0p05)
    if Q.LHA > 0.312727471086 and Q.mass_top3 < 50.352200171245:
        z += -0.529278039932251 * (Q.LHA - 0.312727471086) * (50.352200171245 - Q.mass_top3)
    if Q.e2 < 0.04447356835 and Q.z_dr_0p05_0p1 < 0.964120104909:
        z += -23.62833595275879 * (0.04447356835 - Q.e2) * (0.964120104909 - Q.z_dr_0p05_0p1)
    if Q.mass > 36.229410171509 and Q.eccentricity > 0.620723099573:
        z += 0.11695258319377899 * (Q.mass - 36.229410171509) * (Q.eccentricity - 0.620723099573)
    if Q.e2 < 0.04447356835 and Q.z_dr_0p1_0p2 > 0.0:
        z += -193.63832092285156 * (0.04447356835 - Q.e2) * (Q.z_dr_0p1_0p2 - 0.0)
    if Q.centroid_offset > 0.014379521101 and Q.phi_7 > -0.041534423828:
        z += 127.93888854980469 * (Q.centroid_offset - 0.014379521101) * (Q.phi_7 - -0.041534423828)
    if Q.centroid_offset > 0.014379521101 and Q.eta_0 < -0.039672851562:
        z += -483.80816650390625 * (Q.centroid_offset - 0.014379521101) * (-0.039672851562 - Q.eta_0)
    if Q.mass > 36.229410171509 and Q.phi_5 > 0.112796020508:
        z += 0.10872404277324677 * (Q.mass - 36.229410171509) * (Q.phi_5 - 0.112796020508)
    if Q.width > 0.018827653081 and Q.pt_dispersion < 0.492494773865:
        z += 253.88844299316406 * (Q.width - 0.018827653081) * (0.492494773865 - Q.pt_dispersion)
    if Q.width > 0.018827653081 and Q.z_3 > 0.090493038582:
        z += 442.7025451660156 * (Q.width - 0.018827653081) * (Q.z_3 - 0.090493038582)
    if Q.mass > 36.229410171509 and Q.dr_6 < 0.046481671275:
        z += -1.9941701889038086 * (Q.mass - 36.229410171509) * (0.046481671275 - Q.dr_6)
    if Q.mass_over_sum_pt > 0.06813910019 and Q.dr_7 < 0.042151962757:
        z += -5606.9208984375 * (Q.mass_over_sum_pt - 0.06813910019) * (0.042151962757 - Q.dr_7)
    if Q.mass > 69.611351776123 and Q.z_2nd < 0.15222851187:
        z += -0.13483686745166779 * (Q.mass - 69.611351776123) * (0.15222851187 - Q.z_2nd)
    if Q.LHA > 0.312727471086 and Q.max_dr < 0.145231109113:
        z += -2163.956298828125 * (Q.LHA - 0.312727471086) * (0.145231109113 - Q.max_dr)
    if Q.LHA > 0.312727471086 and Q.planar_flow > 0.00804883781:
        z += -13.211687088012695 * (Q.LHA - 0.312727471086) * (Q.planar_flow - 0.00804883781)
    if Q.centroid_offset > 0.014379521101 and Q.phi_6 > 0.119201660156:
        z += 602.354248046875 * (Q.centroid_offset - 0.014379521101) * (Q.phi_6 - 0.119201660156)
    if Q.mass_over_sum_pt > 0.090413827016 and Q.max_dr < 0.145231109113:
        z += 8347.2568359375 * (Q.mass_over_sum_pt - 0.090413827016) * (0.145231109113 - Q.max_dr)
    if Q.mass > 69.611351776123 and Q.max_dr < 0.177304983139:
        z += 2.519543409347534 * (Q.mass - 69.611351776123) * (0.177304983139 - Q.max_dr)
    if Q.max_dr > 0.145231109113 and Q.dr_3 < 0.04586879935:
        z += -443.32916259765625 * (Q.max_dr - 0.145231109113) * (0.04586879935 - Q.dr_3)
    if Q.lam1 > 0.016433749775 and Q.eccentricity > 0.959856212153:
        z += -10527.62890625 * (Q.lam1 - 0.016433749775) * (Q.eccentricity - 0.959856212153)
    if Q.max_dr > 0.145231109113 and Q.eta_1 < -0.059631347656:
        z += 12.002096176147461 * (Q.max_dr - 0.145231109113) * (-0.059631347656 - Q.eta_1)
    if Q.mean_eta < -0.012844925793 and Q.pt_4 < 68.125:
        z += -3.1130213737487793 * (-0.012844925793 - Q.mean_eta) * (68.125 - Q.pt_4)
    if Q.mean_eta < -0.012844925793 and Q.z_4 < 0.120257140434:
        z += 1428.999267578125 * (-0.012844925793 - Q.mean_eta) * (0.120257140434 - Q.z_4)
    if Q.LHA > 0.312727471086 and Q.pt_5 < 29.875:
        z += 14.8013916015625 * (Q.LHA - 0.312727471086) * (29.875 - Q.pt_5)
    if Q.z_dr_0p1_0p2 < 0.468445876241 and Q.eta_2 > 0.096557617188:
        z += 19.53888702392578 * (0.468445876241 - Q.z_dr_0p1_0p2) * (Q.eta_2 - 0.096557617188)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.dr_7 < 0.04881348081:
        z += 18756.25 * (Q.mass_over_sum_pt - 0.107985668755) * (0.04881348081 - Q.dr_7)
    if Q.LHA > 0.312727471086 and Q.eccentricity > 0.959856212153:
        z += 1092.17138671875 * (Q.LHA - 0.312727471086) * (Q.eccentricity - 0.959856212153)
    if Q.e2 > 0.028531698044 and Q.eccentricity > 0.959856212153:
        z += -1844.716552734375 * (Q.e2 - 0.028531698044) * (Q.eccentricity - 0.959856212153)
    if Q.mass_over_sum_pt > 0.090413827016 and Q.pt_6 < 56.53125:
        z += -1.2240136861801147 * (Q.mass_over_sum_pt - 0.090413827016) * (56.53125 - Q.pt_6)
    if Q.lam1 > 0.012003726523 and Q.pt_6 < 38.25:
        z += 35.33583068847656 * (Q.lam1 - 0.012003726523) * (38.25 - Q.pt_6)
    if Q.mass_over_sum_pt > 0.090413827016 and Q.pt_7 < 48.71875:
        z += 0.9272748827934265 * (Q.mass_over_sum_pt - 0.090413827016) * (48.71875 - Q.pt_7)
    if Q.mass > 36.229410171509 and Q.pt_7 < 20.125:
        z += -0.005710049998015165 * (Q.mass - 36.229410171509) * (20.125 - Q.pt_7)
    return max(0.0, z)


def neuron_4(Q):
    z = -7.011570930480957
    if Q.tau21 < 0.23799610585:
        z += -27.527206420898438 * Q.tau21 + 6.551367933102944
    if Q.lam2 < 0.000306123359:
        z += 5311.960174560547 * Q.lam2 - 1.8113785341073492
    if 0.000306123359 <= Q.lam2 < 0.001130644719:
        z += 224.69210815429688 * Q.lam2 - 0.2540469454856326
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += -229.15216064453125 * Q.mass_over_sum_pt + 20.718523812857292
    if Q.mass_over_sum_pt >= 0.107985668755:
        z += 141.37277221679688 * Q.mass_over_sum_pt - 19.292858852574703
    if 0.000319370692 <= Q.width < 0.001653836415:
        z += -493.94873046875 * Q.width + 0.15775274786232618
    if Q.width >= 0.001653836415:
        z += 507.43304443359375 * Q.width - 1.498368896788503
    if 0.007078157854 <= Q.e2 < 0.041109715588:
        z += 74.35980224609375 * Q.e2 - 0.5263304182900753
    if 0.041109715588 <= Q.e2 < 0.063441075385:
        z += 57.895681381225586 * Q.e2 + 0.15050490787111148
    if Q.e2 >= 0.063441075385:
        z += -54.74304389953613 * Q.e2 + 7.296426769678221
    if Q.sum_pt < 763.825:
        z += -0.007819169200956821 * Q.sum_pt + 5.972476914920844
    if Q.girth2_top2 < 0.009530300104:
        z += 33.63375473022461 * Q.girth2_top2 - 0.3205397762033701
    if Q.mass < 56.920347213745:
        z += 0.0003012120723724365 * Q.mass - 0.961556674233357
    if 56.920347213745 <= Q.mass < 69.611351776123:
        z += 0.07441582530736923 * Q.mass - 5.180186193181796
    if 0.014943876117 <= Q.C2 < 0.067292226106:
        z += -54.4916877746582 * Q.C2 + 0.8143170315107356
    if Q.C2 >= 0.067292226106:
        z += -181.4041862487793 * Q.C2 + 9.354541574508673
    if Q.girth2_top3 < 0.005011406868:
        z += -421.2523498535156 * Q.girth2_top3 + 2.111066919217047
    if Q.girth < 0.047915700823:
        z += -34.779212951660156 * Q.girth + 1.6664703626511548
    if Q.girth >= 0.101940929517:
        z += 8.319043159484863 * Q.girth - 0.8480509923699274
    if Q.e2_sq < 0.017162483186:
        z += -500.3290023803711 * Q.e2_sq + 9.277138902494745
    if 0.017162483186 <= Q.e2_sq < 0.023780909279:
        z += -104.29228973388672 * Q.e2_sq + 2.480165480660743
    if Q.girth2 >= 0.013238675334:
        z += -212.4739532470703 * Q.girth2 + 2.812873683969459
    if Q.sum_pt_top5 < 430.75:
        z += -0.012219972908496857 * Q.sum_pt_top5 + 5.263753330335021
    if Q.centroid_offset < 0.014379521101:
        z += -115.81883239746094 * Q.centroid_offset + 1.6654193443524719
    if 0.102758520097 <= Q.max_dr < 0.197968879342:
        z += 14.108174324035645 * Q.max_dr - 1.4497351148083961
    if Q.max_dr >= 0.197968879342:
        z += -7.024687767028809 * Q.max_dr + 2.7339139106486687
    if Q.mass_over_sum_pt_sq < 0.001101860861:
        z += -982.019775390625 * Q.mass_over_sum_pt_sq + 1.0820491552309408
    if Q.tau21 < 0.23799610585 and Q.mass < 62.55:
        z += -0.6625921726226807 * (0.23799610585 - Q.tau21) * (62.55 - Q.mass)
    if Q.tau21 < 0.23799610585 and Q.e2_sq > 0.011657374702:
        z += -1714.8460693359375 * (0.23799610585 - Q.tau21) * (Q.e2_sq - 0.011657374702)
    if Q.tau21 < 0.23799610585 and Q.lam2 < 0.001130644719:
        z += -11852.212890625 * (0.23799610585 - Q.tau21) * (0.001130644719 - Q.lam2)
    if Q.tau21 < 0.23799610585 and Q.pt_6 < 62.25:
        z += -0.05397845432162285 * (0.23799610585 - Q.tau21) * (62.25 - Q.pt_6)
    if Q.sum_pt < 763.825 and Q.z_dr_0_0p05 > 0.151540452242:
        z += 0.001247952925041318 * (763.825 - Q.sum_pt) * (Q.z_dr_0_0p05 - 0.151540452242)
    if Q.width > 0.000319370692 and Q.C2 < 0.067292226106:
        z += 4383.3837890625 * (Q.width - 0.000319370692) * (0.067292226106 - Q.C2)
    if Q.tau21 < 0.23799610585 and Q.mean_eta > 0.02644207105:
        z += -141.85507202148438 * (0.23799610585 - Q.tau21) * (Q.mean_eta - 0.02644207105)
    if Q.girth2_top2 < 0.009530300104 and Q.centroid_offset > 0.016278845848:
        z += 12459.9228515625 * (0.009530300104 - Q.girth2_top2) * (Q.centroid_offset - 0.016278845848)
    if Q.tau21 < 0.23799610585 and Q.planar_flow > 0.045057236346:
        z += 27.61488914489746 * (0.23799610585 - Q.tau21) * (Q.planar_flow - 0.045057236346)
    if Q.tau21 < 0.23799610585 and Q.mean_phi > 0.004406178184:
        z += -139.07119750976562 * (0.23799610585 - Q.tau21) * (Q.mean_phi - 0.004406178184)
    if Q.mass < 69.611351776123 and Q.mean_eta2 > 0.004247450386:
        z += -0.332247257232666 * (69.611351776123 - Q.mass) * (Q.mean_eta2 - 0.004247450386)
    if Q.sum_pt < 763.825 and Q.n_dr_0p2_0p4 < 1.0:
        z += -0.001854314235970378 * (763.825 - Q.sum_pt) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.width > 0.000319370692 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += -626.10595703125 * (Q.width - 0.000319370692) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.tau21 < 0.23799610585 and Q.dr_7 < 0.175465903809:
        z += 30.097591400146484 * (0.23799610585 - Q.tau21) * (0.175465903809 - Q.dr_7)
    if Q.tau21 < 0.23799610585 and Q.pt_7 < 23.21640625:
        z += -0.5841887593269348 * (0.23799610585 - Q.tau21) * (23.21640625 - Q.pt_7)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.n_dr_0p1_0p2 > 6.0:
        z += 9.377594947814941 * (Q.mass_over_sum_pt - 0.107985668755) * (Q.n_dr_0p1_0p2 - 6.0)
    if Q.lam2 < 0.001130644719 and Q.n_dr_0p1_0p2 > 2.0:
        z += -206.49623107910156 * (0.001130644719 - Q.lam2) * (Q.n_dr_0p1_0p2 - 2.0)
    if Q.tau21 < 0.23799610585 and Q.phi_6 > 0.119201660156:
        z += -43.70795822143555 * (0.23799610585 - Q.tau21) * (Q.phi_6 - 0.119201660156)
    if Q.girth2_top3 < 0.005011406868 and Q.mean_eta < -0.009391680919:
        z += 8083.79150390625 * (0.005011406868 - Q.girth2_top3) * (-0.009391680919 - Q.mean_eta)
    if Q.mass < 69.611351776123 and Q.dr_3 < 0.104247858869:
        z += 0.15763267874717712 * (69.611351776123 - Q.mass) * (0.104247858869 - Q.dr_3)
    if Q.tau21 < 0.23799610585 and Q.dr_6 < 0.169508891404:
        z += 3.166071653366089 * (0.23799610585 - Q.tau21) * (0.169508891404 - Q.dr_6)
    if Q.tau21 < 0.23799610585 and Q.mean_phi < -0.025945045147:
        z += -439.53375244140625 * (0.23799610585 - Q.tau21) * (-0.025945045147 - Q.mean_phi)
    if Q.tau21 < 0.23799610585 and Q.pt_7 > 33.21875:
        z += 0.8346267938613892 * (0.23799610585 - Q.tau21) * (Q.pt_7 - 33.21875)
    if Q.girth2_top2 < 0.009530300104 and Q.dr_4 > 0.199975347593:
        z += -1388.561279296875 * (0.009530300104 - Q.girth2_top2) * (Q.dr_4 - 0.199975347593)
    if Q.e2_sq < 0.017162483186 and Q.eta_4 < -0.10657043457:
        z += 190.47979736328125 * (0.017162483186 - Q.e2_sq) * (-0.10657043457 - Q.eta_4)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.D2 < 3.885568320751:
        z += -62.783546447753906 * (Q.mass_over_sum_pt - 0.107985668755) * (3.885568320751 - Q.D2)
    if Q.max_dr > 0.102758520097 and Q.pt_7 > 37.15625:
        z += -2.580423593521118 * (Q.max_dr - 0.102758520097) * (Q.pt_7 - 37.15625)
    if Q.C2 > 0.014943876117 and Q.pt_7 > 38.53125:
        z += 12.294214248657227 * (Q.C2 - 0.014943876117) * (Q.pt_7 - 38.53125)
    if Q.lam2 < 0.000306123359 and Q.mass_top3 < 50.352200171245:
        z += -50.265438079833984 * (0.000306123359 - Q.lam2) * (50.352200171245 - Q.mass_top3)
    if Q.centroid_offset < 0.014379521101 and Q.z_dr_0p05_0p1 < 0.674770402908:
        z += -103.283447265625 * (0.014379521101 - Q.centroid_offset) * (0.674770402908 - Q.z_dr_0p05_0p1)
    if Q.tau21 < 0.23799610585 and Q.pt_2 > 73.6875:
        z += 0.03897000476717949 * (0.23799610585 - Q.tau21) * (Q.pt_2 - 73.6875)
    if Q.tau21 < 0.23799610585 and Q.phi_0 < -0.040130615234:
        z += -2.8180065155029297 * (0.23799610585 - Q.tau21) * (-0.040130615234 - Q.phi_0)
    if Q.sum_pt_top5 < 430.75 and Q.pt_5 > 73.75:
        z += -0.24087458848953247 * (430.75 - Q.sum_pt_top5) * (Q.pt_5 - 73.75)
    return max(0.0, z)


def neuron_5(Q):
    z = 0.32938241958618164
    if Q.LHA < 0.154689112391:
        z += -16.581667631864548 * Q.LHA + 3.599707415393585
    if 0.154689112391 <= Q.LHA < 0.216055863061:
        z += -16.860986709594727 * Q.LHA + 3.642915035601539
    if Q.z_7 < 0.03243272066:
        z += -160.6236333847046 * Q.z_7 + 8.199689458666507
    if 0.03243272066 <= Q.z_7 < 0.049399692737:
        z += -84.81667995452881 * Q.z_7 + 5.741063713979988
    if 0.049399692737 <= Q.z_7 < 0.071488645583:
        z += -70.22269439697266 * Q.z_7 + 5.020125311628498
    if 6.572937922293 <= Q.log_sum_pt < 6.896095378249:
        z += 0.44143757224082947 * Q.log_sum_pt - 2.9015417589067036
    if Q.log_sum_pt >= 6.896095378249:
        z += -19.077368885278702 * Q.log_sum_pt + 131.70200924173045
    if Q.e2_sq < 0.00528466865:
        z += -190.9046630859375 * Q.e2_sq + 1.0088678881490662
    if Q.z_6 < 0.028865759995:
        z += -86.10581970214844 * Q.z_6 + 2.4855099256949593
    if Q.dr_0 < 0.021588001063:
        z += 252.9560775756836 * Q.dr_0 - 5.889509398525307
    if 0.021588001063 <= Q.dr_0 < 0.026454043164:
        z += 88.0989761352539 * Q.dr_0 - 2.3305741173862127
    if Q.e2 < 0.035560912266:
        z += -50.25151824951172 * Q.e2 + 1.7869898317041841
    if Q.width < 0.002635417778:
        z += -365.2965393066406 * Q.width + 0.9627089939305965
    if Q.girth2 < 4.8108519e-05:
        z += -33099.9453125 * Q.girth2 + 1.5923893479653672
    if Q.mass_over_sum_pt < 0.084751611895:
        z += 7.559699058532715 * Q.mass_over_sum_pt - 0.6406966806517616
    if Q.girth2_top5 < 0.002270363079:
        z += 666.7166137695312 * Q.girth2_top5 - 1.513688784058247
    if Q.sum_pt_top5 >= 752.1:
        z += 0.010539122857153416 * Q.sum_pt_top5 - 7.926474300865084
    if Q.sum_pt_top2 < 548.196875:
        z += 0.0018576470902189612 * Q.sum_pt_top2 - 1.0183563297108775
    if Q.pt_5 < 24.578125:
        z += 0.1876600831747055 * Q.pt_5 - 4.612332981778309
    if Q.sum_pt >= 868.509375:
        z += -0.025428522378206253 * Q.sum_pt + 22.084910077869427
    if Q.mean_phi2 < 0.01426135283:
        z += -50.56047439575195 * Q.mean_phi2 + 0.7210607646099997
    if Q.z_dr_0p1_0p2 < 0.045106684603:
        z += -3.1464691162109375 * Q.z_dr_0p1_0p2 + 0.1419267900380069
    if Q.z_7 < 0.049399692737 and Q.mass_top5 < 62.55:
        z += 1.1387035846710205 * (0.049399692737 - Q.z_7) * (62.55 - Q.mass_top5)
    if Q.LHA < 0.216055863061 and Q.log_sum_pt < 6.804164030582:
        z += -103.45568084716797 * (0.216055863061 - Q.LHA) * (6.804164030582 - Q.log_sum_pt)
    if Q.e2_sq < 0.00528466865 and Q.centroid_offset < 0.014379521101:
        z += -7076.568359375 * (0.00528466865 - Q.e2_sq) * (0.014379521101 - Q.centroid_offset)
    if Q.z_7 < 0.071488645583 and Q.centroid_offset < 0.031170772021:
        z += -3207.64306640625 * (0.071488645583 - Q.z_7) * (0.031170772021 - Q.centroid_offset)
    if Q.z_7 < 0.071488645583 and Q.sum_pt < 788.4484375:
        z += -0.2565552592277527 * (0.071488645583 - Q.z_7) * (788.4484375 - Q.sum_pt)
    if Q.z_7 < 0.071488645583 and Q.lam1 < 0.001503553356:
        z += -24546.3671875 * (0.071488645583 - Q.z_7) * (0.001503553356 - Q.lam1)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_4 > 0.030068239644:
        z += 169.98324584960938 * (Q.log_sum_pt - 6.896095378249) * (Q.dr_4 - 0.030068239644)
    if Q.e2_sq < 0.00528466865 and Q.n_pt_above_50 > 6.0:
        z += -103.70372772216797 * (0.00528466865 - Q.e2_sq) * (Q.n_pt_above_50 - 6.0)
    if Q.LHA < 0.216055863061 and Q.n_dr_0p2_0p4 > 0.0:
        z += -12.82978630065918 * (0.216055863061 - Q.LHA) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.z_7 < 0.071488645583 and Q.n_dr_0p2_0p4 < 1.0:
        z += 12.270661354064941 * (0.071488645583 - Q.z_7) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.log_sum_pt > 6.896095378249 and Q.planar_flow < 0.045057236346:
        z += -325.46917724609375 * (Q.log_sum_pt - 6.896095378249) * (0.045057236346 - Q.planar_flow)
    if Q.z_7 < 0.071488645583 and Q.lam2 < 0.001130644719:
        z += 7628.66259765625 * (0.071488645583 - Q.z_7) * (0.001130644719 - Q.lam2)
    if Q.width < 0.002635417778 and Q.centroid_offset < 0.023554160423:
        z += 84563.9609375 * (0.002635417778 - Q.width) * (0.023554160423 - Q.centroid_offset)
    if Q.log_sum_pt > 6.572937922293 and Q.centroid_offset > 0.018377780003:
        z += -385.733642578125 * (Q.log_sum_pt - 6.572937922293) * (Q.centroid_offset - 0.018377780003)
    if Q.z_6 < 0.028865759995 and Q.phi_0 > 0.014526367188:
        z += -1945.9288330078125 * (0.028865759995 - Q.z_6) * (Q.phi_0 - 0.014526367188)
    if Q.z_7 < 0.03243272066 and Q.pt_5 > 33.0265625:
        z += 3.7880752086639404 * (0.03243272066 - Q.z_7) * (Q.pt_5 - 33.0265625)
    if Q.sum_pt > 868.509375 and Q.centroid_offset < 0.012587644117:
        z += 1.3575981855392456 * (Q.sum_pt - 868.509375) * (0.012587644117 - Q.centroid_offset)
    if Q.mass_over_sum_pt < 0.084751611895 and Q.mass_top3 > 28.345095968085:
        z += -3.1496317386627197 * (0.084751611895 - Q.mass_over_sum_pt) * (Q.mass_top3 - 28.345095968085)
    if Q.log_sum_pt > 6.896095378249 and Q.centroid_offset < 0.018377780003:
        z += -1038.95947265625 * (Q.log_sum_pt - 6.896095378249) * (0.018377780003 - Q.centroid_offset)
    if Q.log_sum_pt > 6.572937922293 and Q.mean_phi2 < 0.000145482056:
        z += 19602.861328125 * (Q.log_sum_pt - 6.572937922293) * (0.000145482056 - Q.mean_phi2)
    if Q.sum_pt_top2 < 548.196875 and Q.dr_0 < 0.021588001063:
        z += 0.3151956796646118 * (548.196875 - Q.sum_pt_top2) * (0.021588001063 - Q.dr_0)
    if Q.log_sum_pt > 6.572937922293 and Q.dr_0 < 0.021588001063:
        z += 578.2640991210938 * (Q.log_sum_pt - 6.572937922293) * (0.021588001063 - Q.dr_0)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_0 < 0.04118638065:
        z += -996.1826782226562 * (Q.log_sum_pt - 6.896095378249) * (0.04118638065 - Q.dr_0)
    if Q.pt_5 < 24.578125 and Q.centroid_offset < 0.001308549272:
        z += 192.0680694580078 * (24.578125 - Q.pt_5) * (0.001308549272 - Q.centroid_offset)
    if Q.z_7 < 0.071488645583 and Q.mean_phi2 < 0.004331280361:
        z += -1812.3516845703125 * (0.071488645583 - Q.z_7) * (0.004331280361 - Q.mean_phi2)
    if Q.log_sum_pt > 6.572937922293 and Q.lam1 < 0.012003726523:
        z += -1126.51904296875 * (Q.log_sum_pt - 6.572937922293) * (0.012003726523 - Q.lam1)
    if Q.log_sum_pt > 6.572937922293 and Q.girth2_top2 < 0.006299534492:
        z += 537.87255859375 * (Q.log_sum_pt - 6.572937922293) * (0.006299534492 - Q.girth2_top2)
    if Q.sum_pt_top2 < 548.196875 and Q.girth2_top3 < 0.003952581551:
        z += -2.2214155197143555 * (548.196875 - Q.sum_pt_top2) * (0.003952581551 - Q.girth2_top3)
    if Q.log_sum_pt > 6.572937922293 and Q.mean_eta2 < 9.0303693e-05:
        z += 39257.4765625 * (Q.log_sum_pt - 6.572937922293) * (9.0303693e-05 - Q.mean_eta2)
    if Q.pt_5 < 24.578125 and Q.mean_eta2 > 1.7977892e-05:
        z += 40.781532287597656 * (24.578125 - Q.pt_5) * (Q.mean_eta2 - 1.7977892e-05)
    if Q.mass_over_sum_pt < 0.084751611895 and Q.max_pair_mass < 18.097979966098:
        z += 0.7896831631660461 * (0.084751611895 - Q.mass_over_sum_pt) * (18.097979966098 - Q.max_pair_mass)
    if Q.LHA < 0.216055863061 and Q.mass_top3 > 3.559569591142:
        z += -1.5268110036849976 * (0.216055863061 - Q.LHA) * (Q.mass_top3 - 3.559569591142)
    if Q.mean_phi2 < 0.01426135283 and Q.max_pair_mass < 40.046952646555:
        z += 1.6951649188995361 * (0.01426135283 - Q.mean_phi2) * (40.046952646555 - Q.max_pair_mass)
    if Q.LHA < 0.216055863061 and Q.planar_flow < 0.083662731125:
        z += 452.77587890625 * (0.216055863061 - Q.LHA) * (0.083662731125 - Q.planar_flow)
    if Q.z_7 < 0.03243272066 and Q.pt_5 < 29.875:
        z += 2.40693736076355 * (0.03243272066 - Q.z_7) * (29.875 - Q.pt_5)
    if Q.sum_pt > 868.509375 and Q.pt_5 < 33.0265625:
        z += 0.00037965780938975513 * (Q.sum_pt - 868.509375) * (33.0265625 - Q.pt_5)
    if Q.e2 < 0.035560912266 and Q.lam2 < 7.3007261e-05:
        z += 335783.375 * (0.035560912266 - Q.e2) * (7.3007261e-05 - Q.lam2)
    if Q.z_7 < 0.071488645583 and Q.phi_0 > 0.021438598633:
        z += 102.18211364746094 * (0.071488645583 - Q.z_7) * (Q.phi_0 - 0.021438598633)
    return max(0.0, z)


def neuron_6(Q):
    z = 8.520337104797363
    if 0.008092360237 <= Q.centroid_offset < 0.018377780003:
        z += 23.63907241821289 * Q.centroid_offset - 0.1912958896767094
    if 0.018377780003 <= Q.centroid_offset < 0.049903668404:
        z += -86.85300064086914 * Q.centroid_offset + 1.8393031210785034
    if Q.centroid_offset >= 0.049903668404:
        z += -117.14528465270996 * Q.centroid_offset + 3.3509992176051986
    if Q.width < 0.013238675006:
        z += 653.9370727539062 * Q.width - 8.657260380563942
    if Q.mass_over_sum_pt < 0.008374148675:
        z += -5.602921962738037 * Q.mass_over_sum_pt + 0.8638069978919592
    if 0.008374148675 <= Q.mass_over_sum_pt < 0.154170806525:
        z += -84.67557668685913 * Q.mass_over_sum_pt + 1.5259731646786903
    if Q.mass_over_sum_pt >= 0.154170806525:
        z += -79.0726547241211 * Q.mass_over_sum_pt + 0.6621661667867311
    if Q.log_sum_pt < 6.327378592257:
        z += -2.308614730834961 * Q.log_sum_pt + 14.569416899323878
    if 6.327378592257 <= Q.log_sum_pt < 6.572937922293:
        z += -0.9178478717803955 * Q.log_sum_pt + 5.769508448521512
    if 6.572937922293 <= Q.log_sum_pt < 6.701242202626:
        z += 2.053311347961426 * Q.log_sum_pt - 13.759736660089986
    if Q.e2 < 0.050284641981:
        z += -70.4969253540039 * Q.e2 + 3.544912652187368
    if Q.lam2 < 0.000537286005:
        z += 1867.610595703125 * Q.lam2 - 1.0034410358610022
    if 0.000537286005 <= Q.lam2 < 0.003408388935:
        z += -50.32699203491211 * Q.lam2 + 0.027039988494104748
    if Q.lam2 >= 0.003408388935:
        z += -970.4497947692871 * Q.lam2 + 3.163176368175136
    if Q.LHA >= 0.312727471086:
        z += 5.743167400360107 * Q.LHA - 1.7960462171381735
    z += 16.022794723510742 * Q.max_dr
    if Q.C2 >= 0.010539266048:
        z += -23.862218856811523 * Q.C2 + 0.25149027302753907
    if 0.002270363079 <= Q.girth2_top5 < 0.011482925368:
        z += -34.15468978881836 * Q.girth2_top5 + 0.07754354667123152
    if Q.girth2_top5 >= 0.011482925368:
        z += 125.2938117980957 * Q.girth2_top5 - 1.7533916970907322
    if Q.girth2 < 0.003562611155:
        z += 808.9196166992188 * Q.girth2 - 9.897937999436635
    if 0.003562611155 <= Q.girth2 < 0.008678044751:
        z += 1371.5498046875 * Q.girth2 - 11.902370583303433
    if Q.lam1 < 0.007330079875:
        z += -528.3242034912109 * Q.lam1 + 4.1764486576170095
    if 0.007330079875 <= Q.lam1 < 0.008375572068:
        z += -290.5713195800781 * Q.lam1 + 2.4337010280368037
    if Q.girth >= 0.087236513197:
        z += 72.75994110107422 * Q.girth - 6.347323562076804
    if Q.D2 < 1.679198372364:
        z += -0.3378303050994873 * Q.D2 + 0.5672840984582926
    if Q.e2_sq < 0.008168570676:
        z += -8.289106369018555 * Q.e2_sq + 0.06771015121620981
    if Q.mass < 49.668099212646:
        z += 0.015246633440256119 * Q.mass - 0.757271302369487
    if Q.z_7 >= 0.06164517166:
        z += -18.326396942138672 * Q.z_7 + 1.1297338854074375
    if Q.centroid_offset > 0.008092360237 and Q.lam2 < 0.003408388935:
        z += 15196.5166015625 * (Q.centroid_offset - 0.008092360237) * (0.003408388935 - Q.lam2)
    if Q.log_sum_pt < 6.327378592257 and Q.z_7 < 0.071488645583:
        z += 747.25830078125 * (6.327378592257 - Q.log_sum_pt) * (0.071488645583 - Q.z_7)
    if Q.centroid_offset > 0.008092360237 and Q.planar_flow > 0.00804883781:
        z += 36.74869918823242 * (Q.centroid_offset - 0.008092360237) * (Q.planar_flow - 0.00804883781)
    if Q.centroid_offset > 0.008092360237 and Q.C2 < 0.094821243733:
        z += 183.41867065429688 * (Q.centroid_offset - 0.008092360237) * (0.094821243733 - Q.C2)
    if Q.log_sum_pt < 6.327378592257 and Q.pt_6 > 27.578125:
        z += 0.17665863037109375 * (6.327378592257 - Q.log_sum_pt) * (Q.pt_6 - 27.578125)
    if Q.log_sum_pt < 6.701242202626 and Q.z_7 < 0.049399692737:
        z += 624.6224975585938 * (6.701242202626 - Q.log_sum_pt) * (0.049399692737 - Q.z_7)
    if Q.centroid_offset > 0.049903668404 and Q.n_dr_0p05_0p1 > 6.0:
        z += -41.48131561279297 * (Q.centroid_offset - 0.049903668404) * (Q.n_dr_0p05_0p1 - 6.0)
    if Q.centroid_offset > 0.018377780003 and Q.mean_phi2 < 0.008921136335:
        z += 4724.59521484375 * (Q.centroid_offset - 0.018377780003) * (0.008921136335 - Q.mean_phi2)
    if Q.LHA > 0.312727471086 and Q.eccentricity > 0.872657364787:
        z += 92.30400848388672 * (Q.LHA - 0.312727471086) * (Q.eccentricity - 0.872657364787)
    if Q.e2 < 0.050284641981 and Q.n_dr_0p05_0p1 < 4.0:
        z += -2.1069865226745605 * (0.050284641981 - Q.e2) * (4.0 - Q.n_dr_0p05_0p1)
    if Q.width < 0.013238675006 and Q.mean_eta < -0.026655913051:
        z += 1022.485107421875 * (0.013238675006 - Q.width) * (-0.026655913051 - Q.mean_eta)
    if Q.width < 0.013238675006 and Q.mean_phi < -0.025945045147:
        z += 2236.513916015625 * (0.013238675006 - Q.width) * (-0.025945045147 - Q.mean_phi)
    if Q.width < 0.013238675006 and Q.mean_phi > 0.026127964072:
        z += 10182.6513671875 * (0.013238675006 - Q.width) * (Q.mean_phi - 0.026127964072)
    if Q.log_sum_pt < 6.701242202626 and Q.mean_phi > 0.009050007537:
        z += -63.961788177490234 * (6.701242202626 - Q.log_sum_pt) * (Q.mean_phi - 0.009050007537)
    if Q.mass_over_sum_pt > 0.008374148675 and Q.tau32 < 0.518696343899:
        z += -51.87193298339844 * (Q.mass_over_sum_pt - 0.008374148675) * (0.518696343899 - Q.tau32)
    if Q.centroid_offset > 0.008092360237 and Q.mean_eta2 < 0.001101289818:
        z += -17699.55859375 * (Q.centroid_offset - 0.008092360237) * (0.001101289818 - Q.mean_eta2)
    if Q.centroid_offset > 0.018377780003 and Q.pt_2 > 56.5:
        z += 0.589805006980896 * (Q.centroid_offset - 0.018377780003) * (Q.pt_2 - 56.5)
    if Q.lam1 < 0.007330079875 and Q.D2 < 1.232133567333:
        z += 195.7918243408203 * (0.007330079875 - Q.lam1) * (1.232133567333 - Q.D2)
    if Q.e2 < 0.050284641981 and Q.z_dr_0p1_0p2 > 0.15855820179:
        z += 713.58056640625 * (0.050284641981 - Q.e2) * (Q.z_dr_0p1_0p2 - 0.15855820179)
    if Q.log_sum_pt < 6.701242202626 and Q.pt_6 < 36.8125:
        z += 0.18179403245449066 * (6.701242202626 - Q.log_sum_pt) * (36.8125 - Q.pt_6)
    if Q.centroid_offset > 0.018377780003 and Q.pt_5 < 24.578125:
        z += 35.446632385253906 * (Q.centroid_offset - 0.018377780003) * (24.578125 - Q.pt_5)
    if Q.log_sum_pt < 6.701242202626 and Q.z_4 < 0.037477688199:
        z += 1089.137939453125 * (6.701242202626 - Q.log_sum_pt) * (0.037477688199 - Q.z_4)
    if Q.width < 0.013238675006 and Q.mean_eta > 0.02644207105:
        z += 9327.6884765625 * (0.013238675006 - Q.width) * (Q.mean_eta - 0.02644207105)
    if Q.lam2 < 0.000537286005 and Q.mean_eta > 0.02644207105:
        z += -141633.828125 * (0.000537286005 - Q.lam2) * (Q.mean_eta - 0.02644207105)
    if Q.lam1 < 0.007330079875 and Q.eta_7 > 0.008316040039:
        z += 88.1223373413086 * (0.007330079875 - Q.lam1) * (Q.eta_7 - 0.008316040039)
    if Q.log_sum_pt < 6.701242202626 and Q.mean_eta2 > 0.004247450386:
        z += 44.313758850097656 * (6.701242202626 - Q.log_sum_pt) * (Q.mean_eta2 - 0.004247450386)
    if Q.D2 < 1.679198372364 and Q.pt_4 < 90.625:
        z += -0.016174746677279472 * (1.679198372364 - Q.D2) * (90.625 - Q.pt_4)
    if Q.e2_sq < 0.008168570676 and Q.mass_top3 > 50.352200171245:
        z += 13.987663269042969 * (0.008168570676 - Q.e2_sq) * (Q.mass_top3 - 50.352200171245)
    if Q.girth2_top5 > 0.011482925368 and Q.mean_eta > 0.0127187056:
        z += -1872.80517578125 * (Q.girth2_top5 - 0.011482925368) * (Q.mean_eta - 0.0127187056)
    if Q.log_sum_pt < 6.701242202626 and Q.pt_7 < 45.75:
        z += 0.22920677065849304 * (6.701242202626 - Q.log_sum_pt) * (45.75 - Q.pt_7)
    if Q.C2 > 0.010539266048 and Q.pt_7 > 31.859375:
        z += 3.010641098022461 * (Q.C2 - 0.010539266048) * (Q.pt_7 - 31.859375)
    if Q.mass < 49.668099212646 and Q.z_dr_0p05_0p1 < 0.750909513235:
        z += 0.06458750367164612 * (49.668099212646 - Q.mass) * (0.750909513235 - Q.z_dr_0p05_0p1)
    if Q.girth2_top5 > 0.002270363079 and Q.z_dr_0p05_0p1 > 0.291944718361:
        z += -40.32427978515625 * (Q.girth2_top5 - 0.002270363079) * (Q.z_dr_0p05_0p1 - 0.291944718361)
    return max(0.0, z)


def neuron_7(Q):
    z = 9.933670043945312
    if Q.planar_flow < 0.195013533663:
        z += 6.684439182281494 * Q.planar_flow - 1.3035561054921283
    if Q.girth2_top2 < 0.001056655216:
        z += 680.809814453125 * Q.girth2_top2 - 0.7193812415458868
    if 0.0016538364 <= Q.girth2 < 0.004372139461:
        z += -541.34130859375 * Q.girth2 + 0.8952899609759766
    if 0.004372139461 <= Q.girth2 < 0.007520088344:
        z += -1040.2738037109375 * Q.girth2 + 3.076692411253022
    if 0.007520088344 <= Q.girth2 < 0.008678044751:
        z += -2445.5384521484375 * Q.girth2 + 13.644406714203122
    if 0.008678044751 <= Q.girth2 < 0.013238675334:
        z += -901.297119140625 * Q.girth2 + 0.24341132001743304
    if Q.girth2 >= 0.013238675334:
        z += -170.97393798828125 * Q.girth2 - 9.425100164152513
    if 0.072690732432 <= Q.mass_over_sum_pt < 0.084751611895:
        z += 113.50086212158203 * Q.mass_over_sum_pt - 8.250460799281242
    if 0.084751611895 <= Q.mass_over_sum_pt < 0.090413827016:
        z += 302.4767532348633 * Q.mass_over_sum_pt - 24.266472180425833
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += 6.706031799316406 * Q.mass_over_sum_pt + 2.4752906638452252
    if Q.mass_over_sum_pt >= 0.107985668755:
        z += 8.502570867538452 * Q.mass_over_sum_pt + 2.2812901911187815
    if Q.e2 < 0.024547699839:
        z += -107.29477310180664 * Q.e2 + 2.300500134342874
    if 0.024547699839 <= Q.e2 < 0.038466955721:
        z += -50.62017822265625 * Q.e2 + 0.9092691907525641
    if 0.038466955721 <= Q.e2 < 0.050284641981:
        z += 87.82894897460938 * Q.e2 - 4.41644725475575
    if Q.girth < 0.04081947431:
        z += 107.64669418334961 * Q.girth - 8.11301050128148
    if 0.04081947431 <= Q.girth < 0.087236513197:
        z += 80.11991119384766 * Q.girth - 6.989381690204559
    if Q.pt_7 < 48.71875:
        z += -0.016122810542583466 * Q.pt_7 + 0.7854831761214882
    if Q.width < 0.000561123155:
        z += 2090.8258056640625 * Q.width - 6.375239091430742
    if 0.000561123155 <= Q.width < 0.005590288644:
        z += 1034.3720703125 * Q.width - 5.782438438338738
    if Q.centroid_offset < 0.02076709205:
        z += 47.04436695575714 * Q.centroid_offset - 1.006606967828286
    if 0.02076709205 <= Q.centroid_offset < 0.031170772021:
        z += 1.7437001466751099 * Q.centroid_offset - 0.06584385027769969
    if 0.031170772021 <= Q.centroid_offset < 0.037760993714:
        z += 24.69274342060089 * Q.centroid_offset - 0.7811832462693037
    if Q.centroid_offset >= 0.037760993714:
        z += 22.94904327392578 * Q.centroid_offset - 0.715339395991604
    if Q.e2_sq < 0.001101266364:
        z += -1482.53564453125 * Q.e2_sq + 1.632666638753326
    if Q.mass < 29.644699859619:
        z += -0.03890545293688774 * Q.mass + 1.1533404752165697
    if Q.mass >= 80.4:
        z += -0.12471292167901993 * Q.mass + 10.026918902993202
    if Q.lam1 < 0.008375572068:
        z += 452.7107849121094 * Q.lam1 - 3.791711804992219
    if Q.z_dr_0p05_0p1 >= 0.674770402908:
        z += -0.6932258009910583 * Q.z_dr_0p05_0p1 + 0.4677682530409575
    if Q.LHA < 0.293190627853:
        z += -12.75031852722168 * Q.LHA + 3.7382738943218623
    if Q.girth2_top3 < 0.005884990035:
        z += -73.40943145751953 * Q.girth2_top3 + 0.43201377260251794
    if Q.max_dr < 0.197968879342:
        z += 2.4357402324676514 * Q.max_dr - 0.4822007641898435
    if Q.m012 < 4.909120770781:
        z += -0.013843449763953686 * Q.m012 + 0.06795916677548837
    if Q.planar_flow < 0.195013533663 and Q.width > 0.00752008842:
        z += -2752.2080078125 * (0.195013533663 - Q.planar_flow) * (Q.width - 0.00752008842)
    if Q.girth2_top2 < 0.001056655216 and Q.centroid_offset > 0.006789738266:
        z += 55025.83984375 * (0.001056655216 - Q.girth2_top2) * (Q.centroid_offset - 0.006789738266)
    if Q.planar_flow < 0.195013533663 and Q.pt_6 < 35.28125:
        z += -0.25138339400291443 * (0.195013533663 - Q.planar_flow) * (35.28125 - Q.pt_6)
    if Q.planar_flow < 0.195013533663 and Q.n_dr_0p1_0p2 < 3.0:
        z += 0.31839704513549805 * (0.195013533663 - Q.planar_flow) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.planar_flow < 0.195013533663 and Q.mass_top3 > 23.663861485439:
        z += 0.16122286021709442 * (0.195013533663 - Q.planar_flow) * (Q.mass_top3 - 23.663861485439)
    if Q.planar_flow < 0.195013533663 and Q.sum_pt > 615.875:
        z += 0.0359356515109539 * (0.195013533663 - Q.planar_flow) * (Q.sum_pt - 615.875)
    if Q.e2 < 0.024547699839 and Q.tau21 < 0.446608647704:
        z += 172.76025390625 * (0.024547699839 - Q.e2) * (0.446608647704 - Q.tau21)
    if Q.width < 0.005590288644 and Q.mean_phi < -0.00469376049:
        z += 5189.97412109375 * (0.005590288644 - Q.width) * (-0.00469376049 - Q.mean_phi)
    if Q.girth2 > 0.004372139461 and Q.eccentricity > 0.945820652852:
        z += 8038.806640625 * (Q.girth2 - 0.004372139461) * (Q.eccentricity - 0.945820652852)
    if Q.lam1 < 0.008375572068 and Q.D2 < 1.122624260187:
        z += -567.9267578125 * (0.008375572068 - Q.lam1) * (1.122624260187 - Q.D2)
    if Q.e2 < 0.050284641981 and Q.D2 < 1.122624260187:
        z += 135.01393127441406 * (0.050284641981 - Q.e2) * (1.122624260187 - Q.D2)
    if Q.centroid_offset < 0.02076709205 and Q.C2 > 0.023843882605:
        z += 1639.447265625 * (0.02076709205 - Q.centroid_offset) * (Q.C2 - 0.023843882605)
    if Q.mass > 80.4 and Q.eccentricity > 0.927072033478:
        z += -2.401623249053955 * (Q.mass - 80.4) * (Q.eccentricity - 0.927072033478)
    if Q.pt_7 < 48.71875 and Q.planar_flow < 0.694781820497:
        z += -0.07831697911024094 * (48.71875 - Q.pt_7) * (0.694781820497 - Q.planar_flow)
    if Q.e2_sq < 0.001101266364 and Q.phi_0 > 0.040283203125:
        z += -100378.046875 * (0.001101266364 - Q.e2_sq) * (Q.phi_0 - 0.040283203125)
    if Q.centroid_offset > 0.031170772021 and Q.pt_0 > 376.5:
        z += -7.9169697761535645 * (Q.centroid_offset - 0.031170772021) * (Q.pt_0 - 376.5)
    if Q.e2_sq < 0.001101266364 and Q.phi_1 < -0.009460449219:
        z += -34571.16015625 * (0.001101266364 - Q.e2_sq) * (-0.009460449219 - Q.phi_1)
    if Q.e2 < 0.024547699839 and Q.phi_0 > 0.054992675781:
        z += -14605.521484375 * (0.024547699839 - Q.e2) * (Q.phi_0 - 0.054992675781)
    if Q.girth2_top3 < 0.005884990035 and Q.n_dr_0p2_0p4 > 1.0:
        z += 95.28987884521484 * (0.005884990035 - Q.girth2_top3) * (Q.n_dr_0p2_0p4 - 1.0)
    if Q.centroid_offset > 0.031170772021 and Q.pt_2 > 56.5:
        z += -1.2129145860671997 * (Q.centroid_offset - 0.031170772021) * (Q.pt_2 - 56.5)
    if Q.centroid_offset > 0.031170772021 and Q.n_pt_above_50 > 6.0:
        z += -16.81757354736328 * (Q.centroid_offset - 0.031170772021) * (Q.n_pt_above_50 - 6.0)
    if Q.girth2 > 0.013238675334 and Q.log_sum_pt > 6.19222188581:
        z += 611.7533569335938 * (Q.girth2 - 0.013238675334) * (Q.log_sum_pt - 6.19222188581)
    if Q.z_dr_0p05_0p1 > 0.674770402908 and Q.pt_2 > 84.625:
        z += 0.012523658573627472 * (Q.z_dr_0p05_0p1 - 0.674770402908) * (Q.pt_2 - 84.625)
    if Q.e2_sq < 0.001101266364 and Q.eta_2 < -0.045445251465:
        z += -141433.34375 * (0.001101266364 - Q.e2_sq) * (-0.045445251465 - Q.eta_2)
    if Q.width < 0.005590288644 and Q.mean_eta < -0.009391680919:
        z += -2557.477294921875 * (0.005590288644 - Q.width) * (-0.009391680919 - Q.mean_eta)
    if Q.lam1 < 0.008375572068 and Q.n_pt_above_50 < 4.0:
        z += -24.50481414794922 * (0.008375572068 - Q.lam1) * (4.0 - Q.n_pt_above_50)
    if Q.e2 < 0.024547699839 and Q.z_dr_0p05_0p1 > 0.750909513235:
        z += -305.2910461425781 * (0.024547699839 - Q.e2) * (Q.z_dr_0p05_0p1 - 0.750909513235)
    if Q.max_dr < 0.197968879342 and Q.z_dr_0p05_0p1 > 0.048758227378:
        z += -4.0867743492126465 * (0.197968879342 - Q.max_dr) * (Q.z_dr_0p05_0p1 - 0.048758227378)
    if Q.width < 0.005590288644 and Q.mean_eta > 0.0127187056:
        z += -3443.444580078125 * (0.005590288644 - Q.width) * (Q.mean_eta - 0.0127187056)
    return max(0.0, z)


def neuron_8(Q):
    z = -0.4082571268081665
    if Q.girth2 < 0.000964142894:
        z += -1232.904146194458 * Q.girth2 + 1.3132565611816283
    if 0.000964142894 <= Q.girth2 < 0.006679471442:
        z += -21.794160842895508 * Q.girth2 + 0.1455734749524752
    if Q.e2 < 0.016554418951:
        z += -165.6617774963379 * Q.e2 + 3.0647318761079876
    if 0.016554418951 <= Q.e2 < 0.024547699839:
        z += -40.321041107177734 * Q.e2 + 0.9897888142949792
    if Q.width < 0.005019718802:
        z += -1314.6231689453125 * Q.width + 6.599038638699607
    if Q.LHA < 0.196739721581:
        z += 16.161863327026367 * Q.LHA - 3.179680491189342
    if Q.log_sum_pt >= 6.701242202626:
        z += -8.76523494720459 * Q.log_sum_pt + 58.737962344139675
    if Q.mass < 8.379955863953:
        z += -0.04999935068190098 * Q.mass - 1.4172263179049673
    if 8.379955863953 <= Q.mass < 15.454033088684:
        z += 0.12062824331223965 * Q.mass - 2.847078024748358
    if 15.454033088684 <= Q.mass < 21.784077072144:
        z += 0.14342443272471428 * Q.mass - 3.1993710902246493
    if 21.784077072144 <= Q.mass < 29.644699859619:
        z += 0.009541507810354233 * Q.mass - 0.2828551352461617
    if Q.girth < 0.061086014472:
        z += 41.74773406982422 * Q.girth - 2.5502026875624897
    if Q.sum_pt_top5 >= 658.125:
        z += -0.0017125409794971347 * Q.sum_pt_top5 + 1.1270660321315518
    if Q.centroid_offset < 0.003343241496:
        z += -271.7344970703125 * Q.centroid_offset + 0.9084740465001592
    if Q.max_dr < 0.177304983139:
        z += -6.930924892425537 * Q.max_dr + 1.2288875211891852
    if Q.z_dr_0_0p05 >= 0.847731333971:
        z += -3.896515130996704 * Q.z_dr_0_0p05 + 3.303197969838022
    if Q.pt_7 >= 34.53125:
        z += -0.06671492010354996 * Q.pt_7 + 2.3037495848257095
    if Q.girth2_top5 < 0.000222950415:
        z += 9518.310546875 * Q.girth2_top5 - 2.122111286524658
    if Q.girth2 < 0.006679471442 and Q.tau21 < 0.501026660204:
        z += -508.2769775390625 * (0.006679471442 - Q.girth2) * (0.501026660204 - Q.tau21)
    if Q.width < 0.005019718802 and Q.pt_7 < 48.71875:
        z += -0.4463695287704468 * (0.005019718802 - Q.width) * (48.71875 - Q.pt_7)
    if Q.girth2 < 0.006679471442 and Q.centroid_offset < 0.023554160423:
        z += 25668.298828125 * (0.006679471442 - Q.girth2) * (0.023554160423 - Q.centroid_offset)
    if Q.girth2 < 0.006679471442 and Q.planar_flow < 0.40079469091:
        z += 608.8926391601562 * (0.006679471442 - Q.girth2) * (0.40079469091 - Q.planar_flow)
    if Q.width < 0.005019718802 and Q.sum_pt_top2 < 248.125:
        z += 3.1579291820526123 * (0.005019718802 - Q.width) * (248.125 - Q.sum_pt_top2)
    if Q.girth2 < 0.006679471442 and Q.n_dr_0p05_0p1 > 0.0:
        z += -46.83988952636719 * (0.006679471442 - Q.girth2) * (Q.n_dr_0p05_0p1 - 0.0)
    if Q.LHA < 0.196739721581 and Q.mean_phi > -0.000855675264:
        z += -1212.5648193359375 * (0.196739721581 - Q.LHA) * (Q.mean_phi - -0.000855675264)
    if Q.girth2 < 0.006679471442 and Q.n_dr_0p1_0p2 > 2.0:
        z += -140.8577117919922 * (0.006679471442 - Q.girth2) * (Q.n_dr_0p1_0p2 - 2.0)
    if Q.width < 0.005019718802 and Q.z_dr_0p2_0p4 < 0.1009733513:
        z += 6371.45263671875 * (0.005019718802 - Q.width) * (0.1009733513 - Q.z_dr_0p2_0p4)
    if Q.girth < 0.061086014472 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += -161.47982788085938 * (0.061086014472 - Q.girth) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.girth2 < 0.006679471442 and Q.phi_0 > -0.040130615234:
        z += -151.5857696533203 * (0.006679471442 - Q.girth2) * (Q.phi_0 - -0.040130615234)
    if Q.log_sum_pt > 6.701242202626 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += -48.00453567504883 * (Q.log_sum_pt - 6.701242202626) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.max_dr < 0.177304983139 and Q.pt1_over_pt0 < 0.465420272571:
        z += 4.030313968658447 * (0.177304983139 - Q.max_dr) * (0.465420272571 - Q.pt1_over_pt0)
    if Q.girth2 < 0.006679471442 and Q.girth2_top3 > 0.002915531053:
        z += -783.3621215820312 * (0.006679471442 - Q.girth2) * (Q.girth2_top3 - 0.002915531053)
    if Q.width < 0.005019718802 and Q.centroid_offset > 0.006789738266:
        z += -46527.6875 * (0.005019718802 - Q.width) * (Q.centroid_offset - 0.006789738266)
    if Q.girth < 0.061086014472 and Q.lam1 > 0.00027588256:
        z += -17579.71875 * (0.061086014472 - Q.girth) * (Q.lam1 - 0.00027588256)
    if Q.width < 0.005019718802 and Q.mass_over_sum_pt_sq > 0.00012320649:
        z += -89310.171875 * (0.005019718802 - Q.width) * (Q.mass_over_sum_pt_sq - 0.00012320649)
    if Q.max_dr < 0.177304983139 and Q.lam2 < 0.000194798295:
        z += 43850.5234375 * (0.177304983139 - Q.max_dr) * (0.000194798295 - Q.lam2)
    if Q.mass < 15.454033088684 and Q.lam2 < 0.000306123359:
        z += -294.9747314453125 * (15.454033088684 - Q.mass) * (0.000306123359 - Q.lam2)
    if Q.log_sum_pt > 6.701242202626 and Q.pt_7 < 48.71875:
        z += 0.2258135974407196 * (Q.log_sum_pt - 6.701242202626) * (48.71875 - Q.pt_7)
    if Q.log_sum_pt > 6.701242202626 and Q.girth2 < 0.018827652745:
        z += -210.232177734375 * (Q.log_sum_pt - 6.701242202626) * (0.018827652745 - Q.girth2)
    if Q.log_sum_pt > 6.701242202626 and Q.mass_over_sum_pt_sq < 0.00023679558:
        z += 28831.3046875 * (Q.log_sum_pt - 6.701242202626) * (0.00023679558 - Q.mass_over_sum_pt_sq)
    if Q.log_sum_pt > 6.701242202626 and Q.centroid_offset < 0.023554160423:
        z += 355.4153747558594 * (Q.log_sum_pt - 6.701242202626) * (0.023554160423 - Q.centroid_offset)
    if Q.mass < 21.784077072144 and Q.centroid_offset < 0.026856224803:
        z += -2.8172402381896973 * (21.784077072144 - Q.mass) * (0.026856224803 - Q.centroid_offset)
    if Q.LHA < 0.196739721581 and Q.width < 0.000561123155:
        z += 31364.30859375 * (0.196739721581 - Q.LHA) * (0.000561123155 - Q.width)
    if Q.girth2 < 0.006679471442 and Q.log_sum_pt > 6.670067010936:
        z += 160.54359436035156 * (0.006679471442 - Q.girth2) * (Q.log_sum_pt - 6.670067010936)
    if Q.LHA < 0.196739721581 and Q.z_6 > 0.02160287394:
        z += -155.590576171875 * (0.196739721581 - Q.LHA) * (Q.z_6 - 0.02160287394)
    if Q.mass < 29.644699859619 and Q.centroid_offset < 0.023554160423:
        z += -8.903515815734863 * (29.644699859619 - Q.mass) * (0.023554160423 - Q.centroid_offset)
    if Q.e2 < 0.024547699839 and Q.sum_pt > 788.4484375:
        z += 0.2833854556083679 * (0.024547699839 - Q.e2) * (Q.sum_pt - 788.4484375)
    if Q.girth < 0.061086014472 and Q.width < 0.005019718802:
        z += -17948.080078125 * (0.061086014472 - Q.girth) * (0.005019718802 - Q.width)
    if Q.girth < 0.061086014472 and Q.lam2 < 0.000194798295:
        z += 171810.984375 * (0.061086014472 - Q.girth) * (0.000194798295 - Q.lam2)
    if Q.girth < 0.061086014472 and Q.centroid_offset > 0.006789738266:
        z += -1871.193603515625 * (0.061086014472 - Q.girth) * (Q.centroid_offset - 0.006789738266)
    if Q.e2 < 0.024547699839 and Q.centroid_offset < 0.031170772021:
        z += 4830.20849609375 * (0.024547699839 - Q.e2) * (0.031170772021 - Q.centroid_offset)
    if Q.girth2 < 0.006679471442 and Q.centroid_offset > 0.018377780003:
        z += -19301.080078125 * (0.006679471442 - Q.girth2) * (Q.centroid_offset - 0.018377780003)
    if Q.LHA < 0.196739721581 and Q.lam2 < 0.000306123359:
        z += -87463.0703125 * (0.196739721581 - Q.LHA) * (0.000306123359 - Q.lam2)
    if Q.mass < 15.454033088684 and Q.z_7 < 0.058613700176:
        z += -1.6267682313919067 * (15.454033088684 - Q.mass) * (0.058613700176 - Q.z_7)
    if Q.LHA < 0.196739721581 and Q.z_7 > 0.016858545121:
        z += 216.89279174804688 * (0.196739721581 - Q.LHA) * (Q.z_7 - 0.016858545121)
    if Q.pt_7 > 34.53125 and Q.width < 0.013238675006:
        z += 0.5216325521469116 * (Q.pt_7 - 34.53125) * (0.013238675006 - Q.width)
    if Q.mass < 21.784077072144 and Q.centroid_offset > 0.016278845848:
        z += -7.596925258636475 * (21.784077072144 - Q.mass) * (Q.centroid_offset - 0.016278845848)
    if Q.max_dr < 0.177304983139 and Q.mean_eta > -0.012844925793:
        z += 26.70271873474121 * (0.177304983139 - Q.max_dr) * (Q.mean_eta - -0.012844925793)
    if Q.z_dr_0_0p05 > 0.847731333971 and Q.lam2 < 0.000537286005:
        z += -19754.86328125 * (Q.z_dr_0_0p05 - 0.847731333971) * (0.000537286005 - Q.lam2)
    if Q.mass < 21.784077072144 and Q.centroid_offset > 0.031170772021:
        z += -3.956652879714966 * (21.784077072144 - Q.mass) * (Q.centroid_offset - 0.031170772021)
    return max(0.0, z)


def neuron_9(Q):
    z = -1.5667284727096558
    if Q.girth < 0.054649224505:
        z += 87.3942642211914 * Q.girth - 4.776028765873178
    if Q.e2 < 0.020459658932:
        z += -76.81711196899414 * Q.e2 + 1.1068929254003559
    if 0.020459658932 <= Q.e2 < 0.032346998155:
        z += 39.09697341918945 * Q.e2 - 1.2646697270566054
    if Q.mass < 29.644699859619:
        z += 0.12695053219795227 * Q.mass - 5.255513792947755
    if 29.644699859619 <= Q.mass < 41.377904891968:
        z += 0.03722146898508072 * Q.mass - 2.5955226453173976
    if 41.377904891968 <= Q.mass < 53.332374954224:
        z += 0.0882829800248146 * Q.mass - 4.70834099275968
    if Q.lam2 >= 0.001130644719:
        z += 645.8186645507812 * Q.lam2 - 0.7301914625059733
    if Q.width < 0.000172198326:
        z += -5550.011962890625 * Q.width + 10.577794885729482
    if 0.000172198326 <= Q.width < 0.006096650059:
        z += -1624.132080078125 * Q.width + 9.901764941832093
    if Q.girth2 < 4.8108519e-05:
        z += -11177.520080566406 * Q.girth2 + 11.75132421068717
    if 4.8108519e-05 <= Q.girth2 < 0.000964142894:
        z += -5515.893615722656 * Q.girth2 + 11.478951746332331
    if 0.000964142894 <= Q.girth2 < 0.004372139461:
        z += -1366.7578735351562 * Q.girth2 + 7.478592004260836
    if 0.004372139461 <= Q.girth2 < 0.007520088344:
        z += -477.43341064453125 * Q.girth2 + 3.590341426424105
    if Q.girth2 >= 0.018827652745:
        z += 200.75437927246094 * Q.girth2 - 3.7797337399799202
    if Q.lam1 < 0.001503553356:
        z += 781.7605628967285 * Q.lam1 - 1.0679888767361394
    if 0.001503553356 <= Q.lam1 < 0.005954149834:
        z += -24.138301849365234 * Q.lam1 + 0.1437230659494399
    if Q.n_dr_0p2_0p4 >= 1.0:
        z += 1.0744822025299072 * Q.n_dr_0p2_0p4 - 1.0744822025299072
    if Q.max_dr < 0.15984864831:
        z += -7.874617576599121 * Q.max_dr + 1.7449107790053926
    if 0.15984864831 <= Q.max_dr < 0.221586732566:
        z += -11.429936170578003 * Q.max_dr + 2.3132236505643267
    if Q.max_dr >= 0.221586732566:
        z += -3.555318593978882 * Q.max_dr + 0.568312871558934
    if Q.C2 >= 0.051192347892:
        z += 17.951080322265625 * Q.C2 - 0.9189579488946573
    if Q.centroid_offset < 0.009480684835:
        z += -200.75723457336426 * Q.centroid_offset + 3.5286831002109746
    if 0.009480684835 <= Q.centroid_offset < 0.018377780003:
        z += -182.6851348876953 * Q.centroid_offset + 3.3573472187844446
    if Q.log_sum_pt >= 6.377722943814:
        z += -4.52570104598999 * Q.log_sum_pt + 28.86366739785338
    if Q.z_dr_0p2_0p4 >= 0.1009733513:
        z += 0.2163352519273758 * Q.z_dr_0p2_0p4 - 0.02184409539143692
    if Q.mass_over_sum_pt < 0.076373631775:
        z += 39.17424392700195 * Q.mass_over_sum_pt - 2.9918792807448775
    if Q.pt_5 < 35.5:
        z += -0.043219055980443954 * Q.pt_5 + 1.5342764873057604
    if Q.mass < 53.332374954224 and Q.centroid_offset < 0.026856224803:
        z += 3.8891146183013916 * (53.332374954224 - Q.mass) * (0.026856224803 - Q.centroid_offset)
    if Q.mass < 53.332374954224 and Q.lam1 < 0.000872228216:
        z += -67.65485382080078 * (53.332374954224 - Q.mass) * (0.000872228216 - Q.lam1)
    if Q.mass < 53.332374954224 and Q.n_dr_0p05_0p1 > 3.0:
        z += -0.0023382119834423065 * (53.332374954224 - Q.mass) * (Q.n_dr_0p05_0p1 - 3.0)
    if Q.girth2 > 0.018827652745 and Q.planar_flow < 0.40079469091:
        z += -442.0376281738281 * (Q.girth2 - 0.018827652745) * (0.40079469091 - Q.planar_flow)
    if Q.mass < 53.332374954224 and Q.pt_3 < 60.59375:
        z += 2.600894913484808e-05 * (53.332374954224 - Q.mass) * (60.59375 - Q.pt_3)
    if Q.e2 < 0.032346998155 and Q.dr01 < 0.055953954317:
        z += 277.0280456542969 * (0.032346998155 - Q.e2) * (0.055953954317 - Q.dr01)
    if Q.mass < 53.332374954224 and Q.log_sum_pt < 6.842716632804:
        z += 0.18706673383712769 * (53.332374954224 - Q.mass) * (6.842716632804 - Q.log_sum_pt)
    if Q.girth < 0.054649224505 and Q.mean_phi < 0.002834883542:
        z += -664.4537963867188 * (0.054649224505 - Q.girth) * (0.002834883542 - Q.mean_phi)
    if Q.max_dr < 0.221586732566 and Q.z_top5 < 0.90890302062:
        z += 11.370370864868164 * (0.221586732566 - Q.max_dr) * (0.90890302062 - Q.z_top5)
    if Q.width < 0.006096650059 and Q.C2 > 0.030867108516:
        z += -9143.447265625 * (0.006096650059 - Q.width) * (Q.C2 - 0.030867108516)
    if Q.width < 0.006096650059 and Q.centroid_offset > 0.003343241496:
        z += -48254.84765625 * (0.006096650059 - Q.width) * (Q.centroid_offset - 0.003343241496)
    if Q.centroid_offset < 0.018377780003 and Q.z_5 > 0.036727111752:
        z += -1765.662353515625 * (0.018377780003 - Q.centroid_offset) * (Q.z_5 - 0.036727111752)
    if Q.mass < 29.644699859619 and Q.mean_phi2 < 0.002127561159:
        z += -17.305627822875977 * (29.644699859619 - Q.mass) * (0.002127561159 - Q.mean_phi2)
    if Q.log_sum_pt > 6.377722943814 and Q.dr_5 < 0.021648628542:
        z += 30.4480037689209 * (Q.log_sum_pt - 6.377722943814) * (0.021648628542 - Q.dr_5)
    if Q.girth < 0.054649224505 and Q.dr_5 < 0.021648628542:
        z += -404.7561340332031 * (0.054649224505 - Q.girth) * (0.021648628542 - Q.dr_5)
    if Q.mass < 53.332374954224 and Q.planar_flow < 0.322073846732:
        z += 0.3443877696990967 * (53.332374954224 - Q.mass) * (0.322073846732 - Q.planar_flow)
    if Q.centroid_offset < 0.018377780003 and Q.pt_4 > 47.34375:
        z += 3.2078452110290527 * (0.018377780003 - Q.centroid_offset) * (Q.pt_4 - 47.34375)
    if Q.centroid_offset < 0.018377780003 and Q.z_4 > 0.047491459878:
        z += -2735.710693359375 * (0.018377780003 - Q.centroid_offset) * (Q.z_4 - 0.047491459878)
    if Q.girth < 0.054649224505 and Q.mean_phi2 > 0.000539434783:
        z += 1935.131591796875 * (0.054649224505 - Q.girth) * (Q.mean_phi2 - 0.000539434783)
    if Q.mass < 53.332374954224 and Q.phi_7 > 0.121704101562:
        z += -0.029038671404123306 * (53.332374954224 - Q.mass) * (Q.phi_7 - 0.121704101562)
    if Q.e2 < 0.020459658932 and Q.eccentricity > 0.903125533696:
        z += -924.7781372070312 * (0.020459658932 - Q.e2) * (Q.eccentricity - 0.903125533696)
    if Q.C2 > 0.051192347892 and Q.eccentricity < 0.620723099573:
        z += 119.81339263916016 * (Q.C2 - 0.051192347892) * (0.620723099573 - Q.eccentricity)
    if Q.girth2 < 0.004372139461 and Q.mass_top2 > 6.77991534008:
        z += -15.951620101928711 * (0.004372139461 - Q.girth2) * (Q.mass_top2 - 6.77991534008)
    if Q.mass < 41.377904891968 and Q.planar_flow < 0.322073846732:
        z += -0.3329674005508423 * (41.377904891968 - Q.mass) * (0.322073846732 - Q.planar_flow)
    if Q.e2 < 0.032346998155 and Q.tau21 < 0.446608647704:
        z += -238.01609802246094 * (0.032346998155 - Q.e2) * (0.446608647704 - Q.tau21)
    if Q.girth2 < 0.004372139461 and Q.n_dr_0p05_0p1 > 3.0:
        z += 115.58281707763672 * (0.004372139461 - Q.girth2) * (Q.n_dr_0p05_0p1 - 3.0)
    if Q.girth2 > 0.018827652745 and Q.pt_7 < 29.0421875:
        z += 40.91547393798828 * (Q.girth2 - 0.018827652745) * (29.0421875 - Q.pt_7)
    if Q.girth2 < 0.000964142894 and Q.mean_eta < 0.006823012256:
        z += -17613.65625 * (0.000964142894 - Q.girth2) * (0.006823012256 - Q.mean_eta)
    if Q.lam2 > 0.001130644719 and Q.mass_top2 > 16.308019673264:
        z += 17.738971710205078 * (Q.lam2 - 0.001130644719) * (Q.mass_top2 - 16.308019673264)
    if Q.centroid_offset < 0.009480684835 and Q.mean_phi2 < 0.002127561159:
        z += -2507.630859375 * (0.009480684835 - Q.centroid_offset) * (0.002127561159 - Q.mean_phi2)
    if Q.e2 < 0.020459658932 and Q.pt_7 < 53.4375:
        z += 0.6780043840408325 * (0.020459658932 - Q.e2) * (53.4375 - Q.pt_7)
    if Q.girth2 > 0.018827652745 and Q.mean_eta < 0.02644207105:
        z += -1495.8668212890625 * (Q.girth2 - 0.018827652745) * (0.02644207105 - Q.mean_eta)
    if Q.pt_5 < 35.5 and Q.min_pair_mass > 0.173071536962:
        z += -0.02540586329996586 * (35.5 - Q.pt_5) * (Q.min_pair_mass - 0.173071536962)
    if Q.C2 > 0.051192347892 and Q.n_dr_0p05_0p1 > 1.0:
        z += -5.633437156677246 * (Q.C2 - 0.051192347892) * (Q.n_dr_0p05_0p1 - 1.0)
    return max(0.0, z)


def neuron_10(Q):
    z = -1.7872759103775024
    z += 65.00287628173828 * Q.e2
    if Q.lam2 >= 0.000194798295:
        z += 1579.9072265625 * Q.lam2 - 0.30776323399255373
    if Q.LHA >= 0.303313749495:
        z += -11.80795669555664 * Q.LHA + 3.581515619203875
    if Q.log_sum_pt < 6.267538488641:
        z += 2.927077054977417 * Q.log_sum_pt - 18.345568101288908
    if Q.log_sum_pt >= 6.701242202626:
        z += -17.442975997924805 * Q.log_sum_pt + 116.88960689668608
    if 0.00231612516 <= Q.centroid_offset < 0.037760993714:
        z += -1.2782397270202637 * Q.centroid_offset + 0.0029605631922631644
    if Q.centroid_offset >= 0.037760993714:
        z += 4.4081621170043945 * Q.centroid_offset - 0.21176362109522995
    if Q.eccentricity >= 0.903125533696:
        z += 0.35956934094429016 * Q.eccentricity - 0.32473625294103103
    if Q.C2 >= 0.051192347892:
        z += 24.261693954467773 * Q.C2 - 1.2420130773663476
    if Q.n_dr_0p2_0p4 >= 2.0:
        z += 0.5772825479507446 * Q.n_dr_0p2_0p4 - 1.1545650959014893
    if Q.lam1 < 0.004183811014:
        z += 638.3098449707031 * Q.lam1 - 3.077242891632012
    if 0.004183811014 <= Q.lam1 < 0.006506575659:
        z += 175.08236694335938 * Q.lam1 - 1.1391866670737683
    if Q.mass_over_sum_pt < 0.090413827016:
        z += -34.068603515625 * Q.mass_over_sum_pt + 3.080272824938408
    if Q.n_dr_0p05_0p1 < 3.0:
        z += -0.24720090627670288 * Q.n_dr_0p05_0p1 + 0.7416027188301086
    if Q.tau32 < 0.269169217348:
        z += -12.183488845825195 * Q.tau32 + 3.2794201571988553
    if Q.tau21 < 0.391541349888:
        z += -1.6013072729110718 * Q.tau21 + 0.626978011221073
    if Q.girth2_top2 < 0.002412890926:
        z += -503.2735900878906 * Q.girth2_top2 + 1.214344278818515
    if Q.phi_6 >= 0.05560760498:
        z += -2.19419527053833 * Q.phi_6 + 0.1220139438530797
    if Q.mass_over_sum_pt_sq < 0.003904593248:
        z += 1.325652837753296 * Q.mass_over_sum_pt_sq - 0.005176135119483559
    if 15.454033088684 <= Q.mass < 53.332374954224:
        z += 0.0399487242102623 * Q.mass - 0.6173689057961051
    if Q.mass >= 53.332374954224:
        z += 0.033764644991606474 * Q.mass - 0.2875572741601281
    if Q.max_dr >= 0.121680960059:
        z += -3.7006118297576904 * Q.max_dr + 0.45029400025060845
    if Q.girth2 < 0.0016538364:
        z += 1316.2269439697266 * Q.girth2 - 1.1248762411674913
    if 0.0016538364 <= Q.girth2 < 0.006679471442:
        z += -209.31639099121094 * Q.girth2 + 1.3981228559682997
    if Q.pt_7 >= 45.75:
        z += 0.014029373414814472 * Q.pt_7 - 0.6418438337277621
    if Q.girth2_top5 < 0.002270363079:
        z += 84.53311157226562 * Q.girth2_top5 - 0.19192085546665952
    if Q.z_7 >= 0.06164517166:
        z += -1.3959424495697021 * Q.z_7 + 0.08605311193120518
    if Q.sum_pt >= 813.415625:
        z += 0.01127642672508955 * Q.sum_pt - 9.17242169235542
    if Q.z_dr_0p2_0p4 >= 0.05643851608:
        z += 0.15049245953559875 * Q.z_dr_0p2_0p4 - 0.00849357109741864
    if Q.lam2 > 0.000194798295 and Q.planar_flow > 0.012569162668:
        z += -526.9957275390625 * (Q.lam2 - 0.000194798295) * (Q.planar_flow - 0.012569162668)
    if Q.centroid_offset > 0.00231612516 and Q.pt_7 < 34.53125:
        z += 0.8738239407539368 * (Q.centroid_offset - 0.00231612516) * (34.53125 - Q.pt_7)
    if Q.lam2 > 0.000194798295 and Q.n_pt_above_50 < 8.0:
        z += -52.72075271606445 * (Q.lam2 - 0.000194798295) * (8.0 - Q.n_pt_above_50)
    if Q.lam2 > 0.000194798295 and Q.z_top2_slots > 0.476619814198:
        z += 850.7223510742188 * (Q.lam2 - 0.000194798295) * (Q.z_top2_slots - 0.476619814198)
    if Q.lam2 > 0.000194798295 and Q.pt_6 < 38.25:
        z += -12.343419075012207 * (Q.lam2 - 0.000194798295) * (38.25 - Q.pt_6)
    if Q.eccentricity > 0.903125533696 and Q.z_top2_slots > 0.55004856109:
        z += -22.065582275390625 * (Q.eccentricity - 0.903125533696) * (Q.z_top2_slots - 0.55004856109)
    if Q.mass_over_sum_pt < 0.090413827016 and Q.pt_7 > 33.21875:
        z += -0.08753801882266998 * (0.090413827016 - Q.mass_over_sum_pt) * (Q.pt_7 - 33.21875)
    if Q.lam2 > 0.000194798295 and Q.tau21 < 0.501026660204:
        z += 1701.93994140625 * (Q.lam2 - 0.000194798295) * (0.501026660204 - Q.tau21)
    if Q.LHA > 0.303313749495 and Q.tau21 < 0.553068161011:
        z += -39.90619659423828 * (Q.LHA - 0.303313749495) * (0.553068161011 - Q.tau21)
    if Q.eccentricity > 0.903125533696 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += 212.52987670898438 * (Q.eccentricity - 0.903125533696) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.tau32 < 0.269169217348 and Q.n_dr_0p2_0p4 < 2.0:
        z += -4.426733493804932 * (0.269169217348 - Q.tau32) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.n_dr_0p2_0p4 > 2.0 and Q.dr_7 > 0.222994708167:
        z += -1.4259655475616455 * (Q.n_dr_0p2_0p4 - 2.0) * (Q.dr_7 - 0.222994708167)
    if Q.lam1 < 0.004183811014 and Q.mean_phi > 0.009050007537:
        z += -699.8038330078125 * (0.004183811014 - Q.lam1) * (Q.mean_phi - 0.009050007537)
    if Q.tau21 < 0.391541349888 and Q.mean_phi < -0.009352574684:
        z += -19.060935974121094 * (0.391541349888 - Q.tau21) * (-0.009352574684 - Q.mean_phi)
    if Q.tau21 < 0.391541349888 and Q.mean_eta < -0.006779838586:
        z += 3.2885043621063232 * (0.391541349888 - Q.tau21) * (-0.006779838586 - Q.mean_eta)
    if Q.tau21 < 0.391541349888 and Q.pt_4 > 39.8125:
        z += -0.08711312711238861 * (0.391541349888 - Q.tau21) * (Q.pt_4 - 39.8125)
    if Q.n_dr_0p05_0p1 < 3.0 and Q.D2 < 1.432482242584:
        z += -0.09762109816074371 * (3.0 - Q.n_dr_0p05_0p1) * (1.432482242584 - Q.D2)
    if Q.n_dr_0p2_0p4 > 2.0 and Q.dr_7 < 0.042151962757:
        z += -10.689244270324707 * (Q.n_dr_0p2_0p4 - 2.0) * (0.042151962757 - Q.dr_7)
    if Q.C2 > 0.051192347892 and Q.dr_7 < 0.222994708167:
        z += -81.2509765625 * (Q.C2 - 0.051192347892) * (0.222994708167 - Q.dr_7)
    if Q.lam2 > 0.000194798295 and Q.D2 < 2.055451202393:
        z += -241.01119995117188 * (Q.lam2 - 0.000194798295) * (2.055451202393 - Q.D2)
    if Q.lam1 < 0.004183811014 and Q.dr_7 < 0.175465903809:
        z += 1456.8031005859375 * (0.004183811014 - Q.lam1) * (0.175465903809 - Q.dr_7)
    if Q.tau21 < 0.391541349888 and Q.z_4 > 0.075444822386:
        z += 79.89892578125 * (0.391541349888 - Q.tau21) * (Q.z_4 - 0.075444822386)
    if Q.C2 > 0.051192347892 and Q.pt_3 < 45.059375:
        z += -0.11625772714614868 * (Q.C2 - 0.051192347892) * (45.059375 - Q.pt_3)
    if Q.lam1 < 0.004183811014 and Q.sum_pt > 988.4078125:
        z += -5.552268981933594 * (0.004183811014 - Q.lam1) * (Q.sum_pt - 988.4078125)
    if Q.lam1 < 0.004183811014 and Q.log_sum_pt > 6.701242202626:
        z += 3703.433837890625 * (0.004183811014 - Q.lam1) * (Q.log_sum_pt - 6.701242202626)
    if Q.mass > 15.454033088684 and Q.n_dr_0p2_0p4 < 2.0:
        z += -0.0037098738830536604 * (Q.mass - 15.454033088684) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.max_dr > 0.121680960059 and Q.mean_phi > -0.003096654534:
        z += -18.952415466308594 * (Q.max_dr - 0.121680960059) * (Q.mean_phi - -0.003096654534)
    if Q.phi_6 > 0.05560760498 and Q.eta_7 < -0.121826171875:
        z += 40.39710235595703 * (Q.phi_6 - 0.05560760498) * (-0.121826171875 - Q.eta_7)
    if Q.eccentricity > 0.903125533696 and Q.mass_top2 < 36.768271023571:
        z += -0.09248523414134979 * (Q.eccentricity - 0.903125533696) * (36.768271023571 - Q.mass_top2)
    if Q.tau21 < 0.391541349888 and Q.dr01 < 0.251215918102:
        z += 0.4145125150680542 * (0.391541349888 - Q.tau21) * (0.251215918102 - Q.dr01)
    if Q.phi_6 > 0.05560760498 and Q.mean_eta > -0.009391680919:
        z += 23.267295837402344 * (Q.phi_6 - 0.05560760498) * (Q.mean_eta - -0.009391680919)
    return max(0.0, z)


def neuron_11(Q):
    z = -1.6532527208328247
    if Q.planar_flow < 0.253403707141:
        z += -8.949878692626953 * Q.planar_flow + 2.2679324391739164
    if Q.LHA < 0.154689112391:
        z += 28.07322120666504 * Q.LHA - 4.3426216704152125
    if Q.girth < 0.076081777364:
        z += 67.81546020507812 * Q.girth - 5.915984289140926
    if 0.076081777364 <= Q.girth < 0.087236513197:
        z += 14.060783386230469 * Q.girth - 1.8262329351355868
    if 0.087236513197 <= Q.girth < 0.101940929517:
        z += -53.754676818847656 * Q.girth + 4.089751354005339
    if Q.girth >= 0.101940929517:
        z += -78.68796157836914 * Q.girth + 6.631473578303009
    if Q.centroid_offset < 0.014379521101:
        z += -77.67986488342285 * Q.centroid_offset + 4.319413937611485
    if 0.014379521101 <= Q.centroid_offset < 0.049903668404:
        z += -124.72063636779785 * Q.centroid_offset + 4.995837703778375
    if Q.centroid_offset >= 0.049903668404:
        z += -38.165597915649414 * Q.centroid_offset + 0.6764237661668894
    if Q.girth2_top2 < 0.001056655216:
        z += -140.24551391601562 * Q.girth2_top2 + 0.1481911537999585
    if Q.n_dr_0p1_0p2 < 2.0:
        z += 0.27926068380475044 * Q.n_dr_0p1_0p2 - 0.8573421910405159
    if 2.0 <= Q.n_dr_0p1_0p2 < 3.0:
        z += 0.298820823431015 * Q.n_dr_0p1_0p2 - 0.896462470293045
    if Q.width < 0.003562611091:
        z += -671.6153564453125 * Q.width + 7.953530611439512
    if 0.003562611091 <= Q.width < 0.008678044951:
        z += -1087.068359375 * Q.width + 9.433628087466072
    if Q.e2_sq < 0.006390124748:
        z += 451.1053161621094 * Q.e2_sq - 2.8826192447618597
    if Q.n_dr_0_0p05 < 7.0:
        z += 0.08124648034572601 * Q.n_dr_0_0p05 - 0.5687253624200821
    if Q.e2 < 0.007078157854:
        z += 53.18154335021973 * Q.e2 - 1.7197942573791816
    if 0.007078157854 <= Q.e2 < 0.04447356835:
        z += 35.923309326171875 * Q.e2 - 1.5976377526756973
    if Q.girth2 < 0.006679471442:
        z += -945.5784606933594 * Q.girth2 + 7.776017528874814
    if 0.006679471442 <= Q.girth2 < 0.013238675334:
        z += -222.59609985351562 * Q.girth2 + 2.9468774965753384
    if Q.lam1 < 0.004839980301:
        z += 491.78265380859375 * Q.lam1 - 3.5673776685771568
    if 0.004839980301 <= Q.lam1 < 0.008375572068:
        z += 335.77386474609375 * Q.lam1 - 2.8122982027317924
    if Q.mass_top5 < 9.257203159811:
        z += -0.04958771914243698 * Q.mass_top5 + 0.45904359033318803
    if Q.mass < 15.454033088684:
        z += -0.05189798027276993 * Q.mass + 0.802033104371256
    if Q.pt_7 < 29.0421875:
        z += 0.05483849346637726 * Q.pt_7 - 1.5926298094680533
    if Q.z_dr_0p05_0p1 >= 0.846033477783:
        z += -0.027731217443943024 * Q.z_dr_0p05_0p1 + 0.02346153833725571
    if Q.sum_pt_top5 < 687.4375:
        z += -0.006699726451188326 * Q.sum_pt_top5 + 4.605643202288775
    if Q.girth2_top3 < 0.002151567843:
        z += 164.2704620361328 * Q.girth2_top3 - 0.3534390436716957
    if Q.C2 < 0.035786485299:
        z += 22.50098419189453 * Q.C2 - 0.8052311399962649
    if Q.girth2_top5 < 0.000657050184:
        z += 261.492431640625 * Q.girth2_top5 - 0.17181365032408008
    if Q.max_dr < 0.111761856824:
        z += 4.343432664871216 * Q.max_dr - 0.1334569085263435
    if 0.111761856824 <= Q.max_dr < 0.221586732566:
        z += -3.2048585414886475 * Q.max_dr + 0.7101541325447057
    if Q.m01 >= 45.595:
        z += -0.13308772444725037 * Q.m01 + 6.06813479617238
    if Q.log_sum_pt < 6.701242202626:
        z += 0.6103333830833435 * Q.log_sum_pt - 4.089991824389603
    if Q.planar_flow < 0.253403707141 and Q.width > 0.006096650059:
        z += -1068.4000244140625 * (0.253403707141 - Q.planar_flow) * (Q.width - 0.006096650059)
    if Q.planar_flow < 0.253403707141 and Q.D2 < 1.679198372364:
        z += -0.42285892367362976 * (0.253403707141 - Q.planar_flow) * (1.679198372364 - Q.D2)
    if Q.planar_flow < 0.253403707141 and Q.girth2 > 0.013238675334:
        z += 976.1707153320312 * (0.253403707141 - Q.planar_flow) * (Q.girth2 - 0.013238675334)
    if Q.planar_flow < 0.253403707141 and Q.mass < 69.611351776123:
        z += -0.12278295308351517 * (0.253403707141 - Q.planar_flow) * (69.611351776123 - Q.mass)
    if Q.planar_flow < 0.253403707141 and Q.max_dr > 0.102758520097:
        z += -48.4774055480957 * (0.253403707141 - Q.planar_flow) * (Q.max_dr - 0.102758520097)
    if Q.centroid_offset < 0.049903668404 and Q.pt_7 < 48.71875:
        z += 0.31047752499580383 * (0.049903668404 - Q.centroid_offset) * (48.71875 - Q.pt_7)
    if Q.centroid_offset < 0.049903668404 and Q.n_dr_0p05_0p1 > 2.0:
        z += 4.074214458465576 * (0.049903668404 - Q.centroid_offset) * (Q.n_dr_0p05_0p1 - 2.0)
    if Q.centroid_offset < 0.049903668404 and Q.log_sum_pt < 6.804164030582:
        z += -101.79106903076172 * (0.049903668404 - Q.centroid_offset) * (6.804164030582 - Q.log_sum_pt)
    if Q.e2_sq < 0.006390124748 and Q.D2 < 1.332146394253:
        z += 139.36729431152344 * (0.006390124748 - Q.e2_sq) * (1.332146394253 - Q.D2)
    if Q.centroid_offset < 0.049903668404 and Q.mean_phi2 < 0.001570267399:
        z += -1375.3287353515625 * (0.049903668404 - Q.centroid_offset) * (0.001570267399 - Q.mean_phi2)
    if Q.width < 0.003562611091 and Q.C2 > 0.030867108516:
        z += 5913.451171875 * (0.003562611091 - Q.width) * (Q.C2 - 0.030867108516)
    if Q.centroid_offset < 0.049903668404 and Q.mean_phi < -0.000855675264:
        z += -281.1932067871094 * (0.049903668404 - Q.centroid_offset) * (-0.000855675264 - Q.mean_phi)
    if Q.planar_flow < 0.253403707141 and Q.z_6 < 0.034484056668:
        z += -112.50518035888672 * (0.253403707141 - Q.planar_flow) * (0.034484056668 - Q.z_6)
    if Q.LHA < 0.154689112391 and Q.z_7 < 0.028070914944:
        z += 818.7977905273438 * (0.154689112391 - Q.LHA) * (0.028070914944 - Q.z_7)
    if Q.girth > 0.076081777364 and Q.n_pt_above_50 < 7.0:
        z += 11.687670707702637 * (Q.girth - 0.076081777364) * (7.0 - Q.n_pt_above_50)
    if Q.mass < 15.454033088684 and Q.phi_1 < -0.058901977539:
        z += 15.344786643981934 * (15.454033088684 - Q.mass) * (-0.058901977539 - Q.phi_1)
    if Q.sum_pt_top5 < 687.4375 and Q.n_dr_0p2_0p4 < 2.0:
        z += 0.00033303516102023423 * (687.4375 - Q.sum_pt_top5) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.girth2 < 0.013238675334 and Q.mass_top5 > 49.186182222392:
        z += 3.2229177951812744 * (0.013238675334 - Q.girth2) * (Q.mass_top5 - 49.186182222392)
    if Q.e2_sq < 0.006390124748 and Q.phi_0 > 0.079772949219:
        z += 18030.939453125 * (0.006390124748 - Q.e2_sq) * (Q.phi_0 - 0.079772949219)
    if Q.pt_7 < 29.0421875 and Q.mass_top2 < 22.844978847276:
        z += 0.002251591067761183 * (29.0421875 - Q.pt_7) * (22.844978847276 - Q.mass_top2)
    if Q.centroid_offset > 0.014379521101 and Q.pt_5 < 29.875:
        z += -3.6258931159973145 * (Q.centroid_offset - 0.014379521101) * (29.875 - Q.pt_5)
    if Q.mass_top5 < 9.257203159811 and Q.eta_0 < -0.053314208984:
        z += 7.318114280700684 * (9.257203159811 - Q.mass_top5) * (-0.053314208984 - Q.eta_0)
    if Q.girth2_top3 < 0.002151567843 and Q.phi_0 > -0.029769897461:
        z += -1114.210205078125 * (0.002151567843 - Q.girth2_top3) * (Q.phi_0 - -0.029769897461)
    if Q.max_dr < 0.221586732566 and Q.phi_0 < 0.021438598633:
        z += 26.836212158203125 * (0.221586732566 - Q.max_dr) * (0.021438598633 - Q.phi_0)
    if Q.e2 < 0.04447356835 and Q.pt_5 > 43.0625:
        z += -0.39709118008613586 * (0.04447356835 - Q.e2) * (Q.pt_5 - 43.0625)
    if Q.n_dr_0_0p05 < 7.0 and Q.z_1st < 0.500737345219:
        z += 0.04141310974955559 * (7.0 - Q.n_dr_0_0p05) * (0.500737345219 - Q.z_1st)
    if Q.pt_7 < 29.0421875 and Q.n_dr_0p2_0p4 < 2.0:
        z += -0.021570784971117973 * (29.0421875 - Q.pt_7) * (2.0 - Q.n_dr_0p2_0p4)
    return max(0.0, z)


def neuron_12(Q):
    z = -1.1632522344589233
    if Q.girth2 >= 0.018827652745:
        z += 229.80149841308594 * Q.girth2 - 4.326622812402251
    if Q.mass >= 91.19:
        z += 0.07892536371946335 * Q.mass - 7.197203917577863
    if Q.mass_over_sum_pt >= 0.13092863437:
        z += -7.325367450714111 * Q.mass_over_sum_pt + 0.9591003565804468
    if Q.girth2_top2 >= 0.0140332421:
        z += 5.683581829071045 * Q.girth2_top2 - 0.07975907980251479
    if Q.e2 >= 0.063441075385:
        z += -122.22758483886719 * Q.e2 + 7.754249423889057
    if Q.mean_phi >= 0.026127964072:
        z += 25.772808074951172 * Q.mean_phi - 0.6733910034168757
    if Q.n_dr_0p2_0p4 >= 1.0:
        z += 0.30232274532318115 * Q.n_dr_0p2_0p4 - 0.30232274532318115
    if Q.girth2 > 0.018827652745 and Q.lam2 > 0.000537286005:
        z += 20462.10546875 * (Q.girth2 - 0.018827652745) * (Q.lam2 - 0.000537286005)
    if Q.mass > 91.19 and Q.max_pair_mass < 45.595:
        z += 7.848533277865499e-05 * (Q.mass - 91.19) * (45.595 - Q.max_pair_mass)
    if Q.girth2 > 0.018827652745 and Q.pt_7 > 15.55390625:
        z += 6.882623195648193 * (Q.girth2 - 0.018827652745) * (Q.pt_7 - 15.55390625)
    if Q.girth2 > 0.018827652745 and Q.mass < 80.4:
        z += -3.361116409301758 * (Q.girth2 - 0.018827652745) * (80.4 - Q.mass)
    if Q.girth2_top2 > 0.0140332421 and Q.z_6 < 0.089100391399:
        z += -83.86389923095703 * (Q.girth2_top2 - 0.0140332421) * (0.089100391399 - Q.z_6)
    if Q.n_dr_0p2_0p4 > 1.0 and Q.lam2 < 0.003408388935:
        z += -84.53605651855469 * (Q.n_dr_0p2_0p4 - 1.0) * (0.003408388935 - Q.lam2)
    if Q.mass > 91.19 and Q.eta_5 < 0.112243652344:
        z += -0.010836445726454258 * (Q.mass - 91.19) * (0.112243652344 - Q.eta_5)
    if Q.girth2_top2 > 0.0140332421 and Q.width > 0.013238675006:
        z += -1114.6807861328125 * (Q.girth2_top2 - 0.0140332421) * (Q.width - 0.013238675006)
    if Q.n_dr_0p2_0p4 > 1.0 and Q.mean_eta < -0.017909069173:
        z += -4.535405158996582 * (Q.n_dr_0p2_0p4 - 1.0) * (-0.017909069173 - Q.mean_eta)
    if Q.mass > 91.19 and Q.eta_3 < -0.066412353516:
        z += 0.06516434252262115 * (Q.mass - 91.19) * (-0.066412353516 - Q.eta_3)
    if Q.mass > 91.19 and Q.centroid_offset > 0.02076709205:
        z += 1.0742005109786987 * (Q.mass - 91.19) * (Q.centroid_offset - 0.02076709205)
    return max(0.0, z)


def neuron_13(Q):
    z = 2.5305356979370117
    if Q.girth < 0.101940929517:
        z += -45.42144012451172 * Q.girth + 6.740924078928302
    if 0.101940929517 <= Q.girth < 0.148408418149:
        z += -53.448567390441895 * Q.girth + 7.559216893768479
    if Q.girth >= 0.148408418149:
        z += -8.027127265930176 * Q.girth + 0.8182928148401769
    if Q.lam1 < 0.006506575659:
        z += -497.36065673828125 * Q.lam1 + 5.007444886904883
    if 0.006506575659 <= Q.lam1 < 0.016433749775:
        z += -178.43246459960938 * Q.lam1 + 2.932314474966526
    if Q.sum_pt_top5 < 531.1875:
        z += -0.002714630914852023 * Q.sum_pt_top5 + 1.441978009082959
    if 658.125 <= Q.sum_pt_top5 < 839.9546875:
        z += 0.0021716756746172905 * Q.sum_pt_top5 - 1.4292340533575043
    if 839.9546875 <= Q.sum_pt_top5 < 902.40625:
        z += 0.016933186911046505 * Q.sum_pt_top5 - 13.828234610980143
    if Q.sum_pt_top5 >= 902.40625:
        z += 0.010385323315858841 * Q.sum_pt_top5 - 7.919401578535325
    if Q.lam2 < 0.000306123359:
        z += -2359.168212890625 * Q.lam2 + 0.7221964977761053
    if Q.e2 < 0.050284641981:
        z += 81.23583984375 * Q.e2 - 4.084915122568824
    if Q.pt_6 < 31.90625:
        z += -0.012512541376054287 * Q.pt_6 + 0.3992282732797321
    if Q.z_top5_slots >= 0.930764273368:
        z += -8.221342086791992 * Q.z_top5_slots + 7.652131493522706
    if Q.z_7 < 0.028070914944:
        z += 105.85017585754395 * Q.z_7 - 3.2357695266420956
    if 0.028070914944 <= Q.z_7 < 0.055577157257:
        z += 9.614480972290039 * Q.z_7 - 0.5343455209413978
    if Q.tau21 < 0.501026660204:
        z += 0.8260151743888855 * Q.tau21 - 0.4138556241018879
    if Q.C2 >= 0.067292226106:
        z += -49.22437286376953 * Q.C2 + 3.31241762867483
    if Q.z_6 < 0.067272114405:
        z += -23.510229110717773 * Q.z_6 + 1.5815828224239674
    if Q.centroid_offset < 0.037760993714:
        z += -46.23400115966797 * Q.centroid_offset + 1.7458418271632907
    if Q.LHA >= 0.09323897448:
        z += -4.5922322273254395 * Q.LHA + 0.4281750234498302
    if Q.width < 0.003562611091:
        z += 212.7697639465332 * Q.width - 0.8429080960630446
    if 0.003562611091 <= Q.width < 0.00752008842:
        z += 237.10861206054688 * Q.width - 0.9296179462961942
    if 0.00752008842 <= Q.width < 0.013238675006:
        z += -149.24313354492188 * Q.width + 1.9757813418782773
    if Q.z_top5 >= 0.877015459538:
        z += 2.633789300918579 * Q.z_top5 - 2.3098739340713754
    if Q.pt_5 < 24.578125:
        z += 0.06449452042579651 * Q.pt_5 - 1.5851543848402798
    if Q.mass >= 53.332374954224:
        z += 0.006307520437985659 * Q.mass - 0.33639504503008233
    if Q.sum_pt < 763.825:
        z += 0.0020046881400048733 * Q.sum_pt - 1.5312309185392223
    if Q.sum_pt >= 988.4078125:
        z += -0.038450125604867935 * Q.sum_pt + 38.00440453945775
    if Q.pt_7 < 25.578125:
        z += 0.19944548606872559 * Q.pt_7 - 5.101441573351622
    if Q.girth < 0.148408418149 and Q.log_sum_pt < 6.804164030582:
        z += -42.00978088378906 * (0.148408418149 - Q.girth) * (6.804164030582 - Q.log_sum_pt)
    if Q.girth < 0.148408418149 and Q.pt_7 < 38.53125:
        z += -1.0689646005630493 * (0.148408418149 - Q.girth) * (38.53125 - Q.pt_7)
    if Q.sum_pt_top5 > 658.125 and Q.z_7 > 0.023207568189:
        z += -0.2908177971839905 * (Q.sum_pt_top5 - 658.125) * (Q.z_7 - 0.023207568189)
    if Q.lam2 < 0.000306123359 and Q.centroid_offset < 0.049903668404:
        z += -95849.8515625 * (0.000306123359 - Q.lam2) * (0.049903668404 - Q.centroid_offset)
    if Q.sum_pt_top5 > 658.125 and Q.pt_7 < 43.5:
        z += 0.0005646605277433991 * (Q.sum_pt_top5 - 658.125) * (43.5 - Q.pt_7)
    if Q.girth < 0.148408418149 and Q.lam2 > 0.003408388935:
        z += 11235.1552734375 * (0.148408418149 - Q.girth) * (Q.lam2 - 0.003408388935)
    if Q.lam1 < 0.016433749775 and Q.pt_6 < 56.53125:
        z += -1.6158039569854736 * (0.016433749775 - Q.lam1) * (56.53125 - Q.pt_6)
    if Q.e2 < 0.050284641981 and Q.pt_dispersion > 0.396830244362:
        z += 75.99822235107422 * (0.050284641981 - Q.e2) * (Q.pt_dispersion - 0.396830244362)
    if Q.sum_pt_top5 > 658.125 and Q.z_dr_0p05_0p1 > 0.048758227378:
        z += -0.004874728620052338 * (Q.sum_pt_top5 - 658.125) * (Q.z_dr_0p05_0p1 - 0.048758227378)
    if Q.sum_pt_top5 > 658.125 and Q.tau32 < 0.362731824815:
        z += -0.02765604294836521 * (Q.sum_pt_top5 - 658.125) * (0.362731824815 - Q.tau32)
    if Q.lam1 < 0.016433749775 and Q.centroid_offset < 0.037760993714:
        z += -1879.298828125 * (0.016433749775 - Q.lam1) * (0.037760993714 - Q.centroid_offset)
    if Q.girth < 0.148408418149 and Q.mean_phi < -0.000855675264:
        z += -44.0218505859375 * (0.148408418149 - Q.girth) * (-0.000855675264 - Q.mean_phi)
    if Q.sum_pt_top5 > 902.40625 and Q.D2 < 3.885568320751:
        z += 0.006409760564565659 * (Q.sum_pt_top5 - 902.40625) * (3.885568320751 - Q.D2)
    if Q.sum_pt_top5 > 839.9546875 and Q.z_dr_0p1_0p2 < 0.15855820179:
        z += 0.04417239502072334 * (Q.sum_pt_top5 - 839.9546875) * (0.15855820179 - Q.z_dr_0p1_0p2)
    if Q.tau21 < 0.501026660204 and Q.max_dr > 0.015595615841:
        z += -16.22652244567871 * (0.501026660204 - Q.tau21) * (Q.max_dr - 0.015595615841)
    if Q.sum_pt_top5 > 902.40625 and Q.n_pt_above_50 > 6.0:
        z += -0.01252188440412283 * (Q.sum_pt_top5 - 902.40625) * (Q.n_pt_above_50 - 6.0)
    if Q.sum_pt_top5 > 839.9546875 and Q.n_pt_above_50 > 2.0:
        z += 3.774244760279544e-05 * (Q.sum_pt_top5 - 839.9546875) * (Q.n_pt_above_50 - 2.0)
    if Q.sum_pt_top5 < 531.1875 and Q.z_4 < 0.037477688199:
        z += -9.40822696685791 * (531.1875 - Q.sum_pt_top5) * (0.037477688199 - Q.z_4)
    if Q.centroid_offset < 0.037760993714 and Q.z_dr_0p2_0p4 > 0.1009733513:
        z += -70.80952453613281 * (0.037760993714 - Q.centroid_offset) * (Q.z_dr_0p2_0p4 - 0.1009733513)
    if Q.width < 0.003562611091 and Q.n_pt_above_50 > 7.0:
        z += 158.63027954101562 * (0.003562611091 - Q.width) * (Q.n_pt_above_50 - 7.0)
    if Q.girth > 0.101940929517 and Q.pt_1 < 116.0:
        z += 0.12051639705896378 * (Q.girth - 0.101940929517) * (116.0 - Q.pt_1)
    if Q.sum_pt_top5 < 531.1875 and Q.pt_5 < 29.875:
        z += -0.0009037166018970311 * (531.1875 - Q.sum_pt_top5) * (29.875 - Q.pt_5)
    if Q.lam1 < 0.006506575659 and Q.z_dr_0p05_0p1 > 0.163898047805:
        z += 252.27261352539062 * (0.006506575659 - Q.lam1) * (Q.z_dr_0p05_0p1 - 0.163898047805)
    if Q.mass > 53.332374954224 and Q.z_dr_0p05_0p1 > 0.588259786367:
        z += 0.059521887451410294 * (Q.mass - 53.332374954224) * (Q.z_dr_0p05_0p1 - 0.588259786367)
    if Q.sum_pt < 763.825 and Q.z_4 < 0.037477688199:
        z += 7.3616108894348145 * (763.825 - Q.sum_pt) * (0.037477688199 - Q.z_4)
    if Q.width < 0.00752008842 and Q.m012 > 16.899120053094:
        z += -2.518404722213745 * (0.00752008842 - Q.width) * (Q.m012 - 16.899120053094)
    if Q.girth > 0.101940929517 and Q.pt_4 > 81.375:
        z += -3.7116527557373047 * (Q.girth - 0.101940929517) * (Q.pt_4 - 81.375)
    if Q.sum_pt > 988.4078125 and Q.n_pt_above_50 > 6.0:
        z += 0.018328147009015083 * (Q.sum_pt - 988.4078125) * (Q.n_pt_above_50 - 6.0)
    if Q.e2 < 0.050284641981 and Q.n_pt_above_50 < 5.0:
        z += 1.8978484869003296 * (0.050284641981 - Q.e2) * (5.0 - Q.n_pt_above_50)
    if Q.girth > 0.101940929517 and Q.pt_balance01 < 0.476255698625:
        z += 28.740713119506836 * (Q.girth - 0.101940929517) * (0.476255698625 - Q.pt_balance01)
    if Q.sum_pt > 988.4078125 and Q.D2 < 3.885568320751:
        z += -0.002404024824500084 * (Q.sum_pt - 988.4078125) * (3.885568320751 - Q.D2)
    return max(0.0, z)


def neuron_14(Q):
    z = -0.9445711970329285
    if Q.planar_flow < 0.111513564951:
        z += -5.984802722930908 * Q.planar_flow + 0.6673866871624775
    if Q.z_dr_0p05_0p1 < 0.588259786367:
        z += -1.8822392225265503 * Q.z_dr_0p05_0p1 + 1.1072456429350568
    if Q.z_dr_0p05_0p1 >= 0.750909513235:
        z += -5.702329158782959 * Q.z_dr_0p05_0p1 + 4.281933212927458
    if 0.002464291268 <= Q.lam1 < 0.004183811014:
        z += 295.3602294921875 * Q.lam1 - 0.7278536344520737
    if 0.004183811014 <= Q.lam1 < 0.00543336053:
        z += 80.52137756347656 * Q.lam1 + 0.1709915204823822
    if 0.00543336053 <= Q.lam1 < 0.005954149834:
        z += 32.20990753173828 * Q.lam1 + 0.4334851548991069
    if 0.005954149834 <= Q.lam1 < 0.007330079875:
        z += 295.1680679321289 * Q.lam1 - 1.1322071321978244
    if 0.007330079875 <= Q.lam1 < 0.008375572068:
        z += 109.0839614868164 * Q.lam1 + 0.2318042315143184
    if 0.008375572068 <= Q.lam1 < 0.012003726523:
        z += -147.02108001708984 * Q.lam1 + 2.3768304636084165
    if Q.lam1 >= 0.012003726523:
        z += -129.4263687133789 * Q.lam1 + 2.165628360867533
    if Q.max_dr < 0.080507021025:
        z += 6.819217681884766 * Q.max_dr - 2.4880630853802286
    if 0.080507021025 <= Q.max_dr < 0.177304983139:
        z += 20.03211784362793 * Q.max_dr - 3.551794316502911
    if Q.mass < 76.655700683594:
        z += 0.015147102996706963 * Q.mass - 1.1611117935391386
    if Q.girth2 < 0.004372139461:
        z += -607.515869140625 * Q.girth2 + 8.479537559456304
    if 0.004372139461 <= Q.girth2 < 0.013238675334:
        z += -656.7833862304688 * Q.girth2 + 8.694942015070302
    if Q.width < 0.00752008842:
        z += 740.810546875 * Q.width - 4.3459013249464125
    if 0.00752008842 <= Q.width < 0.008678044951:
        z += -1057.949462890625 * Q.width + 9.180932994851151
    if Q.e2 < 0.035560912266:
        z += -104.7099723815918 * Q.e2 + 4.12837914858124
    if 0.035560912266 <= Q.e2 < 0.038466955721:
        z += -139.29489135742188 * Q.e2 + 5.358250418007453
    if Q.mass_over_sum_pt_sq < 0.011660904657:
        z += 395.2974548339844 * Q.mass_over_sum_pt_sq - 4.609525931973855
    if Q.girth < 0.087236513197:
        z += 86.16893005371094 * Q.girth - 7.517077003801925
    if Q.D2 < 0.74595130682:
        z += -0.1309577226638794 * Q.D2 - 0.46368353601920664
    if 0.74595130682 <= Q.D2 < 1.122624260187:
        z += 1.4903422594070435 * Q.D2 - 1.6730943763922541
    if Q.n_dr_0p05_0p1 < 5.0:
        z += 0.1457621306180954 * Q.n_dr_0p05_0p1 - 0.728810653090477
    if Q.centroid_offset >= 0.049903668404:
        z += -249.29139709472656 * Q.centroid_offset + 12.440555216585123
    if Q.e2_sq < 0.017162483186:
        z += -110.78145599365234 * Q.e2_sq + 1.9012848758116572
    if Q.LHA < 0.303313749495:
        z += 3.193618059158325 * Q.LHA - 0.9686682679782563
    if Q.planar_flow < 0.111513564951 and Q.centroid_offset > 0.018377780003:
        z += -1185.6229248046875 * (0.111513564951 - Q.planar_flow) * (Q.centroid_offset - 0.018377780003)
    if Q.planar_flow < 0.111513564951 and Q.z_dr_0p1_0p2 < 0.258290868998:
        z += 2.7585253715515137 * (0.111513564951 - Q.planar_flow) * (0.258290868998 - Q.z_dr_0p1_0p2)
    if Q.planar_flow < 0.111513564951 and Q.max_dr < 0.15984864831:
        z += -212.21829223632812 * (0.111513564951 - Q.planar_flow) * (0.15984864831 - Q.max_dr)
    if Q.planar_flow < 0.111513564951 and Q.sum_pt < 739.5:
        z += -0.04334425553679466 * (0.111513564951 - Q.planar_flow) * (739.5 - Q.sum_pt)
    if Q.z_dr_0p05_0p1 < 0.588259786367 and Q.C2 < 0.067292226106:
        z += -74.2882080078125 * (0.588259786367 - Q.z_dr_0p05_0p1) * (0.067292226106 - Q.C2)
    if Q.lam1 > 0.007330079875 and Q.max_dr < 0.13261153996:
        z += 52166.07421875 * (Q.lam1 - 0.007330079875) * (0.13261153996 - Q.max_dr)
    if Q.lam1 > 0.008375572068 and Q.max_dr < 0.13261153996:
        z += -24851.482421875 * (Q.lam1 - 0.008375572068) * (0.13261153996 - Q.max_dr)
    if Q.planar_flow < 0.111513564951 and Q.max_dr < 0.102758520097:
        z += -171.90042114257812 * (0.111513564951 - Q.planar_flow) * (0.102758520097 - Q.max_dr)
    if Q.lam1 > 0.00543336053 and Q.max_dr < 0.15984864831:
        z += 6611.45068359375 * (Q.lam1 - 0.00543336053) * (0.15984864831 - Q.max_dr)
    if Q.planar_flow < 0.111513564951 and Q.centroid_offset > 0.009480684835:
        z += 1202.620361328125 * (0.111513564951 - Q.planar_flow) * (Q.centroid_offset - 0.009480684835)
    if Q.z_dr_0p05_0p1 < 0.588259786367 and Q.eccentricity > 0.970449631164:
        z += 33.2391357421875 * (0.588259786367 - Q.z_dr_0p05_0p1) * (Q.eccentricity - 0.970449631164)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.n_dr_0p2_0p4 < 1.0:
        z += 5.704836368560791 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.z_dr_0p05_0p1 < 0.588259786367 and Q.n_dr_0p1_0p2 < 3.0:
        z += 0.3613712191581726 * (0.588259786367 - Q.z_dr_0p05_0p1) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.planar_flow < 0.111513564951 and Q.n_dr_0p2_0p4 > 0.0:
        z += -0.7558572888374329 * (0.111513564951 - Q.planar_flow) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.mass < 76.655700683594 and Q.D2 < 0.74595130682:
        z += -0.0608513206243515 * (76.655700683594 - Q.mass) * (0.74595130682 - Q.D2)
    if Q.width < 0.00752008842 and Q.planar_flow < 0.111513564951:
        z += -5945.9052734375 * (0.00752008842 - Q.width) * (0.111513564951 - Q.planar_flow)
    if Q.girth2 < 0.013238675334 and Q.eccentricity > 0.970449631164:
        z += 5881.4677734375 * (0.013238675334 - Q.girth2) * (Q.eccentricity - 0.970449631164)
    if Q.girth2 < 0.004372139461 and Q.D2 < 0.87567204833:
        z += 216.6103057861328 * (0.004372139461 - Q.girth2) * (0.87567204833 - Q.D2)
    if Q.width < 0.00752008842 and Q.D2 < 1.002470755577:
        z += 481.1053771972656 * (0.00752008842 - Q.width) * (1.002470755577 - Q.D2)
    if Q.mass < 76.655700683594 and Q.n_dr_0p1_0p2 > 4.0:
        z += 0.010096730664372444 * (76.655700683594 - Q.mass) * (Q.n_dr_0p1_0p2 - 4.0)
    if Q.e2 < 0.038466955721 and Q.D2 < 1.002470755577:
        z += 194.32009887695312 * (0.038466955721 - Q.e2) * (1.002470755577 - Q.D2)
    if Q.D2 < 1.122624260187 and Q.centroid_offset < 0.031170772021:
        z += 31.857391357421875 * (1.122624260187 - Q.D2) * (0.031170772021 - Q.centroid_offset)
    if Q.planar_flow < 0.111513564951 and Q.phi_7 > 0.057647705078:
        z += 16.514507293701172 * (0.111513564951 - Q.planar_flow) * (Q.phi_7 - 0.057647705078)
    if Q.planar_flow < 0.111513564951 and Q.sum_pt > 840.01953125:
        z += -0.0003094263083767146 * (0.111513564951 - Q.planar_flow) * (Q.sum_pt - 840.01953125)
    if Q.girth2 < 0.013238675334 and Q.phi_5 < -0.074035644531:
        z += -76.90791320800781 * (0.013238675334 - Q.girth2) * (-0.074035644531 - Q.phi_5)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.eccentricity > 0.984196588116:
        z += 200.0652618408203 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (Q.eccentricity - 0.984196588116)
    if Q.width < 0.00752008842 and Q.log_sum_pt < 6.804164030582:
        z += 254.2174530029297 * (0.00752008842 - Q.width) * (6.804164030582 - Q.log_sum_pt)
    if Q.width < 0.008678044951 and Q.D2 < 1.002470755577:
        z += -1480.2034912109375 * (0.008678044951 - Q.width) * (1.002470755577 - Q.D2)
    if Q.girth2 < 0.013238675334 and Q.D2 < 1.002470755577:
        z += 158.69500732421875 * (0.013238675334 - Q.girth2) * (1.002470755577 - Q.D2)
    if Q.width < 0.00752008842 and Q.n_dr_0p1_0p2 < 3.0:
        z += 136.03062438964844 * (0.00752008842 - Q.width) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.girth2 < 0.004372139461 and Q.n_dr_0p2_0p4 < 1.0:
        z += -163.0378875732422 * (0.004372139461 - Q.girth2) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.girth2 < 0.013238675334 and Q.n_dr_0p1_0p2 < 3.0:
        z += -48.55009460449219 * (0.013238675334 - Q.girth2) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.e2_sq < 0.017162483186 and Q.pt1_dr01 > 22.385778388206:
        z += -0.6615541577339172 * (0.017162483186 - Q.e2_sq) * (Q.pt1_dr01 - 22.385778388206)
    return max(0.0, z)


def neuron_15(Q):
    z = -1.9915000200271606
    if Q.tau21 < 0.23799610585:
        z += -5.775542259216309 * Q.tau21 + 1.3745565668655928
    if Q.width < 0.006096650059:
        z += 1069.5496215820312 * Q.width - 4.306231607462845
    if 0.006096650059 <= Q.width < 0.006679471358:
        z += 1267.1726684570312 * Q.width - 5.511070167853073
    if 0.006679471358 <= Q.width < 0.00752008842:
        z += -4.76312255859375 * Q.width + 2.9847885174508675
    if 0.00752008842 <= Q.width < 0.013238675006:
        z += -515.6815185546875 * Q.width + 6.826940030746067
    if Q.girth2 < 0.018827652745:
        z += -130.9077911376953 * Q.girth2 + 2.464686433155516
    if Q.lam1 < 0.006506575659:
        z += -6.5714569091796875 * Q.lam1 - 2.0309871512691497
    if 0.006506575659 <= Q.lam1 < 0.008375572068:
        z += 720.2821807861328 * Q.lam1 - 6.760315337953075
    if 0.008375572068 <= Q.lam1 < 0.012003726523:
        z += 200.5261993408203 * Q.lam1 - 2.4070616575837898
    if Q.lam2 < 0.000306123359:
        z += 2623.671142578125 * Q.lam2 - 1.3134311050456746
    if 0.000306123359 <= Q.lam2 < 0.001130644719:
        z += 618.8609619140625 * Q.lam2 - 0.6997118783833949
    if 0.176724128067 <= Q.LHA < 0.346713497427:
        z += 1.4005284309387207 * Q.LHA - 0.24750716579068904
    if Q.LHA >= 0.346713497427:
        z += -45.93311262130737 * Q.LHA + 16.163705069387778
    if Q.e2_sq < 0.008168570676:
        z += 677.2814178466797 * Q.e2_sq - 6.321322840512138
    if 0.008168570676 <= Q.e2_sq < 0.011657374702:
        z += 226.1238250732422 * Q.e2_sq - 2.6360101579282866
    if Q.mass_over_sum_pt_sq < 0.007182835724:
        z += -558.1221313476562 * Q.mass_over_sum_pt_sq + 4.008899583398965
    if Q.mass < 36.229410171509:
        z += 0.013077901676297188 * Q.mass - 0.47380466401323595
    if Q.mass >= 80.4:
        z += -0.00951387733221054 * Q.mass + 0.7649157375097275
    if Q.e2 < 0.024547699839:
        z += -333.6337962150574 * Q.e2 + 9.95785133970637
    if 0.024547699839 <= Q.e2 < 0.032346998155:
        z += -112.60449934005737 * Q.e2 + 4.532090504393648
    if 0.032346998155 <= Q.e2 < 0.038466955721:
        z += -118.91763114929199 * Q.e2 + 4.736301367379232
    if 0.038466955721 <= Q.e2 < 0.041109715588:
        z += -115.83690595626831 * Q.e2 + 4.617795247790621
    if 0.041109715588 <= Q.e2 < 0.063441075385:
        z += 6.458496570587158 * Q.e2 - 0.4097339678083839
    if Q.z_dr_0p05_0p1 >= 0.750909513235:
        z += -8.535049438476562 * Q.z_dr_0p05_0p1 + 6.409049819283095
    if Q.z_dr_0p1_0p2 < 0.328461505473:
        z += -3.7090336978435516 * Q.z_dr_0p1_0p2 + 1.185019781940427
    if 0.328461505473 <= Q.z_dr_0p1_0p2 < 0.790636250377:
        z += 0.07195332646369934 * Q.z_dr_0p1_0p2 - 0.05688890823741141
    if Q.n_dr_0_0p05 < 2.0:
        z += -0.16241684556007385 * Q.n_dr_0_0p05 + 0.3248336911201477
    if Q.log_sum_pt >= 6.896095378249:
        z += 35.2607421875 * Q.log_sum_pt - 243.1614412328483
    if Q.planar_flow < 0.083662731125:
        z += 2.825474739074707 * Q.planar_flow - 0.23638693339568675
    if Q.mass_over_sum_pt < 0.06813910019:
        z += 18.04391860961914 * Q.mass_over_sum_pt - 1.229496377961044
    if Q.D2 < 0.74595130682:
        z += 1.2770978212356567 * Q.D2 - 0.9526527886877129
    if Q.n_dr_0p05_0p1 >= 5.0:
        z += 0.2505616247653961 * Q.n_dr_0p05_0p1 - 1.2528081238269806
    if Q.n_dr_0p1_0p2 < 1.0:
        z += -0.0955553948879242 * Q.n_dr_0p1_0p2 + 0.0955553948879242
    if Q.girth >= 0.033604209498:
        z += 28.822702407836914 * Q.girth - 0.9685641300114607
    if Q.girth2_top3 < 0.002151567843:
        z += 521.4407958984375 * Q.girth2_top3 - 1.1219152484834045
    if Q.girth2_top2 < 0.007639643088:
        z += -44.40835189819336 * Q.girth2_top2 + 0.3392639586285046
    if Q.tau21 < 0.23799610585 and Q.z_dr_0p05_0p1 < 0.588259786367:
        z += -11.057096481323242 * (0.23799610585 - Q.tau21) * (0.588259786367 - Q.z_dr_0p05_0p1)
    if Q.tau21 < 0.23799610585 and Q.max_dr < 0.121680960059:
        z += -105.07672119140625 * (0.23799610585 - Q.tau21) * (0.121680960059 - Q.max_dr)
    if Q.tau21 < 0.23799610585 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += 46.4647102355957 * (0.23799610585 - Q.tau21) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.tau21 < 0.23799610585 and Q.mass < 76.655700683594:
        z += 0.0028531881980597973 * (0.23799610585 - Q.tau21) * (76.655700683594 - Q.mass)
    if Q.tau21 < 0.23799610585 and Q.girth2_top5 > 0.00832969537:
        z += -146.20816040039062 * (0.23799610585 - Q.tau21) * (Q.girth2_top5 - 0.00832969537)
    if Q.width < 0.00752008842 and Q.e2 > 0.024547699839:
        z += -43894.19921875 * (0.00752008842 - Q.width) * (Q.e2 - 0.024547699839)
    if Q.LHA > 0.176724128067 and Q.sum_pt_top3 > 353.0625:
        z += 0.05264676362276077 * (Q.LHA - 0.176724128067) * (Q.sum_pt_top3 - 353.0625)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.n_dr_0p2_0p4 < 2.0:
        z += 1.2382736206054688 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.z_dr_0p1_0p2 < 0.328461505473 and Q.n_dr_0p2_0p4 > 0.0:
        z += 0.05187014862895012 * (0.328461505473 - Q.z_dr_0p1_0p2) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.n_dr_0_0p05 < 2.0 and Q.pt_3 > 66.0:
        z += 0.004666578955948353 * (2.0 - Q.n_dr_0_0p05) * (Q.pt_3 - 66.0)
    if Q.lam1 < 0.008375572068 and Q.m01 > 16.308019673264:
        z += -29.13987159729004 * (0.008375572068 - Q.lam1) * (Q.m01 - 16.308019673264)
    if Q.lam1 < 0.006506575659 and Q.pt1_dr01 > 1.21960336377:
        z += 29.69463539123535 * (0.006506575659 - Q.lam1) * (Q.pt1_dr01 - 1.21960336377)
    if Q.mass > 80.4 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += -0.7132310271263123 * (Q.mass - 80.4) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_4 < 0.04181499946:
        z += 80.51174926757812 * (Q.log_sum_pt - 6.896095378249) * (0.04181499946 - Q.dr_4)
    if Q.n_dr_0_0p05 < 2.0 and Q.pt_dispersion < 0.423827920854:
        z += 1.3990377187728882 * (2.0 - Q.n_dr_0_0p05) * (0.423827920854 - Q.pt_dispersion)
    if Q.log_sum_pt > 6.896095378249 and Q.mean_phi > 0.01746432744:
        z += 34044.0078125 * (Q.log_sum_pt - 6.896095378249) * (Q.mean_phi - 0.01746432744)
    if Q.LHA > 0.176724128067 and Q.z_top5 > 0.865048766136:
        z += -100.69448852539062 * (Q.LHA - 0.176724128067) * (Q.z_top5 - 0.865048766136)
    if Q.width < 0.006096650059 and Q.log_sum_pt > 6.896095378249:
        z += -7217.90771484375 * (0.006096650059 - Q.width) * (Q.log_sum_pt - 6.896095378249)
    if Q.girth2 < 0.018827652745 and Q.mass_top2 > 22.844978847276:
        z += 3.5132789611816406 * (0.018827652745 - Q.girth2) * (Q.mass_top2 - 22.844978847276)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.planar_flow < 0.061262048692:
        z += -35.20658493041992 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (0.061262048692 - Q.planar_flow)
    if Q.LHA > 0.176724128067 and Q.dr_7 < 0.042151962757:
        z += 102.64990997314453 * (Q.LHA - 0.176724128067) * (0.042151962757 - Q.dr_7)
    if Q.log_sum_pt > 6.896095378249 and Q.phi_0 < -0.029769897461:
        z += -175.2867431640625 * (Q.log_sum_pt - 6.896095378249) * (-0.029769897461 - Q.phi_0)
    if Q.width < 0.00752008842 and Q.planar_flow < 0.061262048692:
        z += -4778.7607421875 * (0.00752008842 - Q.width) * (0.061262048692 - Q.planar_flow)
    if Q.D2 < 0.74595130682 and Q.pt_7 < 23.21640625:
        z += -0.0879085436463356 * (0.74595130682 - Q.D2) * (23.21640625 - Q.pt_7)
    return max(0.0, z)


def jet_layer_4(Q):
    return [neuron_0(Q), neuron_1(Q), neuron_2(Q), neuron_3(Q), neuron_4(Q), neuron_5(Q), neuron_6(Q), neuron_7(Q), neuron_8(Q), neuron_9(Q), neuron_10(Q), neuron_11(Q), neuron_12(Q), neuron_13(Q), neuron_14(Q), neuron_15(Q)]


def logits(h):
    h = [(math.floor(x * 2 ** f + 0.5) / 2 ** f) % 2 ** i for x, i, f in zip(h, INT_BITS, FRAC_BITS)]
    return [B[c] + sum(h[j] * W[j][c] for j in range(len(h))) for c in range(5)]


def classify(pt, eta, phi):
    s = logits(jet_layer_4(quantities(pt, eta, phi)))
    m = max(s)
    e = [math.exp(x - m) for x in s]
    p = [x / sum(e) for x in e]
    return CLASSES[s.index(m)], s, p


if __name__ == '__main__':
    pt = [412.0, 230.5, 101.2, 40.3, 22.8, 10.1, 6.4, 3.3][:8] + [0.0] * 0
    eta = [0.01, -0.12, 0.25, 0.05, -0.31, 0.2, -0.05, 0.4][:8] + [0.0] * 0
    phi = [-0.02, 0.18, -0.1, 0.33, 0.07, -0.25, 0.12, -0.36][:8] + [0.0] * 0
    c, s, p = classify(pt, eta, phi)
    print('class:', c)
    print('logits:', dict(zip(CLASSES, [round(x, 4) for x in s])))
    print('probabilities:', dict(zip(CLASSES, [round(x, 4) for x in p])))
