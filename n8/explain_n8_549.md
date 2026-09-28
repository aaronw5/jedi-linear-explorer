# What each part of the 549-term formula does (8 particles)

*the simplest formula at the network's accuracy (from the 931-term tuned formula)*. Validation accuracy 65.74%. Words written by an AI agent from the numbers (60,000 training jets) and checked against them; lines marked *computed* come straight from the numbers. Plots: the page, tab "What each part does".

## Summary

The formula reads each jet on 16 scales, most of them variations on how wide the jet is, how its pT is shared among the hardest particles, and whether it looks like an elongated two-prong object. Tops are picked out mainly because they sit far below every other type on the compactness scale (neuron 13), which the t score subtracts, helped by the broad, massive, spread-out scale (neuron 10); there is no explicit 173 GeV mass or three-prong test among its main inputs. Quarks and gluons both sit high on the narrow, centred-jet scale (neuron 9), which feeds both of their scores; gluons are then told from quarks by the gluon-likeness scale (neuron 2, light jet with a hard 8th particle), which only the g score adds, and the quark-likeness scale (neuron 5, pT in few particles), which the g score subtracts. W and Z jets sit high on the two-prong scales (neurons 0 and 7) and at the bottom of the wide-angle-radiation and broad off-centre scales (neurons 3 and 6), which both boson scores subtract. W is told from Z by the compact, centred scale (neuron 11, highest for W and used only by the W score) against the scales that are largest for Z (neurons 7, 14 and 15), which weigh toward Z and against W; this W/Z split and the q/g split stay the weakest, with the Z score averaging 1.58 on true W jets and the q score 1.52 on true gluons.

## The 5 class scores

### score g: Gluon-like: light, hard-tailed, one-prong jets

High for light, one-prong jets whose pT is spread over many fairly hard particles: mean 2.22 for gluons and 1.37 for quarks, lower for tops (0.88) and near zero for W (0.13) and Z (-0.03).

Adds the gluon-likeness scale (neuron 2, +0.299), the narrow-centred scale (9, +0.267), the not-narrow/hard-8th-particle scale (1, +0.117) and the broad off-centre scale (6, +0.057); subtracts the quark-likeness scale (5, -0.132), the low-C2 scale (4, -0.069) and the two-prong massive scale (0, -0.059).

*computed:* largest for g (2.22), then q (1.37), then t (0.88), then W (0.13), then Z (-0.03); it separates g jets from the rest best (AUC 0.82: large for g)

### score q: Quark-like: narrow, centred jets

High for narrow, centred jets: mean 2.26 for quarks but also 1.52 for gluons (its weakest separation), and near zero for tops (0.07), W (0.03) and Z (-0.17).

Mostly the narrow-centred scale (neuron 9, +0.486), plus the broad off-centre (6, +0.081), quark-likeness (5, +0.041) and narrowness (8, +0.031) scales; subtracts the low-C2 scale (4, -0.255) and the broad, massive scale (10, -0.091).

*computed:* largest for q (2.26), then g (1.52), then t (0.07), then W (0.03), then Z (-0.17); it separates q jets from the rest best (AUC 0.85: large for q)

### score W: W-like: compact, centred two-prong jets

High for compact, centred two-prong jets without wide-angle radiation: mean 2.59 for W and 0.52 for Z, near zero for quarks (-0.04), negative for gluons (-0.59) and strongly negative for tops (-3.84).

Adds the compact-centred scale (neuron 11, +0.258), the two-prong massive (0, +0.081), compactness (13, +0.08) and Z-likeness (7, +0.064) scales; subtracts wide-angle radiation (3, -0.147), broad off-centre (6, -0.103), the two Z-leaning scales 14 (-0.085) and 15 (-0.081), narrowness (8, -0.063) and narrow-centred (9, -0.03).

*computed:* largest for W (2.59), then Z (0.52), then q (-0.04), then g (-0.59), then t (-3.84); it separates W jets from the rest best (AUC 0.89: large for W)

### score Z: Z-like: two-prong, mass-window jets, not broad

High for elongated two-prong jets in the boson mass/pT window that lack wide-angle radiation: mean 2.39 for Z, but also 1.58 for W (the main confusion), low for quarks (0.11) and negative for gluons (-0.38) and tops (-3.21).

Adds the Z-likeness (neuron 7, +0.191), low-C2 (4, +0.15), compactness (13, +0.087), heavier-wider (14, +0.059) and not-narrow (1, +0.033) scales; subtracts wide-angle radiation (3, -0.231, its largest input), broad off-centre (6, -0.172), narrow-centred (9, -0.042) and the width band above W (15, -0.026).

*computed:* largest for Z (2.39), then W (1.58), then q (0.11), then g (-0.38), then t (-3.21); it separates Z jets from the rest best (AUC 0.84: large for Z)

### score t: Top-like: essentially a wide-jet meter

High for wide, massive jets spread out in both directions: mean 2.83 for tops, far above Z (0.34), W (0.17) and gluons (0.05), and negative for quarks (-1.24); it tracks e2, girth and width (+0.884, +0.884, +0.88).

Mostly minus the compactness scale (neuron 13, -0.481), plus the low-C2 (4, +0.179), broad-massive (10, +0.144) and narrowness (8, +0.049) scales; subtracts the quark-likeness scale (5, -0.114).

*computed:* largest for t (2.83), then Z (0.34), then W (0.17), then g (0.05), then q (-1.24); it separates t jets from the rest best (AUC 0.90: large for t)

## The 16 neurons (most important first)

### neuron 1: Not-narrow jet, hard 8th particle (major)

- **What it measures:** Rises for jets that are not very narrow (width < 0.0087 and max ΔR < 0.25 push it down) with small e2_sq (< 0.0081 pushes it up), high total pT (log total pT > 6.4 and > 6.6) and a hard particle 7, the 8th hardest (pT_7 > 34 GeV). Lowest for q (0.49), with Z (1.04), g (1.03) and t (0.97) about equal and W (0.68) in between.
- *computed — its value:* largest for Z (1.04), then g (1.03), then t (0.97), then W (0.68), then q (0.49); it separates q jets from the rest best (AUC 0.37: small for q)
- **How the class scores use it:** The g score adds it (+12%) and the Z score a little (+3%); since quarks sit lowest on this scale, its main use in the g score is to pull gluons ahead of quarks. It does not enter the q, W or t scores.
- *computed — used by:* raises the score of g (+12%), Z (+3%); does not (or hardly) enter the score of q, W, t (share of each class score’s average input)

```
z = 1.28
if width < 0.0087: z += -409 × (0.0087 − width)
if e2_sq < 0.0081: z += 381 × (0.0081 − e2_sq)
if max_dr < 0.250: z += -7.08 × (0.250 − max_dr)
if z_7 < 0.054: z += -85.70 × (0.054 − z_7)
if log_sum_pt > 6.60: z += 10.10 × (log_sum_pt − 6.60)
if log_sum_pt > 6.40: z += 3.43 × (log_sum_pt − 6.40)
if pt_7 > 34.00: z += 0.136 × (pt_7 − 34.00)
if z_7 < 0.054 and girth2_top2 < 0.014: z += 4820 × (0.054 − z_7) × (0.014 − girth2_top2)
if log_sum_pt > 6.40 and centroid_offset < 0.027: z += -132 × (log_sum_pt − 6.40) × (0.027 − centroid_offset)
if C2 < 0.044 and tau21 < 0.220: z += -350 × (0.044 − C2) × (0.220 − tau21)
if log_sum_pt > 6.40 and max_dr < 0.190: z += 22.10 × (log_sum_pt − 6.40) × (0.190 − max_dr)
if LHA > 0.280: z += 13.30 × (LHA − 0.280)
if pt_7 > 34.00 and mass < 80.40: z += -0.0015 × (pt_7 − 34.00) × (80.40 − mass)
if log_sum_pt > 6.60 and girth2_top3 < 0.0068: z += -749 × (log_sum_pt − 6.60) × (0.0068 − girth2_top3)
if tau21 < 0.210 and lam2 < 0.00021: z += 41000 × (0.210 − tau21) × (0.00021 − lam2)
if e2_sq < 0.0081 and planar_flow < 0.086: z += -4230 × (0.0081 − e2_sq) × (0.086 − planar_flow)
if lam1 < 0.0085 and z_7 > 0.037: z += -3520 × (0.0085 − lam1) × (z_7 − 0.037)
if z_7 < 0.044: z += -39.80 × (0.044 − z_7)
if e2 < 0.037 and eccentricity > 0.980: z += 5240 × (0.037 − e2) × (eccentricity − 0.980)
if mass_top5 < 6.10: z += -0.181 × (6.10 − mass_top5)
if e2 > 0.029 and tau32 < 0.640: z += -66.20 × (e2 − 0.029) × (0.640 − tau32)
if e2 > 0.034: z += -20.80 × (e2 − 0.034)
if LHA < 0.330 and planar_flow < 0.082: z += -127 × (0.330 − LHA) × (0.082 − planar_flow)
if max_dr < 0.048: z += -21.50 × (0.048 − max_dr)
if lam1 < 0.0083 and centroid_offset > 0.020: z += 14100 × (0.0083 − lam1) × (centroid_offset − 0.020)
if log_sum_pt > 6.60 and D2 < 1.20: z += 7.52 × (log_sum_pt − 6.60) × (1.20 − D2)
if pt_7 > 35.00 and max_dr < 0.080: z += 1.23 × (pt_7 − 35.00) × (0.080 − max_dr)
if pt_7 > 54.00: z += -0.120 × (pt_7 − 54.00)
if z_7 < 0.042 and z_dr_0p05_0p1 > 0.200: z += -89.80 × (0.042 − z_7) × (z_dr_0p05_0p1 − 0.200)
if pt_7 > 54.00 and mass_top3 < 52.00: z += 0.0024 × (pt_7 − 54.00) × (52.00 − mass_top3)
if n_pt_above_50 > 6.00 and girth2_top2 < 0.00075: z += 483 × (n_pt_above_50 − 6.00) × (0.00075 − girth2_top2)
if pt_7 > 35.00 and centroid_offset > 0.016: z += 1.49 × (pt_7 − 35.00) × (centroid_offset − 0.016)
if mass < 46.00 and tau21 < 0.200: z += 0.515 × (46.00 − mass) × (0.200 − tau21)
if log_sum_pt > 6.60 and n_pt_above_50 > 7.00: z += -3.36 × (log_sum_pt − 6.60) × (n_pt_above_50 − 7.00)
if e2 > 0.025 and pt_1 < 81.00: z += -0.427 × (e2 − 0.025) × (81.00 − pt_1)
if n_pt_above_50 > 6.10 and tau32 < 0.160: z += -19.30 × (n_pt_above_50 − 6.10) × (0.160 − tau32)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.0087`; 2: `e2_sq < 0.0081`; 3: `max_dr < 0.25`; 4: `z_7 < 0.054`; 5: `log_sum_pt > 6.6`; 6: `log_sum_pt > 6.4`; 7: `pt_7 > 34`; 8: `z_7 < 0.054 and girth2_top2 < 0.014`; 9: `log_sum_pt > 6.4 and centroid_offset < 0.027`; 10: `C2 < 0.044 and tau21 < 0.22`; 11: `log_sum_pt > 6.4 and max_dr < 0.19`; 12: `LHA > 0.28`; 13: `pt_7 > 34 and mass < 80.4`; 14: `log_sum_pt > 6.6 and girth2_top3 < 0.0068`; 15: `tau21 < 0.21 and lam2 < 0.00021`; 16: `e2_sq < 0.0081 and planar_flow < 0.086`; 17: `lam1 < 0.0085 and z_7 > 0.037`; 18: `z_7 < 0.044`; 19: `e2 < 0.037 and eccentricity > 0.98`; 20: `mass_top5 < 6.1`; 21: `e2 > 0.029 and tau32 < 0.64`; 22: `e2 > 0.034`; 23: `LHA < 0.33 and planar_flow < 0.082`; 24: `max_dr < 0.048`; 25: `lam1 < 0.0083 and centroid_offset > 0.02`; 26: `log_sum_pt > 6.6 and D2 < 1.2`; 27: `pt_7 > 35 and max_dr < 0.08`; 28: `pt_7 > 54`; 29: `z_7 < 0.042 and z_dr_0p05_0p1 > 0.2`; 30: `pt_7 > 54 and mass_top3 < 52`; 31: `n_pt_above_50 > 6 and girth2_top2 < 0.00075`; 32: `pt_7 > 35 and centroid_offset > 0.016`; 33: `mass < 46 and tau21 < 0.2`; 34: `log_sum_pt > 6.6 and n_pt_above_50 > 7`; 35: `e2 > 0.025 and pt_1 < 81`; 36: `n_pt_above_50 > 6.1 and tau32 < 0.16`):

- `✓✓✓··✓✓·✓·✓·✓···✓··✓···✓··✓·········` **Light soft-leading gluon-rich jets** — 16.0% of jets, neuron 0.34, formula right for 53%. Mostly gluons (49%, q 24%, some W/Z) with low mass (12.4 GeV), narrow (91% of pT within 0.05), a softer leading particle (167 GeV) and a slightly harder 8th particle than average. Being narrow they pass width < 0.0087 (-3.144), max_dr < 0.25 and lam1 < 0.0085 and z_7 > 0.037, which mostly cancel e2_sq < 0.0081 (+2.862); pt_7 > 34 passes for 0.763 but is itself cancelled by pt_7 > 34 and mass < 80.4. The neuron is weak (0.339, on for 0.294) and nudges the g and Z scores up; the formula calls them g but is right only 0.529 of the time, many being quarks.
- `··✓···✓··✓·✓········✓✓··············` **Wide top/Z jets, high LHA** — 15.4% of jets, neuron 0.98, formula right for 70%. Mostly tops (49%) with Z (24%) and some gluons, mass 60.4 GeV, about twice the average width and 38% of pT beyond 0.1 from the axis. They pass LHA > 0.28 (+0.804) and e2 > 0.034 far more than other groups, and fail width < 0.0087 for most jets so avoid its big minus; C2 < 0.044 and tau21 < 0.22 (-0.762) and max_dr < 0.25 pull back while pt_7 > 34 and tau21 < 0.21 and lam2 < 0.00021 add. The neuron is on for 0.758 (mean 0.978), adding to g and Z; the formula calls them t and is right 0.698 of the time, with Z the main alternative.
- `✓✓✓··✓✓·✓✓✓·✓··✓✓···················` **Medium-mass W-leaning mixed jets** — 14.1% of jets, neuron 0.58, formula right for 57%. A mixture led by W (38%) with Z (25%), g and t, at average mass (40.2 GeV) and slightly narrower than average, pT split between the core and 0.05-0.1. The narrow-jet pair width < 0.0087 (-1.612) and e2_sq < 0.0081 (+1.507) cancel; about half pass each of pt_7 > 34 (+), z_7 < 0.054 (-) and e2_sq < 0.0081 and planar_flow < 0.086 (-), and lam1 < 0.0083 and centroid_offset > 0.02 passes more often than elsewhere. The result is middling (0.583, on for 0.554); the formula calls them W but is right only 0.566 of the time.
- `✓✓✓✓✓✓·✓✓·✓··✓···✓·✓···✓············` **Light narrow harder quark jets** — 10.1% of jets, neuron 0.49, formula right for 55%. Mostly light quarks (47%, g 24%, W 15%) with low mass (11.5 GeV), extremely narrow (97% of pT within 0.05), somewhat above-average pT (820 GeV) and a soft 8th particle. The narrowness terms cancel (width < 0.0087 vs e2_sq < 0.0081), z_7 < 0.054 (-1.572) and max_dr < 0.25 subtract, and log_sum_pt > 6.6 and log_sum_pt > 6.4 plus z_7 < 0.054 and girth2_top2 < 0.014 add back, leaving a modest value (0.493, on for 0.484). The formula calls them q and is right 0.548 of the time, with g and W as frequent true alternatives.
- `··✓···✓····✓········✓✓··············` **Wide heavy three-prong top jets** — 8.8% of jets, neuron 0.90, formula right for 86%. Mostly tops (85%) with the largest mass (82.2 GeV), four times the average width and 76% of pT beyond 0.1 from the axis; soft leading particle (143 GeV). They never pass width < 0.0087 or e2_sq < 0.0081, so the big narrow-jet terms drop out; LHA > 0.28 (+1.845) is offset by e2 > 0.029 and tau32 < 0.64 (-1.408) and e2 > 0.034, with pt_7 > 34 adding for half. The neuron is on for 0.732 (mean 0.897), adding to g and Z; the formula calls them t and is right 0.861 of the time.
- `✓✓✓··✓✓·✓✓✓✓✓·✓✓✓····✓✓·············` **Two-prong bosons with hard 8th particle** — 8.7% of jets, neuron 1.68, formula right for 74%. A W/Z mixture (W 44%, Z 37%) of 56.4 GeV with a hard 8th particle (49.6 GeV vs 35 average) and pT concentrated 0.05-0.1 from the axis. All pass pt_7 > 34 (+2.12), and most pass tau21 < 0.21 and lam2 < 0.00021 (+0.804) and log_sum_pt > 6.4, against C2 < 0.044 and tau21 < 0.22 (-1.282), width < 0.0087 and pt_7 > 34 and mass < 80.4. The neuron is high (1.675, on for 0.833), adding to g and Z and slightly lowering W; the formula calls them W and is right 0.735 of the time.
- `✓✓✓✓✓✓·✓✓·✓··✓···✓·✓···✓············` **High-pT one-particle quark jets** — 8.5% of jets, neuron 0.61, formula right for 72%. Mostly light quarks (67%) with high pT (989 GeV), a leading particle of 471 GeV, a soft 8th particle and almost no mass or width. Large terms balance: width < 0.0087 and z_7 < 0.054 (about -6.4) against e2_sq < 0.0081, log_sum_pt > 6.6 and z_7 < 0.054 and girth2_top2 < 0.014, with log_sum_pt > 6.6 and girth2_top3 < 0.0068 and z_7 < 0.044 always passing here and pulling down. The value is moderate (0.612, on for 0.498); the formula calls them q and is right 0.718 of the time.
- `✓✓✓✓✓✓·✓✓✓✓✓·✓✓✓·✓···✓✓··✓··✓·······` **High-pT two-prong Z/W jets** — 7.4% of jets, neuron 1.22, formula right for 81%. Boosted bosons (Z 46%, W 39%) with mass 70.4 GeV, above-average pT (866 GeV) and pT mostly at 0.05-0.1, i.e. two clear prongs. The high-pT tests log_sum_pt > 6.6 and log_sum_pt > 6.4, and the two-prong tests tau21 < 0.21 and lam2 < 0.00021 and log_sum_pt > 6.6 and D2 < 1.2 (passing far more than elsewhere), outweigh z_7 < 0.054 (-1.726) and C2 < 0.044 and tau21 < 0.22 (-1.513). The neuron is on for 0.717 (1.217), adding to g and Z; the formula splits them Z/W and is right 0.808 of the time.
- `✓✓✓✓✓✓·✓✓✓···✓✓✓·✓✓···✓·············` **High-pT bosons with dominant core** — 6.3% of jets, neuron 0.79, formula right for 67%. A W/Z mixture (W 42%, Z 36%, q 14%) at 51.4 GeV with high pT (883 GeV), a very hard leading particle (412 GeV) and 89% of pT within 0.05 of the axis. z_7 < 0.054 (-2.409) and width < 0.0087 subtract, while log_sum_pt > 6.6, z_7 < 0.054 and girth2_top2 < 0.014, e2_sq < 0.0081 and e2 < 0.037 and eccentricity > 0.98 (much more common here) add. The neuron is on for 0.764 (0.791); the formula calls them W but is right only 0.666 of the time, with the quark admixture a source of error.
- `✓✓✓·✓✓✓·✓·✓·✓✓··✓··✓···✓··✓✓·✓✓··✓··` **Many-hard-particle light gluon jets** — 4.6% of jets, neuron 1.98, formula right for 60%. Mostly gluons (54%, q 28%) with low mass (10.5 GeV), very narrow, and pT shared evenly among many particles (8th particle 56.5 GeV, leading only 216 GeV). pt_7 > 34 (+3.056) and pt_7 > 35 and max_dr < 0.08 (+1.357, far more common here) plus log_sum_pt > 6.6 win over pt_7 > 34 and mass < 80.4 (-2.379), with the narrow-jet pair cancelling. This gives the neuron's highest value (1.977, on for 0.894), raising the g and Z scores; the formula calls them g and is right only 0.597 of the time.

### neuron 2: Gluon-likeness: light, hard-tailed jet (major)

- **What it measures:** Rises for compact jets (λ1 < 0.0057) below 69 GeV in a total-pT band (log total pT > 6.3, total pT < 790 GeV) whose particle 7, the 8th hardest, is hard (pT_7 > 31 GeV pushes it up, pT_7 < 54 GeV down); it is also pushed down by LHA > 0.1 and mass < 36 GeV, and overall falls with mass (-0.666) and rises with τ21 (+0.551). Largest for g (3.21), then q (2.41), lower for W (1.58), Z (1.31) and t (1.28).
- *computed — its value:* largest for g (3.21), then q (2.41), then W (1.58), then Z (1.31), then t (1.28); it separates g jets from the rest best (AUC 0.77: large for g)
- **How the class scores use it:** Only the g score uses it (+30%, the g score's largest input), because gluons sit highest on this scale. It does not enter the q, W, Z or t scores.
- *computed — used by:* raises the score of g (+30%); does not (or hardly) enter the score of q, W, Z, t (share of each class score’s average input)

```
z = 2.32
if LHA > 0.100: z += -7.11 × (LHA − 0.100)
if pt_7 < 54.00: z += -0.048 × (54.00 − pt_7)
if mass < 36.00: z += -0.077 × (36.00 − mass)
if lam1 < 0.0057: z += 286 × (0.0057 − lam1)
if log_sum_pt > 6.30: z += 2.40 × (log_sum_pt − 6.30)
if sum_pt < 790: z += 0.0056 × (790 − sum_pt)
if mass < 69.00: z += 0.020 × (69.00 − mass)
if mass_over_sum_pt_sq < 0.012: z += 77.20 × (0.012 − mass_over_sum_pt_sq)
if pt_7 > 31.00: z += 0.089 × (pt_7 − 31.00)
if planar_flow < 0.680: z += -1.30 × (0.680 − planar_flow)
if mass < 37.00 and lam2 < 0.0011: z += 48.80 × (37.00 − mass) × (0.0011 − lam2)
if pt_7 > 30.00 and C2 < 0.051: z += -1.87 × (pt_7 − 30.00) × (0.051 − C2)
if max_dr < 0.160: z += -5.05 × (0.160 − max_dr)
if mass < 69.00 and z_7 < 0.068: z += -0.454 × (69.00 − mass) × (0.068 − z_7)
if log_sum_pt < 6.50: z += 1.81 × (6.50 − log_sum_pt)
if lam1 < 0.0059 and max_dr > 0.078: z += -3030 × (0.0059 − lam1) × (max_dr − 0.078)
if pt_7 > 30.00 and max_dr > 0.092: z += -0.446 × (pt_7 − 30.00) × (max_dr − 0.092)
if mass_over_sum_pt < 0.0098: z += -186 × (0.0098 − mass_over_sum_pt)
if z_7 > 0.044 and dr_7 < 0.066: z += -483 × (z_7 − 0.044) × (0.066 − dr_7)
if sum_pt_top5 > 740 and mean_eta2 < 0.0015: z += -3.84 × (sum_pt_top5 − 740) × (0.0015 − mean_eta2)
if pt_6 < 53.00 and lam2 > -0.00063: z += 5.77 × (53.00 − pt_6) × (lam2 − -0.00063)
if mass < 68.00 and centroid_offset > 0.010: z += -0.406 × (68.00 − mass) × (centroid_offset − 0.010)
if mass < 8.50: z += 0.145 × (8.50 − mass)
if lam1 < 0.004 and centroid_offset < 0.0062: z += -35100 × (0.004 − lam1) × (0.0062 − centroid_offset)
if log_sum_pt < 6.50 and eccentricity > 0.790: z += 8.11 × (6.50 − log_sum_pt) × (eccentricity − 0.790)
if z_7 < 0.017: z += -246 × (0.017 − z_7)
if pt_7 > 30.00 and centroid_offset > 0.013: z += -1.28 × (pt_7 − 30.00) × (centroid_offset − 0.013)
if sum_pt < 790 and dr_7 < 0.064: z += 0.041 × (790 − sum_pt) × (0.064 − dr_7)
if mass < 71.00 and max_pair_mass > 13.00: z += -0.0017 × (71.00 − mass) × (max_pair_mass − 13.00)
if log_sum_pt > 6.80: z += 4.36 × (log_sum_pt − 6.80)
if log_sum_pt > 6.90: z += -7.73 × (log_sum_pt − 6.90)
if pt_7 < 14.00 and n_pt_above_10 < 7.90: z += 0.125 × (14.00 − pt_7) × (7.90 − n_pt_above_10)
if girth2_top2 < 3.7e-05: z += 10700 × (3.7e-05 − girth2_top2)
if log_sum_pt > 6.90 and n_pt_above_50 > 5.00: z += -2.16 × (log_sum_pt − 6.90) × (n_pt_above_50 − 5.00)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `LHA > 0.1`; 2: `pt_7 < 54`; 3: `mass < 36`; 4: `lam1 < 0.0057`; 5: `log_sum_pt > 6.3`; 6: `sum_pt < 790`; 7: `mass < 69`; 8: `mass_over_sum_pt_sq < 0.012`; 9: `pt_7 > 31`; 10: `planar_flow < 0.68`; 11: `mass < 37 and lam2 < 0.0011`; 12: `pt_7 > 30 and C2 < 0.051`; 13: `max_dr < 0.16`; 14: `mass < 69 and z_7 < 0.068`; 15: `log_sum_pt < 6.5`; 16: `lam1 < 0.0059 and max_dr > 0.078`; 17: `pt_7 > 30 and max_dr > 0.092`; 18: `mass_over_sum_pt < 0.0098`; 19: `z_7 > 0.044 and dr_7 < 0.066`; 20: `sum_pt_top5 > 740 and mean_eta2 < 0.0015`; 21: `pt_6 < 53 and lam2 > -0.00063`; 22: `mass < 68 and centroid_offset > 0.01`; 23: `mass < 8.5`; 24: `lam1 < 0.004 and centroid_offset < 0.0062`; 25: `log_sum_pt < 6.5 and eccentricity > 0.79`; 26: `z_7 < 0.017`; 27: `pt_7 > 30 and centroid_offset > 0.013`; 28: `sum_pt < 790 and dr_7 < 0.064`; 29: `mass < 71 and max_pair_mass > 13`; 30: `log_sum_pt > 6.8`; 31: `log_sum_pt > 6.9`; 32: `pt_7 < 14 and n_pt_above_10 < 7.9`; 33: `girth2_top2 < 3.7e-05`; 34: `log_sum_pt > 6.9 and n_pt_above_50 > 5`):

- `✓✓··✓✓✓✓·✓··✓✓······✓·············` **Heavy boosted boson/top jets** — 19.1% of jets, neuron 0.47, formula right for 76%. Heavy jets (65.3 GeV) that are a Z/W/t mixture (Z 38%, W 33%, t 20%), of average total pT but with a harder leading particle (297 GeV) and pT spread over 0.05-0.1. Being heavy they almost never pass mass < 36 or mass < 37 and lam2 < 0.0011, and most fail lam1 < 0.0057, so the gluon-like pluses are missing; LHA > 0.1, pt_7 < 54 and planar_flow < 0.68 pull down against log_sum_pt > 6.3 and mass_over_sum_pt_sq < 0.012. The neuron is low (0.471, the lowest of the groups that are usually on), adding little to the g score; the formula splits them Z/W and is right 0.759 of the time.
- `·✓✓✓✓·✓✓·✓✓·✓✓···✓·✓✓·✓✓··········` **Light narrow hard-core quark jets** — 14.2% of jets, neuron 2.32, formula right for 63%. Mostly light quarks (57%, g 20%) with almost no mass (7.9 GeV) or width, above-average pT (878 GeV) carried by a hard leading particle (358 GeV). The light-mass tests all pass and nearly cancel: mass < 36 (-2.159) and mass < 69 and z_7 < 0.068 against lam1 < 0.0057, mass < 37 and lam2 < 0.0011, mass < 69 and log_sum_pt > 6.3; pt_7 < 54 and, for most, mass_over_sum_pt < 0.0098 subtract. The neuron is on (2.322), pushing the g score up, but the formula still calls them q and is right 0.63 of the time.
- `✓✓···✓✓·✓✓····✓·✓···✓✓··✓·✓·······` **Wide low-pT top jets** — 13.8% of jets, neuron 1.78, formula right for 72%. Mostly tops (66%, g 17%) with mass 60.3 GeV, about three times the average width, 55% of pT beyond 0.1 from the axis, and the lowest total pT (489 GeV). They pass the low-pT tests sum_pt < 790 (+1.674), log_sum_pt < 6.5 and pt_6 < 53 and lam2 > -0.00063, which outweigh LHA > 0.1 (-1.943) and pt_7 < 54, while failing lam1 < 0.0057 and mostly log_sum_pt > 6.3. The neuron is fairly high (1.785), adding to the g score, yet the formula calls them t and is right 0.715 of the time.
- `✓✓··✓✓✓✓✓✓·✓✓·✓·✓···✓✓··✓·✓·······` **Hard-tailed medium-pT top/W/Z mix** — 13.0% of jets, neuron 1.64, formula right for 67%. A mixture of tops (35%), Z (25%), W (23%) and gluons at 56.0 GeV, wider than average, with lower total pT (601 GeV) but a hard 8th particle (41.8 GeV). LHA > 0.1 (-1.556) is outweighed by sum_pt < 790 and pt_7 > 31 (+0.964, always passing), with pt_7 > 30 and C2 < 0.051 and pt_7 > 30 and max_dr > 0.092 taking some back. The neuron is on (1.635), adding to g; the formula leans to t over W and Z and is right only 0.673 of the time.
- `✓✓·✓✓·✓✓·✓···✓·✓····✓✓············` **Narrow high-pT W-leaning jets** — 9.1% of jets, neuron 1.29, formula right for 56%. A W/Z/quark mixture (W 37%, Z 26%, q 20%) at average mass (40.0 GeV), narrow (89% of pT within 0.05), with high pT concentrated in the leading particle (354 GeV). lam1 < 0.0057, log_sum_pt > 6.3 and mass_over_sum_pt_sq < 0.012 add, but pt_7 < 54, LHA > 0.1, planar_flow < 0.68 and especially lam1 < 0.0059 and max_dr > 0.078 (which passes far more often here than elsewhere) subtract. The neuron is middling (1.291); the formula calls them W but is right only 0.561 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓✓···✓✓·✓·✓····✓······` **Light gluon jets with hard tail** — 8.8% of jets, neuron 3.93, formula right for 54%. Mostly gluons (46%, q 31%) with little mass (8.5 GeV), narrow, with pT shared among many particles (leading 203 GeV, 8th 43.0 GeV). mass < 36 (-2.118) and pt_7 > 30 and C2 < 0.051 are beaten by lam1 < 0.0057, mass < 37 and lam2 < 0.0011, mass < 69, pt_7 > 31 and mass_over_sum_pt_sq < 0.012, all passing for every jet. The neuron is high (3.929), strongly raising the g score; the formula calls them g but is right only 0.536 of the time, because many are quarks.
- `✓✓··✓✓✓✓✓✓·✓✓···✓···········✓·····` **Two-prong bosons with hard tail** — 8.5% of jets, neuron 1.55, formula right for 72%. A W/Z mixture (W 39%, Z 34%) of 58.0 GeV, pT at 0.05-0.1 from the axis, and a very hard 8th particle (50.9 GeV). pt_7 > 31 (+1.767) and log_sum_pt > 6.3 are balanced by LHA > 0.1, pt_7 > 30 and C2 < 0.051 and planar_flow < 0.68, while the light-mass pluses (mass < 36 etc.) are absent. The neuron is moderate (1.551), adding to g; the formula calls them W and is right 0.717 of the time.
- `✓✓✓✓·✓✓✓✓✓✓✓✓✓✓···✓·✓✓··✓··✓······` **Light low-pT gluon jets** — 8.2% of jets, neuron 4.00, formula right for 53%. Mostly gluons (51%, q 20%, about 10% each W/Z/t), light (14.6 GeV), of low total pT (537 GeV) and somewhat broader than the pencil-thin groups. Every jet passes sum_pt < 790, mass < 69 and mass_over_sum_pt_sq < 0.012, nearly all pass lam1 < 0.0057 and mass < 37 and lam2 < 0.0011, and most pass log_sum_pt < 6.5, together outweighing mass < 36 and pt_7 < 54. The neuron is high (3.999), raising the g score; the formula calls them g but is right only 0.528 of the time, the q and boson admixture being misread as g.
- `✓·✓✓✓·✓✓✓✓✓✓✓····✓✓···✓✓··········` **Light gluons, very hard 8th particle** — 3.7% of jets, neuron 4.05, formula right for 60%. Mostly gluons (56%, q 28%), nearly massless (8.1 GeV) and narrow, with the hardest 8th particle of all groups (57.8 GeV) and a soft leading particle (204 GeV). pt_7 > 31 (+2.388) is cancelled by pt_7 > 30 and C2 < 0.051, but because pt_7 < 54 mostly fails its penalty is gone, so the light-mass pluses (lam1 < 0.0057, mass < 37 and lam2 < 0.0011, mass < 69) win over mass < 36. This gives the neuron's highest value (4.047), strongly raising g; the formula calls them g and is right 0.605 of the time.
- `·✓✓✓✓·✓✓·✓✓·✓✓·✓···✓✓··✓·✓···✓✓✓✓·` **One-particle high-pT quark jets** — 1.6% of jets, neuron 0.21, formula right for 80%. Mostly light quarks (80%), with high pT (1015 GeV) nearly all in the leading particle (566 GeV) and a very soft 8th particle (7.1 GeV). z_7 < 0.017 (-2.458), which nearly never passes elsewhere, together with pt_7 < 54, mass < 36, mass < 69 and z_7 < 0.068 and sum_pt_top5 > 740 and mean_eta2 < 0.0015 outweigh lam1 < 0.0057, pt_7 < 14 and n_pt_above_10 < 7.9 and log_sum_pt > 6.3. The neuron is mostly off (on for 0.264), leaving the g score alone; the formula calls them q and is right 0.799 of the time.

### neuron 3: Wide-angle radiation (0.2-0.4) (major)

- **What it measures:** Rises with the pT carried at 0.2 ≤ ΔR < 0.4 from the axis (rank correlation +0.695) and with jet width: compact jets are cut off (girth2 < 0.0088 and < 0.013 push it down) while e2 < 0.043 and LHA > 0.32 push it up. Largest for t (4.72), then g (1.13) and q (0.54), and nearly zero for Z (0.17) and W (0.01).
- *computed — its value:* largest for t (4.72), then g (1.13), then q (0.54), then Z (0.17), then W (0.01); it separates t jets from the rest best (AUC 0.80: large for t)
- **How the class scores use it:** The Z score (-23%) and W score (-15%) subtract it: W and Z jets sit at the bottom of this scale, so radiation at wide angle argues against a boson. It does not enter the g, q or t scores, even though tops sit highest on it.
- *computed — used by:* lowers the score of W (-15%), Z (-23%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 1.38
if girth2 < 0.0088: z += -760 × (0.0088 − girth2)
if girth2 < 0.013: z += -372 × (0.013 − girth2)
if e2 < 0.043: z += 130 × (0.043 − e2)
if LHA > 0.320: z += 87.60 × (LHA − 0.320)
if e2 > 0.028: z += -89.10 × (e2 − 0.028)
if mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.90: z += 10.80 × (mass_over_sum_pt − 0.065) × (4.90 − n_dr_0_0p05)
if centroid_offset > 0.013: z += 82.80 × (centroid_offset − 0.013)
if mass > 37.00 and lam2 < 0.0013: z += 55.10 × (mass − 37.00) × (0.0013 − lam2)
if max_dr > 0.150: z += 24.50 × (max_dr − 0.150)
if width > 0.019 and pt_dispersion < 0.490: z += 6930 × (width − 0.019) × (0.490 − pt_dispersion)
if mass_over_sum_pt > 0.070 and tau32 < 0.520: z += -178 × (mass_over_sum_pt − 0.070) × (0.520 − tau32)
if lam1 > 0.016: z += 556 × (lam1 − 0.016)
if LHA > 0.310 and eccentricity > 0.960: z += 2050 × (LHA − 0.310) × (eccentricity − 0.960)
if e2 > 0.051: z += 117 × (e2 − 0.051)
if lam1 > 0.0086 and pt_7 < 38.00: z += 41.60 × (lam1 − 0.0086) × (38.00 − pt_7)
if LHA > 0.320 and planar_flow > 0.012: z += -77.90 × (LHA − 0.320) × (planar_flow − 0.012)
if lam1 > 0.012 and pt_6 < 38.00: z += 78.80 × (lam1 − 0.012) × (38.00 − pt_6)
if lam1 > 0.0028 and z_7 < 0.077: z += -4000 × (lam1 − 0.0028) × (0.077 − z_7)
if e2 > 0.027 and n_pt_above_50 > 3.00: z += -13.00 × (e2 − 0.027) × (n_pt_above_50 − 3.00)
if max_dr > 0.140 and phi_0 < -0.041: z += 704 × (max_dr − 0.140) × (-0.041 − phi_0)
if C2 > 0.094: z += -247 × (C2 − 0.094)
if LHA > 0.310 and max_dr < 0.150: z += -3470 × (LHA − 0.310) × (0.150 − max_dr)
if mass > 70.00: z += -0.085 × (mass − 70.00)
if mass_top5 > 53.00: z += -0.094 × (mass_top5 − 53.00)
if centroid_offset > 0.012 and mean_phi < -0.0092: z += -2390 × (centroid_offset − 0.012) × (-0.0092 − mean_phi)
if mass_over_sum_pt > 0.069 and dr_7 < 0.042: z += -10900 × (mass_over_sum_pt − 0.069) × (0.042 − dr_7)
if mean_eta < -0.016 and z_4 < 0.130: z += 1710 × (-0.016 − mean_eta) × (0.130 − z_4)
if mean_eta < -0.015 and pt_4 < 69.00: z += -3.14 × (-0.015 − mean_eta) × (69.00 − pt_4)
if max_dr > 0.160 and dr_1 < 0.047: z += -640 × (max_dr − 0.160) × (0.047 − dr_1)
if mass_top5 > 54.00 and eta_7 < 0.035: z += -0.763 × (mass_top5 − 54.00) × (0.035 − eta_7)
if centroid_offset > 0.015 and phi_7 > -0.030: z += 246 × (centroid_offset − 0.015) × (phi_7 − -0.030)
if lam1 > 0.018 and eccentricity > 0.960: z += 12900 × (lam1 − 0.018) × (eccentricity − 0.960)
if mass > 70.00 and mean_phi > 0.00098: z += -5.08 × (mass − 70.00) × (mean_phi − 0.00098)
if LHA > 0.420 and pt_7 > 38.00: z += -30.10 × (LHA − 0.420) × (pt_7 − 38.00)
if max_dr > 0.150 and dr_3 < 0.046: z += -507 × (max_dr − 0.150) × (0.046 − dr_3)
if mass_over_sum_pt > 0.110 and dr_7 < 0.049: z += 21900 × (mass_over_sum_pt − 0.110) × (0.049 − dr_7)
if mass > 70.00 and max_dr < 0.180: z += 3.89 × (mass − 70.00) × (0.180 − max_dr)
if LHA > 0.310 and pt_5 < 30.00: z += 16.00 × (LHA − 0.310) × (30.00 − pt_5)
if mass_over_sum_pt > 0.091 and max_dr < 0.150: z += 8590 × (mass_over_sum_pt − 0.091) × (0.150 − max_dr)
if mass > 38.00 and dr_6 < 0.046: z += -1.28 × (mass − 38.00) × (0.046 − dr_6)
if mass > 36.00 and pt_7 < 20.00: z += -0.0044 × (mass − 36.00) × (20.00 − pt_7)
if e2 < 0.038 and phi_0 > 0.080: z += -50100 × (0.038 − e2) × (phi_0 − 0.080)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.0088`; 2: `girth2 < 0.013`; 3: `e2 < 0.043`; 4: `LHA > 0.32`; 5: `e2 > 0.028`; 6: `mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9`; 7: `centroid_offset > 0.013`; 8: `mass > 37 and lam2 < 0.0013`; 9: `max_dr > 0.15`; 10: `width > 0.019 and pt_dispersion < 0.49`; 11: `mass_over_sum_pt > 0.07 and tau32 < 0.52`; 12: `lam1 > 0.016`; 13: `LHA > 0.31 and eccentricity > 0.96`; 14: `e2 > 0.051`; 15: `lam1 > 0.0086 and pt_7 < 38`; 16: `LHA > 0.32 and planar_flow > 0.012`; 17: `lam1 > 0.012 and pt_6 < 38`; 18: `lam1 > 0.0028 and z_7 < 0.077`; 19: `e2 > 0.027 and n_pt_above_50 > 3`; 20: `max_dr > 0.14 and phi_0 < -0.041`; 21: `C2 > 0.094`; 22: `LHA > 0.31 and max_dr < 0.15`; 23: `mass > 70`; 24: `mass_top5 > 53`; 25: `centroid_offset > 0.012 and mean_phi < -0.0092`; 26: `mass_over_sum_pt > 0.069 and dr_7 < 0.042`; 27: `mean_eta < -0.016 and z_4 < 0.13`; 28: `mean_eta < -0.015 and pt_4 < 69`; 29: `max_dr > 0.16 and dr_1 < 0.047`; 30: `mass_top5 > 54 and eta_7 < 0.035`; 31: `centroid_offset > 0.015 and phi_7 > -0.03`; 32: `lam1 > 0.018 and eccentricity > 0.96`; 33: `mass > 70 and mean_phi > 0.00098`; 34: `LHA > 0.42 and pt_7 > 38`; 35: `max_dr > 0.15 and dr_3 < 0.046`; 36: `mass_over_sum_pt > 0.11 and dr_7 < 0.049`; 37: `mass > 70 and max_dr < 0.18`; 38: `LHA > 0.31 and pt_5 < 30`; 39: `mass_over_sum_pt > 0.091 and max_dr < 0.15`; 40: `mass > 38 and dr_6 < 0.046`; 41: `mass > 36 and pt_7 < 20`; 42: `e2 < 0.038 and phi_0 > 0.08`):

- `✓✓✓·······································` **Pencil-thin light quark/gluon jets** — 38.4% of jets, neuron 0.01, formula right for 59%. The largest group (38%), mostly light quarks (41%) with gluons (34%), almost massless (11.5 GeV) with 97% of pT within 0.05 of the axis. girth2 < 0.0088 (-6.245) and girth2 < 0.013 (-4.619) always pass and beat e2 < 0.043 (+4.7), so the neuron is off (on for 0.008) and adds nothing. The formula splits them between q and g and is right only 0.587 of the time.
- `✓✓✓···✓✓·········✓························` **Compact medium-mass W-leaning jets** — 22.7% of jets, neuron 0.27, formula right for 60%. W-rich (40%) mixture with Z (27%) and gluons, mass 44.4 GeV, narrower than average with 60% of pT within 0.05. Both girth2 < 0.0088 and girth2 < 0.013 pass (about -6.6 together) against e2 < 0.043 (+2.407), with only partial help from max_dr > 0.15, mass > 37 and lam2 < 0.0013 and centroid_offset > 0.013. The neuron is usually zero (on for 0.145, mean 0.266), only slightly lowering the W and Z scores; the formula calls them W and is right 0.603 of the time.
- `✓✓✓·✓✓·✓·········✓✓·······················` **Two-prong Z/W jets** — 22.4% of jets, neuron 0.63, formula right for 73%. Mostly Z (45%) with W (29%) and t (16%), mass 58.3 GeV and 65% of pT at 0.05-0.1 from the axis, i.e. two prongs with little wide-angle radiation. girth2 < 0.013, girth2 < 0.0088 and e2 > 0.028 (which passes far more often than elsewhere) subtract, and mass > 37 and lam2 < 0.0013 and mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9 do not fully compensate. The neuron is on for only 0.211 of jets (mean 0.626), so it lowers the W and Z scores just a little; the formula calls them Z and is right 0.726 of the time.
- `···✓✓✓✓✓✓·✓··✓✓✓·✓✓···········✓···········` **Moderately wide top jets** — 5.6% of jets, neuron 5.83, formula right for 77%. Mostly tops (76%, g 17%), 64.2 GeV, about 2.4 times the average width with 43% of pT beyond 0.1 from the axis. They escape girth2 < 0.0088 and mostly girth2 < 0.013, and gain from LHA > 0.32 (+3.205), centroid_offset > 0.013, max_dr > 0.15 and mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9, against e2 > 0.028 and mass_over_sum_pt > 0.07 and tau32 < 0.52. The neuron is high (5.829), lowering the W and Z scores strongly and raising t; the formula calls them t and is right 0.769 of the time, the gluons being the errors.
- `···✓✓✓✓·✓✓✓✓·✓✓✓✓✓✓···✓✓··················` **Wide heavy top jets** — 3.9% of jets, neuron 6.22, formula right for 92%. Almost all tops (92%), 82.6 GeV, nearly four times the average width with 77% of pT beyond 0.1. Large pluses LHA > 0.32 (+8.273), mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9, e2 > 0.051 and width > 0.019 and pt_dispersion < 0.49 are partly cancelled by e2 > 0.028, mass_over_sum_pt > 0.07 and tau32 < 0.52 and LHA > 0.32 and planar_flow > 0.012. The neuron is high (6.218), lowering W and Z and raising t; the formula calls them t and is right 0.921 of the time.
- `···✓✓✓✓✓✓··✓✓✓✓✓·✓✓···✓✓··················` **Wide elongated top/gluon jets** — 3.3% of jets, neuron 8.22, formula right for 73%. Mostly tops (71%) with gluons (19%), 78.4 GeV, with 74% of pT beyond 0.1 and an elongated shape. Besides LHA > 0.32 (+6.423) they nearly all pass LHA > 0.31 and eccentricity > 0.96 (+5.27), which is rare elsewhere, plus mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9 and mass > 37 and lam2 < 0.0013, with e2 > 0.028 the main minus. This gives the neuron's highest value (8.218), pushing W and Z down and t up; the formula calls them t and is right 0.73 of the time, the gluons being misread.
- `···✓✓✓✓·✓✓✓✓·✓✓✓·✓✓·✓·✓✓··················` **Very wide soft-leading top jets** — 1.8% of jets, neuron 7.13, formula right for 91%. Almost all tops (91%), 89.7 GeV, five times the average width with 89% of pT beyond 0.1 and a soft leading particle (118 GeV). Huge pluses LHA > 0.32 (+11.708), width > 0.019 and pt_dispersion < 0.49 (+9.816), lam1 > 0.016 and mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9 beat the minuses mass_over_sum_pt > 0.07 and tau32 < 0.52, LHA > 0.32 and planar_flow > 0.012 and e2 > 0.028. The neuron is high (7.129), lowering W and Z and raising t; the formula calls them t and is right 0.91 of the time.
- `···✓✓✓✓✓✓✓·✓✓✓✓✓·✓✓···✓✓·······✓··········` **Very wide heavy top/gluon mix** — 1.0% of jets, neuron 7.94, formula right for 67%. Tops (57%) mixed with many gluons (31%), the heaviest group (96.5 GeV), five times the average width with 89% of pT beyond 0.1. All the width tests fire: LHA > 0.32 (+11.363), LHA > 0.31 and eccentricity > 0.96, width > 0.019 and pt_dispersion < 0.49, lam1 > 0.016 and lam1 > 0.018 and eccentricity > 0.96 (which almost only passes here), against e2 > 0.028. The neuron is very high (7.938), pushing W and Z down and t up; the formula calls them t and is right only 0.667 of the time, since wide gluons look the same here.
- `···✓✓✓✓·✓✓✓✓·✓✓✓✓✓····✓✓··················` **Wide jets with soft tail** — 0.7% of jets, neuron 7.94, formula right for 71%. Tops (68%) with gluons (23%), 81.5 GeV, very wide (0.0336) and of low pT (475 GeV) with a soft 7th and 8th particle (8th at 25.0 GeV). The decisive tests are the rarely-passed lam1 > 0.012 and pt_6 < 38 (+15.15) and lam1 > 0.0086 and pt_7 < 38 (+11.585), on top of LHA > 0.32 and lam1 > 0.016, with e2 > 0.028 the main minus. The neuron is very high (7.942), lowering W and Z and raising t; the formula calls them t and is right 0.707 of the time.
- `···✓✓✓✓✓✓✓✓✓·✓✓✓·✓✓·✓·✓✓·✓···✓✓✓···✓······` **Heavy core plus wide halo tops** — 0.2% of jets, neuron 5.80, formula right for 92%. A tiny group (0.24%) of almost all tops (92%), 81.3 GeV, with an unusual split: 43% of pT within 0.05 and 51% beyond 0.1. It is defined by a pair that only fires here: mass_over_sum_pt > 0.11 and dr_7 < 0.049 (+24.105) against mass_over_sum_pt > 0.069 and dr_7 < 0.042 (-18.27), leaving a net plus that, with lam1 > 0.016 and width > 0.019 and pt_dispersion < 0.49, outweighs e2 > 0.028 and mass_over_sum_pt > 0.07 and tau32 < 0.52. The neuron is high (5.798), lowering W and Z and raising t; the formula calls them t and is right 0.923 of the time.

### neuron 4: Low C2/D2, moderate width (major)

- **What it measures:** Rises for jets of moderate width (girth2 > 0.0034 and girth < 0.13 push it up) with small e2_sq (< 0.017, its largest term) and small τ21 (< 0.24); it falls as C2 and D2 grow (-0.484, -0.444), i.e. when energy is spread beyond two prongs. Almost every jet has a sizeable value: largest for Z (7.18), then g (6.69), W (6.57), q (5.83), and lowest for t (4.71).
- *computed — its value:* largest for Z (7.18), then g (6.69), then W (6.57), then q (5.83), then t (4.71); it separates t jets from the rest best (AUC 0.36: small for t)
- **How the class scores use it:** The Z (+15%) and t (+18%) scores add it and the q (-26%) and g (-7%) scores subtract it, so a high value mainly pulls jets away from q toward Z. Tops sit lowest on this scale, so its place in the t score acts as a counterweight against q rather than as a top signature; it does not enter the W score.
- *computed — used by:* raises the score of Z (+15%), t (+18%); lowers the score of g (-7%), q (-26%); does not (or hardly) enter the score of W (share of each class score’s average input)

```
z = -6.77
if e2_sq < 0.017: z += 526 × (0.017 − e2_sq)
if girth < 0.130: z += 49.20 × (0.130 − girth)
if girth2 > 0.0034: z += 839 × (girth2 − 0.0034)
if tau21 < 0.240: z += 41.10 × (0.240 − tau21)
if C2 > 0.013: z += -83.00 × (C2 − 0.013)
if tau21 < 0.260 and lam2 < 0.0013: z += -16900 × (0.260 − tau21) × (0.0013 − lam2)
if e2 > 0.020: z += 87.90 × (e2 − 0.020)
if e2_sq < 0.003: z += -1110 × (0.003 − e2_sq)
if mass_over_sum_pt > 0.089: z += -137 × (mass_over_sum_pt − 0.089)
if mass < 44.00: z += 0.082 × (44.00 − mass)
if girth2 > 0.0081: z += -484 × (girth2 − 0.0081)
if lam2 < 0.00033: z += -4450 × (0.00033 − lam2)
if max_dr > 0.094: z += 18.40 × (max_dr − 0.094)
if sum_pt < 760: z += 0.0059 × (760 − sum_pt)
if mass_over_sum_pt > 0.110: z += 102 × (mass_over_sum_pt − 0.110)
if centroid_offset < 0.014: z += 96.80 × (0.014 − centroid_offset)
if centroid_offset < 0.013 and z_dr_0p05_0p1 < 0.650: z += -231 × (0.013 − centroid_offset) × (0.650 − z_dr_0p05_0p1)
if width > -0.00013 and C2 < 0.063: z += 2140 × (width − -0.00013) × (0.063 − C2)
if sum_pt_top5 < 430: z += 0.022 × (430 − sum_pt_top5)
if girth2_top2 < 0.0087 and centroid_offset > 0.016: z += 17100 × (0.0087 − girth2_top2) × (centroid_offset − 0.016)
if C2 > 0.067: z += -102 × (C2 − 0.067)
if max_dr > 0.200: z += -24.60 × (max_dr − 0.200)
if tau21 < 0.230 and mass < 65.00: z += -0.618 × (0.230 − tau21) × (65.00 − mass)
if e2 > 0.064: z += -165 × (e2 − 0.064)
if max_dr > 0.110 and eccentricity > 0.980: z += -952 × (max_dr − 0.110) × (eccentricity − 0.980)
if C2 > 0.015 and pt_7 > 39.00: z += 9.44 × (C2 − 0.015) × (pt_7 − 39.00)
if tau21 < 0.250 and e2_sq > 0.011: z += -2370 × (0.250 − tau21) × (e2_sq − 0.011)
if tau21 < 0.230 and sum_pt_top2 < 410: z += 0.043 × (0.230 − tau21) × (410 − sum_pt_top2)
if tau21 < 0.240 and pt_7 > 32.00: z += 0.476 × (0.240 − tau21) × (pt_7 − 32.00)
if C2 > 0.065 and pt_7 < 36.00: z += -9.53 × (C2 − 0.065) × (36.00 − pt_7)
if max_dr > 0.098 and pt_7 > 38.00: z += -1.64 × (max_dr − 0.098) × (pt_7 − 38.00)
if tau21 < 0.290 and pt_7 < 24.00: z += -1.15 × (0.290 − tau21) × (24.00 − pt_7)
if mass < 70.00 and mean_eta2 > 0.0044: z += -6.87 × (70.00 − mass) × (mean_eta2 − 0.0044)
if tau21 < 0.220 and mean_phi < -0.028: z += -416 × (0.220 − tau21) × (-0.028 − mean_phi)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `e2_sq < 0.017`; 2: `girth < 0.13`; 3: `girth2 > 0.0034`; 4: `tau21 < 0.24`; 5: `C2 > 0.013`; 6: `tau21 < 0.26 and lam2 < 0.0013`; 7: `e2 > 0.02`; 8: `e2_sq < 0.003`; 9: `mass_over_sum_pt > 0.089`; 10: `mass < 44`; 11: `girth2 > 0.0081`; 12: `lam2 < 0.00033`; 13: `max_dr > 0.094`; 14: `sum_pt < 760`; 15: `mass_over_sum_pt > 0.11`; 16: `centroid_offset < 0.014`; 17: `centroid_offset < 0.013 and z_dr_0p05_0p1 < 0.65`; 18: `width > -0.00013 and C2 < 0.063`; 19: `sum_pt_top5 < 430`; 20: `girth2_top2 < 0.0087 and centroid_offset > 0.016`; 21: `C2 > 0.067`; 22: `max_dr > 0.2`; 23: `tau21 < 0.23 and mass < 65`; 24: `e2 > 0.064`; 25: `max_dr > 0.11 and eccentricity > 0.98`; 26: `C2 > 0.015 and pt_7 > 39`; 27: `tau21 < 0.25 and e2_sq > 0.011`; 28: `tau21 < 0.23 and sum_pt_top2 < 410`; 29: `tau21 < 0.24 and pt_7 > 32`; 30: `C2 > 0.065 and pt_7 < 36`; 31: `max_dr > 0.098 and pt_7 > 38`; 32: `tau21 < 0.29 and pt_7 < 24`; 33: `mass < 70 and mean_eta2 > 0.0044`; 34: `tau21 < 0.22 and mean_phi < -0.028`):

- `✓✓·····✓·✓·✓···✓✓✓················` **Pencil-thin light quark/gluon jets** — 35.5% of jets, neuron 6.63, formula right for 59%. The largest group (35.5%), mostly light quarks (42%) with gluons (36%), nearly massless (9.6 GeV) with 96% of pT within 0.05 of the axis. e2_sq < 0.017 (+8.81), girth < 0.13 and mass < 44 always pass, while the only big minus, e2_sq < 0.003 (-3.051), also always passes here and nowhere else as often; girth2 > 0.0034 and e2 > 0.02 almost never pass. The neuron is on for every jet (6.633), which raises the Z and t scores and lowers q and g, the same as for most groups, so it does little to separate them; the formula splits them between q and g and is right only 0.592 of the time.
- `✓✓✓✓✓✓✓····✓✓✓·✓·✓····✓·✓··✓✓·····` **Clean two-prong Z/W jets** — 17.2% of jets, neuron 9.12, formula right for 77%. Mostly Z (46%) with W (35%) and some tops, mass 61.0 GeV with 65% of pT at 0.05-0.1 from the axis, i.e. two well-separated prongs. Every jet passes tau21 < 0.24 (+6.883) on top of e2_sq < 0.017, girth2 > 0.0034, girth < 0.13 and e2 > 0.02, while being too heavy for mass < 44 and too spread for e2_sq < 0.003; tau21 < 0.26 and lam2 < 0.0013 takes back 3.936. This gives the neuron's highest value (9.116), raising the Z and t scores and lowering q and g; the formula calls them Z and is right 0.772 of the time, the errors being mostly W-Z swaps.
- `✓✓✓✓✓✓✓····✓✓✓···✓····✓·✓··✓✓·····` **Medium-mass two-prong W jets** — 12.7% of jets, neuron 6.07, formula right for 63%. W-led (43%) with Z (28%), 46.7 GeV, a bit narrower than average with pT split between the core (59%) and 0.05-0.1. e2_sq < 0.017, tau21 < 0.24 and girth < 0.13 all pass, reduced by tau21 < 0.26 and lam2 < 0.0013, lam2 < 0.00033 and tau21 < 0.23 and mass < 65 (which passes far more often here). The neuron is well on (6.072), adding to Z and t and taking from q and g; the formula calls them W and is right 0.626 of the time.
- `✓✓✓·✓·✓··✓·✓✓✓···✓·✓··············` **Compact medium-mass mixed jets** — 11.7% of jets, neuron 4.66, formula right for 54%. A mixture (W 34%, Z 25%, g 18%, q 14%) at 38.3 GeV, fairly narrow (70% of pT within 0.05) and without a clean two-prong shape. They pass e2_sq < 0.017, girth < 0.13 and mostly max_dr > 0.094, but all pass C2 > 0.013 (-2.74) and most fail tau21 < 0.24, so the neuron is lower than for the clean boson groups (4.661, on for 0.9). It still pushes Z and t up and q and g down; the formula calls them W but is right only 0.542 of the time.
- `✓✓✓·✓·✓·····✓✓···✓················` **Moderately wide low-pT mixed jets** — 7.0% of jets, neuron 7.04, formula right for 61%. A real mixture (Z 33%, t 24%, g 18%, W 17%) of 48.8 GeV, somewhat wider than average, with low total pT (580 GeV) and a soft leading particle. Nearly all pass e2_sq < 0.017, girth2 > 0.0034 (+3.916), girth < 0.13, e2 > 0.02, max_dr > 0.094 and sum_pt < 760, with only C2 > 0.013 (-2.709) against; tau21 < 0.24 passes for under half. The neuron is high (7.044), raising Z and t and lowering q and g; the formula calls them Z but is right only 0.609 of the time.
- `✓✓✓✓✓✓✓·✓·✓✓✓✓✓··✓······✓·✓✓✓·····` **Wide two-prong-looking top jets** — 4.2% of jets, neuron 7.16, formula right for 76%. Mostly tops (74%, g 16%), 70.6 GeV, about 2.4 times the average width with 58% of pT beyond 0.1. girth2 > 0.0034 (+9.971) and tau21 < 0.24 (+6.393) dominate, against mass_over_sum_pt > 0.089, girth2 > 0.0081, tau21 < 0.26 and lam2 < 0.0013 and tau21 < 0.25 and e2_sq > 0.011, the last two firing much more than elsewhere. The neuron stays high (7.161), raising Z and t and lowering q and g; the formula calls them t and is right 0.756 of the time.
- `··✓·✓·✓·✓·✓·✓✓✓···✓·✓✓·✓·····✓····` **Wide heavy three-prong tops** — 4.2% of jets, neuron 0.37, formula right for 93%. Almost all tops (93%), 84.8 GeV, four times the average width with 76% of pT beyond 0.1. They fail e2_sq < 0.017 and tau21 < 0.24, so the big plus girth2 > 0.0034 (+19.26), with e2 > 0.02 and mass_over_sum_pt > 0.11, is beaten by mass_over_sum_pt > 0.089 (-9.407), girth2 > 0.0081, C2 > 0.013 and e2 > 0.064. The neuron is mostly off (on for 0.157, mean 0.373), so it barely adds to the scores; the formula calls them t anyway and is right 0.93 of the time.
- `✓✓✓·✓·✓·✓·✓·✓✓✓·····✓✓·······✓····` **Wide top jets, high C2** — 3.9% of jets, neuron 0.87, formula right for 82%. Mostly tops (81%, g 14%), 71.5 GeV, 2.8 times the average width with half the pT beyond 0.1. girth2 > 0.0034 (+11.914), e2 > 0.02 and max_dr > 0.094 are outweighed by C2 > 0.013 (-6.433), mass_over_sum_pt > 0.089, girth2 > 0.0081 and, for most, C2 > 0.067, while tau21 < 0.24 mostly fails. The neuron is usually zero (on for 0.28, mean 0.867); the formula calls them t and is right 0.817 of the time.
- `··✓✓✓✓✓·✓·✓✓✓✓✓··✓···✓·✓✓·✓✓✓·····` **Very wide jets with small tau21** — 2.1% of jets, neuron 4.74, formula right for 71%. Tops (67%) with gluons (23%), 87.7 GeV, four times the average width with 84% of pT beyond 0.1, but with a two-prong-like tau21. Unlike the other wide groups they all pass tau21 < 0.24 (+6.772), which with girth2 > 0.0034 (+18.281), e2 > 0.02 and mass_over_sum_pt > 0.11 beats mass_over_sum_pt > 0.089, girth2 > 0.0081 and tau21 < 0.25 and e2_sq > 0.011 (almost only passing here). The neuron is on (4.743), raising Z and t; the formula calls them t and is right 0.709 of the time, the gluons being the main errors.
- `··✓·✓·✓·✓·✓·✓✓✓···✓·✓✓·✓··········` **Widest soft-leading top jets** — 1.5% of jets, neuron 1.07, formula right for 80%. Tops (77%) with gluons (18%), 90.4 GeV, the widest group (0.0369) with 89% of pT beyond 0.1 and a soft leading particle (124 GeV). The huge plus girth2 > 0.0034 (+28.087), with mass_over_sum_pt > 0.11 and e2 > 0.02, is cancelled by girth2 > 0.0081, mass_over_sum_pt > 0.089, C2 > 0.013 and e2 > 0.064, and girth < 0.13 never passes. The neuron is usually zero (on for 0.337, mean 1.073); the formula calls them t and is right 0.795 of the time.

### neuron 9: Narrow, centred one-prong jet (major)

- **What it measures:** Rises for narrow jets (width < 0.0061 is its largest term; max ΔR < 0.23 and centroid offset < 0.018 also push it up); overall it falls with λ1 (-0.734), width and girth2 (-0.727). Largest for q (9.14) and g (7.10), far lower for W (2.50), t (1.77) and Z (1.45).
- *computed — its value:* largest for q (9.14), then g (7.10), then W (2.50), then t (1.77), then Z (1.45); it separates q jets from the rest best (AUC 0.80: large for q)
- **How the class scores use it:** The q (+49%) and g (+27%) scores are built mainly on it, since both light-parton types sit high; the Z (-4%) and W (-3%) scores subtract a little. It does not enter the t score, which uses the related compactness scale (neuron 13) instead.
- *computed — used by:* raises the score of g (+27%), q (+49%); lowers the score of W (-3%), Z (-4%); does not (or hardly) enter the score of t (share of each class score’s average input)

```
z = -1.82
if width < 0.0061: z += 3030 × (0.0061 − width)
if mass_over_sum_pt < 0.076: z += -127 × (0.076 − mass_over_sum_pt)
if mass_over_sum_pt_sq < 0.0033: z += 1400 × (0.0033 − mass_over_sum_pt_sq)
if mass < 55.00 and centroid_offset < 0.026: z += 5.17 × (55.00 − mass) × (0.026 − centroid_offset)
if girth < 0.055: z += -92.30 × (0.055 − girth)
if mass < 43.00 and centroid_offset < 0.027: z += -6.37 × (43.00 − mass) × (0.027 − centroid_offset)
if max_dr < 0.230: z += 12.10 × (0.230 − max_dr)
if width < 0.0059 and centroid_offset > 0.0029: z += -48100 × (0.0059 − width) × (centroid_offset − 0.0029)
if centroid_offset < 0.018: z += 151 × (0.018 − centroid_offset)
if mass < 52.00 and log_sum_pt < 6.80: z += 0.190 × (52.00 − mass) × (6.80 − log_sum_pt)
if e2 < 0.017 and centroid_offset < 0.024: z += 11400 × (0.017 − e2) × (0.024 − centroid_offset)
if centroid_offset < 0.018 and z_4 > 0.043: z += -2590 × (0.018 − centroid_offset) × (z_4 − 0.043)
if e2 < 0.032 and dr01 < 0.056: z += 823 × (0.032 − e2) × (0.056 − dr01)
if mass_over_sum_pt < 0.072 and girth2_top2 < 0.00078: z += -35700 × (0.072 − mass_over_sum_pt) × (0.00078 − girth2_top2)
if log_sum_pt > 6.40: z += -2.06 × (log_sum_pt − 6.40)
if girth2 < 0.0046 and centroid_offset > 0.011: z += -60200 × (0.0046 − girth2) × (centroid_offset − 0.011)
if centroid_offset < 0.018 and pt_4 > 49.00: z += 3.08 × (0.018 − centroid_offset) × (pt_4 − 49.00)
if mass < 51.00 and planar_flow < 0.320: z += 0.219 × (51.00 − mass) × (0.320 − planar_flow)
if girth2 > 0.018: z += 326 × (girth2 − 0.018)
if centroid_offset < 0.018 and z_5 > 0.033: z += -1200 × (0.018 − centroid_offset) × (z_5 − 0.033)
if girth2_top2 < 0.00073 and z_7 > 0.023: z += -69100 × (0.00073 − girth2_top2) × (z_7 − 0.023)
if e2 < 0.019 and pt_7 < 53.00: z += -2.29 × (0.019 − e2) × (53.00 − pt_7)
if sum_pt > 850: z += -0.0091 × (sum_pt − 850)
if e2 < 0.032 and tau21 < 0.450: z += -265 × (0.032 − e2) × (0.450 − tau21)
if mean_phi < 0.00042: z += -34.10 × (0.00042 − mean_phi)
if n_dr_0p2_0p4 > 0.900: z += 1.09 × (n_dr_0p2_0p4 − 0.900)
if mass < 33.00 and planar_flow < 0.320: z += -0.335 × (33.00 − mass) × (0.320 − planar_flow)
if C2 > 0.051: z += 29.40 × (C2 − 0.051)
if girth2_top2 < 0.00075 and pt_7 > 33.00: z += 111 × (0.00075 − girth2_top2) × (pt_7 − 33.00)
if lam2 > 0.0017: z += 376 × (lam2 − 0.0017)
if C2 > 0.051 and pt_2 < 85.00: z += -1.03 × (C2 − 0.051) × (85.00 − pt_2)
if C2 > 0.048 and dr_5 < 0.190: z += -230 × (C2 − 0.048) × (0.190 − dr_5)
if girth2 > 0.018 and planar_flow < 0.360: z += -581 × (girth2 − 0.018) × (0.360 − planar_flow)
if log_sum_pt > 6.40 and mean_phi > 0.026: z += -2120 × (log_sum_pt − 6.40) × (mean_phi − 0.026)
if girth2 > 0.019 and mean_eta < 0.025: z += -2270 × (girth2 − 0.019) × (0.025 − mean_eta)
if width < 0.006 and C2 > 0.031: z += -9190 × (0.006 − width) × (C2 − 0.031)
if lam2 > 0.001 and mass_top2 > 16.00: z += 10.80 × (lam2 − 0.001) × (mass_top2 − 16.00)
if n_dr_0p2_0p4 > 0.870 and dr_6 > 0.220: z += 9.75 × (n_dr_0p2_0p4 − 0.870) × (dr_6 − 0.220)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.0061`; 2: `mass_over_sum_pt < 0.076`; 3: `mass_over_sum_pt_sq < 0.0033`; 4: `mass < 55 and centroid_offset < 0.026`; 5: `girth < 0.055`; 6: `mass < 43 and centroid_offset < 0.027`; 7: `max_dr < 0.23`; 8: `width < 0.0059 and centroid_offset > 0.0029`; 9: `centroid_offset < 0.018`; 10: `mass < 52 and log_sum_pt < 6.8`; 11: `e2 < 0.017 and centroid_offset < 0.024`; 12: `centroid_offset < 0.018 and z_4 > 0.043`; 13: `e2 < 0.032 and dr01 < 0.056`; 14: `mass_over_sum_pt < 0.072 and girth2_top2 < 0.00078`; 15: `log_sum_pt > 6.4`; 16: `girth2 < 0.0046 and centroid_offset > 0.011`; 17: `centroid_offset < 0.018 and pt_4 > 49`; 18: `mass < 51 and planar_flow < 0.32`; 19: `girth2 > 0.018`; 20: `centroid_offset < 0.018 and z_5 > 0.033`; 21: `girth2_top2 < 0.00073 and z_7 > 0.023`; 22: `e2 < 0.019 and pt_7 < 53`; 23: `sum_pt > 850`; 24: `e2 < 0.032 and tau21 < 0.45`; 25: `mean_phi < 0.00042`; 26: `n_dr_0p2_0p4 > 0.9`; 27: `mass < 33 and planar_flow < 0.32`; 28: `C2 > 0.051`; 29: `girth2_top2 < 0.00075 and pt_7 > 33`; 30: `lam2 > 0.0017`; 31: `C2 > 0.051 and pt_2 < 85`; 32: `C2 > 0.048 and dr_5 < 0.19`; 33: `girth2 > 0.018 and planar_flow < 0.36`; 34: `log_sum_pt > 6.4 and mean_phi > 0.026`; 35: `girth2 > 0.019 and mean_eta < 0.025`; 36: `width < 0.006 and C2 > 0.031`; 37: `lam2 > 0.001 and mass_top2 > 16`; 38: `n_dr_0p2_0p4 > 0.87 and dr_6 > 0.22`):

- `······✓·······✓·········✓·············` **Wide massive top-led jets** — 21.7% of jets, neuron 0.37, formula right for 70%. A top-led mixture (t 46%, Z 25%, g 15%) at 60.1 GeV, about twice the average width with 35% of pT beyond 0.1. Too wide for width < 0.0061 (passes 0.159), the neuron's main plus; what is left are small terms like max_dr < 0.23 (+0.694), mass < 52 and log_sum_pt < 6.8 and mean_phi < 0.00042 (-0.329). The neuron is usually zero (on for 0.263, mean 0.371), barely touching the scores; the formula calls them t and is right 0.699 of the time.
- `······✓·✓··✓··✓·✓··✓····✓·············` **Centred two-prong Z/W jets** — 15.7% of jets, neuron 0.41, formula right for 77%. Z (42%) and W (38%) with some tops, 62.1 GeV, 58% of pT at 0.05-0.1 from the axis and a well-centred pT distribution. centroid_offset < 0.018 (+1.753) and max_dr < 0.23 pass for nearly all, but centroid_offset < 0.018 and z_4 > 0.043 (-1.338), centroid_offset < 0.018 and z_5 > 0.033 and log_sum_pt > 6.4 take most back, and width < 0.0061 mostly fails. The neuron is usually zero (on for 0.348, mean 0.412); the formula splits them evenly between W and Z and is right 0.771 of the time.
- `✓✓✓✓✓✓✓·✓·✓✓✓✓✓·✓··✓✓✓✓·✓·············` **Pencil-thin high-pT quark jets** — 13.6% of jets, neuron 12.09, formula right for 69%. Mostly light quarks (64%, g 24%), essentially massless (6.9 GeV), all pT within 0.05, with above-average pT (905 GeV) and a hard leading particle. width < 0.0061 adds the most here (+18.244, more the narrower the jet), with mass < 55 and centroid_offset < 0.026, mass_over_sum_pt_sq < 0.0033 and e2 < 0.017 and centroid_offset < 0.024, against mass_over_sum_pt < 0.076 (-8.688), mass < 43 and centroid_offset < 0.027 and girth < 0.055. This is the neuron's highest value (12.086), strongly raising q and g and lowering W and Z; the formula calls them q and is right 0.686 of the time.
- `✓✓·✓··✓✓✓✓·✓✓·✓··✓·✓···✓✓·············` **Medium-mass two-prong W jets** — 10.8% of jets, neuron 1.88, formula right for 63%. Mostly W (49%) with Z (27%), 46.9 GeV, of intermediate width (55% of pT within 0.05, 35% at 0.05-0.1). width < 0.0061 passes but adds only +4.769 because they are close to the cut; mass_over_sum_pt < 0.076, width < 0.0059 and centroid_offset > 0.0029 and e2 < 0.032 and tau21 < 0.45 subtract, while max_dr < 0.23, centroid_offset < 0.018 and mass < 52 and log_sum_pt < 6.8 add. The neuron is modest (1.881), nudging g and q up; the formula calls them W and is right 0.633 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓·✓··✓✓✓··✓···✓·········` **Very narrow light gluon/quark jets** — 9.6% of jets, neuron 11.36, formula right for 62%. Gluons (49%) and quarks (38%), light (10.7 GeV), 99% of pT within 0.05, at average pT. width < 0.0061 (+17.49), mass_over_sum_pt_sq < 0.0033, mass < 55 and centroid_offset < 0.026, max_dr < 0.23 and e2 < 0.017 and centroid_offset < 0.024 outweigh mass_over_sum_pt < 0.076, mass < 43 and centroid_offset < 0.027, girth < 0.055 and girth2_top2 < 0.00073 and z_7 > 0.023. The neuron is very high (11.36), raising g and q; the formula calls them g and is right 0.616 of the time, quark-gluon confusion being the error.
- `✓✓✓✓✓✓✓✓·✓··✓·✓✓·✓···✓·✓✓··········✓··` **Compact medium-mass W-led mixture** — 7.6% of jets, neuron 3.10, formula right for 52%. A W-led (39%) mixture with Z (22%), gluons (18%) and quarks (13%) at 36.5 GeV, narrow (77% of pT within 0.05). width < 0.0061 (+9.381) and several smaller pluses (mass_over_sum_pt_sq < 0.0033, mass < 52 and log_sum_pt < 6.8, max_dr < 0.23) beat mass_over_sum_pt < 0.076, width < 0.0059 and centroid_offset > 0.0029, girth2 < 0.0046 and centroid_offset > 0.011 and e2 < 0.032 and tau21 < 0.45. The neuron is on (3.099), raising g and q and slightly lowering W and Z; the formula calls them W but is right only 0.522 of the time.
- `··················✓······✓·✓·✓✓✓··✓···` **Very wide top jets** — 6.1% of jets, neuron 3.59, formula right for 86%. Mostly tops (84%), 87.7 GeV, 4.6 times the average width with 81% of pT beyond 0.1. They never pass width < 0.0061, but a separate set switches the neuron on: girth2 > 0.018 (+3.762), n_dr_0p2_0p4 > 0.9, lam2 > 0.0017 and C2 > 0.051, partly cancelled by girth2 > 0.018 and planar_flow < 0.36, C2 > 0.051 and pt_2 < 85 and girth2 > 0.019 and mean_eta < 0.025. The neuron is on (3.587), raising g and q rather than t, yet the formula calls them t and is right 0.862 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓·✓✓·✓·✓·✓✓·✓···········` **Narrow light gluon/quark jets** — 5.3% of jets, neuron 8.70, formula right for 54%. Gluons (39%) and quarks (34%) with some W, 25.8 GeV, narrow (89% of pT within 0.05). width < 0.0061 (+14.153), mass_over_sum_pt_sq < 0.0033 and mass < 55 and centroid_offset < 0.026 beat mass_over_sum_pt < 0.076, girth < 0.055, mass < 43 and centroid_offset < 0.027, width < 0.0059 and centroid_offset > 0.0029 and e2 < 0.032 and tau21 < 0.45. The neuron is high (8.701), raising g and q; the formula calls them g but is right only 0.539 of the time.
- `✓✓✓✓✓✓✓✓·✓✓·✓✓✓✓·✓··✓✓··✓·✓···········` **Massless slightly off-centre mixture** — 4.9% of jets, neuron 5.62, formula right for 47%. A gluon-led (37%) mixture with W (23%), quarks (21%) and Z (16%), nearly massless (8.4 GeV) and narrow, with the pT centroid slightly off the axis. width < 0.0061 (+16.865), mass_over_sum_pt_sq < 0.0033 and max_dr < 0.23 outweigh mass_over_sum_pt < 0.076, width < 0.0059 and centroid_offset > 0.0029, girth < 0.055 and girth2 < 0.0046 and centroid_offset > 0.011 (passing for all here). The neuron is high (5.625), raising g and q even for the bosons; the formula calls them g but is right only 0.467 of the time.
- `✓✓✓·✓·✓✓·✓··✓·✓✓·✓···✓··✓·✓···········` **Light off-centre mixed jets** — 4.6% of jets, neuron 1.94, formula right for 44%. A mixture (g 33%, Z 25%, W 20%, q 13%), nearly massless (9.7 GeV) with a softer leading particle (185 GeV) and a clearly off-centre pT centroid. No jet passes centroid_offset < 0.018, and the off-centre penalties width < 0.0059 and centroid_offset > 0.0029 (-6.218) and girth2 < 0.0046 and centroid_offset > 0.011, together with mass_over_sum_pt < 0.076 and mass < 33 and planar_flow < 0.32, eat most of width < 0.0061 (+13.892). The neuron is moderate (1.939, on for 0.649); the formula calls them g but is right only 0.435 of the time, many being low-mass bosons.

### neuron 10: Broad, massive, spread-out jet (major)

- **What it measures:** Rises for jets spread out in both directions (λ2 < 0.0034, its largest term, pushes it down; girth2 > 0.0085 up) with mass/pT < 0.1 and mass > 17 GeV; overall it grows with max ΔR (+0.603), mass (+0.556) and C2 (+0.543). Largest for t (4.14), then W (1.39), Z (1.21), g (0.97) and q (0.61).
- *computed — its value:* largest for t (4.14), then W (1.39), then Z (1.21), then g (0.97), then q (0.61); it separates q jets from the rest best (AUC 0.25: small for q)
- **How the class scores use it:** The t score adds it (+14%) and the q score subtracts it (-9%), since tops sit highest and quarks lowest on this scale. It does not enter the g, W or Z scores.
- *computed — used by:* raises the score of t (+14%); lowers the score of q (-9%); does not (or hardly) enter the score of g, W, Z (share of each class score’s average input)

```
z = 2.32
if lam2 < 0.0034: z += -835 × (0.0034 − lam2)
if mass_over_sum_pt < 0.100: z += 41.30 × (0.100 − mass_over_sum_pt)
if girth2 > 0.0085: z += 494 × (girth2 − 0.0085)
if e2 < 0.037: z += -56.70 × (0.037 − e2)
if girth2 < 0.0017: z += -1460 × (0.0017 − girth2)
if lam1 > 0.0085: z += -347 × (lam1 − 0.0085)
if mass > 17.00: z += 0.024 × (mass − 17.00)
if girth2_top2 < 0.0038: z += 349 × (0.0038 − girth2_top2)
if lam1 < 0.0044: z += -271 × (0.0044 − lam1)
if n_dr_0p05_0p1 < 3.00: z += 0.183 × (3.00 − n_dr_0p05_0p1)
if e2 > 0.036: z += 45.90 × (e2 − 0.036)
if eccentricity > 0.890 and z_dr_0p2_0p4 < 0.044: z += 149 × (eccentricity − 0.890) × (0.044 − z_dr_0p2_0p4)
if log_sum_pt > 6.70: z += -8.24 × (log_sum_pt − 6.70)
if LHA > 0.300 and tau21 < 0.570: z += -40.70 × (LHA − 0.300) × (0.570 − tau21)
if girth2_top3 < 0.0016: z += 463 × (0.0016 − girth2_top3)
if eccentricity > 0.890 and mass_top2 < 37.00: z += -0.145 × (eccentricity − 0.890) × (37.00 − mass_top2)
if LHA > 0.330: z += -17.00 × (LHA − 0.330)
if log_sum_pt < 6.30: z += -5.54 × (6.30 − log_sum_pt)
if mass > 8.00 and n_dr_0p2_0p4 < 1.90: z += -0.0033 × (mass − 8.00) × (1.90 − n_dr_0p2_0p4)
if tau32 < 0.270: z += 9.95 × (0.270 − tau32)
if C2 > 0.055: z += 24.20 × (C2 − 0.055)
if lam1 < 0.0044 and log_sum_pt > 6.80: z += 2070 × (0.0044 − lam1) × (log_sum_pt − 6.80)
if z_7 > 0.062: z += -18.00 × (z_7 − 0.062)
if lam2 > 0.00048 and n_pt_above_50 < 8.10: z += -49.50 × (lam2 − 0.00048) × (8.10 − n_pt_above_50)
if lam2 > 0.00023 and tau21 < 0.510: z += 1370 × (lam2 − 0.00023) × (0.510 − tau21)
if n_dr_0p2_0p4 > 1.90: z += 0.756 × (n_dr_0p2_0p4 − 1.90)
if lam1 > 0.0083 and min_pair_mass < 2.80: z += -16.30 × (lam1 − 0.0083) × (2.80 − min_pair_mass)
if pt_7 > 46.00: z += 0.033 × (pt_7 − 46.00)
if tau32 < 0.270 and n_dr_0p2_0p4 < 2.00: z += -3.53 × (0.270 − tau32) × (2.00 − n_dr_0p2_0p4)
if centroid_offset > 0.038: z += 17.50 × (centroid_offset − 0.038)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `lam2 < 0.0034`; 2: `mass_over_sum_pt < 0.1`; 3: `girth2 > 0.0085`; 4: `e2 < 0.037`; 5: `girth2 < 0.0017`; 6: `lam1 > 0.0085`; 7: `mass > 17`; 8: `girth2_top2 < 0.0038`; 9: `lam1 < 0.0044`; 10: `n_dr_0p05_0p1 < 3`; 11: `e2 > 0.036`; 12: `eccentricity > 0.89 and z_dr_0p2_0p4 < 0.044`; 13: `log_sum_pt > 6.7`; 14: `LHA > 0.3 and tau21 < 0.57`; 15: `girth2_top3 < 0.0016`; 16: `eccentricity > 0.89 and mass_top2 < 37`; 17: `LHA > 0.33`; 18: `log_sum_pt < 6.3`; 19: `mass > 8 and n_dr_0p2_0p4 < 1.9`; 20: `tau32 < 0.27`; 21: `C2 > 0.055`; 22: `lam1 < 0.0044 and log_sum_pt > 6.8`; 23: `z_7 > 0.062`; 24: `lam2 > 0.00048 and n_pt_above_50 < 8.1`; 25: `lam2 > 0.00023 and tau21 < 0.51`; 26: `n_dr_0p2_0p4 > 1.9`; 27: `lam1 > 0.0083 and min_pair_mass < 2.8`; 28: `pt_7 > 46`; 29: `tau32 < 0.27 and n_dr_0p2_0p4 < 2`; 30: `centroid_offset > 0.038`):

- `✓✓····✓···✓✓·✓·✓··✓···········` **** — 27.0% of jets, neuron 1.25, formula right for 71%.  
- `✓✓·✓✓··✓✓✓····✓···············` **** — 22.3% of jets, neuron 0.44, formula right for 59%.  
- `✓✓·✓··✓✓✓✓·✓···✓··✓···········` **** — 16.9% of jets, neuron 1.58, formula right for 60%.  
- `✓✓·✓✓·✓✓✓✓·✓··✓✓··✓···········` **** — 10.9% of jets, neuron 1.29, formula right for 50%.  
- `✓✓·✓✓··✓✓✓··✓·✓······✓········` **** — 6.5% of jets, neuron 0.08, formula right for 71%.  
- `✓·✓··✓✓···✓··✓·✓✓·✓····✓✓·✓···` **** — 5.7% of jets, neuron 2.74, formula right for 75%.  
- `✓·✓··✓✓··✓✓··✓·✓✓·✓···✓·✓·✓···` **** — 3.4% of jets, neuron 2.27, formula right for 76%.  
- `✓·✓··✓✓··✓✓··✓··✓✓·✓✓·✓✓✓✓✓···` **** — 3.3% of jets, neuron 7.24, formula right for 85%.  
- `··✓··✓✓··✓✓··✓··✓··✓✓·✓✓✓✓✓···` **** — 3.0% of jets, neuron 9.22, formula right for 96%.  
- `✓·✓··✓✓··✓✓··✓··✓✓··✓·✓✓✓✓✓··✓` **** — 0.9% of jets, neuron 7.72, formula right for 68%.  

### neuron 11: Compact, centred, flat jet (major)

- **What it measures:** Rises for fairly compact jets (width < 0.0085) whose pT centroid sits near the axis (centroid offset < 0.04) and with low planar flow (< 0.27), while girth < 0.089 pulls it down; overall it falls with centroid offset (-0.602) and grows with total pT (+0.499). Largest for W (4.79), then Z (3.50), q (3.42) and g (2.89), and far lower for t (0.83).
- *computed — its value:* largest for W (4.79), then Z (3.50), then q (3.42), then g (2.89), then t (0.83); it separates t jets from the rest best (AUC 0.13: small for t)
- **How the class scores use it:** Only the W score uses it (+26%, the W score's largest input), because W jets sit highest; the sizeable values on Z, q and g jets are countered by other inputs of the W score (neurons 14 and 15 for Z-like jets, 8 and 9 for narrow jets). It does not enter the g, q, Z or t scores.
- *computed — used by:* raises the score of W (+26%); does not (or hardly) enter the score of g, q, Z, t (share of each class score’s average input)

```
z = -0.351
if width < 0.0085: z += 1320 × (0.0085 − width)
if centroid_offset < 0.040: z += 98.30 × (0.040 − centroid_offset)
if girth < 0.089: z += -61.90 × (0.089 − girth)
if sum_pt_top5 < 690: z += 0.009 × (690 − sum_pt_top5)
if planar_flow < 0.270: z += 9.88 × (0.270 − planar_flow)
if e2_sq < 0.0062: z += -393 × (0.0062 − e2_sq)
if girth > 0.076: z += -103 × (girth − 0.076)
if centroid_offset < 0.050 and log_sum_pt < 6.80: z += -133 × (0.050 − centroid_offset) × (6.80 − log_sum_pt)
if girth > 0.089 and n_pt_above_50 < 7.10: z += -37.20 × (girth − 0.089) × (7.10 − n_pt_above_50)
if girth > 0.077 and n_pt_above_50 < 7.00: z += 27.40 × (girth − 0.077) × (7.00 − n_pt_above_50)
if max_dr < 0.220: z += 6.36 × (0.220 − max_dr)
if centroid_offset > 0.014: z += -84.60 × (centroid_offset − 0.014)
if width < 0.0036: z += -425 × (0.0036 − width)
if C2 < 0.035: z += -27.10 × (0.035 − C2)
if planar_flow < 0.270 and mass < 71.00: z += -0.147 × (0.270 − planar_flow) × (71.00 − mass)
if planar_flow < 0.210 and width > 0.0056: z += -1310 × (0.210 − planar_flow) × (width − 0.0056)
if girth > 0.075 and pt_7 < 40.00: z += -4.29 × (girth − 0.075) × (40.00 − pt_7)
if n_dr_0p1_0p2 < 2.80: z += -0.160 × (2.80 − n_dr_0p1_0p2)
if log_sum_pt < 6.70 and dr_0 < 0.120: z += -27.80 × (6.70 − log_sum_pt) × (0.120 − dr_0)
if planar_flow < 0.230 and girth2 > 0.015: z += 3710 × (0.230 − planar_flow) × (girth2 − 0.015)
if girth2_top3 < 0.002: z += -399 × (0.002 − girth2_top3)
if girth < 0.021: z += -77.50 × (0.021 − girth)
if girth2 < 0.013 and mean_phi < -0.0014: z += -6780 × (0.013 − girth2) × (-0.0014 − mean_phi)
if e2_sq < 0.0063 and mean_phi < -1.8e-05: z += 14900 × (0.0063 − e2_sq) × (-1.8e-05 − mean_phi)
if planar_flow < 0.260 and max_dr > 0.110: z += -33.10 × (0.260 − planar_flow) × (max_dr − 0.110)
if girth2 < 0.014 and mean_phi > 0.0032: z += -6840 × (0.014 − girth2) × (mean_phi − 0.0032)
if pt_7 < 30.00 and n_dr_0p2_0p4 < 1.90: z += -0.041 × (30.00 − pt_7) × (1.90 − n_dr_0p2_0p4)
if e2_sq < 0.0062 and mean_phi > 0.0014: z += 15100 × (0.0062 − e2_sq) × (mean_phi − 0.0014)
if centroid_offset > 0.015 and tau21 < 0.110: z += 1650 × (centroid_offset − 0.015) × (0.110 − tau21)
if LHA < 0.160 and z_7 < 0.028: z += 1400 × (0.160 − LHA) × (0.028 − z_7)
if mass_top5 < 5.50: z += 0.103 × (5.50 − mass_top5)
if girth2 < 0.013 and mass_top5 > 49.00: z += 7.00 × (0.013 − girth2) × (mass_top5 − 49.00)
if m01 > 46.00 and n_pt_above_50 > 6.00: z += 0.931 × (m01 − 46.00) × (n_pt_above_50 − 6.00)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.0085`; 2: `centroid_offset < 0.04`; 3: `girth < 0.089`; 4: `sum_pt_top5 < 690`; 5: `planar_flow < 0.27`; 6: `e2_sq < 0.0062`; 7: `girth > 0.076`; 8: `centroid_offset < 0.05 and log_sum_pt < 6.8`; 9: `girth > 0.089 and n_pt_above_50 < 7.1`; 10: `girth > 0.077 and n_pt_above_50 < 7`; 11: `max_dr < 0.22`; 12: `centroid_offset > 0.014`; 13: `width < 0.0036`; 14: `C2 < 0.035`; 15: `planar_flow < 0.27 and mass < 71`; 16: `planar_flow < 0.21 and width > 0.0056`; 17: `girth > 0.075 and pt_7 < 40`; 18: `n_dr_0p1_0p2 < 2.8`; 19: `log_sum_pt < 6.7 and dr_0 < 0.12`; 20: `planar_flow < 0.23 and girth2 > 0.015`; 21: `girth2_top3 < 0.002`; 22: `girth < 0.021`; 23: `girth2 < 0.013 and mean_phi < -0.0014`; 24: `e2_sq < 0.0063 and mean_phi < -1.8e-05`; 25: `planar_flow < 0.26 and max_dr > 0.11`; 26: `girth2 < 0.014 and mean_phi > 0.0032`; 27: `pt_7 < 30 and n_dr_0p2_0p4 < 1.9`; 28: `e2_sq < 0.0062 and mean_phi > 0.0014`; 29: `centroid_offset > 0.015 and tau21 < 0.11`; 30: `LHA < 0.16 and z_7 < 0.028`; 31: `mass_top5 < 5.5`; 32: `girth2 < 0.013 and mass_top5 > 49`; 33: `m01 > 46 and n_pt_above_50 > 6`):

- `✓✓✓··✓·✓··✓·✓✓···✓··✓✓········✓··` **** — 22.1% of jets, neuron 3.74, formula right for 64%.  
- `✓✓✓✓✓✓·✓··✓··✓✓✓·✓✓·····✓········` **** — 20.0% of jets, neuron 4.87, formula right for 72%.  
- `✓✓✓✓✓✓·✓··✓✓✓✓✓··✓✓·✓··✓······✓··` **** — 15.1% of jets, neuron 3.30, formula right for 52%.  
- `✓✓✓✓✓✓·✓··✓✓✓✓✓··✓✓·✓··✓✓········` **** — 14.9% of jets, neuron 3.67, formula right for 55%.  
- `✓✓✓✓✓·✓✓·✓✓✓·✓✓✓✓✓✓·····✓········` **** — 13.4% of jets, neuron 1.77, formula right for 71%.  
- `·✓·✓✓·✓✓✓✓✓✓····✓·✓·····✓········` **** — 7.8% of jets, neuron 0.03, formula right for 81%.  
- `·✓·✓··✓✓✓✓·✓····✓················` **** — 4.2% of jets, neuron 0.00, formula right for 87%.  
- `·✓·✓✓·✓✓✓✓·✓·✓·✓✓··✓····✓········` **** — 1.6% of jets, neuron 0.16, formula right for 70%.  
- `···✓··✓✓✓✓·✓····✓················` **** — 1.0% of jets, neuron 0.00, formula right for 77%.  

### neuron 13: Compactness (not a wide jet) (major)

- **What it measures:** Rises for any jet that is not wide: girth < 0.15 is by far its largest term, with λ1 < 0.015 and λ1 < 0.0062 adding; overall it falls with λ1 (-0.921), width and girth2 (-0.918) and mass/pT (-0.899). High for q (7.27), g (6.04), W (5.48) and Z (5.07), much lower for t (1.83).
- *computed — its value:* largest for q (7.27), then g (6.04), then W (5.48), then Z (5.07), then t (1.83); it separates t jets from the rest best (AUC 0.10: small for t)
- **How the class scores use it:** The t score subtracts it heavily (-48%, its largest input): tops sit far below every other type, so a compact jet is pushed away from top. The Z (+9%) and W (+8%) scores add it; it does not enter the g or q scores.
- *computed — used by:* raises the score of W (+8%), Z (+9%); lowers the score of t (-48%); does not (or hardly) enter the score of g, q (share of each class score’s average input)

```
z = 0.817
if girth < 0.150: z += 64.50 × (0.150 − girth)
if lam1 < 0.015: z += 187 × (0.015 − lam1)
if width < 0.0076: z += -321 × (0.0076 − width)
if e2 < 0.049: z += -48.10 × (0.049 − e2)
if lam1 < 0.0062: z += 409 × (0.0062 − lam1)
if girth < 0.140 and log_sum_pt < 6.80: z += -42.80 × (0.140 − girth) × (6.80 − log_sum_pt)
if centroid_offset < 0.038: z += 31.60 × (0.038 − centroid_offset)
if lam1 < 0.017 and centroid_offset < 0.037: z += -2220 × (0.017 − lam1) × (0.037 − centroid_offset)
if girth < 0.150 and pt_7 < 39.00: z += -0.794 × (0.150 − girth) × (39.00 − pt_7)
if sum_pt_top5 > 640 and pt_7 < 45.00: z += 0.0005 × (sum_pt_top5 − 640) × (45.00 − pt_7)
if lam2 < 0.00031 and centroid_offset < 0.041: z += -77100 × (0.00031 − lam2) × (0.041 − centroid_offset)
if tau21 < 0.530 and max_dr > 0.013: z += -13.90 × (0.530 − tau21) × (max_dr − 0.013)
if tau21 < 0.500: z += -1.34 × (0.500 − tau21)
if z_7 < 0.027: z += -160 × (0.027 − z_7)
if pt_7 < 25.00: z += -0.139 × (25.00 − pt_7)
if sum_pt_top5 > 660 and z_7 > 0.023: z += -0.559 × (sum_pt_top5 − 660) × (z_7 − 0.023)
if C2 > 0.066: z += -52.50 × (C2 − 0.066)
if sum_pt_top5 > 830 and n_pt_above_50 > 0.880: z += 0.0038 × (sum_pt_top5 − 830) × (n_pt_above_50 − 0.880)
if e2 < 0.053 and pt_dispersion > 0.400: z += 65.00 × (0.053 − e2) × (pt_dispersion − 0.400)
if sum_pt > 980 and D2 < 4.20: z += -0.011 × (sum_pt − 980) × (4.20 − D2)
if sum_pt > 1000: z += -0.023 × (sum_pt − 1000)
if sum_pt_top5 > 900 and D2 < 4.30: z += 0.010 × (sum_pt_top5 − 900) × (4.30 − D2)
if sum_pt > 990 and n_pt_above_50 > 6.00: z += 0.028 × (sum_pt − 990) × (n_pt_above_50 − 6.00)
if width < 0.0074 and m012 > 16.00: z += -12.00 × (0.0074 − width) × (m012 − 16.00)
if lam1 < 0.007 and z_dr_0p05_0p1 > 0.180: z += 277 × (0.007 − lam1) × (z_dr_0p05_0p1 − 0.180)
if sum_pt_top5 > 900 and n_pt_above_50 > 6.10: z += 0.037 × (sum_pt_top5 − 900) × (n_pt_above_50 − 6.10)
if sum_pt_top5 < 520 and pt_5 < 30.00: z += 0.0015 × (520 − sum_pt_top5) × (30.00 − pt_5)
if sum_pt_top5 > 650 and tau32 < 0.370: z += -0.040 × (sum_pt_top5 − 650) × (0.370 − tau32)
if sum_pt < 760 and z_4 < 0.037: z += 7.44 × (760 − sum_pt) × (0.037 − z_4)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth < 0.15`; 2: `lam1 < 0.015`; 3: `width < 0.0076`; 4: `e2 < 0.049`; 5: `lam1 < 0.0062`; 6: `girth < 0.14 and log_sum_pt < 6.8`; 7: `centroid_offset < 0.038`; 8: `lam1 < 0.017 and centroid_offset < 0.037`; 9: `girth < 0.15 and pt_7 < 39`; 10: `sum_pt_top5 > 640 and pt_7 < 45`; 11: `lam2 < 0.00031 and centroid_offset < 0.041`; 12: `tau21 < 0.53 and max_dr > 0.013`; 13: `tau21 < 0.5`; 14: `z_7 < 0.027`; 15: `pt_7 < 25`; 16: `sum_pt_top5 > 660 and z_7 > 0.023`; 17: `C2 > 0.066`; 18: `sum_pt_top5 > 830 and n_pt_above_50 > 0.88`; 19: `e2 < 0.053 and pt_dispersion > 0.4`; 20: `sum_pt > 980 and D2 < 4.2`; 21: `sum_pt > 1e+03`; 22: `sum_pt_top5 > 900 and D2 < 4.3`; 23: `sum_pt > 990 and n_pt_above_50 > 6`; 24: `width < 0.0074 and m012 > 16`; 25: `lam1 < 0.007 and z_dr_0p05_0p1 > 0.18`; 26: `sum_pt_top5 > 900 and n_pt_above_50 > 6.1`; 27: `sum_pt_top5 < 520 and pt_5 < 30`; 28: `sum_pt_top5 > 650 and tau32 < 0.37`; 29: `sum_pt < 760 and z_4 < 0.037`):

- `✓✓✓✓·✓✓✓✓·✓✓✓·····✓··········` **** — 26.2% of jets, neuron 3.78, formula right for 72%.  
- `✓✓✓✓✓✓✓✓✓·✓✓✓·····✓··········` **** — 19.7% of jets, neuron 5.14, formula right for 60%.  
- `✓✓✓✓✓✓✓✓✓·✓✓·················` **** — 16.5% of jets, neuron 6.83, formula right for 53%.  
- `✓✓✓✓✓✓✓✓✓✓✓····✓··✓··········` **** — 15.9% of jets, neuron 8.48, formula right for 59%.  
- `✓····✓✓····✓✓···✓············` **** — 14.1% of jets, neuron 0.43, formula right for 82%.  
- `✓✓✓✓✓·✓✓✓✓✓··✓✓··✓✓··········` **** — 6.5% of jets, neuron 7.78, formula right for 74%.  
- `✓✓✓✓✓·✓✓✓✓✓✓✓✓···✓✓✓✓✓·······` **** — 0.5% of jets, neuron 7.83, formula right for 54%.  
- `✓✓✓✓✓·✓✓··✓····✓·✓✓✓✓✓✓··✓···` **** — 0.4% of jets, neuron 7.41, formula right for 68%.  
- `✓✓✓✓✓·✓✓··✓····✓·✓✓✓✓✓✓··✓···` **** — 0.1% of jets, neuron 9.01, formula right for 66%.  

### neuron 14: Heavier, wider two-prong (Z-like) (major)

- **What it measures:** Rises in an intermediate-width window (girth2 < 0.013 and λ1 > 0.0042 push it up; girth < 0.087 and width < 0.0061 push it down) and grows with mass (+0.437) and mass/pT (+0.417). Largest for Z (1.50), then t (0.53), and low for g (0.20), W (0.18) and q (0.15).
- *computed — its value:* largest for Z (1.50), then t (0.53), then g (0.20), then W (0.18), then q (0.15); it separates Z jets from the rest best (AUC 0.77: large for Z)
- **How the class scores use it:** The Z score adds it (+6%) and the W score subtracts it (-9%): Z jets sit high and W jets low, so it separates W from Z directly. It does not enter the g, q or t scores.
- *computed — used by:* raises the score of Z (+6%); lowers the score of W (-9%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 0.032
if girth2 < 0.013: z += 487 × (0.013 − girth2)
if lam1 > 0.0042: z += 1080 × (lam1 − 0.0042)
if girth < 0.087: z += -89.10 × (0.087 − girth)
if width < 0.0061: z += -1210 × (0.0061 − width)
if lam1 > 0.0025: z += -542 × (lam1 − 0.0025)
if e2 < 0.043: z += 119 × (0.043 − e2)
if mass_over_sum_pt_sq < 0.0081: z += -443 × (0.0081 − mass_over_sum_pt_sq)
if e2_sq < 0.0058: z += 700 × (0.0058 − e2_sq)
if lam1 > 0.0025 and D2 > 0.400: z += 760 × (lam1 − 0.0025) × (D2 − 0.400)
if lam1 > 0.0042 and D2 > 0.410: z += -857 × (lam1 − 0.0042) × (D2 − 0.410)
if lam1 > 0.0061: z += -478 × (lam1 − 0.0061)
if C2 < 0.067: z += -24.20 × (0.067 − C2)
if max_dr < 0.180: z += -12.50 × (0.180 − max_dr)
if girth2 < 0.013 and n_dr_0p1_0p2 < 3.00: z += -45.70 × (0.013 − girth2) × (3.00 − n_dr_0p1_0p2)
if width < 0.0077 and n_dr_0p1_0p2 < 3.00: z += 87.00 × (0.0077 − width) × (3.00 − n_dr_0p1_0p2)
if z_dr_0p05_0p1 < 0.580 and C2 < 0.068: z += -44.30 × (0.580 − z_dr_0p05_0p1) × (0.068 − C2)
if girth2 < 0.013 and eccentricity > 0.970: z += 11300 × (0.013 − girth2) × (eccentricity − 0.970)
if girth2 < 0.0043 and n_dr_0p2_0p4 < 1.10: z += -384 × (0.0043 − girth2) × (1.10 − n_dr_0p2_0p4)
if girth < 0.034: z += -93.40 × (0.034 − girth)
if z_dr_0p05_0p1 < 0.600: z += 1.38 × (0.600 − z_dr_0p05_0p1)
if width < 0.0076 and D2 < 1.00: z += -1950 × (0.0076 − width) × (1.00 − D2)
if width < 0.0075 and planar_flow < 0.110: z += -6520 × (0.0075 − width) × (0.110 − planar_flow)
if planar_flow < 0.110 and centroid_offset > 0.0094: z += 1340 × (0.110 − planar_flow) × (centroid_offset − 0.0094)
if n_dr_0p05_0p1 < 4.80: z += -0.122 × (4.80 − n_dr_0p05_0p1)
if z_dr_0p05_0p1 < 0.600 and n_dr_0p1_0p2 < 3.00: z += 0.317 × (0.600 − z_dr_0p05_0p1) × (3.00 − n_dr_0p1_0p2)
if planar_flow < 0.110 and centroid_offset > 0.018: z += -1670 × (0.110 − planar_flow) × (centroid_offset − 0.018)
if centroid_offset > 0.050: z += -296 × (centroid_offset − 0.050)
if D2 < 0.800: z += -2.01 × (0.800 − D2)
if e2 < 0.041 and D2 < 0.990: z += 304 × (0.041 − e2) × (0.990 − D2)
if planar_flow < 0.110 and max_dr < 0.160: z += -202 × (0.110 − planar_flow) × (0.160 − max_dr)
if centroid_offset > 0.031: z += -81.40 × (centroid_offset − 0.031)
if D2 < 1.20 and centroid_offset < 0.030: z += 41.50 × (1.20 − D2) × (0.030 − centroid_offset)
if tau21 < 0.140: z += 9.90 × (0.140 − tau21)
if lam1 > 0.0054 and max_dr < 0.160: z += 9530 × (lam1 − 0.0054) × (0.160 − max_dr)
if lam1 > 0.0025 and D2 > 1.60: z += -503 × (lam1 − 0.0025) × (D2 − 1.60)
if planar_flow < 0.110 and sum_pt < 750: z += -0.048 × (0.110 − planar_flow) × (750 − sum_pt)
if girth2 < 0.013 and mass_top3 > 24.00: z += 5.76 × (0.013 − girth2) × (mass_top3 − 24.00)
if sum_pt_top3 < 310: z += -0.0077 × (310 − sum_pt_top3)
if max_dr < 0.078: z += 6.00 × (0.078 − max_dr)
if z_dr_0p05_0p1 > 0.740 and n_dr_0p2_0p4 < 1.00: z += 2.71 × (z_dr_0p05_0p1 − 0.740) × (1.00 − n_dr_0p2_0p4)
if width < 0.0074 and mass_top3 > 24.00: z += -18.50 × (0.0074 − width) × (mass_top3 − 24.00)
if width < 0.006 and mean_phi < -0.026: z += 35800 × (0.006 − width) × (-0.026 − mean_phi)
if width < 0.006 and mean_eta < -0.027: z += 35400 × (0.006 − width) × (-0.027 − mean_eta)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.013`; 2: `lam1 > 0.0042`; 3: `girth < 0.087`; 4: `width < 0.0061`; 5: `lam1 > 0.0025`; 6: `e2 < 0.043`; 7: `mass_over_sum_pt_sq < 0.0081`; 8: `e2_sq < 0.0058`; 9: `lam1 > 0.0025 and D2 > 0.4`; 10: `lam1 > 0.0042 and D2 > 0.41`; 11: `lam1 > 0.0061`; 12: `C2 < 0.067`; 13: `max_dr < 0.18`; 14: `girth2 < 0.013 and n_dr_0p1_0p2 < 3`; 15: `width < 0.0077 and n_dr_0p1_0p2 < 3`; 16: `z_dr_0p05_0p1 < 0.58 and C2 < 0.068`; 17: `girth2 < 0.013 and eccentricity > 0.97`; 18: `girth2 < 0.0043 and n_dr_0p2_0p4 < 1.1`; 19: `girth < 0.034`; 20: `z_dr_0p05_0p1 < 0.6`; 21: `width < 0.0076 and D2 < 1`; 22: `width < 0.0075 and planar_flow < 0.11`; 23: `planar_flow < 0.11 and centroid_offset > 0.0094`; 24: `n_dr_0p05_0p1 < 4.8`; 25: `z_dr_0p05_0p1 < 0.6 and n_dr_0p1_0p2 < 3`; 26: `planar_flow < 0.11 and centroid_offset > 0.018`; 27: `centroid_offset > 0.05`; 28: `D2 < 0.8`; 29: `e2 < 0.041 and D2 < 0.99`; 30: `planar_flow < 0.11 and max_dr < 0.16`; 31: `centroid_offset > 0.031`; 32: `D2 < 1.2 and centroid_offset < 0.03`; 33: `tau21 < 0.14`; 34: `lam1 > 0.0054 and max_dr < 0.16`; 35: `lam1 > 0.0025 and D2 > 1.6`; 36: `planar_flow < 0.11 and sum_pt < 750`; 37: `girth2 < 0.013 and mass_top3 > 24`; 38: `sum_pt_top3 < 310`; 39: `max_dr < 0.078`; 40: `z_dr_0p05_0p1 > 0.74 and n_dr_0p2_0p4 < 1`; 41: `width < 0.0074 and mass_top3 > 24`; 42: `width < 0.006 and mean_phi < -0.026`; 43: `width < 0.006 and mean_eta < -0.027`):

- `✓·✓✓·✓✓✓···✓✓✓✓✓·✓✓✓···✓✓·············✓····` **** — 32.2% of jets, neuron 0.00, formula right for 61%.  
- `✓✓✓✓✓✓✓✓✓✓·✓✓✓✓·✓··✓✓✓·✓···✓✓✓·✓✓··········` **** — 21.0% of jets, neuron 0.71, formula right for 69%.  
- `✓·✓✓✓✓✓✓✓··✓✓✓✓✓✓✓·✓·✓·✓✓··················` **** — 16.0% of jets, neuron 0.25, formula right for 52%.  
- `✓✓✓·✓✓✓·✓✓✓✓✓✓··✓··········✓·✓·✓✓✓··✓······` **** — 14.0% of jets, neuron 1.90, formula right for 73%.  
- `·✓··✓·····✓✓···✓···✓··✓✓···✓···✓✓··✓·······` **** — 4.4% of jets, neuron 0.10, formula right for 77%.  
- `·✓··✓···✓✓✓········✓···✓·············✓·····` **** — 4.0% of jets, neuron 0.57, formula right for 90%.  
- `·✓··✓···✓✓✓········✓···✓······✓············` **** — 3.8% of jets, neuron 0.59, formula right for 70%.  
- `·✓··✓···✓✓✓✓···✓···✓··✓✓·✓·✓··✓·✓··✓·✓·····` **** — 1.9% of jets, neuron 0.23, formula right for 72%.  
- `·✓··✓···✓✓✓········✓···✓······✓······✓·····` **** — 1.4% of jets, neuron 0.44, formula right for 83%.  
- `·✓··✓···✓✓✓········✓···✓······✓···✓········` **** — 1.4% of jets, neuron 0.08, formula right for 84%.  

### neuron 0: Elongated two-prong massive jet (moderate)

- **What it measures:** Rises for jets that are compact but not the very narrowest (girth2 < 0.013 pushes it up, girth < 0.078 down) and is pushed down for light jets (mass < 59, < 30 and < 22 GeV); overall it follows an elongated two-prong shape (eccentricity +0.591, planar flow -0.591, τ21 -0.571). Largest for Z (2.15) and W (2.03), low for t (0.60), g (0.29) and q (0.22).
- *computed — its value:* largest for Z (2.15), then W (2.03), then t (0.60), then g (0.29), then q (0.22); it separates Z jets from the rest best (AUC 0.75: large for Z)
- **How the class scores use it:** The W score adds it (+8%) and the g score subtracts it (-6%): a high value marks a massive two-prong jet, which argues for a W and against a gluon. It does not enter the q, Z or t scores, even though Z jets sit highest on it.
- *computed — used by:* raises the score of W (+8%); lowers the score of g (-6%); does not (or hardly) enter the score of q, Z, t (share of each class score’s average input)

```
z = -0.511
if girth2 < 0.013: z += 299 × (0.013 − girth2)
if girth < 0.078: z += -75.60 × (0.078 − girth)
if width < 0.0089: z += 330 × (0.0089 − width)
if width < 0.0044: z += -815 × (0.0044 − width)
if mass < 59.00: z += -0.051 × (59.00 − mass)
if mass < 22.00: z += -0.252 × (22.00 − mass)
if lam1 < 0.0006: z += 9390 × (0.0006 − lam1)
if mass < 30.00: z += -0.132 × (30.00 − mass)
if lam1 < 0.0015: z += -1870 × (0.0015 − lam1)
if z_dr_0_0p05 > 0.850: z += 11.50 × (z_dr_0_0p05 − 0.850)
if girth2_top5 < 0.0085: z += -127 × (0.0085 − girth2_top5)
if centroid_offset < 0.033: z += 30.50 × (0.033 − centroid_offset)
if mass < 30.00 and phi_1 > -0.056: z += -1.13 × (30.00 − mass) × (phi_1 − -0.056)
if girth2 < 0.019 and eccentricity > 0.960: z += 2570 × (0.019 − girth2) × (eccentricity − 0.960)
if mass_over_sum_pt_sq < 0.0081 and n_pt_above_50 < 7.90: z += 37.60 × (0.0081 − mass_over_sum_pt_sq) × (7.90 − n_pt_above_50)
if sum_pt > 810: z += -0.013 × (sum_pt − 810)
if mass < 64.00 and pt_7 < 40.00: z += -0.0017 × (64.00 − mass) × (40.00 − pt_7)
if sum_pt_top5 > 700: z += 0.011 × (sum_pt_top5 − 700)
if tau32 > 0.440: z += -1.89 × (tau32 − 0.440)
if sum_pt > 900: z += -0.025 × (sum_pt − 900)
if n_dr_0_0p05 > 3.80: z += 0.172 × (n_dr_0_0p05 − 3.80)
if mass < 63.00 and centroid_offset > 0.012: z += 1.83 × (63.00 − mass) × (centroid_offset − 0.012)
if planar_flow < 0.140 and centroid_offset < 0.051: z += 135 × (0.140 − planar_flow) × (0.051 − centroid_offset)
if sum_pt > 900 and pt_7 < 26.00: z += 0.0024 × (sum_pt − 900) × (26.00 − pt_7)
if lam1 < 0.0065 and D2 < 0.880: z += -1970 × (0.0065 − lam1) × (0.880 − D2)
if mass < 56.00 and C2 > 0.024: z += 1.57 × (56.00 − mass) × (C2 − 0.024)
if planar_flow < 0.150 and sum_pt_top2 < 370: z += -0.038 × (0.150 − planar_flow) × (370 − sum_pt_top2)
if sum_pt > 900 and pt_7 > 26.00: z += -0.0009 × (sum_pt − 900) × (pt_7 − 26.00)
if D2 > 3.90: z += -0.707 × (D2 − 3.90)
if planar_flow < 0.180 and z_top5 < 0.820: z += 43.50 × (0.180 − planar_flow) × (0.820 − z_top5)
if girth2 < 0.019 and mass_top2 > 29.00: z += -8.40 × (0.019 − girth2) × (mass_top2 − 29.00)
if planar_flow < 0.013: z += 81.10 × (0.013 − planar_flow)
if girth < 0.087 and m01 > 29.00: z += 7.56 × (0.087 − girth) × (m01 − 29.00)
if lam1 < 0.0053 and mass_top3 > 15.00: z += -29.10 × (0.0053 − lam1) × (mass_top3 − 15.00)
if mass < 29.00 and D2 < 0.870: z += -1.28 × (29.00 − mass) × (0.870 − D2)
if planar_flow < 0.150 and dr_2 < 0.028: z += -380 × (0.150 − planar_flow) × (0.028 − dr_2)
if D2 > 3.90 and phi_2 < -0.010: z += -126 × (D2 − 3.90) × (-0.010 − phi_2)
if mass < 30.00 and dr_7 > 0.130: z += -4.44 × (30.00 − mass) × (dr_7 − 0.130)
if girth2_top3 < 0.0039 and m01 > 29.00: z += 632 × (0.0039 − girth2_top3) × (m01 − 29.00)
if z_dr_0p05_0p1 > 0.840 and dr_7 < 0.0073: z += -121000 × (z_dr_0p05_0p1 − 0.840) × (0.0073 − dr_7)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.013`; 2: `girth < 0.078`; 3: `width < 0.0089`; 4: `width < 0.0044`; 5: `mass < 59`; 6: `mass < 22`; 7: `lam1 < 0.0006`; 8: `mass < 30`; 9: `lam1 < 0.0015`; 10: `z_dr_0_0p05 > 0.85`; 11: `girth2_top5 < 0.0085`; 12: `centroid_offset < 0.033`; 13: `mass < 30 and phi_1 > -0.056`; 14: `girth2 < 0.019 and eccentricity > 0.96`; 15: `mass_over_sum_pt_sq < 0.0081 and n_pt_above_50 < 7.9`; 16: `sum_pt > 810`; 17: `mass < 64 and pt_7 < 40`; 18: `sum_pt_top5 > 700`; 19: `tau32 > 0.44`; 20: `sum_pt > 900`; 21: `n_dr_0_0p05 > 3.8`; 22: `mass < 63 and centroid_offset > 0.012`; 23: `planar_flow < 0.14 and centroid_offset < 0.051`; 24: `sum_pt > 900 and pt_7 < 26`; 25: `lam1 < 0.0065 and D2 < 0.88`; 26: `mass < 56 and C2 > 0.024`; 27: `planar_flow < 0.15 and sum_pt_top2 < 370`; 28: `sum_pt > 900 and pt_7 > 26`; 29: `D2 > 3.9`; 30: `planar_flow < 0.18 and z_top5 < 0.82`; 31: `girth2 < 0.019 and mass_top2 > 29`; 32: `planar_flow < 0.013`; 33: `girth < 0.087 and m01 > 29`; 34: `lam1 < 0.0053 and mass_top3 > 15`; 35: `mass < 29 and D2 < 0.87`; 36: `planar_flow < 0.15 and dr_2 < 0.028`; 37: `D2 > 3.9 and phi_2 < -0.01`; 38: `mass < 30 and dr_7 > 0.13`; 39: `girth2_top3 < 0.0039 and m01 > 29`; 40: `z_dr_0p05_0p1 > 0.84 and dr_7 < 0.0073`):

- `✓✓✓·✓·····✓✓·✓✓···✓···✓·················` **Two-prong W/Z boson jets** — 28.3% of jets, neuron 2.72, formula right for 72%. The largest group (28%), a W/Z mixture (Z 42%, W 38%, some t) with mass 54.5 GeV, well above the 40 GeV average, normal width and pT, and most pT sitting 0.05-0.1 from the axis, i.e. in two separated prongs. Almost every jet passes girth2 < 0.013 (+2.015) and width < 0.0089 (+0.871), and most pass girth2 < 0.019 and eccentricity > 0.96 and centroid_offset < 0.033, while the light-mass penalties (mass < 30, width < 0.0044) almost never fire; only girth < 0.078 and mass < 59 take a little back. The neuron sits at its highest value (2.718), which raises the W score and lowers the g score; the formula splits them between W and Z and is right 0.716 of the time, the remaining errors being mostly W-Z swaps.
- `···········✓····························` **Wide massive top-like jets** — 19.8% of jets, neuron 0.33, formula right for 77%. Mostly top jets (74%, plus some gluons) with mass 73.5 GeV, three times the average width and a softer leading particle; 60% of the pT lies beyond 0.1 from the axis, so the radiation is spread out. These jets are too wide to pass width < 0.0089, girth < 0.078 or (mostly) girth2 < 0.013, so the big positive terms are lost; what remains is small pluses such as centroid_offset < 0.033 and mass < 63 and centroid_offset > 0.012 against minuses such as tau32 > 0.44 and planar_flow < 0.15 and sum_pt_top2 < 370. The neuron is only weakly on (0.332, on for 0.372 of jets), so it barely touches the scores; the formula calls them t and is right 0.772 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓·✓·✓·✓·✓···················` **Very light pencil-thin quark/gluon jets** — 16.3% of jets, neuron 0.00, formula right for 62%. Light-quark and gluon jets (q 47%, g 38%) with almost no mass (6.7 GeV) and essentially all pT within 0.05 of the axis. Every compactness and light-mass test passes: the pluses girth2 < 0.013, lam1 < 0.0006 and width < 0.0089 are outweighed by the minuses girth < 0.078 (-5.124), mass < 22, width < 0.0044 and mass < 30, so the sum is negative and the neuron is off for all of them and adds nothing to any score. The formula splits them between q and g and is right only 0.615 of the time: the quark-gluon confusion is decided elsewhere.
- `✓✓✓✓✓····✓✓✓·✓✓·✓·✓·✓✓✓··✓··············` **Compact medium-mass mixed jets** — 13.7% of jets, neuron 1.37, formula right for 53%. A mixture (W 34%, Z 23%, g 19%, q 14%) of jets at 36.9 GeV, a bit below average mass, narrow (78% of pT within 0.05) but not pencil-thin. The large terms nearly cancel: girth2 < 0.013 (+2.926) and width < 0.0089 against girth < 0.078 (-2.519), mass < 59 and, for most jets, width < 0.0044; what tips it positive are medium-mass tests such as mass < 63 and centroid_offset > 0.012, mass < 56 and C2 > 0.024 and n_dr_0_0p05 > 3.8, which pass far more often here than in other groups. The neuron is on for 0.66 of jets (mean 1.368), raising W and lowering g; the formula calls them W but is right only 0.531 of the time, a poorly separated group.
- `✓✓✓✓✓✓·✓✓✓✓✓✓·✓·✓·✓·✓···················` **Light narrow gluon/quark jets** — 7.4% of jets, neuron 0.00, formula right for 55%. Gluon and light-quark jets (g 42%, q 36%, a few W/Z) of 17.7 GeV mass, narrow with 94% of pT within 0.05 of the axis, at average pT. As for the lightest group, the compactness pluses (girth2 < 0.013, width < 0.0089) are beaten by girth < 0.078, width < 0.0044, mass < 59, mass < 30 and lam1 < 0.0015, all of which almost always pass, so the neuron is off and contributes nothing. The formula calls them g and is right only 0.55 of the time, so these are often mistaken quarks (or light bosons).
- `✓✓✓✓✓✓·✓✓✓✓✓✓✓✓·✓·✓·✓✓··················` **Near-massless but spread-out jets** — 5.5% of jets, neuron 0.01, formula right for 46%. A real mixture (g 35%, Z 23%, W 21%, q 13%) with very low mass (6.9 GeV), a softer leading particle (192 GeV) and more pT at 0.05-0.1 than the pencil-thin groups. All three light-mass penalties mass < 22, mass < 30 and mass < 59 pass (together about -9.5) along with girth < 0.078 and width < 0.0044; mass < 63 and centroid_offset > 0.012 almost always passes (+2.083) but cannot compensate, so the neuron is essentially off. The formula calls them g but is right only 0.457 of the time, one of the worst groups here: bosons whose reconstructed mass came out tiny get lost.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓·✓✓✓✓✓✓✓··✓················` **High-pT pencil-like quark jets** — 4.8% of jets, neuron 0.00, formula right for 72%. Mostly light-quark jets (66%) with high total pT (1003 GeV vs 716 average), a leading particle carrying 458 GeV and almost no mass or width. Beyond the usual narrow-jet cancellation (girth < 0.078 -5.396 vs lam1 < 0.0006 +4.914), the high-pT tests sum_pt > 900 and sum_pt > 810 subtract about 5 while sum_pt_top5 > 700 adds back only 2.243, so the neuron is off. The formula calls them q and is right 0.724 of the time.
- `✓✓✓✓·····✓✓✓·✓✓✓·✓✓✓✓·✓✓················` **High-pT boosted W/Z jets** — 2.8% of jets, neuron 1.51, formula right for 67%. Boosted bosons (W 40%, Z 35%) at very high total pT (1006 GeV), mass 62.2 GeV and a hard leading particle (489 GeV), still fairly compact. The high-pT penalties sum_pt > 900 and sum_pt > 810 (about -5) are offset by sum_pt_top5 > 700 and, for 0.65 of jets, sum_pt > 900 and pt_7 < 26 (+1.208), while girth2 < 0.013 and width < 0.0089 give the usual boost. The neuron is on for about half (mean 1.507), raising W and lowering g; the formula calls them W and is right 0.673 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓·✓✓✓✓✓✓✓··✓·✓··✓···········` **One-particle-dominated high-pT quark jets** — 0.8% of jets, neuron 0.11, formula right for 76%. A tiny group (0.8%), mostly light quarks (77%) at high pT (1081 GeV) where the leading particle carries 624 GeV and the 8th only 7.5 GeV. sum_pt > 900 and pt_7 < 26 adds a huge +7.403 but is cancelled by D2 > 3.9 (-4.699), sum_pt > 900, sum_pt > 810 and girth < 0.078, so the neuron is almost always off (on for 0.036). The formula calls them q and is right 0.755 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓✓✓··✓·✓✓✓✓······✓············` **Very high-pT many-particle gluon jets** — 0.4% of jets, neuron 0.00, formula right for 68%. The smallest group (0.4%), mostly gluons (70%) at the highest pT (1308 GeV) with all eight particles hard (8th at 58.7 GeV), light and narrow. sum_pt > 900 and pt_7 > 26 (-11.108), sum_pt > 900 (-10.29) and sum_pt > 810 dwarf everything else, so the neuron is off. The formula calls them g and is right 0.683 of the time.

### neuron 5: Quark-likeness: pT in few particles (moderate)

- **What it measures:** Rises when particle 7 (the 8th hardest) is soft (pT_7 < 53 GeV) and the two hardest particles carry much of the pT (their sum < 540 GeV pushes it down), for narrow, centred, low-e2 jets (e2 < 0.034 pushes it up); overall it falls with e2 (-0.683) and mass/pT (-0.633). Largest for q (4.65), well above W (1.68), Z (1.64) and g (1.57), and lowest for t (0.50).
- *computed — its value:* largest for q (4.65), then W (1.68), then Z (1.64), then g (1.57), then t (0.50); it separates q jets from the rest best (AUC 0.78: large for q)
- **How the class scores use it:** The g (-13%) and t (-11%) scores subtract it and the q score adds a little (+4%): a high value is quark-like, which argues against a gluon and against a top (tops sit lowest). It does not enter the W or Z scores.
- *computed — used by:* raises the score of q (+4%); lowers the score of g (-13%), t (-11%); does not (or hardly) enter the score of W, Z (share of each class score’s average input)

```
z = 0.107
if pt_7 < 53.00: z += 0.074 × (53.00 − pt_7)
if sum_pt_top2 < 540: z += -0.0066 × (540 − sum_pt_top2)
if z_7 < 0.071 and centroid_offset < 0.031: z += -2300 × (0.071 − z_7) × (0.031 − centroid_offset)
if width < 0.0026 and centroid_offset < 0.025: z += 69700 × (0.0026 − width) × (0.025 − centroid_offset)
if dr_0 < 0.023: z += -216 × (0.023 − dr_0)
if e2 < 0.034: z += 65.70 × (0.034 − e2)
if mean_phi2 < 0.015 and max_pair_mass < 41.00: z += 1.83 × (0.015 − mean_phi2) × (41.00 − max_pair_mass)
if log_sum_pt > 6.60 and n_dr_0p2_0p4 < 0.990: z += -10.60 × (log_sum_pt − 6.60) × (0.990 − n_dr_0p2_0p4)
if log_sum_pt > 6.60: z += 7.85 × (log_sum_pt − 6.60)
if mass < 57.00 and n_dr_0p2_0p4 < 2.00: z += 0.012 × (57.00 − mass) × (2.00 − n_dr_0p2_0p4)
if log_sum_pt > 6.60 and dr_0 < 0.021: z += 792 × (log_sum_pt − 6.60) × (0.021 − dr_0)
if log_sum_pt > 6.80: z += -32.70 × (log_sum_pt − 6.80)
if z_7 < 0.070 and n_dr_0p2_0p4 < 1.00: z += 25.80 × (0.070 − z_7) × (1.00 − n_dr_0p2_0p4)
if log_sum_pt > 6.30 and centroid_offset > 0.00063: z += 137 × (log_sum_pt − 6.30) × (centroid_offset − 0.00063)
if sum_pt_top2 < 570 and girth2_top3 < 0.0036: z += -1.43 × (570 − sum_pt_top2) × (0.0036 − girth2_top3)
if z_7 < 0.073 and sum_pt < 790: z += -0.289 × (0.073 − z_7) × (790 − sum_pt)
if sum_pt > 870 and centroid_offset < 0.013: z += 1.93 × (sum_pt − 870) × (0.013 − centroid_offset)
if LHA < 0.220 and log_sum_pt < 6.80: z += -62.50 × (0.220 − LHA) × (6.80 − log_sum_pt)
if z_7 < 0.024: z += 248 × (0.024 − z_7)
if log_sum_pt > 6.90 and dr_0 < 0.043: z += -1630 × (log_sum_pt − 6.90) × (0.043 − dr_0)
if sum_pt_top2 < 550 and dr_0 < 0.022: z += 0.401 × (550 − sum_pt_top2) × (0.022 − dr_0)
if log_sum_pt > 6.60 and mean_phi2 < 0.00014: z += 29200 × (log_sum_pt − 6.60) × (0.00014 − mean_phi2)
if LHA < 0.210 and centroid_offset > 0.0028: z += -920 × (0.210 − LHA) × (centroid_offset − 0.0028)
if sum_pt_top5 > 730 and D2 < 1.60: z += -0.012 × (sum_pt_top5 − 730) × (1.60 − D2)
if sum_pt > 870: z += -0.0037 × (sum_pt − 870)
if girth2 < 5.2e-05: z += 55900 × (5.2e-05 − girth2)
if log_sum_pt > 6.60 and centroid_offset > 0.017: z += -799 × (log_sum_pt − 6.60) × (centroid_offset − 0.017)
if LHA < 0.150 and centroid_offset > 0.0034: z += -3370 × (0.150 − LHA) × (centroid_offset − 0.0034)
if mass_over_sum_pt < 0.081 and mass_top3 > 29.00: z += 6.77 × (0.081 − mass_over_sum_pt) × (mass_top3 − 29.00)
if log_sum_pt > 6.90 and pt_5 > 48.00: z += 0.534 × (log_sum_pt − 6.90) × (pt_5 − 48.00)
if LHA < 0.220 and n_dr_0p2_0p4 > -1.6e-05: z += -14.70 × (0.220 − LHA) × (n_dr_0p2_0p4 − -1.6e-05)
if LHA < 0.210 and mass_top3 > 3.50: z += -1.74 × (0.210 − LHA) × (mass_top3 − 3.50)
if LHA < 0.210 and planar_flow < 0.083: z += 397 × (0.210 − LHA) × (0.083 − planar_flow)
if log_sum_pt > 6.90 and dr_4 > 0.039: z += 201 × (log_sum_pt − 6.90) × (dr_4 − 0.039)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `pt_7 < 53`; 2: `sum_pt_top2 < 540`; 3: `z_7 < 0.071 and centroid_offset < 0.031`; 4: `width < 0.0026 and centroid_offset < 0.025`; 5: `dr_0 < 0.023`; 6: `e2 < 0.034`; 7: `mean_phi2 < 0.015 and max_pair_mass < 41`; 8: `log_sum_pt > 6.6 and n_dr_0p2_0p4 < 0.99`; 9: `log_sum_pt > 6.6`; 10: `mass < 57 and n_dr_0p2_0p4 < 2`; 11: `log_sum_pt > 6.6 and dr_0 < 0.021`; 12: `log_sum_pt > 6.8`; 13: `z_7 < 0.07 and n_dr_0p2_0p4 < 1`; 14: `log_sum_pt > 6.3 and centroid_offset > 0.00063`; 15: `sum_pt_top2 < 570 and girth2_top3 < 0.0036`; 16: `z_7 < 0.073 and sum_pt < 790`; 17: `sum_pt > 870 and centroid_offset < 0.013`; 18: `LHA < 0.22 and log_sum_pt < 6.8`; 19: `z_7 < 0.024`; 20: `log_sum_pt > 6.9 and dr_0 < 0.043`; 21: `sum_pt_top2 < 550 and dr_0 < 0.022`; 22: `log_sum_pt > 6.6 and mean_phi2 < 0.00014`; 23: `LHA < 0.21 and centroid_offset > 0.0028`; 24: `sum_pt_top5 > 730 and D2 < 1.6`; 25: `sum_pt > 870`; 26: `girth2 < 5.2e-05`; 27: `log_sum_pt > 6.6 and centroid_offset > 0.017`; 28: `LHA < 0.15 and centroid_offset > 0.0034`; 29: `mass_over_sum_pt < 0.081 and mass_top3 > 29`; 30: `log_sum_pt > 6.9 and pt_5 > 48`; 31: `LHA < 0.22 and n_dr_0p2_0p4 > -1.6e-05`; 32: `LHA < 0.21 and mass_top3 > 3.5`; 33: `LHA < 0.21 and planar_flow < 0.083`; 34: `log_sum_pt > 6.9 and dr_4 > 0.039`):

- `✓✓····✓··✓···✓····················` **Soft-leading wide massive mixed jets** — 26.6% of jets, neuron 0.17, formula right for 69%. A top-led mixture (t 38%, Z 21%, W 20%, g 16%) at 55.8 GeV, about twice the average width, low total pT (578 GeV) shared evenly (leading particle only 136 GeV, 8th 42.0 GeV). sum_pt_top2 < 540 (-2.008) passes for all, and the small pluses pt_7 < 53 and mean_phi2 < 0.015 and max_pair_mass < 41 cannot beat it, while e2 < 0.034 mostly fails. The neuron is mostly off (on for 0.24, mean 0.17), so it barely touches the scores; the formula calls them t but is right 0.692 of the time.
- `✓✓✓···✓··✓··✓✓·✓··················` **Wide top-led jets, soft 8th particle** — 19.4% of jets, neuron 0.87, formula right for 69%. A top-led mixture (t 40%, Z 23%, W 20%) at 59.1 GeV, wider than average, with a harder leading particle (216 GeV) and a soft 8th particle. pt_7 < 53 (+1.639) always passes and outweighs sum_pt_top2 < 540, but z_7 < 0.073 and sum_pt < 790 (-0.906, far more common here) and z_7 < 0.071 and centroid_offset < 0.031 pull back. The neuron is on for about half (0.866), slightly lowering the t and g scores; the formula calls them t and is right 0.692 of the time.
- `✓✓✓··✓✓✓✓···✓✓····················` **High-pT two-prong W/Z jets** — 15.2% of jets, neuron 2.66, formula right for 71%. A W/Z mixture (W 39%, Z 38%) at 54.4 GeV, of high total pT (855 GeV) with a hard leading particle (352 GeV), fairly narrow. Being high-pT they pass pt_7 < 53, log_sum_pt > 6.6 and log_sum_pt > 6.3 and centroid_offset > 0.00063 and often escape sum_pt_top2 < 540, against z_7 < 0.071 and centroid_offset < 0.031 (-1.582) and log_sum_pt > 6.6 and n_dr_0p2_0p4 < 0.99. The neuron is fairly high (2.66), raising the q score and lowering g and t; the formula calls them W and is right 0.707 of the time.
- `✓✓✓✓·✓✓··✓··✓✓✓✓·✓····✓·······✓···` **Light narrow gluon-led mixture** — 12.7% of jets, neuron 2.03, formula right for 49%. A gluon-led mixture (g 39%, q 20%, W 18%, Z 16%), light (14.8 GeV), narrow (90% of pT within 0.05), with a soft leading particle (179 GeV). Pluses e2 < 0.034, pt_7 < 53, mass < 57 and n_dr_0p2_0p4 < 2 and mean_phi2 < 0.015 and max_pair_mass < 41 beat sum_pt_top2 < 540, sum_pt_top2 < 570 and girth2_top3 < 0.0036 and LHA < 0.22 and log_sum_pt < 6.8. The neuron is on (2.03), raising q and lowering g and t; the formula calls them g but is right only 0.486 of the time, the worst of this neuron's groups.
- `✓✓✓✓✓✓✓··✓··✓✓✓✓·✓··✓·✓····✓··✓···` **Pencil-thin soft-leading gluon jets** — 9.0% of jets, neuron 1.28, formula right for 59%. Mostly gluons (53%, q 35%), nearly massless (8.5 GeV), 98% of pT within 0.05, with pT spread over many particles (leading 182 GeV, 8th 40.7 GeV). width < 0.0026 and centroid_offset < 0.025 (+2.992), e2 < 0.034 and sum_pt_top2 < 550 and dr_0 < 0.022 add, but dr_0 < 0.023 (-2.908), LHA < 0.22 and log_sum_pt < 6.8, sum_pt_top2 < 540 and sum_pt_top2 < 570 and girth2_top3 < 0.0036 subtract. The neuron is moderate (1.278, on for 0.666); the formula calls them g and is right 0.587 of the time.
- `✓✓✓✓✓✓✓✓✓✓✓·✓✓✓·✓✓··✓✓✓·✓··✓··✓···` **Narrow harder quark jets** — 8.4% of jets, neuron 6.18, formula right for 65%. Mostly light quarks (61%, g 23%), nearly massless (8.6 GeV), extremely narrow, of above-average pT (876 GeV) with a hard leading particle (330 GeV). width < 0.0026 and centroid_offset < 0.025 (+3.444), e2 < 0.034, log_sum_pt > 6.6 and dr_0 < 0.021 (common only here and in the high-pT groups) and pt_7 < 53 beat dr_0 < 0.023 (-3.449), z_7 < 0.071 and centroid_offset < 0.031 and log_sum_pt > 6.6 and n_dr_0p2_0p4 < 0.99. The neuron is high (6.181), raising q and lowering g and t; the formula calls them q and is right 0.652 of the time.
- `✓·✓✓✓✓✓✓✓✓✓✓✓✓··✓·✓··✓··✓·····✓···` **High-pT one-particle quark jets** — 4.6% of jets, neuron 9.18, formula right for 77%. Mostly light quarks (75%), nearly massless, of high pT (980 GeV) with the leading particle carrying 468 GeV and a soft 8th particle. Large pluses width < 0.0026 and centroid_offset < 0.025, log_sum_pt > 6.6 and dr_0 < 0.021, pt_7 < 53 and sum_pt > 870 and centroid_offset < 0.013 outweigh dr_0 < 0.023, z_7 < 0.071 and centroid_offset < 0.031, log_sum_pt > 6.6 and n_dr_0p2_0p4 < 0.99 and log_sum_pt > 6.8. This is the neuron's highest value (9.184), strongly raising q and lowering g and t; the formula calls them q and is right 0.77 of the time.
- `✓·✓··✓✓✓✓··✓✓✓··✓······✓✓·········` **Very high-pT W/Z jets** — 2.6% of jets, neuron 1.04, formula right for 67%. A W/Z mixture (W 35%, Z 34%, g 19%) at 62.2 GeV and very high pT (1015 GeV), leading particle 465 GeV. log_sum_pt > 6.8 (-3.932) always passes, joined by log_sum_pt > 6.6 and n_dr_0p2_0p4 < 0.99, z_7 < 0.071 and centroid_offset < 0.031 and sum_pt_top5 > 730 and D2 < 1.6, outweighing log_sum_pt > 6.6, pt_7 < 53 and sum_pt > 870 and centroid_offset < 0.013. The neuron is usually zero (on for 0.385, mean 1.037); the formula calls them W and is right 0.672 of the time.
- `✓·✓✓✓✓✓✓✓✓✓✓✓✓··✓··✓·✓··✓·····✓···` **Very high-pT light quark/gluon jets** — 1.2% of jets, neuron 2.29, formula right for 67%. Quarks (46%) and gluons (41%) in nearly equal parts, light (14.3 GeV), very narrow, at very high pT (1134 GeV) with a 505 GeV leading particle. The very-high-pT penalties log_sum_pt > 6.8 (-7.588) and log_sum_pt > 6.9 and dr_0 < 0.043 (-7.333), plus log_sum_pt > 6.6 and n_dr_0p2_0p4 < 0.99 and dr_0 < 0.023, are mostly offset by log_sum_pt > 6.6 and dr_0 < 0.021, sum_pt > 870 and centroid_offset < 0.013 and width < 0.0026 and centroid_offset < 0.025. The neuron is on for 0.567 (2.295); the formula divides them almost evenly between g and q and is right 0.669 of the time.
- `✓·✓✓✓✓✓✓✓✓✓✓✓✓··✓··✓·✓··✓····✓✓···` **Highest-pT gluon-rich jets** — 0.3% of jets, neuron 0.04, formula right for 66%. A tiny group (0.3%), mostly gluons (59%, q 30%), at the highest pT (1391 GeV) with a 673 GeV leading particle, light and very narrow. log_sum_pt > 6.9 and dr_0 < 0.043 (-19.634) and log_sum_pt > 6.8 (-14.112) outweigh sum_pt > 870 and centroid_offset < 0.013 and log_sum_pt > 6.6 and dr_0 < 0.021, so the neuron is off (on for 0.029). The formula calls them g and is right 0.659 of the time.

### neuron 6: Broad jet with off-centre pT (moderate)

- **What it measures:** Rises for broad jets (compact ones are cut off by girth2 < 0.0086 and width < 0.013) and grows with the offset of the pT centroid from the axis (+0.492), falling at high total pT (-0.376). Largest for t (3.80), then g (1.86), q (0.92), Z (0.56) and W (0.23).
- *computed — its value:* largest for t (3.80), then g (1.86), then q (0.92), then Z (0.56), then W (0.23); it separates t jets from the rest best (AUC 0.78: large for t)
- **How the class scores use it:** The Z (-17%) and W (-10%) scores subtract it and the q (+8%) and g (+6%) scores add it: W and Z sit lowest on this scale, so a broad, lopsided jet moves the decision from the bosons toward quark or gluon. It does not enter the t score, even though tops sit highest on it.
- *computed — used by:* raises the score of g (+6%), q (+8%); lowers the score of W (-10%), Z (-17%); does not (or hardly) enter the score of t (share of each class score’s average input)

```
z = 10.50
if girth2 < 0.0086: z += -1290 × (0.0086 − girth2)
if width < 0.013: z += -657 × (0.013 − width)
if mass_over_sum_pt > 0.0081: z += -80.70 × (mass_over_sum_pt − 0.0081)
if lam1 < 0.0078: z += 485 × (0.0078 − lam1)
if e2 < 0.051: z += 57.20 × (0.051 − e2)
if girth > 0.083: z += 100 × (girth − 0.083)
if girth2_top2 < 0.010: z += 106 × (0.010 − girth2_top2)
if girth2 < 0.0036: z += 573 × (0.0036 − girth2)
if mass < 50.00 and z_dr_0p05_0p1 < 0.760: z += 0.056 × (50.00 − mass) × (0.760 − z_dr_0p05_0p1)
if log_sum_pt < 6.70 and pt_7 < 46.00: z += 0.317 × (6.70 − log_sum_pt) × (46.00 − pt_7)
if lam2 < 0.00054 and z_dr_0p2_0p4 < 0.200: z += -8070 × (0.00054 − lam2) × (0.200 − z_dr_0p2_0p4)
if max_dr > 0.120: z += 14.10 × (max_dr − 0.120)
if mass < 50.00: z += -0.028 × (50.00 − mass)
if centroid_offset > 0.0076 and lam2 < 0.0035: z += 14800 × (centroid_offset − 0.0076) × (0.0035 − lam2)
if max_dr < 0.110: z += -13.80 × (0.110 − max_dr)
if C2 < 0.034: z += 27.20 × (0.034 − C2)
if mass_over_sum_pt > 0.0086 and pt_7 < 42.00: z += -0.709 × (mass_over_sum_pt − 0.0086) × (42.00 − pt_7)
if mass_over_sum_pt > 0.015 and tau32 < 0.520: z += -54.50 × (mass_over_sum_pt − 0.015) × (0.520 − tau32)
if girth2_top5 > 0.011: z += 178 × (girth2_top5 − 0.011)
if log_sum_pt < 6.80: z += -1.05 × (6.80 − log_sum_pt)
if centroid_offset > 0.0084 and C2 < 0.096: z += 477 × (centroid_offset − 0.0084) × (0.096 − C2)
if D2 < 1.70 and min_pair_mass < 2.40: z += -0.302 × (1.70 − D2) × (2.40 − min_pair_mass)
if e2 < 0.050 and z_dr_0p1_0p2 > 0.160: z += 1160 × (0.050 − e2) × (z_dr_0p1_0p2 − 0.160)
if C2 > 0.033: z += -23.90 × (C2 − 0.033)
if centroid_offset > 0.019: z += -38.10 × (centroid_offset − 0.019)
if D2 < 1.80 and pt_4 < 86.00: z += -0.011 × (1.80 − D2) × (86.00 − pt_4)
if girth2_top5 > 0.011 and pt_7 > 17.00: z += -6.12 × (girth2_top5 − 0.011) × (pt_7 − 17.00)
if lam2 > 0.0034: z += -1060 × (lam2 − 0.0034)
if C2 > 0.010 and pt_7 > 32.00: z += 1.88 × (C2 − 0.010) × (pt_7 − 32.00)
if planar_flow < 0.060: z += -10.50 × (0.060 − planar_flow)
if sum_pt > 990: z += 0.026 × (sum_pt − 990)
if log_sum_pt < 6.70 and z_7 < 0.049: z += 542 × (6.70 − log_sum_pt) × (0.049 − z_7)
if log_sum_pt < 6.70 and pt_6 < 37.00: z += 0.234 × (6.70 − log_sum_pt) × (37.00 − pt_6)
if centroid_offset > 0.0078 and mass_top3 < 3.50: z += -10.10 × (centroid_offset − 0.0078) × (3.50 − mass_top3)
if centroid_offset > 0.050: z += 106 × (centroid_offset − 0.050)
if log_sum_pt < 6.30 and z_7 < 0.071: z += 1010 × (6.30 − log_sum_pt) × (0.071 − z_7)
if sum_pt_top5 > 840: z += -0.0083 × (sum_pt_top5 − 840)
if log_sum_pt < 6.70 and mean_phi > 0.0098: z += -76.10 × (6.70 − log_sum_pt) × (mean_phi − 0.0098)
if log_sum_pt < 6.30 and pt_6 > 27.00: z += 0.248 × (6.30 − log_sum_pt) × (pt_6 − 27.00)
if girth2_top5 > 0.0082 and mean_eta > 0.014: z += -4370 × (girth2_top5 − 0.0082) × (mean_eta − 0.014)
if log_sum_pt < 6.70 and pt_dispersion > 0.400: z += -20.20 × (6.70 − log_sum_pt) × (pt_dispersion − 0.400)
if centroid_offset > 0.0079 and mean_eta2 < 0.0012: z += -24600 × (centroid_offset − 0.0079) × (0.0012 − mean_eta2)
if pt_6 < 25.00: z += 0.079 × (25.00 − pt_6)
if girth2_top2 < 0.0096 and mean_phi < -0.0091: z += 4430 × (0.0096 − girth2_top2) × (-0.0091 − mean_phi)
if mass < 49.00 and dr_7 > 0.150: z += 0.972 × (49.00 − mass) × (dr_7 − 0.150)
if girth2 < 0.0035 and dr_7 > 0.130: z += -7360 × (0.0035 − girth2) × (dr_7 − 0.130)
if centroid_offset > 0.019 and pt_5 > 59.00: z += 4.75 × (centroid_offset − 0.019) × (pt_5 − 59.00)
if width < 0.014 and mean_phi > 0.026: z += 7910 × (0.014 − width) × (mean_phi − 0.026)
if sum_pt > 970 and pt_6 > 36.00: z += -0.0002 × (sum_pt − 970) × (pt_6 − 36.00)
if width < 0.014 and mean_phi < -0.026: z += 5630 × (0.014 − width) × (-0.026 − mean_phi)
if centroid_offset > 0.019 and pt_5 < 25.00: z += 31.80 × (centroid_offset − 0.019) × (25.00 − pt_5)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.0086`; 2: `width < 0.013`; 3: `mass_over_sum_pt > 0.0081`; 4: `lam1 < 0.0078`; 5: `e2 < 0.051`; 6: `girth > 0.083`; 7: `girth2_top2 < 0.01`; 8: `girth2 < 0.0036`; 9: `mass < 50 and z_dr_0p05_0p1 < 0.76`; 10: `log_sum_pt < 6.7 and pt_7 < 46`; 11: `lam2 < 0.00054 and z_dr_0p2_0p4 < 0.2`; 12: `max_dr > 0.12`; 13: `mass < 50`; 14: `centroid_offset > 0.0076 and lam2 < 0.0035`; 15: `max_dr < 0.11`; 16: `C2 < 0.034`; 17: `mass_over_sum_pt > 0.0086 and pt_7 < 42`; 18: `mass_over_sum_pt > 0.015 and tau32 < 0.52`; 19: `girth2_top5 > 0.011`; 20: `log_sum_pt < 6.8`; 21: `centroid_offset > 0.0084 and C2 < 0.096`; 22: `D2 < 1.7 and min_pair_mass < 2.4`; 23: `e2 < 0.05 and z_dr_0p1_0p2 > 0.16`; 24: `C2 > 0.033`; 25: `centroid_offset > 0.019`; 26: `D2 < 1.8 and pt_4 < 86`; 27: `girth2_top5 > 0.011 and pt_7 > 17`; 28: `lam2 > 0.0034`; 29: `C2 > 0.01 and pt_7 > 32`; 30: `planar_flow < 0.06`; 31: `sum_pt > 990`; 32: `log_sum_pt < 6.7 and z_7 < 0.049`; 33: `log_sum_pt < 6.7 and pt_6 < 37`; 34: `centroid_offset > 0.0078 and mass_top3 < 3.5`; 35: `centroid_offset > 0.05`; 36: `log_sum_pt < 6.3 and z_7 < 0.071`; 37: `sum_pt_top5 > 840`; 38: `log_sum_pt < 6.7 and mean_phi > 0.0098`; 39: `log_sum_pt < 6.3 and pt_6 > 27`; 40: `girth2_top5 > 0.0082 and mean_eta > 0.014`; 41: `log_sum_pt < 6.7 and pt_dispersion > 0.4`; 42: `centroid_offset > 0.0079 and mean_eta2 < 0.0012`; 43: `pt_6 < 25`; 44: `girth2_top2 < 0.0096 and mean_phi < -0.0091`; 45: `mass < 49 and dr_7 > 0.15`; 46: `girth2 < 0.0035 and dr_7 > 0.13`; 47: `centroid_offset > 0.019 and pt_5 > 59`; 48: `width < 0.014 and mean_phi > 0.026`; 49: `sum_pt > 970 and pt_6 > 36`; 50: `width < 0.014 and mean_phi < -0.026`; 51: `centroid_offset > 0.019 and pt_5 < 25`):

- `✓✓✓✓✓·✓✓✓·✓·✓·✓✓···✓·······························` **Pencil-thin light quark/gluon jets** — 29.8% of jets, neuron 0.54, formula right for 61%. The largest group (30%), mostly light quarks (45%) with gluons (34%), nearly massless (8.2 GeV) with 99% of pT within 0.05 of the axis. The compactness cuts girth2 < 0.0086 (-10.725) and width < 0.013 (-8.353), plus mass < 50 and max_dr < 0.11, subtract heavily, only partly offset by lam1 < 0.0078, e2 < 0.051, girth2 < 0.0036 and mass < 50 and z_dr_0p05_0p1 < 0.76. The neuron is usually zero (on for 0.394, mean 0.541), so its small push up of g and q and down of W and Z hardly matters; the formula calls them q and is right only 0.611 of the time.
- `✓✓✓✓✓·✓··✓✓✓·✓·✓✓··✓✓✓···✓··✓✓·····················` **Two-prong W-rich jets** — 17.7% of jets, neuron 0.46, formula right for 71%. Mostly W (51%) with Z (31%), mass 54.0 GeV, pT concentrated at 0.05-0.1 from the axis (two prongs) with little beyond 0.1. mass_over_sum_pt > 0.0081 (-5.334), width < 0.013 and girth2 < 0.0086 all pass and outweigh lam1 < 0.0078, e2 < 0.051 and girth2_top2 < 0.01, while girth2 < 0.0036 never passes. The neuron is usually zero (on for 0.259, mean 0.458), only slightly lowering W and Z; the formula calls them W and is right 0.708 of the time.
- `✓✓✓✓✓·✓·✓✓✓✓✓✓·✓✓··✓✓✓···✓··✓✓···✓·················` **Compact medium-mass W-led jets** — 13.0% of jets, neuron 0.53, formula right for 58%. W-led (44%) mixture with Z (26%) and gluons, 42.5 GeV, fairly narrow (66% of pT within 0.05). girth2 < 0.0086, width < 0.013 and mass_over_sum_pt > 0.0081 subtract about 16 in total, against lam1 < 0.0078, e2 < 0.051, girth2_top2 < 0.01, max_dr > 0.12 and centroid_offset > 0.0076 and lam2 < 0.0035. The neuron is usually zero (on for 0.285, mean 0.533); the formula calls them W but is right only 0.58 of the time.
- `✓✓✓✓✓✓✓··✓✓✓·✓·✓✓··✓✓✓✓··✓··✓✓·····················` **Z jets with extra radiation** — 11.5% of jets, neuron 1.58, formula right for 72%. Mostly Z (62%) with tops (19%), 59.7 GeV, somewhat wider than average with pT at 0.05-0.1 and 23% beyond 0.1. mass_over_sum_pt > 0.0081 (-6.35) and width < 0.013 subtract, but girth2 < 0.0086 fails for some and e2 < 0.05 and z_dr_0p1_0p2 > 0.16 (common only here and in the off-centre group) plus log_sum_pt < 6.7 and pt_7 < 46 add. The neuron is on for 0.638 (1.576), which lowers the Z and W scores and raises g and q, working against the right answer, yet the formula still calls them Z and is right 0.723 of the time.
- `✓✓✓✓✓·✓✓✓✓✓·✓✓✓✓✓··✓✓····✓·······✓·······✓·········` **Light compact gluon-led mixture** — 10.5% of jets, neuron 0.94, formula right for 50%. A mixture led by gluons (35%) with quarks (25%), W (19%) and Z (14%), light (23.5 GeV) and narrow (85% of pT within 0.05). girth2 < 0.0086 (-8.827), width < 0.013, mass_over_sum_pt > 0.0081 and mass < 50 subtract; lam1 < 0.0078, e2 < 0.051, girth2 < 0.0036, girth2_top2 < 0.01 and mass < 50 and z_dr_0p05_0p1 < 0.76 add back. The neuron is on for 0.392 (0.94); the formula calls them g but is right only 0.504 of the time, a badly mixed group.
- `··✓··✓✓··✓✓✓·✓··✓✓✓✓✓✓·✓✓✓✓·✓······················` **Moderately wide top jets** — 6.5% of jets, neuron 5.62, formula right for 73%. Mostly tops (71%, g 19%), 65.7 GeV, about twice the average width with 40% of pT beyond 0.1 and low pT (588 GeV). They escape girth2 < 0.0086 and lam1 < 0.0078 and mostly width < 0.013, and gain from girth > 0.083, max_dr > 0.12, log_sum_pt < 6.7 and pt_7 < 46 and centroid_offset > 0.0076 and lam2 < 0.0035, against mass_over_sum_pt > 0.0081 (-8.329). The neuron is high (5.619), strongly lowering W and Z and raising g and q; the formula calls them t and is right 0.728 of the time, the gluons being the main errors.
- `··✓··✓···✓·✓·✓··✓✓✓✓✓✓·✓✓✓✓·✓······················` **Wide top jets** — 5.9% of jets, neuron 5.07, formula right for 83%. Mostly tops (82%), 79.6 GeV, over three times the average width with 71% of pT beyond 0.1. No compactness cut passes (width < 0.013 and e2 < 0.051 fail); girth > 0.083 (+5.053), girth2_top5 > 0.011, max_dr > 0.12 and log_sum_pt < 6.7 and pt_7 < 46 add, while mass_over_sum_pt > 0.0081 (-10.691), mass_over_sum_pt > 0.015 and tau32 < 0.52 and girth2_top5 > 0.011 and pt_7 > 17 subtract. The neuron is high (5.07), lowering W and Z; the formula calls them t and is right 0.829 of the time.
- `··✓··✓···✓·✓·✓··✓✓✓✓✓✓·✓✓✓✓·✓·········✓············` **Very wide top/gluon jets** — 3.0% of jets, neuron 6.11, formula right for 79%. Mostly tops (75%, g 18%), 89.4 GeV, five times the average width with 87% of pT beyond 0.1 and low pT (523 GeV). girth > 0.083 (+8.435), girth2_top5 > 0.011 and log_sum_pt < 6.7 and pt_7 < 46 add more than mass_over_sum_pt > 0.0081 (-13.151), girth2_top5 > 0.011 and pt_7 > 17 and mass_over_sum_pt > 0.015 and tau32 < 0.52 take away, the amounts growing with the width. The neuron is high (6.109), lowering W and Z; the formula calls them t and is right 0.791 of the time.
- `··✓··✓···✓·✓····✓✓✓✓·✓·✓✓✓✓✓✓·········✓············` **Wide tops with large lam2** — 1.9% of jets, neuron 0.63, formula right for 95%. Almost all tops (95%), 86.9 GeV, very wide with 89% of pT beyond 0.1. They look like the other wide top groups except that all pass lam2 > 0.0034 (-6.159), which barely fires elsewhere, and nearly all pass mass_over_sum_pt > 0.015 and tau32 < 0.52; with mass_over_sum_pt > 0.0081 (-12.695) this beats girth > 0.083 and girth2_top5 > 0.011. The neuron is usually zero (on for 0.254, mean 0.626), but the formula still calls them t and is right 0.953 of the time.
- `··✓·✓✓··✓✓✓✓✓✓··✓·✓✓✓✓✓✓✓✓✓·····✓✓✓··✓··✓··········` **Off-centre wide jets** — 0.4% of jets, neuron 7.61, formula right for 67%. A tiny group (0.4%) of tops (67%) and gluons (24%), lighter (44.5 GeV), wide with 87% of pT beyond 0.1 and a pT centroid far from the axis. All pass centroid_offset > 0.05, which is rare elsewhere, and e2 < 0.05 and z_dr_0p1_0p2 > 0.16 (+13.65), plus girth > 0.083 and centroid_offset > 0.0076 and lam2 < 0.0035, outweighing mass_over_sum_pt > 0.0081 and centroid_offset > 0.019. This is the neuron's highest value (7.614), lowering W and Z and raising g and q; the formula calls them t but is right only 0.667 of the time.

### neuron 7: Z-likeness: two-prong, mass window (moderate)

- **What it measures:** Rises for elongated two-prong jets (eccentricity +0.569, planar flow -0.569, τ21 -0.52) inside a mass/pT window (mass/pT > 0.072 and > 0.085 push it up, > 0.091 pushes it down) and of intermediate width (set by several girth2 cuts). Largest for Z (3.17), then W (1.87), with t (0.70), g (0.51) and q (0.26) low.
- *computed — its value:* largest for Z (3.17), then W (1.87), then t (0.70), then g (0.51), then q (0.26); it separates Z jets from the rest best (AUC 0.82: large for Z)
- **How the class scores use it:** The Z score adds it strongly (+19%) and the W score more weakly (+6%), so it marks a boson and leans the choice toward Z. It does not enter the g, q or t scores.
- *computed — used by:* raises the score of W (+6%), Z (+19%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 9.24
if girth2 > 0.0075: z += -1410 × (girth2 − 0.0075)
if girth2 > 0.0015: z += -612 × (girth2 − 0.0015)
if girth2 > 0.0087: z += 1470 × (girth2 − 0.0087)
if lam1 < 0.0084: z += -610 × (0.0084 − lam1)
if max_dr < 0.160: z += -40.20 × (0.160 − max_dr)
if mass_over_sum_pt > 0.091: z += -280 × (mass_over_sum_pt − 0.091)
if girth < 0.088: z += -52.90 × (0.088 − girth)
if mass_over_sum_pt > 0.085: z += 191 × (mass_over_sum_pt − 0.085)
if width < 0.0055: z += -781 × (0.0055 − width)
if max_dr < 0.160 and z_dr_0p05_0p1 < 0.670: z += 56.90 × (0.160 − max_dr) × (0.670 − z_dr_0p05_0p1)
if girth2 > 0.0044: z += -457 × (girth2 − 0.0044)
if mass_over_sum_pt > 0.072: z += 97.80 × (mass_over_sum_pt − 0.072)
if centroid_offset < 0.039 and sum_pt > 560: z += 0.227 × (0.039 − centroid_offset) × (sum_pt − 560)
if width < 0.0056 and n_dr_0p2_0p4 < 0.960: z += -445 × (0.0056 − width) × (0.960 − n_dr_0p2_0p4)
if width < 0.0053 and n_dr_0p1_0p2 < 3.10: z += 128 × (0.0053 − width) × (3.10 − n_dr_0p1_0p2)
if mass < 30.00: z += 0.093 × (30.00 − mass)
if girth2 > 0.015: z += 554 × (girth2 − 0.015)
if girth2 > 0.004 and eccentricity > 0.950: z += 9130 × (girth2 − 0.004) × (eccentricity − 0.950)
if max_dr < 0.200 and z_dr_0p05_0p1 > 0.056: z += 37.60 × (0.200 − max_dr) × (z_dr_0p05_0p1 − 0.056)
if centroid_offset < 0.021: z += -70.80 × (0.021 − centroid_offset)
if pt_7 < 47.00 and planar_flow < 0.740: z += -0.097 × (47.00 − pt_7) × (0.740 − planar_flow)
if girth2_top2 < 0.0011 and n_dr_0p2_0p4 < 0.970: z += 1880 × (0.0011 − girth2_top2) × (0.970 − n_dr_0p2_0p4)
if girth2 > 0.0075 and log_sum_pt > 6.20: z += -1440 × (girth2 − 0.0075) × (log_sum_pt − 6.20)
if lam1 < 0.0081 and D2 < 1.10: z += -1250 × (0.0081 − lam1) × (1.10 − D2)
if e2_sq < 0.0012: z += 1250 × (0.0012 − e2_sq)
if max_dr < 0.160 and D2 < 1.20: z += 34.60 × (0.160 − max_dr) × (1.20 − D2)
if girth2_top2 < 0.0011: z += -1090 × (0.0011 − girth2_top2)
if planar_flow < 0.200 and D2 < 1.60: z += -4.77 × (0.200 − planar_flow) × (1.60 − D2)
if mass_over_sum_pt < 0.130 and z_dr_0p05_0p1 > 0.270: z += -34.70 × (0.130 − mass_over_sum_pt) × (z_dr_0p05_0p1 − 0.270)
if girth2_top2 < 0.001 and log_sum_pt > 6.30: z += -2170 × (0.001 − girth2_top2) × (log_sum_pt − 6.30)
if planar_flow < 0.200 and sum_pt > 620: z += 0.023 × (0.200 − planar_flow) × (sum_pt − 620)
if mass > 80.40: z += -0.189 × (mass − 80.40)
if e2 < 0.038 and D2 < 1.10: z += 325 × (0.038 − e2) × (1.10 − D2)
if width < 0.00052: z += -2300 × (0.00052 − width)
if planar_flow < 0.190 and n_dr_0p1_0p2 < 2.90: z += -1.17 × (0.190 − planar_flow) × (2.90 − n_dr_0p1_0p2)
if e2 < 0.025 and tau21 < 0.460: z += 338 × (0.025 − e2) × (0.460 − tau21)
if centroid_offset < 0.022 and C2 > 0.025: z += 2380 × (0.022 − centroid_offset) × (C2 − 0.025)
if z_dr_0p05_0p1 > 0.660: z += -2.07 × (z_dr_0p05_0p1 − 0.660)
if lam1 < 0.0087 and n_pt_above_50 < 4.10: z += -78.80 × (0.0087 − lam1) × (4.10 − n_pt_above_50)
if centroid_offset < 0.037 and C2 > 0.068: z += -1970 × (0.037 − centroid_offset) × (C2 − 0.068)
if e2 < 0.025 and D2 < 1.10: z += -509 × (0.025 − e2) × (1.10 − D2)
if mass > 80.40 and eccentricity > 0.920: z += -1.05 × (mass − 80.40) × (eccentricity − 0.920)
if centroid_offset > 0.031 and pt_2 > 64.00: z += -1.32 × (centroid_offset − 0.031) × (pt_2 − 64.00)
if width < 0.006 and mean_phi < -0.0044: z += 7290 × (0.006 − width) × (-0.0044 − mean_phi)
if mass > 80.40 and m012 < 5.40: z += -0.056 × (mass − 80.40) × (5.40 − m012)
if centroid_offset > 0.031 and pt_0 > 380: z += -10.90 × (centroid_offset − 0.031) × (pt_0 − 380)
if girth2_top3 < 0.005 and n_dr_0p2_0p4 > 0.880: z += 147 × (0.005 − girth2_top3) × (n_dr_0p2_0p4 − 0.880)
if e2 < 0.025 and phi_0 > 0.055: z += -38000 × (0.025 − e2) × (phi_0 − 0.055)
if girth2_top3 < 0.0059 and max_pair_mass > 46.00: z += 255 × (0.0059 − girth2_top3) × (max_pair_mass − 46.00)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 > 0.0075`; 2: `girth2 > 0.0015`; 3: `girth2 > 0.0087`; 4: `lam1 < 0.0084`; 5: `max_dr < 0.16`; 6: `mass_over_sum_pt > 0.091`; 7: `girth < 0.088`; 8: `mass_over_sum_pt > 0.085`; 9: `width < 0.0055`; 10: `max_dr < 0.16 and z_dr_0p05_0p1 < 0.67`; 11: `girth2 > 0.0044`; 12: `mass_over_sum_pt > 0.072`; 13: `centroid_offset < 0.039 and sum_pt > 560`; 14: `width < 0.0056 and n_dr_0p2_0p4 < 0.96`; 15: `width < 0.0053 and n_dr_0p1_0p2 < 3.1`; 16: `mass < 30`; 17: `girth2 > 0.015`; 18: `girth2 > 0.004 and eccentricity > 0.95`; 19: `max_dr < 0.2 and z_dr_0p05_0p1 > 0.056`; 20: `centroid_offset < 0.021`; 21: `pt_7 < 47 and planar_flow < 0.74`; 22: `girth2_top2 < 0.0011 and n_dr_0p2_0p4 < 0.97`; 23: `girth2 > 0.0075 and log_sum_pt > 6.2`; 24: `lam1 < 0.0081 and D2 < 1.1`; 25: `e2_sq < 0.0012`; 26: `max_dr < 0.16 and D2 < 1.2`; 27: `girth2_top2 < 0.0011`; 28: `planar_flow < 0.2 and D2 < 1.6`; 29: `mass_over_sum_pt < 0.13 and z_dr_0p05_0p1 > 0.27`; 30: `girth2_top2 < 0.001 and log_sum_pt > 6.3`; 31: `planar_flow < 0.2 and sum_pt > 620`; 32: `mass > 80.4`; 33: `e2 < 0.038 and D2 < 1.1`; 34: `width < 0.00052`; 35: `planar_flow < 0.19 and n_dr_0p1_0p2 < 2.9`; 36: `e2 < 0.025 and tau21 < 0.46`; 37: `centroid_offset < 0.022 and C2 > 0.025`; 38: `z_dr_0p05_0p1 > 0.66`; 39: `lam1 < 0.0087 and n_pt_above_50 < 4.1`; 40: `centroid_offset < 0.037 and C2 > 0.068`; 41: `e2 < 0.025 and D2 < 1.1`; 42: `mass > 80.4 and eccentricity > 0.92`; 43: `centroid_offset > 0.031 and pt_2 > 64`; 44: `width < 0.006 and mean_phi < -0.0044`; 45: `mass > 80.4 and m012 < 5.4`; 46: `centroid_offset > 0.031 and pt_0 > 380`; 47: `girth2_top3 < 0.005 and n_dr_0p2_0p4 > 0.88`; 48: `e2 < 0.025 and phi_0 > 0.055`; 49: `girth2_top3 < 0.0059 and max_pair_mass > 46`):

- `···✓✓·✓·✓✓··✓✓✓✓···✓✓✓··✓·✓··✓···✓···············` **Pencil-thin light quark/gluon jets** — 32.9% of jets, neuron 0.20, formula right for 60%. The largest group (33%), mostly light quarks (42%) with gluons (36%), nearly massless (9.0 GeV) with 98% of pT within 0.05. Every compactness test fires: max_dr < 0.16, lam1 < 0.0084, width < 0.0055, girth < 0.088 and width < 0.0056 and n_dr_0p2_0p4 < 0.96 subtract about 20, while max_dr < 0.16 and z_dr_0p05_0p1 < 0.67, mass < 30, girth2_top2 < 0.0011 and n_dr_0p2_0p4 < 0.97 and e2_sq < 0.0012 add back less. The neuron is usually zero (on for 0.191, mean 0.197), so it adds almost nothing to the W and Z scores; the formula calls them q and is right only 0.597 of the time.
- `·✓·✓✓·✓···✓✓✓····✓✓✓✓··✓·✓·✓✓·✓···✓··✓···········` **Two-prong Z/W jets** — 28.5% of jets, neuron 3.30, formula right for 71%. Mostly Z (42%) with W (34%) and tops (13%), mass 54.7 GeV and 64% of pT at 0.05-0.1 from the axis: a clean two-prong shape of intermediate width. The two-prong tests max_dr < 0.2 and z_dr_0p05_0p1 > 0.056, centroid_offset < 0.039 and sum_pt > 560 and girth2 > 0.004 and eccentricity > 0.95 add, and the width cuts girth2 > 0.0015, girth2 > 0.0044, max_dr < 0.16, lam1 < 0.0084 and lam1 < 0.0081 and D2 < 1.1 subtract moderately, leaving the neuron's highest value (3.299, on for 0.958). This raises the Z score most and the W score too; the formula calls them Z and is right 0.708 of the time, the rest being mainly W-Z swaps.
- `·✓·✓✓·✓·✓✓··✓✓✓····✓✓·········✓···✓✓✓············` **Compact medium-mass W-led mixture** — 20.2% of jets, neuron 1.25, formula right for 57%. A W-led (36%) mixture with Z (24%), gluons (17%) and quarks (15%), 38.6 GeV, narrow (79% of pT within 0.05). lam1 < 0.0084, girth < 0.088, width < 0.0055, girth2 > 0.0015, pt_7 < 47 and planar_flow < 0.74 and (for half) max_dr < 0.16 subtract, against centroid_offset < 0.039 and sum_pt > 560, width < 0.0053 and n_dr_0p1_0p2 < 3.1 and e2 < 0.025 and tau21 < 0.46; the mass window cut mass_over_sum_pt > 0.072 almost never passes. The neuron is middling (1.255, on for 0.664), adding to W and Z; the formula calls them W but is right only 0.571 of the time.
- `✓✓✓··✓·✓··✓✓·····✓✓·✓·✓····✓✓····················` **Moderately wide top/gluon jets** — 3.9% of jets, neuron 1.16, formula right for 65%. Mostly tops (63%) with gluons (22%), 58.6 GeV, nearly twice the average width, 37% of pT beyond 0.1. Here the width ladder girth2 > 0.0015, girth2 > 0.0044, girth2 > 0.0075 (together about -15) against girth2 > 0.0087 (+4.096) meets the mass window mass_over_sum_pt > 0.072 and > 0.085 (+) and > 0.091 (-), and the balance stays slightly positive (1.164, on for 0.594). That adds to the W and Z scores for these tops; the formula still calls them t and is right 0.648 of the time.
- `✓✓✓··✓·✓··✓✓····✓✓··✓·✓····✓✓····················` **Wide top jets** — 3.6% of jets, neuron 0.08, formula right for 76%. Mostly tops (75%, g 17%), 69.3 GeV, 2.4 times the average width with 52% of pT beyond 0.1. The same ladder with bigger amounts (they grow with width): girth2 > 0.0075 (-11.238) against girth2 > 0.0087 (+9.952), and mass_over_sum_pt > 0.091 (-7.428) against mass_over_sum_pt > 0.085 and > 0.072, with girth2 > 0.0015 and > 0.0044 tipping it negative. The neuron is mostly zero (on for 0.094), leaving the W and Z scores alone; the formula calls them t and is right 0.763 of the time.
- `✓✓✓··✓·✓··✓✓····✓···✓·✓··························` **Wider heavy top jets** — 3.3% of jets, neuron 0.03, formula right for 82%. Mostly tops (81%), 77.2 GeV, three times the average width with 65% of pT beyond 0.1. All pass the whole girth2 ladder and mass window; the opposing pairs girth2 > 0.0075 / girth2 > 0.0087 and mass_over_sum_pt > 0.091 / > 0.085 nearly cancel, and girth2 > 0.0015 and girth2 > 0.0044 leave the total below zero, so the neuron is essentially off (on for 0.034). The formula calls them t and is right 0.821 of the time.
- `✓✓✓··✓·✓··✓✓····✓···✓·✓········✓·················` **Very wide heavy top jets** — 3.1% of jets, neuron 0.02, formula right for 86%. Mostly tops (86%), 82.7 GeV, nearly four times the average width with 75% of pT beyond 0.1. Same cancellation with larger amounts (girth2 > 0.0075 at -23.081 against girth2 > 0.0087 at +22.299), and girth2 > 0.015 now adds but cannot overcome girth2 > 0.0015 and the mass-window minus, so the neuron is off (on for 0.026). The formula calls them t and is right 0.864 of the time.
- `✓✓✓··✓·✓··✓✓····✓···✓·✓········✓·················` **Very wide heavy top jets** — 2.6% of jets, neuron 0.01, formula right for 88%. Mostly tops (87%), 88.8 GeV, 4.5 times the average width with 83% of pT beyond 0.1. The girth2 ladder and the mass_over_sum_pt window again cancel pairwise (about -29.69 against +29.19 for the first pair) with the leftover negative, so the neuron is off (on for 0.016). The formula calls them t and is right 0.884 of the time.
- `✓✓✓··✓·✓··✓✓····✓···✓·✓········✓·················` **Extremely wide top/gluon jets** — 1.4% of jets, neuron 0.02, formula right for 81%. Mostly tops (77%, g 17%), 91.1 GeV, over five times the average width with 88% of pT beyond 0.1. Same pattern with even larger opposing terms (girth2 > 0.0075 and girth2 > 0.0087 each near 37.6 in size) and girth2 > 0.015 adding, but the total stays negative and the neuron is off (on for 0.029). The formula calls them t and is right 0.814 of the time.
- `✓✓✓··✓·✓··✓✓····✓···✓··········✓·················` **Widest soft-leading top/gluon jets** — 0.3% of jets, neuron 0.02, formula right for 61%. A tiny group (0.3%) of tops (58%) and gluons (30%), 93.9 GeV, the widest jets (0.0449) with 92% of pT beyond 0.1 and a soft leading particle (113 GeV). The largest cancellation of all (girth2 > 0.0087 +53.247 against girth2 > 0.0075 -52.766, and mass_over_sum_pt > 0.091 against > 0.085) with girth2 > 0.0015 and > 0.0044 winning, so the neuron is off (on for 0.02). The formula calls them t but is right only 0.613 of the time, the gluons being misread.

### neuron 8: Narrowness (small width) (moderate)

- **What it measures:** Rises for narrow jets: width < 0.0049 is its largest term, though the very narrowest (girth < 0.063 with width < 0.0055) are pulled back; overall it falls with width and girth2 (-0.686). Largest for q (2.96), then g (1.74), with W (0.55), Z (0.35) and t (0.15) low.
- *computed — its value:* largest for q (2.96), then g (1.74), then W (0.55), then Z (0.35), then t (0.15); it separates q jets from the rest best (AUC 0.82: large for q)
- **How the class scores use it:** The q score adds it (+3%) and the W score subtracts it (-6%), in line with quarks sitting high and W jets low. The t score also adds a little (+5%) although tops sit lowest, probably as a small correction for narrow jets; it does not enter the g or Z scores.
- *computed — used by:* raises the score of q (+3%), t (+5%); lowers the score of W (-6%); does not (or hardly) enter the score of g, Z (share of each class score’s average input)

```
z = -0.441
if width < 0.0049: z += 2510 × (0.0049 − width)
if girth < 0.063 and width < 0.0055: z += -31300 × (0.063 − girth) × (0.0055 − width)
if girth2 < 0.0067 and centroid_offset < 0.025: z += 24600 × (0.0067 − girth2) × (0.025 − centroid_offset)
if max_dr < 0.180 and lam2 < 0.00021: z += 85800 × (0.180 − max_dr) × (0.00021 − lam2)
if C2 < 0.027: z += -92.20 × (0.027 − C2)
if mass < 29.00 and centroid_offset < 0.024: z += -7.46 × (29.00 − mass) × (0.024 − centroid_offset)
if width < 0.0051 and centroid_offset > 0.0071: z += -60500 × (0.0051 − width) × (centroid_offset − 0.0071)
if LHA < 0.200 and width < 0.00067: z += 51300 × (0.200 − LHA) × (0.00067 − width)
if log_sum_pt > 6.70: z += -16.90 × (log_sum_pt − 6.70)
if z_dr_0_0p05 > 0.870 and lam2 < 0.00054: z += -18700 × (z_dr_0_0p05 − 0.870) × (0.00054 − lam2)
if dr_0 < 0.016: z += -152 × (0.016 − dr_0)
if girth < 0.057 and log_sum_pt > 6.70: z += 219 × (0.057 − girth) × (log_sum_pt − 6.70)
if width < 0.0048 and mass_over_sum_pt_sq > 0.00045: z += -402000 × (0.0048 − width) × (mass_over_sum_pt_sq − 0.00045)
if girth2 < 0.0065 and planar_flow < 0.380: z += 523 × (0.0065 − girth2) × (0.380 − planar_flow)
if pt_7 > 34.00: z += -0.035 × (pt_7 − 34.00)
if log_sum_pt > 6.70 and pt_7 < 50.00: z += 0.155 × (log_sum_pt − 6.70) × (50.00 − pt_7)
if mass < 22.00 and centroid_offset > 0.031: z += -28.00 × (22.00 − mass) × (centroid_offset − 0.031)
if centroid_offset < 0.0034: z += 433 × (0.0034 − centroid_offset)
if LHA < 0.200 and mean_phi > -0.00075: z += -912 × (0.200 − LHA) × (mean_phi − -0.00075)
if mass < 22.00 and max_pair_mass > 13.00: z += 61.50 × (22.00 − mass) × (max_pair_mass − 13.00)
if girth2_top5 < 0.00022 and n_dr_0p2_0p4 > 0.029: z += 23500 × (0.00022 − girth2_top5) × (n_dr_0p2_0p4 − 0.029)
if LHA < 0.190 and girth2 > 0.0075: z += 178000 × (0.190 − LHA) × (girth2 − 0.0075)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.0049`; 2: `girth < 0.063 and width < 0.0055`; 3: `girth2 < 0.0067 and centroid_offset < 0.025`; 4: `max_dr < 0.18 and lam2 < 0.00021`; 5: `C2 < 0.027`; 6: `mass < 29 and centroid_offset < 0.024`; 7: `width < 0.0051 and centroid_offset > 0.0071`; 8: `LHA < 0.2 and width < 0.00067`; 9: `log_sum_pt > 6.7`; 10: `z_dr_0_0p05 > 0.87 and lam2 < 0.00054`; 11: `dr_0 < 0.016`; 12: `girth < 0.057 and log_sum_pt > 6.7`; 13: `width < 0.0048 and mass_over_sum_pt_sq > 0.00045`; 14: `girth2 < 0.0065 and planar_flow < 0.38`; 15: `pt_7 > 34`; 16: `log_sum_pt > 6.7 and pt_7 < 50`; 17: `mass < 22 and centroid_offset > 0.031`; 18: `centroid_offset < 0.0034`; 19: `LHA < 0.2 and mean_phi > -0.00075`; 20: `mass < 22 and max_pair_mass > 13`; 21: `girth2_top5 < 0.00022 and n_dr_0p2_0p4 > 0.029`; 22: `LHA < 0.19 and girth2 > 0.0075`):

- `··············✓·······` **Massive wide boson/top jets** — 47.5% of jets, neuron 0.06, formula right for 73%. Nearly half of all jets (47%): a top-led mixture (t 38%, Z 26%, W 21%, g 10%) at 60.8 GeV, about twice the average width with 34% of pT beyond 0.1. They are too wide for width < 0.0049 (passes for 0.104), the neuron's main plus, so only small terms remain, such as C2 < 0.027 (-0.464) and max_dr < 0.18 and lam2 < 0.00021 (+0.337) for about half. The neuron is usually zero (on for 0.108, mean 0.06) and leaves the scores alone; the formula calls them t and is right 0.726 of the time, the separation happening in other neurons.
- `✓✓✓✓✓✓·✓·✓✓···✓···✓···` **Pencil-thin massless quark jets** — 10.6% of jets, neuron 3.37, formula right for 63%. Mostly light quarks (52%) with gluons (37%), essentially massless (6.4 GeV) with all pT within 0.05 of the axis. width < 0.0049 adds the most here (+12.033, it grows the narrower the jet), helped by girth2 < 0.0067 and centroid_offset < 0.025, LHA < 0.2 and width < 0.00067 and max_dr < 0.18 and lam2 < 0.00021, while girth < 0.063 and width < 0.0055 (-9.243), mass < 29 and centroid_offset < 0.024, C2 < 0.027 and dr_0 < 0.016 pull back. The neuron is on for all (3.365), raising the q and t scores and lowering W; the formula calls them q and is right 0.626 of the time, the gluons being the errors.
- `✓✓✓✓✓✓✓✓·✓✓··✓✓···✓···` **Very narrow light gluon/quark jets** — 9.6% of jets, neuron 2.81, formula right for 57%. Gluons (44%) and quarks (35%) with some W, light (11.8 GeV) and very narrow (98% of pT within 0.05). width < 0.0049 (+11.148) against girth < 0.063 and width < 0.0055 (-7.101), with smaller pluses (girth2 < 0.0067 and centroid_offset < 0.025, max_dr < 0.18 and lam2 < 0.00021) and minuses (mass < 29 and centroid_offset < 0.024, C2 < 0.027, width < 0.0051 and centroid_offset > 0.0071). The neuron is high (2.812), raising q and t and lowering W; the formula calls them g but is right only 0.57 of the time.
- `✓✓✓✓··✓·····✓✓········` **Medium-mass narrowish W-led jets** — 8.7% of jets, neuron 0.72, formula right for 53%. A W-led (39%) mixture with Z (23%), gluons (18%) and quarks (11%) at 37.6 GeV, fairly narrow (74% of pT within 0.05). Being just narrow enough, width < 0.0049 adds only +4.17, and width < 0.0051 and centroid_offset > 0.0071, width < 0.0048 and mass_over_sum_pt_sq > 0.00045 (almost only here and in the next-lightest mixed group) and girth < 0.063 and width < 0.0055 take most of it back. The neuron is on for about half (0.716); the formula calls them W but is right only 0.532 of the time.
- `✓✓✓✓✓✓·✓✓✓✓✓···✓·✓✓···` **High-pT pencil-thin quark jets** — 6.8% of jets, neuron 3.74, formula right for 74%. Mostly light quarks (67%), essentially massless, at high pT (1012 GeV) with a 454 GeV leading particle. width < 0.0049 (+12.065), girth2 < 0.0067 and centroid_offset < 0.025, LHA < 0.2 and width < 0.00067 and girth < 0.057 and log_sum_pt > 6.7 add, while girth < 0.063 and width < 0.0055, log_sum_pt > 6.7 and mass < 29 and centroid_offset < 0.024 subtract. This is the neuron's highest value (3.741), raising q and t and lowering W; the formula calls them q and is right 0.744 of the time.
- `✓✓·✓✓·✓··✓···✓✓·······` **Light off-centre mixed jets** — 5.8% of jets, neuron 0.16, formula right for 43%. A mixture (g 31%, Z 25%, W 24%, q 13%), nearly massless (9.2 GeV) but with the pT centroid off the axis, and a softer leading particle (204 GeV). width < 0.0049 (+9.452) is cancelled by width < 0.0051 and centroid_offset > 0.0071 (-5.031, passing for all here) and girth < 0.063 and width < 0.0055, with C2 < 0.027 and z_dr_0_0p05 > 0.87 and lam2 < 0.00054 pushing it below zero. The neuron is usually zero (on for 0.174); the formula calls them g but is right only 0.428 of the time, the worst group of this neuron: low-mass bosons get misread.
- `✓✓✓✓✓✓✓··✓··✓✓········` **Narrow light gluon-led mixture** — 5.7% of jets, neuron 2.76, formula right for 52%. A gluon-led (35%) mixture with quarks (29%) and W (20%), 28.0 GeV, narrow (88% of pT within 0.05). width < 0.0049 (+8.197) and girth2 < 0.0067 and centroid_offset < 0.025 outweigh girth < 0.063 and width < 0.0055, width < 0.0048 and mass_over_sum_pt_sq > 0.00045 and width < 0.0051 and centroid_offset > 0.0071. The neuron is high (2.76), raising q and t and lowering W; the formula calls them g but is right only 0.524 of the time.
- `··✓✓✓···✓····✓·✓······` **High-pT two-prong Z/W jets** — 5.0% of jets, neuron 0.01, formula right for 78%. Z (45%) and W (41%) at 73.0 GeV, high pT (943 GeV) with a 412 GeV leading particle, moderately narrow. Most fail width < 0.0049, and log_sum_pt > 6.7 (-2.476, always passing) plus C2 < 0.027 beat log_sum_pt > 6.7 and pt_7 < 50 and max_dr < 0.18 and lam2 < 0.00021, so the neuron is essentially off (on for 0.02). The formula splits them Z/W and is right 0.783 of the time.
- `✓✓·✓✓·✓······✓✓·✓·····` **Massless jets with off-axis pT** — 0.6% of jets, neuron 0.00, formula right for 54%. A tiny group (0.6%) of gluons (52%), tops (26%) and quarks (13%) with almost no mass (6.6 GeV) yet 75% of pT at 0.05-0.1 from the axis and a soft leading particle (146 GeV): an odd, off-centre configuration. mass < 22 and centroid_offset > 0.031 (-13.26), which fires for all of them and almost never elsewhere, overwhelms width < 0.0049, so the neuron is off for every jet. The formula calls them g and is right only 0.544 of the time.

### neuron 15: Width band above W (Z-like) (moderate)

- **What it measures:** Rises in a width band (width < 0.0067 pushes it down, width < 0.013 up; λ1 < 0.0067 up, λ1 < 0.0083 down) with small e2 (< 0.024 and < 0.041 push it up); it grows with the number of particles at 0.05 ≤ ΔR < 0.1 (+0.384). Largest for Z (1.33), then t (0.64), low for g (0.29), q (0.19) and W (0.17).
- *computed — its value:* largest for Z (1.33), then t (0.64), then g (0.29), then q (0.19), then W (0.17); it separates Z jets from the rest best (AUC 0.74: large for Z)
- **How the class scores use it:** The W score subtracts it (-8%) and the Z score more weakly (-3%); since W jets sit lowest and Z jets highest, the net effect moves jets from W toward Z. It does not enter the g, q or t scores.
- *computed — used by:* lowers the score of W (-8%), Z (-3%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = -1.86
if width < 0.0067: z += -1390 × (0.0067 − width)
if lam1 < 0.0067: z += 933 × (0.0067 − lam1)
if lam1 < 0.0083: z += -654 × (0.0083 − lam1)
if width < 0.013: z += 315 × (0.013 − width)
if e2 < 0.024: z += 244 × (0.024 − e2)
if e2 < 0.041: z += 64.20 × (0.041 − e2)
if girth > 0.032: z += 33.70 × (girth − 0.032)
if z_dr_0p1_0p2 < 0.320: z += 3.68 × (0.320 − z_dr_0p1_0p2)
if girth2_top2 < 0.0038: z += -436 × (0.0038 − girth2_top2)
if tau21 < 0.230 and z_dr_0p2_0p4 < 0.220: z += 69.70 × (0.230 − tau21) × (0.220 − z_dr_0p2_0p4)
if lam2 < 0.00031: z += -3280 × (0.00031 − lam2)
if mass_over_sum_pt < 0.068: z += -27.10 × (0.068 − mass_over_sum_pt)
if girth2_top2 < 0.0074: z += 89.90 × (0.0074 − girth2_top2)
if LHA > 0.340: z += -35.40 × (LHA − 0.340)
if LHA > 0.180 and sum_pt_top3 > 350: z += 0.049 × (LHA − 0.180) × (sum_pt_top3 − 350)
if width < 0.0076 and e2 > 0.024: z += -66400 × (0.0076 − width) × (e2 − 0.024)
if width < 0.0061 and log_sum_pt > 6.90: z += -10600 × (0.0061 − width) × (log_sum_pt − 6.90)
if log_sum_pt > 6.90: z += 48.60 × (log_sum_pt − 6.90)
if tau21 < 0.270 and girth2_top5 > 0.0084: z += -1160 × (0.270 − tau21) × (girth2_top5 − 0.0084)
if z_dr_0p05_0p1 > 0.750: z += -5.80 × (z_dr_0p05_0p1 − 0.750)
if LHA > 0.310 and pt_dispersion < 0.450: z += -163 × (LHA − 0.310) × (0.450 − pt_dispersion)
if lam1 < 0.0082 and D2 < 0.760: z += -852 × (0.0082 − lam1) × (0.760 − D2)
if tau21 < 0.230 and z_dr_0p05_0p1 < 0.630: z += -7.98 × (0.230 − tau21) × (0.630 − z_dr_0p05_0p1)
if lam1 < 0.0065 and pt1_dr01 > 1.30: z += 33.00 × (0.0065 − lam1) × (pt1_dr01 − 1.30)
if n_dr_0_0p05 < 1.80 and pt_dispersion < 0.430: z += 5.81 × (1.80 − n_dr_0_0p05) × (0.430 − pt_dispersion)
if width < 0.0086 and planar_flow < 0.064: z += -2630 × (0.0086 − width) × (0.064 − planar_flow)
if lam1 < 0.0083 and m01 > 17.00: z += -24.50 × (0.0083 − lam1) × (m01 − 17.00)
if mass > 80.40 and z_dr_0p2_0p4 < 0.220: z += -0.665 × (mass − 80.40) × (0.220 − z_dr_0p2_0p4)
if log_sum_pt > 6.90 and mean_phi > 0.017: z += 17900 × (log_sum_pt − 6.90) × (mean_phi − 0.017)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.0067`; 2: `lam1 < 0.0067`; 3: `lam1 < 0.0083`; 4: `width < 0.013`; 5: `e2 < 0.024`; 6: `e2 < 0.041`; 7: `girth > 0.032`; 8: `z_dr_0p1_0p2 < 0.32`; 9: `girth2_top2 < 0.0038`; 10: `tau21 < 0.23 and z_dr_0p2_0p4 < 0.22`; 11: `lam2 < 0.00031`; 12: `mass_over_sum_pt < 0.068`; 13: `girth2_top2 < 0.0074`; 14: `LHA > 0.34`; 15: `LHA > 0.18 and sum_pt_top3 > 350`; 16: `width < 0.0076 and e2 > 0.024`; 17: `width < 0.0061 and log_sum_pt > 6.9`; 18: `log_sum_pt > 6.9`; 19: `tau21 < 0.27 and girth2_top5 > 0.0084`; 20: `z_dr_0p05_0p1 > 0.75`; 21: `LHA > 0.31 and pt_dispersion < 0.45`; 22: `lam1 < 0.0082 and D2 < 0.76`; 23: `tau21 < 0.23 and z_dr_0p05_0p1 < 0.63`; 24: `lam1 < 0.0065 and pt1_dr01 > 1.3`; 25: `n_dr_0_0p05 < 1.8 and pt_dispersion < 0.43`; 26: `width < 0.0086 and planar_flow < 0.064`; 27: `lam1 < 0.0083 and m01 > 17`; 28: `mass > 80.4 and z_dr_0p2_0p4 < 0.22`; 29: `log_sum_pt > 6.9 and mean_phi > 0.017`):

- `✓✓✓✓✓✓·✓✓·✓✓✓················` **** — 28.0% of jets, neuron 0.01, formula right for 61%.  
- `✓✓✓✓·✓✓✓✓✓✓·✓·✓✓·····✓···✓···` **** — 14.2% of jets, neuron 0.36, formula right for 69%.  
- `··✓✓·✓✓✓·✓✓·✓·✓✓·····✓··✓✓···` **** — 13.4% of jets, neuron 2.15, formula right for 76%.  
- `···✓··✓✓····✓·······✓········` **** — 11.0% of jets, neuron 1.11, formula right for 69%.  
- `✓✓✓✓✓✓✓✓✓✓✓✓✓·✓·······✓······` **** — 10.9% of jets, neuron 0.36, formula right for 56%.  
- `✓✓✓✓✓✓✓✓✓·✓✓✓················` **** — 10.4% of jets, neuron 0.15, formula right for 52%.  
- `······✓······✓······✓···✓····` **** — 6.6% of jets, neuron 0.05, formula right for 88%.  
- `······✓··✓✓··✓····✓·✓·✓·✓····` **** — 3.8% of jets, neuron 0.02, formula right for 74%.  
- `✓✓✓✓✓✓·✓✓·✓✓✓···✓✓···········` **** — 1.3% of jets, neuron 0.18, formula right for 66%.  
- `✓✓✓✓✓✓·✓✓·✓✓✓···✓✓·····✓·····` **** — 0.3% of jets, neuron 0.13, formula right for 63%.  

### neuron 12: Very wide, busy jet (minor)

- **What it measures:** Switched on only for very wide jets (girth2 > 0.019, more so with pT_7 > 15 GeV, a little more for mass > 91.2 GeV) and cut off when e2 > 0.063; it tracks the number of particles above 10 GeV (+0.849). Small for all types: t (0.23), g (0.10), q (0.03), W (0.00), Z (0.00).
- *computed — its value:* largest for t (0.23), then g (0.10), then q (0.03), then W (0.00), then Z (0.00); it separates t jets from the rest best (AUC 0.57: large for t)
- **How the class scores use it:** It does not enter any class score appreciably (at most a -0.009 share, in the t score), so it has almost no effect on the decision.
- *computed — used by:* ; does not (or hardly) enter the score of g, q, W, Z, t (share of each class score’s average input)

```
z = -1.38
if e2 > 0.063: z += -119 × (e2 − 0.063)
if girth2 > 0.019: z += 232 × (girth2 − 0.019)
if girth2 > 0.019 and pt_7 > 15.00: z += 6.87 × (girth2 − 0.019) × (pt_7 − 15.00)
if mass > 91.20: z += 0.099 × (mass − 91.20)
if girth2 > 0.015 and lam2 > 5.6e-06: z += 8450 × (girth2 − 0.015) × (lam2 − 5.6e-06)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `e2 > 0.063`; 2: `girth2 > 0.019`; 3: `girth2 > 0.019 and pt_7 > 15`; 4: `mass > 91.2`; 5: `girth2 > 0.015 and lam2 > 5.6e-06`):

- `·····` **** — 91.2% of jets, neuron 0.00, formula right for 64%.  
- `✓✓✓·✓` **** — 2.1% of jets, neuron 0.16, formula right for 90%.  
- `✓✓✓·✓` **** — 2.0% of jets, neuron 0.00, formula right for 84%.  
- `✓✓✓·✓` **** — 1.7% of jets, neuron 0.53, formula right for 89%.  
- `✓✓✓·✓` **** — 0.8% of jets, neuron 0.81, formula right for 76%.  
- `✓✓✓·✓` **** — 0.7% of jets, neuron 2.20, formula right for 80%.  
- `✓✓✓✓✓` **** — 0.7% of jets, neuron 2.73, formula right for 81%.  
- `✓✓✓✓✓` **** — 0.6% of jets, neuron 1.38, formula right for 79%.  
- `✓✓✓✓✓` **** — 0.1% of jets, neuron 5.79, formula right for 66%.  
- `✓✓✓✓✓` **** — 0.1% of jets, neuron 10.25, formula right for 67%.  
