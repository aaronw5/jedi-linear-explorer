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

Combinations of its strongest if-statements (1: `width < 0.0087`; 2: `e2_sq < 0.0081`; 3: `max_dr < 0.25`; 4: `z_7 < 0.054`; 5: `log_sum_pt > 6.6`; 6: `log_sum_pt > 6.4`):

- `✓✓✓✓✓✓` **High-pT narrow jets, soft tail** — 33.7% of jets, neuron 0.83, formula right for 69%. A third of all jets: a mixture of q, W and Z (none reaching 35%) with some gluons; below-average mass, narrow, high total pT with a leading particle carrying about 41% of it and a soft 8th particle; pT mostly at the core. All six tests pass: the narrowness and soft-8th-particle penalties are balanced by the e2_sq bonus and both high-pT bonuses, leaving a moderate value that adds a little to the g and Z scores. The formula calls them q and is right about 69% of the time.
- `✓✓✓···` **Soft, narrow gluon-leaning jets** — 12.9% of jets, neuron 0.36, formula right for 55%. Mostly g (38%) with W, Z, t and quarks: light (about 25 GeV), narrower than average, low total pT (about 514 GeV) with the pT evenly shared and a relatively hard 8th particle. Only the e2_sq bonus and the two narrowness penalties pass, so the neuron is small and on in about a third of jets, adding a little to g. The formula calls them g but is right only about 55% of the time.
- `✓✓✓··✓` **Mid-pT narrow mixed jets** — 12.5% of jets, neuron 0.55, formula right for 62%. A mixture of W, Z and g (each around 25-30%) plus quarks; mass about 32 GeV, narrow, total pT a bit below average with evenly shared pT and a hard 8th particle. As in the previous pattern plus the lower pT bonus, giving a value around 0.5 that slightly raises g and Z. The formula calls them W and is right about 62% of the time.
- `✓✓✓✓·✓` **Mid-pT narrow jets, soft tail** — 8.7% of jets, neuron 0.27, formula right for 54%. A broad mixture (W, Z, g, q and some t, none above 30%); mass about 33 GeV, narrow, total pT near average with a soft 8th particle. The soft-8th-particle penalty joins the narrowness penalties and only the lower pT bonus helps, so the neuron is zero in about two-thirds of these jets and barely touches the scores. The formula calls them W and is right only about 54% of the time.
- `✓✓✓·✓✓` **High-pT jets with hard tail** — 7.0% of jets, neuron 1.98, formula right for 63%. A mixture led by gluons (31%) with W, Z and quarks; mass about 31 GeV, narrow, high total pT shared unusually evenly, with a hard 8th particle (about 53 GeV). Both pT bonuses and the e2_sq bonus pass while the 8th particle is not soft, so the neuron is high (about 2) and clearly raises the g score and somewhat the Z score. The formula calls them g and is right about 63% of the time.
- `··✓···` **Wide, soft top jets** — 6.6% of jets, neuron 1.05, formula right for 75%. Mostly t (73%) with some gluons: mass about 64 GeV, about three times wider than average, low total pT, radiation spread out to 0.1-0.2. Only the max-ΔR penalty applies, so the neuron stays near its baseline (about 1) and gives a mild push to g and Z. The formula calls them t and is right 75% of the time.
- `······` **Wide, heavy, soft top jets** — 3.7% of jets, neuron 1.03, formula right for 81%. Mostly t (81%): mass about 72 GeV, very wide, low total pT, with the pT spread across the outer rings. No test passes; the neuron sits at its baseline (about 1) and adds a little to g and Z. The formula calls them t and is right 81% of the time.
- `✓✓·✓✓✓` **Very hard, collimated Z-leaning jets** — 2.2% of jets, neuron 0.84, formula right for 61%. Mostly Z (41%) with W and quarks; mass about 53 GeV, narrow, very high total pT with the leading particle carrying nearly half of it and a very soft 8th particle; almost all pT within 0.05 of the axis. Narrow and soft-tailed (strong penalties) but with the largest high-pT bonuses and no max-ΔR penalty, giving a moderate value that adds a little to g and Z. The formula calls them Z and is right about 61% of the time.
- `··✓··✓` **Heavy, wide mid-pT top jets** — 1.8% of jets, neuron 1.90, formula right for 77%. Mostly t (68%) with some gluons and Z: mass about 82 GeV, wide, total pT somewhat below average, radiation spread to 0.1-0.2. Only the max-ΔR penalty and the lower pT bonus pass, so the neuron is high (about 1.9) and raises the g and Z scores for these top jets; other parts of the formula override it: it calls them t and is right 77% of the time.
- `✓✓✓✓··` **Soft, light, narrow gluon-leaning jets** — 1.6% of jets, neuron 0.32, formula right for 50%. Mostly g (39%) with a fifth tops and quarks; light (about 24 GeV), narrow, low total pT with a soft 8th particle. All three narrowness and soft-tail penalties apply against only the e2_sq bonus, so the neuron is zero in most of these jets. The formula calls them g but is right only about half the time (0.495), so this is a poorly separated group.

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

Combinations of its strongest if-statements (1: `LHA > 0.1`; 2: `pt_7 < 54`; 3: `mass < 36`; 4: `lam1 < 0.0057`; 5: `log_sum_pt > 6.3`; 6: `sum_pt < 790`):

- `✓✓··✓✓` **Heavy two/three-prong top-leaning jets** — 19.4% of jets, neuron 0.66, formula right for 77%. Mostly t (46%) with Z and W: mass about 68 GeV, twice the average width, total pT a bit below average, pT mostly in the 0.05-0.1 ring. The large LHA > 0.1 penalty and the pT_7 penalty outweigh the two pT-band bonuses, leaving a small value (about 0.7) that adds only a little to the g score. The formula calls them t and is right 77% of the time.
- `✓✓✓✓✓✓` **Light, narrow gluon/quark jets** — 15.7% of jets, neuron 3.26, formula right for 48%. Mostly g (37%) with many quarks and some W/Z: very light (about 16 GeV), very narrow, average total pT, pT concentrated within 0.05 of the axis. All six tests pass; the λ1 and pT-band bonuses beat the three penalties, so the neuron is high (about 3.3) and strongly raises the g score. The formula calls them g but is right less than half the time (0.482), since many of these are quarks or W/Z.
- `✓✓···✓` **Soft, wide, heavy top jets** — 9.8% of jets, neuron 1.91, formula right for 73%. Mostly t (68%) with some gluons: mass about 61 GeV, three times wider than average, low total pT (about 468 GeV), radiation spread out to 0.1-0.2. The total-pT < 790 bonus is large here and outweighs the LHA and pT_7 penalties, so the neuron is fairly high (about 1.9) and raises the g score even for these tops; the rest of the formula corrects it: it calls them t and is right about 73% of the time.
- `·✓✓✓✓·` **Ultra-collimated high-pT quark jets** — 9.3% of jets, neuron 2.12, formula right for 73%. Mostly q (71%) with some gluons: very light (about 7 GeV), essentially all pT within 0.025 of the axis, very high total pT with a dominant leading particle and a soft 8th particle. LHA is low (no LHA penalty) and the λ1 and lower pT bonuses pass, but the pT is above 790 GeV so that bonus is lost; the neuron is still sizeable (about 2.1) and raises the g score. Other terms dominate: the formula calls them q and is right 73% of the time.
- `✓✓·✓✓✓` **Mid-mass W jets, moderate pT** — 8.9% of jets, neuron 1.47, formula right for 64%. Mostly W (51%) with a quarter Z: mass about 46 GeV, somewhat narrower than average, average pT, pT in the 0.025-0.1 range. The LHA and pT_7 penalties are partly offset by the λ1 and both pT-band bonuses, leaving a moderate value (about 1.5) that raises the g score somewhat. The formula calls them W and is right about 64% of the time.
- `✓✓·✓✓·` **High-pT W jets, hard leader** — 8.6% of jets, neuron 0.83, formula right for 70%. Mostly W (55%) with Z: mass about 55 GeV, narrower than average, high total pT with the leading particle carrying about 43% of it; pT largely within 0.05 of the axis. Above 790 GeV the total-pT bonus is lost, so the penalties nearly cancel the other bonuses and the neuron is small (about 0.8), adding a little to the g score. The formula calls them W and is right 70% of the time.
- `✓✓✓✓✓·` **Light, hard, narrow quark-leaning jets** — 8.3% of jets, neuron 2.37, formula right for 55%. Mostly q (41%) with a quarter gluons and some W/Z: light (about 14 GeV), very narrow, high total pT with a dominant leading particle; pT largely within 0.025. Like pattern 1 but above 790 GeV total pT, so one bonus is lost; the neuron is still high (about 2.4) and raises the g score. The formula calls them q but is right only about 55% of the time.
- `✓✓··✓·` **Heavy high-pT Z jets** — 6.1% of jets, neuron 0.36, formula right for 81%. Mostly Z (57%) with W: mass about 76 GeV, a bit wider than average, high total pT with a hard leading particle; pT in the 0.025-0.1 ring. The LHA and pT_7 penalties nearly cancel the single pT bonus, so the neuron is small (about 0.4) and barely touches the g score. The formula calls them Z and is right 81% of the time.
- `✓✓✓✓·✓` **Light, soft gluon jets** — 5.9% of jets, neuron 4.30, formula right for 55%. Mostly g (53%) with quarks, W and tops: light (about 18 GeV), narrower than average, low total pT (about 470 GeV) shared evenly among the particles. The λ1 bonus and the large total-pT < 790 bonus beat the three penalties, giving the neuron's highest value here (about 4.3) and the strongest push to the g score. The formula calls them g but is right only about 55% of the time, as many quarks land here.
- `·✓✓✓✓✓` **Ultra-collimated gluon/quark jets** — 1.7% of jets, neuron 4.00, formula right for 55%. Mostly g (49%) with nearly as many quarks: extremely light (about 5 GeV), essentially all pT inside 0.025 of the axis, average total pT. No LHA penalty and every bonus passes, so the neuron is high (about 4) and strongly raises the g score. The formula calls them g, but only barely over q, and is right about 55% of the time: gluons and quarks are nearly indistinguishable here.

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

Combinations of its strongest if-statements (1: `girth2 < 0.0088`; 2: `girth2 < 0.013`; 3: `e2 < 0.043`; 4: `LHA > 0.32`; 5: `e2 > 0.028`; 6: `mass_over_sum_pt > 0.065 and n_dr_0_0p05 < 4.9`):

- `✓✓✓···` **Narrow light quark/gluon/boson jets** — 52.3% of jets, neuron 0.08, formula right for 59%. Half of all jets: a mixture of quarks, gluons, W and Z (none reaching 35%); light (about 20 GeV), narrow, with most pT within 0.025 of the axis and a slightly harder leading particle than usual. The two compactness penalties (girth2 < 0.0088 and < 0.013) overwhelm the e2 < 0.043 bonus, so the neuron is zero in nearly all of these jets and does not touch the scores. The formula is right only about 59% of the time here, mostly confusing gluons and quarks.
- `✓✓✓·✓✓` **Compact W jets, mid mass** — 16.0% of jets, neuron 0.11, formula right for 72%. Mostly W (48%) with a third Z: mass about 55 GeV, average width, pT in the 0.05-0.1 ring with little at the core or outside. The compactness penalties and the e2 > 0.028 penalty outweigh the small bonuses, so the neuron is essentially zero (on in about 9% of jets). The formula calls them W and is right about 72% of the time.
- `···✓✓✓` **Wide, heavy top jets** — 13.5% of jets, neuron 6.99, formula right for 83%. Mostly t (81%) with some gluons: mass about 81 GeV, nearly four times the average width, softer total pT, with a large share of the pT at 0.1-0.2 and beyond. Not compact, so no penalty from girth2; the big LHA > 0.32 bonus and the mass/pT bonus beat the e2 > 0.028 penalty, giving a high value (about 7) that strongly lowers the W and Z scores and adds a little to t. The formula calls them t and is right 83% of the time.
- `✓✓✓·✓·` **Narrow W-leaning mid-mass jets** — 4.9% of jets, neuron 0.09, formula right for 59%. Mostly W (39%) with Z and some gluons and tops: mass about 47 GeV, a bit narrower than average, pT mainly 0.025-0.05 from the axis. The compactness penalties outweigh the e2 < 0.043 bonus, so the neuron is essentially zero. The formula calls them W but is right only about 59% of the time.
- `✓✓·✓✓✓` **Z jets with a clean ring** — 3.4% of jets, neuron 0.11, formula right for 83%. Mostly Z (82%): mass about 63 GeV, slightly wider than average, with the pT gathered in a ring 0.05-0.1 from the axis and almost nothing at the core. The LHA and mass/pT bonuses pass but the girth2 < 0.013 and e2 > 0.028 penalties cancel them, so the neuron is zero in most of these jets. The formula calls them Z and is right 83% of the time.
- `·✓·✓✓✓` **Medium-wide top/gluon/Z jets** — 2.4% of jets, neuron 4.15, formula right for 63%. Mostly t (54%) with gluons and Z: mass about 59 GeV, wider than average, somewhat soft, pT in the 0.05-0.2 region. Only one mild compactness penalty applies and the LHA and mass/pT bonuses beat the e2 > 0.028 penalty, so the neuron is high (about 4) and lowers the W and Z scores. The formula calls them t and is right about 63% of the time, with gluons and Z being the usual errors.
- `✓✓··✓✓` **Z/W jets, moderate width** — 1.5% of jets, neuron 0.02, formula right for 66%. Mostly Z (49%) with a third W: mass about 52 GeV, slightly wider than average, pT mostly in the 0.05-0.1 ring. The compactness and e2 > 0.028 penalties outweigh the mass/pT bonus, so the neuron is essentially zero. The formula calls them Z and is right about 66% of the time.
- `✓✓✓··✓` **Hard-leader mixed boson jets** — 1.3% of jets, neuron 1.78, formula right for 66%. A mixture led by Z (39%) with W, t, g and q: mass about 54 GeV, narrower than average, with a hard leading particle carrying about 44% of the pT. The e2 < 0.043 bonus is large here and can beat the compactness penalties, so the neuron is on in about 60% of jets and lowers the W and Z scores. The formula calls them Z and is right about 66% of the time.
- `✓✓✓✓✓✓` **Z jets, pure ring shape** — 1.1% of jets, neuron 0.43, formula right for 75%. Mostly Z (67%) with some tops: mass about 57 GeV, slightly wider than average, with nearly all pT in the 0.05-0.1 ring and none at the core. All six tests pass; the penalties roughly cancel the bonuses and the neuron is zero in most jets, only slightly lowering W and Z. The formula calls them Z and is right 75% of the time.
- `·✓✓✓✓✓` **Lighter wide top/gluon jets** — 0.7% of jets, neuron 7.04, formula right for 64%. Mostly t (59%) with a quarter gluons and some quarks: mass about 55 GeV, wider than average, pT mainly in the 0.05-0.1 ring. Only the mild girth2 < 0.013 penalty applies against the LHA, e2 and mass/pT bonuses, so the neuron is very high (about 7) and strongly lowers the W and Z scores. The formula calls them t and is right about 64% of the time.

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

Combinations of its strongest if-statements (1: `e2_sq < 0.017`; 2: `girth < 0.13`; 3: `girth2 > 0.0034`; 4: `tau21 < 0.24`; 5: `C2 > 0.013`; 6: `tau21 < 0.26 and lam2 < 0.0013`):

- `✓✓✓✓✓✓` **Two-prong boson/top jets, low τ21** — 26.9% of jets, neuron 7.17, formula right for 69%. Mostly Z (36%) with W and a fifth tops: mass about 56 GeV, a bit wider than average, pT mostly 0.025-0.1 from the axis; average pT sharing. All six tests pass; the e2_sq, girth, girth2 and τ21 bonuses outweigh the C2 and τ21-λ2 penalties, giving about 7.2, which raises the t and Z scores and lowers q. The formula splits them between W and Z and is right about 69% of the time.
- `✓✓····` **Pencil-thin quark/gluon jets** — 23.1% of jets, neuron 6.79, formula right for 60%. Mostly q (43%) with a third gluons: very light (about 6 GeV), extremely collimated with most pT inside 0.025 of the axis. Only the e2_sq and girth bonuses pass (too thin for the girth2 bonus) but they are large, so the neuron is still high (about 6.8), raising t and Z and lowering q; the rest of the formula overrides it: it calls them q and is right about 60% of the time.
- `✓✓··✓·` **Light narrow quark/gluon jets** — 14.0% of jets, neuron 5.73, formula right for 58%. Mostly q (36%) with nearly as many gluons and some W: light (about 20 GeV), narrow, with a slightly hard leading particle and most pT within 0.05 of the axis. The e2_sq and girth bonuses minus the C2 penalty give about 5.7. The formula calls them g, though quarks are slightly more common, and is right only about 58% of the time.
- `✓✓✓·✓·` **Mid-mass jets, all classes mixed** — 9.0% of jets, neuron 4.98, formula right for 61%. A mixture of t, Z, W and g (each around 20-30%): mass about 48 GeV, a bit wider than average, soft total pT, pT mostly 0.025-0.1 from the axis. The girth2 bonus joins the e2_sq and girth bonuses, but a large C2 penalty pulls the value down to about 5, still raising t and Z. The formula spreads its calls over t, Z and W and is right about 61% of the time.
- `✓✓✓✓·✓` **Clean two-prong W/Z jets** — 8.0% of jets, neuron 9.42, formula right for 80%. W and Z bosons in nearly equal parts: mass about 62 GeV, about average width, with most pT in a ring 0.05-0.1 from the axis. The large τ21 < 0.24 bonus plus the width bonuses, with no C2 penalty, give the neuron's highest value (about 9.4), raising the t and Z scores and lowering q. The formula calls them W and is right about 80% of the time.
- `··✓·✓·` **Very wide, heavy top jets** — 4.6% of jets, neuron 0.23, formula right for 92%. Mostly t (93%): mass about 85 GeV, over four times wider than average, softer, with radiation spread far from the axis. Too wide for the e2_sq and girth bonuses; the big girth2 bonus is eaten by the C2 penalty and the negative baseline, so the neuron is zero in nearly all of these jets. The formula calls them t and is right 92.5% of the time.
- `✓✓·✓✓✓` **Narrow low-τ21 mixed jets** — 4.1% of jets, neuron 4.80, formula right for 51%. A mixture led by W (34%) with quarks, gluons and Z: mass about 35 GeV, narrow, pT largely within 0.05 of the axis with a slightly hard leader. The e2_sq, girth and τ21 bonuses outweigh the two penalties, giving about 4.8. The formula calls them W but is right only about half the time (0.507).
- `··✓✓✓✓` **Wide top jets with low τ21** — 2.1% of jets, neuron 3.73, formula right for 68%. Mostly t (63%) with a quarter gluons: mass about 87 GeV, very wide, soft, pT spread out to 0.1-0.2 and beyond. The girth2 and τ21 bonuses outweigh the penalties, so the neuron is fairly high (about 3.7) and raises the t and Z scores. The formula calls them t and is right about 68% of the time, the gluons being the main errors.
- `✓✓·✓·✓` **Light gluon/quark low-τ21 jets** — 1.6% of jets, neuron 5.88, formula right for 50%. Mostly g (39%) with a third quarks: light (about 26 GeV), narrow, pT concentrated 0.025-0.05 from the axis. The e2_sq, girth and τ21 bonuses beat the τ21-λ2 penalty, giving about 5.9. The formula calls them g but is right only about half the time (0.495).
- `·✓✓·✓·` **Wide, heavy top jets** — 1.3% of jets, neuron 0.15, formula right for 91%. Mostly t (92%): mass about 80 GeV, wider than average with some pT at the core as well as far out; soft total pT. The girth2 bonus is cancelled by the C2 penalty and baseline, so the neuron is zero in almost all of these jets. The formula calls them t and is right 91% of the time.

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

Combinations of its strongest if-statements (1: `width < 0.0061`; 2: `mass_over_sum_pt < 0.076`; 3: `mass_over_sum_pt_sq < 0.0033`; 4: `mass < 55 and centroid_offset < 0.026`; 5: `girth < 0.055`; 6: `mass < 43 and centroid_offset < 0.027`):

- `✓✓✓✓✓✓` **Light, narrow quark/gluon jets** — 37.6% of jets, neuron 9.70, formula right for 60%. The largest group (38% of jets), mostly q with a third gluons: light (about 13 GeV), very narrow, most pT inside 0.025 of the axis, average total pT. All tests pass and the huge width < 0.0061 bonus dominates, so the neuron is very high (about 9.7), strongly raising the q and g scores and lowering W and Z. The formula calls them q and is right about 60% of the time, as gluons and quarks stay mixed.
- `······` **Wide, heavy top/Z jets** — 28.2% of jets, neuron 0.93, formula right for 79%. Mostly t (53%) with a quarter Z: mass about 72 GeV, wider than average, somewhat softer total pT, pT spread out to 0.05-0.2. No test passes; the neuron is small (zero in about 70% of these jets) and only mildly raises the q and g scores. The formula calls them t and is right 79% of the time.
- `✓✓····` **Mid-mass W jets, average width** — 5.1% of jets, neuron 0.92, formula right for 72%. Mostly W (53%) with Z: mass about 55 GeV, a bit narrower than average, pT in the 0.025-0.1 ring. The width bonus and the mild mass/pT penalty pass, leaving the neuron around 0.9 with a small push towards q and g. The formula calls them W and is right about 72% of the time.
- `✓✓✓·✓·` **Light jets with ring-shaped pT** — 4.7% of jets, neuron 1.35, formula right for 44%. A mixture of Z, g and W (each 22-29%) with some quarks: light (about 16 GeV) and narrow, but with most pT 0.025-0.05 from the axis rather than at the core. The big width bonus is largely cancelled by the mass/pT and girth penalties, leaving a moderate value that nudges q and g up. The formula calls them g but is right less than half the time (0.439): a badly confused group.
- `✓✓·✓··` **Compact mid-mass W jets** — 4.4% of jets, neuron 1.53, formula right for 73%. Mostly W (64%) with Z: mass about 49 GeV, a bit narrower than average, pT in the 0.025-0.1 ring. Width and the mass-and-centred bonuses pass against a mild mass/pT penalty, giving about 1.5 and a small push to the q and g scores. The formula calls them W and is right about 73% of the time.
- `···✓··` **Soft, medium-wide Z/W/top jets** — 4.2% of jets, neuron 0.20, formula right for 64%. Mostly Z (40%) with W and tops: mass about 50 GeV, a bit wider than average, low total pT with evenly shared pT, mostly in the 0.05-0.1 ring. Only the small mass-and-centred bonus passes; the neuron is zero in most jets and barely matters. The formula calls them Z and is right about 64% of the time.
- `✓✓·✓·✓` **Soft, light W-leaning jets** — 2.4% of jets, neuron 3.80, formula right for 53%. Mostly W (47%) with gluons, Z and tops: mass about 37 GeV, a bit narrower than average, low total pT with evenly shared pT, mostly 0.05-0.1 from the axis. The width and mass-and-centred bonuses win over the small penalties, so the neuron is high (about 3.8) and pushes the q and g scores up for these mostly-W jets. The formula calls them W but is right only about 53% of the time.
- `✓✓·✓✓·` **Narrow W/Z, hard leader** — 2.0% of jets, neuron 1.07, formula right for 63%. Mostly W (44%) with a third Z: mass about 50 GeV, narrower than average, pT concentrated 0.025-0.05 from the axis. The width bonus outweighs the mass/pT and girth penalties, leaving about 1.1 with a small push to q and g. The formula calls them W and is right about 63% of the time.
- `✓✓··✓·` **Very hard, heavier W/Z jets** — 2.0% of jets, neuron 0.46, formula right for 72%. Mostly W (46%) with nearly as many Z: mass about 61 GeV, narrower than average, very high total pT with a leading particle carrying nearly half; pT largely within 0.05. The width bonus is cut back by the mass/pT and girth penalties, so the neuron is on in only about 40% of these jets and has little effect. The formula calls them W, just ahead of Z, and is right about 72% of the time.
- `✓✓✓✓✓·` **High-pT narrow W jets** — 1.6% of jets, neuron 1.95, formula right for 60%. Mostly W (49%) with Z: mass about 47 GeV, narrow, very high total pT with a hard leading particle; pT within 0.05 of the axis. The large width bonus and small mass-related bonuses beat the penalties, giving about 2 and a push to the q and g scores. The formula calls them W and is right about 60% of the time.

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

Combinations of its strongest if-statements (1: `lam2 < 0.0034`; 2: `mass_over_sum_pt < 0.1`; 3: `girth2 > 0.0085`; 4: `e2 < 0.037`; 5: `girth2 < 0.0017`; 6: `lam1 > 0.0085`):

- `✓✓·✓✓·` **Very light, collimated quark/gluon jets** — 35.0% of jets, neuron 0.50, formula right for 60%. Mostly q (43%) with a third gluons: very light (about 10 GeV), extremely collimated, most pT inside 0.025 of the axis. The mass/pT bonus is offset by the λ2, e2 and very-compact penalties, so the neuron is small (about 0.5), slightly raising t and lowering q. The formula calls them q and is right about 60% of the time.
- `✓✓·✓··` **Mid-mass W/Z jets** — 31.0% of jets, neuron 1.48, formula right for 61%. Mostly W (37%) with a third Z plus gluons: mass about 45 GeV, narrower than average, pT mostly 0.025-0.1 from the axis. The mass/pT bonus and the λ2 and e2 penalties leave a moderate value (about 1.5) that raises t and lowers q. The formula calls them W and is right about 61% of the time.
- `✓✓····` **Ring-shaped Z/W jets** — 13.8% of jets, neuron 1.21, formula right for 75%. Mostly Z (48%) with W: mass about 57 GeV, about average width, pT gathered in the 0.05-0.1 ring. Only the λ2 penalty and a small mass/pT bonus pass, leaving about 1.2 with a modest push to t and away from q. The formula calls them Z and is right 75% of the time.
- `✓·✓··✓` **Wide, heavy top jets** — 11.2% of jets, neuron 3.02, formula right for 76%. Mostly t (74%) with gluons: mass about 77 GeV, three times wider than average, softer total pT, pT spread out to 0.1-0.2. The large girth2 bonus beats the λ1 and λ2 penalties, so the neuron is high (about 3) and clearly raises the t score while lowering q. The formula calls them t and is right about 75% of the time.
- `··✓··✓` **Very wide, heavy top jets** — 4.7% of jets, neuron 9.86, formula right for 94%. Mostly t (93%): mass about 83 GeV, four times wider than average, soft, with the pT spread well away from the axis. The λ2 penalty is absent and the girth2 bonus is large, so the neuron reaches its highest value (about 9.9), strongly raising the t score and lowering q. The formula calls them t and is right 93% of the time.
- `✓✓✓··✓` **Medium-wide top/Z jets** — 2.2% of jets, neuron 1.00, formula right for 65%. Mostly t (45%) with a third Z and some gluons: mass about 56 GeV, wider than average, softer, pT mostly 0.05-0.2 from the axis. The λ2 and λ1 penalties roughly cancel the girth2 and mass/pT bonuses, giving about 1 and a mild push to t. The formula calls them t and is right about 65% of the time, often confusing them with Z.
- `✓✓✓✓·✓` **Medium-wide top/gluon mixture** — 0.9% of jets, neuron 0.86, formula right for 57%. Mostly t (50%) with many gluons and quarks: mass about 52 GeV, wider than average, pT mostly in the 0.05-0.1 ring. Bonuses and penalties nearly cancel, so the neuron is small and off in many jets, giving a slight push to t. The formula calls them t but is right only about 58% of the time, the gluons and quarks being misread as tops.
- `✓✓✓···` **Rare Z/top medium jets** — 0.5% of jets, neuron 1.82, formula right for 65%. A rare mix, mostly Z (39%) with nearly as many tops and some gluons: mass about 52 GeV, somewhat wider than average, soft. The λ2 penalty is outweighed by the intercept and small bonuses, giving about 1.8, which pushes the t score up. The formula calls them Z and is right about 65% of the time.
- `✓·✓✓·✓` **Rare heavy top/quark/gluon jets** — 0.3% of jets, neuron 1.56, formula right for 55%. A rare mix, mostly t (58%) with quarks and gluons: mass about 73 GeV, wider than average, a fairly hard leading particle. The girth2 bonus roughly balances the λ1 and λ2 penalties, giving about 1.6 with a push to t. The formula calls them t but is right only about 55% of the time.
- `✓✓✓✓··` **Rare lighter top jets** — 0.2% of jets, neuron 2.98, formula right for 72%. A rare group, mostly t (73%) with gluons: mass about 50 GeV, a bit wider than average, pT mostly in the 0.05-0.1 ring. The small bonuses and the intercept outweigh the λ2 and e2 penalties, so the neuron is around 3 and clearly raises the t score. The formula calls them t and is right about 72% of the time.

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

Combinations of its strongest if-statements (1: `width < 0.0085`; 2: `centroid_offset < 0.04`; 3: `girth < 0.089`; 4: `sum_pt_top5 < 690`; 5: `planar_flow < 0.27`; 6: `e2_sq < 0.0062`):

- `✓✓✓✓✓✓` **Compact, centred W-leaning jets** — 24.0% of jets, neuron 4.16, formula right for 58%. Mostly W (38%) with Z, gluons and quarks: mass about 34 GeV, narrower than average, slightly soft total pT, pT spread over 0-0.1 from the axis. All six tests pass; the width, centroid, top-5 pT and planar-flow bonuses outweigh the girth and e2_sq penalties, giving about 4.2 and a clear push to the W score. The formula calls them W but is right only about 58% of the time.
- `✓✓✓✓·✓` **Light, narrow gluon jets** — 16.3% of jets, neuron 3.26, formula right for 55%. Mostly g (46%) with a quarter quarks: light (about 15 GeV), narrow, slightly soft, pT largely within 0.025 of the axis. Everything passes except low planar flow; the big width bonus wins, so the neuron is high (about 3.3) and raises the W score even for these gluons. Other terms override it: the formula calls them g, but is right only about 55% of the time.
- `✓✓✓·✓✓` **High-pT, narrow W jets** — 13.1% of jets, neuron 4.59, formula right for 67%. Mostly W (41%) with Z and quarks: mass about 43 GeV, narrow, high total pT with a leading particle carrying about 43%; pT within 0.05 of the axis. The width, centroid and planar-flow bonuses pass (the top-5 pT test fails at this pT), giving about 4.6 and a strong push to the W score. The formula calls them W and is right about 67% of the time.
- `✓✓✓··✓` **Ultra-collimated high-pT quark jets** — 12.3% of jets, neuron 3.72, formula right for 69%. Mostly q (61%) with gluons: very light (about 10 GeV), almost all pT inside 0.025 of the axis, high total pT with a hard leading particle. The large width and centroid bonuses beat the girth and e2_sq penalties, so the neuron is high (about 3.7) and raises the W score for these quark jets; the rest of the formula overrides it: it calls them q and is right about 69% of the time.
- `✓✓✓✓✓·` **Ring-shaped Z jets, average pT** — 7.7% of jets, neuron 3.70, formula right for 72%. Mostly Z (59%) with W and tops: mass about 57 GeV, a bit wider than average, pT concentrated in the 0.05-0.1 ring. Five bonuses pass and only a weak girth penalty applies, giving about 3.7 and a push to the W score. The formula still calls them Z and is right about 72% of the time.
- `·✓·✓✓·` **Wide, heavy top jets** — 6.7% of jets, neuron 0.24, formula right for 72%. Mostly t (67%) with gluons: mass about 75 GeV, three times wider than average, softer, radiation spread out to 0.1-0.2. Too wide for the width bonus; the centroid, top-5 pT and planar-flow bonuses are not enough to lift the neuron, which is zero in most of these jets. The formula calls them t and is right about 72% of the time.
- `·✓·✓··` **Very wide, heavy top jets** — 4.4% of jets, neuron 0.03, formula right for 89%. Mostly t (88%): mass about 81 GeV, very wide, soft, pT spread far from the axis. Only the centroid and top-5 pT bonuses pass; the neuron stays at zero and does not matter. The formula calls them t and is right 89% of the time.
- `···✓··` **Wide top jets, off-centre pT** — 3.1% of jets, neuron 0.00, formula right for 88%. Mostly t (89%): mass about 69 GeV, very wide, soft, with the pT centroid away from the axis and radiation spread to 0.1-0.2. Only the top-5 pT bonus passes, which is not enough; the neuron is zero here. The formula calls them t and is right 88% of the time.
- `···✓✓·` **Wide top/gluon jets, off-centre** — 2.9% of jets, neuron 0.03, formula right for 70%. Mostly t (67%) with a fifth gluons: mass about 69 GeV, very wide, soft, off-centre pT. The top-5 pT and planar-flow bonuses pass but the neuron stays zero. The formula calls them t and is right about 70% of the time, with gluons the usual errors.
- `✓✓✓·✓·` **Heavy high-pT Z jets** — 2.6% of jets, neuron 4.80, formula right for 87%. Mostly Z (79%) with some W: mass about 74 GeV, a bit wider than average, high total pT with a hard leading particle, pT in the 0.025-0.1 ring. The width, centroid and planar-flow bonuses pass with only a small girth penalty, giving the neuron's highest value (about 4.8) and a strong push to the W score; the formula still calls them Z and is right 87% of the time.

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

Combinations of its strongest if-statements (1: `girth < 0.15`; 2: `lam1 < 0.015`; 3: `width < 0.0076`; 4: `e2 < 0.049`; 5: `lam1 < 0.0062`; 6: `girth < 0.14 and log_sum_pt < 6.8`):

- `✓✓✓✓✓✓` **Compact jets of all kinds** — 53.2% of jets, neuron 6.23, formula right for 58%. Half of all jets: a mixture of W, gluons, quarks and Z (none reaching 35%) with few tops; mass about 27 GeV, narrower than average, pT largely within 0.05 of the axis. All six tests pass; the girth < 0.15 bonus dominates, so the neuron is high (about 6.2) and strongly lowers the t score, while slightly raising W and Z. The formula calls them W but is right only about 58% of the time.
- `✓✓✓✓✓·` **Very hard, collimated quark jets** — 13.8% of jets, neuron 7.89, formula right for 70%. Mostly q (45%) with W, gluons and Z: mass about 24 GeV, very narrow, very high total pT with a hard leading particle; pT mostly inside 0.025. The high pT removes the last penalty, so the neuron reaches its highest value (about 7.9) and pushes the t score down hardest. The formula calls them q and is right 70% of the time.
- `✓✓·✓·✓` **Medium-wide Z/top jets** — 8.0% of jets, neuron 3.04, formula right for 72%. Mostly Z (41%) with nearly as many tops: mass about 59 GeV, wider than average, pT mostly in the 0.05-0.1 ring. The girth and λ1 bonuses pass but not the narrowest λ1 one, so the neuron is about 3, lowering the t score. The formula calls them Z and is right about 72% of the time.
- `✓✓✓✓·✓` **Z/W jets, moderate width** — 7.7% of jets, neuron 3.92, formula right for 71%. Mostly Z (55%) with a quarter W: mass about 57 GeV, about average width, pT concentrated 0.05-0.1 from the axis. The girth and λ1 bonuses minus small penalties give about 3.9, lowering the t score and slightly raising W and Z. The formula calls them Z and is right 71% of the time.
- `✓····✓` **Wide, heavy top jets** — 4.6% of jets, neuron 0.51, formula right for 82%. Mostly t (82%) with gluons: mass about 78 GeV, three times wider than average, soft. Only the girth bonus and a small penalty pass, giving about 0.5 and a slight pull down on t. The formula calls them t and is right 82% of the time.
- `······` **Very wide, heavy top jets** — 4.5% of jets, neuron 0.03, formula right for 82%. Mostly t (80%) with gluons: mass about 88 GeV, about five times wider than average, soft, radiation far from the axis. No test passes and the neuron is zero. The formula calls them t and is right about 82% of the time.
- `✓✓···✓` **Medium-wide top jets** — 4.4% of jets, neuron 2.05, formula right for 75%. Mostly t (68%) with gluons and Z: mass about 64 GeV, twice the average width, pT spread over 0.05-0.2. The girth and λ1 < 0.015 bonuses give about 2, lowering the t score for these tops; the rest of the formula calls them t and is right about 75% of the time.
- `✓·····` **Wide, heavy top jets** — 1.8% of jets, neuron 0.12, formula right for 86%. Mostly t (84%): mass about 85 GeV, nearly four times wider than average, soft, radiation spread out to 0.1-0.2. Only the small girth bonus passes and the neuron is zero in most jets. The formula calls them t and is right 86% of the time.
- `✓✓✓✓··` **Heavy, very hard Z jets** — 0.7% of jets, neuron 4.49, formula right for 84%. Mostly Z (78%) with some W: mass about 78 GeV, average width, very high total pT with a hard leading particle. Girth, λ1 and width tests give about 4.5, strongly lowering the t score and slightly raising W and Z. The formula calls them Z and is right 84% of the time.
- `✓··✓·✓` **Rare wide top/gluon jets** — 0.4% of jets, neuron 0.27, formula right for 62%. Mostly t (62%) with a quarter gluons: mass about 67 GeV, wide, soft, pT spread 0.05-0.2. The girth bonus is mostly cancelled by two penalties; the neuron is on in about 40% of jets and has little effect. The formula calls them t and is right about 62% of the time.

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

Combinations of its strongest if-statements (1: `girth2 < 0.013`; 2: `lam1 > 0.0042`; 3: `girth < 0.087`; 4: `width < 0.0061`; 5: `lam1 > 0.0025`; 6: `e2 < 0.043`):

- `✓·✓✓·✓` **Light, narrow quark/gluon jets** — 39.8% of jets, neuron 0.00, formula right for 58%. Two in five jets, mostly q (40%) with a third gluons: light (about 12 GeV), very narrow, pT mostly inside 0.025 of the axis. The girth2 and e2 bonuses are cancelled by the girth and width penalties, so the neuron is zero. The formula calls them q, barely ahead of g, and is right about 58% of the time.
- `✓✓✓✓✓✓` **Mid-mass W two-prong jets** — 14.9% of jets, neuron 0.64, formula right for 70%. Mostly W (54%) with a quarter Z: mass about 52 GeV, a bit narrower than average, pT mostly 0.025-0.1 from the axis. All six tests pass and nearly cancel, so the neuron is on in about 40% of these jets and slightly lowers the W score and raises Z. The formula calls them W and is right 70% of the time.
- `·✓··✓·` **Wide, heavy top jets** — 14.0% of jets, neuron 0.33, formula right for 83%. Mostly t (81%) with gluons: mass about 80 GeV, nearly four times wider than average, soft, radiation spread to 0.1-0.2. The huge λ1 > 0.0042 bonus is largely cancelled by the λ1 > 0.0025 penalty and the baseline, so the neuron is small. The formula calls them t and is right 83% of the time.
- `✓✓✓·✓✓` **Z-leaning medium-width jets** — 11.5% of jets, neuron 1.67, formula right for 70%. Mostly Z (48%) with W and tops: mass about 58 GeV, about average width, pT mostly in the 0.05-0.1 ring. The girth2 and λ1 bonuses beat the penalties, giving about 1.7, which lowers the W score and raises Z. The formula calls them Z and is right 70% of the time.
- `✓·✓✓✓✓` **Narrow W-leaning mixed jets** — 10.0% of jets, neuron 0.35, formula right for 55%. Mostly W (42%) with Z, gluons and quarks: mass about 40 GeV, narrower than average, pT mostly 0.025-0.05 from the axis. The girth and width penalties cancel the bonuses, so the neuron is zero in most jets. The formula calls them W but is right only about 55% of the time.
- `✓✓··✓·` **Ring-shaped Z/top jets** — 4.4% of jets, neuron 1.84, formula right for 73%. Mostly Z (48%) with a third tops: mass about 61 GeV, wider than average, pT concentrated 0.05-0.2 from the axis. The λ1 > 0.0042 bonus is large and the girth/width penalties are absent, giving about 1.8, which lowers the W score and raises Z. The formula calls them Z and is right about 73% of the time.
- `✓✓✓·✓·` **Z jets, moderate width** — 3.3% of jets, neuron 1.67, formula right for 71%. Mostly Z (58%) with W and tops: mass about 57 GeV, a bit wider than average, pT mostly in the 0.05-0.1 ring. The girth2 and λ1 bonuses outweigh the penalties, giving about 1.7, which lowers W and raises Z. The formula calls them Z and is right 71% of the time.
- `✓✓··✓✓` **Lighter top/gluon ring jets** — 1.1% of jets, neuron 0.81, formula right for 62%. Mostly t (52%) with a quarter gluons: mass about 51 GeV, wider than average, pT concentrated in the 0.05-0.1 ring. Bonuses minus the λ1 > 0.0025 penalty give about 0.8 (on in under half), lowering W a little. The formula calls them t and is right about 62% of the time.
- `·✓··✓✓` **Rare wide top/gluon jets** — 0.6% of jets, neuron 0.14, formula right for 65%. Mostly t (65%) with gluons: mass about 59 GeV, over twice the average width, pT spread over 0.05-0.2. The λ1 bonus is cancelled by the λ1 > 0.0025 penalty and the baseline, so the neuron is zero in most jets. The formula calls them t and is right about 65% of the time.
- `·✓✓·✓·` **Rare heavy top jets, hard core** — 0.2% of jets, neuron 0.08, formula right for 83%. Mostly t (85%): mass about 76 GeV, wider than average yet with most pT within 0.05 of the axis. The λ1 bonus is cancelled by the λ1 > 0.0025 and girth penalties, so the neuron is zero in most jets. The formula calls them t and is right 83% of the time.

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

Combinations of its strongest if-statements (1: `girth2 < 0.013`; 2: `girth < 0.078`; 3: `width < 0.0089`; 4: `width < 0.0044`; 5: `mass < 59`; 6: `mass < 22`):

- `✓✓✓✓✓✓` **Very light, pencil-thin quark/gluon jets** — 34.4% of jets, neuron 0.00, formula right for 60%. A third of all jets: a gluon-quark mixture (mostly q, with gluons close behind) that is very light (about 9 GeV) and extremely narrow, with most of the pT inside 0.025 of the axis; pT sharing among particles is like the average jet. All six tests pass: the two narrowness bonuses are more than cancelled by the very-narrow and both light-mass penalties, so the neuron stays at zero and adds nothing to any class score. The formula calls them q only narrowly over g and is right just 60% of the time.
- `✓✓✓✓✓·` **Narrow, moderately light mixed jets** — 15.0% of jets, neuron 1.16, formula right for 54%. A mixture led by W (36%) with sizeable Z, g and q shares; mass around 37 GeV, narrower than average, with the pT concentrated within 0.05 of the axis and a slightly harder leading particle than usual. Everything passes except the lowest-mass penalty, so the compactness bonuses win by a little and the neuron is on in about 60% of these jets, giving a modest push to W and a small pull away from g. The formula mostly calls them W but is right only about half the time (0.541).
- `✓✓✓·✓·` **Medium-width W-like two-prong jets** — 14.3% of jets, neuron 2.44, formula right for 64%. Mostly W with a good share of Z (and some t); mass about 47 GeV, average width, softer total pT than average, with the pT sitting in the 0.05-0.1 ring rather than at the core. The girth2 and width < 0.0089 bonuses pass while the very-narrow penalty does not; only the mild mass < 59 penalty and the girth penalty subtract, so the neuron is almost always on (about 2.4), raising the W score and lowering the g score. The formula calls them W and is right about two-thirds of the time.
- `······` **Wide, heavy top jets** — 12.5% of jets, neuron 0.10, formula right for 84%. Mostly t (83%) with some gluons: heavy (about 85 GeV), roughly four times wider than average, softer in total pT, with the pT spread out to 0.1-0.2 from the axis. No test passes, so only the (small) intercept is left and the neuron is near zero with essentially no effect on the scores. Other parts of the formula handle these: it calls them t and is right 84% of the time.
- `✓✓✓···` **Heavy, compact W/Z jets** — 7.2% of jets, neuron 3.06, formula right for 79%. W and Z bosons in nearly equal parts; mass about 67 GeV, average width, high total pT with a hard leading particle, and pT concentrated between 0.025 and 0.1 from the axis. The three compactness tests pass but none of the width-too-small or light-mass penalties apply, so the neuron is high (about 3) and gives a strong push to the W score and a pull away from g. The formula splits them between Z and W almost evenly and is right about 79% of the time.
- `✓·✓···` **Z-like two-prong ring jets** — 4.7% of jets, neuron 3.12, formula right for 86%. Mostly Z (78%): mass about 68 GeV, slightly wider than average, with the pT gathered in a clear ring 0.05-0.1 from the axis and almost nothing at the core. Only the girth2 and width < 0.0089 bonuses pass and no penalty applies, giving the neuron's highest value here (about 3.1); it pushes the W score up even though these are Z jets, but the rest of the formula overrides that: it calls them Z and is right 86% of the time.
- `✓·✓·✓·` **Softer, lighter Z-leaning jets** — 4.3% of jets, neuron 2.53, formula right for 65%. Mostly Z (50%) with W and t admixtures; mass about 49 GeV, width slightly above average, softer total pT, and again the pT sits in the 0.05-0.1 ring. Same as the previous pattern but the mass < 59 penalty also applies, so the neuron is a little lower (about 2.5) while still raising W and lowering g. The formula calls them Z and is right about two-thirds of the time.
- `····✓·` **Soft, wide, lighter top jets** — 2.3% of jets, neuron 0.34, formula right for 70%. Mostly t (69%) with a quarter gluons; mass about 50 GeV, wide, and clearly softer than average in total pT, with radiation spread out to 0.1-0.2. Only the mass < 59 penalty passes, so the neuron is small (on in under 40% of jets) with little effect on the scores. The formula calls them t and is right 70% of the time; the gluons in this group are the ones it tends to miss.
- `✓···✓·` **Lighter top/gluon medium-wide jets** — 2.2% of jets, neuron 0.86, formula right for 60%. Mostly t (56%) with a quarter gluons and some Z; mass about 47 GeV, wider than average, soft total pT, with pT mainly in the 0.05-0.1 ring. The girth2 bonus passes but the width test fails and the mass < 59 penalty applies, leaving a small value (about 0.9) that nudges W up and g down. The formula calls them t and is right about 60% of the time, so this is a mixed, error-prone group.
- `✓·····` **Heavier, wider top-like jets** — 1.7% of jets, neuron 0.94, formula right for 65%. Mostly t (57%) with gluons, quarks and some Z; mass about 71 GeV, wider than average, total pT near average, pT mostly in the 0.05-0.1 ring. Only the girth2 bonus passes, so the neuron is modest (about 0.9) and slightly raises W and lowers g. The formula calls them t and is right about 65% of the time.

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

Combinations of its strongest if-statements (1: `pt_7 < 53`; 2: `sum_pt_top2 < 540`; 3: `z_7 < 0.071 and centroid_offset < 0.031`; 4: `width < 0.0026 and centroid_offset < 0.025`; 5: `dr_0 < 0.023`; 6: `e2 < 0.034`):

- `✓✓✓···` **Heavy, medium-width boson/top jets** — 18.9% of jets, neuron 0.23, formula right for 77%. A mixture of Z, t and W (each about 30%): mass about 66 GeV, wider than average, pT mostly in the 0.05-0.1 ring. The soft-8th-particle bonus is cancelled by the top-2 pT and centroid penalties, so the neuron is zero in most of these jets. The formula calls them Z and is right 77% of the time.
- `✓✓✓✓✓✓` **Light, narrow quark/gluon jets** — 16.0% of jets, neuron 3.44, formula right for 58%. Mostly q (45%) with many gluons: very light (about 9 GeV), very narrow, nearly all pT within 0.025 of the axis. All six tests pass; the narrow-and-centred and e2 bonuses win, giving about 3.4, which lowers the g and t scores and raises q. The formula calls them q but is right only about 58% of the time.
- `✓✓····` **Soft, wide top jets** — 15.2% of jets, neuron 0.20, formula right for 74%. Mostly t (62%) with some gluons: mass about 64 GeV, nearly three times wider than average, soft total pT, pT spread to 0.1-0.2. The soft-8th bonus is outweighed by the top-2 pT penalty, so the neuron is zero in most jets. The formula calls them t and is right about 74% of the time.
- `✓✓✓··✓` **Mid-mass W/Z jets** — 13.0% of jets, neuron 1.73, formula right for 62%. Mostly W (41%) with a third Z: mass about 44 GeV, narrower than average, most pT 0.025-0.05 from the axis. The pT_7 and e2 bonuses beat the top-2 pT and centroid penalties, giving about 1.7, which lowers g and t. The formula calls them W and is right about 62% of the time.
- `✓·✓✓✓✓` **Very hard one-prong quark jets** — 8.6% of jets, neuron 7.16, formula right for 69%. Mostly q (65%) with some gluons: light (about 12 GeV), extremely collimated, very high total pT with the leading particle carrying about half and a very soft 8th particle. The top-2 pT penalty does not apply and the narrow-and-centred bonus is big, giving the neuron's highest value (about 7.2): it raises q and strongly lowers g and t. The formula calls them q and is right about 69% of the time.
- `✓✓···✓` **Soft, light mixed jets** — 7.5% of jets, neuron 1.95, formula right for 49%. A mixture led by gluons (30%) with Z, t and W: mass about 26 GeV, a bit narrower than average, soft total pT, pT mostly 0.025-0.1 from the axis. The pT_7 and e2 bonuses outweigh the top-2 pT penalty, giving about 2, which lowers the g and t scores. The formula calls them g but is right less than half the time (0.486).
- `✓✓✓✓·✓` **Light, narrow gluon/quark/W mix** — 4.0% of jets, neuron 2.38, formula right for 47%. A mixture of gluons, quarks and W (none reaching 35%): light (about 21 GeV), narrow, pT concentrated 0.025-0.05 from the axis. Most bonuses pass, giving about 2.4 and lowering the g and t scores. The formula calls them g but is right less than half the time (0.473): a hard, confused group.
- `✓·✓··✓` **Very hard-leader W/Z jets** — 3.8% of jets, neuron 3.18, formula right for 73%. Mostly W (44%) with nearly as many Z: mass about 60 GeV, narrower than average, very high total pT with the leading particle carrying over half. No top-2 pT penalty and a strong pT_7 bonus give about 3.2, lowering the g and t scores. The formula calls them W and is right about 73% of the time.
- `✓✓·✓✓✓` **Soft, light, evenly shared gluon jets** — 2.0% of jets, neuron 0.31, formula right for 67%. Mostly g (66%) with quarks: very light (about 10 GeV), narrow, soft total pT shared unusually evenly, with a hard 8th particle. The narrow-and-centred and e2 bonuses are cancelled by the top-2 pT and dr_0 penalties, so the neuron is small and zero in most of these jets. The formula calls them g and is right about 67% of the time.
- `✓·✓···` **Heavy, very hard Z jets** — 1.4% of jets, neuron 0.70, formula right for 82%. Mostly Z (55%) with a quarter W: mass about 80 GeV, a bit wider than average, very high total pT with a hard leading particle. The pT_7 bonus is offset by the centroid penalty, so the neuron is small (on in about half) and slightly lowers g and t. The formula calls them Z and is right about 82% of the time.

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

Combinations of its strongest if-statements (1: `girth2 < 0.0086`; 2: `width < 0.013`; 3: `mass_over_sum_pt > 0.0081`; 4: `lam1 < 0.0078`; 5: `e2 < 0.051`; 6: `girth > 0.083`):

- `✓✓✓✓✓·` **Compact jets of all kinds** — 60.7% of jets, neuron 0.59, formula right for 62%. Most jets (61%): a mixture of W, Z, g and q with few tops; mass about 36 GeV, narrower than average, pT largely within 0.05 of the axis. The girth2, width and mass/pT penalties outweigh the λ1 and e2 bonuses, so the neuron is zero in about two-thirds of these jets and has little effect. The formula calls them W and is right about 62% of the time.
- `✓✓·✓✓·` **Ultra-light, pencil-thin quark jets** — 14.2% of jets, neuron 0.66, formula right for 61%. Mostly q (48%) with gluons: extremely light (about 5 GeV), nearly all pT inside 0.025 of the axis, high total pT. Mass/pT is so small that its penalty does not apply, but the girth2 and width penalties still dominate; the neuron is zero in over half of these jets. The formula calls them q and is right about 61% of the time.
- `··✓··✓` **Wide, heavy top jets** — 13.1% of jets, neuron 4.64, formula right for 83%. Mostly t (82%) with gluons: mass about 81 GeV, nearly four times wider than average, soft, radiation spread to 0.1-0.2. The mass/pT penalty is offset by the girth bonus and the positive baseline, giving about 4.6, which raises the g and q scores and lowers W and Z. The formula calls them t and is right 83% of the time.
- `·✓✓·✓✓` **Medium-wide top/gluon/Z jets** — 2.7% of jets, neuron 4.88, formula right for 63%. Mostly t (50%) with gluons and Z: mass about 57 GeV, wider than average, pT mostly in the 0.05-0.1 ring. Only mild penalties and the girth and e2 bonuses apply, giving about 4.9, which lowers the W and Z scores. The formula calls them t and is right about 63% of the time.
- `✓✓✓✓✓✓` **Ring-shaped Z jets** — 2.4% of jets, neuron 0.87, formula right for 78%. Mostly Z (75%): mass about 59 GeV, a bit wider than average, pT concentrated 0.05-0.1 from the axis. All tests pass and the penalties roughly balance the bonuses, so the neuron is small (on in under half) and slightly lowers W and Z. The formula calls them Z and is right about 78% of the time.
- `✓✓✓·✓✓` **Heavier ring-shaped Z jets** — 1.9% of jets, neuron 0.83, formula right for 86%. Mostly Z (83%) with some tops: mass about 64 GeV, a bit wider than average, pT in the 0.05-0.1 ring. Like the previous pattern but without the λ1 bonus; the neuron is small (about 0.8). The formula calls them Z and is right 86% of the time.
- `··✓·✓✓` **Medium-wide, broad top jets** — 1.6% of jets, neuron 7.36, formula right for 72%. Mostly t (71%) with gluons: mass about 65 GeV, over twice the average width, pT spread over 0.05-0.2. Only the mass/pT penalty applies against the e2 and girth bonuses, giving the neuron's highest value (about 7.4), which strongly lowers W and Z and raises g and q. The formula calls them t and is right about 72% of the time.
- `·✓✓··✓` **Medium-wide top/gluon jets** — 1.1% of jets, neuron 3.88, formula right for 62%. Mostly t (57%) with a quarter gluons: mass about 59 GeV, wider than average, soft, pT spread over 0.05-0.2. Mild penalties and the girth bonus give about 3.9, lowering W and Z. The formula calls them t and is right about 62% of the time.
- `·✓✓·✓·` **Top jets with a hard core** — 0.9% of jets, neuron 4.84, formula right for 63%. Mostly t (55%) with gluons, quarks and Z: mass about 62 GeV, wider than average yet with much of the pT 0.025-0.05 from the axis. Only the width and mass/pT penalties apply against the e2 bonus and baseline, giving about 4.8, which lowers W and Z. The formula calls them t and is right about 63% of the time.
- `✓✓✓·✓·` **Z jets with off-centre pT** — 0.7% of jets, neuron 2.29, formula right for 67%. Mostly Z (55%) with a quarter tops: mass about 61 GeV, a bit wider than average, pT mostly 0.025-0.1 from the axis. The penalties are partly offset, leaving about 2.3, which lowers the W and Z scores and so works against these Z jets. The formula still calls them Z and is right about 67% of the time.

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

Combinations of its strongest if-statements (1: `girth2 > 0.0075`; 2: `girth2 > 0.0015`; 3: `girth2 > 0.0087`; 4: `lam1 < 0.0084`; 5: `max_dr < 0.16`; 6: `mass_over_sum_pt > 0.091`):

- `···✓✓·` **Pencil-thin quark/gluon jets** — 33.1% of jets, neuron 0.16, formula right for 60%. A third of all jets, mostly q (43%) with many gluons: very light (about 9 GeV), extremely narrow, nearly all pT inside 0.025 of the axis. The λ1 and max-ΔR penalties apply and no bonus, so the neuron is zero in most of these jets. The formula calls them q and is right about 60% of the time.
- `·✓·✓✓·` **Mid-mass W two-prong jets** — 29.2% of jets, neuron 2.10, formula right for 63%. Mostly W (44%) with a quarter Z: mass about 45 GeV, a bit narrower than average, pT mostly 0.025-0.1 from the axis. Three moderate penalties but a positive baseline leave about 2.1, raising the Z and W scores. The formula calls them W and is right about 63% of the time.
- `✓✓✓··✓` **Wide, heavy top jets** — 15.4% of jets, neuron 0.15, formula right for 80%. Mostly t (78%) with gluons: mass about 79 GeV, three times wider than average, soft, radiation spread out to 0.1-0.2. The big girth2 > 0.0087 bonus is cancelled by the other two girth2 penalties and the mass/pT penalty, so the neuron is zero in about 90% of these jets. The formula calls them t and is right about 80% of the time.
- `·✓·✓··` **Z/W jets with a stray particle** — 11.9% of jets, neuron 2.46, formula right for 64%. Mostly Z (43%) with a third W: mass about 51 GeV, narrower than average, fairly high total pT with a hard leading particle, but some particle far from the axis. Only the girth2 > 0.0015 and λ1 penalties apply against the baseline, giving about 2.5, which raises the Z score and somewhat the W score. The formula calls them Z and is right about 64% of the time.
- `✓✓·✓✓·` **Clean ring-shaped Z jets** — 3.6% of jets, neuron 5.25, formula right for 82%. Mostly Z (79%): mass about 61 GeV, a bit wider than average, pT concentrated 0.05-0.1 from the axis. The penalties are small here, giving the neuron's highest value (about 5.2) and a strong push to the Z score (and some to W). The formula calls them Z and is right about 82% of the time.
- `✓✓✓·✓✓` **Medium-wide top/Z jets** — 2.9% of jets, neuron 1.88, formula right for 70%. Mostly t (59%) with gluons and Z: mass about 64 GeV, twice the average width, pT mostly 0.05-0.2 from the axis. The girth2 > 0.0087 bonus is outweighed by the other girth2 and mass/pT penalties, leaving about 1.9, which raises the Z score for these top-heavy jets. The formula calls them t and is right about 70% of the time.
- `✓✓·✓··` **Z/top jets, medium width** — 1.0% of jets, neuron 3.23, formula right for 63%. Mostly Z (40%) with a third tops and some gluons: mass about 59 GeV, a bit wider than average, pT largely within 0.1. Mild girth2 and λ1 penalties leave about 3.2, raising Z and W. The formula calls them Z and is right about 63% of the time.
- `···✓··` **Very hard one-prong quark jets** — 0.7% of jets, neuron 0.11, formula right for 66%. Mostly q (68%) with some W and Z: mass about 26 GeV, extremely narrow, very high total pT with the leading particle carrying about half and a very soft 8th particle. Only the λ1 penalty applies, so the neuron is zero in about 90% of these jets. The formula calls them q and is right about 66% of the time.
- `✓✓✓···` **Lighter top/gluon jets** — 0.5% of jets, neuron 0.46, formula right for 63%. Mostly t (57%) with a quarter gluons: mass about 48 GeV, wider than average, pT mostly in the 0.05-0.1 ring. The large girth2 penalties beat the girth2 > 0.0087 bonus, so the neuron is zero in most jets. The formula calls them t and is right about 63% of the time.
- `✓✓✓·✓·` **Light, soft top/gluon jets** — 0.4% of jets, neuron 1.38, formula right for 65%. Mostly t (58%) with gluons: mass about 41 GeV, wider than average, soft, pT spread 0.05-0.2 from the axis. Bonus and penalties nearly cancel, leaving about 1.4 (on in about half) and a small push to Z. The formula calls them t and is right about 65% of the time.

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

Combinations of its strongest if-statements (1: `width < 0.0049`; 2: `girth < 0.063 and width < 0.0055`; 3: `girth2 < 0.0067 and centroid_offset < 0.025`; 4: `max_dr < 0.18 and lam2 < 0.00021`; 5: `C2 < 0.027`; 6: `mass < 29 and centroid_offset < 0.024`):

- `✓✓✓✓✓✓` **Pencil-thin, very light quark/gluon jets** — 28.9% of jets, neuron 3.14, formula right for 61%. Mostly q (46%) with many gluons: very light (about 9 GeV), extremely narrow, with nearly all pT inside 0.025 of the axis; average total pT and pT sharing. All six tests pass: the big width < 0.0049 bonus outweighs the very-narrow and light-mass penalties, so the neuron is high (about 3.1), raising the q and t scores and lowering the W score. The formula calls them q and is right about 61% of the time, the gluons being the main errors.
- `······` **Wide, heavy top jets** — 16.6% of jets, neuron 0.01, formula right for 75%. Mostly t (68%) with some gluons and Z: mass about 70 GeV, three times wider than average, softer total pT, with radiation spread to 0.1-0.2. No test passes and the neuron is zero, so it plays no role here. The formula calls them t and is right 75% of the time.
- `···✓✓·` **Z jets with ring-shaped pT** — 9.4% of jets, neuron 0.01, formula right for 78%. Mostly Z (61%) with a quarter tops: mass about 63 GeV, somewhat wider than average, pT gathered 0.05-0.1 from the axis. The max-ΔR bonus passes but the C2 penalty cancels it, so the neuron is zero and does nothing. The formula calls them Z and is right about 78% of the time.
- `··✓✓✓·` **Compact W two-prong jets** — 8.4% of jets, neuron 0.07, formula right for 77%. Mostly W (67%) with some Z: mass about 57 GeV, about average width, pT concentrated in the 0.05-0.1 ring. Two small bonuses pass but the C2 penalty offsets them, so the neuron is zero in most of these jets with no real effect. The formula calls them W and is right about 77% of the time.
- `✓✓✓···` **Narrow, hard-leader W/Z jets** — 5.2% of jets, neuron 0.49, formula right for 58%. Mostly W (42%) with a third Z and some quarks: mass about 45 GeV, narrower than average, high total pT with the leading particle carrying about 43% of it; pT within 0.05 of the axis. The width bonus passes but the girth penalty and the intercept keep it small; the neuron is on in about 40% of these jets and slightly lowers the W score. The formula calls them W but is right only about 58% of the time.
- `✓✓✓✓✓·` **Narrow W-leaning mixed jets** — 4.5% of jets, neuron 1.42, formula right for 58%. Mostly W (49%) with gluons, Z and quarks: mass about 42 GeV, narrower than average, pT mostly 0.025-0.05 from the axis. Width, girth2 and max-ΔR bonuses beat the girth and C2 penalties, so the neuron is moderate (about 1.4); this lowers the W score and raises t and q, working against these mostly-W jets. The formula still calls them W but is right only 58% of the time.
- `····✓·` **Wide, heavy top-leaning jets** — 4.4% of jets, neuron 0.00, formula right for 75%. Mostly t (63%) with gluons and Z: mass about 72 GeV, over twice the average width, radiation spread out to 0.1-0.2. Only the C2 penalty passes and the neuron is zero, with no effect. The formula calls them t and is right 75% of the time.
- `✓✓·✓✓·` **Light but ringed, confusing mix** — 4.1% of jets, neuron 0.06, formula right for 44%. A mixture of gluons, Z and W (each 22-29%) with some quarks: light (about 11 GeV) and narrow, yet with the pT sitting 0.025-0.05 from the axis rather than at the core. The large width bonus is cancelled by the girth and C2 penalties, so the neuron is zero in most jets. The formula calls them g but is right less than half the time (0.443): this is one of the hardest groups.
- `··✓···` **Mid-mass Z/W jets** — 2.2% of jets, neuron 0.03, formula right for 64%. Mostly Z (43%) with a third W: mass about 51 GeV, around average width, pT mainly 0.025-0.1 from the axis. Only the small girth2 bonus passes and the neuron stays zero. The formula calls them Z and is right about 65% of the time, W being the common confusion.
- `✓✓✓✓··` **Narrow, lighter W jets** — 2.0% of jets, neuron 1.18, formula right for 57%. Mostly W (51%) with gluons, quarks and Z: mass about 39 GeV, narrower than average, pT largely within 0.05 of the axis. Width, girth2 and max-ΔR bonuses pass with only the girth penalty against them, so the neuron is around 1.2, which lowers the W score and raises t. The formula still calls them W but is right only about 57% of the time.

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

Combinations of its strongest if-statements (1: `width < 0.0067`; 2: `lam1 < 0.0067`; 3: `lam1 < 0.0083`; 4: `width < 0.013`; 5: `e2 < 0.024`; 6: `e2 < 0.041`):

- `✓✓✓✓✓✓` **Narrow, light quark/gluon jets** — 48.5% of jets, neuron 0.17, formula right for 59%. Half of all jets: a quark-gluon mixture with some W and Z; light (about 18 GeV), narrow, pT mostly inside 0.025 of the axis. All six tests pass; the large width < 0.0067 and λ1 < 0.0083 penalties cancel the bonuses, so the neuron is zero in most of these jets. The formula calls them q, barely ahead of g, and is right about 59% of the time.
- `✓✓✓✓·✓` **Mid-mass W jets** — 20.0% of jets, neuron 0.32, formula right for 67%. Mostly W (52%) with a quarter Z: mass about 50 GeV, a bit narrower than average, pT mostly 0.025-0.1 from the axis. The narrow-width penalties nearly cancel the bonuses, so the neuron is zero in about 70% of these jets and only slightly lowers the W score. The formula calls them W and is right about 67% of the time.
- `······` **Wide, heavy top jets** — 14.4% of jets, neuron 0.21, formula right for 83%. Mostly t (81%) with gluons: mass about 80 GeV, nearly four times wider than average, soft. No test passes; the neuron is zero in most of these jets. The formula calls them t and is right about 83% of the time.
- `··✓✓··` **Z jets in the width band** — 5.1% of jets, neuron 2.50, formula right for 78%. Mostly Z (74%): mass about 61 GeV, a bit wider than average, pT concentrated in the 0.05-0.1 ring. The width < 0.013 bonus passes without the narrow-width penalty, giving about 2.5, which strongly lowers the W score and slightly raises q. The formula calls them Z and is right about 78% of the time.
- `···✓··` **Medium-wide top/Z jets** — 3.7% of jets, neuron 2.02, formula right for 67%. Mostly t (47%) with Z and gluons: mass about 60 GeV, wider than average, pT spread 0.05-0.2. Only the width < 0.013 bonus passes, giving about 2 and lowering the W score. The formula calls them t and is right about 67% of the time, Z being the usual confusion.
- `··✓✓·✓` **Z jets, lower e2** — 3.5% of jets, neuron 2.31, formula right for 75%. Mostly Z (65%) with some tops: mass about 60 GeV, a bit wider than average, pT mostly 0.025-0.1 from the axis. The width band and e2 bonuses beat the λ1 penalty, giving about 2.3 and lowering the W score. The formula calls them Z and is right 75% of the time.
- `✓✓✓✓··` **Narrow-ish W jets, ring pT** — 1.4% of jets, neuron 0.23, formula right for 71%. Mostly W (69%) with some Z: mass about 51 GeV, about average width, pT concentrated 0.05-0.1 from the axis. The narrow-width and λ1 penalties roughly cancel the bonuses, so the neuron is zero in most jets. The formula calls them W and is right about 71% of the time.
- `···✓·✓` **Medium-wide top/gluon jets** — 1.3% of jets, neuron 2.19, formula right for 57%. Mostly t (53%) with a quarter gluons: mass about 60 GeV, wider than average, pT mostly in the 0.05-0.1 ring. The width band and e2 < 0.041 bonuses give about 2.2, lowering the W score. The formula calls them t but is right only about 57% of the time.
- `·✓✓✓·✓` **Rare Z/top mixture** — 0.6% of jets, neuron 1.65, formula right for 64%. Mostly Z (37%) with nearly as many tops: mass about 51 GeV, a bit wider than average, pT mostly 0.025-0.1 from the axis. The width band, e2 and λ1 < 0.0067 bonuses beat the λ1 penalty, giving about 1.6 and lowering W. The formula calls them Z and is right about 64% of the time.
- `·✓✓✓··` **Rare Z-leaning mixed jets** — 0.6% of jets, neuron 0.75, formula right for 55%. Mostly Z (46%) with W, tops and gluons: mass about 49 GeV, a bit wider than average, soft, pT mostly in the 0.05-0.1 ring. The width band and λ1 bonuses slightly beat the λ1 penalty, giving about 0.75 and lowering W a little. The formula calls them Z but is right only about 55% of the time.

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

- `·····` **Ordinary (not very wide) jets** — 86.5% of jets, neuron 0.00, formula right for 63%. Nearly all jets (86.5%): a mixture of all classes, with tops underrepresented; mass about 34 GeV, narrower than average. No test passes and the neuron is zero, with no effect on any score. The formula calls them W and is right about 63% of the time, so this neuron plays no part here.
- `✓✓✓·✓` **Very wide, soft top jets** — 5.5% of jets, neuron 0.34, formula right for 85%. Mostly t (85%): mass about 74 GeV, four times wider than average, soft total pT, radiation spread far from the axis. The width bonuses pass but the e2 > 0.063 penalty cancels them, so the neuron is zero in about three-quarters of these jets and only slightly lowers the t score. The formula calls them t and is right 85% of the time.
- `✓✓✓✓✓` **Very wide, very heavy top jets** — 3.1% of jets, neuron 1.62, formula right for 86%. Mostly t (83%) with gluons: mass about 106 GeV (above the Z mass), very wide, with radiation spread out to 0.1-0.2. All five tests pass; the width and mass bonuses beat the e2 penalty, giving about 1.6 and lowering the t score. The formula still calls them t and is right 86% of the time.
- `····✓` **Moderately wide top jets** — 2.1% of jets, neuron 0.00, formula right for 77%. Mostly t (78%) with gluons: mass about 67 GeV, over twice the average width, soft. Only the small girth2-λ2 bonus passes and the neuron stays zero. The formula calls them t and is right about 77% of the time.
- `✓···✓` **Wide top jets, high e2** — 1.0% of jets, neuron 0.00, formula right for 79%. Mostly t (78%) with gluons: mass about 68 GeV, wide, soft, pT spread out to 0.1-0.2. The e2 penalty and the small bonus leave the neuron zero. The formula calls them t and is right about 79% of the time.
- `·✓✓·✓` **Very wide, lower-e2 top jets** — 0.8% of jets, neuron 0.24, formula right for 77%. Mostly t (76%) with gluons: mass about 67 GeV, very wide, soft, pT spread out to 0.1-0.2. The width bonuses pass without the e2 penalty but are small, so the neuron is on in under a quarter of these jets, only slightly lowering the t score. The formula calls them t and is right 77% of the time.
- `···✓✓` **Heavy, high-pT top jets** — 0.3% of jets, neuron 0.36, formula right for 80%. Mostly t (72%) with gluons: mass about 102 GeV, wide, higher total pT than average with a hard leading particle. The mass > 91.2 bonus passes but the neuron is on in only about a quarter of these jets, slightly lowering t. The formula calls them t and is right about 80% of the time.
- `···✓·` **Rare heavy, very hard jets** — 0.3% of jets, neuron 0.23, formula right for 60%. A rare mixture, mostly t (43%) with a third gluons and some quarks: mass about 100 GeV, wider than average, very high total pT with a hard leading particle. Only the mass bonus passes; the neuron is zero in most of these jets and barely touches the t score. The formula calls them t, often confusing them with gluons, and is right only about 60% of the time.
- `✓··✓✓` **Heavy wide top jets, high e2** — 0.2% of jets, neuron 0.16, formula right for 83%. Mostly t (81%): mass about 102 GeV, wide, somewhat high total pT, pT spread out to 0.1-0.2. The mass bonus is mostly cancelled by the e2 penalty, so the neuron is zero in most of these jets. The formula calls them t and is right 83% of the time.
- `·✓✓✓✓` **Rare heavy, wide top/gluon jets** — 0.2% of jets, neuron 0.91, formula right for 70%. Mostly t (63%) with a quarter gluons: mass about 102 GeV, very wide, total pT near average. Width and mass bonuses pass without the e2 penalty, giving about 0.9 and lowering the t score. The formula calls them t and is right 70% of the time.
