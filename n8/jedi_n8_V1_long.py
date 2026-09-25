"""JEDI-linear jet tagger, 8 particles, 3 features, written as a formula (V1, long formulas).

Input:  the 8 hardest particles of a jet, hardest first, each (pT [GeV], Δη, Δφ) relative to the jet axis;
        empty slots have pT = 0.
Output: the class (g, q, W, Z or t), the 5 logits and the 5 probabilities.

1. quantities():  physics quantities of the particles.
2. jet_layer_4(): the 16 neurons of the network's last hidden layer, each max(0, z) with z built from if-statements.
3. logits():      the network's own last layer: each neuron is rounded to the network's fixed-point grid
                  (round to a multiple of 2^-f, then wrap modulo 2^i), multiplied by the weights, plus the biases.
4. classify():    softmax of the logits; the class is the largest logit.

Test set (50,000 jets of the hls4ml LHC jet dataset, test file): accuracy 64.6% (the network: 65.8%); same class as the network for 88.1% of jets.

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
  Q.z_0                    pT of particle 0 / total pT
  Q.z_1                    pT of particle 1 / total pT
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
  Q.orientation_deg        direction of the major axis [degrees]
  Q.dr_0                   ΔR of particle 0 from the jet axis
  Q.dr_1                   ΔR of particle 1 from the jet axis
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
  Q.phi_3                  Δφ of particle 3
  Q.phi_4                  Δφ of particle 4
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
  Q.n_pt_above_10          number of particles with pT > 10 GeV
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
        z_0=z[0],
        z_1=z[1],
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
        orientation_deg=math.degrees(0.5 * math.atan2(2 * tb, ta - tc)),
        dr_0=dr[0] if pt[0] > 0 else 0.0,
        dr_1=dr[1] if pt[1] > 0 else 0.0,
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
        phi_3=phi[3],
        phi_4=phi[4],
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
        n_pt_above_10=sum(1 for x in pt if x > 10),
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
    z = -0.3026721814904832
    if Q.planar_flow < 0.012569162668:
        z += -6.768542264489307 * Q.planar_flow + 0.2113275485506224
    if 0.012569162668 <= Q.planar_flow < 0.148419710734:
        z += -0.9293495065009685 * Q.planar_flow + 0.13793378492565941
    if Q.width < 0.004372139331:
        z += -304.8579932161648 * Q.width + 5.035291820755281
    if 0.004372139331 <= Q.width < 0.008678044951:
        z += -859.8447167648684 * Q.width + 7.4617711029653915
    if Q.girth2 < 0.013238675334:
        z += -510.83604153379406 * Q.girth2 + 7.173646609816824
    if 0.013238675334 <= Q.girth2 < 0.018827652745:
        z += -73.51149894371714 * Q.girth2 + 1.3840489748767406
    if Q.mass < 21.784077072144:
        z += 0.04864720551168318 * Q.mass - 4.20656349977903
    if 21.784077072144 <= Q.mass < 29.644699859619:
        z += 0.06901220856922459 * Q.mass - 4.65019629595896
    if 29.644699859619 <= Q.mass < 56.920347213745:
        z += 0.0843864467833872 * Q.mass - 5.105960973388095
    if 56.920347213745 <= Q.mass < 64.618731689453:
        z += 0.039314108472822976 * Q.mass - 2.5404278270153986
    if Q.girth2_top3 < 0.003952581551:
        z += -15.188962331323637 * Q.girth2_top3 - 0.13711864997944018
    if 0.003952581551 <= Q.girth2_top3 < 0.007929074034:
        z += 49.57994089311697 * Q.girth2_top3 - 0.3931230219428685
    if Q.lam1 < 0.000504949057:
        z += -715.1403222372593 * Q.lam1 - 0.6061802551970088
    if 0.000504949057 <= Q.lam1 < 0.001503553356:
        z += -238.87130405976063 * Q.lam1 - 0.8466718468040526
    if 0.001503553356 <= Q.lam1 < 0.00543336053:
        z += 118.73329354991529 * Q.lam1 - 1.3843494396611105
    if 0.00543336053 <= Q.lam1 < 0.006506575659:
        z += 272.10552584374136 * Q.lam1 - 2.2176760730043763
    if 0.006506575659 <= Q.lam1 < 0.008375572068:
        z += 239.27326971664286 * Q.lam1 - 2.004050514457744
    if 813.415625 <= Q.sum_pt < 901.59375:
        z += -0.004051720776260481 * Q.sum_pt + 3.2957329875474044
    if Q.sum_pt >= 901.59375:
        z += -0.012058211458855883 * Q.sum_pt + 10.514334946408653
    if Q.girth2_top5 < 0.000657050184:
        z += 1460.5753239732742 * Q.girth2_top5 - 1.5045596721033205
    if 0.000657050184 <= Q.girth2_top5 < 0.00832969537:
        z += 71.01701871149461 * Q.girth2_top5 - 0.59155013195234
    if Q.z_dr_0_0p05 >= 0.847731333971:
        z += -0.03309938130152279 * Q.z_dr_0_0p05 + 0.028059382664354687
    if Q.girth < 0.076081777364:
        z += 69.67229068942572 * Q.girth - 5.5487805525018725
    if 0.076081777364 <= Q.girth < 0.087236513197:
        z += 22.231709252625187 * Q.girth - 1.9394167976085042
    if Q.centroid_offset < 0.031170772021:
        z += -4.801198944400747 * Q.centroid_offset + 0.14965707772338155
    if Q.e2 < 0.020459658932:
        z += -19.776538534584517 * Q.e2 + 0.4046212332731543
    if Q.mass_over_sum_pt_sq < 0.003904593248:
        z += -31.821108221518614 * Q.mass_over_sum_pt_sq - 1.1032630983333338
    if 0.003904593248 <= Q.mass_over_sum_pt_sq < 0.008174660116:
        z += 287.46893680704596 * Q.mass_over_sum_pt_sq - 2.349960852305483
    if 6.377722943814 <= Q.log_sum_pt < 6.638338705138:
        z += 0.5495910293616362 * Q.log_sum_pt - 3.5051393176740606
    if Q.log_sum_pt >= 6.638338705138:
        z += -5.917025980714129 * Q.log_sum_pt + 39.42245467161566
    if Q.sum_pt_top5 >= 687.4375:
        z += 0.010336405562270556 * Q.sum_pt_top5 - 7.105632798713366
    if Q.mass_over_sum_pt < 0.13092863437:
        z += 22.076242280410497 * Q.mass_over_sum_pt - 2.8904122537954007
    if Q.z_dr_0p05_0p1 >= 0.846033477783:
        z += 0.5964944791177231 * Q.z_dr_0p05_0p1 - 0.5046542986463264
    if Q.tau32 >= 0.430992257595:
        z += -0.12787186338209722 * Q.tau32 + 0.05511178308192949
    if Q.D2 >= 3.885568320751:
        z += -0.044100908921791415 * Q.D2 + 0.17135709462283788
    if Q.n_dr_0_0p05 >= 4.0:
        z += 0.08562128608082276 * Q.n_dr_0_0p05 - 0.342485144323291
    if Q.LHA < 0.293190627853:
        z += -7.225180695588847 * Q.LHA + 2.1183552644910693
    if Q.planar_flow < 0.148419710734 and Q.centroid_offset < 0.049903668404:
        z += 72.54276329895687 * (0.148419710734 - Q.planar_flow) * (0.049903668404 - Q.centroid_offset)
    if Q.width < 0.004372139331 and Q.D2 < 0.74595130682:
        z += 1578.210174650157 * (0.004372139331 - Q.width) * (0.74595130682 - Q.D2)
    if Q.lam1 < 0.006506575659 and Q.D2 < 0.87567204833:
        z += -1032.0569510436426 * (0.006506575659 - Q.lam1) * (0.87567204833 - Q.D2)
    if Q.girth2 < 0.013238675334 and Q.D2 < 1.002470755577:
        z += -16.244508858550148 * (0.013238675334 - Q.girth2) * (1.002470755577 - Q.D2)
    if Q.sum_pt > 901.59375 and Q.pt_7 < 25.578125:
        z += 0.00013189211414244006 * (Q.sum_pt - 901.59375) * (25.578125 - Q.pt_7)
    if Q.girth2 < 0.013238675334 and Q.mean_phi < -0.001813532785:
        z += -739.8347134262568 * (0.013238675334 - Q.girth2) * (-0.001813532785 - Q.mean_phi)
    if Q.planar_flow < 0.148419710734 and Q.sum_pt_top2 < 380.5875:
        z += -0.01974437304362464 * (0.148419710734 - Q.planar_flow) * (380.5875 - Q.sum_pt_top2)
    if Q.planar_flow < 0.148419710734 and Q.dr_2 < 0.027807975573:
        z += -212.00082586351556 * (0.148419710734 - Q.planar_flow) * (0.027807975573 - Q.dr_2)
    if Q.sum_pt > 901.59375 and Q.dr_2 < 0.038438041256:
        z += 0.09220505392753298 * (Q.sum_pt - 901.59375) * (0.038438041256 - Q.dr_2)
    if Q.girth2 < 0.018827652745 and Q.mass_top2 > 28.78966323496:
        z += 3.5034319846061788 * (0.018827652745 - Q.girth2) * (Q.mass_top2 - 28.78966323496)
    if Q.mass < 56.920347213745 and Q.C2 > 0.023843882605:
        z += 0.7566176679409038 * (56.920347213745 - Q.mass) * (Q.C2 - 0.023843882605)
    if Q.mass < 29.644699859619 and Q.D2 < 0.87567204833:
        z += 0.31841970255728835 * (29.644699859619 - Q.mass) * (0.87567204833 - Q.D2)
    if Q.planar_flow < 0.148419710734 and Q.max_dr < 0.111761856824:
        z += -87.43621566293723 * (0.148419710734 - Q.planar_flow) * (0.111761856824 - Q.max_dr)
    if Q.girth2 < 0.013238675334 and Q.centroid_offset > 0.014379521101:
        z += -6494.343361434313 * (0.013238675334 - Q.girth2) * (Q.centroid_offset - 0.014379521101)
    if Q.mass < 64.618731689453 and Q.centroid_offset > 0.012587644117:
        z += 1.3942446937910415 * (64.618731689453 - Q.mass) * (Q.centroid_offset - 0.012587644117)
    if Q.girth2 < 0.018827652745 and Q.phi_0 > 0.021438598633:
        z += 349.22268922651745 * (0.018827652745 - Q.girth2) * (Q.phi_0 - 0.021438598633)
    if Q.girth2 < 0.018827652745 and Q.eccentricity > 0.959856212153:
        z += 991.1870808060738 * (0.018827652745 - Q.girth2) * (Q.eccentricity - 0.959856212153)
    if Q.sum_pt > 901.59375 and Q.pt_7 > 29.0421875:
        z += 0.00013503257974889493 * (Q.sum_pt - 901.59375) * (Q.pt_7 - 29.0421875)
    if Q.girth2_top3 < 0.007929074034 and Q.pt_6 < 35.28125:
        z += -0.9136199336895174 * (0.007929074034 - Q.girth2_top3) * (35.28125 - Q.pt_6)
    if Q.log_sum_pt > 6.638338705138 and Q.dr_4 < 0.072321663733:
        z += 80.2652097394848 * (Q.log_sum_pt - 6.638338705138) * (0.072321663733 - Q.dr_4)
    if Q.sum_pt_top5 > 687.4375 and Q.phi_2 > 0.064147949219:
        z += 0.04228482282451296 * (Q.sum_pt_top5 - 687.4375) * (Q.phi_2 - 0.064147949219)
    if Q.girth2_top3 < 0.007929074034 and Q.phi_1 < -0.002475547791:
        z += 77.60243559050211 * (0.007929074034 - Q.girth2_top3) * (-0.002475547791 - Q.phi_1)
    if Q.sum_pt_top5 > 687.4375 and Q.eta_6 > 0.076599121094:
        z += 0.01011003489588802 * (Q.sum_pt_top5 - 687.4375) * (Q.eta_6 - 0.076599121094)
    if Q.sum_pt_top5 > 687.4375 and Q.z_7 > 0.023207568189:
        z += -0.13358407670898487 * (Q.sum_pt_top5 - 687.4375) * (Q.z_7 - 0.023207568189)
    if Q.mass < 64.618731689453 and Q.pt_7 < 40.040625:
        z += -0.0002481962250158176 * (64.618731689453 - Q.mass) * (40.040625 - Q.pt_7)
    if Q.log_sum_pt > 6.638338705138 and Q.dr_7 < 0.093979107928:
        z += 14.413150479388008 * (Q.log_sum_pt - 6.638338705138) * (0.093979107928 - Q.dr_7)
    if Q.mass_over_sum_pt_sq < 0.008174660116 and Q.eta_7 > 0.020645141602:
        z += 243.04085651581843 * (0.008174660116 - Q.mass_over_sum_pt_sq) * (Q.eta_7 - 0.020645141602)
    if Q.mass < 29.644699859619 and Q.phi_1 > -0.058901977539:
        z += -0.32561481276127324 * (29.644699859619 - Q.mass) * (Q.phi_1 - -0.058901977539)
    if Q.planar_flow < 0.148419710734 and Q.pt_1 > 159.25:
        z += -0.014696974690480147 * (0.148419710734 - Q.planar_flow) * (Q.pt_1 - 159.25)
    if Q.width < 0.004372139331 and Q.n_dr_0p1_0p2 > 1.0:
        z += -131.6053538056738 * (0.004372139331 - Q.width) * (Q.n_dr_0p1_0p2 - 1.0)
    if Q.z_dr_0_0p05 > 0.847731333971 and Q.n_dr_0p2_0p4 > 2.0:
        z += -9.696878606593131 * (Q.z_dr_0_0p05 - 0.847731333971) * (Q.n_dr_0p2_0p4 - 2.0)
    if Q.width < 0.008678044951 and Q.phi_1 < 0.03088684082:
        z += -546.8731182197633 * (0.008678044951 - Q.width) * (0.03088684082 - Q.phi_1)
    if Q.z_dr_0p05_0p1 > 0.846033477783 and Q.z_3rd < 0.09921980761:
        z += 89.8448563399111 * (Q.z_dr_0p05_0p1 - 0.846033477783) * (0.09921980761 - Q.z_3rd)
    if Q.girth2_top5 < 0.00832969537 and Q.eta_2 > 0.096557617188:
        z += 2118.9773634118283 * (0.00832969537 - Q.girth2_top5) * (Q.eta_2 - 0.096557617188)
    if Q.sum_pt_top5 > 687.4375 and Q.dr_4 < 0.063364507347:
        z += -0.08487495477180573 * (Q.sum_pt_top5 - 687.4375) * (0.063364507347 - Q.dr_4)
    if Q.lam1 < 0.00543336053 and Q.n_dr_0p2_0p4 < 2.0:
        z += -190.62981472523109 * (0.00543336053 - Q.lam1) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.mass < 56.920347213745 and Q.dr_2 > 0.022704921512:
        z += -0.06276697541574094 * (56.920347213745 - Q.mass) * (Q.dr_2 - 0.022704921512)
    if Q.girth2 < 0.018827652745 and Q.n_dr_0p2_0p4 < 2.0:
        z += 19.39933411719187 * (0.018827652745 - Q.girth2) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.mass_over_sum_pt_sq < 0.008174660116 and Q.m01 > 28.789663234961:
        z += -15.596618536625385 * (0.008174660116 - Q.mass_over_sum_pt_sq) * (Q.m01 - 28.789663234961)
    if Q.girth < 0.087236513197 and Q.m01 > 28.789663234961:
        z += 0.594369398019353 * (0.087236513197 - Q.girth) * (Q.m01 - 28.789663234961)
    if Q.lam1 < 0.00543336053 and Q.mass_top3 > 16.899120053094:
        z += -16.063833620627804 * (0.00543336053 - Q.lam1) * (Q.mass_top3 - 16.899120053094)
    if Q.mass_over_sum_pt_sq < 0.008174660116 and Q.n_pt_above_50 < 8.0:
        z += 4.364860011950981 * (0.008174660116 - Q.mass_over_sum_pt_sq) * (8.0 - Q.n_pt_above_50)
    if Q.planar_flow < 0.148419710734 and Q.z_top5 < 0.814386516809:
        z += 19.974763687181138 * (0.148419710734 - Q.planar_flow) * (0.814386516809 - Q.z_top5)
    if Q.log_sum_pt > 6.638338705138 and Q.dr_3 < 0.078464230803:
        z += 25.90532850025855 * (Q.log_sum_pt - 6.638338705138) * (0.078464230803 - Q.dr_3)
    if Q.mass < 29.644699859619 and Q.dr_0 < 0.111955475493:
        z += 0.7258896760608877 * (29.644699859619 - Q.mass) * (0.111955475493 - Q.dr_0)
    if Q.centroid_offset < 0.031170772021 and Q.dr_0 < 0.046494648555:
        z += -409.8438234840463 * (0.031170772021 - Q.centroid_offset) * (0.046494648555 - Q.dr_0)
    if Q.mass < 56.920347213745 and Q.dr_4 > 0.04181499946:
        z += -0.060642091033628276 * (56.920347213745 - Q.mass) * (Q.dr_4 - 0.04181499946)
    if Q.D2 > 3.885568320751 and Q.phi_2 < -0.009959030151:
        z += 3.614549018599316 * (Q.D2 - 3.885568320751) * (-0.009959030151 - Q.phi_2)
    if Q.z_dr_0p05_0p1 > 0.846033477783 and Q.dr_7 < 0.007333702861:
        z += -2459.6458950113906 * (Q.z_dr_0p05_0p1 - 0.846033477783) * (0.007333702861 - Q.dr_7)
    if Q.girth2_top3 < 0.003952581551 and Q.m01 > 28.789663234961:
        z += 37.49576714245004 * (0.003952581551 - Q.girth2_top3) * (Q.m01 - 28.789663234961)
    if Q.planar_flow < 0.012569162668 and Q.dr_7 < 0.082575402011:
        z += 523.1901399084213 * (0.012569162668 - Q.planar_flow) * (0.082575402011 - Q.dr_7)
    if Q.mass < 29.644699859619 and Q.dr_7 > 0.124275510792:
        z += -0.42821161047638157 * (29.644699859619 - Q.mass) * (Q.dr_7 - 0.124275510792)
    if Q.sum_pt > 901.59375 and Q.dr_7 < 0.107835464377:
        z += 0.0366118660920165 * (Q.sum_pt - 901.59375) * (0.107835464377 - Q.dr_7)
    if Q.sum_pt_top5 > 687.4375 and Q.dr_7 < 0.093979107928:
        z += -0.0398248395386247 * (Q.sum_pt_top5 - 687.4375) * (0.093979107928 - Q.dr_7)
    if Q.z_dr_0_0p05 > 0.847731333971 and Q.tau21 < 0.112473037094:
        z += 82.17177077005304 * (Q.z_dr_0_0p05 - 0.847731333971) * (0.112473037094 - Q.tau21)
    if Q.D2 > 3.885568320751 and Q.mean_eta > 0.006823012256:
        z += -16.472979045001864 * (Q.D2 - 3.885568320751) * (Q.mean_eta - 0.006823012256)
    if Q.sum_pt_top5 > 687.4375 and Q.phi_0 < -0.078189086914:
        z += 0.08677210440328054 * (Q.sum_pt_top5 - 687.4375) * (-0.078189086914 - Q.phi_0)
    if Q.girth2_top5 < 0.000657050184 and Q.dr_7 < 0.222994708167:
        z += 6273.0787961734495 * (0.000657050184 - Q.girth2_top5) * (0.222994708167 - Q.dr_7)
    if Q.girth2_top5 < 0.000657050184 and Q.dr_6 > 0.120255619185:
        z += -2848.289260139974 * (0.000657050184 - Q.girth2_top5) * (Q.dr_6 - 0.120255619185)
    if Q.girth2 < 0.018827652745 and Q.phi_2 < -0.096621704102:
        z += -65.75741972633176 * (0.018827652745 - Q.girth2) * (-0.096621704102 - Q.phi_2)
    if Q.width < 0.004372139331 and Q.dr_7 > 0.007333702861:
        z += 939.7722551920926 * (0.004372139331 - Q.width) * (Q.dr_7 - 0.007333702861)
    if Q.girth2_top3 < 0.003952581551 and Q.dr_7 < 0.107835464377:
        z += 660.3171350818059 * (0.003952581551 - Q.girth2_top3) * (0.107835464377 - Q.dr_7)
    return max(0.0, z)


def neuron_1(Q):
    z = 0.5023479892410638
    if Q.lam1 < 0.008375572068:
        z += 41.196776070523846 * Q.lam1 - 0.3450465669479303
    if Q.lam1 >= 0.012003726523:
        z += -0.05683038723327627 * Q.lam1 + 0.0006821764265444389
    if 34.53125 <= Q.pt_7 < 53.4375:
        z += 0.15323084107118967 * Q.pt_7 - 5.2912524807395185
    if Q.pt_7 >= 53.4375:
        z += 0.011950791899041469 * Q.pt_7 + 2.2584001468971513
    if Q.e2 < 0.032346998155:
        z += 3.4292873245444104 * Q.e2 - 0.12194858568302964
    if 0.032346998155 <= Q.e2 < 0.035560912266:
        z += -10.448223755118825 * Q.e2 + 0.32694723960682914
    if Q.e2 >= 0.035560912266:
        z += -13.877511079663236 * Q.e2 + 0.4488958252898588
    if 6.377722943814 <= Q.log_sum_pt < 6.572937922293:
        z += 1.8736398652651647 * Q.log_sum_pt - 11.949555957146211
    if 6.572937922293 <= Q.log_sum_pt < 6.638338705138:
        z += 4.920574622152042 * Q.log_sum_pt - 31.976868967440573
    if Q.log_sum_pt >= 6.638338705138:
        z += 10.372864068993902 * Q.log_sum_pt - 68.17101303402634
    if Q.z_7 < 0.043044721986:
        z += 78.51781961989279 * Q.z_7 - 4.1297372892581965
    if 0.043044721986 <= Q.z_7 < 0.055577157257:
        z += 59.841487831851666 * Q.z_7 - 3.325819779723672
    if Q.girth < 0.076081777364:
        z += -8.713929663180945 * Q.girth + 0.6629712565996881
    if Q.mass < 49.668099212646:
        z += -0.018634189741304374 * Q.mass + 0.8476009411739291
    if 49.668099212646 <= Q.mass < 53.332374954224:
        z += 0.02126582417372591 * Q.mass - 1.134156908543751
    if Q.width < 0.008678044951:
        z += 398.558679010235 * Q.width - 3.4587101320619995
    if Q.planar_flow < 0.083662731125:
        z += -3.1316374567330976 * Q.planar_flow + 0.26200134252364
    if Q.tau21 < 0.197783735394:
        z += -5.8747528689278266 * Q.tau21 + 1.1619305669331634
    if Q.e2_sq < 0.008168570676:
        z += -284.56636054850867 * Q.e2_sq + 2.3245004281525916
    if Q.C2 < 0.035786485299:
        z += -10.770101571522275 * Q.C2 + 0.31736903248228526
    if 0.035786485299 <= Q.C2 < 0.042322802544:
        z += 10.411833839275857 * Q.C2 - 0.44065798770060954
    if Q.LHA < 0.266912960293:
        z += -2.607822364186177 * Q.LHA + 0.6939805800026937
    if 0.266912960293 <= Q.LHA < 0.312727471086:
        z += 0.6374530902203333 * Q.LHA - 0.1722254984991587
    if 0.312727471086 <= Q.LHA < 0.346713497427:
        z += 6.8219546392901975 * Q.LHA - 2.106289027867227
    if Q.LHA >= 0.346713497427:
        z += 3.24527545440651 * Q.LHA - 0.8662060785018524
    if Q.mass_over_sum_pt >= 0.054892207095:
        z += 3.4736534660696634 * Q.mass_over_sum_pt - 0.1906765054357605
    if Q.n_pt_above_50 >= 6.0:
        z += 0.08862240314192604 * Q.n_pt_above_50 - 0.5317344188515563
    if Q.max_dr < 0.046566883102:
        z += 9.158543444590123 * Q.max_dr - 1.2190061570110386
    if 0.046566883102 <= Q.max_dr < 0.093110798299:
        z += 5.460206808254043 * Q.max_dr - 1.0467861471949327
    if 0.093110798299 <= Q.max_dr < 0.250761204958:
        z += 3.415036750049694 * Q.max_dr - 0.8563587304183135
    if Q.mass_top5 < 6.366664058612:
        z += 0.031465496052987874 * Q.mass_top5 - 0.20033024280695563
    if Q.girth2_top5 < 0.024419631481:
        z += -26.18837883960441 * Q.girth2_top5 + 0.6395105603479582
    if Q.sum_pt_top5 >= 579.875:
        z += -0.003452367291174596 * Q.sum_pt_top5 + 2.001941482969869
    if Q.dr_6 >= 0.120255619185:
        z += -0.7114348623508704 * Q.dr_6 + 0.08555403988179916
    if Q.z_dr_0p1_0p2 < 0.045106684603:
        z += -2.5943778100299824 * Q.z_dr_0p1_0p2 + 0.11702378161804426
    if Q.lam1 < 0.008375572068 and Q.centroid_offset > 0.02076709205:
        z += 10981.044115281158 * (0.008375572068 - Q.lam1) * (Q.centroid_offset - 0.02076709205)
    if Q.lam1 < 0.008375572068 and Q.z_7 > 0.039784489456:
        z += -662.6898841324436 * (0.008375572068 - Q.lam1) * (Q.z_7 - 0.039784489456)
    if Q.pt_7 > 34.53125 and Q.mass < 91.19:
        z += -0.0020415039558025483 * (Q.pt_7 - 34.53125) * (91.19 - Q.mass)
    if Q.log_sum_pt > 6.377722943814 and Q.z_dr_0_0p05 < 0.90085350275:
        z += 2.8247817306504155 * (Q.log_sum_pt - 6.377722943814) * (0.90085350275 - Q.z_dr_0_0p05)
    if Q.lam1 < 0.008375572068 and Q.lam2 < 0.000537286005:
        z += -161171.72028872164 * (0.008375572068 - Q.lam1) * (0.000537286005 - Q.lam2)
    if Q.z_7 < 0.055577157257 and Q.lam2 < 0.003408388935:
        z += -2062.258696725485 * (0.055577157257 - Q.z_7) * (0.003408388935 - Q.lam2)
    if Q.pt_7 > 34.53125 and Q.C2 > 0.004836016125:
        z += -0.25738849119057405 * (Q.pt_7 - 34.53125) * (Q.C2 - 0.004836016125)
    if Q.pt_7 > 34.53125 and Q.centroid_offset > 0.014379521101:
        z += 0.6165543669069189 * (Q.pt_7 - 34.53125) * (Q.centroid_offset - 0.014379521101)
    if Q.log_sum_pt > 6.377722943814 and Q.centroid_offset < 0.023554160423:
        z += -53.470122082673925 * (Q.log_sum_pt - 6.377722943814) * (0.023554160423 - Q.centroid_offset)
    if Q.pt_7 > 53.4375 and Q.mass_top3 < 45.595:
        z += 0.008227545227406763 * (Q.pt_7 - 53.4375) * (45.595 - Q.mass_top3)
    if Q.log_sum_pt > 6.377722943814 and Q.max_dr < 0.197968879342:
        z += 2.1396138221096006 * (Q.log_sum_pt - 6.377722943814) * (0.197968879342 - Q.max_dr)
    if Q.pt_7 > 34.53125 and Q.pt_6 < 52.90625:
        z += -0.0027744876285491493 * (Q.pt_7 - 34.53125) * (52.90625 - Q.pt_6)
    if Q.z_7 < 0.055577157257 and Q.dr01 > 0.055953954317:
        z += 40.995638654129216 * (0.055577157257 - Q.z_7) * (Q.dr01 - 0.055953954317)
    if Q.pt_7 > 53.4375 and Q.tau21 < 0.553068161011:
        z += -0.10584168502919855 * (Q.pt_7 - 53.4375) * (0.553068161011 - Q.tau21)
    if Q.log_sum_pt > 6.572937922293 and Q.D2 < 1.232133567333:
        z += -0.17751529055834858 * (Q.log_sum_pt - 6.572937922293) * (1.232133567333 - Q.D2)
    if Q.width < 0.008678044951 and Q.planar_flow < 0.083662731125:
        z += 567.5960110883861 * (0.008678044951 - Q.width) * (0.083662731125 - Q.planar_flow)
    if Q.e2 < 0.035560912266 and Q.eccentricity > 0.978160776925:
        z += 2635.990703701169 * (0.035560912266 - Q.e2) * (Q.eccentricity - 0.978160776925)
    if Q.z_7 < 0.055577157257 and Q.tau21 < 0.163363117725:
        z += 60.68017390655875 * (0.055577157257 - Q.z_7) * (0.163363117725 - Q.tau21)
    if Q.z_7 < 0.055577157257 and Q.C2 < 0.042322802544:
        z += 191.1632424885269 * (0.055577157257 - Q.z_7) * (0.042322802544 - Q.C2)
    if Q.e2 < 0.035560912266 and Q.mean_phi > 0.001618889696:
        z += -405.9320908871265 * (0.035560912266 - Q.e2) * (Q.mean_phi - 0.001618889696)
    if Q.pt_7 > 34.53125 and Q.max_dr < 0.080507021025:
        z += 0.8843058533821022 * (Q.pt_7 - 34.53125) * (0.080507021025 - Q.max_dr)
    if Q.pt_7 > 53.4375 and Q.mass_top3 < 32.617988451746:
        z += -0.007697096664287528 * (Q.pt_7 - 53.4375) * (32.617988451746 - Q.mass_top3)
    if Q.log_sum_pt > 6.572937922293 and Q.max_dr < 0.290267042816:
        z += -9.789789830223526 * (Q.log_sum_pt - 6.572937922293) * (0.290267042816 - Q.max_dr)
    if Q.tau21 < 0.197783735394 and Q.pt_6 < 50.25:
        z += -0.18564054174021294 * (0.197783735394 - Q.tau21) * (50.25 - Q.pt_6)
    if Q.log_sum_pt > 6.572937922293 and Q.girth2_top3 < 0.006756161242:
        z += -264.1610974566012 * (Q.log_sum_pt - 6.572937922293) * (0.006756161242 - Q.girth2_top3)
    if Q.z_7 < 0.055577157257 and Q.girth2_top3 < 0.007929074034:
        z += 4379.933034219268 * (0.055577157257 - Q.z_7) * (0.007929074034 - Q.girth2_top3)
    if Q.tau21 < 0.197783735394 and Q.lam2 < 0.000194798295:
        z += -15032.834040431828 * (0.197783735394 - Q.tau21) * (0.000194798295 - Q.lam2)
    if Q.log_sum_pt > 6.572937922293 and Q.lam2 < 0.001130644719:
        z += 2286.3111360766848 * (Q.log_sum_pt - 6.572937922293) * (0.001130644719 - Q.lam2)
    if Q.planar_flow < 0.083662731125 and Q.tau32 < 0.269169217348:
        z += -15.895378915034257 * (0.083662731125 - Q.planar_flow) * (0.269169217348 - Q.tau32)
    if Q.mass < 53.332374954224 and Q.mass_top3 > 23.663861485439:
        z += 0.005817810217195074 * (53.332374954224 - Q.mass) * (Q.mass_top3 - 23.663861485439)
    if Q.log_sum_pt > 6.572937922293 and Q.n_dr_0p1_0p2 > 1.0:
        z += 0.3043110665198583 * (Q.log_sum_pt - 6.572937922293) * (Q.n_dr_0p1_0p2 - 1.0)
    if Q.LHA < 0.346713497427 and Q.planar_flow < 0.083662731125:
        z += -50.479275056930476 * (0.346713497427 - Q.LHA) * (0.083662731125 - Q.planar_flow)
    if Q.lam1 < 0.008375572068 and Q.n_pt_above_50 > 6.0:
        z += -232.0873068921634 * (0.008375572068 - Q.lam1) * (Q.n_pt_above_50 - 6.0)
    if Q.e2_sq < 0.008168570676 and Q.planar_flow < 0.083662731125:
        z += -2767.465937379193 * (0.008168570676 - Q.e2_sq) * (0.083662731125 - Q.planar_flow)
    if Q.e2_sq < 0.008168570676 and Q.n_pt_above_50 > 6.0:
        z += 152.0181895770776 * (0.008168570676 - Q.e2_sq) * (Q.n_pt_above_50 - 6.0)
    if Q.log_sum_pt > 6.572937922293 and Q.planar_flow < 0.033200121667:
        z += 28.177854172541117 * (Q.log_sum_pt - 6.572937922293) * (0.033200121667 - Q.planar_flow)
    if Q.log_sum_pt > 6.572937922293 and Q.n_pt_above_50 > 7.0:
        z += -2.7150352909375215 * (Q.log_sum_pt - 6.572937922293) * (Q.n_pt_above_50 - 7.0)
    if Q.log_sum_pt > 6.377722943814 and Q.n_pt_above_50 > 7.0:
        z += 1.216152423641688 * (Q.log_sum_pt - 6.377722943814) * (Q.n_pt_above_50 - 7.0)
    if Q.planar_flow < 0.083662731125 and Q.mean_eta < 6.2888237e-05:
        z += 61.1911545612179 * (0.083662731125 - Q.planar_flow) * (6.2888237e-05 - Q.mean_eta)
    if Q.e2 > 0.032346998155 and Q.tau32 < 0.641386964917:
        z += -2.1666982168744653 * (Q.e2 - 0.032346998155) * (0.641386964917 - Q.tau32)
    if Q.e2 > 0.032346998155 and Q.pt_1 < 80.8125:
        z += 0.1832710376693285 * (Q.e2 - 0.032346998155) * (80.8125 - Q.pt_1)
    if Q.C2 < 0.042322802544 and Q.tau21 < 0.197783735394:
        z += -154.41219806303238 * (0.042322802544 - Q.C2) * (0.197783735394 - Q.tau21)
    if Q.planar_flow < 0.083662731125 and Q.tau21 < 0.112473037094:
        z += 74.52202775524819 * (0.083662731125 - Q.planar_flow) * (0.112473037094 - Q.tau21)
    if Q.girth < 0.076081777364 and Q.tau21 < 0.077540414408:
        z += -366.0253307303954 * (0.076081777364 - Q.girth) * (0.077540414408 - Q.tau21)
    if Q.mass < 49.668099212646 and Q.tau21 < 0.197783735394:
        z += 0.15364168662927113 * (49.668099212646 - Q.mass) * (0.197783735394 - Q.tau21)
    if Q.pt_7 > 53.4375 and Q.phi_3 < -0.100952148438:
        z += -0.4714164445245217 * (Q.pt_7 - 53.4375) * (-0.100952148438 - Q.phi_3)
    if Q.mass_over_sum_pt > 0.054892207095 and Q.pt_3 > 74.5625:
        z += 0.0616054837446427 * (Q.mass_over_sum_pt - 0.054892207095) * (Q.pt_3 - 74.5625)
    if Q.tau21 < 0.197783735394 and Q.n_pt_above_50 > 2.0:
        z += -0.3788576357837883 * (0.197783735394 - Q.tau21) * (Q.n_pt_above_50 - 2.0)
    if Q.C2 < 0.035786485299 and Q.phi_0 > -0.054077148438:
        z += 34.282488920953796 * (0.035786485299 - Q.C2) * (Q.phi_0 - -0.054077148438)
    if Q.z_7 < 0.043044721986 and Q.phi_1 < -0.042755126953:
        z += -52.97888462410941 * (0.043044721986 - Q.z_7) * (-0.042755126953 - Q.phi_1)
    if Q.n_pt_above_50 > 6.0 and Q.tau32 < 0.159295958281:
        z += -1.949232647071085 * (Q.n_pt_above_50 - 6.0) * (0.159295958281 - Q.tau32)
    if Q.z_7 < 0.055577157257 and Q.dr_5 > 0.086515665416:
        z += -96.60549151657796 * (0.055577157257 - Q.z_7) * (Q.dr_5 - 0.086515665416)
    if Q.log_sum_pt > 6.638338705138 and Q.dr_5 > 0.075300493619:
        z += 12.843070668407563 * (Q.log_sum_pt - 6.638338705138) * (Q.dr_5 - 0.075300493619)
    if Q.LHA > 0.266912960293 and Q.lam2 < 0.003408388935:
        z += 1635.767444795055 * (Q.LHA - 0.266912960293) * (0.003408388935 - Q.lam2)
    if Q.n_pt_above_50 > 6.0 and Q.dr_5 > 0.099455629452:
        z += -0.8653403129033848 * (Q.n_pt_above_50 - 6.0) * (Q.dr_5 - 0.099455629452)
    if Q.pt_7 > 34.53125 and Q.dr_5 < 0.099455629452:
        z += -0.11252539474662626 * (Q.pt_7 - 34.53125) * (0.099455629452 - Q.dr_5)
    if Q.z_7 < 0.043044721986 and Q.dr_7 < 0.222994708167:
        z += 42.710577135811945 * (0.043044721986 - Q.z_7) * (0.222994708167 - Q.dr_7)
    if Q.n_pt_above_50 > 6.0 and Q.girth2_top2 < 0.001056655216:
        z += 312.23655325176804 * (Q.n_pt_above_50 - 6.0) * (0.001056655216 - Q.girth2_top2)
    if Q.log_sum_pt > 6.377722943814 and Q.girth2_top2 < 0.001864147842:
        z += -1257.0555055656857 * (Q.log_sum_pt - 6.377722943814) * (0.001864147842 - Q.girth2_top2)
    if Q.sum_pt_top5 > 579.875 and Q.girth2_top2 < 0.002412890926:
        z += 1.2483872940256333 * (Q.sum_pt_top5 - 579.875) * (0.002412890926 - Q.girth2_top2)
    if Q.mass < 49.668099212646 and Q.mean_phi2 > 0.004331280361:
        z += -1.6960710552481828 * (49.668099212646 - Q.mass) * (Q.mean_phi2 - 0.004331280361)
    if Q.z_7 < 0.055577157257 and Q.girth2_top2 < 0.0140332421:
        z += 2433.4495946268776 * (0.055577157257 - Q.z_7) * (0.0140332421 - Q.girth2_top2)
    if Q.log_sum_pt > 6.638338705138 and Q.girth2_top3 < 0.007929074034:
        z += -674.5387483968999 * (Q.log_sum_pt - 6.638338705138) * (0.007929074034 - Q.girth2_top3)
    if Q.lam1 > 0.012003726523 and Q.eccentricity > 0.872657364787:
        z += -257.0913010422486 * (Q.lam1 - 0.012003726523) * (Q.eccentricity - 0.872657364787)
    if Q.n_pt_above_50 > 6.0 and Q.z_dr_0p2_0p4 < 0.1009733513:
        z += 1.8206218074110438 * (Q.n_pt_above_50 - 6.0) * (0.1009733513 - Q.z_dr_0p2_0p4)
    if Q.z_7 < 0.043044721986 and Q.z_dr_0p05_0p1 > 0.163898047805:
        z += -27.39208392355323 * (0.043044721986 - Q.z_7) * (Q.z_dr_0p05_0p1 - 0.163898047805)
    if Q.max_dr < 0.250761204958 and Q.z_dr_0p05_0p1 > 0.088784894347:
        z += -1.6913264149525276 * (0.250761204958 - Q.max_dr) * (Q.z_dr_0p05_0p1 - 0.088784894347)
    return max(0.0, z)


def neuron_2(Q):
    z = 2.12760954023028
    if Q.mass < 8.379955863953:
        z += 0.08318153969247732 * Q.mass - 1.7953805206113809
    if 8.379955863953 <= Q.mass < 36.229410171509:
        z += 0.06658411893812932 * Q.mass - 1.656294867234487
    if 36.229410171509 <= Q.mass < 69.611351776123:
        z += -0.02264722938042185 * Q.mass + 1.5765042511550937
    if Q.log_sum_pt < 6.267538488641:
        z += -3.0688164564495173 * Q.log_sum_pt + 19.789209987471924
    if 6.267538488641 <= Q.log_sum_pt < 6.464150123592:
        z += -1.4683506945044291 * Q.log_sum_pt + 9.75822922472894
    if 6.464150123592 <= Q.log_sum_pt < 6.572937922293:
        z += 1.151971722933045 * Q.log_sum_pt - 7.179928253800394
    if 6.572937922293 <= Q.log_sum_pt < 6.638338705138:
        z += 3.0816554937501026 * Q.log_sum_pt - 19.863619889037185
    if 6.638338705138 <= Q.log_sum_pt < 6.804164030582:
        z += 1.6004657619450882 * Q.log_sum_pt - 10.030980762742985
    if 6.804164030582 <= Q.log_sum_pt < 6.842716632804:
        z += 10.022561087647773 * Q.log_sum_pt - 67.33629884002198
    if 6.842716632804 <= Q.log_sum_pt < 6.896095378249:
        z += 11.064688828980884 * Q.log_sum_pt - 74.46728366914853
    if Q.log_sum_pt >= 6.896095378249:
        z += 18.59099074209866 * Q.log_sum_pt - 126.36937950750664
    if Q.z_7 < 0.016858545121:
        z += 284.3955338423145 * Q.z_7 - 4.993048015084125
    if 0.016858545121 <= Q.z_7 < 0.028070914944:
        z += 17.708395167745074 * Q.z_7 - 0.49709085454851254
    if Q.z_7 >= 0.046240320761:
        z += -20.88207334419326 * Q.z_7 + 0.9655937695902242
    if Q.lam1 < 0.003377388461:
        z += -414.703649345711 * Q.lam1 + 1.9258096099920174
    if 0.003377388461 <= Q.lam1 < 0.005954149834:
        z += -203.81952922003182 * Q.lam1 + 1.2135720160714105
    if Q.width < 9.1213921e-05:
        z += 15016.230564890073 * Q.width - 1.0343641098563476
    if 9.1213921e-05 <= Q.width < 0.000172198326:
        z += -4140.6139689156325 * Q.width + 0.713006794059488
    if Q.pt_7 < 15.55390625:
        z += -0.3205235988139066 * Q.pt_7 + 3.905172805286086
    if 15.55390625 <= Q.pt_7 < 20.125:
        z += -0.04944303819593188 * Q.pt_7 - 0.3111888207633342
    if 20.125 <= Q.pt_7 < 30.484375:
        z += 0.024212677164541674 * Q.pt_7 - 1.7935100923928644
    if 30.484375 <= Q.pt_7 < 43.5:
        z += 0.08072801150946365 * Q.pt_7 - 3.5163447378138457
    if 43.5 <= Q.pt_7 < 53.4375:
        z += 0.13100676938746805 * Q.pt_7 - 5.703470705507037
    if Q.pt_7 >= 53.4375:
        z += 0.05651533434492197 * Q.pt_7 - 1.7228346454209809
    if Q.LHA >= 0.111565049159:
        z += -6.62349303600924 * Q.LHA + 0.738950326166665
    if Q.planar_flow < 0.694781820497:
        z += 0.734470133217899 * Q.planar_flow - 0.5102964962578059
    if Q.pt_6 < 56.53125:
        z += 0.015912379693153844 * Q.pt_6 - 0.8995467145286032
    if Q.sum_pt_top5 < 687.4375:
        z += 0.004106103939193417 * Q.sum_pt_top5 - 2.822689826699275
    if 752.1 <= Q.sum_pt_top5 < 839.9546875:
        z += -0.0006159138338261982 * Q.sum_pt_top5 + 0.4632287944206837
    if Q.sum_pt_top5 >= 839.9546875:
        z += -0.010766640925325754 * Q.sum_pt_top5 + 8.989379596458976
    if Q.sum_pt < 788.4484375:
        z += -0.01188558516696503 * Q.sum_pt + 9.371171053666753
    if Q.girth2 < 4.8108519e-05:
        z += 31540.77976033509 * Q.girth2 - 1.5173802023748961
    if Q.tau21 < 0.335550022125:
        z += 0.7013571156139449 * Q.tau21 - 0.23534039566178538
    if Q.girth2_top2 < 3.8495183e-05:
        z += -6008.94144305725 * Q.girth2_top2 + 0.2313153004867729
    if Q.max_dr < 0.15984864831:
        z += -3.1409039195687 * Q.max_dr + 0.5020692460146376
    if Q.mass_over_sum_pt_sq < 0.011660904657:
        z += -34.60822968159107 * Q.mass_over_sum_pt_sq + 0.4035632666645909
    if Q.dr_5 < 0.021648628542:
        z += -63.46955588634529 * Q.dr_5 + 1.3740288391091988
    if Q.mass_over_sum_pt < 0.011099841777:
        z += -55.47479048935749 * Q.mass_over_sum_pt + 0.6157613970440925
    if Q.z_dr_0p1_0p2 < 0.20502409339:
        z += 0.3385176892199979 * Q.z_dr_0p1_0p2 - 0.06940428232880785
    if Q.mass < 69.611351776123 and Q.z_7 < 0.068101508468:
        z += -0.4047190133275768 * (69.611351776123 - Q.mass) * (0.068101508468 - Q.z_7)
    if Q.mass < 69.611351776123 and Q.centroid_offset > 0.010960638421:
        z += -0.5761423126742891 * (69.611351776123 - Q.mass) * (Q.centroid_offset - 0.010960638421)
    if Q.pt_7 > 30.484375 and Q.dr_0 > 0.031288303462:
        z += -0.13046462906102016 * (Q.pt_7 - 30.484375) * (Q.dr_0 - 0.031288303462)
    if Q.pt_7 > 30.484375 and Q.C2 < 0.051192347892:
        z += -0.8312371879342426 * (Q.pt_7 - 30.484375) * (0.051192347892 - Q.C2)
    if Q.z_7 < 0.028070914944 and Q.width < 0.00752008842:
        z += -10478.319794841698 * (0.028070914944 - Q.z_7) * (0.00752008842 - Q.width)
    if Q.lam1 < 0.005954149834 and Q.max_dr > 0.080507021025:
        z += -1180.0059419283727 * (0.005954149834 - Q.lam1) * (Q.max_dr - 0.080507021025)
    if Q.log_sum_pt > 6.842716632804 and Q.dr01 > 0.141033647649:
        z += 15.812651145158899 * (Q.log_sum_pt - 6.842716632804) * (Q.dr01 - 0.141033647649)
    if Q.pt_6 < 56.53125 and Q.m012 > 32.617988451746:
        z += 0.0005784275382225146 * (56.53125 - Q.pt_6) * (Q.m012 - 32.617988451746)
    if Q.mass < 36.229410171509 and Q.lam2 < 0.001130644719:
        z += 40.845144242420645 * (36.229410171509 - Q.mass) * (0.001130644719 - Q.lam2)
    if Q.pt_7 > 30.484375 and Q.max_dr > 0.093110798299:
        z += -0.11300566489192826 * (Q.pt_7 - 30.484375) * (Q.max_dr - 0.093110798299)
    if Q.log_sum_pt > 6.842716632804 and Q.n_pt_above_50 > 5.0:
        z += -4.075269694722889 * (Q.log_sum_pt - 6.842716632804) * (Q.n_pt_above_50 - 5.0)
    if Q.mass < 36.229410171509 and Q.pt_4 < 55.65625:
        z += 0.0004626138080670028 * (36.229410171509 - Q.mass) * (55.65625 - Q.pt_4)
    if Q.lam1 < 0.003377388461 and Q.centroid_offset < 0.006789738266:
        z += -20390.23793642491 * (0.003377388461 - Q.lam1) * (0.006789738266 - Q.centroid_offset)
    if Q.mass < 8.379955863953 and Q.centroid_offset < 0.010960638421:
        z += 38.420334676980694 * (8.379955863953 - Q.mass) * (0.010960638421 - Q.centroid_offset)
    if Q.pt_7 > 30.484375 and Q.centroid_offset > 0.012587644117:
        z += -0.5177386154802412 * (Q.pt_7 - 30.484375) * (Q.centroid_offset - 0.012587644117)
    if Q.sum_pt_top5 > 839.9546875 and Q.dr_7 < 0.04881348081:
        z += 0.0616569532048743 * (Q.sum_pt_top5 - 839.9546875) * (0.04881348081 - Q.dr_7)
    if Q.width < 9.1213921e-05 and Q.pt_2 < 154.25:
        z += 110.79101749424898 * (9.1213921e-05 - Q.width) * (154.25 - Q.pt_2)
    if Q.pt_6 < 56.53125 and Q.lam2 > 0.000306123359:
        z += -1.731357015584308 * (56.53125 - Q.pt_6) * (Q.lam2 - 0.000306123359)
    if Q.log_sum_pt > 6.842716632804 and Q.z_3rd < 0.073680565134:
        z += -62.78107968353899 * (Q.log_sum_pt - 6.842716632804) * (0.073680565134 - Q.z_3rd)
    if Q.mass < 8.379955863953 and Q.z_2 < 0.181856399189:
        z += -0.4593698420272858 * (8.379955863953 - Q.mass) * (0.181856399189 - Q.z_2)
    if Q.mass < 36.229410171509 and Q.mean_phi < -0.003096654534:
        z += 0.29475497994280886 * (36.229410171509 - Q.mass) * (-0.003096654534 - Q.mean_phi)
    if Q.log_sum_pt < 6.464150123592 and Q.eta_0 > 0.029803466797:
        z += 4.121802121716371 * (6.464150123592 - Q.log_sum_pt) * (Q.eta_0 - 0.029803466797)
    if Q.pt_7 > 30.484375 and Q.z_dr_0p05_0p1 < 0.750909513235:
        z += 0.01584203505444748 * (Q.pt_7 - 30.484375) * (0.750909513235 - Q.z_dr_0p05_0p1)
    if Q.mass < 69.611351776123 and Q.max_pair_mass > 13.047927274731:
        z += -0.0006849701626379101 * (69.611351776123 - Q.mass) * (Q.max_pair_mass - 13.047927274731)
    if Q.log_sum_pt > 6.267538488641 and Q.phi_0 < 0.004838562012:
        z += 3.339947536130097 * (Q.log_sum_pt - 6.267538488641) * (0.004838562012 - Q.phi_0)
    if Q.log_sum_pt < 6.572937922293 and Q.eccentricity > 0.779212655895:
        z += 3.7858715317411225 * (6.572937922293 - Q.log_sum_pt) * (Q.eccentricity - 0.779212655895)
    if Q.width < 0.000172198326 and Q.dr_7 < 0.222994708167:
        z += -53424.13645950347 * (0.000172198326 - Q.width) * (0.222994708167 - Q.dr_7)
    if Q.log_sum_pt < 6.464150123592 and Q.dr_7 < 0.072549472237:
        z += -17.768077835985196 * (6.464150123592 - Q.log_sum_pt) * (0.072549472237 - Q.dr_7)
    if Q.sum_pt < 788.4484375 and Q.dr_7 < 0.063966271204:
        z += 0.04097022922633187 * (788.4484375 - Q.sum_pt) * (0.063966271204 - Q.dr_7)
    if Q.z_7 > 0.046240320761 and Q.dr_7 < 0.063966271204:
        z += -323.4216636039674 * (Q.z_7 - 0.046240320761) * (0.063966271204 - Q.dr_7)
    if Q.pt_7 > 30.484375 and Q.dr_7 < 0.093979107928:
        z += 0.17689213531411951 * (Q.pt_7 - 30.484375) * (0.093979107928 - Q.dr_7)
    if Q.log_sum_pt > 6.896095378249 and Q.z_0 < 0.181012575092:
        z += -2354.026963840386 * (Q.log_sum_pt - 6.896095378249) * (0.181012575092 - Q.z_0)
    if Q.log_sum_pt > 6.896095378249 and Q.phi_5 < -0.052006530762:
        z += -43.741169997531614 * (Q.log_sum_pt - 6.896095378249) * (-0.052006530762 - Q.phi_5)
    if Q.log_sum_pt > 6.267538488641 and Q.dr_5 < 0.021648628542:
        z += -136.26932282841153 * (Q.log_sum_pt - 6.267538488641) * (0.021648628542 - Q.dr_5)
    if Q.pt_7 < 15.55390625 and Q.n_pt_above_10 < 8.0:
        z += 0.007939429743601067 * (15.55390625 - Q.pt_7) * (8.0 - Q.n_pt_above_10)
    if Q.log_sum_pt < 6.572937922293 and Q.dr_5 < 0.021648628542:
        z += -152.451470805107 * (6.572937922293 - Q.log_sum_pt) * (0.021648628542 - Q.dr_5)
    if Q.log_sum_pt > 6.842716632804 and Q.mean_eta2 < 0.008675069455:
        z += 1387.0122693787805 * (Q.log_sum_pt - 6.842716632804) * (0.008675069455 - Q.mean_eta2)
    if Q.sum_pt_top5 > 752.1 and Q.mean_eta2 < 0.001533485984:
        z += -1.6228593583418842 * (Q.sum_pt_top5 - 752.1) * (0.001533485984 - Q.mean_eta2)
    if Q.log_sum_pt > 6.842716632804 and Q.phi_2 < -5.334616e-06:
        z += -26.742798963356115 * (Q.log_sum_pt - 6.842716632804) * (-5.334616e-06 - Q.phi_2)
    return max(0.0, z)


def neuron_3(Q):
    z = 4.552551703818497
    if 0.06813910019 <= Q.mass_over_sum_pt < 0.090413827016:
        z += -22.984593247378893 * Q.mass_over_sum_pt + 1.5661495021095477
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += 81.77944081797129 * Q.mass_over_sum_pt - 7.905967751373355
    if Q.mass_over_sum_pt >= 0.107985668755:
        z += 27.504824598936793 * Q.mass_over_sum_pt - 2.0450870225399456
    if Q.centroid_offset >= 0.014379521101:
        z += 0.8033548718460726 * Q.centroid_offset - 0.011551858331301752
    if Q.width < 0.006679471358:
        z += -567.8686029169918 * Q.width + 3.7930620682915217
    if Q.width >= 0.018827653081:
        z += 111.94339159118648 * Q.width - 2.107631341589392
    if 36.229410171509 <= Q.mass < 69.611351776123:
        z += -0.05479053587819749 * Q.mass + 1.985028797847997
    if Q.mass >= 69.611351776123:
        z += -0.09514694812875746 * Q.mass + 4.794293207443967
    if Q.e2 < 0.028531698044:
        z += -16.17408547649076 * Q.e2 + 0.9371668785323171
    if 0.028531698044 <= Q.e2 < 0.038466955721:
        z += -53.65423065545775 * Q.e2 + 2.0065390634238858
    if 0.038466955721 <= Q.e2 < 0.04447356835:
        z += -89.92218999465204 * Q.e2 + 3.401657049415701
    if 0.04447356835 <= Q.e2 < 0.050284641981:
        z += -37.48014517896699 * Q.e2 + 1.0693721848915685
    if Q.e2 >= 0.050284641981:
        z += -0.07384446342155115 * Q.e2 - 0.8115902544232583
    if 0.312727471086 <= Q.LHA < 0.325582223496:
        z += 8.32659098880947 * Q.LHA - 2.6039537426978616
    if 0.325582223496 <= Q.LHA < 0.423592510895:
        z += 22.386572012398204 * Q.LHA - 7.1816336266694485
    if Q.LHA >= 0.423592510895:
        z += 34.29958051515733 * Q.LHA - 12.227894810666672
    if Q.girth2 < 0.004372139461:
        z += 871.9835874691958 * Q.girth2 - 11.486439011579765
    if 0.004372139461 <= Q.girth2 < 0.008678044751:
        z += 1521.613183658067 * Q.girth2 - 14.326710204110626
    if 0.008678044751 <= Q.girth2 < 0.013238675334:
        z += 246.03678859606924 * Q.girth2 - 3.2572011644433543
    if Q.lam1 < 0.004183811014:
        z += -254.88157610633286 * Q.lam1 + 1.8683023115253115
    if 0.004183811014 <= Q.lam1 < 0.007330079875:
        z += -486.1223453831741 * Q.lam1 + 2.8357699889115926
    if 0.007330079875 <= Q.lam1 < 0.008375572068:
        z += -231.24076927684126 * Q.lam1 + 0.9674676773862813
    if 0.008375572068 <= Q.lam1 < 0.012003726523:
        z += 162.42684286227365 * Q.lam1 - 2.329723778922347
    if 0.012003726523 <= Q.lam1 < 0.016433749775:
        z += -67.66728921813257 * Q.lam1 + 0.43226325711789026
    if Q.lam1 >= 0.016433749775:
        z += -70.82562276988418 * Q.lam1 + 0.48416652041336306
    if Q.mass_top5 >= 53.607658247923:
        z += 0.009237964867992332 * Q.mass_top5 - 0.49522566354965203
    if Q.mean_eta < -0.012844925793:
        z += 3.722151065731495 * Q.mean_eta + 0.04781075422965692
    if Q.z_dr_0p1_0p2 < 0.468445876241:
        z += -0.5884201962149405 * Q.z_dr_0p1_0p2 + 0.27564301441380895
    if Q.max_dr >= 0.145231109113:
        z += 5.240515718356058 * Q.max_dr - 0.7610859101009602
    if Q.C2 >= 0.094821243733:
        z += -9.698928227240955 * Q.C2 + 0.9196644373840882
    if Q.mass_over_sum_pt_sq >= 0.006387803907:
        z += -132.1665957972319 * Q.mass_over_sum_pt_sq + 0.8442542970084478
    if Q.mass_over_sum_pt > 0.06813910019 and Q.tau32 < 0.518696343899:
        z += -2.035102160737573 * (Q.mass_over_sum_pt - 0.06813910019) * (0.518696343899 - Q.tau32)
    if Q.e2 > 0.028531698044 and Q.n_pt_above_50 > 3.0:
        z += -0.851258114503608 * (Q.e2 - 0.028531698044) * (Q.n_pt_above_50 - 3.0)
    if Q.mass > 36.229410171509 and Q.lam2 < 0.001130644719:
        z += 22.45806453711708 * (Q.mass - 36.229410171509) * (0.001130644719 - Q.lam2)
    if Q.mass_over_sum_pt > 0.06813910019 and Q.n_dr_0_0p05 < 5.0:
        z += 2.558727474371455 * (Q.mass_over_sum_pt - 0.06813910019) * (5.0 - Q.n_dr_0_0p05)
    if Q.LHA > 0.312727471086 and Q.mass_top3 < 50.352200171245:
        z += -0.08472284222158777 * (Q.LHA - 0.312727471086) * (50.352200171245 - Q.mass_top3)
    if Q.e2 < 0.04447356835 and Q.z_dr_0p05_0p1 < 0.964120104909:
        z += -8.167843815864344 * (0.04447356835 - Q.e2) * (0.964120104909 - Q.z_dr_0p05_0p1)
    if Q.mass > 36.229410171509 and Q.eccentricity > 0.620723099573:
        z += 0.08069188617085388 * (Q.mass - 36.229410171509) * (Q.eccentricity - 0.620723099573)
    if Q.e2 < 0.04447356835 and Q.z_dr_0p1_0p2 > 0.0:
        z += -17.2230673104033 * (0.04447356835 - Q.e2) * (Q.z_dr_0p1_0p2 - 0.0)
    if Q.centroid_offset > 0.014379521101 and Q.phi_7 > -0.041534423828:
        z += 30.15385121953493 * (Q.centroid_offset - 0.014379521101) * (Q.phi_7 - -0.041534423828)
    if Q.centroid_offset > 0.014379521101 and Q.eta_0 < -0.039672851562:
        z += -157.60307813172773 * (Q.centroid_offset - 0.014379521101) * (-0.039672851562 - Q.eta_0)
    if Q.mass > 36.229410171509 and Q.phi_5 > 0.112796020508:
        z += 0.044098098492327154 * (Q.mass - 36.229410171509) * (Q.phi_5 - 0.112796020508)
    if Q.width > 0.018827653081 and Q.pt_dispersion < 0.492494773865:
        z += -298.42415242786615 * (Q.width - 0.018827653081) * (0.492494773865 - Q.pt_dispersion)
    if Q.width > 0.018827653081 and Q.z_3 > 0.090493038582:
        z += 467.17709766806536 * (Q.width - 0.018827653081) * (Q.z_3 - 0.090493038582)
    if Q.mass > 36.229410171509 and Q.dr_6 < 0.046481671275:
        z += -0.29592065747085883 * (Q.mass - 36.229410171509) * (0.046481671275 - Q.dr_6)
    if Q.mass_over_sum_pt > 0.06813910019 and Q.dr_7 < 0.042151962757:
        z += -698.7809440586693 * (Q.mass_over_sum_pt - 0.06813910019) * (0.042151962757 - Q.dr_7)
    if Q.mass > 69.611351776123 and Q.z_2nd < 0.15222851187:
        z += -0.11133567599449634 * (Q.mass - 69.611351776123) * (0.15222851187 - Q.z_2nd)
    if Q.LHA > 0.312727471086 and Q.max_dr < 0.145231109113:
        z += -1187.1827909179258 * (Q.LHA - 0.312727471086) * (0.145231109113 - Q.max_dr)
    if Q.LHA > 0.312727471086 and Q.planar_flow > 0.00804883781:
        z += -5.6068170525171865 * (Q.LHA - 0.312727471086) * (Q.planar_flow - 0.00804883781)
    if Q.centroid_offset > 0.014379521101 and Q.phi_6 > 0.119201660156:
        z += 63.535265178390794 * (Q.centroid_offset - 0.014379521101) * (Q.phi_6 - 0.119201660156)
    if Q.mass_over_sum_pt > 0.090413827016 and Q.max_dr < 0.145231109113:
        z += 3662.063477437587 * (Q.mass_over_sum_pt - 0.090413827016) * (0.145231109113 - Q.max_dr)
    if Q.mass > 69.611351776123 and Q.max_dr < 0.177304983139:
        z += 0.7795924329152655 * (Q.mass - 69.611351776123) * (0.177304983139 - Q.max_dr)
    if Q.max_dr > 0.145231109113 and Q.dr_3 < 0.04586879935:
        z += -52.3837119739202 * (Q.max_dr - 0.145231109113) * (0.04586879935 - Q.dr_3)
    if Q.lam1 > 0.016433749775 and Q.eccentricity > 0.959856212153:
        z += -1879.8990191403968 * (Q.lam1 - 0.016433749775) * (Q.eccentricity - 0.959856212153)
    if Q.max_dr > 0.145231109113 and Q.eta_1 < -0.059631347656:
        z += -19.656006064256566 * (Q.max_dr - 0.145231109113) * (-0.059631347656 - Q.eta_1)
    if Q.mean_eta < -0.012844925793 and Q.pt_4 < 68.125:
        z += 0.8974959205727373 * (-0.012844925793 - Q.mean_eta) * (68.125 - Q.pt_4)
    if Q.mean_eta < -0.012844925793 and Q.z_4 < 0.120257140434:
        z += -343.2539040132717 * (-0.012844925793 - Q.mean_eta) * (0.120257140434 - Q.z_4)
    if Q.LHA > 0.312727471086 and Q.pt_5 < 29.875:
        z += -0.822557178363013 * (Q.LHA - 0.312727471086) * (29.875 - Q.pt_5)
    if Q.z_dr_0p1_0p2 < 0.468445876241 and Q.eta_2 > 0.096557617188:
        z += 3.9902561510671717 * (0.468445876241 - Q.z_dr_0p1_0p2) * (Q.eta_2 - 0.096557617188)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.dr_7 < 0.04881348081:
        z += 1046.6456894569947 * (Q.mass_over_sum_pt - 0.107985668755) * (0.04881348081 - Q.dr_7)
    if Q.LHA > 0.312727471086 and Q.eccentricity > 0.959856212153:
        z += 359.43161476747815 * (Q.LHA - 0.312727471086) * (Q.eccentricity - 0.959856212153)
    if Q.e2 > 0.028531698044 and Q.eccentricity > 0.959856212153:
        z += -477.4191815775086 * (Q.e2 - 0.028531698044) * (Q.eccentricity - 0.959856212153)
    if Q.mass_over_sum_pt > 0.090413827016 and Q.pt_6 < 56.53125:
        z += 0.44008376699756013 * (Q.mass_over_sum_pt - 0.090413827016) * (56.53125 - Q.pt_6)
    if Q.lam1 > 0.012003726523 and Q.pt_6 < 38.25:
        z += -1.5328484908918085 * (Q.lam1 - 0.012003726523) * (38.25 - Q.pt_6)
    if Q.mass_over_sum_pt > 0.090413827016 and Q.pt_7 < 48.71875:
        z += 0.39395536659375807 * (Q.mass_over_sum_pt - 0.090413827016) * (48.71875 - Q.pt_7)
    if Q.mass > 36.229410171509 and Q.pt_7 < 20.125:
        z += -0.0009139490347251922 * (Q.mass - 36.229410171509) * (20.125 - Q.pt_7)
    if Q.mass_top5 > 53.607658247923 and Q.eta_7 < 0.029556274414:
        z += 0.03743235845729487 * (Q.mass_top5 - 53.607658247923) * (0.029556274414 - Q.eta_7)
    if Q.mass > 36.229410171509 and Q.phi_3 > 0.102603149414:
        z += 0.03481301987891072 * (Q.mass - 36.229410171509) * (Q.phi_3 - 0.102603149414)
    if Q.max_dr > 0.145231109113 and Q.dr_1 < 0.047732555332:
        z += -110.67045931811695 * (Q.max_dr - 0.145231109113) * (0.047732555332 - Q.dr_1)
    if Q.mass > 69.611351776123 and Q.mean_phi > 0.001618889696:
        z += -0.33651191978037787 * (Q.mass - 69.611351776123) * (Q.mean_phi - 0.001618889696)
    if Q.centroid_offset > 0.014379521101 and Q.mean_phi < -0.006701702951:
        z += -186.47137300156587 * (Q.centroid_offset - 0.014379521101) * (-0.006701702951 - Q.mean_phi)
    if Q.e2 < 0.038466955721 and Q.phi_0 > 0.079772949219:
        z += -1114.865806670783 * (0.038466955721 - Q.e2) * (Q.phi_0 - 0.079772949219)
    if Q.mass > 36.229410171509 and Q.mean_eta > -0.017909069173:
        z += -0.102901884795358 * (Q.mass - 36.229410171509) * (Q.mean_eta - -0.017909069173)
    if Q.mean_eta < -0.012844925793 and Q.phi_0 > -0.029769897461:
        z += -50.312773748888944 * (-0.012844925793 - Q.mean_eta) * (Q.phi_0 - -0.029769897461)
    if Q.max_dr > 0.145231109113 and Q.phi_0 < -0.040130615234:
        z += -10.300355323311985 * (Q.max_dr - 0.145231109113) * (-0.040130615234 - Q.phi_0)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.z_7 < 0.068101508468:
        z += 1069.139869722989 * (Q.mass_over_sum_pt - 0.107985668755) * (0.068101508468 - Q.z_7)
    if Q.lam1 > 0.008375572068 and Q.pt_7 < 37.15625:
        z += -4.047045936454083 * (Q.lam1 - 0.008375572068) * (37.15625 - Q.pt_7)
    if Q.LHA > 0.423592510895 and Q.pt_7 > 37.15625:
        z += 0.6900520594470265 * (Q.LHA - 0.423592510895) * (Q.pt_7 - 37.15625)
    if Q.centroid_offset > 0.014379521101 and Q.pt_7 > 25.578125:
        z += -0.5340412710351785 * (Q.centroid_offset - 0.014379521101) * (Q.pt_7 - 25.578125)
    if Q.lam1 > 0.004183811014 and Q.z_7 < 0.075389597551:
        z += -1928.2687499340027 * (Q.lam1 - 0.004183811014) * (0.075389597551 - Q.z_7)
    if Q.mean_eta < -0.012844925793 and Q.min_pair_mass < 2.801373397908:
        z += 2.6804351293780257 * (-0.012844925793 - Q.mean_eta) * (2.801373397908 - Q.min_pair_mass)
    if Q.girth2 < 0.008678044751 and Q.pt1_dr01 > 5.351076855015:
        z += 1.7735581660479056 * (0.008678044751 - Q.girth2) * (Q.pt1_dr01 - 5.351076855015)
    if Q.mass > 69.611351776123 and Q.n_pt_above_50 < 4.0:
        z += 0.01019795095574949 * (Q.mass - 69.611351776123) * (4.0 - Q.n_pt_above_50)
    if Q.mean_eta < -0.012844925793 and Q.mean_phi < 0.01746432744:
        z += 210.1175732863664 * (-0.012844925793 - Q.mean_eta) * (0.01746432744 - Q.mean_phi)
    if Q.e2 > 0.028531698044 and Q.z_7 < 0.086709591836:
        z += 318.56762786458756 * (Q.e2 - 0.028531698044) * (0.086709591836 - Q.z_7)
    return max(0.0, z)


def neuron_4(Q):
    z = -12.472071427247583
    if Q.tau21 < 0.23799610585:
        z += -21.82465735086248 * Q.tau21 + 5.1941834610158475
    if Q.lam2 < 0.000306123359:
        z += 226.94085516243274 * Q.lam2 - 0.6922626098390139
    if 0.000306123359 <= Q.lam2 < 0.001130644719:
        z += 755.3360569850579 * Q.lam2 - 0.8540167239004388
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += -167.32301707664368 * Q.mass_over_sum_pt + 15.128314321762875
    if Q.mass_over_sum_pt >= 0.107985668755:
        z += 183.5239182975663 * Q.mass_over_sum_pt - 22.758126625263454
    if 0.000319370692 <= Q.width < 0.001653836415:
        z += -318.1844889611839 * Q.width + 0.10161880042319966
    if 0.001653836415 <= Q.width < 0.002635417778:
        z += 77.68293598678207 * Q.width - 0.5530811624680259
    if Q.width >= 0.002635417778:
        z += 659.4876476842985 * Q.width - 2.086379642999825
    if 0.007078157854 <= Q.e2 < 0.020459658932:
        z += 5.672357674244381 * Q.e2 - 0.04014984302265004
    if 0.020459658932 <= Q.e2 < 0.041109715588:
        z += 84.41122565467026 * Q.e2 - 1.6511202265939393
    if 0.041109715588 <= Q.e2 < 0.063441075385:
        z += 128.79599504944838 * Q.e2 - 3.4757654728522347
    if Q.e2 >= 0.063441075385:
        z += 81.1389439679765 * Q.e2 - 0.45235090256578125
    if Q.sum_pt < 763.825:
        z += -7.774746134892041e-05 * Q.sum_pt + 0.05938545466483914
    if Q.girth2_top2 < 0.003111083776:
        z += 146.29764111599778 * Q.girth2_top2 - 0.15572580294239635
    if 0.003111083776 <= Q.girth2_top2 < 0.007639643088:
        z += -94.01582267191506 * Q.girth2_top2 + 0.5919095154025428
    if 0.007639643088 <= Q.girth2_top2 < 0.009530300104:
        z += 66.8221752366675 * Q.girth2_top2 - 0.6368353836075186
    if Q.mass < 41.377904891968:
        z += 0.027999201129453866 * Q.mass - 3.6858411106703297
    if 41.377904891968 <= Q.mass < 56.920347213745:
        z += 0.06476217140922103 * Q.mass - 5.207015798452781
    if 56.920347213745 <= Q.mass < 69.611351776123:
        z += 0.09280449943312163 * Q.mass - 6.803194846254936
    if 69.611351776123 <= Q.mass < 80.4:
        z += 0.03178787394790561 * Q.mass - 2.555745065411611
    if 0.014943876117 <= Q.C2 < 0.067292226106:
        z += -31.769550765045324 * Q.C2 + 0.4747602309255799
    if Q.C2 >= 0.067292226106:
        z += -63.6716884213987 * Q.C2 + 2.621526091361648
    if Q.girth2_top3 < 0.005011406868:
        z += -126.92936001698497 * Q.girth2_top3 + 0.6360946665399632
    if Q.girth < 0.047915700823:
        z += -37.624122654561006 * Q.girth + 4.836022239921565
    if 0.047915700823 <= Q.girth < 0.076081777364:
        z += -59.501351578074946 * Q.girth + 5.884284995856942
    if 0.076081777364 <= Q.girth < 0.101940929517:
        z += -28.002091400408744 * Q.girth + 3.487765295889031
    if 0.101940929517 <= Q.girth < 0.124553743005:
        z += -16.541147853457574 * Q.girth + 2.3194260575709658
    if Q.girth >= 0.124553743005:
        z += 11.460943546951171 * Q.girth - 1.1683392383180653
    if Q.e2_sq < 0.003013300392:
        z += -1559.3602201338886 * Q.e2_sq + 37.3814552372832
    if 0.003013300392 <= Q.e2_sq < 0.007182789718:
        z += -2662.1595223202394 * Q.e2_sq + 40.70452080685865
    if 0.007182789718 <= Q.e2_sq < 0.017162483186:
        z += -2104.7984077364285 * Q.e2_sq + 36.70111312381304
    if 0.017162483186 <= Q.e2_sq < 0.023780909279:
        z += -87.26332106780694 * Q.e2_sq + 2.0752011216977664
    if 0.003562611155 <= Q.girth2 < 0.007520088344:
        z += 807.0065484267452 * Q.girth2 - 2.8750505315831703
    if 0.007520088344 <= Q.girth2 < 0.013238675334:
        z += -37.077357448440125 * Q.girth2 + 3.472535010346804
    if 0.013238675334 <= Q.girth2 < 0.018827652745:
        z += -390.5471629403396 * Q.girth2 + 8.152007005626189
    if Q.girth2 >= 0.018827652745:
        z += -600.6319471156746 * Q.girth2 + 12.107410369087669
    if Q.sum_pt_top5 < 430.75:
        z += -0.0021987266351004564 * Q.sum_pt_top5 + 0.9471014980695216
    if Q.centroid_offset < 0.014379521101:
        z += -7.880333401955454 * Q.centroid_offset + 0.11331542043633357
    if Q.max_dr < 0.102758520097:
        z += -2.9359546212290297 * Q.max_dr + 0.7362235185213999
    if 0.102758520097 <= Q.max_dr < 0.197968879342:
        z += 15.571682299159534 * Q.max_dr - 1.1655938619103274
    if 0.197968879342 <= Q.max_dr < 0.250761204958:
        z += -3.401440184524972 * Q.max_dr + 2.590493933803198
    if Q.max_dr >= 0.250761204958:
        z += -0.4654855632959425 * Q.max_dr + 1.854270415281798
    if Q.mass_over_sum_pt_sq < 0.001101860861:
        z += 2238.915897638697 * Q.mass_over_sum_pt_sq - 27.541725072106527
    if 0.001101860861 <= Q.mass_over_sum_pt_sq < 0.017142307326:
        z += 1563.2202836835293 * Q.mass_over_sum_pt_sq - 26.797202521139962
    if Q.mean_eta >= 0.02644207105:
        z += -24.60062311211547 * Q.mean_eta + 0.6504914242048294
    if Q.lam1 < 0.012003726523:
        z += -90.08686402720514 * Q.lam1 + 1.081378079097257
    if Q.tau21 < 0.23799610585 and Q.mass < 62.55:
        z += -0.15471269055402026 * (0.23799610585 - Q.tau21) * (62.55 - Q.mass)
    if Q.tau21 < 0.23799610585 and Q.e2_sq > 0.011657374702:
        z += -1044.0579290039018 * (0.23799610585 - Q.tau21) * (Q.e2_sq - 0.011657374702)
    if Q.tau21 < 0.23799610585 and Q.lam2 < 0.001130644719:
        z += -12948.103567992575 * (0.23799610585 - Q.tau21) * (0.001130644719 - Q.lam2)
    if Q.tau21 < 0.23799610585 and Q.pt_6 < 62.25:
        z += -0.1519394449779714 * (0.23799610585 - Q.tau21) * (62.25 - Q.pt_6)
    if Q.sum_pt < 763.825 and Q.z_dr_0_0p05 > 0.151540452242:
        z += 0.004100982970642875 * (763.825 - Q.sum_pt) * (Q.z_dr_0_0p05 - 0.151540452242)
    if Q.width > 0.000319370692 and Q.C2 < 0.067292226106:
        z += 3346.576023592542 * (Q.width - 0.000319370692) * (0.067292226106 - Q.C2)
    if Q.tau21 < 0.23799610585 and Q.mean_eta > 0.02644207105:
        z += -295.44812542832005 * (0.23799610585 - Q.tau21) * (Q.mean_eta - 0.02644207105)
    if Q.girth2_top2 < 0.009530300104 and Q.centroid_offset > 0.016278845848:
        z += 6614.435046268072 * (0.009530300104 - Q.girth2_top2) * (Q.centroid_offset - 0.016278845848)
    if Q.tau21 < 0.23799610585 and Q.planar_flow > 0.045057236346:
        z += 11.682237506022211 * (0.23799610585 - Q.tau21) * (Q.planar_flow - 0.045057236346)
    if Q.tau21 < 0.23799610585 and Q.mean_phi > 0.004406178184:
        z += -147.45213616698157 * (0.23799610585 - Q.tau21) * (Q.mean_phi - 0.004406178184)
    if Q.mass < 69.611351776123 and Q.mean_eta2 > 0.004247450386:
        z += 3.667170424613005 * (69.611351776123 - Q.mass) * (Q.mean_eta2 - 0.004247450386)
    if Q.sum_pt < 763.825 and Q.n_dr_0p2_0p4 < 1.0:
        z += -0.004484666776946256 * (763.825 - Q.sum_pt) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.width > 0.000319370692 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += 1084.5355969823524 * (Q.width - 0.000319370692) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.tau21 < 0.23799610585 and Q.dr_7 < 0.175465903809:
        z += -26.74337993895989 * (0.23799610585 - Q.tau21) * (0.175465903809 - Q.dr_7)
    if Q.tau21 < 0.23799610585 and Q.pt_7 < 23.21640625:
        z += -0.7575692380133887 * (0.23799610585 - Q.tau21) * (23.21640625 - Q.pt_7)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.n_dr_0p1_0p2 > 6.0:
        z += -6.362996674766791 * (Q.mass_over_sum_pt - 0.107985668755) * (Q.n_dr_0p1_0p2 - 6.0)
    if Q.lam2 < 0.001130644719 and Q.n_dr_0p1_0p2 > 2.0:
        z += 142.2087330027831 * (0.001130644719 - Q.lam2) * (Q.n_dr_0p1_0p2 - 2.0)
    if Q.tau21 < 0.23799610585 and Q.phi_6 > 0.119201660156:
        z += -42.40577512097782 * (0.23799610585 - Q.tau21) * (Q.phi_6 - 0.119201660156)
    if Q.girth2_top3 < 0.005011406868 and Q.mean_eta < -0.009391680919:
        z += 9888.995457692155 * (0.005011406868 - Q.girth2_top3) * (-0.009391680919 - Q.mean_eta)
    if Q.mass < 69.611351776123 and Q.dr_3 < 0.104247858869:
        z += 0.06115012537838993 * (69.611351776123 - Q.mass) * (0.104247858869 - Q.dr_3)
    if Q.tau21 < 0.23799610585 and Q.dr_6 < 0.169508891404:
        z += -25.026433719507907 * (0.23799610585 - Q.tau21) * (0.169508891404 - Q.dr_6)
    if Q.tau21 < 0.23799610585 and Q.mean_phi < -0.025945045147:
        z += 327.15943614490214 * (0.23799610585 - Q.tau21) * (-0.025945045147 - Q.mean_phi)
    if Q.tau21 < 0.23799610585 and Q.pt_7 > 33.21875:
        z += 0.345318637656419 * (0.23799610585 - Q.tau21) * (Q.pt_7 - 33.21875)
    if Q.girth2_top2 < 0.009530300104 and Q.dr_4 > 0.199975347593:
        z += -879.7679772316334 * (0.009530300104 - Q.girth2_top2) * (Q.dr_4 - 0.199975347593)
    if Q.e2_sq < 0.017162483186 and Q.eta_4 < -0.10657043457:
        z += 540.4591678806894 * (0.017162483186 - Q.e2_sq) * (-0.10657043457 - Q.eta_4)
    if Q.mass_over_sum_pt > 0.107985668755 and Q.D2 < 3.885568320751:
        z += -83.92276274889286 * (Q.mass_over_sum_pt - 0.107985668755) * (3.885568320751 - Q.D2)
    if Q.max_dr > 0.102758520097 and Q.pt_7 > 37.15625:
        z += -0.7565241213151239 * (Q.max_dr - 0.102758520097) * (Q.pt_7 - 37.15625)
    if Q.C2 > 0.014943876117 and Q.pt_7 > 38.53125:
        z += 1.62010228270492 * (Q.C2 - 0.014943876117) * (Q.pt_7 - 38.53125)
    if Q.lam2 < 0.000306123359 and Q.mass_top3 < 50.352200171245:
        z += -17.83913868250236 * (0.000306123359 - Q.lam2) * (50.352200171245 - Q.mass_top3)
    if Q.centroid_offset < 0.014379521101 and Q.z_dr_0p05_0p1 < 0.674770402908:
        z += -86.95352536731241 * (0.014379521101 - Q.centroid_offset) * (0.674770402908 - Q.z_dr_0p05_0p1)
    if Q.tau21 < 0.23799610585 and Q.pt_2 > 73.6875:
        z += 0.026614528722461728 * (0.23799610585 - Q.tau21) * (Q.pt_2 - 73.6875)
    if Q.tau21 < 0.23799610585 and Q.phi_0 < -0.040130615234:
        z += -24.003965480869873 * (0.23799610585 - Q.tau21) * (-0.040130615234 - Q.phi_0)
    if Q.sum_pt_top5 < 430.75 and Q.pt_5 > 73.75:
        z += 0.07580963734744728 * (430.75 - Q.sum_pt_top5) * (Q.pt_5 - 73.75)
    if Q.girth2_top3 < 0.005011406868 and Q.eta_7 < -0.080383300781:
        z += 647.1637119576794 * (0.005011406868 - Q.girth2_top3) * (-0.080383300781 - Q.eta_7)
    if Q.mass < 69.611351776123 and Q.dr_5 > 0.135101491951:
        z += 0.1223367404261353 * (69.611351776123 - Q.mass) * (Q.dr_5 - 0.135101491951)
    if Q.mean_eta > 0.02644207105 and Q.orientation_deg > 36.241523288937:
        z += -0.0783740921460776 * (Q.mean_eta - 0.02644207105) * (Q.orientation_deg - 36.241523288937)
    if Q.lam2 < 0.001130644719 and Q.mean_phi < -0.025945045147:
        z += -65235.25667367369 * (0.001130644719 - Q.lam2) * (-0.025945045147 - Q.mean_phi)
    if Q.e2_sq < 0.023780909279 and Q.mean_phi < -0.01753483098:
        z += 1563.9896851075584 * (0.023780909279 - Q.e2_sq) * (-0.01753483098 - Q.mean_phi)
    if Q.lam2 < 0.000306123359 and Q.mean_eta < -0.004664941598:
        z += -61424.34288585621 * (0.000306123359 - Q.lam2) * (-0.004664941598 - Q.mean_eta)
    if Q.mean_eta > 0.02644207105 and Q.dr01 > 0.141033647649:
        z += 78.9363517679207 * (Q.mean_eta - 0.02644207105) * (Q.dr01 - 0.141033647649)
    if Q.max_dr > 0.197968879342 and Q.z_dr_0p05_0p1 > 0.846033477783:
        z += -106.50446712253242 * (Q.max_dr - 0.197968879342) * (Q.z_dr_0p05_0p1 - 0.846033477783)
    if Q.lam2 < 0.000306123359 and Q.n_dr_0p05_0p1 > 0.0:
        z += 194.6461208549316 * (0.000306123359 - Q.lam2) * (Q.n_dr_0p05_0p1 - 0.0)
    if Q.girth2 > 0.018827652745 and Q.pt_6 > 62.25:
        z += 9.319458925510787 * (Q.girth2 - 0.018827652745) * (Q.pt_6 - 62.25)
    if Q.max_dr > 0.197968879342 and Q.z_7 > 0.028070914944:
        z += 195.25745120178067 * (Q.max_dr - 0.197968879342) * (Q.z_7 - 0.028070914944)
    if Q.C2 > 0.067292226106 and Q.pt_7 < 37.15625:
        z += 1.0522960344343346 * (Q.C2 - 0.067292226106) * (37.15625 - Q.pt_7)
    if Q.girth2 > 0.003562611155 and Q.pt_7 > 53.4375:
        z += -4.637293658359084 * (Q.girth2 - 0.003562611155) * (Q.pt_7 - 53.4375)
    if Q.mean_eta > 0.02644207105 and Q.phi_6 > 0.119201660156:
        z += 145.45920590180398 * (Q.mean_eta - 0.02644207105) * (Q.phi_6 - 0.119201660156)
    if Q.mass < 56.920347213745 and Q.dr01 > 0.141033647649:
        z += 0.33454639542196674 * (56.920347213745 - Q.mass) * (Q.dr01 - 0.141033647649)
    if Q.girth2 > 0.013238675334 and Q.eccentricity > 0.959856212153:
        z += 2450.0012651072047 * (Q.girth2 - 0.013238675334) * (Q.eccentricity - 0.959856212153)
    if Q.max_dr > 0.102758520097 and Q.eccentricity > 0.984196588116:
        z += -259.3245609499674 * (Q.max_dr - 0.102758520097) * (Q.eccentricity - 0.984196588116)
    if Q.max_dr > 0.102758520097 and Q.phi_5 > 0.112796020508:
        z += -7.06818964918849 * (Q.max_dr - 0.102758520097) * (Q.phi_5 - 0.112796020508)
    if Q.e2 > 0.041109715588 and Q.tau32 > 0.430992257595:
        z += 25.288862843631705 * (Q.e2 - 0.041109715588) * (Q.tau32 - 0.430992257595)
    if Q.tau21 < 0.23799610585 and Q.sum_pt_top2 < 405.0:
        z += -0.01202178183734759 * (0.23799610585 - Q.tau21) * (405.0 - Q.sum_pt_top2)
    return max(0.0, z)


def neuron_5(Q):
    z = -0.10017298887384445
    if Q.LHA < 0.154689112391:
        z += -4.406006068566391 * Q.LHA + 1.8734740395800435
    if 0.154689112391 <= Q.LHA < 0.216055863061:
        z += -19.422779577391445 * Q.LHA + 4.196405404636874
    if Q.z_7 < 0.023207568189:
        z += -118.83607395380443 * Q.z_7 + 4.229826121484638
    if 0.023207568189 <= Q.z_7 < 0.03243272066:
        z += -72.55927062555645 * Q.z_7 + 3.155854052675381
    if 0.03243272066 <= Q.z_7 < 0.049399692737:
        z += -28.25250766620169 * Q.z_7 + 1.7188651862657935
    if 0.049399692737 <= Q.z_7 < 0.071488645583:
        z += -14.631747858713922 * Q.z_7 + 1.0460038369314186
    if 6.267538488641 <= Q.log_sum_pt < 6.572937922293:
        z += 0.42192267099426317 * Q.log_sum_pt - 2.644416579686758
    if 6.572937922293 <= Q.log_sum_pt < 6.842716632804:
        z += 2.927080967204356 * Q.log_sum_pt - 19.110666546192995
    if 6.842716632804 <= Q.log_sum_pt < 6.896095378249:
        z += -2.8786074117424416 * Q.log_sum_pt + 20.616013889303147
    if Q.log_sum_pt >= 6.896095378249:
        z += 12.03855840982763 * Q.log_sum_pt - 82.25418438940018
    if Q.e2_sq < 0.00528466865:
        z += -119.23848231700832 * Q.e2_sq + 0.6301358693742732
    if Q.z_6 < 0.028865759995:
        z += -24.69971369394301 * Q.z_6 + 1.2035612869637973
    if 0.028865759995 <= Q.z_6 < 0.05096141791:
        z += -22.202791218820494 * Q.z_6 + 1.1314857220707895
    if Q.dr_0 < 0.021588001063:
        z += 101.65662250542475 * Q.dr_0 - 2.2977652115244425
    if 0.021588001063 <= Q.dr_0 < 0.026454043164:
        z += 21.208599242315405 * Q.dr_0 - 0.5610531998041894
    if Q.e2 < 0.035560912266:
        z += -38.703157299073 * Q.e2 + 1.3763195811295323
    if Q.width < 0.002635417778:
        z += -323.8737433616392 * Q.width + 0.8535426210826734
    if Q.girth2 < 4.8108519e-05:
        z += -10455.767632870591 * Q.girth2 + 0.5030114958255398
    if Q.mass_over_sum_pt < 0.084751611895:
        z += 16.631333890618833 * Q.mass_over_sum_pt - 1.6728318859419349
    if 0.084751611895 <= Q.mass_over_sum_pt < 0.107985668755:
        z += 11.332481982573881 * Q.mass_over_sum_pt - 1.2237456455422289
    if Q.girth2_top5 < 0.002270363079:
        z += 75.45969881350122 * Q.girth2_top5 - 0.1713209141386333
    if Q.sum_pt_top5 >= 752.1:
        z += 0.007913939250922652 * Q.sum_pt_top5 - 5.952073710618927
    if Q.sum_pt_top2 < 548.196875:
        z += 0.002451061775701646 * Q.sum_pt_top2 - 1.3436644058715934
    if Q.pt_5 < 24.578125:
        z += -0.03849476205459723 * Q.pt_5 + 0.9461290736231476
    if Q.sum_pt >= 868.509375:
        z += -0.00923783038649617 * Q.sum_pt + 8.023142295331798
    if Q.mean_phi2 < 0.01426135283:
        z += 21.544228592055788 * Q.mean_phi2 - 0.30724984540148176
    if Q.z_dr_0p1_0p2 < 0.045106684603:
        z += -3.2659488511771997 * Q.z_dr_0p1_0p2 + 0.1473161247595801
    if Q.z_dr_0p05_0p1 >= 0.964120104909:
        z += -3.674903809728221 * Q.z_dr_0p05_0p1 + 3.5430486465656563
    if Q.pt_3 < 45.059375:
        z += -0.01182662280734803 * Q.pt_3 + 0.5329002320598477
    if Q.z_top2_slots < 0.55004856109:
        z += -1.2159761485845593 * Q.z_top2_slots + 0.6688459308486968
    if Q.mass < 60.630975723267:
        z += 0.004419818684255006 * Q.mass - 0.26797791934630716
    if Q.pt_7 < 53.4375:
        z += -0.013369949517255009 * Q.pt_7 + 0.7144566773283145
    if Q.girth2_top2 < 0.004007841607:
        z += 75.88260418208125 * Q.girth2_top2 - 0.30412545828845744
    if Q.dr_7 < 0.030522088714:
        z += -3.143986954942534 * Q.dr_7 + 0.09596104875441475
    if Q.z_7 < 0.049399692737 and Q.mass_top5 < 62.55:
        z += 0.35052114401312096 * (0.049399692737 - Q.z_7) * (62.55 - Q.mass_top5)
    if Q.LHA < 0.216055863061 and Q.log_sum_pt < 6.804164030582:
        z += -43.480305240936744 * (0.216055863061 - Q.LHA) * (6.804164030582 - Q.log_sum_pt)
    if Q.e2_sq < 0.00528466865 and Q.centroid_offset < 0.014379521101:
        z += -3277.4157818817275 * (0.00528466865 - Q.e2_sq) * (0.014379521101 - Q.centroid_offset)
    if Q.z_7 < 0.071488645583 and Q.centroid_offset < 0.031170772021:
        z += -450.13385041574895 * (0.071488645583 - Q.z_7) * (0.031170772021 - Q.centroid_offset)
    if Q.z_7 < 0.071488645583 and Q.sum_pt < 788.4484375:
        z += -0.0960125124350458 * (0.071488645583 - Q.z_7) * (788.4484375 - Q.sum_pt)
    if Q.z_7 < 0.071488645583 and Q.lam1 < 0.001503553356:
        z += 6150.4842339671595 * (0.071488645583 - Q.z_7) * (0.001503553356 - Q.lam1)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_4 > 0.030068239644:
        z += 5.860984922861235 * (Q.log_sum_pt - 6.896095378249) * (Q.dr_4 - 0.030068239644)
    if Q.e2_sq < 0.00528466865 and Q.n_pt_above_50 > 6.0:
        z += -31.252042678399757 * (0.00528466865 - Q.e2_sq) * (Q.n_pt_above_50 - 6.0)
    if Q.LHA < 0.216055863061 and Q.n_dr_0p2_0p4 > 0.0:
        z += -4.781153009935813 * (0.216055863061 - Q.LHA) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.z_7 < 0.071488645583 and Q.n_dr_0p2_0p4 < 1.0:
        z += 0.3291790954529503 * (0.071488645583 - Q.z_7) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.log_sum_pt > 6.896095378249 and Q.planar_flow < 0.045057236346:
        z += 52.041096285799306 * (Q.log_sum_pt - 6.896095378249) * (0.045057236346 - Q.planar_flow)
    if Q.z_7 < 0.071488645583 and Q.lam2 < 0.001130644719:
        z += 8601.74309871678 * (0.071488645583 - Q.z_7) * (0.001130644719 - Q.lam2)
    if Q.width < 0.002635417778 and Q.centroid_offset < 0.023554160423:
        z += 26926.56205310129 * (0.002635417778 - Q.width) * (0.023554160423 - Q.centroid_offset)
    if Q.log_sum_pt > 6.572937922293 and Q.centroid_offset > 0.018377780003:
        z += 76.57304971584566 * (Q.log_sum_pt - 6.572937922293) * (Q.centroid_offset - 0.018377780003)
    if Q.z_6 < 0.028865759995 and Q.phi_0 > 0.014526367188:
        z += -1531.7796868041978 * (0.028865759995 - Q.z_6) * (Q.phi_0 - 0.014526367188)
    if Q.z_7 < 0.03243272066 and Q.pt_5 > 33.0265625:
        z += -0.1013558968674495 * (0.03243272066 - Q.z_7) * (Q.pt_5 - 33.0265625)
    if Q.sum_pt > 868.509375 and Q.centroid_offset < 0.012587644117:
        z += 0.6095469283432067 * (Q.sum_pt - 868.509375) * (0.012587644117 - Q.centroid_offset)
    if Q.mass_over_sum_pt < 0.084751611895 and Q.mass_top3 > 28.345095968085:
        z += -0.41079340685791976 * (0.084751611895 - Q.mass_over_sum_pt) * (Q.mass_top3 - 28.345095968085)
    if Q.log_sum_pt > 6.896095378249 and Q.centroid_offset < 0.018377780003:
        z += -675.4825608862354 * (Q.log_sum_pt - 6.896095378249) * (0.018377780003 - Q.centroid_offset)
    if Q.log_sum_pt > 6.572937922293 and Q.mean_phi2 < 0.000145482056:
        z += 4705.385621142988 * (Q.log_sum_pt - 6.572937922293) * (0.000145482056 - Q.mean_phi2)
    if Q.sum_pt_top2 < 548.196875 and Q.dr_0 < 0.021588001063:
        z += 0.4349954917870491 * (548.196875 - Q.sum_pt_top2) * (0.021588001063 - Q.dr_0)
    if Q.log_sum_pt > 6.572937922293 and Q.dr_0 < 0.021588001063:
        z += 362.66863041944003 * (Q.log_sum_pt - 6.572937922293) * (0.021588001063 - Q.dr_0)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_0 < 0.04118638065:
        z += -552.8781524897846 * (Q.log_sum_pt - 6.896095378249) * (0.04118638065 - Q.dr_0)
    if Q.pt_5 < 24.578125 and Q.centroid_offset < 0.001308549272:
        z += -9.341819559236143 * (24.578125 - Q.pt_5) * (0.001308549272 - Q.centroid_offset)
    if Q.z_7 < 0.071488645583 and Q.mean_phi2 < 0.004331280361:
        z += 2528.7134891834457 * (0.071488645583 - Q.z_7) * (0.004331280361 - Q.mean_phi2)
    if Q.log_sum_pt > 6.572937922293 and Q.lam1 < 0.012003726523:
        z += -535.6112419123402 * (Q.log_sum_pt - 6.572937922293) * (0.012003726523 - Q.lam1)
    if Q.log_sum_pt > 6.572937922293 and Q.girth2_top2 < 0.006299534492:
        z += 281.49043912799567 * (Q.log_sum_pt - 6.572937922293) * (0.006299534492 - Q.girth2_top2)
    if Q.sum_pt_top2 < 548.196875 and Q.girth2_top3 < 0.003952581551:
        z += -0.17810706461864356 * (548.196875 - Q.sum_pt_top2) * (0.003952581551 - Q.girth2_top3)
    if Q.log_sum_pt > 6.572937922293 and Q.mean_eta2 < 9.0303693e-05:
        z += 12029.42657164457 * (Q.log_sum_pt - 6.572937922293) * (9.0303693e-05 - Q.mean_eta2)
    if Q.pt_5 < 24.578125 and Q.mean_eta2 > 1.7977892e-05:
        z += -14.965367175479741 * (24.578125 - Q.pt_5) * (Q.mean_eta2 - 1.7977892e-05)
    if Q.mass_over_sum_pt < 0.084751611895 and Q.max_pair_mass < 18.097979966098:
        z += -0.698421405978479 * (0.084751611895 - Q.mass_over_sum_pt) * (18.097979966098 - Q.max_pair_mass)
    if Q.LHA < 0.216055863061 and Q.mass_top3 > 3.559569591142:
        z += -0.541031794526134 * (0.216055863061 - Q.LHA) * (Q.mass_top3 - 3.559569591142)
    if Q.mean_phi2 < 0.01426135283 and Q.max_pair_mass < 40.046952646555:
        z += 0.619973238070088 * (0.01426135283 - Q.mean_phi2) * (40.046952646555 - Q.max_pair_mass)
    if Q.LHA < 0.216055863061 and Q.planar_flow < 0.083662731125:
        z += 41.689413294405014 * (0.216055863061 - Q.LHA) * (0.083662731125 - Q.planar_flow)
    if Q.z_7 < 0.03243272066 and Q.pt_5 < 29.875:
        z += -2.8276940401374304 * (0.03243272066 - Q.z_7) * (29.875 - Q.pt_5)
    if Q.sum_pt > 868.509375 and Q.pt_5 < 33.0265625:
        z += 0.0001973513873281263 * (Q.sum_pt - 868.509375) * (33.0265625 - Q.pt_5)
    if Q.e2 < 0.035560912266 and Q.lam2 < 7.3007261e-05:
        z += 127949.80597906603 * (0.035560912266 - Q.e2) * (7.3007261e-05 - Q.lam2)
    if Q.z_7 < 0.071488645583 and Q.phi_0 > 0.021438598633:
        z += 65.7206597233984 * (0.071488645583 - Q.z_7) * (Q.phi_0 - 0.021438598633)
    if Q.LHA < 0.216055863061 and Q.centroid_offset > 0.00231612516:
        z += -411.24789729694817 * (0.216055863061 - Q.LHA) * (Q.centroid_offset - 0.00231612516)
    if Q.log_sum_pt > 6.572937922293 and Q.mean_phi < -9.3112965e-05:
        z += 25.0611731405524 * (Q.log_sum_pt - 6.572937922293) * (-9.3112965e-05 - Q.mean_phi)
    if Q.log_sum_pt > 6.896095378249 and Q.pt_5 > 50.125:
        z += 0.0934236384664473 * (Q.log_sum_pt - 6.896095378249) * (Q.pt_5 - 50.125)
    if Q.log_sum_pt > 6.572937922293 and Q.n_dr_0p2_0p4 < 1.0:
        z += -2.04035215228123 * (Q.log_sum_pt - 6.572937922293) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.log_sum_pt > 6.896095378249 and Q.centroid_offset > 0.005576073186:
        z += -318.2217424843161 * (Q.log_sum_pt - 6.896095378249) * (Q.centroid_offset - 0.005576073186)
    if Q.LHA < 0.154689112391 and Q.pt_5 < 41.375:
        z += -0.17493160692811216 * (0.154689112391 - Q.LHA) * (41.375 - Q.pt_5)
    if Q.z_7 < 0.049399692737 and Q.pt_5 < 73.75:
        z += -0.4094175062159593 * (0.049399692737 - Q.z_7) * (73.75 - Q.pt_5)
    if Q.z_7 < 0.03243272066 and Q.mean_eta > 0.0127187056:
        z += -2001.1623114844278 * (0.03243272066 - Q.z_7) * (Q.mean_eta - 0.0127187056)
    if Q.z_dr_0p1_0p2 < 0.045106684603 and Q.n_dr_0p1_0p2 > 1.0:
        z += -16.56800269931827 * (0.045106684603 - Q.z_dr_0p1_0p2) * (Q.n_dr_0p1_0p2 - 1.0)
    if Q.dr_0 < 0.021588001063 and Q.pt_dispersion < 0.456324180961:
        z += -635.3743137363032 * (0.021588001063 - Q.dr_0) * (0.456324180961 - Q.pt_dispersion)
    if Q.mean_phi2 < 0.01426135283 and Q.pt_5 < 24.578125:
        z += 10.695748727613818 * (0.01426135283 - Q.mean_phi2) * (24.578125 - Q.pt_5)
    if Q.z_6 < 0.028865759995 and Q.n_dr_0p2_0p4 < 2.0:
        z += 22.349751605774827 * (0.028865759995 - Q.z_6) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.z_6 < 0.05096141791 and Q.e2_sq > 0.003902458471:
        z += -1959.152202218678 * (0.05096141791 - Q.z_6) * (Q.e2_sq - 0.003902458471)
    if Q.log_sum_pt > 6.267538488641 and Q.centroid_offset > 0.00231612516:
        z += 66.14132293780676 * (Q.log_sum_pt - 6.267538488641) * (Q.centroid_offset - 0.00231612516)
    if Q.mass_over_sum_pt < 0.084751611895 and Q.centroid_offset < 0.018377780003:
        z += 1198.6440785589205 * (0.084751611895 - Q.mass_over_sum_pt) * (0.018377780003 - Q.centroid_offset)
    if Q.girth2_top5 < 0.002270363079 and Q.phi_1 < 0.021865844727:
        z += -2010.074400090319 * (0.002270363079 - Q.girth2_top5) * (0.021865844727 - Q.phi_1)
    if Q.z_6 < 0.05096141791 and Q.phi_4 < -0.049652099609:
        z += 76.82685576239176 * (0.05096141791 - Q.z_6) * (-0.049652099609 - Q.phi_4)
    if Q.log_sum_pt > 6.572937922293 and Q.mean_phi > 0.001618889696:
        z += -141.18539130482878 * (Q.log_sum_pt - 6.572937922293) * (Q.mean_phi - 0.001618889696)
    if Q.z_7 < 0.049399692737 and Q.centroid_offset < 0.010960638421:
        z += -1256.7677281011906 * (0.049399692737 - Q.z_7) * (0.010960638421 - Q.centroid_offset)
    if Q.log_sum_pt > 6.267538488641 and Q.mean_phi > 0.002834883542:
        z += 21.407193266941817 * (Q.log_sum_pt - 6.267538488641) * (Q.mean_phi - 0.002834883542)
    if Q.log_sum_pt > 6.572937922293 and Q.centroid_offset > 0.037760993714:
        z += -118.30427931830808 * (Q.log_sum_pt - 6.572937922293) * (Q.centroid_offset - 0.037760993714)
    if Q.mass < 60.630975723267 and Q.n_dr_0p2_0p4 < 2.0:
        z += 0.009375010348321666 * (60.630975723267 - Q.mass) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.LHA < 0.154689112391 and Q.centroid_offset > 0.003343241496:
        z += -999.8951736184862 * (0.154689112391 - Q.LHA) * (Q.centroid_offset - 0.003343241496)
    if Q.log_sum_pt > 6.267538488641 and Q.z_dr_0p2_0p4 > 0.1009733513:
        z += -3.3129641237164833 * (Q.log_sum_pt - 6.267538488641) * (Q.z_dr_0p2_0p4 - 0.1009733513)
    if Q.LHA < 0.154689112391 and Q.n_pt_above_50 < 5.0:
        z += -1.9749484772946744 * (0.154689112391 - Q.LHA) * (5.0 - Q.n_pt_above_50)
    if Q.girth2_top2 < 0.004007841607 and Q.pt_2 < 101.0625:
        z += 0.575362061463693 * (0.004007841607 - Q.girth2_top2) * (101.0625 - Q.pt_2)
    if Q.sum_pt_top5 > 752.1 and Q.D2 < 1.679198372364:
        z += -0.0022689985323722794 * (Q.sum_pt_top5 - 752.1) * (1.679198372364 - Q.D2)
    return max(0.0, z)


def neuron_6(Q):
    z = 7.008449255199035
    if 0.008092360237 <= Q.centroid_offset < 0.018377780003:
        z += 1.3210608515329758 * Q.centroid_offset - 0.010690500305602813
    if 0.018377780003 <= Q.centroid_offset < 0.049903668404:
        z += -8.174585181417559 * Q.centroid_offset + 0.16381839347432178
    if Q.centroid_offset >= 0.049903668404:
        z += -22.939815269190625 * Q.centroid_offset + 0.9006575396833127
    if Q.width < 0.013238675006:
        z += 516.7930990374049 * Q.width - 6.841655883499774
    if Q.mass_over_sum_pt < 0.008374148675:
        z += -14.529977095008265 * Q.mass_over_sum_pt + 2.240098287527201
    if 0.008374148675 <= Q.mass_over_sum_pt < 0.154170806525:
        z += -71.74543436053139 * Q.mass_over_sum_pt + 2.7192290331768003
    if Q.mass_over_sum_pt >= 0.154170806525:
        z += -57.21545726552313 * Q.mass_over_sum_pt + 0.4791307456495996
    if Q.log_sum_pt < 6.327378592257:
        z += -2.1936469517553903 * Q.log_sum_pt + 14.146954691790327
    if 6.327378592257 <= Q.log_sum_pt < 6.572937922293:
        z += -1.4554707061454373 * Q.log_sum_pt + 9.476234118005266
    if 6.572937922293 <= Q.log_sum_pt < 6.701242202626:
        z += 0.7052335352320789 * Q.log_sum_pt - 4.725940729004337
    if Q.e2 < 0.050284641981:
        z += -40.64597241689969 * Q.e2 + 2.0438681709534023
    if Q.lam2 < 0.000537286005:
        z += -725.2375191503803 * Q.lam2 + 0.3896599693404188
    if 0.000537286005 <= Q.lam2 < 0.003408388935:
        z += -470.39760804908235 * Q.lam2 + 0.2527380515902473
    if Q.lam2 >= 0.003408388935:
        z += -81.55173981730712 * Q.lam2 - 1.0725999031114035
    if Q.LHA >= 0.312727471086:
        z += -7.362863663036865 * Q.LHA + 2.3025697332925215
    z += 9.087875129449749 * Q.max_dr
    if 0.010539266048 <= Q.C2 < 0.094821243733:
        z += -14.034951219774383 * Q.C2 + 0.14791808487590435
    if Q.C2 >= 0.094821243733:
        z += -4.562442081460757 * Q.C2 - 0.7502770128912017
    if Q.girth2_top5 < 0.002270363079:
        z += 28.497036734994936 * Q.girth2_top5 - 0.6958871353690959
    if 0.002270363079 <= Q.girth2_top5 < 0.011482925368:
        z += -40.363504426065276 * Q.girth2_top5 - 0.539548705117065
    if 0.011482925368 <= Q.girth2_top5 < 0.024419631481:
        z += 81.98629829260099 * Q.girth2_top5 - 1.944482358525033
    if Q.girth2_top5 >= 0.024419631481:
        z += 53.489261557606056 * Q.girth2_top5 - 1.2485952231559372
    if Q.girth2 < 0.003562611155:
        z += 881.3289090069416 * Q.girth2 - 9.329086115305708
    if 0.003562611155 <= Q.girth2 < 0.008678044751:
        z += 1209.9177511938126 * Q.girth2 - 10.49972038988919
    if Q.lam1 < 0.007330079875:
        z += -784.5813710913801 * Q.lam1 + 6.126754141975878
    if 0.007330079875 <= Q.lam1 < 0.008375572068:
        z += -359.36186415793355 * Q.lam1 + 3.0098611917455984
    if Q.girth >= 0.087236513197:
        z += 48.8647626831429 * Q.girth - 4.262791514676269
    if Q.D2 < 1.679198372364:
        z += -0.2287568000056126 * Q.D2 + 0.3841280462366218
    if Q.e2_sq < 0.008168570676:
        z += -134.7396909695749 * Q.e2_sq + 1.1006306885473716
    if Q.mass < 49.668099212646:
        z += 0.05121608008198564 * Q.mass - 2.543805346794885
    if Q.z_7 >= 0.06164517166:
        z += 2.7190549403204756 * Q.z_7 - 0.16761660854902677
    if Q.girth2_top2 < 0.004007841607:
        z += 19.33964786864192 * Q.girth2_top2 + 0.2576039099069836
    if 0.004007841607 <= Q.girth2_top2 < 0.009530300104:
        z += -60.682059535929824 * Q.girth2_top2 + 0.5783182383062062
    if Q.pt1_dr01 < 5.351076855015:
        z += 0.024158752644325432 * Q.pt1_dr01 - 0.12927534212108224
    if Q.z_dr_0_0p05 >= 0.768138587475:
        z += -2.4341813012124476 * Q.z_dr_0_0p05 + 1.869788586371387
    if Q.pt_4 < 31.125:
        z += -0.06629596601806043 * Q.pt_4 + 2.0634619423121308
    if Q.z_4 < 0.037477688199:
        z += 39.95495345352101 * Q.z_4 - 1.4974192875366186
    if Q.n_dr_0p1_0p2 < 1.0:
        z += -0.13718577192821613 * Q.n_dr_0p1_0p2 + 0.13718577192821613
    if Q.z_dr_0p1_0p2 < 0.790636250377:
        z += 0.5611894939645481 * Q.z_dr_0p1_0p2 - 0.4436967572590964
    if Q.pt_5 < 33.0265625:
        z += -0.0326689700660836 * Q.pt_5 + 1.078943781698139
    if Q.z_5 < 0.036727111752:
        z += 20.87140261210728 * Q.z_5 - 0.7665463361558487
    if Q.planar_flow < 0.061262048692:
        z += 2.3168738087775864 * Q.planar_flow - 0.141936436086552
    if Q.sum_pt >= 988.4078125:
        z += 0.007952467082304793 * Q.sum_pt - 7.860280592799137
    if Q.sum_pt_top5 >= 839.9546875:
        z += -0.005962259651823842 * Q.sum_pt_top5 + 5.008027942641554
    if Q.pt_6 < 24.421875:
        z += -0.040878946248767534 * Q.pt_6 + 0.9983405154191196
    if Q.centroid_offset > 0.008092360237 and Q.lam2 < 0.003408388935:
        z += 251.71967565549033 * (Q.centroid_offset - 0.008092360237) * (0.003408388935 - Q.lam2)
    if Q.log_sum_pt < 6.327378592257 and Q.z_7 < 0.071488645583:
        z += 107.31706104092292 * (6.327378592257 - Q.log_sum_pt) * (0.071488645583 - Q.z_7)
    if Q.centroid_offset > 0.008092360237 and Q.planar_flow > 0.00804883781:
        z += 2.3629603508400066 * (Q.centroid_offset - 0.008092360237) * (Q.planar_flow - 0.00804883781)
    if Q.centroid_offset > 0.008092360237 and Q.C2 < 0.094821243733:
        z += 44.51719750689266 * (Q.centroid_offset - 0.008092360237) * (0.094821243733 - Q.C2)
    if Q.log_sum_pt < 6.327378592257 and Q.pt_6 > 27.578125:
        z += -0.017016559631565453 * (6.327378592257 - Q.log_sum_pt) * (Q.pt_6 - 27.578125)
    if Q.log_sum_pt < 6.701242202626 and Q.z_7 < 0.049399692737:
        z += 183.65411506406616 * (6.701242202626 - Q.log_sum_pt) * (0.049399692737 - Q.z_7)
    if Q.centroid_offset > 0.049903668404 and Q.n_dr_0p05_0p1 > 6.0:
        z += 2.2319680770538817 * (Q.centroid_offset - 0.049903668404) * (Q.n_dr_0p05_0p1 - 6.0)
    if Q.centroid_offset > 0.018377780003 and Q.mean_phi2 < 0.008921136335:
        z += 1983.8396694218566 * (Q.centroid_offset - 0.018377780003) * (0.008921136335 - Q.mean_phi2)
    if Q.LHA > 0.312727471086 and Q.eccentricity > 0.872657364787:
        z += 104.24019321417855 * (Q.LHA - 0.312727471086) * (Q.eccentricity - 0.872657364787)
    if Q.e2 < 0.050284641981 and Q.n_dr_0p05_0p1 < 4.0:
        z += -0.9507239530813543 * (0.050284641981 - Q.e2) * (4.0 - Q.n_dr_0p05_0p1)
    if Q.width < 0.013238675006 and Q.mean_eta < -0.026655913051:
        z += 11405.572459609642 * (0.013238675006 - Q.width) * (-0.026655913051 - Q.mean_eta)
    if Q.width < 0.013238675006 and Q.mean_phi < -0.025945045147:
        z += 8877.615656597784 * (0.013238675006 - Q.width) * (-0.025945045147 - Q.mean_phi)
    if Q.width < 0.013238675006 and Q.mean_phi > 0.026127964072:
        z += 13055.363996844417 * (0.013238675006 - Q.width) * (Q.mean_phi - 0.026127964072)
    if Q.log_sum_pt < 6.701242202626 and Q.mean_phi > 0.009050007537:
        z += -11.84076769299297 * (6.701242202626 - Q.log_sum_pt) * (Q.mean_phi - 0.009050007537)
    if Q.mass_over_sum_pt > 0.008374148675 and Q.tau32 < 0.518696343899:
        z += -5.36440833728625 * (Q.mass_over_sum_pt - 0.008374148675) * (0.518696343899 - Q.tau32)
    if Q.centroid_offset > 0.008092360237 and Q.mean_eta2 < 0.001101289818:
        z += -17451.45052692252 * (Q.centroid_offset - 0.008092360237) * (0.001101289818 - Q.mean_eta2)
    if Q.centroid_offset > 0.018377780003 and Q.pt_2 > 56.5:
        z += 0.25876831249843235 * (Q.centroid_offset - 0.018377780003) * (Q.pt_2 - 56.5)
    if Q.lam1 < 0.007330079875 and Q.D2 < 1.232133567333:
        z += 150.93509731477099 * (0.007330079875 - Q.lam1) * (1.232133567333 - Q.D2)
    if Q.e2 < 0.050284641981 and Q.z_dr_0p1_0p2 > 0.15855820179:
        z += -58.17182089151859 * (0.050284641981 - Q.e2) * (Q.z_dr_0p1_0p2 - 0.15855820179)
    if Q.log_sum_pt < 6.701242202626 and Q.pt_6 < 36.8125:
        z += 0.11707725881490205 * (6.701242202626 - Q.log_sum_pt) * (36.8125 - Q.pt_6)
    if Q.centroid_offset > 0.018377780003 and Q.pt_5 < 24.578125:
        z += -7.703642404590967 * (Q.centroid_offset - 0.018377780003) * (24.578125 - Q.pt_5)
    if Q.log_sum_pt < 6.701242202626 and Q.z_4 < 0.037477688199:
        z += 677.3023850143928 * (6.701242202626 - Q.log_sum_pt) * (0.037477688199 - Q.z_4)
    if Q.width < 0.013238675006 and Q.mean_eta > 0.02644207105:
        z += 12459.434089153561 * (0.013238675006 - Q.width) * (Q.mean_eta - 0.02644207105)
    if Q.lam2 < 0.000537286005 and Q.mean_eta > 0.02644207105:
        z += -49905.93555695024 * (0.000537286005 - Q.lam2) * (Q.mean_eta - 0.02644207105)
    if Q.lam1 < 0.007330079875 and Q.eta_7 > 0.008316040039:
        z += -136.63392225438358 * (0.007330079875 - Q.lam1) * (Q.eta_7 - 0.008316040039)
    if Q.log_sum_pt < 6.701242202626 and Q.mean_eta2 > 0.004247450386:
        z += -2.2364174551353297 * (6.701242202626 - Q.log_sum_pt) * (Q.mean_eta2 - 0.004247450386)
    if Q.D2 < 1.679198372364 and Q.pt_4 < 90.625:
        z += -0.004068607920089562 * (1.679198372364 - Q.D2) * (90.625 - Q.pt_4)
    if Q.e2_sq < 0.008168570676 and Q.mass_top3 > 50.352200171245:
        z += 19.74487388082012 * (0.008168570676 - Q.e2_sq) * (Q.mass_top3 - 50.352200171245)
    if Q.girth2_top5 > 0.011482925368 and Q.mean_eta > 0.0127187056:
        z += -436.979804328567 * (Q.girth2_top5 - 0.011482925368) * (Q.mean_eta - 0.0127187056)
    if Q.log_sum_pt < 6.701242202626 and Q.pt_7 < 45.75:
        z += 0.11904634101165357 * (6.701242202626 - Q.log_sum_pt) * (45.75 - Q.pt_7)
    if Q.C2 > 0.010539266048 and Q.pt_7 > 31.859375:
        z += 0.29240852660404926 * (Q.C2 - 0.010539266048) * (Q.pt_7 - 31.859375)
    if Q.mass < 49.668099212646 and Q.z_dr_0p05_0p1 < 0.750909513235:
        z += 0.04007358900366853 * (49.668099212646 - Q.mass) * (0.750909513235 - Q.z_dr_0p05_0p1)
    if Q.girth2_top5 > 0.002270363079 and Q.z_dr_0p05_0p1 > 0.291944718361:
        z += 90.38704961387526 * (Q.girth2_top5 - 0.002270363079) * (Q.z_dr_0p05_0p1 - 0.291944718361)
    if Q.girth2_top2 < 0.009530300104 and Q.mean_phi < -0.009352574684:
        z += 2362.1656312207233 * (0.009530300104 - Q.girth2_top2) * (-0.009352574684 - Q.mean_phi)
    if Q.lam2 < 0.000537286005 and Q.eta_7 < -0.121826171875:
        z += 6712.2353765577045 * (0.000537286005 - Q.lam2) * (-0.121826171875 - Q.eta_7)
    if Q.girth2 < 0.003562611155 and Q.dr_7 > 0.124275510792:
        z += -3635.1496441876075 * (0.003562611155 - Q.girth2) * (Q.dr_7 - 0.124275510792)
    if Q.girth2_top5 > 0.011482925368 and Q.pt_7 > 15.55390625:
        z += -2.0220979430869193 * (Q.girth2_top5 - 0.011482925368) * (Q.pt_7 - 15.55390625)
    if Q.centroid_offset > 0.018377780003 and Q.pt_5 > 59.125:
        z += 1.131994914482675 * (Q.centroid_offset - 0.018377780003) * (Q.pt_5 - 59.125)
    if Q.pt_4 < 31.125 and Q.eta_4 > -0.025806427002:
        z += -0.14454675981164655 * (31.125 - Q.pt_4) * (Q.eta_4 - -0.025806427002)
    if Q.C2 > 0.010539266048 and Q.mean_phi2 > 0.006445344212:
        z += -272.77073116245833 * (Q.C2 - 0.010539266048) * (Q.mean_phi2 - 0.006445344212)
    if Q.mass < 49.668099212646 and Q.dr_7 > 0.145488477229:
        z += 0.374904007105215 * (49.668099212646 - Q.mass) * (Q.dr_7 - 0.145488477229)
    if Q.pt_4 < 31.125 and Q.eta_0 > 0.00523147583:
        z += -1.0296717904375754 * (31.125 - Q.pt_4) * (Q.eta_0 - 0.00523147583)
    if Q.D2 < 1.679198372364 and Q.eta_3 < -0.066412353516:
        z += 1.2974940615370656 * (1.679198372364 - Q.D2) * (-0.066412353516 - Q.eta_3)
    if Q.mass_over_sum_pt > 0.008374148675 and Q.dr_7 > 0.222994708167:
        z += -24.487626542301882 * (Q.mass_over_sum_pt - 0.008374148675) * (Q.dr_7 - 0.222994708167)
    if Q.girth2 < 0.003562611155 and Q.eta_1 < -0.089233398438:
        z += 46563.89672096406 * (0.003562611155 - Q.girth2) * (-0.089233398438 - Q.eta_1)
    if Q.lam2 < 0.000537286005 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += -5019.698790542497 * (0.000537286005 - Q.lam2) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.mass_over_sum_pt > 0.008374148675 and Q.pt_7 < 41.65625:
        z += -0.13845927653255785 * (Q.mass_over_sum_pt - 0.008374148675) * (41.65625 - Q.pt_7)
    if Q.lam2 > 0.000537286005 and Q.z_3 < 0.07235619231:
        z += -2143.7384562297693 * (Q.lam2 - 0.000537286005) * (0.07235619231 - Q.z_3)
    if Q.centroid_offset > 0.008092360237 and Q.mass_top3 < 3.559569591142:
        z += -2.4307316481098837 * (Q.centroid_offset - 0.008092360237) * (3.559569591142 - Q.mass_top3)
    if Q.centroid_offset > 0.018377780003 and Q.orientation_deg < 8.699799315952:
        z += 0.0780781159437538 * (Q.centroid_offset - 0.018377780003) * (8.699799315952 - Q.orientation_deg)
    if Q.log_sum_pt < 6.701242202626 and Q.pt_dispersion > 0.409020702541:
        z += -7.088053279512771 * (6.701242202626 - Q.log_sum_pt) * (Q.pt_dispersion - 0.409020702541)
    if Q.sum_pt > 988.4078125 and Q.phi_6 > 0.078552246094:
        z += 0.012769989235493995 * (Q.sum_pt - 988.4078125) * (Q.phi_6 - 0.078552246094)
    if Q.sum_pt > 988.4078125 and Q.pt_6 > 29.90625:
        z += -5.445320084618288e-05 * (Q.sum_pt - 988.4078125) * (Q.pt_6 - 29.90625)
    if Q.girth2 < 0.003562611155 and Q.dr_6 > 0.169508891404:
        z += -2592.3906045319254 * (0.003562611155 - Q.girth2) * (Q.dr_6 - 0.169508891404)
    if Q.D2 < 1.679198372364 and Q.min_pair_mass < 2.801373397908:
        z += -0.05990327411382168 * (1.679198372364 - Q.D2) * (2.801373397908 - Q.min_pair_mass)
    if Q.girth2_top2 < 0.004007841607 and Q.mean_eta < -0.012844925793:
        z += 9010.197794724581 * (0.004007841607 - Q.girth2_top2) * (-0.012844925793 - Q.mean_eta)
    return max(0.0, z)


def neuron_7(Q):
    z = 9.710936289379866
    if Q.planar_flow < 0.195013533663:
        z += -1.3007809969061894 * Q.planar_flow + 0.2536698987283559
    if Q.girth2_top2 < 0.001056655216:
        z += 518.0045432270814 * Q.girth2_top2 - 0.5473522025125931
    if 0.0016538364 <= Q.girth2 < 0.004372139461:
        z += -597.2762084362716 * Q.girth2 + 0.9877971343658931
    if 0.004372139461 <= Q.girth2 < 0.007520088344:
        z += -1150.8628897458555 * Q.girth2 + 3.408155308803556
    if 0.007520088344 <= Q.girth2 < 0.008678044751:
        z += -2567.3951300492354 * Q.girth2 + 14.06060289800921
    if 0.008678044751 <= Q.girth2 < 0.013238675334:
        z += -767.5513106554251 * Q.girth2 - 1.5585223115010365
    if Q.girth2 >= 0.013238675334:
        z += 68.97725937378209 * Q.girth2 - 12.633052457732994
    if Q.mass_over_sum_pt < 0.072690732432:
        z += -13.950400494849418 * Q.mass_over_sum_pt + 1.8265068857052065
    if 0.072690732432 <= Q.mass_over_sum_pt < 0.084751611895:
        z += 72.91877749457052 * Q.mass_over_sum_pt - 4.488077288111502
    if 0.084751611895 <= Q.mass_over_sum_pt < 0.090413827016:
        z += 210.0213409243246 * Q.mass_over_sum_pt - 16.107740533719635
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += 6.319162687669433 * Q.mass_over_sum_pt + 2.3097529721517
    if 0.107985668755 <= Q.mass_over_sum_pt < 0.13092863437:
        z += -23.284791515594378 * Q.mass_over_sum_pt + 5.506555764583536
    if Q.mass_over_sum_pt >= 0.13092863437:
        z += -9.33439102074496 * Q.mass_over_sum_pt + 3.6800488788783294
    if Q.e2 < 0.016554418951:
        z += 8.089271215202317 * Q.e2 - 1.2713045258929947
    if 0.016554418951 <= Q.e2 < 0.024547699839:
        z += -12.189486326692403 * Q.e2 - 0.9356014777387186
    if 0.024547699839 <= Q.e2 < 0.038466955721:
        z += -3.0778588485407 * Q.e2 - 1.1592709741171712
    if 0.038466955721 <= Q.e2 < 0.050284641981:
        z += 50.23486039813611 * Q.e2 - 3.2100489847451925
    if Q.e2 >= 0.050284641981:
        z += -20.27875754189472 * Q.e2 + 0.3357030481542761
    if Q.girth < 0.04081947431:
        z += 52.836370327008495 * Q.girth - 5.475706135519425
    if 0.04081947431 <= Q.girth < 0.087236513197:
        z += 71.50290828336301 * Q.girth - 6.237664402085478
    if Q.pt_7 < 48.71875:
        z += 0.010931876351193637 * Q.pt_7 - 0.532587350984715
    if Q.width < 0.000561123155:
        z += 1736.5093776163237 * Q.width - 5.698628750674999
    if 0.000561123155 <= Q.width < 0.005590288644:
        z += 939.3672052257738 * Q.width - 5.25133381991966
    if Q.centroid_offset < 0.02076709205:
        z += 24.868050240756737 * Q.centroid_offset - 0.038024002020426106
    if 0.02076709205 <= Q.centroid_offset < 0.031170772021:
        z += -28.152045121390074 * Q.centroid_offset + 1.063049198865055
    if 0.031170772021 <= Q.centroid_offset < 0.037760993714:
        z += -29.978631105473823 * Q.centroid_offset + 1.1199852941516835
    if Q.centroid_offset >= 0.037760993714:
        z += -1.8265859840837493 * Q.centroid_offset + 0.056936095286628484
    if Q.e2_sq < 0.001101266364:
        z += -648.4558919222318 * Q.e2_sq + 0.7141226623115731
    if Q.mass < 29.644699859619:
        z += -0.07566792348097806 * Q.mass + 2.2431528805942116
    if Q.mass >= 80.4:
        z += -0.03364947996453793 * Q.mass + 2.70541818914885
    if Q.lam1 < 0.002464291268:
        z += -21.273366739796245 * Q.lam1 - 2.7977240414279545
    if 0.002464291268 <= Q.lam1 < 0.008375572068:
        z += 482.1540220734898 * Q.lam1 - 4.038315759752576
    if Q.z_dr_0p05_0p1 >= 0.674770402908:
        z += -2.7605398110536044 * Q.z_dr_0p05_0p1 + 1.862730560548215
    if Q.LHA < 0.293190627853:
        z += -9.81545444736102 * Q.LHA + 2.8777992520842983
    if Q.girth2_top3 < 0.005884990035:
        z += -48.952329101334726 * Q.girth2_top3 + 0.2880839689513954
    if Q.max_dr < 0.046566883102:
        z += 45.11758206137665 * Q.max_dr - 7.1553400659278985
    if 0.046566883102 <= Q.max_dr < 0.093110798299:
        z += 41.77780670148468 * Q.max_dr - 6.999817137156869
    if 0.093110798299 <= Q.max_dr < 0.15984864831:
        z += 44.205045465991134 * Q.max_dr - 7.225819276182343
    if 0.15984864831 <= Q.max_dr < 0.197968879342:
        z += 4.189442341718859 * Q.max_dr - 0.8293792054580067
    if Q.m012 < 4.909120770781:
        z += -0.0002446433136356063 * Q.m012 + 0.0012009835724012456
    if Q.mass_top5 >= 53.607658247923:
        z += 0.011560373489828635 * Q.mass_top5 - 0.6197245512610824
    if Q.C2 < 0.067292226106:
        z += 2.4379602120288837 * Q.C2 - 0.16405576982527934
    if Q.planar_flow < 0.195013533663 and Q.width > 0.00752008842:
        z += -2249.6879111159146 * (0.195013533663 - Q.planar_flow) * (Q.width - 0.00752008842)
    if Q.girth2_top2 < 0.001056655216 and Q.centroid_offset > 0.006789738266:
        z += 10887.713903238366 * (0.001056655216 - Q.girth2_top2) * (Q.centroid_offset - 0.006789738266)
    if Q.planar_flow < 0.195013533663 and Q.pt_6 < 35.28125:
        z += -0.2727835186806278 * (0.195013533663 - Q.planar_flow) * (35.28125 - Q.pt_6)
    if Q.planar_flow < 0.195013533663 and Q.n_dr_0p1_0p2 < 3.0:
        z += -0.433851511657835 * (0.195013533663 - Q.planar_flow) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.planar_flow < 0.195013533663 and Q.mass_top3 > 23.663861485439:
        z += 0.0548362450524138 * (0.195013533663 - Q.planar_flow) * (Q.mass_top3 - 23.663861485439)
    if Q.planar_flow < 0.195013533663 and Q.sum_pt > 615.875:
        z += 0.008901884692022577 * (0.195013533663 - Q.planar_flow) * (Q.sum_pt - 615.875)
    if Q.e2 < 0.024547699839 and Q.tau21 < 0.446608647704:
        z += 81.99132639028463 * (0.024547699839 - Q.e2) * (0.446608647704 - Q.tau21)
    if Q.width < 0.005590288644 and Q.mean_phi < -0.00469376049:
        z += 19691.858974939474 * (0.005590288644 - Q.width) * (-0.00469376049 - Q.mean_phi)
    if Q.girth2 > 0.004372139461 and Q.eccentricity > 0.945820652852:
        z += 6975.514973257916 * (Q.girth2 - 0.004372139461) * (Q.eccentricity - 0.945820652852)
    if Q.lam1 < 0.008375572068 and Q.D2 < 1.122624260187:
        z += -1136.9219231831908 * (0.008375572068 - Q.lam1) * (1.122624260187 - Q.D2)
    if Q.e2 < 0.050284641981 and Q.D2 < 1.122624260187:
        z += 75.45758342809967 * (0.050284641981 - Q.e2) * (1.122624260187 - Q.D2)
    if Q.centroid_offset < 0.02076709205 and Q.C2 > 0.023843882605:
        z += 771.2470252625315 * (0.02076709205 - Q.centroid_offset) * (Q.C2 - 0.023843882605)
    if Q.mass > 80.4 and Q.eccentricity > 0.927072033478:
        z += -0.23145514479256235 * (Q.mass - 80.4) * (Q.eccentricity - 0.927072033478)
    if Q.pt_7 < 48.71875 and Q.planar_flow < 0.694781820497:
        z += -0.01625460512968857 * (48.71875 - Q.pt_7) * (0.694781820497 - Q.planar_flow)
    if Q.e2_sq < 0.001101266364 and Q.phi_0 > 0.040283203125:
        z += -45911.18234047202 * (0.001101266364 - Q.e2_sq) * (Q.phi_0 - 0.040283203125)
    if Q.centroid_offset > 0.031170772021 and Q.pt_0 > 376.5:
        z += 0.03459293140167574 * (Q.centroid_offset - 0.031170772021) * (Q.pt_0 - 376.5)
    if Q.e2_sq < 0.001101266364 and Q.phi_1 < -0.009460449219:
        z += -14945.107406082761 * (0.001101266364 - Q.e2_sq) * (-0.009460449219 - Q.phi_1)
    if Q.e2 < 0.024547699839 and Q.phi_0 > 0.054992675781:
        z += 2743.1283793882285 * (0.024547699839 - Q.e2) * (Q.phi_0 - 0.054992675781)
    if Q.girth2_top3 < 0.005884990035 and Q.n_dr_0p2_0p4 > 1.0:
        z += -36.23317505217369 * (0.005884990035 - Q.girth2_top3) * (Q.n_dr_0p2_0p4 - 1.0)
    if Q.centroid_offset > 0.031170772021 and Q.pt_2 > 56.5:
        z += -0.2963634218567677 * (Q.centroid_offset - 0.031170772021) * (Q.pt_2 - 56.5)
    if Q.centroid_offset > 0.031170772021 and Q.n_pt_above_50 > 6.0:
        z += -15.812367864649985 * (Q.centroid_offset - 0.031170772021) * (Q.n_pt_above_50 - 6.0)
    if Q.girth2 > 0.013238675334 and Q.log_sum_pt > 6.19222188581:
        z += 720.8550159866865 * (Q.girth2 - 0.013238675334) * (Q.log_sum_pt - 6.19222188581)
    if Q.z_dr_0p05_0p1 > 0.674770402908 and Q.pt_2 > 84.625:
        z += 0.013318280544808658 * (Q.z_dr_0p05_0p1 - 0.674770402908) * (Q.pt_2 - 84.625)
    if Q.e2_sq < 0.001101266364 and Q.eta_2 < -0.045445251465:
        z += -67271.24526462518 * (0.001101266364 - Q.e2_sq) * (-0.045445251465 - Q.eta_2)
    if Q.width < 0.005590288644 and Q.mean_eta < -0.009391680919:
        z += 23710.495710253657 * (0.005590288644 - Q.width) * (-0.009391680919 - Q.mean_eta)
    if Q.lam1 < 0.008375572068 and Q.n_pt_above_50 < 4.0:
        z += -11.124555201900648 * (0.008375572068 - Q.lam1) * (4.0 - Q.n_pt_above_50)
    if Q.e2 < 0.024547699839 and Q.z_dr_0p05_0p1 > 0.750909513235:
        z += -524.377966730796 * (0.024547699839 - Q.e2) * (Q.z_dr_0p05_0p1 - 0.750909513235)
    if Q.max_dr < 0.197968879342 and Q.z_dr_0p05_0p1 > 0.048758227378:
        z += 41.08182759362717 * (0.197968879342 - Q.max_dr) * (Q.z_dr_0p05_0p1 - 0.048758227378)
    if Q.width < 0.005590288644 and Q.mean_eta > 0.0127187056:
        z += 29227.9994973872 * (0.005590288644 - Q.width) * (Q.mean_eta - 0.0127187056)
    if Q.e2_sq < 0.001101266364 and Q.phi_0 > 0.014526367188:
        z += -18810.470306478674 * (0.001101266364 - Q.e2_sq) * (Q.phi_0 - 0.014526367188)
    if Q.e2_sq < 0.001101266364 and Q.eta_2 > 0.015283966064:
        z += -24894.78596199907 * (0.001101266364 - Q.e2_sq) * (Q.eta_2 - 0.015283966064)
    if Q.z_dr_0p05_0p1 > 0.674770402908 and Q.tau32 < 0.362731824815:
        z += 7.3660452259620115 * (Q.z_dr_0p05_0p1 - 0.674770402908) * (0.362731824815 - Q.tau32)
    if Q.e2 < 0.024547699839 and Q.phi_1 > 0.088684082031:
        z += 78.80699450697307 * (0.024547699839 - Q.e2) * (Q.phi_1 - 0.088684082031)
    if Q.mass < 29.644699859619 and Q.phi_1 < -0.058901977539:
        z += -1.6632380456326246 * (29.644699859619 - Q.mass) * (-0.058901977539 - Q.phi_1)
    if Q.planar_flow < 0.195013533663 and Q.phi_0 < 0.021438598633:
        z += 8.091974521329064 * (0.195013533663 - Q.planar_flow) * (0.021438598633 - Q.phi_0)
    if Q.max_dr < 0.15984864831 and Q.z_dr_0p05_0p1 < 0.674770402908:
        z += 44.82279882898092 * (0.15984864831 - Q.max_dr) * (0.674770402908 - Q.z_dr_0p05_0p1)
    if Q.mass_over_sum_pt < 0.13092863437 and Q.z_dr_0p05_0p1 > 0.291944718361:
        z += -23.0294799045339 * (0.13092863437 - Q.mass_over_sum_pt) * (Q.z_dr_0p05_0p1 - 0.291944718361)
    if Q.width < 0.005590288644 and Q.mean_phi > 0.012519553723:
        z += 27303.34518896195 * (0.005590288644 - Q.width) * (Q.mean_phi - 0.012519553723)
    if Q.max_dr < 0.15984864831 and Q.lam2 > 1.2258237e-05:
        z += 8032.337094753958 * (0.15984864831 - Q.max_dr) * (Q.lam2 - 1.2258237e-05)
    if Q.centroid_offset < 0.037760993714 and Q.sum_pt > 559.6875:
        z += 0.0861808630138512 * (0.037760993714 - Q.centroid_offset) * (Q.sum_pt - 559.6875)
    if Q.girth2_top2 < 0.001056655216 and Q.log_sum_pt > 6.327378592257:
        z += -2038.8259584442392 * (0.001056655216 - Q.girth2_top2) * (Q.log_sum_pt - 6.327378592257)
    if Q.girth2 > 0.007520088344 and Q.log_sum_pt > 6.19222188581:
        z += -414.47056269826794 * (Q.girth2 - 0.007520088344) * (Q.log_sum_pt - 6.19222188581)
    if Q.width < 0.005590288644 and Q.n_dr_0p1_0p2 < 3.0:
        z += 88.6112438908379 * (0.005590288644 - Q.width) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.e2 < 0.038466955721 and Q.planar_flow < 0.195013533663:
        z += -3.2446757765706877 * (0.038466955721 - Q.e2) * (0.195013533663 - Q.planar_flow)
    if Q.lam1 < 0.008375572068 and Q.max_pair_mass > 45.595:
        z += -27.577138282482494 * (0.008375572068 - Q.lam1) * (Q.max_pair_mass - 45.595)
    if Q.girth2_top3 < 0.005884990035 and Q.max_pair_mass > 45.595:
        z += 82.25457659361322 * (0.005884990035 - Q.girth2_top3) * (Q.max_pair_mass - 45.595)
    if Q.LHA < 0.293190627853 and Q.m012 < 16.899120053094:
        z += -0.1458300738631806 * (0.293190627853 - Q.LHA) * (16.899120053094 - Q.m012)
    if Q.e2 < 0.038466955721 and Q.dr_2 > 0.175028083821:
        z += -531.9434352669876 * (0.038466955721 - Q.e2) * (Q.dr_2 - 0.175028083821)
    if Q.mass > 80.4 and Q.m012 < 4.909120770781:
        z += 0.005222191222856054 * (Q.mass - 80.4) * (4.909120770781 - Q.m012)
    if Q.planar_flow < 0.195013533663 and Q.dr_5 < 0.032106131611:
        z += -60.67212523523808 * (0.195013533663 - Q.planar_flow) * (0.032106131611 - Q.dr_5)
    if Q.centroid_offset < 0.037760993714 and Q.tau32 < 0.269169217348:
        z += -40.552746548216376 * (0.037760993714 - Q.centroid_offset) * (0.269169217348 - Q.tau32)
    if Q.width < 0.005590288644 and Q.D2 < 1.122624260187:
        z += 533.4524244008319 * (0.005590288644 - Q.width) * (1.122624260187 - Q.D2)
    if Q.max_dr < 0.15984864831 and Q.D2 < 1.122624260187:
        z += 20.158204583953193 * (0.15984864831 - Q.max_dr) * (1.122624260187 - Q.D2)
    if Q.e2 < 0.038466955721 and Q.D2 < 1.122624260187:
        z += 140.22134475892898 * (0.038466955721 - Q.e2) * (1.122624260187 - Q.D2)
    if Q.e2 < 0.024547699839 and Q.D2 < 1.122624260187:
        z += -218.11514775920833 * (0.024547699839 - Q.e2) * (1.122624260187 - Q.D2)
    if Q.planar_flow < 0.195013533663 and Q.D2 < 1.432482242584:
        z += -2.43755802810756 * (0.195013533663 - Q.planar_flow) * (1.432482242584 - Q.D2)
    if Q.girth2 > 0.007520088344 and Q.D2 > 2.055451202393:
        z += 120.84165964925225 * (Q.girth2 - 0.007520088344) * (Q.D2 - 2.055451202393)
    if Q.mass < 29.644699859619 and Q.C2 > 0.014943876117:
        z += -1.9061218373353768 * (29.644699859619 - Q.mass) * (Q.C2 - 0.014943876117)
    if Q.centroid_offset < 0.037760993714 and Q.C2 > 0.067292226106:
        z += -476.96195671649366 * (0.037760993714 - Q.centroid_offset) * (Q.C2 - 0.067292226106)
    if Q.girth2_top2 < 0.001056655216 and Q.n_dr_0p2_0p4 < 1.0:
        z += 1195.380191674064 * (0.001056655216 - Q.girth2_top2) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.width < 0.005590288644 and Q.n_dr_0p2_0p4 < 1.0:
        z += -222.31365305833398 * (0.005590288644 - Q.width) * (1.0 - Q.n_dr_0p2_0p4)
    return max(0.0, z)


def neuron_8(Q):
    z = -0.1328842314468518
    if Q.girth2 < 0.000964142894:
        z += -1128.0004234896874 * Q.girth2 + 0.33588582986413407
    if 0.000964142894 <= Q.girth2 < 0.006679471442:
        z += 131.51785703299146 * Q.girth2 - 0.8784697701649054
    if Q.girth2 >= 0.02530566426:
        z += 6.701115581716294 * Q.girth2 - 0.16957618107836714
    if Q.e2 < 0.016554418951:
        z += -37.08264873458644 * Q.e2 + 0.7247509803809071
    if 0.016554418951 <= Q.e2 < 0.024547699839:
        z += -13.870309197095384 * Q.e2 + 0.3404841868444186
    if Q.width < 0.000319370692:
        z += -2803.6252774611603 * Q.width + 8.106716385264104
    if 0.000319370692 <= Q.width < 0.005019718802:
        z += -1534.2099077620535 * Q.width + 7.701302320207865
    if Q.LHA < 0.196739721581:
        z += 6.567780422199284 * Q.LHA - 1.29214329166863
    if Q.log_sum_pt >= 6.701242202626:
        z += -0.9804562098880615 * Q.log_sum_pt + 6.570274531528613
    if Q.mass < 8.379955863953:
        z += -0.02460422404000484 * Q.mass - 0.8015934831621441
    if 8.379955863953 <= Q.mass < 15.454033088684:
        z += 0.08121736887515807 * Q.mass - 1.6883737612444107
    if 15.454033088684 <= Q.mass < 21.784077072144:
        z += 0.0658043898746743 * Q.mass - 1.4501810737757428
    if 21.784077072144 <= Q.mass < 29.644699859619:
        z += 0.0021236450993455946 * Q.mass - 0.06295482157845092
    if Q.girth < 0.061086014472:
        z += 22.853359953847164 * Q.girth - 1.3960206768745331
    if Q.sum_pt_top5 >= 658.125:
        z += 0.0010336494889866543 * Q.sum_pt_top5 - 0.6802705699393419
    if Q.centroid_offset < 0.003343241496:
        z += -5.341255148089791 * Q.centroid_offset + 0.017857105851817417
    if Q.max_dr < 0.177304983139:
        z += 0.6536001725340501 * Q.max_dr - 0.11588656757079725
    if Q.z_dr_0_0p05 >= 0.847731333971:
        z += 0.23586824949947527 * Q.z_dr_0_0p05 - 0.19995290578959482
    if Q.pt_7 >= 34.53125:
        z += 0.0013727303812629543 * Q.pt_7 - 0.04740209597798639
    if Q.girth2_top5 < 0.000222950415:
        z += 2588.3804621646727 * Q.girth2_top5 - 0.5770804982175056
    if Q.C2 < 0.027029510401:
        z += 4.397261391859502 * Q.C2 - 0.11885582252718213
    if Q.lam2 < 0.000194798295:
        z += 355.4414270045636 * Q.lam2 - 0.06923938395285595
    if Q.n_dr_0_0p05 >= 5.0:
        z += 0.06722637469829351 * Q.n_dr_0_0p05 - 0.33613187349146756
    if Q.dr_0 < 0.016755406876:
        z += -9.372266727798888 * Q.dr_0 + 0.15703614237466748
    if Q.dr_7 < 0.007333702861:
        z += 11.8240884442871 * Q.dr_7 - 0.08671435125258534
    if Q.girth2_top3 < 0.000823693417:
        z += 81.41421400565525 * Q.girth2_top3 - 0.06706035212668743
    if Q.lam1 < 0.000872228216:
        z += 626.3362519629563 * Q.lam1 - 0.5463081516657758
    if Q.e2_sq < 0.002074109229:
        z += 89.75309836318775 * Q.e2_sq - 0.1861577296464325
    if Q.girth2 < 0.006679471442 and Q.tau21 < 0.501026660204:
        z += -81.08040525078759 * (0.006679471442 - Q.girth2) * (0.501026660204 - Q.tau21)
    if Q.width < 0.005019718802 and Q.pt_7 < 48.71875:
        z += -4.102046684281232 * (0.005019718802 - Q.width) * (48.71875 - Q.pt_7)
    if Q.girth2 < 0.006679471442 and Q.centroid_offset < 0.023554160423:
        z += 14735.29413306689 * (0.006679471442 - Q.girth2) * (0.023554160423 - Q.centroid_offset)
    if Q.girth2 < 0.006679471442 and Q.planar_flow < 0.40079469091:
        z += 283.8427472478556 * (0.006679471442 - Q.girth2) * (0.40079469091 - Q.planar_flow)
    if Q.width < 0.005019718802 and Q.sum_pt_top2 < 248.125:
        z += 0.032458040961269474 * (0.005019718802 - Q.width) * (248.125 - Q.sum_pt_top2)
    if Q.girth2 < 0.006679471442 and Q.n_dr_0p05_0p1 > 0.0:
        z += -1.8472540778034274 * (0.006679471442 - Q.girth2) * (Q.n_dr_0p05_0p1 - 0.0)
    if Q.LHA < 0.196739721581 and Q.mean_phi > -0.000855675264:
        z += 174.87533252653887 * (0.196739721581 - Q.LHA) * (Q.mean_phi - -0.000855675264)
    if Q.girth2 < 0.006679471442 and Q.n_dr_0p1_0p2 > 2.0:
        z += -28.9143215580955 * (0.006679471442 - Q.girth2) * (Q.n_dr_0p1_0p2 - 2.0)
    if Q.width < 0.005019718802 and Q.z_dr_0p2_0p4 < 0.1009733513:
        z += 2926.254061027765 * (0.005019718802 - Q.width) * (0.1009733513 - Q.z_dr_0p2_0p4)
    if Q.girth < 0.061086014472 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += -126.4328209205383 * (0.061086014472 - Q.girth) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.girth2 < 0.006679471442 and Q.phi_0 > -0.040130615234:
        z += 408.017186956578 * (0.006679471442 - Q.girth2) * (Q.phi_0 - -0.040130615234)
    if Q.log_sum_pt > 6.701242202626 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += 1.2960840553602253 * (Q.log_sum_pt - 6.701242202626) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.max_dr < 0.177304983139 and Q.pt1_over_pt0 < 0.465420272571:
        z += 1.8675358690096573 * (0.177304983139 - Q.max_dr) * (0.465420272571 - Q.pt1_over_pt0)
    if Q.girth2 < 0.006679471442 and Q.girth2_top3 > 0.002915531053:
        z += 25432.665638782586 * (0.006679471442 - Q.girth2) * (Q.girth2_top3 - 0.002915531053)
    if Q.width < 0.005019718802 and Q.centroid_offset > 0.006789738266:
        z += -37155.52448048982 * (0.005019718802 - Q.width) * (Q.centroid_offset - 0.006789738266)
    if Q.girth < 0.061086014472 and Q.lam1 > 0.00027588256:
        z += -617.7074889010308 * (0.061086014472 - Q.girth) * (Q.lam1 - 0.00027588256)
    if Q.width < 0.005019718802 and Q.mass_over_sum_pt_sq > 0.00012320649:
        z += -246441.49508711687 * (0.005019718802 - Q.width) * (Q.mass_over_sum_pt_sq - 0.00012320649)
    if Q.max_dr < 0.177304983139 and Q.lam2 < 0.000194798295:
        z += 14291.531128157943 * (0.177304983139 - Q.max_dr) * (0.000194798295 - Q.lam2)
    if Q.mass < 15.454033088684 and Q.lam2 < 0.000306123359:
        z += 173.33083510672185 * (15.454033088684 - Q.mass) * (0.000306123359 - Q.lam2)
    if Q.log_sum_pt > 6.701242202626 and Q.pt_7 < 48.71875:
        z += 0.029847076550936436 * (Q.log_sum_pt - 6.701242202626) * (48.71875 - Q.pt_7)
    if Q.log_sum_pt > 6.701242202626 and Q.girth2 < 0.018827652745:
        z += 51.2929038003067 * (Q.log_sum_pt - 6.701242202626) * (0.018827652745 - Q.girth2)
    if Q.log_sum_pt > 6.701242202626 and Q.mass_over_sum_pt_sq < 0.00023679558:
        z += 11986.543567363107 * (Q.log_sum_pt - 6.701242202626) * (0.00023679558 - Q.mass_over_sum_pt_sq)
    if Q.log_sum_pt > 6.701242202626 and Q.centroid_offset < 0.023554160423:
        z += -115.45449152325273 * (Q.log_sum_pt - 6.701242202626) * (0.023554160423 - Q.centroid_offset)
    if Q.mass < 21.784077072144 and Q.centroid_offset < 0.026856224803:
        z += 1.807624611639767 * (21.784077072144 - Q.mass) * (0.026856224803 - Q.centroid_offset)
    if Q.LHA < 0.196739721581 and Q.width < 0.000561123155:
        z += 25248.888586390563 * (0.196739721581 - Q.LHA) * (0.000561123155 - Q.width)
    if Q.girth2 < 0.006679471442 and Q.log_sum_pt > 6.670067010936:
        z += -877.5144048399802 * (0.006679471442 - Q.girth2) * (Q.log_sum_pt - 6.670067010936)
    if Q.LHA < 0.196739721581 and Q.z_6 > 0.02160287394:
        z += -36.0321734275858 * (0.196739721581 - Q.LHA) * (Q.z_6 - 0.02160287394)
    if Q.mass < 29.644699859619 and Q.centroid_offset < 0.023554160423:
        z += -4.695950417519271 * (29.644699859619 - Q.mass) * (0.023554160423 - Q.centroid_offset)
    if Q.e2 < 0.024547699839 and Q.sum_pt > 788.4484375:
        z += 0.09435991652026132 * (0.024547699839 - Q.e2) * (Q.sum_pt - 788.4484375)
    if Q.girth < 0.061086014472 and Q.width < 0.005019718802:
        z += -26124.507210819353 * (0.061086014472 - Q.girth) * (0.005019718802 - Q.width)
    if Q.girth < 0.061086014472 and Q.lam2 < 0.000194798295:
        z += 90920.61441038494 * (0.061086014472 - Q.girth) * (0.000194798295 - Q.lam2)
    if Q.girth < 0.061086014472 and Q.centroid_offset > 0.006789738266:
        z += 1512.438781999244 * (0.061086014472 - Q.girth) * (Q.centroid_offset - 0.006789738266)
    if Q.e2 < 0.024547699839 and Q.centroid_offset < 0.031170772021:
        z += 1786.9321439338917 * (0.024547699839 - Q.e2) * (0.031170772021 - Q.centroid_offset)
    if Q.girth2 < 0.006679471442 and Q.centroid_offset > 0.018377780003:
        z += 3888.1972922581635 * (0.006679471442 - Q.girth2) * (Q.centroid_offset - 0.018377780003)
    if Q.LHA < 0.196739721581 and Q.lam2 < 0.000306123359:
        z += -15523.41608632657 * (0.196739721581 - Q.LHA) * (0.000306123359 - Q.lam2)
    if Q.mass < 15.454033088684 and Q.z_7 < 0.058613700176:
        z += 1.2138614143796076 * (15.454033088684 - Q.mass) * (0.058613700176 - Q.z_7)
    if Q.LHA < 0.196739721581 and Q.z_7 > 0.016858545121:
        z += 116.72573582016821 * (0.196739721581 - Q.LHA) * (Q.z_7 - 0.016858545121)
    if Q.pt_7 > 34.53125 and Q.width < 0.013238675006:
        z += -0.6775156346484437 * (Q.pt_7 - 34.53125) * (0.013238675006 - Q.width)
    if Q.mass < 21.784077072144 and Q.centroid_offset > 0.016278845848:
        z += 4.543679063703166 * (21.784077072144 - Q.mass) * (Q.centroid_offset - 0.016278845848)
    if Q.max_dr < 0.177304983139 and Q.mean_eta > -0.012844925793:
        z += 12.149991015760861 * (0.177304983139 - Q.max_dr) * (Q.mean_eta - -0.012844925793)
    if Q.z_dr_0_0p05 > 0.847731333971 and Q.lam2 < 0.000537286005:
        z += -4309.366254052944 * (Q.z_dr_0_0p05 - 0.847731333971) * (0.000537286005 - Q.lam2)
    if Q.mass < 21.784077072144 and Q.centroid_offset > 0.031170772021:
        z += -4.431111842830433 * (21.784077072144 - Q.mass) * (Q.centroid_offset - 0.031170772021)
    if Q.girth2_top5 < 0.000222950415 and Q.n_dr_0p2_0p4 > 0.0:
        z += 2022.9073311623679 * (0.000222950415 - Q.girth2_top5) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.C2 < 0.027029510401 and Q.width < 0.004372139331:
        z += -14176.211118481348 * (0.027029510401 - Q.C2) * (0.004372139331 - Q.width)
    if Q.C2 < 0.027029510401 and Q.width < 0.000964142901:
        z += 45079.536407890344 * (0.027029510401 - Q.C2) * (0.000964142901 - Q.width)
    if Q.LHA < 0.196739721581 and Q.centroid_offset > 0.006789738266:
        z += 749.3110065456798 * (0.196739721581 - Q.LHA) * (Q.centroid_offset - 0.006789738266)
    if Q.LHA < 0.196739721581 and Q.girth2 > 0.006679471442:
        z += -3430.2208015340516 * (0.196739721581 - Q.LHA) * (Q.girth2 - 0.006679471442)
    if Q.C2 < 0.027029510401 and Q.width < 0.006096650059:
        z += 2609.416254891975 * (0.027029510401 - Q.C2) * (0.006096650059 - Q.width)
    if Q.LHA < 0.196739721581 and Q.n_pt_above_10 < 8.0:
        z += 0.9089555442424171 * (0.196739721581 - Q.LHA) * (8.0 - Q.n_pt_above_10)
    if Q.sum_pt_top5 > 658.125 and Q.girth2 < 0.0016538364:
        z += -0.8744189384960919 * (Q.sum_pt_top5 - 658.125) * (0.0016538364 - Q.girth2)
    if Q.C2 < 0.027029510401 and Q.centroid_offset > 0.016278845848:
        z += 242.47207500722288 * (0.027029510401 - Q.C2) * (Q.centroid_offset - 0.016278845848)
    if Q.width < 0.005019718802 and Q.z_6 < 0.089100391399:
        z += -1018.5024987697689 * (0.005019718802 - Q.width) * (0.089100391399 - Q.z_6)
    if Q.mass < 21.784077072144 and Q.lam2 < 0.000194798295:
        z += -364.5107980309085 * (21.784077072144 - Q.mass) * (0.000194798295 - Q.lam2)
    if Q.mass < 15.454033088684 and Q.width < 0.000964142901:
        z += -124.2957988218111 * (15.454033088684 - Q.mass) * (0.000964142901 - Q.width)
    if Q.e2 < 0.024547699839 and Q.eccentricity > 0.872657364787:
        z += -232.82969868825876 * (0.024547699839 - Q.e2) * (Q.eccentricity - 0.872657364787)
    if Q.girth2 < 0.006679471442 and Q.n_pt_above_50 > 4.0:
        z += -4.6104726252524415 * (0.006679471442 - Q.girth2) * (Q.n_pt_above_50 - 4.0)
    if Q.mass < 29.644699859619 and Q.mass_top3 > 8.92141334422:
        z += -0.001289123156311689 * (29.644699859619 - Q.mass) * (Q.mass_top3 - 8.92141334422)
    if Q.max_dr < 0.177304983139 and Q.phi_7 < 0.041662597656:
        z += 2.8956298247394443 * (0.177304983139 - Q.max_dr) * (0.041662597656 - Q.phi_7)
    if Q.log_sum_pt > 6.701242202626 and Q.width < 0.006679471358:
        z += -742.1724163616868 * (Q.log_sum_pt - 6.701242202626) * (0.006679471358 - Q.width)
    if Q.girth2_top5 < 0.000222950415 and Q.log_sum_pt < 6.804164030582:
        z += 6671.537236761031 * (0.000222950415 - Q.girth2_top5) * (6.804164030582 - Q.log_sum_pt)
    if Q.width < 0.000319370692 and Q.log_sum_pt < 6.464150123592:
        z += -9798.804217121964 * (0.000319370692 - Q.width) * (6.464150123592 - Q.log_sum_pt)
    if Q.girth < 0.061086014472 and Q.log_sum_pt > 6.670067010936:
        z += 109.09750789653117 * (0.061086014472 - Q.girth) * (Q.log_sum_pt - 6.670067010936)
    if Q.C2 < 0.027029510401 and Q.log_sum_pt > 6.701242202626:
        z += 36.345267833306934 * (0.027029510401 - Q.C2) * (Q.log_sum_pt - 6.701242202626)
    if Q.width < 0.005019718802 and Q.eta_4 < -0.006616973877:
        z += -84.03018498338272 * (0.005019718802 - Q.width) * (-0.006616973877 - Q.eta_4)
    if Q.width < 0.005019718802 and Q.phi_4 < -0.02555847168:
        z += 75.98635192693644 * (0.005019718802 - Q.width) * (-0.02555847168 - Q.phi_4)
    if Q.mass < 29.644699859619 and Q.mass_top5 > 9.257203159811:
        z += -0.0021760431554866955 * (29.644699859619 - Q.mass) * (Q.mass_top5 - 9.257203159811)
    if Q.max_dr < 0.177304983139 and Q.dr_5 < 0.066004994044:
        z += 8.995544226643688 * (0.177304983139 - Q.max_dr) * (0.066004994044 - Q.dr_5)
    if Q.girth2 < 0.000964142894 and Q.mass_top5 < 9.257203159811:
        z += 66.19604492414373 * (0.000964142894 - Q.girth2) * (9.257203159811 - Q.mass_top5)
    if Q.e2 < 0.016554418951 and Q.mass_top5 < 9.257203159811:
        z += -2.47965986825875 * (0.016554418951 - Q.e2) * (9.257203159811 - Q.mass_top5)
    if Q.mass < 21.784077072144 and Q.max_pair_mass > 13.047927274731:
        z += -0.2294416441291105 * (21.784077072144 - Q.mass) * (Q.max_pair_mass - 13.047927274731)
    if Q.girth2 < 0.006679471442 and Q.mass_top5 > 53.607658247923:
        z += 10.344562442960978 * (0.006679471442 - Q.girth2) * (Q.mass_top5 - 53.607658247923)
    if Q.e2 < 0.024547699839 and Q.mass_top5 > 40.2:
        z += -1.1190593705250649 * (0.024547699839 - Q.e2) * (Q.mass_top5 - 40.2)
    return max(0.0, z)


def neuron_9(Q):
    z = -0.9681103538376431
    if Q.girth < 0.033604209498:
        z += 135.92614047325594 * Q.girth - 6.638977624750984
    if 0.033604209498 <= Q.girth < 0.054649224505:
        z += 98.42174611632072 * Q.girth - 5.378672099684923
    if Q.e2 < 0.016554418951:
        z += -100.15858661908527 * Q.e2 + 2.1045060127424646
    if 0.016554418951 <= Q.e2 < 0.020459658932:
        z += -129.46583848205995 * Q.e2 + 2.5896705383846226
    if 0.020459658932 <= Q.e2 < 0.032346998155:
        z += 4.976417278415573 * Q.e2 - 0.16097216052341867
    if Q.mass < 29.644699859619:
        z += 0.05533773399571973 * Q.mass - 2.3758290274167058
    if 29.644699859619 <= Q.mass < 41.377904891968:
        z += -0.040211113134190235 * Q.mass + 0.4566878676820929
    if 41.377904891968 <= Q.mass < 53.332374954224:
        z += 0.10098011378990268 * Q.mass - 5.385509291563295
    if Q.lam2 >= 0.001130644719:
        z += 322.4113873753718 * Q.lam2 - 0.3645327324814274
    if Q.width < 0.000172198326:
        z += -8896.953547402041 * Q.width + 12.33452300288317
    if 0.000172198326 <= Q.width < 0.006096650059:
        z += -1823.3725216038952 * Q.width + 11.116464191415366
    if Q.girth2 < 4.8108519e-05:
        z += -20057.034388052427 * Q.girth2 + 10.604689521106735
    if 4.8108519e-05 <= Q.girth2 < 0.000964142894:
        z += -3628.9116975493453 * Q.girth2 + 9.814356868516336
    if 0.000964142894 <= Q.girth2 < 0.004372139461:
        z += -1384.5617773241097 * Q.girth2 + 7.6504828412817085
    if 0.004372139461 <= Q.girth2 < 0.007520088344:
        z += -507.3099080721869 * Q.girth2 + 3.815015326489364
    if Q.girth2 >= 0.018827652745:
        z += 180.9862596100778 * Q.girth2 - 3.407546447554964
    if Q.lam1 < 0.001503553356:
        z += 1063.0774126602523 * Q.lam1 - 2.6785865135466227
    if 0.001503553356 <= Q.lam1 < 0.005954149834:
        z += 242.70744548355873 * Q.lam1 - 1.4451164962364953
    if Q.n_dr_0p2_0p4 >= 1.0:
        z += 0.2750579600954326 * Q.n_dr_0p2_0p4 - 0.2750579600954326
    if Q.max_dr < 0.15984864831:
        z += -6.283692716767375 * Q.max_dr + 1.3923829375572543
    if 0.15984864831 <= Q.max_dr < 0.221586732566:
        z += -3.972144431566532 * Q.max_dr + 1.0228850686646012
    if Q.max_dr >= 0.221586732566:
        z += 2.3115482852008427 * Q.max_dr - 0.36949786889265307
    if Q.C2 >= 0.051192347892:
        z += 9.805989460605565 * Q.C2 - 0.5019916238926055
    if Q.centroid_offset < 0.009480684835:
        z += -62.80985403734957 * Q.centroid_offset + 1.1288374384457642
    if 0.009480684835 <= Q.centroid_offset < 0.018377780003:
        z += -59.947319626704115 * Q.centroid_offset + 1.1016986518690923
    if Q.log_sum_pt >= 6.377722943814:
        z += -2.197293082362364 * Q.log_sum_pt + 14.013726505666234
    if Q.z_dr_0p2_0p4 >= 0.1009733513:
        z += -0.9907258295270367 * Q.z_dr_0p2_0p4 + 0.10003690722681739
    if Q.mass_over_sum_pt < 0.076373631775:
        z += 77.44088640637142 * Q.mass_over_sum_pt - 5.914441742729815
    if Q.pt_5 < 35.5:
        z += -0.023191961035422537 * Q.pt_5 + 0.8233146167575001
    if 840.01953125 <= Q.sum_pt < 988.4078125:
        z += -0.003027055008487878 * Q.sum_pt + 2.542785329297952
    if Q.sum_pt >= 988.4078125:
        z += -0.0025513353950827877 * Q.sum_pt + 2.072580346848881
    if Q.mass_over_sum_pt_sq < 0.0030131544:
        z += -502.57584461475994 * Q.mass_over_sum_pt_sq + 1.4631487842215156
    if 0.0030131544 <= Q.mass_over_sum_pt_sq < 0.003904593248:
        z += 57.42383050504486 * Q.mass_over_sum_pt_sq - 0.2242167008642946
    if Q.girth2_top2 < 0.000759634834:
        z += -1482.0141070247107 * Q.girth2_top2 + 1.1257895401753744
    if Q.n_pt_above_50 < 2.0:
        z += 0.22267481720245996 * Q.n_pt_above_50 - 0.4453496344049199
    if Q.mean_phi < 0.000697365613:
        z += 3.9477254743678714 * Q.mean_phi - 0.002753007995388266
    if Q.mass < 53.332374954224 and Q.centroid_offset < 0.026856224803:
        z += 6.069652295721005 * (53.332374954224 - Q.mass) * (0.026856224803 - Q.centroid_offset)
    if Q.mass < 53.332374954224 and Q.lam1 < 0.000872228216:
        z += -36.085736252568005 * (53.332374954224 - Q.mass) * (0.000872228216 - Q.lam1)
    if Q.mass < 53.332374954224 and Q.n_dr_0p05_0p1 > 3.0:
        z += 0.005510071314087872 * (53.332374954224 - Q.mass) * (Q.n_dr_0p05_0p1 - 3.0)
    if Q.girth2 > 0.018827652745 and Q.planar_flow < 0.40079469091:
        z += -341.67382334846064 * (Q.girth2 - 0.018827652745) * (0.40079469091 - Q.planar_flow)
    if Q.mass < 53.332374954224 and Q.pt_3 < 60.59375:
        z += -0.00023290083915994408 * (53.332374954224 - Q.mass) * (60.59375 - Q.pt_3)
    if Q.e2 < 0.032346998155 and Q.dr01 < 0.055953954317:
        z += 274.1396614881653 * (0.032346998155 - Q.e2) * (0.055953954317 - Q.dr01)
    if Q.mass < 53.332374954224 and Q.log_sum_pt < 6.842716632804:
        z += 0.08656112732061594 * (53.332374954224 - Q.mass) * (6.842716632804 - Q.log_sum_pt)
    if Q.girth < 0.054649224505 and Q.mean_phi < 0.002834883542:
        z += -1085.1628934067683 * (0.054649224505 - Q.girth) * (0.002834883542 - Q.mean_phi)
    if Q.max_dr < 0.221586732566 and Q.z_top5 < 0.90890302062:
        z += -9.086745565639182 * (0.221586732566 - Q.max_dr) * (0.90890302062 - Q.z_top5)
    if Q.width < 0.006096650059 and Q.C2 > 0.030867108516:
        z += -10228.440341147958 * (0.006096650059 - Q.width) * (Q.C2 - 0.030867108516)
    if Q.width < 0.006096650059 and Q.centroid_offset > 0.003343241496:
        z += -33266.99320326763 * (0.006096650059 - Q.width) * (Q.centroid_offset - 0.003343241496)
    if Q.centroid_offset < 0.018377780003 and Q.z_5 > 0.036727111752:
        z += -238.404324735535 * (0.018377780003 - Q.centroid_offset) * (Q.z_5 - 0.036727111752)
    if Q.mass < 29.644699859619 and Q.mean_phi2 < 0.002127561159:
        z += -6.310080213971027 * (29.644699859619 - Q.mass) * (0.002127561159 - Q.mean_phi2)
    if Q.log_sum_pt > 6.377722943814 and Q.dr_5 < 0.021648628542:
        z += 56.49588076352873 * (Q.log_sum_pt - 6.377722943814) * (0.021648628542 - Q.dr_5)
    if Q.girth < 0.054649224505 and Q.dr_5 < 0.021648628542:
        z += -433.8813456932185 * (0.054649224505 - Q.girth) * (0.021648628542 - Q.dr_5)
    if Q.mass < 53.332374954224 and Q.planar_flow < 0.322073846732:
        z += 0.18915416166328214 * (53.332374954224 - Q.mass) * (0.322073846732 - Q.planar_flow)
    if Q.centroid_offset < 0.018377780003 and Q.pt_4 > 47.34375:
        z += 1.601851069901386 * (0.018377780003 - Q.centroid_offset) * (Q.pt_4 - 47.34375)
    if Q.centroid_offset < 0.018377780003 and Q.z_4 > 0.047491459878:
        z += -1505.7402676524844 * (0.018377780003 - Q.centroid_offset) * (Q.z_4 - 0.047491459878)
    if Q.girth < 0.054649224505 and Q.mean_phi2 > 0.000539434783:
        z += 6508.505634365131 * (0.054649224505 - Q.girth) * (Q.mean_phi2 - 0.000539434783)
    if Q.mass < 53.332374954224 and Q.phi_7 > 0.121704101562:
        z += -0.19747022171657136 * (53.332374954224 - Q.mass) * (Q.phi_7 - 0.121704101562)
    if Q.e2 < 0.020459658932 and Q.eccentricity > 0.903125533696:
        z += -868.613992828227 * (0.020459658932 - Q.e2) * (Q.eccentricity - 0.903125533696)
    if Q.C2 > 0.051192347892 and Q.eccentricity < 0.620723099573:
        z += -44.001040908192266 * (Q.C2 - 0.051192347892) * (0.620723099573 - Q.eccentricity)
    if Q.girth2 < 0.004372139461 and Q.mass_top2 > 6.77991534008:
        z += -11.343112260131761 * (0.004372139461 - Q.girth2) * (Q.mass_top2 - 6.77991534008)
    if Q.mass < 41.377904891968 and Q.planar_flow < 0.322073846732:
        z += -0.08874084360832057 * (41.377904891968 - Q.mass) * (0.322073846732 - Q.planar_flow)
    if Q.e2 < 0.032346998155 and Q.tau21 < 0.446608647704:
        z += -158.01744697955266 * (0.032346998155 - Q.e2) * (0.446608647704 - Q.tau21)
    if Q.girth2 < 0.004372139461 and Q.n_dr_0p05_0p1 > 3.0:
        z += -133.38363417570608 * (0.004372139461 - Q.girth2) * (Q.n_dr_0p05_0p1 - 3.0)
    if Q.girth2 > 0.018827652745 and Q.pt_7 < 29.0421875:
        z += -8.321770293523969 * (Q.girth2 - 0.018827652745) * (29.0421875 - Q.pt_7)
    if Q.girth2 < 0.000964142894 and Q.mean_eta < 0.006823012256:
        z += -23660.662230702663 * (0.000964142894 - Q.girth2) * (0.006823012256 - Q.mean_eta)
    if Q.lam2 > 0.001130644719 and Q.mass_top2 > 16.308019673264:
        z += -2.727367404843335 * (Q.lam2 - 0.001130644719) * (Q.mass_top2 - 16.308019673264)
    if Q.centroid_offset < 0.009480684835 and Q.mean_phi2 < 0.002127561159:
        z += -6639.343374018258 * (0.009480684835 - Q.centroid_offset) * (0.002127561159 - Q.mean_phi2)
    if Q.e2 < 0.020459658932 and Q.pt_7 < 53.4375:
        z += -2.1961094952512212 * (0.020459658932 - Q.e2) * (53.4375 - Q.pt_7)
    if Q.girth2 > 0.018827652745 and Q.mean_eta < 0.02644207105:
        z += -383.44519584975734 * (Q.girth2 - 0.018827652745) * (0.02644207105 - Q.mean_eta)
    if Q.pt_5 < 35.5 and Q.min_pair_mass > 0.173071536962:
        z += -0.0037282639405020745 * (35.5 - Q.pt_5) * (Q.min_pair_mass - 0.173071536962)
    if Q.C2 > 0.051192347892 and Q.n_dr_0p05_0p1 > 1.0:
        z += -1.4713335248252406 * (Q.C2 - 0.051192347892) * (Q.n_dr_0p05_0p1 - 1.0)
    if Q.girth2 < 0.007520088344 and Q.mass_top3 > 28.345095968085:
        z += -12.607094323378988 * (0.007520088344 - Q.girth2) * (Q.mass_top3 - 28.345095968085)
    if Q.sum_pt > 988.4078125 and Q.dr_3 < 0.060129364309:
        z += 0.09416288794113825 * (Q.sum_pt - 988.4078125) * (0.060129364309 - Q.dr_3)
    if Q.sum_pt > 840.01953125 and Q.dr_2 > 0.057648924067:
        z += 0.033104935999062945 * (Q.sum_pt - 840.01953125) * (Q.dr_2 - 0.057648924067)
    if Q.centroid_offset < 0.018377780003 and Q.z_4 > 0.079416465542:
        z += 332.2026699882622 * (0.018377780003 - Q.centroid_offset) * (Q.z_4 - 0.079416465542)
    if Q.log_sum_pt > 6.377722943814 and Q.mean_phi > 0.026127964072:
        z += 19.053629361591227 * (Q.log_sum_pt - 6.377722943814) * (Q.mean_phi - 0.026127964072)
    if Q.log_sum_pt > 6.377722943814 and Q.dr_2 < 0.027807975573:
        z += 43.16444922140897 * (Q.log_sum_pt - 6.377722943814) * (0.027807975573 - Q.dr_2)
    if Q.lam1 < 0.005954149834 and Q.dr_2 < 0.027807975573:
        z += -3691.2828049360714 * (0.005954149834 - Q.lam1) * (0.027807975573 - Q.dr_2)
    if Q.log_sum_pt > 6.377722943814 and Q.mean_phi < -0.012753285235:
        z += 33.33440088207263 * (Q.log_sum_pt - 6.377722943814) * (-0.012753285235 - Q.mean_phi)
    if Q.z_dr_0p2_0p4 > 0.1009733513 and Q.dr_3 < 0.090460968459:
        z += 25.418853232030948 * (Q.z_dr_0p2_0p4 - 0.1009733513) * (0.090460968459 - Q.dr_3)
    if Q.n_dr_0p2_0p4 > 1.0 and Q.dr_6 > 0.216251221288:
        z += 1.957532105604514 * (Q.n_dr_0p2_0p4 - 1.0) * (Q.dr_6 - 0.216251221288)
    if Q.n_dr_0p2_0p4 > 1.0 and Q.n_pt_above_10 < 8.0:
        z += -0.10444444718086743 * (Q.n_dr_0p2_0p4 - 1.0) * (8.0 - Q.n_pt_above_10)
    if Q.girth2_top2 < 0.000759634834 and Q.z_4 < 0.102581170079:
        z += 4443.971711909197 * (0.000759634834 - Q.girth2_top2) * (0.102581170079 - Q.z_4)
    if Q.girth2_top2 < 0.000759634834 and Q.z_7 > 0.023207568189:
        z += -29632.29915962765 * (0.000759634834 - Q.girth2_top2) * (Q.z_7 - 0.023207568189)
    if Q.girth2_top2 < 0.000759634834 and Q.pt_7 > 33.21875:
        z += 42.456139615012376 * (0.000759634834 - Q.girth2_top2) * (Q.pt_7 - 33.21875)
    if Q.girth2 < 0.007520088344 and Q.pt_7 > 20.125:
        z += -2.2137032396431096 * (0.007520088344 - Q.girth2) * (Q.pt_7 - 20.125)
    if Q.mass < 29.644699859619 and Q.m01 > 6.779915340079:
        z += -0.01040722994071075 * (29.644699859619 - Q.mass) * (Q.m01 - 6.779915340079)
    if Q.girth2 > 0.018827652745 and Q.phi_1 > 0.088684082031:
        z += 53.62209888196973 * (Q.girth2 - 0.018827652745) * (Q.phi_1 - 0.088684082031)
    if Q.mass < 41.377904891968 and Q.centroid_offset < 0.026856224803:
        z += -7.057230480485259 * (41.377904891968 - Q.mass) * (0.026856224803 - Q.centroid_offset)
    if Q.e2 < 0.016554418951 and Q.centroid_offset < 0.023554160423:
        z += 10679.794131399867 * (0.016554418951 - Q.e2) * (0.023554160423 - Q.centroid_offset)
    if Q.girth2 < 0.004372139461 and Q.centroid_offset > 0.010960638421:
        z += -30485.405760369693 * (0.004372139461 - Q.girth2) * (Q.centroid_offset - 0.010960638421)
    if Q.log_sum_pt > 6.377722943814 and Q.centroid_offset > 0.02076709205:
        z += 78.54402288966742 * (Q.log_sum_pt - 6.377722943814) * (Q.centroid_offset - 0.02076709205)
    if Q.mass_over_sum_pt < 0.076373631775 and Q.girth2_top2 < 0.000759634834:
        z += -35966.04786777913 * (0.076373631775 - Q.mass_over_sum_pt) * (0.000759634834 - Q.girth2_top2)
    if Q.C2 > 0.051192347892 and Q.pt_2 < 84.625:
        z += 0.1738908448210168 * (Q.C2 - 0.051192347892) * (84.625 - Q.pt_2)
    if Q.centroid_offset < 0.009480684835 and Q.z_0 > 0.580417435819:
        z += -333.0995587184413 * (0.009480684835 - Q.centroid_offset) * (Q.z_0 - 0.580417435819)
    if Q.C2 > 0.051192347892 and Q.dr_5 < 0.208101322361:
        z += -40.27832857187681 * (Q.C2 - 0.051192347892) * (0.208101322361 - Q.dr_5)
    if Q.mass < 41.377904891968 and Q.pt_3 < 52.28125:
        z += 0.0009942531542037614 * (41.377904891968 - Q.mass) * (52.28125 - Q.pt_3)
    if Q.lam1 < 0.005954149834 and Q.mean_phi2 < 0.002127561159:
        z += -45139.26582463382 * (0.005954149834 - Q.lam1) * (0.002127561159 - Q.mean_phi2)
    if Q.e2 < 0.016554418951 and Q.phi_1 < 0.005035400391:
        z += 479.6277401356468 * (0.016554418951 - Q.e2) * (0.005035400391 - Q.phi_1)
    if Q.mass < 41.377904891968 and Q.dr_7 > 0.222994708167:
        z += -0.7625394239942125 * (41.377904891968 - Q.mass) * (Q.dr_7 - 0.222994708167)
    if Q.C2 > 0.051192347892 and Q.dr_7 < 0.222994708167:
        z += -31.12273145261105 * (Q.C2 - 0.051192347892) * (0.222994708167 - Q.dr_7)
    if Q.girth2 < 0.007520088344 and Q.m01 > 36.768271023571:
        z += 25.033905091549144 * (0.007520088344 - Q.girth2) * (Q.m01 - 36.768271023571)
    return max(0.0, z)


def neuron_10(Q):
    z = -0.09679492000256275
    z += 49.77958076835217 * Q.e2
    if Q.lam2 < 0.000194798295:
        z += 393.43359733218006 * Q.lam2 - 1.340974719804248
    if 0.000194798295 <= Q.lam2 < 0.003408388935:
        z += 1043.6237656905173 * Q.lam2 - 1.4676306560262151
    if Q.lam2 >= 0.003408388935:
        z += 650.1901683583372 * Q.lam2 - 0.12665593622196705
    if 0.303313749495 <= Q.LHA < 0.346713497427:
        z += -8.33702094372 * Q.LHA + 2.5287330820580567
    if Q.LHA >= 0.346713497427:
        z += -18.272109027357082 * Q.LHA + 5.973362218781181
    if Q.log_sum_pt < 6.267538488641:
        z += 1.4609437803715226 * Q.log_sum_pt - 9.156521373219201
    if Q.log_sum_pt >= 6.701242202626:
        z += -13.792893555899354 * Q.log_sum_pt + 92.42952039312095
    if 0.00231612516 <= Q.centroid_offset < 0.037760993714:
        z += 5.0642203022001295 * Q.centroid_offset - 0.011729368057708522
    if Q.centroid_offset >= 0.037760993714:
        z += 20.112362656650326 * Q.centroid_offset - 0.5799621769114796
    if Q.eccentricity >= 0.903125533696:
        z += 1.5671245276825538 * Q.eccentricity - 1.4153101754313984
    if Q.C2 >= 0.051192347892:
        z += 26.244795316894315 * Q.C2 - 1.3435326922167863
    if Q.n_dr_0p2_0p4 >= 2.0:
        z += 0.1833737084202136 * Q.n_dr_0p2_0p4 - 0.3667474168404272
    if Q.lam1 < 0.004183811014:
        z += 693.653699834462 * Q.lam1 - 3.2990608535571053
    if 0.004183811014 <= Q.lam1 < 0.006506575659:
        z += 170.89327803499128 * Q.lam1 - 1.1119300431491936
    if Q.lam1 >= 0.008375572068:
        z += -327.18475361153196 * Q.lam1 + 2.740359483424209
    if Q.mass_over_sum_pt < 0.090413827016:
        z += -27.227786877846277 * Q.mass_over_sum_pt + 2.7748305480656335
    if 0.090413827016 <= Q.mass_over_sum_pt < 0.107985668755:
        z += -17.816125362015782 * Q.mass_over_sum_pt + 1.9238862118401907
    if Q.n_dr_0p05_0p1 < 3.0:
        z += -0.12161414850470686 * Q.n_dr_0p05_0p1 + 0.3648424455141206
    if Q.tau32 < 0.269169217348:
        z += -3.717157883338997 * Q.tau32 + 1.000544478217306
    if Q.tau21 < 0.391541349888:
        z += -1.0909809302069178 * Q.tau21 + 0.4271641461152825
    if Q.girth2_top2 < 0.002412890926:
        z += -126.72291025855627 * Q.girth2_top2 + 0.4861089130286627
    if 0.002412890926 <= Q.girth2_top2 < 0.004007841607:
        z += -113.06954810440311 * Q.girth2_top2 + 0.4531648393775147
    if Q.phi_6 >= 0.05560760498:
        z += 0.489654180441903 * Q.phi_6 - 0.027228496242818985
    if Q.mass_over_sum_pt_sq < 0.003904593248:
        z += -204.30638493842076 * Q.mass_over_sum_pt_sq + 0.7977333311538466
    if 15.454033088684 <= Q.mass < 53.332374954224:
        z += 0.04041886459037869 * Q.mass - 0.6246344707867503
    if Q.mass >= 53.332374954224:
        z += 0.018860669594729984 * Q.mass + 0.5251152680574619
    if Q.max_dr >= 0.121680960059:
        z += -4.338334358893462 * Q.max_dr + 0.5278926898471028
    if Q.girth2 < 0.0016538364:
        z += 529.8013089213517 * Q.girth2 - 0.6528977953237205
    if 0.0016538364 <= Q.girth2 < 0.006679471442:
        z += -44.433567553522266 * Q.girth2 + 0.2967927455399298
    if Q.girth2 >= 0.008678044751:
        z += 377.2063578581626 * Q.girth2 - 3.2734136538548553
    if Q.pt_7 >= 45.75:
        z += -0.027200750655538286 * Q.pt_7 + 1.2444343424908766
    if Q.girth2_top5 < 0.002270363079:
        z += -151.63561506564176 * Q.girth2_top5 + 0.34426790190648926
    if Q.z_7 >= 0.06164517166:
        z += 7.219842096474167 * Q.z_7 - 0.4450684053952443
    if Q.sum_pt >= 813.415625:
        z += 0.010805042541164767 * Q.sum_pt - 8.788990431773126
    if Q.z_dr_0p2_0p4 >= 0.05643851608:
        z += -1.8464365472259487 * Q.z_dr_0p2_0p4 + 0.10421013876131138
    if Q.girth2_top3 < 0.001592177626:
        z += -294.59151610343724 * Q.girth2_top3 + 0.4690420207493115
    if Q.lam2 > 0.000194798295 and Q.planar_flow > 0.012569162668:
        z += -518.6718288941868 * (Q.lam2 - 0.000194798295) * (Q.planar_flow - 0.012569162668)
    if Q.centroid_offset > 0.00231612516 and Q.pt_7 < 34.53125:
        z += -1.2628439248660124 * (Q.centroid_offset - 0.00231612516) * (34.53125 - Q.pt_7)
    if Q.lam2 > 0.000194798295 and Q.n_pt_above_50 < 8.0:
        z += -25.249181495068353 * (Q.lam2 - 0.000194798295) * (8.0 - Q.n_pt_above_50)
    if Q.lam2 > 0.000194798295 and Q.z_top2_slots > 0.476619814198:
        z += 1844.9184615049985 * (Q.lam2 - 0.000194798295) * (Q.z_top2_slots - 0.476619814198)
    if Q.lam2 > 0.000194798295 and Q.pt_6 < 38.25:
        z += -22.267331519821084 * (Q.lam2 - 0.000194798295) * (38.25 - Q.pt_6)
    if Q.eccentricity > 0.903125533696 and Q.z_top2_slots > 0.55004856109:
        z += -31.980237175475246 * (Q.eccentricity - 0.903125533696) * (Q.z_top2_slots - 0.55004856109)
    if Q.mass_over_sum_pt < 0.090413827016 and Q.pt_7 > 33.21875:
        z += 0.4206045433412804 * (0.090413827016 - Q.mass_over_sum_pt) * (Q.pt_7 - 33.21875)
    if Q.lam2 > 0.000194798295 and Q.tau21 < 0.501026660204:
        z += 1164.0586941957956 * (Q.lam2 - 0.000194798295) * (0.501026660204 - Q.tau21)
    if Q.LHA > 0.303313749495 and Q.tau21 < 0.553068161011:
        z += -27.06666920798817 * (Q.LHA - 0.303313749495) * (0.553068161011 - Q.tau21)
    if Q.eccentricity > 0.903125533696 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += 121.6409315737093 * (Q.eccentricity - 0.903125533696) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.tau32 < 0.269169217348 and Q.n_dr_0p2_0p4 < 2.0:
        z += -1.2861686192899704 * (0.269169217348 - Q.tau32) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.n_dr_0p2_0p4 > 2.0 and Q.dr_7 > 0.222994708167:
        z += 3.5984686286189103 * (Q.n_dr_0p2_0p4 - 2.0) * (Q.dr_7 - 0.222994708167)
    if Q.lam1 < 0.004183811014 and Q.mean_phi > 0.009050007537:
        z += 8268.407374171453 * (0.004183811014 - Q.lam1) * (Q.mean_phi - 0.009050007537)
    if Q.tau21 < 0.391541349888 and Q.mean_phi < -0.009352574684:
        z += -34.04401410754116 * (0.391541349888 - Q.tau21) * (-0.009352574684 - Q.mean_phi)
    if Q.tau21 < 0.391541349888 and Q.mean_eta < -0.006779838586:
        z += -36.97923679614431 * (0.391541349888 - Q.tau21) * (-0.006779838586 - Q.mean_eta)
    if Q.tau21 < 0.391541349888 and Q.pt_4 > 39.8125:
        z += -0.05077566367864961 * (0.391541349888 - Q.tau21) * (Q.pt_4 - 39.8125)
    if Q.n_dr_0p05_0p1 < 3.0 and Q.D2 < 1.432482242584:
        z += -0.06218519420887958 * (3.0 - Q.n_dr_0p05_0p1) * (1.432482242584 - Q.D2)
    if Q.n_dr_0p2_0p4 > 2.0 and Q.dr_7 < 0.042151962757:
        z += 26.273492620116116 * (Q.n_dr_0p2_0p4 - 2.0) * (0.042151962757 - Q.dr_7)
    if Q.C2 > 0.051192347892 and Q.dr_7 < 0.222994708167:
        z += -44.67615680189908 * (Q.C2 - 0.051192347892) * (0.222994708167 - Q.dr_7)
    if Q.lam2 > 0.000194798295 and Q.D2 < 2.055451202393:
        z += -68.00920898621882 * (Q.lam2 - 0.000194798295) * (2.055451202393 - Q.D2)
    if Q.lam1 < 0.004183811014 and Q.dr_7 < 0.175465903809:
        z += -620.5142016302472 * (0.004183811014 - Q.lam1) * (0.175465903809 - Q.dr_7)
    if Q.tau21 < 0.391541349888 and Q.z_4 > 0.075444822386:
        z += 41.72106617068283 * (0.391541349888 - Q.tau21) * (Q.z_4 - 0.075444822386)
    if Q.C2 > 0.051192347892 and Q.pt_3 < 45.059375:
        z += -1.1900954980828828 * (Q.C2 - 0.051192347892) * (45.059375 - Q.pt_3)
    if Q.lam1 < 0.004183811014 and Q.sum_pt > 988.4078125:
        z += -0.3012614621260923 * (0.004183811014 - Q.lam1) * (Q.sum_pt - 988.4078125)
    if Q.lam1 < 0.004183811014 and Q.log_sum_pt > 6.701242202626:
        z += 1507.109270988939 * (0.004183811014 - Q.lam1) * (Q.log_sum_pt - 6.701242202626)
    if Q.mass > 15.454033088684 and Q.n_dr_0p2_0p4 < 2.0:
        z += -0.005391459258135001 * (Q.mass - 15.454033088684) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.max_dr > 0.121680960059 and Q.mean_phi > -0.003096654534:
        z += 35.04341287278146 * (Q.max_dr - 0.121680960059) * (Q.mean_phi - -0.003096654534)
    if Q.phi_6 > 0.05560760498 and Q.eta_7 < -0.121826171875:
        z += 34.937381741150325 * (Q.phi_6 - 0.05560760498) * (-0.121826171875 - Q.eta_7)
    if Q.eccentricity > 0.903125533696 and Q.mass_top2 < 36.768271023571:
        z += -0.155902402926813 * (Q.eccentricity - 0.903125533696) * (36.768271023571 - Q.mass_top2)
    if Q.tau21 < 0.391541349888 and Q.dr01 < 0.251215918102:
        z += 4.190643690563547 * (0.391541349888 - Q.tau21) * (0.251215918102 - Q.dr01)
    if Q.phi_6 > 0.05560760498 and Q.mean_eta > -0.009391680919:
        z += 73.62258624427895 * (Q.phi_6 - 0.05560760498) * (Q.mean_eta - -0.009391680919)
    if Q.mass > 15.454033088684 and Q.eta_7 < 0.121951293945:
        z += -0.005484096825512097 * (Q.mass - 15.454033088684) * (0.121951293945 - Q.eta_7)
    if Q.C2 > 0.051192347892 and Q.eta_4 > -0.050323486328:
        z += 17.807448620831963 * (Q.C2 - 0.051192347892) * (Q.eta_4 - -0.050323486328)
    if Q.girth2_top2 < 0.002412890926 and Q.mean_phi2 > 0.004331280361:
        z += 24340.528718472287 * (0.002412890926 - Q.girth2_top2) * (Q.mean_phi2 - 0.004331280361)
    if Q.C2 > 0.051192347892 and Q.pt1_over_pt0 < 0.213129110777:
        z += 113.64251248514704 * (Q.C2 - 0.051192347892) * (0.213129110777 - Q.pt1_over_pt0)
    if Q.centroid_offset > 0.00231612516 and Q.phi_4 > 0.072021484375:
        z += 34.712664002836625 * (Q.centroid_offset - 0.00231612516) * (Q.phi_4 - 0.072021484375)
    if Q.centroid_offset > 0.00231612516 and Q.eta_6 > -0.116455078125:
        z += 16.42720939863932 * (Q.centroid_offset - 0.00231612516) * (Q.eta_6 - -0.116455078125)
    if Q.log_sum_pt < 6.267538488641 and Q.eta_3 < -0.047210693359:
        z += -1.850295886132585 * (6.267538488641 - Q.log_sum_pt) * (-0.047210693359 - Q.eta_3)
    if Q.z_dr_0p2_0p4 > 0.05643851608 and Q.phi_2 > 0.064147949219:
        z += -0.7254459397734507 * (Q.z_dr_0p2_0p4 - 0.05643851608) * (Q.phi_2 - 0.064147949219)
    if Q.log_sum_pt < 6.267538488641 and Q.min_pair_mass > 0.173071536962:
        z += -0.06409264695867023 * (6.267538488641 - Q.log_sum_pt) * (Q.min_pair_mass - 0.173071536962)
    if Q.log_sum_pt > 6.701242202626 and Q.pt_dispersion < 0.443545366824:
        z += 24.623755283184323 * (Q.log_sum_pt - 6.701242202626) * (0.443545366824 - Q.pt_dispersion)
    if Q.lam1 > 0.008375572068 and Q.dr_5 < 0.037867470435:
        z += 3718.7074445564263 * (Q.lam1 - 0.008375572068) * (0.037867470435 - Q.dr_5)
    if Q.C2 > 0.051192347892 and Q.dr_5 < 0.16311139345:
        z += -54.51169485911656 * (Q.C2 - 0.051192347892) * (0.16311139345 - Q.dr_5)
    if Q.mass > 53.332374954224 and Q.eta_3 > 0.101684570312:
        z += 0.03896058956857473 * (Q.mass - 53.332374954224) * (Q.eta_3 - 0.101684570312)
    if Q.phi_6 > 0.05560760498 and Q.eta_2 < -0.095520019531:
        z += 48.55396380762672 * (Q.phi_6 - 0.05560760498) * (-0.095520019531 - Q.eta_2)
    if Q.log_sum_pt < 6.267538488641 and Q.eta_2 < -0.095520019531:
        z += -12.18368580644568 * (6.267538488641 - Q.log_sum_pt) * (-0.095520019531 - Q.eta_2)
    if Q.lam1 > 0.008375572068 and Q.dr_3 < 0.068547137772:
        z += 1021.0277589913144 * (Q.lam1 - 0.008375572068) * (0.068547137772 - Q.dr_3)
    if Q.z_7 > 0.06164517166 and Q.min_pair_mass > 1.096883408173:
        z += 0.6555107021072217 * (Q.z_7 - 0.06164517166) * (Q.min_pair_mass - 1.096883408173)
    if Q.lam1 > 0.008375572068 and Q.min_pair_mass < 2.801373397908:
        z += 7.611529447523367 * (Q.lam1 - 0.008375572068) * (2.801373397908 - Q.min_pair_mass)
    if Q.log_sum_pt > 6.701242202626 and Q.max_pair_mass < 25.327486904849:
        z += -0.06210277191485147 * (Q.log_sum_pt - 6.701242202626) * (25.327486904849 - Q.max_pair_mass)
    return max(0.0, z)


def neuron_11(Q):
    z = 0.5056883934507649
    if Q.planar_flow < 0.253403707141:
        z += -8.646815182972285 * Q.planar_flow + 2.1911350223282615
    if Q.LHA < 0.154689112391:
        z += -8.789899103697252 * Q.LHA + 0.8865403276676833
    if 0.154689112391 <= Q.LHA < 0.196739721581:
        z += 11.252188061099787 * Q.LHA - 2.213752346317824
    if Q.girth < 0.02054281719:
        z += 196.4504739475655 * Q.girth - 8.433351863742166
    if 0.02054281719 <= Q.girth < 0.076081777364:
        z += 65.93885110351205 * Q.girth - 5.752275454486547
    if 0.076081777364 <= Q.girth < 0.087236513197:
        z += 15.388836079546074 * Q.girth - 1.9063404656863128
    if 0.087236513197 <= Q.girth < 0.101940929517:
        z += -50.550015023965976 * Q.girth + 3.8459349888002343
    if Q.girth >= 0.101940929517:
        z += -1.7178080946027237 * Q.girth - 1.1320655759455436
    if Q.centroid_offset < 0.014379521101:
        z += -24.942068492670764 * Q.centroid_offset + 2.0443388976613006
    if 0.014379521101 <= Q.centroid_offset < 0.037760993714:
        z += -57.097783020764986 * Q.centroid_offset + 2.506722673235764
    if 0.037760993714 <= Q.centroid_offset < 0.049903668404:
        z += -36.683026116927955 * Q.centroid_offset + 1.7358411661171358
    if Q.centroid_offset >= 0.049903668404:
        z += 4.282677668836975 * Q.centroid_offset - 0.30849773154416504
    if Q.girth2_top2 < 0.001056655216:
        z += 77.53276822945321 * Q.girth2_top2 - 0.08192540396057083
    if Q.n_dr_0p1_0p2 < 2.0:
        z += 0.1590009845313607 * Q.n_dr_0p1_0p2 - 0.44530425584992006
    if 2.0 <= Q.n_dr_0p1_0p2 < 3.0:
        z += 0.12730228678719868 * Q.n_dr_0p1_0p2 - 0.38190686036159605
    if Q.width < 0.000172198326:
        z += 4205.560265254838 * Q.width + 6.474337818398316
    if 0.000172198326 <= Q.width < 0.003562611091:
        z += -671.8960329723169 * Q.width + 7.314227628091189
    if 0.003562611091 <= Q.width < 0.008678044951:
        z += -961.8975640562987 * Q.width + 8.347390299137963
    if Q.e2_sq < 0.006390124748:
        z += 886.6264913914143 * Q.e2_sq - 5.665653884872686
    if Q.n_dr_0_0p05 < 7.0:
        z += 0.12341629904566709 * Q.n_dr_0_0p05 - 0.8639140933196696
    if Q.e2 < 0.007078157854:
        z += 47.39279109578339 * Q.e2 - 2.343133434811669
    if 0.007078157854 <= Q.e2 < 0.04447356835:
        z += 53.687865747825384 * Q.e2 - 2.3876909669015363
    if Q.girth2 < 0.006679471442:
        z += -1106.672495800288 * Q.girth2 + 9.379361724834592
    if 0.006679471442 <= Q.girth2 < 0.013238675334:
        z += -302.990183902291 * Q.girth2 + 4.011188674071383
    if Q.lam1 < 0.004839980301:
        z += 695.287111228378 * Q.lam1 - 4.567665635616083
    if 0.004839980301 <= Q.lam1 < 0.008375572068:
        z += 340.1098862586921 * Q.lam1 - 2.848614863398958
    if Q.mass_top5 < 4.959630489142:
        z += -0.062322394963725936 * Q.mass_top5 + 0.3596914859925067
    if 4.959630489142 <= Q.mass_top5 < 9.257203159811:
        z += -0.011773026229288996 * Q.mass_top5 + 0.10898529561031188
    if Q.mass < 15.454033088684:
        z += -0.13601708369327525 * Q.mass + 2.3770232251314716
    if 15.454033088684 <= Q.mass < 21.784077072144:
        z += -0.04344530840984362 * Q.mass + 0.9464159468230994
    if Q.pt_7 < 29.0421875:
        z += 0.02941762922955604 * Q.pt_7 - 0.8543523038902471
    if Q.z_dr_0p05_0p1 >= 0.846033477783:
        z += 3.3063845502715594 * Q.z_dr_0p05_0p1 - 2.797312019954228
    if Q.sum_pt_top5 < 687.4375:
        z += -0.004086653397052942 * Q.sum_pt_top5 + 2.8093187946365816
    if Q.girth2_top3 < 0.002151567843:
        z += 86.57415658429596 * Q.girth2_top3 - 0.18627017134161794
    if Q.C2 < 0.011899968609:
        z += -20.03840177284684 * Q.C2 - 0.04613941440962893
    if 0.011899968609 <= Q.C2 < 0.035786485299:
        z += 11.914494280372878 * Q.C2 - 0.4263778744095836
    if Q.girth2_top5 < 0.000657050184:
        z += 382.8613807535627 * Q.girth2_top5 - 0.2515591406706224
    if Q.max_dr < 0.111761856824:
        z += 4.816256247431625 * Q.max_dr + 0.20308126769922707
    if 0.111761856824 <= Q.max_dr < 0.221586732566:
        z += -6.750337788625984 * Q.max_dr + 1.4957852942984298
    if Q.m01 >= 45.595:
        z += 0.0007510615621413308 * Q.m01 - 0.03424465192583398
    if Q.log_sum_pt < 6.701242202626:
        z += 0.9145851944394963 * Q.log_sum_pt - 6.128856902874858
    if Q.planar_flow < 0.253403707141 and Q.width > 0.006096650059:
        z += -1066.1668852797432 * (0.253403707141 - Q.planar_flow) * (Q.width - 0.006096650059)
    if Q.planar_flow < 0.253403707141 and Q.D2 < 1.679198372364:
        z += 1.4112141375135865 * (0.253403707141 - Q.planar_flow) * (1.679198372364 - Q.D2)
    if Q.planar_flow < 0.253403707141 and Q.girth2 > 0.013238675334:
        z += 1006.504972213056 * (0.253403707141 - Q.planar_flow) * (Q.girth2 - 0.013238675334)
    if Q.planar_flow < 0.253403707141 and Q.mass < 69.611351776123:
        z += -0.12431380694492822 * (0.253403707141 - Q.planar_flow) * (69.611351776123 - Q.mass)
    if Q.planar_flow < 0.253403707141 and Q.max_dr > 0.102758520097:
        z += -7.581361654983407 * (0.253403707141 - Q.planar_flow) * (Q.max_dr - 0.102758520097)
    if Q.centroid_offset < 0.049903668404 and Q.pt_7 < 48.71875:
        z += -0.6409398086482533 * (0.049903668404 - Q.centroid_offset) * (48.71875 - Q.pt_7)
    if Q.centroid_offset < 0.049903668404 and Q.n_dr_0p05_0p1 > 2.0:
        z += 2.1069975538952184 * (0.049903668404 - Q.centroid_offset) * (Q.n_dr_0p05_0p1 - 2.0)
    if Q.centroid_offset < 0.049903668404 and Q.log_sum_pt < 6.804164030582:
        z += -61.759271026180635 * (0.049903668404 - Q.centroid_offset) * (6.804164030582 - Q.log_sum_pt)
    if Q.e2_sq < 0.006390124748 and Q.D2 < 1.332146394253:
        z += -231.15204454325757 * (0.006390124748 - Q.e2_sq) * (1.332146394253 - Q.D2)
    if Q.centroid_offset < 0.049903668404 and Q.mean_phi2 < 0.001570267399:
        z += -3281.287611851196 * (0.049903668404 - Q.centroid_offset) * (0.001570267399 - Q.mean_phi2)
    if Q.width < 0.003562611091 and Q.C2 > 0.030867108516:
        z += 17804.649299470824 * (0.003562611091 - Q.width) * (Q.C2 - 0.030867108516)
    if Q.centroid_offset < 0.049903668404 and Q.mean_phi < -0.000855675264:
        z += 397.8757626896328 * (0.049903668404 - Q.centroid_offset) * (-0.000855675264 - Q.mean_phi)
    if Q.planar_flow < 0.253403707141 and Q.z_6 < 0.034484056668:
        z += -117.0986319148598 * (0.253403707141 - Q.planar_flow) * (0.034484056668 - Q.z_6)
    if Q.LHA < 0.154689112391 and Q.z_7 < 0.028070914944:
        z += 701.58020125249 * (0.154689112391 - Q.LHA) * (0.028070914944 - Q.z_7)
    if Q.girth > 0.076081777364 and Q.n_pt_above_50 < 7.0:
        z += 4.840015944115635 * (Q.girth - 0.076081777364) * (7.0 - Q.n_pt_above_50)
    if Q.mass < 15.454033088684 and Q.phi_1 < -0.058901977539:
        z += 12.177167726631296 * (15.454033088684 - Q.mass) * (-0.058901977539 - Q.phi_1)
    if Q.sum_pt_top5 < 687.4375 and Q.n_dr_0p2_0p4 < 2.0:
        z += -5.363422224036185e-05 * (687.4375 - Q.sum_pt_top5) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.girth2 < 0.013238675334 and Q.mass_top5 > 49.186182222392:
        z += 7.3412151902434175 * (0.013238675334 - Q.girth2) * (Q.mass_top5 - 49.186182222392)
    if Q.e2_sq < 0.006390124748 and Q.phi_0 > 0.079772949219:
        z += -4042.784338648564 * (0.006390124748 - Q.e2_sq) * (Q.phi_0 - 0.079772949219)
    if Q.pt_7 < 29.0421875 and Q.mass_top2 < 22.844978847276:
        z += 0.0002342247868227787 * (29.0421875 - Q.pt_7) * (22.844978847276 - Q.mass_top2)
    if Q.centroid_offset > 0.014379521101 and Q.pt_5 < 29.875:
        z += 1.035882156567851 * (Q.centroid_offset - 0.014379521101) * (29.875 - Q.pt_5)
    if Q.mass_top5 < 9.257203159811 and Q.eta_0 < -0.053314208984:
        z += 0.46229117469124503 * (9.257203159811 - Q.mass_top5) * (-0.053314208984 - Q.eta_0)
    if Q.girth2_top3 < 0.002151567843 and Q.phi_0 > -0.029769897461:
        z += 3395.978466972672 * (0.002151567843 - Q.girth2_top3) * (Q.phi_0 - -0.029769897461)
    if Q.max_dr < 0.221586732566 and Q.phi_0 < 0.021438598633:
        z += 20.431303113970444 * (0.221586732566 - Q.max_dr) * (0.021438598633 - Q.phi_0)
    if Q.e2 < 0.04447356835 and Q.pt_5 > 43.0625:
        z += -0.08079277966430709 * (0.04447356835 - Q.e2) * (Q.pt_5 - 43.0625)
    if Q.n_dr_0_0p05 < 7.0 and Q.z_1st < 0.500737345219:
        z += 0.12647711587635513 * (7.0 - Q.n_dr_0_0p05) * (0.500737345219 - Q.z_1st)
    if Q.pt_7 < 29.0421875 and Q.n_dr_0p2_0p4 < 2.0:
        z += -0.017360524660261945 * (29.0421875 - Q.pt_7) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.girth < 0.087236513197 and Q.mean_eta < -0.026655913051:
        z += -2169.8275718265877 * (0.087236513197 - Q.girth) * (-0.026655913051 - Q.mean_eta)
    if Q.mass < 15.454033088684 and Q.mean_phi < -0.012753285235:
        z += 1.314858370174079 * (15.454033088684 - Q.mass) * (-0.012753285235 - Q.mean_phi)
    if Q.e2_sq < 0.006390124748 and Q.eta_0 < -0.020553588867:
        z += 5305.681113535324 * (0.006390124748 - Q.e2_sq) * (-0.020553588867 - Q.eta_0)
    if Q.girth2 < 0.013238675334 and Q.eta_0 < -0.013826751709:
        z += -954.4701795909372 * (0.013238675334 - Q.girth2) * (-0.013826751709 - Q.eta_0)
    if Q.girth2_top3 < 0.002151567843 and Q.pt_7 < 48.71875:
        z += 12.826507655528644 * (0.002151567843 - Q.girth2_top3) * (48.71875 - Q.pt_7)
    if Q.girth > 0.101940929517 and Q.n_pt_above_50 < 7.0:
        z += -5.942598678176637 * (Q.girth - 0.101940929517) * (7.0 - Q.n_pt_above_50)
    if Q.girth > 0.076081777364 and Q.z_dr_0p1_0p2 < 0.20502409339:
        z += 45.41796994995326 * (Q.girth - 0.076081777364) * (0.20502409339 - Q.z_dr_0p1_0p2)
    if Q.log_sum_pt < 6.701242202626 and Q.z_dr_0p2_0p4 < 0.05643851608:
        z += -16.667927989855087 * (6.701242202626 - Q.log_sum_pt) * (0.05643851608 - Q.z_dr_0p2_0p4)
    if Q.girth > 0.076081777364 and Q.pt_7 < 40.040625:
        z += 0.45307553468819606 * (Q.girth - 0.076081777364) * (40.040625 - Q.pt_7)
    if Q.m01 > 45.595 and Q.n_pt_above_50 > 6.0:
        z += 0.015585586766860615 * (Q.m01 - 45.595) * (Q.n_pt_above_50 - 6.0)
    if Q.sum_pt_top5 < 687.4375 and Q.D2 < 0.74595130682:
        z += -0.0027250764135260397 * (687.4375 - Q.sum_pt_top5) * (0.74595130682 - Q.D2)
    if Q.centroid_offset > 0.014379521101 and Q.C2 < 0.009171459824:
        z += -4347.944196320954 * (Q.centroid_offset - 0.014379521101) * (0.009171459824 - Q.C2)
    if Q.planar_flow < 0.253403707141 and Q.n_pt_above_50 < 7.0:
        z += 0.15552379932273652 * (0.253403707141 - Q.planar_flow) * (7.0 - Q.n_pt_above_50)
    if Q.LHA < 0.154689112391 and Q.C2 > 0.02102663191:
        z += -316.62905649454365 * (0.154689112391 - Q.LHA) * (Q.C2 - 0.02102663191)
    if Q.lam1 < 0.004839980301 and Q.mean_phi > 0.026127964072:
        z += -29502.963401712364 * (0.004839980301 - Q.lam1) * (Q.mean_phi - 0.026127964072)
    if Q.e2_sq < 0.006390124748 and Q.mean_phi > 0.001618889696:
        z += 14388.4440283121 * (0.006390124748 - Q.e2_sq) * (Q.mean_phi - 0.001618889696)
    if Q.e2 < 0.04447356835 and Q.pt1_dr01 > 28.393960910299:
        z += -5.601955441359763 * (0.04447356835 - Q.e2) * (Q.pt1_dr01 - 28.393960910299)
    if Q.width < 0.008678044951 and Q.phi_0 < -0.054077148438:
        z += -3001.3821186439704 * (0.008678044951 - Q.width) * (-0.054077148438 - Q.phi_0)
    if Q.e2_sq < 0.006390124748 and Q.mean_phi < -9.3112965e-05:
        z += 10504.102571711965 * (0.006390124748 - Q.e2_sq) * (-9.3112965e-05 - Q.mean_phi)
    if Q.girth2 < 0.013238675334 and Q.mean_phi > 0.002834883542:
        z += -4377.032732620365 * (0.013238675334 - Q.girth2) * (Q.mean_phi - 0.002834883542)
    if Q.mass < 15.454033088684 and Q.phi_0 > 0.002076053619:
        z += -0.09137254452252819 * (15.454033088684 - Q.mass) * (Q.phi_0 - 0.002076053619)
    if Q.girth2 < 0.013238675334 and Q.mean_phi < -0.001813532785:
        z += -2573.3551543956473 * (0.013238675334 - Q.girth2) * (-0.001813532785 - Q.mean_phi)
    if Q.log_sum_pt < 6.701242202626 and Q.dr_0 < 0.016755406876:
        z += 116.24670858698803 * (6.701242202626 - Q.log_sum_pt) * (0.016755406876 - Q.dr_0)
    if Q.log_sum_pt < 6.701242202626 and Q.dr_0 < 0.111955475493:
        z += -7.2146112053217735 * (6.701242202626 - Q.log_sum_pt) * (0.111955475493 - Q.dr_0)
    if Q.C2 < 0.011899968609 and Q.phi_6 < -0.11682434082:
        z += 1565.7093736679712 * (0.011899968609 - Q.C2) * (-0.11682434082 - Q.phi_6)
    if Q.mass < 21.784077072144 and Q.mean_phi < -0.006701702951:
        z += -4.4888467232349285 * (21.784077072144 - Q.mass) * (-0.006701702951 - Q.mean_phi)
    if Q.centroid_offset > 0.014379521101 and Q.tau21 < 0.112473037094:
        z += 177.27367051661275 * (Q.centroid_offset - 0.014379521101) * (0.112473037094 - Q.tau21)
    if Q.mass < 21.784077072144 and Q.mean_phi > 0.004406178184:
        z += -2.3200571230845526 * (21.784077072144 - Q.mass) * (Q.mean_phi - 0.004406178184)
    if Q.log_sum_pt < 6.701242202626 and Q.mean_phi < 0.026127964072:
        z += -3.8118496744131107 * (6.701242202626 - Q.log_sum_pt) * (0.026127964072 - Q.mean_phi)
    if Q.planar_flow < 0.253403707141 and Q.n_dr_0p1_0p2 < 3.0:
        z += -0.5884280884174586 * (0.253403707141 - Q.planar_flow) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.girth2 < 0.006679471442 and Q.eta_7 > 0.041320800781:
        z += 292.99123738772937 * (0.006679471442 - Q.girth2) * (Q.eta_7 - 0.041320800781)
    if Q.centroid_offset > 0.037760993714 and Q.D2 > 0.74595130682:
        z += 9.302408206084408 * (Q.centroid_offset - 0.037760993714) * (Q.D2 - 0.74595130682)
    if Q.mass < 21.784077072144 and Q.D2 < 1.332146394253:
        z += 0.09043938035119936 * (21.784077072144 - Q.mass) * (1.332146394253 - Q.D2)
    return max(0.0, z)


def neuron_12(Q):
    z = -0.3412427296322808
    if Q.girth2 >= 0.018827652745:
        z += 272.5217499172195 * Q.girth2 - 5.130944872901141
    if Q.mass >= 91.19:
        z += 0.05047352392524954 * Q.mass - 4.602680646743505
    if Q.mass_over_sum_pt >= 0.13092863437:
        z += -41.13420607644422 * Q.mass_over_sum_pt + 5.385645427482998
    if Q.girth2_top2 >= 0.0140332421:
        z += 6.4083855236162455 * Q.girth2_top2 - 0.08993042552304203
    if Q.e2 >= 0.063441075385:
        z += -34.410585197115054 * Q.e2 + 2.1830445295321415
    if Q.mean_phi >= 0.026127964072:
        z += 10.918857809038096 * Q.mean_phi - 0.285287524541824
    if Q.n_dr_0p2_0p4 >= 1.0:
        z += 0.18502653021486903 * Q.n_dr_0p2_0p4 - 0.18502653021486903
    if Q.girth2 > 0.018827652745 and Q.lam2 > 0.000537286005:
        z += 7324.805972884395 * (Q.girth2 - 0.018827652745) * (Q.lam2 - 0.000537286005)
    if Q.mass > 91.19 and Q.max_pair_mass < 45.595:
        z += 0.0008283205313745285 * (Q.mass - 91.19) * (45.595 - Q.max_pair_mass)
    if Q.girth2 > 0.018827652745 and Q.pt_7 > 15.55390625:
        z += 2.5910316982261254 * (Q.girth2 - 0.018827652745) * (Q.pt_7 - 15.55390625)
    if Q.girth2 > 0.018827652745 and Q.mass < 80.4:
        z += -4.18194368445501 * (Q.girth2 - 0.018827652745) * (80.4 - Q.mass)
    if Q.girth2_top2 > 0.0140332421 and Q.z_6 < 0.089100391399:
        z += -986.8622050277936 * (Q.girth2_top2 - 0.0140332421) * (0.089100391399 - Q.z_6)
    if Q.n_dr_0p2_0p4 > 1.0 and Q.lam2 < 0.003408388935:
        z += -60.537510375668816 * (Q.n_dr_0p2_0p4 - 1.0) * (0.003408388935 - Q.lam2)
    if Q.mass > 91.19 and Q.eta_5 < 0.112243652344:
        z += 0.028757970977605032 * (Q.mass - 91.19) * (0.112243652344 - Q.eta_5)
    if Q.girth2_top2 > 0.0140332421 and Q.width > 0.013238675006:
        z += -1018.9977298786463 * (Q.girth2_top2 - 0.0140332421) * (Q.width - 0.013238675006)
    if Q.n_dr_0p2_0p4 > 1.0 and Q.mean_eta < -0.017909069173:
        z += 4.0683668508247175 * (Q.n_dr_0p2_0p4 - 1.0) * (-0.017909069173 - Q.mean_eta)
    if Q.mass > 91.19 and Q.eta_3 < -0.066412353516:
        z += -0.0628327373286351 * (Q.mass - 91.19) * (-0.066412353516 - Q.eta_3)
    if Q.mass > 91.19 and Q.centroid_offset > 0.02076709205:
        z += 0.5867180935012872 * (Q.mass - 91.19) * (Q.centroid_offset - 0.02076709205)
    return max(0.0, z)


def neuron_13(Q):
    z = 2.32686965833201
    if Q.girth < 0.101940929517:
        z += -44.07390119243446 * Q.girth + 6.540937957624523
    if 0.101940929517 <= Q.girth < 0.148408418149:
        z += -18.172016823094182 * Q.girth + 3.900475788772122
    if Q.girth >= 0.148408418149:
        z += 25.90188436934028 * Q.girth - 2.6404621688524013
    if Q.lam1 < 0.006506575659:
        z += -544.2608427005356 * Q.lam1 + 5.283030524205068
    if 0.006506575659 <= Q.lam1 < 0.016433749775:
        z += -175.45337198585864 * Q.lam1 + 2.8833568123955957
    if Q.sum_pt_top5 < 531.1875:
        z += -0.004623577087153219 * Q.sum_pt_top5 + 2.4559863539822007
    if 658.125 <= Q.sum_pt_top5 < 839.9546875:
        z += 0.0021824191881318414 * Q.sum_pt_top5 - 1.4363046281892682
    if 839.9546875 <= Q.sum_pt_top5 < 902.40625:
        z += 0.00815078850154833 * Q.sum_pt_top5 - 6.449464409724604
    if Q.sum_pt_top5 >= 902.40625:
        z += 0.015150228448487853 * Q.sum_pt_top5 - 12.7658027643425
    if Q.lam2 < 0.000306123359:
        z += 363.3090328094205 * Q.lam2 - 0.11121738147866102
    if Q.e2 < 0.050284641981:
        z += 65.31112976204689 * Q.e2 - 3.2841467774591617
    if Q.pt_6 < 31.90625:
        z += 0.05665435689950615 * Q.pt_6 - 1.807628074824868
    if Q.z_top5_slots >= 0.930764273368:
        z += -20.868506370182306 * Q.z_top5_slots + 19.423660167918214
    if Q.z_7 < 0.028070914944:
        z += 0.20282638548165366 * Q.z_7 + 0.4447391791927398
    if 0.028070914944 <= Q.z_7 < 0.055577157257:
        z += -16.375653798232946 * Q.z_7 + 0.9101122863305818
    if Q.tau21 < 0.501026660204:
        z += 0.5634144741207177 * Q.tau21 - 0.28228567227929613
    if Q.C2 >= 0.067292226106:
        z += -11.682980177692315 * Q.C2 + 0.7861737437091872
    if Q.z_6 < 0.067272114405:
        z += -10.455031544631977 * Q.z_6 + 0.7033320781783662
    if Q.centroid_offset < 0.037760993714:
        z += -19.760845267035414 * Q.centroid_offset + 0.7461891539118509
    if Q.LHA >= 0.09323897448:
        z += -7.230156890806506 * Q.LHA + 0.6741324138283039
    if Q.width < 0.003562611091:
        z += 374.7448881331393 * Q.width - 1.657816354118344
    if 0.003562611091 <= Q.width < 0.00752008842:
        z += 323.35862447183047 * Q.width - 1.4747470812735148
    if 0.00752008842 <= Q.width < 0.013238675006:
        z += -167.33826649874678 * Q.width + 2.215336926244326
    if Q.z_top5 >= 0.877015459538:
        z += -5.1450267100196285 * Q.z_top5 + 4.512267964423149
    if Q.pt_5 < 24.578125:
        z += 0.08879692380014603 * Q.pt_5 - 2.182461892775464
    if Q.mass >= 53.332374954224:
        z += -0.02540725976837166 * Q.mass + 1.3550295045261678
    if Q.sum_pt < 763.825:
        z += 0.0033179103547809063 * Q.sum_pt - 2.534302876740526
    if Q.sum_pt >= 988.4078125:
        z += -0.023803398855307023 * Q.sum_pt + 23.52746539263902
    if Q.pt_7 < 25.578125:
        z += 0.07896771712887585 * Q.pt_7 - 2.0198461396870275
    if Q.girth < 0.148408418149 and Q.log_sum_pt < 6.804164030582:
        z += -46.58755912922974 * (0.148408418149 - Q.girth) * (6.804164030582 - Q.log_sum_pt)
    if Q.girth < 0.148408418149 and Q.pt_7 < 38.53125:
        z += -1.0831738817626022 * (0.148408418149 - Q.girth) * (38.53125 - Q.pt_7)
    if Q.sum_pt_top5 > 658.125 and Q.z_7 > 0.023207568189:
        z += -0.07933901635922613 * (Q.sum_pt_top5 - 658.125) * (Q.z_7 - 0.023207568189)
    if Q.lam2 < 0.000306123359 and Q.centroid_offset < 0.049903668404:
        z += -54559.073771063435 * (0.000306123359 - Q.lam2) * (0.049903668404 - Q.centroid_offset)
    if Q.sum_pt_top5 > 658.125 and Q.pt_7 < 43.5:
        z += 0.00044423583077146667 * (Q.sum_pt_top5 - 658.125) * (43.5 - Q.pt_7)
    if Q.girth < 0.148408418149 and Q.lam2 > 0.003408388935:
        z += -2191.225345647603 * (0.148408418149 - Q.girth) * (Q.lam2 - 0.003408388935)
    if Q.lam1 < 0.016433749775 and Q.pt_6 < 56.53125:
        z += -2.051343987128169 * (0.016433749775 - Q.lam1) * (56.53125 - Q.pt_6)
    if Q.e2 < 0.050284641981 and Q.pt_dispersion > 0.396830244362:
        z += 25.38794121799683 * (0.050284641981 - Q.e2) * (Q.pt_dispersion - 0.396830244362)
    if Q.sum_pt_top5 > 658.125 and Q.z_dr_0p05_0p1 > 0.048758227378:
        z += -0.0017917345155655795 * (Q.sum_pt_top5 - 658.125) * (Q.z_dr_0p05_0p1 - 0.048758227378)
    if Q.sum_pt_top5 > 658.125 and Q.tau32 < 0.362731824815:
        z += -0.01698434111084346 * (Q.sum_pt_top5 - 658.125) * (0.362731824815 - Q.tau32)
    if Q.lam1 < 0.016433749775 and Q.centroid_offset < 0.037760993714:
        z += -3612.357632429428 * (0.016433749775 - Q.lam1) * (0.037760993714 - Q.centroid_offset)
    if Q.girth < 0.148408418149 and Q.mean_phi < -0.000855675264:
        z += -97.60425737409402 * (0.148408418149 - Q.girth) * (-0.000855675264 - Q.mean_phi)
    if Q.sum_pt_top5 > 902.40625 and Q.D2 < 3.885568320751:
        z += -0.002661049542206806 * (Q.sum_pt_top5 - 902.40625) * (3.885568320751 - Q.D2)
    if Q.sum_pt_top5 > 839.9546875 and Q.z_dr_0p1_0p2 < 0.15855820179:
        z += 0.011220779195945774 * (Q.sum_pt_top5 - 839.9546875) * (0.15855820179 - Q.z_dr_0p1_0p2)
    if Q.tau21 < 0.501026660204 and Q.max_dr > 0.015595615841:
        z += -3.0551721622960466 * (0.501026660204 - Q.tau21) * (Q.max_dr - 0.015595615841)
    if Q.sum_pt_top5 > 902.40625 and Q.n_pt_above_50 > 6.0:
        z += -0.006116873594237404 * (Q.sum_pt_top5 - 902.40625) * (Q.n_pt_above_50 - 6.0)
    if Q.sum_pt_top5 > 839.9546875 and Q.n_pt_above_50 > 2.0:
        z += -8.191066444851458e-05 * (Q.sum_pt_top5 - 839.9546875) * (Q.n_pt_above_50 - 2.0)
    if Q.sum_pt_top5 < 531.1875 and Q.z_4 < 0.037477688199:
        z += -1.591940707546705 * (531.1875 - Q.sum_pt_top5) * (0.037477688199 - Q.z_4)
    if Q.centroid_offset < 0.037760993714 and Q.z_dr_0p2_0p4 > 0.1009733513:
        z += -26.287502822058762 * (0.037760993714 - Q.centroid_offset) * (Q.z_dr_0p2_0p4 - 0.1009733513)
    if Q.width < 0.003562611091 and Q.n_pt_above_50 > 7.0:
        z += 108.830279834842 * (0.003562611091 - Q.width) * (Q.n_pt_above_50 - 7.0)
    if Q.girth > 0.101940929517 and Q.pt_1 < 116.0:
        z += -0.26879486747202463 * (Q.girth - 0.101940929517) * (116.0 - Q.pt_1)
    if Q.sum_pt_top5 < 531.1875 and Q.pt_5 < 29.875:
        z += 0.0008628394134575501 * (531.1875 - Q.sum_pt_top5) * (29.875 - Q.pt_5)
    if Q.lam1 < 0.006506575659 and Q.z_dr_0p05_0p1 > 0.163898047805:
        z += 170.8857162810324 * (0.006506575659 - Q.lam1) * (Q.z_dr_0p05_0p1 - 0.163898047805)
    if Q.mass > 53.332374954224 and Q.z_dr_0p05_0p1 > 0.588259786367:
        z += -0.042949065026846256 * (Q.mass - 53.332374954224) * (Q.z_dr_0p05_0p1 - 0.588259786367)
    if Q.sum_pt < 763.825 and Q.z_4 < 0.037477688199:
        z += 2.2869893350456323 * (763.825 - Q.sum_pt) * (0.037477688199 - Q.z_4)
    if Q.width < 0.00752008842 and Q.m012 > 16.899120053094:
        z += -3.9379513235774084 * (0.00752008842 - Q.width) * (Q.m012 - 16.899120053094)
    if Q.girth > 0.101940929517 and Q.pt_4 > 81.375:
        z += 0.5636498390176712 * (Q.girth - 0.101940929517) * (Q.pt_4 - 81.375)
    if Q.sum_pt > 988.4078125 and Q.n_pt_above_50 > 6.0:
        z += 0.007651855376025196 * (Q.sum_pt - 988.4078125) * (Q.n_pt_above_50 - 6.0)
    if Q.e2 < 0.050284641981 and Q.n_pt_above_50 < 5.0:
        z += 2.7147912111372534 * (0.050284641981 - Q.e2) * (5.0 - Q.n_pt_above_50)
    if Q.girth > 0.101940929517 and Q.pt_balance01 < 0.476255698625:
        z += 40.97734731543674 * (Q.girth - 0.101940929517) * (0.476255698625 - Q.pt_balance01)
    if Q.sum_pt > 988.4078125 and Q.D2 < 3.885568320751:
        z += 0.003924292181181954 * (Q.sum_pt - 988.4078125) * (3.885568320751 - Q.D2)
    return max(0.0, z)


def neuron_14(Q):
    z = -1.1821023115897025
    if Q.planar_flow < 0.111513564951:
        z += -2.0627108267969696 * Q.planar_flow + 0.23002023775915478
    if Q.z_dr_0p05_0p1 < 0.588259786367:
        z += -0.2951161300130881 * Q.z_dr_0p05_0p1 + 0.17360495159495504
    if Q.z_dr_0p05_0p1 >= 0.750909513235:
        z += -4.329734764132372 * Q.z_dr_0p05_0p1 + 3.251239024171297
    if 0.002464291268 <= Q.lam1 < 0.004183811014:
        z += -275.659667842809 * Q.lam1 + 0.6793057124048146
    if 0.004183811014 <= Q.lam1 < 0.00543336053:
        z += 446.9045068844995 * Q.lam1 - 2.343766240141119
    if 0.00543336053 <= Q.lam1 < 0.005954149834:
        z += 794.531996146222 * Q.lam1 - 4.232551719438761
    if 0.005954149834 <= Q.lam1 < 0.007330079875:
        z += 284.76757601385486 * Q.lam1 - 1.1973379819285208
    if 0.007330079875 <= Q.lam1 < 0.008375572068:
        z += 90.34422426972924 * Q.lam1 + 0.22780071592114048
    if 0.008375572068 <= Q.lam1 < 0.012003726523:
        z += 29.148836534269776 * Q.lam1 + 0.7403470961286828
    if Q.lam1 >= 0.012003726523:
        z += 19.19984704695321 * Q.lam1 + 0.8597720451146352
    if Q.max_dr < 0.080507021025:
        z += -1.6518823768080182 * Q.max_dr - 0.31370712479523244
    if 0.080507021025 <= Q.max_dr < 0.177304983139:
        z += 4.614717544463019 * Q.max_dr - 0.8182124164122632
    if Q.mass < 69.611351776123:
        z += 0.01635602412246584 * Q.mass - 0.992826350402336
    if 69.611351776123 <= Q.mass < 76.655700683594:
        z += -0.006440878835896058 * Q.mass + 0.5940968808383331
    if 76.655700683594 <= Q.mass < 86.4:
        z += -0.010300053128048603 * Q.mass + 0.8899245902633993
    if Q.girth2 < 0.004372139461:
        z += -899.2114513481761 * Q.girth2 + 8.49585048073558
    if 0.004372139461 <= Q.girth2 < 0.013238675334:
        z += -514.7864595475638 * Q.girth2 + 6.815090804289522
    if Q.width < 0.006096650059:
        z += 878.354444415081 * Q.width - 4.407352938128589
    if 0.006096650059 <= Q.width < 0.00752008842:
        z += -44.44888045147343 * Q.width + 1.218656006864486
    if 0.00752008842 <= Q.width < 0.008678044951:
        z += -763.7562136599724 * Q.width + 6.627910753746801
    if Q.e2 < 0.035560912266:
        z += -42.133270070052774 * Q.e2 + 1.48969538300361
    if 0.035560912266 <= Q.e2 < 0.038466955721:
        z += -62.19930227094102 * Q.e2 + 2.203261793626128
    if 0.038466955721 <= Q.e2 < 0.041109715588:
        z += -19.111080265807573 * Q.e2 + 0.5457890656580417
    if 0.041109715588 <= Q.e2 < 0.04447356835:
        z += -35.792431730303974 * Q.e2 + 1.2315546799869561
    if 0.04447356835 <= Q.e2 < 0.050284641981:
        z += 61.995855131064786 * Q.e2 - 3.1174393795715347
    if Q.mass_over_sum_pt_sq < 0.008174660116:
        z += 554.8959195499446 * Q.mass_over_sum_pt_sq - 5.169566432415977
    if 0.008174660116 <= Q.mass_over_sum_pt_sq < 0.011660904657:
        z += 181.70867903551948 * Q.mass_over_sum_pt_sq - 2.1188875815826074
    if Q.girth < 0.033604209498:
        z += 48.80766795569579 * Q.girth - 5.2831466263503915
    if 0.033604209498 <= Q.girth < 0.087236513197:
        z += 67.9255462846414 * Q.girth - 5.925587814873554
    if Q.D2 < 0.74595130682:
        z += 0.51863216392303 * Q.D2 - 0.5668405265390764
    if 0.74595130682 <= Q.D2 < 1.122624260187:
        z += 0.47777836049317557 * Q.D2 - 0.536365578482009
    if Q.n_dr_0p05_0p1 < 5.0:
        z += 0.05557691597687153 * Q.n_dr_0p05_0p1 - 0.27788457988435766
    if 0.012587644117 <= Q.centroid_offset < 0.031170772021:
        z += -11.654744505524832 * Q.centroid_offset + 0.14670577611010774
    if 0.031170772021 <= Q.centroid_offset < 0.049903668404:
        z += 6.5334668044970385 * Q.centroid_offset - 0.42023481210435776
    if Q.centroid_offset >= 0.049903668404:
        z += 3.1847211872596404 * Q.centroid_offset - 0.2531201212523943
    if Q.e2_sq < 0.005834489329:
        z += -658.1136398643976 * Q.e2_sq + 4.622865213066776
    if 0.005834489329 <= Q.e2_sq < 0.017162483186:
        z += -69.13035210772887 * Q.e2_sq + 1.1864485056911562
    if Q.LHA < 0.303313749495:
        z += -6.575076749213622 * Q.LHA + 1.9943111820213795
    if Q.z_dr_0_0p05 >= 0.608073231578:
        z += -0.6038976331919912 * Q.z_dr_0_0p05 + 0.3672139853573597
    if Q.C2 < 0.067292226106:
        z += 0.23824776774245038 * Q.C2 - 0.016032222656174742
    if Q.tau21 < 0.135767506063:
        z += -2.0536923879699316 * Q.tau21 + 0.27882469373524466
    if Q.sum_pt_top3 < 309.625:
        z += -0.0009809806642806507 * Q.sum_pt_top3 + 0.30373613817789646
    if Q.planar_flow < 0.111513564951 and Q.centroid_offset > 0.018377780003:
        z += -529.478856618954 * (0.111513564951 - Q.planar_flow) * (Q.centroid_offset - 0.018377780003)
    if Q.planar_flow < 0.111513564951 and Q.z_dr_0p1_0p2 < 0.258290868998:
        z += 10.247188257530723 * (0.111513564951 - Q.planar_flow) * (0.258290868998 - Q.z_dr_0p1_0p2)
    if Q.planar_flow < 0.111513564951 and Q.max_dr < 0.15984864831:
        z += -81.97748092281489 * (0.111513564951 - Q.planar_flow) * (0.15984864831 - Q.max_dr)
    if Q.planar_flow < 0.111513564951 and Q.sum_pt < 739.5:
        z += -0.012176876718925644 * (0.111513564951 - Q.planar_flow) * (739.5 - Q.sum_pt)
    if Q.z_dr_0p05_0p1 < 0.588259786367 and Q.C2 < 0.067292226106:
        z += -6.295444218720002 * (0.588259786367 - Q.z_dr_0p05_0p1) * (0.067292226106 - Q.C2)
    if Q.lam1 > 0.007330079875 and Q.max_dr < 0.13261153996:
        z += 15908.196546211311 * (Q.lam1 - 0.007330079875) * (0.13261153996 - Q.max_dr)
    if Q.lam1 > 0.008375572068 and Q.max_dr < 0.13261153996:
        z += -24275.90743711801 * (Q.lam1 - 0.008375572068) * (0.13261153996 - Q.max_dr)
    if Q.planar_flow < 0.111513564951 and Q.max_dr < 0.102758520097:
        z += 171.76944442446788 * (0.111513564951 - Q.planar_flow) * (0.102758520097 - Q.max_dr)
    if Q.lam1 > 0.00543336053 and Q.max_dr < 0.15984864831:
        z += 3792.062390405016 * (Q.lam1 - 0.00543336053) * (0.15984864831 - Q.max_dr)
    if Q.planar_flow < 0.111513564951 and Q.centroid_offset > 0.009480684835:
        z += 452.5139580486562 * (0.111513564951 - Q.planar_flow) * (Q.centroid_offset - 0.009480684835)
    if Q.z_dr_0p05_0p1 < 0.588259786367 and Q.eccentricity > 0.970449631164:
        z += -1.0151463186104195 * (0.588259786367 - Q.z_dr_0p05_0p1) * (Q.eccentricity - 0.970449631164)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.n_dr_0p2_0p4 < 1.0:
        z += 5.043343418759868 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.z_dr_0p05_0p1 < 0.588259786367 and Q.n_dr_0p1_0p2 < 3.0:
        z += 0.23775101666413434 * (0.588259786367 - Q.z_dr_0p05_0p1) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.planar_flow < 0.111513564951 and Q.n_dr_0p2_0p4 > 0.0:
        z += -1.2483368454778656 * (0.111513564951 - Q.planar_flow) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.mass < 76.655700683594 and Q.D2 < 0.74595130682:
        z += -0.010644905010408934 * (76.655700683594 - Q.mass) * (0.74595130682 - Q.D2)
    if Q.width < 0.00752008842 and Q.planar_flow < 0.111513564951:
        z += -3287.5495661680625 * (0.00752008842 - Q.width) * (0.111513564951 - Q.planar_flow)
    if Q.girth2 < 0.013238675334 and Q.eccentricity > 0.970449631164:
        z += 4438.293238366234 * (0.013238675334 - Q.girth2) * (Q.eccentricity - 0.970449631164)
    if Q.girth2 < 0.004372139461 and Q.D2 < 0.87567204833:
        z += -1609.8380073404596 * (0.004372139461 - Q.girth2) * (0.87567204833 - Q.D2)
    if Q.width < 0.00752008842 and Q.D2 < 1.002470755577:
        z += -1325.126305927101 * (0.00752008842 - Q.width) * (1.002470755577 - Q.D2)
    if Q.mass < 76.655700683594 and Q.n_dr_0p1_0p2 > 4.0:
        z += 0.00157039750115473 * (76.655700683594 - Q.mass) * (Q.n_dr_0p1_0p2 - 4.0)
    if Q.e2 < 0.038466955721 and Q.D2 < 1.002470755577:
        z += -163.08299692218048 * (0.038466955721 - Q.e2) * (1.002470755577 - Q.D2)
    if Q.D2 < 1.122624260187 and Q.centroid_offset < 0.031170772021:
        z += 19.77838221357115 * (1.122624260187 - Q.D2) * (0.031170772021 - Q.centroid_offset)
    if Q.planar_flow < 0.111513564951 and Q.phi_7 > 0.057647705078:
        z += 7.049735022809443 * (0.111513564951 - Q.planar_flow) * (Q.phi_7 - 0.057647705078)
    if Q.planar_flow < 0.111513564951 and Q.sum_pt > 840.01953125:
        z += -0.014170820822162256 * (0.111513564951 - Q.planar_flow) * (Q.sum_pt - 840.01953125)
    if Q.girth2 < 0.013238675334 and Q.phi_5 < -0.074035644531:
        z += -238.02553791456168 * (0.013238675334 - Q.girth2) * (-0.074035644531 - Q.phi_5)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.eccentricity > 0.984196588116:
        z += -138.37835215951483 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (Q.eccentricity - 0.984196588116)
    if Q.width < 0.00752008842 and Q.log_sum_pt < 6.804164030582:
        z += 47.16178235387201 * (0.00752008842 - Q.width) * (6.804164030582 - Q.log_sum_pt)
    if Q.width < 0.008678044951 and Q.D2 < 1.002470755577:
        z += -788.4433107534248 * (0.008678044951 - Q.width) * (1.002470755577 - Q.D2)
    if Q.girth2 < 0.013238675334 and Q.D2 < 1.002470755577:
        z += 161.8586114902846 * (0.013238675334 - Q.girth2) * (1.002470755577 - Q.D2)
    if Q.width < 0.00752008842 and Q.n_dr_0p1_0p2 < 3.0:
        z += 73.32639608294642 * (0.00752008842 - Q.width) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.girth2 < 0.004372139461 and Q.n_dr_0p2_0p4 < 1.0:
        z += 82.7423726332562 * (0.004372139461 - Q.girth2) * (1.0 - Q.n_dr_0p2_0p4)
    if Q.girth2 < 0.013238675334 and Q.n_dr_0p1_0p2 < 3.0:
        z += -26.548894012456685 * (0.013238675334 - Q.girth2) * (3.0 - Q.n_dr_0p1_0p2)
    if Q.e2_sq < 0.017162483186 and Q.pt1_dr01 > 22.385778388206:
        z += 0.8318411969312365 * (0.017162483186 - Q.e2_sq) * (Q.pt1_dr01 - 22.385778388206)
    if Q.width < 0.00752008842 and Q.mass_top3 > 23.663861485439:
        z += -13.357485205722696 * (0.00752008842 - Q.width) * (Q.mass_top3 - 23.663861485439)
    if Q.girth2 < 0.013238675334 and Q.mass_top3 > 23.663861485439:
        z += 3.9813376128072377 * (0.013238675334 - Q.girth2) * (Q.mass_top3 - 23.663861485439)
    if Q.girth2 < 0.013238675334 and Q.centroid_offset > 0.031170772021:
        z += -7666.672359036581 * (0.013238675334 - Q.girth2) * (Q.centroid_offset - 0.031170772021)
    if Q.e2_sq < 0.005834489329 and Q.D2 < 0.87567204833:
        z += 1070.189955080185 * (0.005834489329 - Q.e2_sq) * (0.87567204833 - Q.D2)
    if Q.e2 < 0.035560912266 and Q.D2 < 0.87567204833:
        z += -29.567070626513356 * (0.035560912266 - Q.e2) * (0.87567204833 - Q.D2)
    if Q.lam1 > 0.004183811014 and Q.D2 > 0.415245993435:
        z += -676.3074004975313 * (Q.lam1 - 0.004183811014) * (Q.D2 - 0.415245993435)
    if Q.lam1 > 0.002464291268 and Q.D2 > 0.415245993435:
        z += 477.64551164533805 * (Q.lam1 - 0.002464291268) * (Q.D2 - 0.415245993435)
    if Q.width < 0.006096650059 and Q.mean_phi < -0.025945045147:
        z += 11822.505308049473 * (0.006096650059 - Q.width) * (-0.025945045147 - Q.mean_phi)
    if Q.centroid_offset > 0.012587644117 and Q.z_4 < 0.047491459878:
        z += -602.7282812467472 * (Q.centroid_offset - 0.012587644117) * (0.047491459878 - Q.z_4)
    if Q.width < 0.008678044951 and Q.dr01 > 0.141033647649:
        z += -4108.369338260503 * (0.008678044951 - Q.width) * (Q.dr01 - 0.141033647649)
    if Q.e2 < 0.041109715588 and Q.dr01 > 0.055953954317:
        z += 267.33975698705797 * (0.041109715588 - Q.e2) * (Q.dr01 - 0.055953954317)
    if Q.e2_sq < 0.017162483186 and Q.phi_1 > 0.088684082031:
        z += 411.8282116608688 * (0.017162483186 - Q.e2_sq) * (Q.phi_1 - 0.088684082031)
    if Q.width < 0.006096650059 and Q.mean_eta < -0.026655913051:
        z += 9792.012554582803 * (0.006096650059 - Q.width) * (-0.026655913051 - Q.mean_eta)
    if Q.z_dr_0_0p05 > 0.608073231578 and Q.phi_4 < -0.02555847168:
        z += -3.409318213041388 * (Q.z_dr_0_0p05 - 0.608073231578) * (-0.02555847168 - Q.phi_4)
    if Q.width < 0.006096650059 and Q.mean_eta > 0.02644207105:
        z += 18804.43929825064 * (0.006096650059 - Q.width) * (Q.mean_eta - 0.02644207105)
    if Q.lam1 > 0.007330079875 and Q.D2 > 0.415245993435:
        z += 160.097977968598 * (Q.lam1 - 0.007330079875) * (Q.D2 - 0.415245993435)
    if Q.e2_sq < 0.017162483186 and Q.phi_6 < -0.075933837891:
        z += -90.4485969784772 * (0.017162483186 - Q.e2_sq) * (-0.075933837891 - Q.phi_6)
    if Q.girth2 < 0.013238675334 and Q.mean_eta > 0.017724257335:
        z += -1465.826870324427 * (0.013238675334 - Q.girth2) * (Q.mean_eta - 0.017724257335)
    if Q.e2_sq < 0.017162483186 and Q.phi_7 < -0.124209594727:
        z += -123.54690021712257 * (0.017162483186 - Q.e2_sq) * (-0.124209594727 - Q.phi_7)
    if Q.z_dr_0_0p05 > 0.608073231578 and Q.eta_5 < -0.113525390625:
        z += -6.029445866489269 * (Q.z_dr_0_0p05 - 0.608073231578) * (-0.113525390625 - Q.eta_5)
    if Q.e2 < 0.035560912266 and Q.phi_3 < -0.033630371094:
        z += -63.36239576722881 * (0.035560912266 - Q.e2) * (-0.033630371094 - Q.phi_3)
    if Q.width < 0.006096650059 and Q.D2 < 1.002470755577:
        z += 2063.862719990604 * (0.006096650059 - Q.width) * (1.002470755577 - Q.D2)
    if Q.lam1 > 0.005954149834 and Q.D2 > 1.679198372364:
        z += 338.6955301378898 * (Q.lam1 - 0.005954149834) * (Q.D2 - 1.679198372364)
    if Q.e2 < 0.041109715588 and Q.D2 < 1.002470755577:
        z += 270.9278518283155 * (0.041109715588 - Q.e2) * (1.002470755577 - Q.D2)
    if Q.lam1 > 0.002464291268 and Q.D2 > 1.679198372364:
        z += -211.1496478593557 * (Q.lam1 - 0.002464291268) * (Q.D2 - 1.679198372364)
    return max(0.0, z)


def neuron_15(Q):
    z = -1.7498587052402512
    if Q.tau21 < 0.23799610585:
        z += -0.7794683287389315 * Q.tau21 + 0.18551042687327332
    if Q.width < 0.006096650059:
        z += 476.39363757296303 * Q.width + 0.10078778969070668
    if 0.006096650059 <= Q.width < 0.006679471358:
        z += 626.7666607576317 * Q.width - 0.8159839109801119
    if 0.006679471358 <= Q.width < 0.00752008842:
        z += -71.76692519917026 * Q.width + 3.8498511690193777
    if 0.00752008842 <= Q.width < 0.013238675006:
        z += -578.8419036959025 * Q.width + 7.663099842884403
    if Q.girth2 < 0.018827652745:
        z += -151.50898197488192 * Q.girth2 + 2.852558500371541
    if Q.lam1 < 0.00543336053:
        z += -301.5928291612504 * Q.lam1 - 0.03530109879306975
    if 0.00543336053 <= Q.lam1 < 0.006506575659:
        z += 25.41559712051395 * Q.lam1 - 1.812055775129823
    if 0.006506575659 <= Q.lam1 < 0.008375572068:
        z += 542.499542371801 * Q.lam1 - 5.176501586961535
    if 0.008375572068 <= Q.lam1 < 0.012003726523:
        z += 174.40204953168046 * Q.lam1 - 2.0934745076289927
    if Q.lam2 < 0.000306123359:
        z += -112.45014507080896 * Q.lam2 + 0.028037203953884454
    if 0.000306123359 <= Q.lam2 < 0.001130644719:
        z += -131.7441591069447 * Q.lam2 + 0.033943552339219474
    if 0.001130644719 <= Q.lam2 < 0.003408388935:
        z += 50.49394247441842 * Q.lam2 - 0.17210299481433428
    if 0.176724128067 <= Q.LHA < 0.280934097202:
        z += -2.0955112633864585 * Q.LHA + 0.3703274008765495
    if 0.280934097202 <= Q.LHA < 0.312727471086:
        z += -10.922529306099921 * Q.LHA + 2.850137745692021
    if 0.312727471086 <= Q.LHA < 0.346713497427:
        z += 3.326152989620379 * Q.LHA - 1.605816634956449
    if Q.LHA >= 0.346713497427:
        z += -18.846133243595876 * Q.LHA + 6.081614270914482
    if Q.e2_sq < 0.008168570676:
        z += 544.3669337164824 * Q.e2_sq - 5.159636322418249
    if 0.008168570676 <= Q.e2_sq < 0.011657374702:
        z += 204.34984176945966 * Q.e2_sq - 2.382182675801002
    if Q.mass_over_sum_pt_sq < 0.007182835724:
        z += -574.8463483917425 * Q.mass_over_sum_pt_sq + 4.129026887039158
    if Q.mass < 36.229410171509:
        z += -0.014380439587966976 * Q.mass + 0.5209948442790615
    if Q.mass >= 80.4:
        z += -0.014271319475014366 * Q.mass + 1.147414085791155
    if Q.e2 < 0.024547699839:
        z += -62.072124652016754 * Q.e2 + 0.9668084378697022
    if 0.024547699839 <= Q.e2 < 0.032346998155:
        z += 42.54591426825894 * Q.e2 - 1.6013237792900452
    if 0.032346998155 <= Q.e2 < 0.038466955721:
        z += -20.913848222759924 * Q.e2 + 0.4514090409236804
    if 0.038466955721 <= Q.e2 < 0.041109715588:
        z += -56.74159328465427 * Q.e2 + 1.8295933238028466
    if 0.041109715588 <= Q.e2 < 0.063441075385:
        z += 22.526054960918202 * Q.e2 - 1.429077150902265
    if Q.z_dr_0p05_0p1 >= 0.750909513235:
        z += -5.89687191125364 * Q.z_dr_0p05_0p1 + 4.428017216488614
    if Q.z_dr_0p1_0p2 < 0.328461505473:
        z += -1.2536369359297312 * Q.z_dr_0p1_0p2 + 0.18581127708530093
    if 0.328461505473 <= Q.z_dr_0p1_0p2 < 0.790636250377:
        z += 0.48890641623802367 * Q.z_dr_0p1_0p2 - 0.38654713571968785
    if Q.n_dr_0_0p05 < 2.0:
        z += -0.17325040339423303 * Q.n_dr_0_0p05 + 0.34650080678846606
    if Q.log_sum_pt >= 6.896095378249:
        z += 10.518661960811187 * Q.log_sum_pt - 72.53769613331359
    if Q.planar_flow < 0.083662731125:
        z += -4.389129603396668 * Q.planar_flow + 0.3672065698817533
    if Q.mass_over_sum_pt < 0.06813910019:
        z += 30.677637658285164 * Q.mass_over_sum_pt - 2.0903466259904095
    if Q.D2 < 0.74595130682:
        z += -0.015315988847305562 * Q.D2 + 0.011424981895888128
    if Q.n_dr_0p05_0p1 >= 5.0:
        z += -0.16252005637943512 * Q.n_dr_0p05_0p1 + 0.8126002818971756
    if Q.n_dr_0p1_0p2 < 1.0:
        z += -0.14896465566107508 * Q.n_dr_0p1_0p2 + 0.14896465566107508
    if Q.girth >= 0.033604209498:
        z += 27.89460767349533 * Q.girth - 0.9373762401246554
    if Q.girth2_top3 < 0.002151567843:
        z += 61.211518283244914 * Q.girth2_top3 - 0.13170073435943633
    if Q.girth2_top2 < 0.004007841607:
        z += 7.827134274647051 * Q.girth2_top2 + 0.08120331809167408
    if 0.004007841607 <= Q.girth2_top2 < 0.007639643088:
        z += -69.9917412714774 * Q.girth2_top2 + 0.39308904531538646
    if 0.007639643088 <= Q.girth2_top2 < 0.0140332421:
        z += 22.150728696080478 * Q.girth2_top2 - 0.3108465384835146
    if Q.z_1 < 0.113617043658:
        z += 2.10353937165155 * Q.z_1 - 0.23899792462525604
    if Q.tau21 < 0.23799610585 and Q.z_dr_0p05_0p1 < 0.588259786367:
        z += -2.818096072590209 * (0.23799610585 - Q.tau21) * (0.588259786367 - Q.z_dr_0p05_0p1)
    if Q.tau21 < 0.23799610585 and Q.max_dr < 0.121680960059:
        z += 35.94375854688194 * (0.23799610585 - Q.tau21) * (0.121680960059 - Q.max_dr)
    if Q.tau21 < 0.23799610585 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += 9.842239285367238 * (0.23799610585 - Q.tau21) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.tau21 < 0.23799610585 and Q.mass < 76.655700683594:
        z += -0.057810373031217 * (0.23799610585 - Q.tau21) * (76.655700683594 - Q.mass)
    if Q.tau21 < 0.23799610585 and Q.girth2_top5 > 0.00832969537:
        z += -31.427913183374635 * (0.23799610585 - Q.tau21) * (Q.girth2_top5 - 0.00832969537)
    if Q.width < 0.00752008842 and Q.e2 > 0.024547699839:
        z += -40157.94533710484 * (0.00752008842 - Q.width) * (Q.e2 - 0.024547699839)
    if Q.LHA > 0.176724128067 and Q.sum_pt_top3 > 353.0625:
        z += 0.015200219152319505 * (Q.LHA - 0.176724128067) * (Q.sum_pt_top3 - 353.0625)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.n_dr_0p2_0p4 < 2.0:
        z += 2.858486843263961 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (2.0 - Q.n_dr_0p2_0p4)
    if Q.z_dr_0p1_0p2 < 0.328461505473 and Q.n_dr_0p2_0p4 > 0.0:
        z += -0.35915044479814817 * (0.328461505473 - Q.z_dr_0p1_0p2) * (Q.n_dr_0p2_0p4 - 0.0)
    if Q.n_dr_0_0p05 < 2.0 and Q.pt_3 > 66.0:
        z += 0.0035653401928046335 * (2.0 - Q.n_dr_0_0p05) * (Q.pt_3 - 66.0)
    if Q.lam1 < 0.008375572068 and Q.m01 > 16.308019673264:
        z += -14.982415122638603 * (0.008375572068 - Q.lam1) * (Q.m01 - 16.308019673264)
    if Q.lam1 < 0.006506575659 and Q.pt1_dr01 > 1.21960336377:
        z += 6.408548123376015 * (0.006506575659 - Q.lam1) * (Q.pt1_dr01 - 1.21960336377)
    if Q.mass > 80.4 and Q.z_dr_0p2_0p4 < 0.20552001074:
        z += -0.08996192590529972 * (Q.mass - 80.4) * (0.20552001074 - Q.z_dr_0p2_0p4)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_4 < 0.04181499946:
        z += -13.676431725746141 * (Q.log_sum_pt - 6.896095378249) * (0.04181499946 - Q.dr_4)
    if Q.n_dr_0_0p05 < 2.0 and Q.pt_dispersion < 0.423827920854:
        z += -0.5844231358224476 * (2.0 - Q.n_dr_0_0p05) * (0.423827920854 - Q.pt_dispersion)
    if Q.log_sum_pt > 6.896095378249 and Q.mean_phi > 0.01746432744:
        z += -825.9929502166307 * (Q.log_sum_pt - 6.896095378249) * (Q.mean_phi - 0.01746432744)
    if Q.LHA > 0.176724128067 and Q.z_top5 > 0.865048766136:
        z += -22.90978266696186 * (Q.LHA - 0.176724128067) * (Q.z_top5 - 0.865048766136)
    if Q.width < 0.006096650059 and Q.log_sum_pt > 6.896095378249:
        z += -1697.5508901331334 * (0.006096650059 - Q.width) * (Q.log_sum_pt - 6.896095378249)
    if Q.girth2 < 0.018827652745 and Q.mass_top2 > 22.844978847276:
        z += 2.880911447494327 * (0.018827652745 - Q.girth2) * (Q.mass_top2 - 22.844978847276)
    if Q.z_dr_0p05_0p1 > 0.750909513235 and Q.planar_flow < 0.061262048692:
        z += -24.3843357498763 * (Q.z_dr_0p05_0p1 - 0.750909513235) * (0.061262048692 - Q.planar_flow)
    if Q.LHA > 0.176724128067 and Q.dr_7 < 0.042151962757:
        z += -54.10754723263267 * (Q.LHA - 0.176724128067) * (0.042151962757 - Q.dr_7)
    if Q.log_sum_pt > 6.896095378249 and Q.phi_0 < -0.029769897461:
        z += -74.60030513908615 * (Q.log_sum_pt - 6.896095378249) * (-0.029769897461 - Q.phi_0)
    if Q.width < 0.00752008842 and Q.planar_flow < 0.061262048692:
        z += -1541.5985506284949 * (0.00752008842 - Q.width) * (0.061262048692 - Q.planar_flow)
    if Q.D2 < 0.74595130682 and Q.pt_7 < 23.21640625:
        z += -0.133891426243963 * (0.74595130682 - Q.D2) * (23.21640625 - Q.pt_7)
    if Q.girth2_top2 < 0.007639643088 and Q.mean_phi < 0.001618889696:
        z += 636.8708384998665 * (0.007639643088 - Q.girth2_top2) * (0.001618889696 - Q.mean_phi)
    if Q.lam1 < 0.006506575659 and Q.dr01 > 0.055953954317:
        z += 1221.6745434883192 * (0.006506575659 - Q.lam1) * (Q.dr01 - 0.055953954317)
    if Q.n_dr_0p05_0p1 > 5.0 and Q.pt_dispersion > 0.432994687557:
        z += -0.698988377128444 * (Q.n_dr_0p05_0p1 - 5.0) * (Q.pt_dispersion - 0.432994687557)
    if Q.LHA > 0.312727471086 and Q.pt_dispersion < 0.456324180961:
        z += 101.45214400997372 * (Q.LHA - 0.312727471086) * (0.456324180961 - Q.pt_dispersion)
    if Q.LHA > 0.280934097202 and Q.pt_dispersion < 0.456324180961:
        z += -70.21511839401967 * (Q.LHA - 0.280934097202) * (0.456324180961 - Q.pt_dispersion)
    if Q.lam1 < 0.008375572068 and Q.D2 < 0.74595130682:
        z += -349.77783248263785 * (0.008375572068 - Q.lam1) * (0.74595130682 - Q.D2)
    if Q.z_1 < 0.113617043658 and Q.pt_5 > 73.75:
        z += -6.959947603433562 * (0.113617043658 - Q.z_1) * (Q.pt_5 - 73.75)
    if Q.log_sum_pt > 6.896095378249 and Q.dr_4 > 0.155114653206:
        z += -64.49060077226159 * (Q.log_sum_pt - 6.896095378249) * (Q.dr_4 - 0.155114653206)
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
