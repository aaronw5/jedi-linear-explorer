# What each part of the 250-term formula does (8 particles)

*the formula simplified by hand with the training data (main result)*. Validation accuracy 65.18%. Words written by an AI agent from the numbers (60,000 training jets) and checked against them; lines marked *computed* come straight from the numbers. Plots: the page, tab "What each part does".

## Summary

Every jet is placed on 16 scales (each a clipped sum of if-statements on jet-shape quantities), and each class score adds some scales and subtracts others. Tops are recognised by size: the t score subtracts compactness (neuron 13, on which tops sit far below all other types) and adds overall size (neuron 10: e2, width, mass), so it is essentially a jet-width measure. Quarks and gluons both sit high on the narrow-and-light scale (neuron 9), which feeds both of their scores; they are told apart by how the pT is shared among the particles: the g score adds gluon-likeness (neuron 2: even the 8th-hardest particle is hard) and subtracts quark-likeness (neuron 5: pT concentrated in the few hardest particles), while the q score subtracts overall size (neuron 10). W and Z jets sit high on scales for a compact, centred, elongated two-prong jet with mass/pT in the boson window (neurons 7 and 13 feed both boson scores, neurons 0 and 11 only the W score), and both boson scores subtract the broad-off-centre and wide-angle-radiation scales (neurons 6 and 3), on which tops and gluons sit higher. W and Z are split mainly by width: Z jets sit highest on an intermediate-width scale (neuron 14), which the Z score adds and the W score subtracts, and a 'slightly wider than a W' scale (neuron 15) takes a larger share out of the W score than out of the Z score, consistent with the heavier Z opening wider at the same pT.

## The 5 class scores

### score g: gluon: many hard particles, light jet

High for light, fairly narrow jets whose pT is spread over many hard particles; it averages 2.21 for g jets, 1.40 for q and 1.08 for t, and is near zero for W and Z (AUC 0.81 for gluons against the rest).

Adds gluon-likeness (neuron 2, +36%) and narrow-light-ness (neuron 9, +26%), plus smaller amounts of neurons 1 and 6; subtracts quark-likeness (neuron 5, -15%) and, less, the compact two-prong scale (neuron 0) and neuron 4.

*computed:* largest for g (2.21), then q (1.40), then t (1.08), then W (0.18), then Z (0.04); it separates g jets from the rest best (AUC 0.81: large for g)

### score q: quark: narrow, light, small jet

High for narrow, light jets that are small in e2, width and mass; it averages 2.22 for q jets and 1.49 for g, with tops lower (0.32) and W and Z near or below zero (AUC 0.83 for quarks). Gluons are its main confusion.

Mostly adds narrow-light-ness (neuron 9, +49%); subtracts overall size (neuron 10, -18%) and neuron 4 (-16%); adds a little of neuron 6 and of quark-likeness (neuron 5, +5%).

*computed:* largest for q (2.22), then g (1.49), then t (0.32), then W (-0.00), then Z (-0.16); it separates q jets from the rest best (AUC 0.83: large for q)

### score W: W: compact, centred two-prong jet

High for compact, centred, elongated two-prong jets with W-like mass/pT that are not wider than a W; it averages 2.55 for W jets and 0.51 for Z, is near zero for q, slightly negative for g and strongly negative for t (-2.64) (AUC 0.89).

Adds the compact-centred scale (neuron 11, +24%, its largest input), the two-prong scales (neurons 0 and 7) and compactness (neuron 13); subtracts broad off-centre spread (neuron 6), the 'wider than a W' scales (neurons 15 and 14), wide-angle radiation (neuron 3) and a little of neurons 8 and 9.

*computed:* largest for W (2.55), then Z (0.51), then q (0.03), then g (-0.40), then t (-2.64); it separates W jets from the rest best (AUC 0.89: large for W)

### score Z: Z: two-prong jet, wider than a W

High for two-prong jets in the W/Z mass-to-pT window with an intermediate, Z-sized width; it averages 2.31 for Z jets and 1.58 for W (W is its main confusion), is near zero for q and g, and strongly negative for t (-1.93) (AUC 0.85).

Adds the two-prong W/Z-window scale (neuron 7, +27%, its largest input), neuron 4, compactness (neuron 13), the intermediate-width scale (neuron 14) and a little of neuron 1; subtracts broad off-centre spread (neuron 6, -21%), wide-angle radiation (neuron 3) and a little of neurons 9 and 15.

*computed:* largest for Z (2.31), then W (1.58), then q (0.14), then g (-0.16), then t (-1.93); it separates Z jets from the rest best (AUC 0.85: large for Z)

### score t: top: wide, massive jet

High for wide, massive jets: it follows girth, width and e2 with rank correlations of about 0.90. It averages 2.90 for t jets, 0.38 for Z and 0.18 for W, is near zero for g and negative for q (-1.42) (AUC 0.91).

Subtracts compactness (neuron 13, -46%) and adds overall size (neuron 10, +26%); also subtracts quark-likeness (neuron 5) and adds smaller amounts of neurons 4 and 8.

*computed:* largest for t (2.90), then Z (0.38), then W (0.18), then g (-0.01), then q (-1.42); it separates t jets from the rest best (AUC 0.91: large for t)

## The 16 neurons (most important first)

### neuron 2: gluon-likeness: many hard particles (major)

- **What it measures:** Moved up when the 8th-hardest particle is still hard (pT_7 > 30.2 GeV, and more so above 54.2 GeV) and for total pT below 788 GeV, and down for large angularity (LHA > 0.116); overall it falls with jet mass and spread (rank correlation -0.675 with mass). Gluons sit highest (3.79), then quarks (2.72), with W, Z and top jets lower (1.71-2.07).
- *computed — its value:* largest for g (3.79), then q (2.72), then W (2.07), then Z (1.78), then t (1.71); it separates g jets from the rest best (AUC 0.79: large for g)
- **How the class scores use it:** Since gluons sit highest on it, the g score reads it as direct evidence for a gluon: it raises the g score, where it is the largest input (+36%). It does not enter the q, W, Z or t scores.
- *computed — used by:* raises the score of g (+36%); does not (or hardly) enter the score of q, W, Z, t (share of each class score’s average input)

```
z = 3.38
if pt_7 > 30.20: z += 0.173 × (pt_7 − 30.20)
if LHA > 0.116: z += -7.91 × (LHA − 0.116)
if pt_7 < 54.20: z += -0.050 × (54.20 − pt_7)
if sum_pt < 788: z += 0.0056 × (788 − sum_pt)
if z_7 > 0.045: z += -45.70 × (z_7 − 0.045)
if lam1 < 0.0053: z += 267 × (0.0053 − lam1)
if pt_7 > 29.60 and C2 < 0.051: z += -1.91 × (pt_7 − 29.60) × (0.051 − C2)
if log_sum_pt < 6.46: z += 4.86 × (6.46 − log_sum_pt)
if planar_flow < 0.654: z += -0.791 × (0.654 − planar_flow)
if pt_7 > 29.20 and max_dr > 0.075: z += -0.564 × (pt_7 − 29.20) × (max_dr − 0.075)
if log_sum_pt > 6.83: z += 11.40 × (log_sum_pt − 6.83)
if z_7 < 0.018: z += -303 × (0.018 − z_7)
if lam1 < 0.0037 and centroid_offset < 0.0058: z += -32100 × (0.0037 − lam1) × (0.0058 − centroid_offset)
if log_sum_pt > 6.89: z += -13.70 × (log_sum_pt − 6.89)
if girth2 < 4.9e-05: z += -54100 × (4.9e-05 − girth2)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `pt_7 > 30.2`; 2: `LHA > 0.116`; 3: `pt_7 < 54.2`; 4: `sum_pt < 788`; 5: `z_7 > 0.045`; 6: `lam1 < 0.0053`):

- `✓✓✓✓✓·` **medium-width heavy top/Z jets** — 23.9% of jets, neuron 1.73, formula right for 74%. Mostly tops (47%) with Z and W; mass about 63 GeV, about twice the average width, lower total pT (591 GeV) shared evenly with a hard 8th particle, and pT spread out to 0.1 and beyond. The hard-8th-particle and low-pT bonuses are partly cancelled by the angularity, pt_7 and z_7 penalties, giving a value of 1.73 (on 98%) that adds 0.742 to the g score. The formula still calls them t and is right 0.743 of the time.
- `✓✓✓✓✓✓` **light narrow jets, many hard particles** — 19.5% of jets, neuron 3.74, formula right for 53%. A mixture: gluons 34%, W 26%, quarks and Z; light (23.6 GeV), narrow, total pT 618 GeV shared evenly with a hard 8th particle, most pT within 0.05 of the axis. All tests pass, including the small-lam1 bonus, giving the neuron its highest value (3.74) and the largest boost to the g score (1.608). The formula calls them g but is right only 0.531 of the time, since W jets here get pulled toward g.
- `·✓✓··✓` **high-pT, one dominant particle, W-leaning** — 8.0% of jets, neuron 1.45, formula right for 61%. Mostly W (39%) with quarks and Z (25% each); mass about 37 GeV, narrow, high total pT (893 GeV) with one dominant particle (nearly half the pT) and a soft 8th particle. The pt_7 and angularity penalties are offset by the small-lam1 bonus, giving a value of 1.45 (on 90%) and a moderate boost to g. The formula calls them W and is right 0.607 of the time.
- `··✓··✓` **very light pencil-like quark jets** — 7.5% of jets, neuron 1.71, formula right for 76%. Mostly quarks (76%); very light (8.6 GeV), extremely collimated (98% of the pT inside 0.025), highest total pT (952 GeV) with one dominant particle and a soft 8th particle. Only the pt_7 penalty (about -1.8) and the lam1 bonus (about +1.4) pass, leaving a value of 1.71 (on 78%) that adds to the g score. The formula calls them q anyway and is right 0.764 of the time.
- `·✓✓✓·✓` **mid-pT narrow mixed jets** — 4.4% of jets, neuron 2.16, formula right for 47%. A mixture: quarks and W (25% each), Z and gluons; mass about 28 GeV, narrow, total pT 704 GeV with a fairly hard leading particle. The lam1 and low-pT bonuses outweigh the angularity and pt_7 penalties, giving a value of 2.16 that adds 0.927 to the g score. The formula leans W and is right only 0.472 of the time: a confused mixture.
- `·✓✓✓✓·` **wide low-pT top jets** — 3.9% of jets, neuron 2.34, formula right for 70%. Mostly tops (66%) with gluons 21%; mass about 58 GeV, three times the average width, low total pT (472 GeV), pT spread far from the axis. The low-pT bonus (about +1.8) beats the angularity and pt_7 penalties, giving a value of 2.34 that adds about 1.0 to the g score. The formula still calls them t and is right 0.705 of the time.
- `·✓✓···` **heavy high-pT two-prong Z jets** — 3.8% of jets, neuron 0.13, formula right for 81%. Mostly Z (55%) with W 26%; heavy (74.8 GeV), average width, high total pT (884 GeV) with one dominant particle and most pT at 0.025-0.1 from the axis. Only the angularity and pt_7 penalties pass, so the value is small (0.13, on 42%) and barely touches the g score. The formula calls them Z and is right 0.812 of the time.
- `·✓✓✓··` **heavy mid-pT top/Z jets** — 3.8% of jets, neuron 0.57, formula right for 73%. Mostly tops (55%) with Z 21%; heavy (70.2 GeV), about twice the average width, total pT 684 GeV with a fairly hard leading particle, pT spread to 0.1 and beyond. The angularity and pt_7 penalties are only slightly offset by the low-pT bonus, giving a small value (0.57, on 78%). The formula calls them t and is right 0.731 of the time.
- `✓✓✓··✓` **high-pT narrow W-leaning jets** — 3.2% of jets, neuron 2.55, formula right for 60%. Mostly W (40%) with Z, gluons and quarks; mass about 35 GeV, narrow, high total pT (900 GeV) with a moderately hard 8th particle, most pT within 0.05. The hard-8th-particle and lam1 bonuses outweigh the penalties, giving a value of 2.55 that adds about 1.1 to the g score. The formula calls them W and is right 0.603 of the time.
- `✓✓✓·✓✓` **high-pT evenly shared W/gluon jets** — 2.5% of jets, neuron 3.50, formula right for 60%. Mostly W (37%) with gluons 28%; mass about 32 GeV, narrow, high total pT (850 GeV) shared very evenly with a hard 8th particle. The hard-8th-particle bonus is large here (about +2.5), plus the lam1 bonus, giving a high value (3.50) and a large boost to the g score (1.505). The formula calls them W and is right 0.599 of the time; many gluons and W are confused.

### neuron 6: broad, off-centre spread (major)

- **What it measures:** Switched off for narrow jets (girth2 < 0.00862 and width < 0.0133 both push it down) and pushed up for lam1 < 0.00802 and e2 < 0.0508; it follows the offset of the pT centroid from the jet axis and the jet width (rank correlations 0.562 and 0.525). Tops sit far highest (4.60), then gluons (1.82) and quarks (0.84), with Z (0.58) and W (0.20) lowest.
- *computed — its value:* largest for t (4.60), then g (1.82), then q (0.84), then Z (0.58), then W (0.20); it separates t jets from the rest best (AUC 0.83: large for t)
- **How the class scores use it:** Boosted W and Z jets sit lowest on it, so the W and Z scores read a broad, off-centre spread as evidence against a boson: it lowers the W score (-12%) and the Z score (-21%). It raises the g and q scores (among non-top jets a broad spread is more QCD-like than boson-like), and it does not enter the t score although tops sit highest on it; the t score gets its width information from neurons 13 and 10.
- *computed — used by:* raises the score of g (+6%), q (+9%); lowers the score of W (-12%), Z (-21%); does not (or hardly) enter the score of t (share of each class score’s average input)

```
z = 6.56
if girth2 < 0.0086: z += -1680 × (0.0086 − girth2)
if width < 0.013: z += -540 × (0.013 − width)
if lam1 < 0.008: z += 919 × (0.008 − lam1)
if mass_over_sum_pt > 0.0094: z += -53.20 × (mass_over_sum_pt − 0.0094)
if e2 < 0.051: z += 85.70 × (0.051 − e2)
if max_dr > 0.028: z += 14.70 × (max_dr − 0.028)
if girth > 0.087: z += 126 × (girth − 0.087)
if lam2 < 0.00052: z += -2400 × (0.00052 − lam2)
if e2_sq < 0.0033: z += 626 × (0.0033 − e2_sq)
if mass < 46.60 and z_dr_0p05_0p1 < 0.800: z += 0.058 × (46.60 − mass) × (0.800 − z_dr_0p05_0p1)
if centroid_offset > 0.0078 and lam2 < 0.0035: z += 19800 × (centroid_offset − 0.0078) × (0.0035 − lam2)
if log_sum_pt < 6.57 and pt_7 < 45.40: z += 0.343 × (6.57 − log_sum_pt) × (45.40 − pt_7)
if C2 > 0.010: z += -20.80 × (C2 − 0.010)
if mass_over_sum_pt > 0.017 and tau32 < 0.530: z += -68.70 × (mass_over_sum_pt − 0.017) × (0.530 − tau32)
if centroid_offset > 0.021: z += -59.40 × (centroid_offset − 0.021)
if lam2 > 0.0029: z += -1090 × (lam2 − 0.0029)
if C2 > 0.010 and pt_7 > 32.60: z += 2.56 × (C2 − 0.010) × (pt_7 − 32.60)
if log_sum_pt < 6.71 and z_7 < 0.049: z += 833 × (6.71 − log_sum_pt) × (0.049 − z_7)
if e2 < 0.050 and z_dr_0p1_0p2 > 0.159: z += 766 × (0.050 − e2) × (z_dr_0p1_0p2 − 0.159)
if log_sum_pt < 6.31 and z_7 < 0.071: z += 1090 × (6.31 − log_sum_pt) × (0.071 − z_7)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.00862`; 2: `width < 0.0133`; 3: `lam1 < 0.00802`; 4: `mass_over_sum_pt > 0.00941`; 5: `e2 < 0.0508`; 6: `max_dr > 0.0279`):

- `✓✓✓✓✓✓` **narrow medium-mass mixed jets** — 58.7% of jets, neuron 0.57, formula right for 62%. Most jets (59%): a mixture of W (31%), Z (28%), gluons and quarks; mass about 40 GeV, narrower than average, pT largely within 0.1 of the axis. All six tests pass; the narrow-girth and width penalties balance the lam1, e2 and max-ΔR bonuses, leaving a small value (0.57, on 34%) that slightly lowers the W and Z scores. The formula leans W and is right 0.625 of the time.
- `···✓·✓` **wide heavy top jets** — 13.1% of jets, neuron 6.11, formula right for 83%. Mostly tops (82%) with some gluons; heavy (81.3 GeV), nearly four times the average width, lower pT, much of the pT beyond 0.1 from the axis. The narrow-jet penalties fail; the max-ΔR bonus and base value outweigh the mass/pT penalty, giving a high value (6.11, on 92%) that strongly lowers the W and Z scores. The formula calls them t and is right 0.834 of the time.
- `✓✓✓·✓·` **pencil-like very light quark jets** — 11.9% of jets, neuron 0.12, formula right for 63%. Mostly quarks (51%) with gluons 34%; very light (5.1 GeV), with 99% of the pT inside 0.025 of the axis, higher total pT than average. The very large narrow-jet penalties (about -14.3 and -7.1) swamp the bonuses and the max-ΔR test fails, so the neuron is off most of the time (on 12%). The formula calls them q and is right 0.626 of the time.
- `✓✓✓·✓✓` **very light jets, one stray particle** — 5.2% of jets, neuron 1.10, formula right for 56%. Quarks are the largest class (39%) with gluons, Z and W; very light (5.9 GeV), a hard leading particle, 64% of the pT in the core but some particles beyond 0.025. The same large penalties apply, but the max-ΔR bonus passes, so the value is 1.10 (on 57%), lowering the W and Z scores somewhat. The formula calls them q but is right only 0.564 of the time.
- `·✓·✓✓✓` **medium-width top jets** — 3.6% of jets, neuron 5.12, formula right for 64%. Mostly tops (52%) with gluons 20% and Z 17%; mass about 59 GeV, somewhat wider than average, pT mostly at 0.05-0.1 from the axis. The girth penalty fails and the max-ΔR bonus beats the width and mass/pT penalties, giving a high value (5.13) that strongly lowers the W and Z scores. The formula calls them t and is right 0.635 of the time.
- `✓✓✓✓✓·` **light collimated gluon jets** — 2.5% of jets, neuron 0.18, formula right for 59%. Mostly gluons (50%) with quarks 39%; light (8.9 GeV), 96% of the pT inside 0.025, with pT shared more evenly among the 8 particles than average. The narrow-jet penalties dominate and the max-ΔR bonus fails, so the neuron is nearly off (on 9%). The formula calls them g and is right 0.592 of the time.
- `✓✓·✓✓✓` **heavy Z jets, large lam1** — 1.6% of jets, neuron 1.38, formula right for 80%. Mostly Z (76%) with some tops; mass about 64.5 GeV, somewhat wider than average, 65% of the pT at 0.05-0.1 from the axis. The lam1 bonus fails and the width and mass/pT penalties are partly offset by the max-ΔR bonus, giving a value of 1.38 (on 81%) that lowers the Z and W scores, working against these Z jets. The formula still calls them Z and is right 0.8 of the time.
- `···✓✓✓` **wide top jets, highest value** — 1.5% of jets, neuron 7.44, formula right for 73%. Mostly tops (71%) with gluons 19%; mass about 66 GeV, about 2.5 times the average width, pT mostly at 0.05-0.15 from the axis. No narrow-jet penalty, a smaller mass/pT penalty and the max-ΔR bonus give the neuron its highest value (7.44), which cuts the W and Z scores most. The formula calls them t and is right 0.729 of the time.
- `·✓·✓·✓` **medium-width top/gluon jets** — 1.3% of jets, neuron 4.55, formula right for 65%. Mostly tops (58%) with gluons 23%; mass about 60 GeV, wider than average, pT mostly at 0.05-0.15 from the axis. Only the width, mass/pT and max-ΔR tests pass, giving a high value (4.55) that lowers the W and Z scores. The formula calls them t and is right 0.65 of the time.
- `·✓✓✓✓✓` **rare medium-width tops, small lam1** — 0.3% of jets, neuron 5.05, formula right for 68%. A rare pattern: mostly tops (70%) with gluons; mass about 52 GeV, wider than average, pT mostly at 0.05-0.1 from the axis. As for the other medium-width top pattern but with the lam1 bonus too, giving a high value (5.05, always on) that lowers the W and Z scores. The formula calls them t and is right 0.685 of the time.

### neuron 7: two-prong shape in W/Z window (major)

- **What it measures:** Pushed up for mass/pT above 0.0729 but down again above 0.0906 (a window where boosted W/Z jets sit), and down both for very narrow jets (width < 0.00564) and for girth2 > 0.00445; it rises with eccentricity and falls with planar flow and τ21 (rank correlations 0.562, -0.562, -0.525). Z jets sit highest (3.45), then W (2.28), with top (1.10), gluon (0.84) and quark (0.44) jets low.
- *computed — its value:* largest for Z (3.45), then W (2.28), then t (1.10), then g (0.84), then q (0.44); it separates Z jets from the rest best (AUC 0.82: large for Z)
- **How the class scores use it:** High values mark a boson, so it raises the W score and the Z score, and it is the largest input of the Z score (+27%). It does not enter the g, q or t scores.
- *computed — used by:* raises the score of W (+9%), Z (+27%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 4.74
if girth2 > 0.0044: z += -765 × (girth2 − 0.0044)
if mass_over_sum_pt > 0.073: z += 183 × (mass_over_sum_pt − 0.073)
if width < 0.0056: z += -1070 × (0.0056 − width)
if girth < 0.089: z += -40.90 × (0.089 − girth)
if mass_over_sum_pt > 0.091: z += -185 × (mass_over_sum_pt − 0.091)
if e2 < 0.037: z += 81.60 × (0.037 − e2)
if girth2 > 0.0044 and eccentricity > 0.945: z += 10600 × (girth2 − 0.0044) × (eccentricity − 0.945)
if planar_flow < 0.205 and width > 0.0077: z += -3780 × (0.205 − planar_flow) × (width − 0.0077)
if planar_flow < 0.184: z += -7.43 × (0.184 − planar_flow)
if e2 < 0.025: z += 56.50 × (0.025 − e2)
if e2_sq < 0.0011: z += 1320 × (0.0011 − e2_sq)
if planar_flow < 0.179 and sum_pt > 607: z += 0.041 × (0.179 − planar_flow) × (sum_pt − 607)
if pt_7 < 44.50 and planar_flow < 0.596: z += -0.095 × (44.50 − pt_7) × (0.596 − planar_flow)
if e2 < 0.051 and D2 < 1.10: z += 120 × (0.051 − e2) × (1.10 − D2)
if girth2 < 0.00071: z += -2290 × (0.00071 − girth2)
if centroid_offset < 0.020: z += -37.90 × (0.020 − centroid_offset)
if mass > 80.40: z += -0.206 × (mass − 80.40)
if lam1 < 0.008 and D2 < 1.06: z += -754 × (0.008 − lam1) × (1.06 − D2)
if mass > 80.40 and eccentricity > 0.928: z += -2.23 × (mass − 80.40) × (eccentricity − 0.928)
if centroid_offset < 0.023 and C2 > 0.025: z += 1100 × (0.023 − centroid_offset) × (C2 − 0.025)
if centroid_offset > 0.031 and pt_0 > 375: z += -8.88 × (centroid_offset − 0.031) × (pt_0 − 375)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 > 0.00445`; 2: `mass_over_sum_pt > 0.0729`; 3: `width < 0.00564`; 4: `girth < 0.089`; 5: `mass_over_sum_pt > 0.0906`; 6: `e2 < 0.0372`):

- `··✓✓·✓` **light narrow quark/gluon jets** — 50.3% of jets, neuron 0.70, formula right for 57%. Half of all jets: quarks 34%, gluons 30%, W 19%; light (18.1 GeV), narrow, 61% of the pT inside 0.025 of the axis. Below the mass/pT window, so the window bonus fails and the narrow-width and girth penalties beat the e2 bonus; the value is small (0.70, on 43%), giving a slight push to the Z and W scores. The formula splits them between g and q and is right 0.575 of the time.
- `✓✓··✓·` **wide heavy tops above the window** — 17.1% of jets, neuron 0.56, formula right for 80%. Mostly tops (75%) with some gluons; heavy (76.8 GeV), wide, pT spread well beyond 0.1 from the axis. The window's lower edge adds about +11.7 but its upper edge (about -8.6) and the large-girth penalty (about -12.7) take it back, so the neuron is mostly off (on 20%). The formula calls them t and is right 0.801 of the time.
- `✓✓·✓··` **two-prong Z/W jets in window** — 11.5% of jets, neuron 4.35, formula right for 74%. Mostly Z (49%) and W (35%); mass about 57.5 GeV, average width, 72% of the pT at 0.05-0.1 from the axis. The mass/pT sits inside the window (bonus about +1.7) and only mild penalties apply, giving a high value (4.35, always on) that raises the Z score by about 2 and the W score by about 1. The formula calls them Z and is right 0.736 of the time.
- `✓·✓✓·✓` **narrower W jets below window** — 7.9% of jets, neuron 2.80, formula right for 66%. Mostly W (50%) with Z 29%; mass about 49 GeV, narrower than average, pT mostly at 0.025-0.1 from the axis. The window bonus fails but only small penalties apply and the e2 bonus passes, giving a value of 2.80 that raises the Z and W scores. The formula calls them W and is right 0.664 of the time.
- `✓✓·✓·✓` **Z-leaning jets in window** — 6.2% of jets, neuron 4.05, formula right for 70%. Mostly Z (51%) with W 20% and tops; mass about 59 GeV, average width, a fairly hard leading particle, pT mostly at 0.025-0.1. The window bonus and e2 bonus beat the girth penalties, giving a high value (4.05) that raises the Z score most. The formula calls them Z and is right 0.698 of the time.
- `✓✓·✓✓·` **top/Z jets above window** — 1.7% of jets, neuron 3.05, formula right for 71%. Tops are the largest class (46%) with Z 33%; mass about 64 GeV, wider than average, pT spread from the core to beyond 0.1. The window's lower edge (about +5.2) beats the girth and upper-edge penalties, giving a value of 3.05 (on 82%) that raises the Z score, pulling tops toward Z. The formula leans t and is right 0.707 of the time.
- `✓··✓·✓` **mixed medium-mass jets, no class dominant** — 1.1% of jets, neuron 3.57, formula right for 52%. A mixture of Z (28%), tops (27%) and gluons (25%); mass about 39 GeV, average width, 76% of the pT at 0.05-0.1 from the axis. The e2 bonus beats the girth penalties, giving a value of 3.57 that raises the Z score. The formula splits them between Z and t and is right only 0.523 of the time.
- `✓✓✓✓·✓` **narrow W jets in window** — 1.1% of jets, neuron 3.11, formula right for 79%. Mostly W (69%) with Z 20%; mass about 59 GeV, narrower than average, a fairly hard leading particle, pT mostly at 0.025-0.05. Every test except the upper window edge passes and they nearly cancel, leaving a value of 3.11 that raises the Z and W scores. The formula calls them W and is right 0.792 of the time.
- `✓✓····` **Z/top jets in window** — 0.8% of jets, neuron 4.41, formula right for 79%. Mostly Z (53%) with tops 33%; mass about 56 GeV, wider than average, pT mostly at 0.05-0.15 from the axis. The window bonus (about +2.7) against the girth penalty gives a high value (4.41) that raises the Z score by about 2. The formula calls them Z and is right 0.786 of the time.
- `✓·✓✓··` **rare W jets below window** — 0.5% of jets, neuron 2.21, formula right for 58%. A rare pattern: mostly W (56%) with some Z, gluons and tops; mass about 44 GeV, average width, 76% of the pT at 0.05-0.1 from the axis. Only small girth and width penalties pass, giving a value of 2.21 that raises the Z and W scores. The formula calls them W but is right only 0.583 of the time, as the others are also called W.

### neuron 9: narrow, light single-core jet (major)

- **What it measures:** Pushed up mainly for narrow jets (width < 0.00662, its strongest term), a small largest particle distance (max ΔR < 0.257) and light, centred jets (mass < 51.1 GeV with small centroid offset); it falls with width and mass (rank correlations -0.652 and -0.629). Quarks sit highest (9.07), then gluons (6.63), far above top (2.40), W (2.35) and Z (1.42) jets.
- *computed — its value:* largest for q (9.07), then g (6.63), then t (2.40), then W (2.35), then Z (1.42); it separates q jets from the rest best (AUC 0.79: large for q)
- **How the class scores use it:** High values mean a light-parton (QCD) jet, so it raises the q score (its largest input, +49%) and the g score (+26%), and lowers the W and Z scores slightly. It does not enter the t score.
- *computed — used by:* raises the score of g (+26%), q (+49%); lowers the score of W (-3%), Z (-5%); does not (or hardly) enter the score of t (share of each class score’s average input)

```
z = -2.22
if width < 0.0066: z += 1550 × (0.0066 − width)
if max_dr < 0.257: z += 14.70 × (0.257 − max_dr)
if mass < 51.10 and centroid_offset < 0.024: z += 5.63 × (51.10 − mass) × (0.024 − centroid_offset)
if width < 0.0068 and centroid_offset > 0.0029: z += -43400 × (0.0068 − width) × (centroid_offset − 0.0029)
if mass < 31.30: z += -0.136 × (31.30 − mass)
if centroid_offset < 0.017: z += 170 × (0.017 − centroid_offset)
if log_sum_pt > 6.36: z += -4.60 × (log_sum_pt − 6.36)
if mass < 49.90 and log_sum_pt < 6.79: z += 0.208 × (49.90 − mass) × (6.79 − log_sum_pt)
if centroid_offset < 0.019 and z_4 > 0.031: z += -1420 × (0.019 − centroid_offset) × (z_4 − 0.031)
if lam2 > 0.0014: z += 1500 × (lam2 − 0.0014)
if n_dr_0p2_0p4 > 1.00: z += 1.23 × (n_dr_0p2_0p4 − 1.00)
if girth2 > 0.018 and pt_7 < 29.80: z += 59.40 × (girth2 − 0.018) × (29.80 − pt_7)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.00662`; 2: `max_dr < 0.257`; 3: `mass < 51.1 and centroid_offset < 0.0241`; 4: `width < 0.00676 and centroid_offset > 0.00285`; 5: `mass < 31.3`; 6: `centroid_offset < 0.0174`):

- `✓✓✓✓✓✓` **light narrow gluon/quark jets** — 20.1% of jets, neuron 10.10, formula right for 58%. About 20% of jets: gluons 44% and quarks 39%; light (11.8 GeV), narrow, 82% of the pT inside 0.025 of the axis. All tests pass and the width bonus (about +9.4) dominates, giving a very high value (10.1) that strongly raises the q and g scores. The formula leans g and is right only 0.583 of the time, the g/q split being the problem.
- `·✓····` **wide top jets, compact spread** — 11.0% of jets, neuron 1.66, formula right for 75%. Mostly tops (68%) with gluons; mass about 68 GeV, nearly three times the average width, lower pT, pT spread to 0.2 from the axis. Only the max-ΔR test passes (about +1.0), giving a moderate value (1.66, on 42%) with a small push to q and g. The formula calls them t and is right 0.752 of the time.
- `✓✓✓·✓✓` **pencil-like high-pT quark jets** — 9.4% of jets, neuron 12.27, formula right for 70%. Mostly quarks (68%) with gluons 22%; very light (8.4 GeV), 95% of the pT in the core, high total pT (892 GeV) with one dominant particle. The width, light-centred and centred bonuses pass while the off-centre penalty fails, giving the neuron its highest value (12.27) and the largest boost to the q score. The formula calls them q and is right 0.701 of the time.
- `·✓···✓` **heavy centred Z/top jets** — 9.3% of jets, neuron 0.41, formula right for 81%. Mostly Z (59%) with tops 28%; heavy (70.7 GeV), wider than average, pT mostly at 0.05-0.1 from the axis. The max-ΔR and centred bonuses pass but not the width bonus, and the value is small (0.41, on 19%). The formula calls them Z and is right 0.813 of the time.
- `✓✓·✓·✓` **heavy high-pT W jets** — 9.0% of jets, neuron 0.55, formula right for 77%. Mostly W (64%) with Z 28%; mass about 60 GeV, narrower than average, high total pT (835 GeV), pT mostly at 0.025-0.1. The width, max-ΔR and centred bonuses pass but the light-mass tests fail, and the value ends small (0.55, on 51%). The formula calls them W and is right 0.768 of the time.
- `✓✓✓✓·✓` **narrow medium-mass W jets** — 7.7% of jets, neuron 3.14, formula right for 58%. Mostly W (53%) with Z, gluons and quarks; mass about 42.5 GeV, narrow, pT largely within 0.1 of the axis. The width bonus plus the lighter-than-51.1-GeV bonus give a value of 3.14 that pulls these jets toward q and g. The formula still calls them W but is right only 0.583 of the time.
- `✓✓·✓✓·` **light off-centre mixed jets** — 6.6% of jets, neuron 1.70, formula right for 43%. A mixture: gluons 32%, Z 24%, W 21%; light (13.6 GeV) yet 63% of the pT at 0.025-0.05 from the axis, with an off-centre pT centroid. The centred tests fail and the off-centre penalty (about -6.0) plus the light-mass penalty offset the width bonus, giving a value of 1.70 (on 67%). The formula leans g and is right only 0.431 of the time: often wrong.
- `······` **wide heavy tops, nothing passes** — 5.4% of jets, neuron 2.71, formula right for 81%. Mostly tops (79%) with gluons; heavy (78 GeV), very wide, pT spread far from the axis. No test passes; the base value (2.71, on 54%) still gives a push toward q and g. The formula calls them t anyway and is right 0.807 of the time.
- `✓✓·✓··` **off-centre medium-mass Z/W jets** — 4.9% of jets, neuron 0.37, formula right for 61%. Mostly Z (48%) with W 24%; mass about 44.6 GeV, narrower than average, pT mostly at 0.025-0.1 from the axis. The width and max-ΔR bonuses are largely cancelled by the off-centre penalty, leaving a small value (0.37, on 33%). The formula calls them Z and is right 0.606 of the time.
- `✓✓✓✓✓·` **light slightly off-centre mixture** — 4.1% of jets, neuron 4.36, formula right for 44%. A mixture: gluons 35%, W 25%, quarks and Z; light (13.4 GeV), narrow, pT within 0.05 of the axis. The width bonus (about +8.4) beats the off-centre and light-mass penalties, giving a value of 4.36 that raises the q and g scores. The formula leans g but is right only 0.436 of the time: often wrong.

### neuron 10: overall jet size (e2, width, mass) (major)

- **What it measures:** Pushed down for small e2 (< 0.0467, its strongest term) and up for mass > 9.7 GeV and for mass/pT < 0.0966; it follows e2, width and mass very closely (rank correlations 0.798, 0.794, 0.789). Tops sit highest (5.97), W (3.26) and Z (3.19) in the middle, gluons (2.01) and quarks (1.65) lowest.
- *computed — its value:* largest for t (5.97), then W (3.26), then Z (3.19), then g (2.01), then q (1.65); it separates t jets from the rest best (AUC 0.79: large for t)
- **How the class scores use it:** Large size marks a top, so it raises the t score (+26%); small size marks a quark, so the q score reads a large value as evidence against a quark and it lowers the q score (-18%). It does not enter the g, W or Z scores.
- *computed — used by:* raises the score of t (+26%); lowers the score of q (-18%); does not (or hardly) enter the score of g, W, Z (share of each class score’s average input)

```
z = 1.73
if e2 < 0.047: z += -70.60 × (0.047 − e2)
if mass_over_sum_pt < 0.097: z += 31.90 × (0.097 − mass_over_sum_pt)
if mass > 9.70: z += 0.024 × (mass − 9.70)
if girth2 < 0.0018: z += -1260 × (0.0018 − girth2)
if eccentricity > 0.901 and z_dr_0p2_0p4 < 0.054: z += 259 × (eccentricity − 0.901) × (0.054 − z_dr_0p2_0p4)
if n_dr_0p05_0p1 < 2.95: z += 0.324 × (2.95 − n_dr_0p05_0p1)
if lam1 < 0.004 and log_sum_pt > 6.69: z += 3650 × (0.004 − lam1) × (log_sum_pt − 6.69)
if LHA > 0.301 and tau21 < 0.699: z += -42.40 × (LHA − 0.301) × (0.699 − tau21)
if log_sum_pt > 6.69: z += -6.91 × (log_sum_pt − 6.69)
if e2 > 0.046: z += 61.30 × (e2 − 0.046)
if lam2 > 0.00023: z += 514 × (lam2 − 0.00023)
if lam2 > 8.4e-05 and tau21 < 0.518: z += 2350 × (lam2 − 8.4e-05) × (0.518 − tau21)
if tau32 < 0.271: z += 12.10 × (0.271 − tau32)
if lam1 < 0.004 and sum_pt > 989: z += -9.18 × (0.004 − lam1) × (sum_pt − 989)
if C2 > 0.060: z += 27.90 × (C2 − 0.060)
if log_sum_pt < 6.24: z += -3.17 × (6.24 − log_sum_pt)
if n_dr_0p2_0p4 > 1.56: z += 0.519 × (n_dr_0p2_0p4 − 1.56)
if tau32 < 0.290 and n_dr_0p2_0p4 < 2.00: z += -4.11 × (0.290 − tau32) × (2.00 − n_dr_0p2_0p4)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `e2 < 0.0467`; 2: `mass_over_sum_pt < 0.0966`; 3: `mass > 9.7`; 4: `girth2 < 0.00182`; 5: `eccentricity > 0.901 and z_dr_0p2_0p4 < 0.0539`; 6: `n_dr_0p05_0p1 < 2.95`):

- `✓✓✓·✓·` **two-prong W/Z jets** — 22.1% of jets, neuron 3.50, formula right for 69%. About 22% of jets: Z (39%) and W (37%) with some tops; mass about 52 GeV, near-average width, 75% of the pT at 0.05-0.1 from the axis. The mass, mass/pT and eccentricity bonuses beat the small-e2 penalty, giving a value of 3.50 that raises the t score and lowers the q score. The formula calls them W and is right 0.693 of the time.
- `✓✓·✓·✓` **very light pencil-like quark jets** — 15.5% of jets, neuron 0.78, formula right for 65%. Mostly quarks (51%) with gluons 35%; very light (6.1 GeV, below the mass cut), 96% of the pT in the core. The mass bonus fails and the small-e2 and small-girth penalties leave a small value (0.78). The formula calls them q and is right 0.65 of the time.
- `✓✓✓·✓✓` **narrow W jets, hard leading particle** — 14.3% of jets, neuron 3.59, formula right for 63%. Mostly W (44%) with Z 31%; mass about 48 GeV, narrow, a dominant leading particle, 66% of the pT at 0.025-0.05. Mass, mass/pT, eccentricity and few-particles-at-0.05-0.1 bonuses beat the e2 penalty, giving a value of 3.59 that raises t and lowers q. The formula calls them W and is right 0.631 of the time.
- `··✓··✓` **large wide heavy top jets** — 7.4% of jets, neuron 8.96, formula right for 85%. Mostly tops (83%) with some gluons; heavy (83 GeV), about four times the average width, lower pT, with most pT beyond 0.1 from the axis. The e2 penalty fails and the mass bonus passes, so the value is the highest (8.96) and raises the t score by about 3.4 while lowering q. The formula calls them t and is right 0.848 of the time.
- `✓✓✓✓✓✓` **light collimated quark/gluon jets** — 7.0% of jets, neuron 2.09, formula right for 56%. Mostly quarks (44%) with gluons 34%; mass about 19 GeV, narrow, 67% of the pT in the core. All tests pass; the penalties roughly cancel the bonuses, giving a value of 2.09 with a moderate push to t. The formula calls them q but is right only 0.557 of the time.
- `✓✓·✓✓✓` **very light mixed jets** — 6.4% of jets, neuron 1.77, formula right for 49%. A mixture: gluons 31%, quarks 26%, W 20%, Z 19%; very light (5.5 GeV), narrow, pT all within 0.05 of the axis. The mass bonus fails; the small-e2 and girth penalties leave a value of 1.77. The formula leans g but is right only 0.488 of the time.
- `✓✓✓✓·✓` **light gluon/quark jets** — 6.1% of jets, neuron 1.16, formula right for 58%. Equal gluons (40%) and quarks (39%); light (14.8 GeV), narrow, 71% of the pT in the core with a hard leading particle. The penalties nearly cancel the bonuses, leaving a value of 1.16. The formula leans g and is right 0.585 of the time.
- `✓✓✓··✓` **medium-mass Z-leaning mixture** — 4.7% of jets, neuron 2.94, formula right for 60%. Z is the largest class (38%) with W, gluons and tops; mass about 48 GeV, a dominant leading particle, 65% of the pT at 0.025-0.05. Mass, mass/pT and few-particles bonuses beat the e2 penalty, giving a value of 2.94 that raises t. The formula leans Z and is right 0.599 of the time: a mixture.
- `··✓···` **wide heavy top jets** — 3.9% of jets, neuron 7.04, formula right for 83%. Mostly tops (83%) with some gluons; heavy (77.6 GeV), about three times the average width, pT mostly at 0.05-0.1 but with a tail far out. Only the mass bonus passes, with no e2 penalty, giving a high value (7.04) that raises the t score by about 2.6. The formula calls them t and is right 0.832 of the time.
- `✓✓✓···` **medium-mass mixture, no class dominant** — 3.7% of jets, neuron 2.82, formula right for 52%. A mixture of gluons (27%), tops (25%), W and Z (19% each); mass about 40 GeV, near-average width, lower pT, pT mostly at 0.05-0.1. The mass and mass/pT bonuses slightly beat the e2 penalty, giving a value of 2.82 that raises t. The formula splits its calls among g, W and t and is right only 0.524 of the time.

### neuron 13: compactness (girth below top size) (major)

- **What it measures:** Driven mostly by girth < 0.15 (its dominant term) and width < 0.0159, both pushing it up, i.e. by the jet being narrower than a typical top; very small e2 (< 0.0509) pulls it down a little. It falls with width, girth and LHA (rank correlations about -0.81 to -0.83); quarks (7.15), W (6.17), gluons (5.88) and Z (5.66) all sit high, tops far lower (2.01).
- *computed — its value:* largest for q (7.15), then W (6.17), then g (5.88), then Z (5.66), then t (2.01); it separates t jets from the rest best (AUC 0.09: small for t)
- **How the class scores use it:** Being narrower than a top is the main evidence against a top, so it lowers the t score, where it is the largest input (-46%); it also raises the W and Z scores. It does not enter the g or q scores.
- *computed — used by:* raises the score of W (+9%), Z (+10%); lowers the score of t (-46%); does not (or hardly) enter the score of g, q (share of each class score’s average input)

```
z = 1.68
if girth < 0.150: z += 67.00 × (0.150 − girth)
if width < 0.016: z += 217 × (0.016 − width)
if e2 < 0.051: z += -88.60 × (0.051 − e2)
if girth < 0.156 and log_sum_pt < 6.91: z += -41.10 × (0.156 − girth) × (6.91 − log_sum_pt)
if girth < 0.148 and pt_7 < 39.50: z += -1.09 × (0.148 − girth) × (39.50 − pt_7)
if tau21 < 0.518 and max_dr > -0.038: z += -14.90 × (0.518 − tau21) × (max_dr − -0.038)
if sum_pt_top5 > 653 and pt_7 < 42.60: z += 0.00059 × (sum_pt_top5 − 653) × (42.60 − pt_7)
if pt_7 < 24.80: z += -0.246 × (24.80 − pt_7)
if pt_0 > 179: z += 0.0022 × (pt_0 − 179)
if C2 > 0.066: z += -52.40 × (C2 − 0.066)
if sum_pt > 998: z += -0.024 × (sum_pt − 998)
if sum_pt_top5 > 677 and z_7 > 0.029: z += -0.566 × (sum_pt_top5 − 677) × (z_7 − 0.029)
if sum_pt > 1070 and n_pt_above_50 > 6.01: z += 0.019 × (sum_pt − 1070) × (n_pt_above_50 − 6.01)
if sum_pt < 764 and z_4 < 0.038: z += 6.47 × (764 − sum_pt) × (0.038 − z_4)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth < 0.15`; 2: `width < 0.0159`; 3: `e2 < 0.0509`; 4: `girth < 0.156 and log_sum_pt < 6.91`; 5: `girth < 0.148 and pt_7 < 39.5`; 6: `tau21 < 0.518 and max_dr > -0.0382`):

- `✓✓✓✓✓✓` **compact jets of all kinds** — 38.1% of jets, neuron 5.37, formula right for 63%. 38% of jets: a mixture led by Z (29%) and W (28%) with g, q and t (14-15% each); mass about 44 GeV, narrower than average, fairly hard leading particle. All six tests pass; the girth-below-top-size bonus (about +6.3) dominates the penalties, giving a high value (5.37) that lowers the t score by about 2.2 and raises W and Z. The formula calls them W and is right 0.63 of the time.
- `✓✓✓✓·✓` **compact jets, many hard particles** — 19.5% of jets, neuron 5.97, formula right for 65%. A mixture of W (32%), Z (30%) and gluons (20%); mass about 42 GeV, narrower than average, pT shared very evenly (the 8th particle is still hard). The hard-8th-particle penalty does not apply, so the value is a bit higher (5.97, always on), lowering the t score by about 2.4. The formula calls them W and is right 0.646 of the time.
- `✓✓✓✓✓·` **light collimated quark jets** — 16.0% of jets, neuron 7.11, formula right for 61%. Mostly quarks (45%) with gluons 26%; light (10.8 GeV), 76% of the pT in the core, a hard leading particle. The τ21 penalty fails and the compactness bonuses are large, giving a high value (7.11) that lowers the t score by about 2.9. The formula calls them q and is right 0.608 of the time.
- `✓✓✓✓··` **light evenly shared gluon jets** — 7.4% of jets, neuron 7.96, formula right for 55%. Mostly gluons (50%) with quarks 27%; very light (9.0 GeV), 76% of the pT in the core, pT shared very evenly with a hard 8th particle. Neither the hard-8th-particle nor the τ21 penalty applies, giving a very high value (7.96) that lowers the t score by about 3.2. The formula calls them g but is right only 0.553 of the time, as many quarks are called gluons.
- `✓··✓✓✓` **wide heavy tops, girth below cut** — 3.8% of jets, neuron 0.61, formula right for 84%. Mostly tops (83%) with some gluons; mass about 77 GeV, about three times the average width, pT spread beyond 0.1. The width bonus fails; the girth bonus is small (about +1.4) and penalties pull it back, so the value is small (0.61) and the t score is only slightly lowered. The formula calls them t and is right 0.839 of the time.
- `·····✓` **widest, heaviest top jets** — 3.0% of jets, neuron 0.14, formula right for 80%. Mostly tops (76%) with gluons 17%; heavy (89.9 GeV), about five times the average width, pT mostly beyond 0.15 from the axis. Too wide for any compactness bonus; only the τ21 penalty passes, leaving a small value (0.14, on 39%). The formula calls them t and is right 0.8 of the time.
- `✓✓·✓✓✓` **medium-width top/gluon jets** — 1.8% of jets, neuron 2.42, formula right for 71%. Mostly tops (68%) with gluons 19%; mass about 62 GeV, twice the average width, pT mostly at 0.05-0.15 from the axis. Girth and width bonuses pass but smaller, and three penalties pull it down, giving a value of 2.43 that lowers the t score by about 1.0. The formula still calls them t and is right 0.712 of the time.
- `✓··✓·✓` **wide heavy tops, many hard particles** — 1.7% of jets, neuron 0.73, formula right for 80%. Mostly tops (79%) with gluons 16%; heavy (83.8 GeV), about three times the average width, pT shared very evenly with a hard 8th particle. A small girth bonus against the pT and τ21 penalties gives a small value (0.73) and a slight cut to the t score. The formula calls them t and is right 0.798 of the time.
- `✓✓✓·✓·` **pencil-like very high-pT quark jets** — 1.6% of jets, neuron 8.89, formula right for 71%. Mostly quarks (64%) with gluons 22%; light (10.1 GeV), 97% of the pT in the core, the highest total pT (1082 GeV) with one particle carrying about half of it. The largest compactness bonuses with no high-pT or τ21 penalty give the neuron its highest value (8.89), lowering the t score by about 3.6. The formula calls them q and is right 0.713 of the time.
- `✓✓✓·✓✓` **very high-pT one-particle-dominated mixture** — 1.3% of jets, neuron 7.79, formula right for 64%. A mixture: quarks 31%, Z 24%, W 23%, gluons 20%; mass about 46 GeV, narrow, the highest total pT (1082 GeV) with one particle carrying about half. Large compactness bonuses without the high-pT penalty give a high value (7.79) that lowers the t score. The formula splits them among q, W and Z and is right 0.643 of the time: a mixture.

### neuron 14: intermediate width (Z-sized spread) (major)

- **What it measures:** Pushed up for girth2 < 0.0131 and e2 < 0.0385 but down for the narrowest jets (width < 0.00741, girth < 0.0869), so it peaks for jets of intermediate width, a bit wider than a typical W; it rises with the number and pT share of particles at 0.1-0.4 in ΔR (rank correlations about 0.33-0.34). Z jets sit highest (1.50), well above tops (0.43), gluons (0.24), W (0.18) and quarks (0.16).
- *computed — its value:* largest for Z (1.50), then t (0.43), then g (0.24), then W (0.18), then q (0.16); it separates Z jets from the rest best (AUC 0.78: large for Z)
- **How the class scores use it:** It is the W/Z separator: Z jets sit high and W jets low on it, so it raises the Z score and lowers the W score. It does not enter the g, q or t scores.
- *computed — used by:* raises the score of Z (+7%); lowers the score of W (-9%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = -1.51
if girth2 < 0.013: z += 632 × (0.013 − girth2)
if width < 0.0074: z += -1040 × (0.0074 − width)
if girth < 0.087: z += -80.10 × (0.087 − girth)
if e2 < 0.038: z += 106 × (0.038 − e2)
if max_dr < 0.177: z += -20.10 × (0.177 − max_dr)
if z_dr_0p05_0p1 < 0.597 and C2 < 0.066: z += -77.00 × (0.597 − z_dr_0p05_0p1) × (0.066 − C2)
if girth2 < 0.0045 and n_dr_0p2_0p4 < 0.930: z += -486 × (0.0045 − girth2) × (0.930 − n_dr_0p2_0p4)
if girth2 < 0.013 and eccentricity > 0.971: z += 11600 × (0.013 − girth2) × (eccentricity − 0.971)
if z_dr_0p05_0p1 < 0.572: z += 1.85 × (0.572 − z_dr_0p05_0p1)
if mass > 5.61: z += 0.019 × (mass − 5.61)
if width < 0.0076 and planar_flow < 0.109: z += -6890 × (0.0076 − width) × (0.109 − planar_flow)
if width < 0.0086 and D2 < 1.04: z += -986 × (0.0086 − width) × (1.04 − D2)
if planar_flow < 0.110 and centroid_offset > 0.0095: z += 1270 × (0.110 − planar_flow) × (centroid_offset − 0.0095)
if width < 0.0079 and log_sum_pt < 6.82: z += 381 × (0.0079 − width) × (6.82 − log_sum_pt)
if planar_flow < 0.116 and max_dr < 0.164: z += -187 × (0.116 − planar_flow) × (0.164 − max_dr)
if lam1 > 0.0073: z += -101 × (lam1 − 0.0073)
if planar_flow < 0.116 and centroid_offset > 0.019: z += -1310 × (0.116 − planar_flow) × (centroid_offset − 0.019)
if D2 < 1.04 and centroid_offset < 0.031: z += 38.50 × (1.04 − D2) × (0.031 − centroid_offset)
if lam1 > 0.0055 and max_dr < 0.168: z += 6850 × (lam1 − 0.0055) × (0.168 − max_dr)
if mass < 75.30 and D2 < 0.865: z += -0.049 × (75.30 − mass) × (0.865 − D2)
if planar_flow < 0.106 and sum_pt < 740: z += -0.051 × (0.106 − planar_flow) × (740 − sum_pt)
if e2 < 0.038 and D2 < 0.961: z += 192 × (0.038 − e2) × (0.961 − D2)
if lam1 > 0.0073 and max_dr < 0.134: z += 43000 × (lam1 − 0.0073) × (0.134 − max_dr)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.0131`; 2: `width < 0.00741`; 3: `girth < 0.0869`; 4: `e2 < 0.0385`; 5: `max_dr < 0.177`; 6: `z_dr_0p05_0p1 < 0.597 and C2 < 0.0662`):

- `✓✓✓✓✓✓` **light narrow quark/gluon jets** — 48.7% of jets, neuron 0.07, formula right for 59%. Almost half of all jets: quarks 33%, gluons 30%, W 20%; light (19 GeV), narrow, 59% of the pT in the core. All tests pass; the narrow-width and narrow-girth penalties cancel the bonuses, so the neuron is off most of the time (on 7%). The formula splits them between g and q and is right 0.586 of the time.
- `✓✓✓✓✓·` **two-prong W/Z jets, small max ΔR** — 9.6% of jets, neuron 0.67, formula right for 65%. Mostly W (42%) with Z 30%; mass about 46 GeV, narrower than average, 83% of the pT at 0.05-0.1 from the axis. The narrow penalties are smaller here, leaving a value of 0.67 (on 40%) that lowers the W score and raises Z. The formula calls them W and is right 0.654 of the time.
- `······` **wide heavy tops, off** — 8.7% of jets, neuron 0.04, formula right for 88%. Mostly tops (88%); heavy (81.3 GeV), nearly four times the average width, pT spread far from the axis. No test passes and the neuron is off most of the time (on 13%). The formula calls them t and is right 0.884 of the time.
- `✓✓✓✓·✓` **high-pT narrow Z/W jets** — 7.5% of jets, neuron 1.11, formula right for 66%. Mostly Z (44%) with W 32%; mass about 51 GeV, narrower than average, high total pT (823 GeV) with a dominant leading particle, 65% of the pT at 0.025-0.05. The girth2 and e2 bonuses outweigh the narrow penalties, giving a value of 1.12 (on 76%) that lowers the W score and raises Z. The formula calls them Z and is right 0.659 of the time.
- `✓✓✓·✓·` **two-prong W jets, W-sized width** — 5.5% of jets, neuron 0.67, formula right for 73%. Mostly W (53%) with Z 34%; mass about 56.5 GeV, near-average width, 87% of the pT at 0.05-0.1 from the axis. The girth2 bonus beats the small penalties, giving a value of 0.67 (on 53%) that lowers the W score, working against these W. The formula still calls them W and is right 0.727 of the time.
- `·····✓` **wide heavy tops, off** — 3.4% of jets, neuron 0.00, formula right for 72%. Mostly tops (68%) with gluons 22%; heavy (82.7 GeV), nearly four times the average width, pT mostly beyond 0.1. Only one small penalty passes, so the neuron is off (on 1%). The formula calls them t and is right 0.719 of the time.
- `✓···✓·` **Z-sized two-prong jets** — 2.7% of jets, neuron 2.86, formula right for 77%. Mostly Z (62%) with tops 24%; mass about 62 GeV, somewhat wider than average, 77% of the pT at 0.05-0.1 from the axis. Too wide for the narrow penalties but the girth2 bonus passes, giving a high value (2.86, on 95%) that lowers the W score by about 2.1 and raises Z by about 1.1. The formula calls them Z and is right 0.772 of the time.
- `····✓✓` **wide top jets, off** — 1.9% of jets, neuron 0.04, formula right for 77%. Mostly tops (76%) with gluons; mass about 71 GeV, more than twice the average width, 66% of the pT at 0.1-0.15 from the axis. Only penalties pass, so the neuron is off (on 6%). The formula calls them t and is right 0.773 of the time.
- `✓·✓·✓·` **clean Z-sized jets** — 1.9% of jets, neuron 2.89, formula right for 83%. Mostly Z (81%); mass about 62.6 GeV, a bit wider than average, 72% of the pT at 0.05-0.1 from the axis. The girth2 bonus beats small penalties, giving a high value (2.89, always on) that lowers the W score and raises Z. The formula calls them Z and is right 0.83 of the time.
- `✓✓✓✓··` **high-pT narrow mixture, Z-leaning** — 1.7% of jets, neuron 1.52, formula right for 53%. A mixture: Z 32%, quarks 25%, W, gluons and tops; mass about 46 GeV, narrow, high total pT (800 GeV) with one dominant particle. The girth2 and e2 bonuses beat the narrow penalties, giving a value of 1.53 that lowers the W score and raises Z. The formula leans Z but is right only 0.526 of the time: a mixture.

### neuron 0: compact massive two-prong-ness (moderate)

- **What it measures:** Pushed down for light jets (mass < 22.5 GeV and < 29.3 GeV are its two strongest terms) and up for compact jets (girth2 < 0.0121); it rises with eccentricity and falls with τ21 and planar flow, so it measures how much the jet looks like a compact, elongated two-prong object with real mass. Z (2.28) and W (1.95) jets sit highest, tops in the middle (0.76), gluons (0.28) and quarks (0.22) lowest.
- *computed — its value:* largest for Z (2.28), then W (1.95), then t (0.76), then g (0.28), then q (0.22); it separates Z jets from the rest best (AUC 0.75: large for Z)
- **How the class scores use it:** Because W jets sit high on it and gluons low, the W score reads it as evidence for a W and the g score as evidence against a gluon: it raises the W score and lowers the g score. The q, Z and t scores do not use it (the Z score relies on the related neuron 7 instead).
- *computed — used by:* raises the score of W (+9%); lowers the score of g (-6%); does not (or hardly) enter the score of q, Z, t (share of each class score’s average input)

```
z = -0.480
if mass < 22.50: z += -0.543 × (22.50 − mass)
if mass < 29.30 and phi_1 > -0.077: z += -4.03 × (29.30 − mass) × (phi_1 − -0.077)
if girth2 < 0.012: z += 301 × (0.012 − girth2)
if girth < 0.077: z += -56.80 × (0.077 − girth)
if centroid_offset < 0.034: z += 71.00 × (0.034 − centroid_offset)
if width < 0.0045: z += -799 × (0.0045 − width)
if mass < 71.30: z += -0.026 × (71.30 − mass)
if z_dr_0_0p05 > 0.852: z += 15.40 × (z_dr_0_0p05 − 0.852)
if girth2 < 0.020 and eccentricity > 0.961: z += 3910 × (0.020 − girth2) × (eccentricity − 0.961)
if mass < 64.90 and pt_7 < 40.10: z += -0.0022 × (64.90 − mass) × (40.10 − pt_7)
if mass < 64.80 and centroid_offset > 0.011: z += 2.55 × (64.80 − mass) × (centroid_offset − 0.011)
if sum_pt > 895: z += -0.028 × (sum_pt − 895)
if sum_pt > 871 and pt_7 < 27.80: z += 0.0018 × (sum_pt − 871) × (27.80 − pt_7)
if planar_flow < 0.148 and sum_pt_top2 < 388: z += -0.052 × (0.148 − planar_flow) × (388 − sum_pt_top2)
if lam1 < 0.0065 and D2 < 0.886: z += -2060 × (0.0065 − lam1) × (0.886 − D2)
if sum_pt_top5 > 655 and z_7 > 0.027: z += -0.514 × (sum_pt_top5 − 655) × (z_7 − 0.027)
if mass < 30.00 and D2 < 0.910: z += -2.90 × (30.00 − mass) × (0.910 − D2)
if eccentricity > 0.997: z += 499 × (eccentricity − 0.997)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass < 22.5`; 2: `mass < 29.3 and phi_1 > -0.0771`; 3: `girth2 < 0.0121`; 4: `girth < 0.0775`; 5: `centroid_offset < 0.0338`; 6: `width < 0.00449`):

- `✓✓✓✓✓✓` **light, very collimated quark/gluon jets** — 32.7% of jets, neuron 0.00, formula right for 60%. About a third of all jets: mostly quarks and gluons (q 43%, g 36%), very light (mean mass 9.1 GeV) and very narrow, with 82% of the pT inside 0.025 of the axis versus 32% for all jets; pT sharing among the 8 particles is like the average jet. All six tests pass, and the two light-mass tests (about -7.3 and -6.3) swamp the compactness bonuses, so the neuron is off and adds nothing to any class score. The formula calls them q or g and is right only 0.596 of the time, since quarks and gluons look alike here.
- `··✓✓✓·` **compact two-prong W/Z jets** — 19.4% of jets, neuron 2.63, formula right for 70%. Mostly W and Z (45% and 35%) with some tops, mass about 55 GeV, average width; almost no pT in the very core, instead a ring at 0.025-0.1 from the axis, as expected for two hard prongs. The mass tests fail, while the compact-girth and small-centroid-offset tests pass (about +1.9 and +1.5) against a small girth penalty, giving a large value (2.63, on 98% of the time) that raises the W score and lowers the g score. The formula calls them W and is right 0.702 of the time; the W/Z split is the main error.
- `··✓✓✓✓` **narrower, lighter W-like jets** — 11.9% of jets, neuron 1.33, formula right for 57%. Mostly W (46%) with Z and a quarter quarks/gluons; mass 42.5 GeV, narrower than average, with a harder leading particle and most pT at 0.025-0.05 from the axis. Like the W/Z pattern but the narrow-width test also passes and subtracts about 1, so the value is moderate (1.33, on 71%), giving a smaller push toward W and away from g. The formula calls them W but is right only 0.568 of the time, because the quark/gluon admixture is often mislabelled.
- `··✓·✓·` **wider two-prong jets (mostly Z)** — 10.9% of jets, neuron 2.93, formula right for 74%. Mostly Z (57%) with some tops and W; mass about 60 GeV, slightly wider than average, pT spread evenly over the particles, and 74% of the pT at 0.05-0.1 from the axis. The girth penalty no longer applies (only girth2 and centroid pass), so this pattern gives the neuron its highest value (2.93, on 98%) and the biggest boost to the W score, with a cut to g. The formula nonetheless calls them Z and is right 0.736 of the time.
- `····✓·` **wide, heavy three-prong jets (tops)** — 8.3% of jets, neuron 0.49, formula right for 82%. Mostly tops (80%) with some gluons; heavy (mean 83.7 GeV), about three times the average width, lower total pT, and pT spread far from the axis (much of it beyond 0.1). Only the small-centroid-offset test passes (about +1.0), so the value is small (0.49, on 60%) and the pushes toward W and away from g are weak. The formula calls them t and is right 0.818 of the time.
- `······` **wide heavy jets, nothing passes** — 7.3% of jets, neuron 0.19, formula right for 81%. Mostly tops (80%) with some gluons; heavy (72.9 GeV), very wide, lowest total pT among the main patterns, with the pT spread well outside 0.1 from the axis. No test passes, so only the base value remains and the neuron is on just 16% of the time, adding almost nothing to the scores. The formula calls them t and is right 0.813 of the time, using other neurons.
- `·✓✓✓✓✓` **light-medium mixed narrow jets** — 3.5% of jets, neuron 0.08, formula right for 48%. A mixture: gluons 35%, quarks 30%, plus W and Z; mass about 26 GeV (just above the lighter mass cut), narrow, with most pT within 0.05 of the axis. The second mass test passes (about -1.1) along with the width and girth penalties, so the compactness bonuses are cancelled and the neuron is nearly off (on 10%). The formula calls them g but is right only 0.477 of the time: a hard, mixed group.
- `✓✓✓✓·✓` **very light, slightly spread odd mix** — 2.0% of jets, neuron 0.01, formula right for 46%. A mixture: gluons 40%, Z 24%, tops and W; very light (9.0 GeV) with lower pT, and unlike the first pattern the pT sits mostly at 0.025-0.05 rather than in the very core. The mass tests pass with large negative amounts and the centroid test fails, so the neuron is essentially off (on 1%). The formula calls them g but is right only 0.461 of the time; the Z share here is often mistaken for gluons.
- `··✓···` **moderately compact top/gluon jets** — 1.6% of jets, neuron 1.40, formula right for 60%. Mostly tops (54%) with gluons 23%; mass about 48 GeV, slightly wider than average, lower pT, with 70% of the pT at 0.05-0.1 from the axis. Only the girth2 test passes (about +0.76), giving a fair value (1.40, on 89%) that pushes toward W and away from g even though these are mainly tops. The formula still calls them t and is right 0.596 of the time.
- `··✓✓··` **mixed medium jets, top/Z/gluon** — 0.9% of jets, neuron 1.96, formula right for 46%. A mixture: tops 33%, gluons 24%, Z 22%; mass about 42 GeV, average width, lower pT, with most pT at 0.05-0.1 from the axis. The two girth tests pass (net about +1.2) but the centroid test fails; the value is sizeable (1.96) and pushes toward W and away from g. The formula splits them between Z and t and is right only 0.461 of the time.

### neuron 1: moderate width at high pT (moderate)

- **What it measures:** Pushed down for narrow jets (width < 0.009, its strongest term) and up for small e2_sq and for high total pT (log of total pT > 6.41); it follows width, girth and mass (rank correlations about +0.44 to +0.46). Z (0.75) and top (0.74) jets sit highest, gluons in the middle (0.53), W (0.31) and quarks (0.21) lowest; its clearest separation is that it is small for quarks.
- *computed — its value:* largest for Z (0.75), then t (0.74), then g (0.53), then W (0.31), then q (0.21); it separates q jets from the rest best (AUC 0.33: small for q)
- **How the class scores use it:** The g score uses it mainly to tell gluons from quarks, which sit lowest on it: it raises the g score and, only slightly, the Z score. It does not (or hardly) enter the q, W or t scores; the Z and top jets that also sit high on it are kept out of the g score by other scales.
- *computed — used by:* raises the score of g (+7%), Z (+2%); does not (or hardly) enter the score of q, W, t (share of each class score’s average input)

```
z = 1.20
if width < 0.009: z += -657 × (0.009 − width)
if e2_sq < 0.0077: z += 470 × (0.0077 − e2_sq)
if log_sum_pt > 6.59 and lam2 < 0.0012: z += 10300 × (log_sum_pt − 6.59) × (0.0012 − lam2)
if log_sum_pt > 6.41: z += 4.58 × (log_sum_pt − 6.41)
if pt_7 > 30.40: z += 0.115 × (pt_7 − 30.40)
if pt_7 > 29.20 and mass < 97.00: z += -0.0015 × (pt_7 − 29.20) × (97.00 − mass)
if log_sum_pt > 6.40 and centroid_offset < 0.024: z += -235 × (log_sum_pt − 6.40) × (0.024 − centroid_offset)
if C2 < 0.049: z += -23.70 × (0.049 − C2)
if log_sum_pt > 6.33 and max_dr < 0.191: z += 19.00 × (log_sum_pt − 6.33) × (0.191 − max_dr)
if e2_sq < 0.0078 and planar_flow < 0.085: z += -8390 × (0.0078 − e2_sq) × (0.085 − planar_flow)
if log_sum_pt > 6.60 and girth2_top3 < 0.0063: z += -1090 × (log_sum_pt − 6.60) × (0.0063 − girth2_top3)
if z_7 < 0.056: z += -33.70 × (0.056 − z_7)
if max_dr < 0.045: z += -63.30 × (0.045 − max_dr)
if e2 < 0.038 and eccentricity > 0.979: z += 6000 × (0.038 − e2) × (eccentricity − 0.979)
if e2 > 0.031 and tau32 < 0.629: z += -82.70 × (e2 − 0.031) × (0.629 − tau32)
if lam1 < 0.0083 and centroid_offset > 0.021: z += 14300 × (0.0083 − lam1) × (centroid_offset − 0.021)
if log_sum_pt > 6.59 and n_pt_above_50 > 7.01: z += -7.05 × (log_sum_pt − 6.59) × (n_pt_above_50 − 7.01)
if pt_7 > 32.90 and centroid_offset > 0.014: z += 1.53 × (pt_7 − 32.90) × (centroid_offset − 0.014)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.009`; 2: `e2_sq < 0.00775`; 3: `log_sum_pt > 6.59 and lam2 < 0.0012`; 4: `log_sum_pt > 6.41`; 5: `pt_7 > 30.4`; 6: `pt_7 > 29.2 and mass < 97`):

- `✓✓✓✓✓✓` **narrow high-pT mixed jets** — 21.9% of jets, neuron 0.60, formula right for 64%. A mixture of W, gluons, Z and quarks (each 21-30%), mass about 33 GeV, narrow, high total pT (843 GeV) with pT shared fairly evenly and a hard 8th particle; most pT within 0.05 of the axis. All tests pass: the narrow-width penalty (about -4.1) is roughly balanced by the e2 and high-pT bonuses, leaving a small value (0.60, on 45%) that slightly raises the g and Z scores. The formula leans W and is right 0.639 of the time.
- `✓✓✓✓··` **hard-leading-particle narrow quark jets** — 19.9% of jets, neuron 0.32, formula right for 69%. Mostly quarks (41%) with W and Z; mass about 31 GeV, narrow, the highest total pT (899 GeV) and one dominant particle carrying close to half of it while the 8th particle is soft; very collimated. The width penalty meets the e2 and both high-pT bonuses, but the pt_7 tests fail, leaving a small value (0.32, on 35%) with a slight push to g and Z. The formula calls them q and is right 0.692 of the time.
- `✓✓·✓✓✓` **narrow mid-pT evenly shared jets** — 15.3% of jets, neuron 0.26, formula right for 60%. A mixture: W 30%, Z 25%, gluons 24%; mass about 32 GeV, narrow, mid total pT (671 GeV) evenly shared with a hard 8th particle, pT spread up to 0.1 from the axis. The width penalty is partly offset by e2, the lower pT cut and the pt_7 bonus, leaving a small value (0.26, on 30%). The formula calls them W but is right only 0.597 of the time, mixing up W, Z and gluons.
- `✓✓··✓✓` **narrow low-pT gluon-leaning jets** — 12.3% of jets, neuron 0.26, formula right for 54%. Gluons are the largest class (37%) with W, Z, quarks and tops; mass about 26 GeV, narrow, low total pT (529 GeV) shared very evenly among the particles. Width penalty plus e2 and pt_7 bonuses give a small value (0.26, on 27%); the pT tests fail. The formula calls them g but is right only 0.538 of the time.
- `····✓✓` **wide low-pT top jets** — 8.1% of jets, neuron 0.77, formula right for 79%. Mostly tops (78%) with some gluons; mass about 68 GeV, about three times the average width, low total pT (500 GeV) spread evenly, with most pT beyond 0.05 from the axis. The width and e2 tests fail, so no penalty; only the pt_7 tests pass (net about +0.46), giving a fair value (0.77, on 76%) that raises the g and Z scores. The formula still calls them t and is right 0.791 of the time.
- `✓✓·✓··` **narrow mid-pT jets, no dominant class** — 2.9% of jets, neuron 0.18, formula right for 45%. An even mixture of all five classes (17-21% each); mass about 32 GeV, narrow, total pT 680 GeV with a fairly hard leading particle and soft 8th particle. The width penalty is only partly offset by e2 and the lower pT bonus, so the value is small (0.18, on 21%). The formula is right only 0.453 of the time, splitting its calls between q and W: a genuinely confused group.
- `······` **wide low-pT tops, nothing passes** — 2.7% of jets, neuron 0.34, formula right for 75%. Mostly tops (74%) with some gluons; mass about 64 GeV, very wide, the lowest total pT (468 GeV), with pT far from the axis. No test passes, so only the base value remains (0.34, on 58%), giving a small push to g and Z. The formula calls them t and is right 0.75 of the time.
- `···✓✓✓` **wide higher-pT top jets** — 2.5% of jets, neuron 1.56, formula right for 78%. Mostly tops (75%) with some gluons; heavy (78.3 GeV), wide, total pT 660 GeV evenly shared with a hard 8th particle, pT spread well away from the axis. No width penalty, while the pT and pt_7 tests add up, giving the neuron its highest value (1.56, on 96%) and the largest push to the g (0.608) and Z scores. The formula still calls them t and is right 0.783 of the time.
- `✓✓····` **narrow low-pT gluon jets** — 2.2% of jets, neuron 0.33, formula right for 52%. Mostly gluons (46%) with tops 21% and quarks; mass about 22 GeV, narrow, low total pT (491 GeV) with a soft 8th particle. Only the width penalty and e2 bonus pass, leaving a small value (0.33, on 29%). The formula calls them g but is right only 0.515 of the time, often mistaking the tops and quarks here.
- `✓✓✓✓·✓` **narrow high-pT W/Z/quark mix** — 1.6% of jets, neuron 0.39, formula right for 64%. A mixture: W 30%, Z 28%, quarks 26%; mass about 36 GeV, narrow, high total pT (842 GeV) with a fairly hard leading particle. Like the first pattern but the 8th particle sits right at the pt_7 threshold, so one pt_7 bonus fails; the value stays small (0.39, on 40%). The formula leans W and is right 0.643 of the time.

### neuron 3: radiation at wide angle (ΔR 0.2-0.4) (moderate)

- **What it measures:** Switched off for narrow jets (girth2 < 0.00905 and girth2 < 0.0126 are its two strongest terms, both pushing down) and pushed up for e2 < 0.0433; it follows the pT share and number of particles at 0.2 ≤ ΔR < 0.4 (rank correlations 0.604 and 0.602). Tops sit clearly highest (1.80), then gluons (0.61) and quarks (0.32); Z jets are rarely on it (0.15) and W jets almost never (0.01, zero for 98% of them).
- *computed — its value:* largest for t (1.80), then g (0.61), then q (0.32), then Z (0.15), then W (0.01); it separates t jets from the rest best (AUC 0.71: large for t)
- **How the class scores use it:** A clean two-prong boson has little pT at such wide angles, so the W and Z scores read this scale as evidence against a boson: it lowers the W score and the Z score. It does not (or hardly) enter the g, q or t scores, even though tops sit highest on it.
- *computed — used by:* lowers the score of W (-7%), Z (-11%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 2.90
if girth2 < 0.0091: z += -833 × (0.0091 − girth2)
if e2 < 0.043: z += 179 × (0.043 − e2)
if girth2 < 0.013: z += -441 × (0.013 − girth2)
if e2 > 0.028: z += -126 × (e2 − 0.028)
if mass_over_sum_pt > 0.062 and n_dr_0_0p05 < 5.99: z += 10.80 × (mass_over_sum_pt − 0.062) × (5.99 − n_dr_0_0p05)
if centroid_offset > 0.010: z += 49.30 × (centroid_offset − 0.010)
if mass_over_sum_pt > 0.075 and tau32 < 0.529: z += -133 × (mass_over_sum_pt − 0.075) × (0.529 − tau32)
if LHA > 0.316 and eccentricity > 0.953: z += 1090 × (LHA − 0.316) × (eccentricity − 0.953)
if lam1 > 0.015 and eccentricity > 0.951: z += -12100 × (lam1 − 0.015) × (eccentricity − 0.951)
if e2 < 0.043 and z_dr_0p1_0p2 > 0.0006: z += -328 × (0.043 − e2) × (z_dr_0p1_0p2 − 0.0006)
if mass > 71.90: z += -0.069 × (mass − 71.90)
if LHA > 0.308 and max_dr < 0.156: z += -1610 × (LHA − 0.308) × (0.156 − max_dr)
if mass_over_sum_pt > 0.068 and dr_7 < 0.042: z += -7530 × (mass_over_sum_pt − 0.068) × (0.042 − dr_7)
if mass > 62.00 and max_dr < 0.176: z += 2.06 × (mass − 62.00) × (0.176 − max_dr)
if mass_over_sum_pt > 0.091 and max_dr < 0.148: z += 9260 × (mass_over_sum_pt − 0.091) × (0.148 − max_dr)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2 < 0.00905`; 2: `e2 < 0.0433`; 3: `girth2 < 0.0126`; 4: `e2 > 0.0278`; 5: `mass_over_sum_pt > 0.0616 and n_dr_0_0p05 < 5.99`; 6: `centroid_offset > 0.0103`):

- `✓✓✓···` **light, very collimated quark/gluon jets** — 26.0% of jets, neuron 0.01, formula right for 64%. About a quarter of all jets: mostly quarks (50%) with gluons 32%; light (14.4 GeV), very narrow, with 86% of the pT inside 0.025 of the axis and little wide-angle radiation. The two narrow-girth penalties (about -7.0 and -5.3) swamp the small-e2 bonus, so the neuron is off (on 1%) and leaves the W and Z scores alone. The formula calls them q and is right 0.636 of the time.
- `✓✓✓··✓` **light narrow mixed jets** — 24.4% of jets, neuron 0.19, formula right for 52%. A mixture: gluons 28%, W 26%, Z 23%, quarks 16%; mass about 23 GeV, narrow, pT largely within 0.05 of the axis. Same narrow-girth penalties with the e2 and centroid bonuses; the value is small (0.19, on 12%), lowering the W and Z scores only slightly. The formula leans g but is right only 0.517 of the time: a confused mixture.
- `···✓✓✓` **wide, heavy top jets** — 13.0% of jets, neuron 2.06, formula right for 83%. Mostly tops (82%) with some gluons; heavy (79.3 GeV), nearly four times the average width, lower pT, with much of the pT beyond 0.1 from the axis. The girth penalties fail; the large-e2 penalty (about -5.7) is mostly offset by the mass-over-pT and centroid bonuses, giving a value of 2.06 (on 58%) that clearly lowers the W and Z scores. The formula calls them t and is right 0.831 of the time.
- `✓✓✓✓✓✓` **medium-mass two-prong Z/W jets** — 10.6% of jets, neuron 0.22, formula right for 66%. Mostly Z (40%) with W 34% and some tops; mass about 50 GeV, average width, 68% of the pT at 0.05-0.1 from the axis. All six tests pass; the girth and e2 penalties outweigh the bonuses, so the value is small (0.22, on 17%) and the W/Z scores are hardly touched. The formula calls them W and is right 0.658 of the time.
- `✓✓✓✓✓·` **compact two-prong W jets** — 9.5% of jets, neuron 0.03, formula right for 77%. Mostly W (57%) with Z 31%; mass about 60 GeV, average width, pT sitting in a ring at 0.025-0.1 from the axis. The same penalties pass but the centroid bonus fails, so the neuron is essentially off (on 5%) and leaves W and Z scores alone. The formula calls them W and is right 0.769 of the time.
- `✓·✓✓✓·` **Z jets with larger e2** — 3.0% of jets, neuron 0.16, formula right for 83%. Mostly Z (78%); mass about 63 GeV, slightly wider than average, 72% of the pT at 0.05-0.1 from the axis. The small-e2 bonus fails and the girth and large-e2 penalties dominate, so the value stays small (0.16, on 24%). The formula calls them Z and is right 0.826 of the time.
- `✓✓✓·✓✓` **two-prong jets with hard leading particle** — 2.3% of jets, neuron 1.12, formula right for 63%. Z is the largest class (39%) with W 24% and tops; mass about 51 GeV, a hard leading particle, and pT at 0.025-0.1 from the axis. The small-e2 bonus (about +3.4) and centroid bonus offset the girth penalties, giving a value of 1.12 (on 48%) that lowers the W and Z scores. The formula calls them Z and is right 0.632 of the time.
- `✓·✓✓✓✓` **Z jets, full two-prong set** — 1.8% of jets, neuron 0.09, formula right for 66%. Mostly Z (62%) with some tops and W; mass about 53 GeV, slightly wider than average, lower pT, 67% of the pT at 0.05-0.1 from the axis. Penalties from girth and large e2 outweigh the mass-over-pT and centroid bonuses, so the value is small (0.09, on 13%). The formula calls them Z and is right 0.665 of the time.
- `··✓✓✓✓` **medium-width top/gluon jets** — 1.7% of jets, neuron 2.29, formula right for 61%. Mostly tops (56%) with gluons 23%; mass about 56 GeV, wider than average, lower pT, with pT spread out to 0.1-0.15. Only the looser girth penalty passes, and the mass-over-pT and centroid bonuses beat the e2 penalty, giving a high value (2.29, on 88%) that lowers the W and Z scores most. The formula calls them t and is right 0.612 of the time.
- `···✓✓·` **wide heavy tops, centred** — 1.4% of jets, neuron 1.75, formula right for 80%. Mostly tops (78%) with some gluons; heaviest pattern (86.9 GeV), very wide, pT spread far from the axis. Like the main top pattern but the centroid bonus fails, giving a value of 1.75 (on 48%) that lowers the W and Z scores. The formula calls them t and is right 0.798 of the time.

### neuron 4: low C2, mass/pT below top (moderate)

- **What it measures:** Pushed up for mass/pT < 0.111 and width > 0.00219, and down for mass/pT > 0.0885, for very thin jets (lam2 < 0.000389) and for C2 > 0.00878; it falls with C2 and D2 (rank correlations -0.515 and -0.421). It is on for almost all g, q, W and Z jets (Z highest at 4.54, then g 4.18, W 4.12, q 3.69) but zero for 35% of tops, which sit lowest (2.95).
- *computed — its value:* largest for Z (4.54), then g (4.18), then W (4.12), then q (3.69), then t (2.95); it separates t jets from the rest best (AUC 0.34: small for t)
- **How the class scores use it:** It raises the Z and t scores and lowers the g and q scores, and does not enter the W score. The q score (its strongest use, -16%) reads a high value as less typical of quarks than of Z, g or W jets; the t score adds it although tops sit lowest on it, so that use is not 'top-likeness' but a small correction alongside the t score's much larger inputs from neurons 13 and 10.
- *computed — used by:* raises the score of Z (+11%), t (+10%); lowers the score of g (-4%), q (-16%); does not (or hardly) enter the score of W (share of each class score’s average input)

```
z = 2.33
if mass_over_sum_pt < 0.111: z += 41.60 × (0.111 − mass_over_sum_pt)
if width > 0.0022: z += 393 × (width − 0.0022)
if lam2 < 0.00039: z += -6470 × (0.00039 − lam2)
if mass_over_sum_pt > 0.088: z += -174 × (mass_over_sum_pt − 0.088)
if tau21 < 0.279: z += 15.50 × (0.279 − tau21)
if C2 > 0.0088: z += -57.40 × (C2 − 0.0088)
if tau21 < 0.285 and mass < 66.20: z += -0.609 × (0.285 − tau21) × (66.20 − mass)
if sum_pt_top5 < 486: z += 0.017 × (486 − sum_pt_top5)
if tau21 < 0.246 and pt_7 > 34.20: z += 0.670 × (0.246 − tau21) × (pt_7 − 34.20)
if C2 > 0.016 and pt_7 > 39.70: z += 11.00 × (C2 − 0.016) × (pt_7 − 39.70)
if max_dr > 0.109 and pt_7 > 39.20: z += -2.35 × (max_dr − 0.109) × (pt_7 − 39.20)
if tau21 < 0.243 and planar_flow > 0.033: z += 54.60 × (0.243 − tau21) × (planar_flow − 0.033)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass_over_sum_pt < 0.111`; 2: `width > 0.00219`; 3: `lam2 < 0.000389`; 4: `mass_over_sum_pt > 0.0885`; 5: `tau21 < 0.279`; 6: `C2 > 0.00878`):

- `✓✓✓·✓✓` **two-prong W/Z jets, low tau21** — 29.9% of jets, neuron 4.31, formula right for 68%. About 30% of jets: mostly W (42%) and Z (36%) with some tops; mass about 52 GeV, slightly narrower than average, with the pT in a ring at 0.025-0.1 from the axis as two prongs give. The low mass/pT, non-narrow width and low-τ21 bonuses outweigh the thin-jet and C2 penalties, giving a high value (4.31, on 99%) that lowers the q and g scores and raises the Z and t scores. The formula calls them W and is right 0.679 of the time.
- `✓·✓··✓` **light collimated quark/gluon jets** — 17.2% of jets, neuron 3.85, formula right for 60%. Mostly quarks (42%) and gluons (36%); light (13.6 GeV), very narrow, with 75% of the pT inside 0.025 of the axis and a fairly hard leading particle. The low mass/pT bonus (about +3.9) beats the thin-jet and C2 penalties, so the value is high (3.85, on 98%), which pushes the g and q scores down and Z and t up; other neurons must undo this. The formula splits them evenly between g and q and is right only 0.603 of the time.
- `✓·✓···` **very light pencil-like quark/gluon jets** — 16.1% of jets, neuron 4.34, formula right for 59%. Mostly quarks (44%) with gluons 33%; very light (5.3 GeV), extremely narrow, 88% of the pT inside 0.025, higher total pT than average. Only the low mass/pT bonus and thin-jet penalty pass, giving a high value (4.34, always on) with the same push away from g and q. The formula calls them q and is right 0.588 of the time, as quarks and gluons are hard to separate here.
- `·✓·✓·✓` **heavy wide three-prong tops** — 6.5% of jets, neuron 0.30, formula right for 91%. Mostly tops (91%); heavy (80.9 GeV), about four times the average width, lower pT spread evenly, with much of the pT beyond 0.1 from the axis. The mass/pT is above the upper cut, so the low-mass/pT bonus fails and the high-mass/pT (about -10.8) and C2 penalties overwhelm the width bonus: the neuron is off (on 14%). Being off is itself the top signature; the formula calls them t and is right 0.911 of the time.
- `✓✓✓✓✓✓` **heavy two-prong Z/top mixture** — 4.7% of jets, neuron 5.20, formula right for 71%. A mixture of Z (44%) and tops (35%) with some gluons; mass about 64 GeV, somewhat wider than average, pT mostly at 0.05-0.1 from the axis. All six tests pass; the width and τ21 bonuses dominate, giving the neuron its highest value (5.20) and the largest boost to the Z and t scores while cutting q and g. The formula calls them Z but is right 0.714 of the time, confusing Z with tops.
- `✓✓✓··✓` **medium-mass mixed jets, high C2** — 4.6% of jets, neuron 2.86, formula right for 54%. A mixture: W 31%, Z 28%, gluons 21%; mass about 36 GeV, slightly narrower than average, pT largely within 0.05 of the axis. The τ21 bonus fails and the C2 penalty is sizeable (about -2.2), so the value is lower (2.86, on 89%). The formula leans W but is right only 0.536 of the time: a confused mixture.
- `·✓✓✓✓✓` **wide top jets, low tau21** — 3.7% of jets, neuron 2.49, formula right for 70%. Mostly tops (66%) with gluons 23%; heavy (82.4 GeV), about three times the average width, pT mostly at 0.05-0.15 from the axis. The high-mass/pT penalty (about -8.3) is offset by the width and τ21 bonuses, leaving a fair value (2.49, on 88%) that raises the t and Z scores. The formula calls them t and is right 0.703 of the time.
- `·✓·✓✓✓` **wide top jets with high C2** — 3.3% of jets, neuron 3.12, formula right for 79%. Mostly tops (78%) with some gluons; heavy (79.5 GeV), very wide, pT spread far from the axis. The large width bonus (about +8.6) and τ21 bonus beat the high-mass/pT and C2 penalties, giving a value of 3.12 (on 71%) that raises the t score. The formula calls them t and is right 0.79 of the time.
- `✓✓···✓` **medium-mass mixture, no class dominant** — 3.3% of jets, neuron 4.54, formula right for 52%. An even mixture of gluons, W and Z (26% each) with tops; mass about 39 GeV, average width, lower pT, pT mostly at 0.025-0.1 from the axis. The low mass/pT and width bonuses beat the C2 penalty, giving a high value (4.54) that lowers the g and q scores. The formula leans W but is right only 0.519 of the time.
- `✓·✓·✓✓` **light narrow quark/gluon jets, low tau21** — 3.2% of jets, neuron 2.82, formula right for 48%. Equal quarks and gluons (34% each) with some W and Z; mass about 25 GeV, narrow, most pT within 0.05 of the axis. The low mass/pT and τ21 bonuses beat the thin-jet and C2 penalties, giving a value of 2.82 that pushes away from g and q. The formula splits them between q and g and is right only 0.479 of the time.

### neuron 5: quark-likeness: pT in few particles (moderate)

- **What it measures:** Pushed up when the 8th-hardest particle carries little of the pT (z_7 < 0.0683, its strongest term) and for small e2 (< 0.0374); it rises with the summed pT of the 2-5 hardest particles and falls with e2 and z_7 (rank correlations about 0.56-0.59 in size). Quarks sit far highest (4.89); Z (2.10), W (2.04) and gluons (1.89) are similar, and tops lowest (1.09).
- *computed — its value:* largest for q (4.89), then Z (2.10), then W (2.04), then g (1.89), then t (1.09); it separates q jets from the rest best (AUC 0.77: large for q)
- **How the class scores use it:** Because quarks sit highest on it and gluons and tops well below them, it raises the q score and lowers the g and t scores: the g score reads it as evidence against a gluon (-15%), the t score as evidence against a top (-13%). It does not (or hardly) enter the W or Z scores.
- *computed — used by:* raises the score of q (+5%); lowers the score of g (-15%), t (-13%); does not (or hardly) enter the score of W, Z (share of each class score’s average input)

```
z = 0.465
if z_7 < 0.068: z += 107 × (0.068 − z_7)
if e2 < 0.037: z += 106 × (0.037 − e2)
if z_7 < 0.071 and centroid_offset < 0.030: z += -3370 × (0.071 − z_7) × (0.030 − centroid_offset)
if width < 0.0027 and centroid_offset < 0.023: z += 75200 × (0.0027 − width) × (0.023 − centroid_offset)
if log_sum_pt > 6.59 and lam1 < 0.012: z += -982 × (log_sum_pt − 6.59) × (0.012 − lam1)
if dr_0 < 0.024: z += -169 × (0.024 − dr_0)
if log_sum_pt > 6.60 and dr_0 < 0.022: z += 757 × (log_sum_pt − 6.60) × (0.022 − dr_0)
if sum_pt_top2 < 546 and girth2_top3 < 0.0038: z += -1.79 × (546 − sum_pt_top2) × (0.0038 − girth2_top3)
if z_7 < 0.033: z += 185 × (0.033 − z_7)
if LHA < 0.221 and log_sum_pt < 6.79: z += -90.90 × (0.221 − LHA) × (6.79 − log_sum_pt)
if e2 < 0.034 and lam2 < 7.1e-05: z += 685000 × (0.034 − e2) × (7.1e-05 − lam2)
if log_sum_pt > 6.89: z += -67.90 × (log_sum_pt − 6.89)
if z_7 < 0.068 and sum_pt < 803: z += -0.278 × (0.068 − z_7) × (803 − sum_pt)
if girth2 < 6.4e-05: z += 31500 × (6.4e-05 − girth2)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `z_7 < 0.0683`; 2: `e2 < 0.0374`; 3: `z_7 < 0.0707 and centroid_offset < 0.0301`; 4: `width < 0.00267 and centroid_offset < 0.0234`; 5: `log_sum_pt > 6.59 and lam1 < 0.0124`; 6: `dr_0 < 0.0238`):

- `✓✓✓✓✓✓` **collimated high-pT quark jets** — 20.1% of jets, neuron 5.90, formula right for 64%. Mostly quarks (57%) with gluons 24%; light (10.7 GeV), extremely narrow (95% of the pT inside 0.025), high total pT (904 GeV), a hard leading particle and a soft 8th particle. All six tests pass; the soft-8th-particle, small-e2 and narrow-width bonuses beat the penalties, giving the neuron its highest value (5.90) that lowers the g and t scores strongly and raises the q score. The formula calls them q and is right 0.635 of the time.
- `✓✓✓·✓·` **high-pT two-prong W/Z jets** — 13.2% of jets, neuron 2.63, formula right for 72%. Mostly W (46%) and Z (39%); mass about 55 GeV, high total pT (845 GeV) with a hard leading particle and a soft 8th, pT mostly at 0.025-0.05 from the axis. The soft-8th-particle and e2 bonuses are partly offset by two penalties, giving a value of 2.63 that lowers the t and g scores. The formula calls them W and is right 0.718 of the time, the W/Z split being the main error.
- `······` **wide low-pT evenly shared jets** — 10.2% of jets, neuron 0.48, formula right for 72%. Mostly tops (54%) with gluons and Z; mass about 61 GeV, wide, low total pT (507 GeV) shared very evenly (the 8th particle is still hard), pT spread beyond 0.05. No test passes, so only the base value remains (0.48, on 97%), with a small cut to the t and g scores. The formula calls them t and is right 0.721 of the time.
- `✓·✓···` **heavy top/Z jets, soft 8th particle** — 9.4% of jets, neuron 0.59, formula right for 76%. Tops are the largest class (48%) with Z 24%; heavy (70.2 GeV), about twice the average width, pT mostly at 0.05-0.1 from the axis. Only the soft-8th-particle bonus and its centroid-linked penalty pass, leaving a small value (0.59, on 82%). The formula calls them t and is right 0.755 of the time.
- `✓✓✓···` **medium-mass W-leaning two-prong jets** — 6.9% of jets, neuron 1.52, formula right for 55%. Mostly W (38%) with Z 26% and tops; mass about 40 GeV, below-average width, pT mostly at 0.025-0.1 from the axis. The soft-8th-particle and e2 bonuses beat the small penalty, giving a value of 1.52 that lowers the t and g scores. The formula calls them W but is right only 0.546 of the time.
- `✓·✓·✓·` **heavy high-pT Z jets** — 5.7% of jets, neuron 0.72, formula right for 83%. Mostly Z (56%) with W 32%; heavy (69.8 GeV), average width, high total pT (824 GeV), 76% of the pT at 0.05-0.1 from the axis. The soft-8th-particle bonus (about +2.8) is mostly cancelled by two penalties, leaving a small value (0.72). The formula calls them Z and is right 0.832 of the time.
- `·✓····` **low-pT evenly shared mixed jets** — 5.1% of jets, neuron 1.26, formula right for 52%. A mixture: gluons 30%, W 26%, Z 21%; mass about 29 GeV, below-average width, low total pT (539 GeV) shared very evenly with a hard 8th particle. Only the small-e2 bonus passes, giving a value of 1.26 that lowers the t and g scores. The formula calls them g but is right only 0.521 of the time: a confused mixture.
- `✓✓✓✓·✓` **collimated lower-pT gluon jets** — 5.1% of jets, neuron 1.10, formula right for 54%. Mostly gluons (53%) with quarks 31%; light (10.2 GeV), very narrow (87% of the pT inside 0.025), lower total pT (640 GeV) shared more evenly than for the quark pattern. Like the quark pattern but the high-pT test fails, and the penalties leave a lower value (1.10, on 64%). The formula calls them g but is right only 0.541 of the time, as many quarks get called gluons.
- `✓·····` **wide heavy tops, soft 8th particle** — 4.7% of jets, neuron 1.28, formula right for 83%. Mostly tops (82%) with some gluons; heavy (77.4 GeV), wide, pT spread well beyond 0.1 from the axis. Only the soft-8th-particle bonus passes, giving a value of 1.28 (on 99%) that slightly lowers the t score, working against these tops. The formula still calls them t and is right 0.828 of the time.
- `✓✓····` **off-centre medium-mass mixture** — 3.7% of jets, neuron 3.15, formula right for 49%. A mixture: tops 28%, gluons 24%, Z 23%; mass about 30 GeV, slightly narrower than average, pT mostly at 0.025-0.1 from the axis. The soft-8th-particle and e2 bonuses pass with no penalty (the centroid is off-axis), giving a high value (3.15) that lowers the t and g scores. The formula splits them between t and Z and is right only 0.488 of the time.

### neuron 8: narrow core, nothing at wide angle (moderate)

- **What it measures:** Pushed up mainly for narrow jets with little pT at 0.2 ≤ ΔR < 0.4 (width < 0.00506 together with z_dr_0p2_0p4 < 0.0996, its strongest term), and down for narrow jets whose pT centroid is off the axis and for very high total pT (log of total pT > 6.71); it falls with width and centroid offset (rank correlations -0.414 and -0.404). Quarks (1.48) and gluons (1.24) sit highest; W (0.45), Z (0.26) and tops (0.21) low.
- *computed — its value:* largest for q (1.48), then g (1.24), then W (0.45), then Z (0.26), then t (0.21); it separates q jets from the rest best (AUC 0.72: large for q)
- **How the class scores use it:** The W score reads a single narrow core as evidence against a W, so it lowers the W score (-4%); it also raises the t score slightly (+3%), a small correction since tops sit lowest on it. Although quarks and gluons sit highest, it does not (or hardly) enter the g, q or Z scores.
- *computed — used by:* raises the score of t (+3%); lowers the score of W (-4%); does not (or hardly) enter the score of g, q, Z (share of each class score’s average input)

```
z = 0.104
if width < 0.0051 and z_dr_0p2_0p4 < 0.100: z += 12900 × (0.0051 − width) × (0.100 − z_dr_0p2_0p4)
if LHA < 0.198 and lam2 < 0.00032: z += -169000 × (0.198 − LHA) × (0.00032 − lam2)
if width < 0.0054 and centroid_offset > 0.006: z += -76700 × (0.0054 − width) × (centroid_offset − 0.006)
if girth2 < 0.0062 and planar_flow < 0.453: z += 1240 × (0.0062 − girth2) × (0.453 − planar_flow)
if log_sum_pt > 6.71: z += -11.60 × (log_sum_pt − 6.71)
if mass < 20.20 and centroid_offset > 0.016: z += -15.20 × (20.20 − mass) × (centroid_offset − 0.016)
if e2 < 0.022 and sum_pt > 830: z += 0.561 × (0.022 − e2) × (sum_pt − 830)
if girth < 0.060 and lam1 > 0.0012: z += -32700 × (0.060 − girth) × (lam1 − 0.0012)
if pt_7 > 37.10: z += -0.043 × (pt_7 − 37.10)
if centroid_offset < 0.0037: z += 477 × (0.0037 − centroid_offset)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.00506 and z_dr_0p2_0p4 < 0.0996`; 2: `LHA < 0.198 and lam2 < 0.000321`; 3: `width < 0.00544 and centroid_offset > 0.00598`; 4: `girth2 < 0.00621 and planar_flow < 0.453`; 5: `log_sum_pt > 6.71`; 6: `mass < 20.2 and centroid_offset > 0.0163`):

- `······` **wide heavy top/Z jets** — 30.7% of jets, neuron 0.10, formula right for 75%. About 31% of jets: mostly tops (53%) with Z 23%; mass about 66 GeV, more than twice the average width, lower pT, pT spread out to 0.1 and beyond. No test passes, leaving only a tiny base value (0.10) with negligible effect on the scores. The formula calls them t and is right 0.746 of the time.
- `✓·✓✓··` **narrow medium-mass W jets** — 10.1% of jets, neuron 0.77, formula right for 55%. Mostly W (42%) with Z 22% and some quarks and gluons; mass about 37 GeV, narrow, pT mostly at 0.025-0.05 from the axis. The narrow-core and girth/planar-flow bonuses slightly beat the off-centre penalty, giving a small value (0.77, on 56%) that nudges the W score down and the t score up. The formula calls them W but is right only 0.551 of the time.
- `✓✓··✓·` **pencil-like very high-pT quark jets** — 7.6% of jets, neuron 0.72, formula right for 73%. Mostly quarks (69%); very light (6.9 GeV), 99% of the pT inside 0.025 of the axis, very high total pT (953 GeV) with one dominant particle. The narrow-core bonus (about +6.4) is offset by the LHA/lam2 and high-pT penalties, leaving a small value (0.73). The formula calls them q and is right 0.732 of the time.
- `···✓··` **two-prong W/Z jets, flat** — 5.3% of jets, neuron 0.23, formula right for 70%. Mostly W (55%) with Z 26%; mass about 50 GeV, close to average width, 64% of the pT at 0.05-0.1 from the axis. Only the small girth/planar-flow test passes with a tiny amount, so the value is small (0.23) and the scores are barely touched. The formula calls them W and is right 0.696 of the time.
- `✓✓✓✓··` **light collimated gluon-leaning jets** — 4.0% of jets, neuron 2.46, formula right for 54%. Mostly gluons (45%) with quarks 32%; light (15.1 GeV), very narrow (80% of the pT in the core), lower total pT (681 GeV) shared evenly. The narrow-core and girth/planar-flow bonuses beat two penalties and the high-pT penalty does not apply, giving the neuron its highest value (2.46) that lowers the W score and raises the t and q scores. The formula calls them g but is right only 0.536 of the time.
- `✓✓✓✓✓·` **narrow high-pT quark/W mixture** — 3.7% of jets, neuron 1.45, formula right for 56%. A mixture: quarks 32%, W 29%, gluons 21%; mass about 26 GeV, narrow, high total pT (922 GeV) with one dominant particle. Like the gluon-leaning pattern but the high-pT penalty passes, trimming the value to 1.45. The formula leans q and is right only 0.561 of the time: a mixture.
- `····✓·` **heavy high-pT Z jets** — 3.7% of jets, neuron 0.04, formula right for 81%. Mostly Z (64%) with W and tops; heavy (81.4 GeV), slightly wider than average, high total pT (893 GeV) with a hard leading particle. Only the high-pT penalty passes, so the neuron is off most of the time (on 9%). The formula calls them Z and is right 0.812 of the time.
- `✓✓·✓✓·` **collimated high-pT quark jets** — 3.5% of jets, neuron 2.29, formula right for 70%. Mostly quarks (63%) with gluons 20%; light (17.2 GeV), very narrow (93% of the pT in the core), very high total pT (955 GeV) with one dominant particle. The narrow-core and girth/planar-flow bonuses outweigh the LHA and high-pT penalties, giving a value of 2.29 that raises the q and t scores and lowers W. The formula calls them q and is right 0.701 of the time.
- `✓·✓✓✓·` **high-pT narrow two-prong W jets** — 3.5% of jets, neuron 0.34, formula right for 68%. Mostly W (52%) with Z 32%; mass about 52 GeV, narrow, high total pT (899 GeV) with a dominant leading particle, 76% of the pT at 0.025-0.05. The bonuses and the off-centre and high-pT penalties nearly cancel, leaving a small value (0.34, on 32%). The formula calls them W and is right 0.681 of the time.
- `✓✓····` **very light gluon/quark jets** — 3.4% of jets, neuron 1.74, formula right for 55%. Gluons (48%) and quarks (43%); very light (6.9 GeV), 96% of the pT in the core, pT shared evenly among the particles. The narrow-core bonus (about +6.3) beats the LHA/lam2 penalty, giving a value of 1.74 that raises the q and t scores. The formula leans g and is right only 0.55 of the time, as quarks and gluons look alike here.

### neuron 11: compact, centred, flat (non-top) jet (moderate)

- **What it measures:** Pushed up for width < 0.0087 and a pT centroid close to the axis (centroid offset < 0.0498), and down for girth < 0.0883; it falls with centroid offset and planar flow (rank correlations -0.387 and -0.364). W jets sit highest (4.30), then Z (3.17), gluons (2.34) and quarks (2.26); tops are lowest (0.85) and at zero for 68% of them.
- *computed — its value:* largest for W (4.30), then Z (3.17), then g (2.34), then q (2.26), then t (0.85); it separates t jets from the rest best (AUC 0.16: small for t)
- **How the class scores use it:** It is the largest input of the W score, which it raises (+24%), since W jets sit highest on it. It does not enter the g, q, Z or t scores; in particular the Z score, though Z jets sit second on it, does not use it.
- *computed — used by:* raises the score of W (+24%); does not (or hardly) enter the score of g, q, Z, t (share of each class score’s average input)

```
z = -1.15
if width < 0.0087: z += 1070 × (0.0087 − width)
if centroid_offset < 0.050: z += 101 × (0.050 − centroid_offset)
if girth < 0.088: z += -84.90 × (0.088 − girth)
if planar_flow < 0.271: z += 8.98 × (0.271 − planar_flow)
if girth > 0.077: z += -81.50 × (girth − 0.077)
if sum_pt_top5 < 688: z += 0.0054 × (688 − sum_pt_top5)
if centroid_offset < 0.044 and log_sum_pt < 6.84: z += -101 × (0.044 − centroid_offset) × (6.84 − log_sum_pt)
if width < 0.0037: z += -514 × (0.0037 − width)
if centroid_offset > 0.014: z += -73.10 × (centroid_offset − 0.014)
if girth > 0.077 and n_pt_above_50 < 7.47: z += 12.60 × (girth − 0.077) × (7.47 − n_pt_above_50)
if planar_flow < 0.217 and width > 0.0053: z += -1310 × (0.217 − planar_flow) × (width − 0.0053)
if planar_flow < 0.281 and max_dr > 0.114: z += -57.90 × (0.281 − planar_flow) × (max_dr − 0.114)
if LHA < 0.157: z += -22.80 × (0.157 − LHA)
if C2 < 0.035: z += -19.10 × (0.035 − C2)
if planar_flow < 0.254 and mass < 66.70: z += -0.128 × (0.254 − planar_flow) × (66.70 − mass)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.0087`; 2: `centroid_offset < 0.0498`; 3: `girth < 0.0883`; 4: `planar_flow < 0.271`; 5: `girth > 0.0766`; 6: `sum_pt_top5 < 688`):

- `✓✓✓✓·✓` **narrow medium-mass W-leaning mixture** — 26.0% of jets, neuron 3.71, formula right for 57%. About 26% of jets: W 35%, Z 23%, gluons 19% and some quarks and tops; mass about 35 GeV, narrow, lower pT, pT largely within 0.1 of the axis. The width, centroid, flat-shape and low-pT bonuses beat the girth penalty, giving a value of 3.72 that raises the W score. The formula calls them W but is right only 0.57 of the time.
- `✓✓✓··✓` **light, evenly shared gluon jets** — 16.7% of jets, neuron 2.60, formula right for 54%. Mostly gluons (46%) with quarks 25%; light (15.9 GeV), 61% of the pT in the core, lower pT shared evenly among the particles. Width and centroid bonuses beat a large girth penalty (the flat-shape test fails), giving a value of 2.60 that raises the W score. The formula calls them g but is right only 0.543 of the time.
- `✓✓✓✓··` **high-pT narrow W/Z jets** — 14.4% of jets, neuron 3.76, formula right for 68%. Mostly W (38%) with Z 30%; mass about 45 GeV, narrow, high total pT (904 GeV) with a dominant leading particle. Width, centroid and flat-shape bonuses beat the girth penalty, giving a value of 3.76 that raises the W score. The formula calls them W and is right 0.676 of the time.
- `✓✓✓···` **collimated high-pT quark jets** — 12.4% of jets, neuron 1.93, formula right for 68%. Mostly quarks (61%) with gluons 20%; light (10.4 GeV), 93% of the pT in the core, high total pT (939 GeV) with one dominant particle. The large width and centroid bonuses are largely cancelled by the girth penalty, leaving a value of 1.93 that still raises the W score. The formula calls them q and is right 0.685 of the time.
- `·✓·✓✓✓` **wide top jets, girth window** — 7.6% of jets, neuron 0.23, formula right for 72%. Mostly tops (68%) with gluons 18%; heavy (75.3 GeV), about three times the average width, pT spread beyond 0.1. The width bonus fails and the large-girth penalty (about -3.9) beats the other bonuses, so the value is small (0.23, on 18%). The formula calls them t and is right 0.724 of the time.
- `✓✓✓✓✓✓` **compact two-prong Z jets** — 6.5% of jets, neuron 3.86, formula right for 73%. Mostly Z (55%) with W 27%; mass about 56 GeV, near-average width, 79% of the pT at 0.05-0.1 from the axis. All tests pass; the centroid and flat-shape bonuses dominate, giving a value of 3.86 that raises the W score. The formula calls them Z and is right 0.729 of the time.
- `·✓··✓✓` **wide heavy tops, off** — 5.6% of jets, neuron 0.12, formula right for 90%. Mostly tops (89%); heavy (79.5 GeV), very wide, pT spread well beyond 0.1. The large-girth penalty (about -5.0) outweighs the centroid and low-pT bonuses, so the neuron is off most of the time (on 15%). The formula calls them t and is right 0.897 of the time.
- `···✓✓✓` **wide off-centre top/gluon jets** — 2.0% of jets, neuron 0.00, formula right for 68%. Mostly tops (65%) with gluons 25%; mass about 64 GeV, very wide, pT spread far from the axis with an off-centre centroid. The centroid bonus fails and the large-girth penalty wins, so the neuron is off entirely and adds nothing. The formula calls them t and is right 0.678 of the time.
- `····✓✓` **wide off-centre top jets** — 2.0% of jets, neuron 0.00, formula right for 86%. Mostly tops (87%); mass about 65 GeV, very wide, pT spread far from the axis. Only the girth penalty and low-pT bonus pass, so the neuron is off entirely. The formula calls them t and is right 0.863 of the time.
- `✓✓✓✓✓·` **heavy high-pT Z jets** — 1.5% of jets, neuron 4.86, formula right for 87%. Mostly Z (72%) with W 22%; heavy (74 GeV), near-average width, high total pT (878 GeV), 78% of the pT at 0.05-0.1. The centroid and flat-shape bonuses dominate, giving the neuron its highest value (4.86) and the biggest boost to the W score, even though these are Z. The formula still calls them Z and is right 0.869 of the time.

### neuron 15: slightly wider than a W (moderate)

- **What it measures:** Switched off for narrow jets (width < 0.00695, its strongest term) and pushed up for lam1 < 0.00679 and small e2 (< 0.041), so it responds to jets just wider than the typical W but not broad; it follows lam1 and width (rank correlations 0.44 and 0.438). Z jets sit highest (1.41), then tops (0.96), with gluons (0.37), quarks (0.24) and W (0.21) low.
- *computed — its value:* largest for Z (1.41), then t (0.96), then g (0.37), then q (0.24), then W (0.21); it separates Z jets from the rest best (AUC 0.73: large for Z)
- **How the class scores use it:** W jets sit lowest on it, so the W score reads it as evidence against a W and it lowers the W score (-11%); it also lowers the Z score, but with a smaller share (-4%), even though Z jets sit highest. It does not (or hardly) enter the g, q or t scores.
- *computed — used by:* lowers the score of W (-11%), Z (-4%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 0.951
if width < 0.0069: z += -2070 × (0.0069 − width)
if lam1 < 0.0068: z += 1610 × (0.0068 − lam1)
if lam1 < 0.0081: z += -790 × (0.0081 − lam1)
if e2 < 0.041: z += 104 × (0.041 − e2)
if e2 < 0.024: z += 199 × (0.024 − e2)
if z_dr_0p1_0p2 < 0.342: z += 3.61 × (0.342 − z_dr_0p1_0p2)
if tau21 < 0.240 and z_dr_0p2_0p4 < 0.210: z += 62.20 × (0.240 − tau21) × (0.210 − z_dr_0p2_0p4)
if LHA > 0.342: z += -54.80 × (LHA − 0.342)
if mass < 37.40: z += -0.046 × (37.40 − mass)
if girth2_top3 < 0.002: z += -665 × (0.002 − girth2_top3)
if n_dr_0_0p05 < 2.12: z += 0.454 × (2.12 − n_dr_0_0p05)
if LHA > 0.186 and sum_pt_top3 > 338: z += 0.031 × (LHA − 0.186) × (sum_pt_top3 − 338)
if width < 0.0079 and e2 > 0.024: z += -35800 × (0.0079 − width) × (e2 − 0.024)
if D2 < 0.711: z += -1.98 × (0.711 − D2)
if width < 0.0087 and planar_flow < 0.075: z += -3420 × (0.0087 − width) × (0.075 − planar_flow)
if width < 0.0061 and log_sum_pt > 6.90: z += -7700 × (0.0061 − width) × (log_sum_pt − 6.90)
if log_sum_pt > 6.90: z += 37.60 × (log_sum_pt − 6.90)
if z_dr_0p05_0p1 > 0.757: z += -6.11 × (z_dr_0p05_0p1 − 0.757)
if tau21 < 0.260 and z_dr_0p05_0p1 < 0.513: z += -9.02 × (0.260 − tau21) × (0.513 − z_dr_0p05_0p1)
if mass > 80.40 and z_dr_0p2_0p4 < 0.236: z += -0.572 × (mass − 80.40) × (0.236 − z_dr_0p2_0p4)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `width < 0.00695`; 2: `lam1 < 0.00679`; 3: `lam1 < 0.00813`; 4: `e2 < 0.041`; 5: `e2 < 0.0244`; 6: `z_dr_0p1_0p2 < 0.342`):

- `✓✓✓✓✓✓` **light narrow quark/gluon jets** — 49.1% of jets, neuron 0.17, formula right for 58%. Almost half of all jets: quarks 34%, gluons 30%, with W and Z; light (18.3 GeV), narrow, 63% of the pT in the core. The narrow-width penalty (about -11.7) cancels the lam1 and e2 bonuses, so the value is tiny (0.17, on 14%). The formula splits them between q and g and is right 0.581 of the time.
- `✓✓✓✓·✓` **two-prong W jets, narrow** — 19.9% of jets, neuron 0.44, formula right for 66%. Mostly W (50%) with Z 27%; mass about 50 GeV, below-average width, pT mostly at 0.025-0.1. Still under the width cut, so the penalty keeps the value small (0.44, on 39%) and the W score is lowered only a little. The formula calls them W and is right 0.664 of the time.
- `······` **wide heavy tops, nothing passes** — 11.8% of jets, neuron 0.52, formula right for 80%. Mostly tops (74%) with some gluons and Z; mass about 77 GeV, more than three times the average width, pT mostly at 0.1-0.15. No test passes; the base value is small (0.52, on 28%). The formula calls them t and is right 0.796 of the time.
- `·····✓` **wide top jets, little mid-angle pT** — 6.8% of jets, neuron 1.73, formula right for 80%. Mostly tops (71%) with gluons and Z; mass about 74 GeV, nearly three times the average width, pT mostly at 0.05-0.1 with a tail far out. Only the mid-angle test passes, giving a value of 1.73 (on 79%) that lowers the W score by about 1.2. The formula calls them t and is right 0.801 of the time.
- `··✓··✓` **slightly-wider-than-W Z jets** — 3.1% of jets, neuron 2.53, formula right for 80%. Mostly Z (77%); mass about 60.6 GeV, a bit wider than average, 78% of the pT at 0.05-0.1 from the axis. No narrow-width penalty; the mid-angle bonus beats a small lam1 penalty, giving a value of 2.53 that lowers the W score by about 1.7 and Z a little. The formula calls them Z and is right 0.796 of the time.
- `··✓✓·✓` **Z/top jets, small e2** — 2.6% of jets, neuron 2.84, formula right for 75%. Mostly Z (66%) with tops 19%; mass about 61 GeV, a bit wider than average, fairly hard leading particle, pT mostly at 0.025-0.1. The e2 and mid-angle bonuses beat the lam1 penalty, giving a value of 2.84 that lowers the W score by about 2. The formula calls them Z and is right 0.754 of the time.
- `✓✓✓··✓` **W jets near width cut** — 1.7% of jets, neuron 0.42, formula right for 67%. Mostly W (63%) with Z 23%; mass about 51.5 GeV, near-average width, 81% of the pT at 0.05-0.1. The narrow-width penalty (about -1.1) is small here and the lam1 penalty offsets the bonuses, leaving a small value (0.42, on 51%). The formula calls them W and is right 0.672 of the time.
- `···✓·✓` **medium-width top/gluon jets** — 1.6% of jets, neuron 3.54, formula right for 60%. Mostly tops (53%) with gluons 25% and quarks 16%; mass about 63 GeV, wider than average, a fairly hard leading particle, pT mostly at 0.05-0.1. The e2 and mid-angle bonuses with no penalty give the neuron its highest value (3.54), lowering the W score by about 2.4. The formula calls them t but is right only 0.595 of the time.
- `··✓···` **Z jets, larger e2** — 1.1% of jets, neuron 2.55, formula right for 75%. Mostly Z (73%) with tops and W; mass about 61 GeV, a bit wider than average, pT at 0.05-0.15 from the axis. Only the lam1 penalty passes, yet the base value stays high (2.55), lowering the W score by about 1.8. The formula calls them Z and is right 0.754 of the time.
- `···✓··` **rare low-pT wide top/gluon jets** — 0.3% of jets, neuron 1.21, formula right for 66%. A rare pattern: mostly tops (66%) with gluons 25%; mass about 49 GeV, more than twice the average width, lower pT, 71% of the pT at 0.1-0.15. Only the e2 bonus passes, giving a value of 1.21 that lowers the W score. The formula calls them t and is right 0.655 of the time.

### neuron 12: very wide jet, many hard particles (minor)

- **What it measures:** Almost always zero: it needs girth2 > 0.0188 (pushes up) and is pushed down strongly for e2 > 0.0622; it follows the number of particles above 10 GeV (rank correlation 0.843). Only tops reach it with any frequency (non-zero for 16% of them), so tops sit highest (0.24), then gluons (0.09) and quarks (0.03), with W and Z at 0.00.
- *computed — its value:* largest for t (0.24), then g (0.09), then q (0.03), then W (0.00), then Z (0.00); it separates t jets from the rest best (AUC 0.58: large for t)
- **How the class scores use it:** It does not (or hardly) enter any of the five class scores, so it has essentially no effect on the classification.
- *computed — used by:* ; does not (or hardly) enter the score of g, q, W, Z, t (share of each class score’s average input)

```
z = -0.910
if e2 > 0.062: z += -124 × (e2 − 0.062)
if girth2 > 0.019: z += 220 × (girth2 − 0.019)
if girth2 > 0.020 and pt_7 > 16.10: z += 6.92 × (girth2 − 0.020) × (pt_7 − 16.10)
if mass > 91.20: z += 0.078 × (mass − 91.20)
if girth2 > 0.019 and lam2 > 0.00049: z += 15300 × (girth2 − 0.019) × (lam2 − 0.00049)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `e2 > 0.0622`; 2: `girth2 > 0.0188`; 3: `girth2 > 0.0197 and pt_7 > 16.1`; 4: `mass > 91.2`; 5: `girth2 > 0.0186 and lam2 > 0.000489`):

- `·····` **all non-wide jets (neuron off)** — 88.3% of jets, neuron 0.00, formula right for 63%. 88% of all jets: a mixture of g, q, W and Z (21-23% each) with fewer tops (12%); mass about 35 GeV, narrower than average, pT sharing like the average jet. No test passes, so the neuron is off and adds nothing to any score; it only matters for the rare very wide jets. The formula gets 0.63 of these right using other neurons.
- `✓✓✓·✓` **very wide low-pT tops** — 4.2% of jets, neuron 0.45, formula right for 89%. Mostly tops (88%); mass about 74 GeV, about four times the average width, the lowest total pT (474 GeV) shared very evenly, with most pT beyond 0.1 from the axis. The large-e2 penalty (about -2.6) is offset by the three wide-girth bonuses, giving a small value (0.45, on 31%) that slightly lowers the t score, working against these tops. The formula still calls them t and is right 0.886 of the time.
- `✓✓✓✓✓` **very wide, very heavy tops** — 2.2% of jets, neuron 1.43, formula right for 91%. Mostly tops (91%); very heavy (104.5 GeV, above the Z mass), more than four times the average width, pT spread far from the axis. All five tests pass; the girth and heavy-mass bonuses beat the e2 penalty, giving a value of 1.43 (on 72%) that lowers the t score. The formula still calls them t and is right 0.912 of the time.
- `✓····` **wide tops with large e2 only** — 1.1% of jets, neuron 0.00, formula right for 77%. Mostly tops (76%) with gluons 18%; mass about 67 GeV, more than twice the average width, pT mostly at 0.1-0.15 from the axis. Only the large-e2 penalty passes, so the neuron is off and adds nothing. The formula calls them t and is right 0.768 of the time.
- `✓✓✓··` **very wide low-pT top/gluon jets** — 1.0% of jets, neuron 0.27, formula right for 71%. Mostly tops (70%) with gluons 21%; mass about 76 GeV, about four times the average width, low pT shared evenly, pT mostly beyond 0.1. The e2 penalty nearly cancels the two girth bonuses, leaving a small value (0.27, on 25%). The formula calls them t and is right 0.713 of the time.
- `✓✓✓✓·` **very heavy wide top/gluon jets** — 0.8% of jets, neuron 1.54, formula right for 72%. Mostly tops (60%) with gluons 26%; the heaviest pattern (108.6 GeV), very wide, pT spread far from the axis. Girth and heavy-mass bonuses beat the e2 penalty, giving a value of 1.55 (on 69%) that lowers the t score. The formula calls them t and is right 0.723 of the time, with the gluons often mistaken for tops.
- `···✓·` **heavy high-pT top/gluon jets** — 0.5% of jets, neuron 0.27, formula right for 71%. Mostly tops (57%) with gluons 26%; heavy (101 GeV) but only about twice the average width, high total pT (881 GeV) with a dominant leading particle. Only the heavy-mass bonus passes, giving a small value (0.27, on 25%). The formula calls them t but is right only 0.71 of the time, as the gluons here look like tops.
- `·✓✓·✓` **wide tops, small e2** — 0.3% of jets, neuron 0.51, formula right for 84%. A rare pattern: mostly tops (82%) with gluons; mass about 67 GeV, wide, pT mostly at 0.1-0.15 from the axis. The girth bonuses pass without the e2 penalty, giving a value of 0.51 (on 44%) that slightly lowers the t score. The formula calls them t and is right 0.837 of the time.
- `✓✓··✓` **wide tops just above girth cut** — 0.3% of jets, neuron 0.00, formula right for 89%. A rare pattern: mostly tops (88%); mass about 69 GeV, three times the average width, pT spread beyond 0.05. The e2 penalty outweighs tiny girth bonuses, so the neuron is off. The formula calls them t and is right 0.889 of the time.
- `✓··✓·` **heavy tops, large e2** — 0.2% of jets, neuron 0.13, formula right for 84%. A rare pattern: mostly tops (82%); heavy (102.6 GeV), wider than average, higher pT, half of the pT at 0.1-0.15 from the axis. The heavy-mass bonus is largely cancelled by the e2 penalty, leaving a small value (0.13, on 19%). The formula calls them t and is right 0.844 of the time.
