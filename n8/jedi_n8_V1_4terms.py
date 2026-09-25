"""JEDI-linear jet tagger, 8 particles, 3 features, written as a formula (V1, 4-term formulas).

Input:  the 8 hardest particles of a jet, hardest first, each (pT [GeV], Δη, Δφ) relative to the jet axis;
        empty slots have pT = 0.
Output: the class (g, q, W, Z or t), the 5 logits and the 5 probabilities.

1. quantities():  physics quantities of the particles.
2. jet_layer_4(): the 16 neurons of the network's last hidden layer, each max(0, z) with z built from if-statements.
3. logits():      the network's own last layer: each neuron is rounded to the network's fixed-point grid
                  (round to a multiple of 2^-f, then wrap modulo 2^i), multiplied by the weights, plus the biases.
4. classify():    softmax of the logits; the class is the largest logit.

Test set (50,000 jets of the hls4ml LHC jet dataset, test file): accuracy 61.7% (the network: 65.8%); same class as the network for 80.6% of jets.

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
  Q.mass_top5              mass of the 5 hardest particles [GeV]
  Q.max_dr                 largest distance ΔR of a particle from the jet axis
  Q.pt_7                   pT of particle 7 [GeV]
  Q.z_7                    pT of particle 7 / total pT
  Q.planar_flow            planar flow of the pT-weighted (Δη, Δφ) tensor
  Q.dr_0                   ΔR of particle 0 from the jet axis
  Q.sum_pt_top5            total pT of the 5 hardest particles [GeV]
  Q.girth2_top5            pT-weighted mean ΔR² of the 5 hardest particles
  Q.sum_pt                 total pT of the particles [GeV]
  Q.girth                  pT-weighted mean ΔR
  Q.girth2                 pT-weighted mean ΔR²
  Q.e2                     energy correlation e2 = Σ_{i<j} zᵢzⱼΔRᵢⱼ
  Q.e2_sq                  Σ_{i<j} zᵢzⱼΔRᵢⱼ²
  Q.lam1                   larger eigenvalue of the pT-weighted (Δη, Δφ) tensor
  Q.width                  λ1 + λ2 of the pT-weighted (Δη, Δφ) tensor
  Q.lam2                   smaller eigenvalue of the pT-weighted (Δη, Δφ) tensor
  Q.tau21                  N-subjettiness τ2/τ1 (axes from pT-weighted k-means)
  Q.centroid_offset        distance of the pT centroid from the jet axis
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
        mass_top5=mass_of(5),
        max_dr=max(dr[i] for i in real),
        pt_7=pt[7],
        z_7=z[7],
        planar_flow=4 * (ta * tc - tb ** 2) / max((ta + tc) ** 2, 1e-12),
        dr_0=dr[0] if pt[0] > 0 else 0.0,
        sum_pt_top5=sum(pt[:5]),
        girth2_top5=sum(pt[i] * dr[i] ** 2 for i in range(5)) / max(sum(pt[:5]), 1e-9),
        sum_pt=tot,
        girth=sum(z[i] * dr[i] for i in P),
        girth2=sum(z[i] * dr[i] ** 2 for i in P),
        e2=e2,
        e2_sq=sum(z[i] * z[j] * dist2(i, j) for i in P for j in P if i < j),
        lam1=lam1,
        width=ta + tc,
        lam2=lam2,
        tau21=tau(2) / max(tau(1), 1e-12),
        centroid_offset=math.hypot(sum(z[i] * eta[i] for i in P), sum(z[i] * phi[i] for i in P)),
    )


def neuron_0(Q):
    z = -0.11786458818183805
    if Q.e2_sq > 4.4131442e-05:
        z += 627.4668137467692 * math.exp(-((Q.girth2 - 0.004372139461) / 0.004013074139074726) ** 2) * (Q.e2_sq - 4.4131442e-05)
    z += -1.642589718390942 * math.exp(-((Q.girth2 - 0.006679471442) / 0.002006537069537363) ** 2) * math.exp(-((Q.e2 - 0.024547699839) / 0.012014812183974575) ** 2)
    if Q.eccentricity > 0.978160776925:
        z += 76.07032122027137 * math.exp(-((Q.lam1 - 0.006506575659) / 0.0035579998857043524) ** 2) * (Q.eccentricity - 0.978160776925)
    z += -1.0730922656085273 * math.exp(-((Q.mass_top5 - 22.1834155076) / 11.931780509663183) ** 2)
    return max(0.0, z)


def neuron_1(Q):
    z = 0.8526266165489794
    if Q.width < 0.008678044951:
        z += 846.4384467166523 * Q.width - 7.345430888861727
    if Q.e2_sq < 0.008168570676:
        z += -724.0701933439159 * Q.e2_sq + 5.9146185487147624
    if Q.pt_7 >= 33.21875:
        z += 0.048506521133702095 * Q.pt_7 - 1.6113259989101665
    if Q.width < 0.025305664527 and Q.mass > 53.332374954224:
        z += 3.684938135552683 * (0.025305664527 - Q.width) * (Q.mass - 53.332374954224)
    return max(0.0, z)


def neuron_2(Q):
    z = -5.046827660550755
    if Q.mass < 69.611351776123:
        z += -0.03425430824666386 * Q.mass + 2.384488701206269
    if Q.log_sum_pt >= 6.842716632804:
        z += 13.152458671668498 * Q.log_sum_pt - 89.99854771489323
    z += 1.7025219669939735 * math.exp(-((Q.dr_0 - 0.016755406876) / 0.022998003426677665) ** 2)
    z += 23.35340577212032 * math.sqrt(max(Q.z_7, 0.0))
    return max(0.0, z)


def neuron_3(Q):
    z = -0.3906307186932076
    if Q.girth >= 0.061086014472:
        z += 57.47953492212265 * Q.girth - 3.511195702096614
    if Q.LHA < 0.423592510895:
        z += 18.903351990619264 * math.exp(-((Q.width - 0.008678044951) / 0.0020065370690141317) ** 2) * (0.423592510895 - Q.LHA)
    if Q.e2 > 0.020459658932:
        z += -119.88260365641547 * math.exp(-((Q.girth2 - 0.007520088344) / 0.002006537069537363) ** 2) * (Q.e2 - 0.020459658932)
    if Q.lam1 > 0.007330079875 and Q.width < 0.025305664527:
        z += 30538.18767964688 * (Q.lam1 - 0.007330079875) * (0.025305664527 - Q.width)
    return max(0.0, z)


def neuron_4(Q):
    z = -0.4921430736550941
    if Q.tau21 < 0.197783735394:
        z += -7.594762482875103 * Q.tau21 + 1.5021204932932477
    if Q.mass > 8.379955863953:
        z += 0.06947632440059485 * math.exp(-((Q.mass_over_sum_pt_sq - 0.008174660116) / 0.0037855858872927308) ** 2) * (Q.mass - 8.379955863953)
    if Q.D2 < 1.002470755577:
        z += 3.6617239725263735 * math.exp(-((Q.lam1 - 0.016433749775) / 0.0035579998857043524) ** 2) * (1.002470755577 - Q.D2)
    z += 282.5989194409039 * Q.centroid_offset ** 2
    return max(0.0, z)


def neuron_5(Q):
    z = -0.3955928493066339
    if Q.log_sum_pt >= 6.896095378249:
        z += -8.751405095294036 * Q.log_sum_pt + 60.35052423084195
    if Q.z_7 < 0.043044721986:
        z += -90.92331109462212 * Q.z_7 + 3.9137686481145986
    if Q.LHA < 0.196739721581 and Q.width < 0.005019718802:
        z += 5489.914264068566 * (0.196739721581 - Q.LHA) * (0.005019718802 - Q.width)
    if Q.LHA < 0.38556468879 and Q.z_top5 > 0.75833107233:
        z += 76.12205708539298 * (0.38556468879 - Q.LHA) * (Q.z_top5 - 0.75833107233)
    return max(0.0, z)


def neuron_6(Q):
    z = -0.2850198460999476
    if Q.centroid_offset >= 0.008092360237:
        z += 46.06202949721788 * Q.centroid_offset - 0.372750535938807
    if Q.centroid_offset > 0.026856224803:
        z += 132.90181658805437 * (Q.centroid_offset - 0.026856224803) * math.exp(-((Q.girth2_top5 - 0.003279780165) / 0.003976205959301676) ** 2)
    if Q.log_sum_pt < 6.502799415134 and Q.sum_pt < 559.6875:
        z += 0.01838321882386296 * (6.502799415134 - Q.log_sum_pt) * (559.6875 - Q.sum_pt)
    z += 3.2724992449783854 * math.exp(-((Q.width - 0.013238675006) / 0.0040130741380282635) ** 2)
    return max(0.0, z)


def neuron_7(Q):
    z = -0.2936488886927746
    if Q.e2_sq < 0.004641800986:
        z += 894.4137194213401 * (0.004641800986 - Q.e2_sq) * math.exp(-((Q.LHA - 0.216055863061) / 0.052577351963363564) ** 2)
    if Q.mass_over_sum_pt_sq > 7.0126366e-05:
        z += -2257.753354506299 * math.exp(-((Q.width - 4.8108519e-05) / 0.0020065370690141317) ** 2) * (Q.mass_over_sum_pt_sq - 7.0126366e-05)
    z += 1.636557479512052 * math.exp(-((Q.lam1 - 0.007330079875) / 0.0035579998857043524) ** 2) * math.exp(-((Q.planar_flow - 0.00804883781) / 0.07503537023928272) ** 2)
    z += 3.929926299213026 * math.exp(-((Q.girth2 - 0.007520088344) / 0.004013074139074726) ** 2)
    return max(0.0, z)


def neuron_8(Q):
    z = -0.17861002568952664
    if Q.sum_pt_top5 >= 658.125:
        z += -0.001970303563661045 * Q.sum_pt_top5 + 1.2967060328344253
    z += -2.885581575367825 * math.exp(-((Q.mass_over_sum_pt_sq - 0.002073653798) / 0.0018927929436463654) ** 2) * math.exp(-((Q.width - 0.000964142901) / 0.0020065370690141317) ** 2)
    z += 13.075837053623589 * math.exp(-((Q.e2_sq - 0.003013300392) / 0.0018928076343462277) ** 2) * math.exp(-((Q.width - 9.1213921e-05) / 0.0020065370690141317) ** 2)
    z += 0.4040220152773636 * math.exp(-((Q.centroid_offset - 0.005576073186) / 0.008072572009885343) ** 2)
    return max(0.0, z)


def neuron_9(Q):
    z = -0.6896060934642969
    if Q.e2 < 0.028531698044:
        z += 288.78535984607805 * Q.e2 - 8.239536686656182
    if Q.lam2 >= 0.000537286005:
        z += 491.22709259177856 * Q.lam2 - 0.2639294421264018
    if Q.mass_over_sum_pt_sq < 0.00023679558:
        z += -14204.229271432061 * math.exp(-((Q.girth - 0.02054281719) / 0.010919112173384286) ** 2) * (0.00023679558 - Q.mass_over_sum_pt_sq)
    if Q.LHA < 0.423592510895 and Q.girth2 < 0.007520088344:
        z += 6704.779711682528 * (0.423592510895 - Q.LHA) * (0.007520088344 - Q.girth2)
    return max(0.0, z)


def neuron_10(Q):
    z = -0.349089290903962
    if Q.e2 >= 0.004157758062:
        z += 41.483355897090526 * Q.e2 - 0.17247775741994337
    if Q.C2 >= 0.067292226106:
        z += 63.8092352823154 * Q.C2 - 4.29386548826852
    if Q.LHA >= 0.111565049159:
        z += 10.23406390957905 * Q.LHA - 1.1417638431685344
    if Q.LHA > 0.293190627853:
        z += -30.93673393489583 * math.exp(-((Q.lam2 - 3.8028565e-05) / 0.000797290334398297) ** 2) * (Q.LHA - 0.293190627853)
    return max(0.0, z)


def neuron_11(Q):
    z = 0.07713384783623205
    if Q.sum_pt < 788.4484375:
        z += 0.002712966100888033 * Q.sum_pt - 2.139033883235637
    if Q.LHA > 0.076586555683:
        z += 18.84629454487865 * math.exp(-((Q.width - 0.001653836415) / 0.0040130741380282635) ** 2) * (Q.LHA - 0.076586555683)
    if Q.max_dr > 0.015595615841:
        z += -16.351058234115072 * math.exp(-((Q.girth2 - 0.005590288714) / 0.002006537069537363) ** 2) * (Q.max_dr - 0.015595615841)
    z += 558.854261395004 * math.exp(-((Q.girth2 - 9.1213921e-05) / 0.004013074139074726) ** 2) * math.exp(-((Q.e2_sq - 0.011657374702) / 0.0037856152686924554) ** 2)
    return max(0.0, z)


def neuron_12(Q):
    z = -0.34263277324576913
    if Q.mass >= 91.19:
        z += 0.1421314273480893 * Q.mass - 12.960964859872265
    if Q.girth2 > 0.004372139461 and Q.mass > 45.595:
        z += 8.367961577472217 * (Q.girth2 - 0.004372139461) * (Q.mass - 45.595)
    if Q.mass > 41.377904891968 and Q.mass_over_sum_pt > 0.072690732432:
        z += -1.653109066697784 * (Q.mass - 41.377904891968) * (Q.mass_over_sum_pt - 0.072690732432)
    if Q.mass > 86.4 and Q.e2 > 0.004157758062:
        z += -1.6432595491429476 * (Q.mass - 86.4) * (Q.e2 - 0.004157758062)
    return max(0.0, z)


def neuron_13(Q):
    z = 1.986294614111177
    if Q.sum_pt < 988.4078125:
        z += 0.011989748159802678 * Q.sum_pt - 11.850760751056464
    if Q.mass >= 36.229410171509:
        z += -0.04385245639993708 * Q.mass + 1.5887486299415357
    if Q.lam1 < 0.016433749775:
        z += -77.12078789381333 * Q.lam1 + 1.2673837306977775
    z += 19.4887831199931 * math.sqrt(max(Q.z_7, 0.0))
    return max(0.0, z)


def neuron_14(Q):
    z = -0.27479008461935817
    if Q.e2_sq > 0.000236797256:
        z += 392.96395470346835 * math.exp(-((Q.girth2 - 0.007520088344) / 0.002006537069537363) ** 2) * (Q.e2_sq - 0.000236797256)
    z += 0.9700783945378099 * math.exp(-((Q.girth2 - 0.004372139461) / 0.002006537069537363) ** 2) * math.exp(-((Q.e2 - 0.012899691472) / 0.012014812183974575) ** 2)
    if Q.mass > 36.229410171509:
        z += 0.035630700318741076 * math.exp(-((Q.width - 0.008678044951) / 0.0040130741380282635) ** 2) * (Q.mass - 36.229410171509)
    if Q.e2 > 0.028531698044:
        z += -113.12242989950052 * math.exp(-((Q.e2_sq - 0.00528466865) / 0.0018928076343462277) ** 2) * (Q.e2 - 0.028531698044)
    return max(0.0, z)


def neuron_15(Q):
    z = -0.16790384750380793
    if Q.mass > 53.332374954224:
        z += 0.05534935646698371 * math.exp(-((Q.width - 0.006679471358) / 0.0040130741380282635) ** 2) * (Q.mass - 53.332374954224)
    if Q.e2 < 0.024547699839:
        z += 87.92173053600388 * math.exp(-((Q.lam1 - 0.004839980301) / 0.0017789999428521762) ** 2) * (0.024547699839 - Q.e2)
    if Q.e2_sq > 0.007182789718:
        z += 760.4577473986625 * math.exp(-((Q.width - 0.00752008842) / 0.0040130741380282635) ** 2) * (Q.e2_sq - 0.007182789718)
    z += 45191.398973631316 * math.exp(-((Q.girth2 - 0.003562611155) / 0.002006537069537363) ** 2) * math.exp(-((Q.lam1 - 0.012003726523) / 0.0017789999428521762) ** 2)
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
