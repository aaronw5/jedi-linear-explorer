# What each part of the 399-term formula does (64 particles)

*the simplified formula closest to the start formula (within 0.1 point on validation jets)*. Validation accuracy 81.39%. Words written by an AI agent from the numbers (60,000 training jets) and checked against them; lines marked *computed* come straight from the numbers. Plots: the page, tab "What each part does".

## Summary

Each jet is placed on 16 scales, and each class score adds some scales and subtracts others. Gluon and quark jets are told apart mainly by gluon-likeness (many particles sharing the pT thinly, neuron 1), which the g score adds and the q score subtracts; both light-QCD scores subtract heavy two-prong-ness (neuron 4) and add light one-prong scales (9, 6, 12). W and Z jets are marked by compact, few-particle, two-prong structure (neurons 5, 3) and by the absence of busy, wide radiation (neuron 8, which both boson scores subtract strongly). W and Z are then split by narrow mass windows around 80.4, 91.2 and 101 GeV: W-side mass (0) and the 80-91 GeV scale (11) raise the W score (0 also lowers the Z score), while the 91-101 GeV window (7) raises the Z score and mass just above the Z (14) lowers the W score. Top jets are recognised by hard particles spread far from the axis in a heavy jet (neuron 10) and by busy wide radiation (8), and the t score is pulled down strongly by the high-pT, below-top-mass scale (13).

## The 5 class scores

### score g: Many soft particles, no heavy prongs

High for jets with many particles, one-prong and without a heavy two-prong mass: gluon jets score highest (mean 3.05 for g, AUC 0.93), quark jets next, top jets near zero and W and Z jets far below.

Adds gluon-likeness (neuron 1, +43%) and light one-prong (9, +10%), with small additions from 6 and 12; subtracts heavy two-prong-ness (4, -22%), the sparse-jet scale (3, -9%) and the hard-core scale (5, -8%).

*computed:* largest for g (3.05), then q (0.76), then t (-0.03), then Z (-2.24), then W (-2.56); it separates g jets from the rest best (AUC 0.93: large for g)

### score q: Light, one-prong jet with few particles

High for light one-prong jets that are not particle-rich: quark jets score highest (mean 2.68 for q, AUC 0.89), gluon jets next, top jets near zero, Z and W jets below.

Subtracts heavy two-prong-ness (neuron 4, -40%), gluon-likeness (1, -20%) and the 80-91 GeV two-prong scale (11, -7%); adds light one-prong (9, +17%), one-prong outside the Z mass (6, +7%) and lightness (12, +7%).

*computed:* largest for q (2.68), then g (1.14), then t (0.08), then Z (-0.75), then W (-0.77); it separates q jets from the rest best (AUC 0.89: large for q)

### score W: Compact two-prong jet at the W mass

High for compact two-prong jets with mass up to about the W: W jets score highest (mean 3.55 for W, AUC 0.97), quark and Z jets below zero, gluon and especially top jets far below.

Subtracts the busy wide-radiation scale (neuron 8, -34%) and mass just above the Z (14, -14%), plus small amounts of 7, 12 and 9; adds the hard-core scale (5, +11%), the 80-91 GeV two-prong scale (11, +8%), W-side mass (0, +7%), heavy two-prong-ness (4, +6%) and the sparse-jet scale (3, +4%).

*computed:* largest for W (3.55), then q (-0.29), then Z (-1.40), then g (-2.28), then t (-5.36); it separates W jets from the rest best (AUC 0.97: large for W)

### score Z: Compact two-prong jet at the Z mass

High for compact two-prong jets at or just above 91 GeV: Z jets score highest (mean 3.49 for Z, AUC 0.95), quark and W jets slightly below zero, gluon and especially top jets far below.

Subtracts the busy wide-radiation scale (neuron 8, -37%), one-prong outside the Z mass (6, -15%), W-side mass (0, -14%) and a little of 2; adds the hard-core scale (5, +13%), the 91-101 GeV window (7, +9%) and small amounts of 3, 12 and 15.

*computed:* largest for Z (3.49), then q (-0.17), then W (-0.29), then g (-2.07), then t (-5.71); it separates Z jets from the rest best (AUC 0.95: large for Z)

### score t: Heavy jet with widely spread hard prongs

High for heavy jets whose hard particles are spread far from the axis: top jets score highest (mean 3.36 for t, AUC 0.95), W and gluon jets slightly below zero, Z and quark jets further below.

Subtracts the high-pT, below-top-mass scale (neuron 13, -38%), the hard-core scale (5, -10%) and small amounts of 12 and 7; adds spread-out hard particles (10, +27%), the busy wide-radiation scale (8, +10%) and a little heavy two-prong-ness (4, +4%).

*computed:* largest for t (3.36), then W (-0.20), then g (-0.36), then Z (-1.10), then q (-1.35); it separates t jets from the rest best (AUC 0.95: large for t)

## The 16 neurons (most important first)

### neuron 1: Gluon-likeness: many soft particles (major)

- **What it measures:** Grows with the number of particles and with how thinly the pT is shared among them (a small pT share held by the 30-40 hardest particles). Gluon jets sit far highest (mean 5.89 for g, AUC 0.93), top jets next, then quark jets, with W and Z jets lowest.
- *computed — its value:* largest for g (5.89), then t (2.76), then q (2.23), then Z (1.55), then W (1.39); it separates g jets from the rest best (AUC 0.93: large for g)
- **How the class scores use it:** It raises the g score (+43%) and lowers the q score (-20%), making it the main gluon-versus-quark handle; freezing it costs 12.064 points. The W, Z and t scores hardly use it, even though top jets are fairly high on it.
- *computed — used by:* raises the score of g (+43%); lowers the score of q (-20%); does not (or hardly) enter the score of W, Z, t (share of each class score’s average input)

```
z = 2.19
if log_sum_pt > 6.91: z += 30.00 × (log_sum_pt − 6.91)
if log_sum_pt > 6.89: z += 18.70 × (log_sum_pt − 6.89)
if z_top50_slots > 0.959: z += -36.50 × (z_top50_slots − 0.959)
if LHA < 0.411: z += 7.47 × (0.411 − LHA)
if sum_pt_top2 < 668: z += 0.0035 × (668 − sum_pt_top2)
if log_sum_pt > 6.81: z += -6.45 × (log_sum_pt − 6.81)
if sum_pt_top50 > 960: z += -0.010 × (sum_pt_top50 − 960)
if tau32 > 0.328: z += 2.09 × (tau32 − 0.328)
if z_top20_slots < 0.952: z += -10.70 × (0.952 − z_top20_slots)
if n_pt_above_10 < 31.30: z += -0.063 × (31.30 − n_pt_above_10)
if mass_top30 < 80.70: z += 0.050 × (80.70 − mass_top30)
if mass_top50 < 117: z += -0.020 × (117 − mass_top50)
if max_dr < 0.435: z += -7.22 × (0.435 − max_dr)
if sum_pt_top30 < 1080: z += 0.0051 × (1080 − sum_pt_top30)
if mass_top30 < 80.80 and mass_top5 < 68.20: z += -0.00053 × (80.80 − mass_top30) × (68.20 − mass_top5)
if log_sum_pt > 6.99: z += -20.40 × (log_sum_pt − 6.99)
if max_dr < 0.433 and z_dr_0p2_0p4 < 0.191: z += 28.80 × (0.433 − max_dr) × (0.191 − z_dr_0p2_0p4)
if n_dr_0p2_0p4 < 13.30: z += -0.045 × (13.30 − n_dr_0p2_0p4)
if n_particles > 37.80 and dr_0 < 0.143: z += 0.297 × (n_particles − 37.80) × (0.143 − dr_0)
if z_top30_slots > 0.940 and mass_top10 < 92.70: z += -0.169 × (z_top30_slots − 0.940) × (92.70 − mass_top10)
if pt_9 < 35.20: z += -0.026 × (35.20 − pt_9)
if mass_over_sum_pt < 0.074: z += 21.70 × (0.074 − mass_over_sum_pt)
if mass_top20 < 41.10: z += -0.048 × (41.10 − mass_top20)
if lam2 < 0.00084: z += -719 × (0.00084 − lam2)
if n_particles > 37.70: z += 0.015 × (n_particles − 37.70)
if n_particles > 38.20 and z_top50_slots < 0.986: z += 1.71 × (n_particles − 38.20) × (0.986 − z_top50_slots)
if girth2_top3 < 0.00085: z += 766 × (0.00085 − girth2_top3)
if sum_pt_top2 < 701 and n_dr_0p2_0p4 < 6.95: z += -0.00024 × (701 − sum_pt_top2) × (6.95 − n_dr_0p2_0p4)
if girth2_top20 < 0.0011: z += 1080 × (0.0011 − girth2_top20)
if girth2_top3 < 0.00084 and n_dr_0p05_0p1 < 10.40: z += -102 × (0.00084 − girth2_top3) × (10.40 − n_dr_0p05_0p1)
if mass_top20 < 40.50 and n_real_top40 > 26.60: z += 0.0029 × (40.50 − mass_top20) × (n_real_top40 − 26.60)
if z_top30_slots > 0.943 and m012 > 13.70: z += 0.373 × (z_top30_slots − 0.943) × (m012 − 13.70)
if girth2_top15 < 0.0029: z += 120 × (0.0029 − girth2_top15)
if n_dr_0p1_0p2 < 7.22 and dr_6 < 0.078: z += -1.59 × (7.22 − n_dr_0p1_0p2) × (0.078 − dr_6)
if D2 < 1.18: z += 0.651 × (1.18 − D2)
if log_sum_pt > 7.13: z += -2.33 × (log_sum_pt − 7.13)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `log_sum_pt > 6.91`; 2: `log_sum_pt > 6.89`; 3: `z_top50_slots > 0.959`; 4: `LHA < 0.411`; 5: `sum_pt_top2 < 668`; 6: `log_sum_pt > 6.81`):

- `✓✓✓✓✓✓` **Bulk: all tests pass** — 59.1% of jets, neuron 2.89, formula right for 83%. The majority of jets (59.12%): a mixture of every class (27% W, 27% Z, 21% g, 16% q, 8% t) with high total pT, mean mass 82.6 GeV and average pT sharing and spread. All six tests pass; the positive total-pT, LHA and top-2-pT amounts outweigh the negative ones, giving a solid neuron value (mean 2.893) that adds +1.808 to g and takes a little from q. This is a baseline shift the formula corrects with other terms; the decisions mirror the class mix and are right 83.3% of the time.
- `··✓✓✓✓` **Lower-pT tops and quarks** — 9.7% of jets, neuron 2.37, formula right for 73%. Jets with lower total pT (mean 955 GeV): top-led mixture (43% t, 27% q, 16% g), mean mass 85.5 GeV, somewhat broader than average. The two higher total-pT tests fail, so only LHA, top-2-pT and the lowest pT cut contribute; the neuron is still on (mean 2.366), adding to g and slightly lowering q. The formula calls them t about half the time and q next, right 73.4% — a mixed, error-prone group.
- `·✓✓✓✓✓` **Mid-pT mixed jets** — 9.3% of jets, neuron 1.41, formula right for 77%. Jets whose total pT sits between the cuts (mean 994 GeV): a mixture with no dominant class (29% q, 23% W, 23% Z, 17% t), mean mass 78.9 GeV, average pT sharing. Of the three total-pT cuts only the middle one passes (+0.214), so the neuron is lower (mean 1.413) and adds less to g. The formula calls them q most often (33.6%) and is right 76.9% of the time.
- `✓✓✓✓·✓` **One dominant hard particle** — 5.3% of jets, neuron 2.03, formula right for 79%. Mostly quark jets (44%) with W, Z and gluons, light (mean 60.5 GeV) and very collimated: the hardest particle carries about 591 GeV, far above the usual 240, and about two thirds of the pT sits in the core. The 'two hardest carry < 668 GeV' test fails, losing its bonus, but the big total-pT amounts (+3.397, +2.491) keep the neuron on (mean 2.032). It adds to g and lowers q somewhat; the formula calls them q (51.8%) and is right 78.8% of the time.
- `··✓✓✓·` **Low-pT soft, many-particle jets** — 3.6% of jets, neuron 3.50, formula right for 66%. Low total pT jets (mean 816 GeV) that also fail the lowest pT cut: a three-way mixture of tops (36%), gluons (34%) and quarks (29%), mean mass 71 GeV, with softer particles throughout. Losing the negative lowest-pT amount leaves LHA (+1.222) and top-2-pT (+1.334) against the -1.256 of the top-50 share, so the neuron is high (mean 3.497) and adds 2.186 to g. The formula splits them between t and g and is right only 66.2% of the time — one of the harder groups.
- `✓✓✓·✓✓` **High-pT broad tops** — 3.5% of jets, neuron 2.65, formula right for 89%. Mostly tops (82%), heavy (mean 179 GeV) and wide, with almost no pT at the very core and most of it at medium-to-large radius; high total pT. The LHA test fails (angularly broad jets), so its bonus is missing, but the total-pT tests keep the neuron on (mean 2.647), adding to g and lowering q. The formula calls them t and is right 88.9% of the time.
- `✓✓·✓✓✓` **High-multiplicity gluon jets** — 1.9% of jets, neuron 7.34, formula right for 85%. Mostly gluons (80%) with some tops (14%): many particles share the pT (soft leader of 123 GeV, the top 50 carry less than 95.9% of the pT), mass 126 GeV, high total pT. The top-50-share test fails, so its -1.3 penalty is absent while all pT tests add large amounts; the neuron reaches its highest value here (mean 7.339), adding +4.587 to g and taking 1.376 from q. The formula calls them g and is right 84.7% of the time.
- `··✓·✓✓` **Low-pT broad tops** — 1.9% of jets, neuron 2.16, formula right for 93%. Mostly tops (93%), heavy (mean 165.6 GeV), wide, lower total pT (954 GeV), with pT spread out at medium-to-large radius. The higher pT cuts and LHA fail; top-2-pT (+1.47) keeps the neuron on (mean 2.158), adding to g. The formula calls them t anyway and is right 93.2% of the time.
- `·✓✓·✓✓` **Mid-pT broad tops** — 1.2% of jets, neuron 1.64, formula right for 94%. Mostly tops (93%), heavy (mean 170 GeV) and wide, total pT near 993 GeV, little pT near the axis. Like the previous group but the middle pT cut adds +0.198; the neuron stays on (mean 1.639) with a modest push to g. The formula calls them t and is right 93.6% of the time.
- `···✓✓✓` **Low-pT gluon/top many-particle** — 0.8% of jets, neuron 4.92, formula right for 69%. A gluon-top mixture (44% g, 43% t), mass 122 GeV, low total pT (951 GeV) with the pT thinly shared among many particles (leader only about 99 GeV). The pT and top-50-share tests fail, leaving LHA and a large top-2-pT bonus (+1.734): the neuron is high (mean 4.915), adding +3.072 to g. The formula splits almost evenly between g and t and is right only 68.8% of the time.

### neuron 4: Heavy two-prong-ness (major)

- **What it measures:** Grows with the mass of the hardest 10-20 particles and with e2, and with small D2 (a two-prong pattern); jets lighter than 80.4 GeV or with a broad, soft spread (large LHA) are pushed down. Z and W jets sit highest, top jets next, gluon jets low and quark jets lowest (AUC 0.16 for q: small for q).
- *computed — its value:* largest for Z (1.68), then W (1.63), then t (1.15), then g (0.31), then q (0.15); it separates q jets from the rest best (AUC 0.16: small for q)
- **How the class scores use it:** It lowers the q score (-40%) and the g score (-22%) strongly, since a heavy pronged jet is not a light QCD jet, and it raises the W (+6%) and t (+4%) scores a little. The Z score hardly uses it.
- *computed — used by:* raises the score of W (+6%), t (+4%); lowers the score of g (-22%), q (-40%); does not (or hardly) enter the score of Z (share of each class score’s average input)

```
z = 1.87
if mass < 80.40: z += -0.128 × (80.40 − mass)
if LHA > 0.114: z += -7.88 × (LHA − 0.114)
if girth < 0.121: z += -20.30 × (0.121 − girth)
if mass < 101: z += 0.038 × (101 − mass)
if D2 < 6.92: z += 0.185 × (6.92 − D2)
if girth2_top15 < 0.016: z += 72.30 × (0.016 − girth2_top15)
if width > 0.0097: z += 163 × (width − 0.0097)
if mass < 120: z += 0.013 × (120 − mass)
if girth2_top40 < 0.013: z += 73.60 × (0.013 − girth2_top40)
if mass_top40 < 84.30 and D2 < 6.61: z += -0.014 × (84.30 − mass_top40) × (6.61 − D2)
if lam1 > 0.0076: z += -158 × (lam1 − 0.0076)
if z_dr_0p2_0p4 < 0.069: z += -10.30 × (0.069 − z_dr_0p2_0p4)
if mass_top40 < 95.90: z += -0.017 × (95.90 − mass_top40)
if girth2_top15 < 0.0073: z += -132 × (0.0073 − girth2_top15)
if mass < 122 and max_dr < 0.403: z += 0.141 × (122 − mass) × (0.403 − max_dr)
if girth < 0.061: z += -26.50 × (0.061 − girth)
if n_dr_0p2_0p4 < 15.40: z += 0.042 × (15.40 − n_dr_0p2_0p4)
if sum_pt < 1070: z += -0.0054 × (1070 − sum_pt)
if n_particles > 28.20: z += -0.013 × (n_particles − 28.20)
if mass < 74.40 and max_dr < 0.388: z += -0.535 × (74.40 − mass) × (0.388 − max_dr)
if e2 > 0.037: z += 40.80 × (e2 − 0.037)
if n_dr_0p2_0p4 < 14.60 and max_dr < 0.436: z += -0.209 × (14.60 − n_dr_0p2_0p4) × (0.436 − max_dr)
if z_dr_0p2_0p4 < 0.194: z += 1.09 × (0.194 − z_dr_0p2_0p4)
if tau21 < 0.465: z += -1.24 × (0.465 − tau21)
if planar_flow < 0.425: z += 0.978 × (0.425 − planar_flow)
if lam2 > 0.0024: z += -173 × (lam2 − 0.0024)
if tau32 < 0.577: z += 2.23 × (0.577 − tau32)
if C2 > 0.110: z += 15.40 × (C2 − 0.110)
if mass > 143: z += 0.015 × (mass − 143)
if mass_top20 > 106: z += -0.016 × (mass_top20 − 106)
if z_top5_slots > 0.569: z += -0.777 × (z_top5_slots − 0.569)
if z_top5_slots < 0.548: z += 0.793 × (0.548 − z_top5_slots)
if planar_flow < 0.303 and n_dr_0p05_0p1 > 6.21: z += -0.104 × (0.303 − planar_flow) × (n_dr_0p05_0p1 − 6.21)
if n_dr_0p2_0p4 < 15.20 and n_dr_0p1_0p2 > 11.90: z += -0.0012 × (15.20 − n_dr_0p2_0p4) × (n_dr_0p1_0p2 − 11.90)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass < 80.4`; 2: `LHA > 0.114`; 3: `girth < 0.121`; 4: `mass < 101`; 5: `D2 < 6.92`; 6: `girth2_top15 < 0.0159`):

- `·✓✓✓✓✓` **Z-mass two-prong jets** — 31.8% of jets, neuron 1.69, formula right for 86%. About a third of jets (31.78%): mostly Z (56%) with W (23%), mass between 80.4 and 101 GeV (mean 88.4 GeV), typical two-prong spread with pT at small-to-medium radius. The mass < 101, low-D2 and compact-core tests add about 2.2 while the broad-LHA and girth tests take off about 2.4, leaving the neuron high (mean 1.685); it lowers g and q strongly and raises W and t. The formula calls them Z and is right 86% of the time.
- `✓✓✓✓✓✓` **Sub-80 GeV mixed jets** — 31.0% of jets, neuron 0.64, formula right for 78%. A mixture of light jets (39% W, 28% g, 25% q), mass below 80.4 GeV (mean 63.4 GeV), more core-heavy than average. All tests pass, but 'mass < 80.4' (-2.178) and the girth/LHA penalties outweigh the bonuses, so the neuron is on for only 41.7% (mean 0.635). The formula calls them W most often (40.4%) with g and q close behind, right 77.9% of the time.
- `·✓··✓·` **Heavy wide top jets** — 13.5% of jets, neuron 1.31, formula right for 87%. Mostly tops (83%), heavy (mean 168.8 GeV), wide, with a soft leader and pT spread well away from the axis. Only the broad-LHA (-2.432) and low-D2 (+0.904) tests pass, yet the neuron is usually on (mean 1.309) from its intercept, lowering g and q and raising W and t. The formula calls them t and is right 87.4% of the time.
- `·✓✓·✓✓` **Heavy gluon/top mixture** — 8.9% of jets, neuron 0.65, formula right for 71%. A gluon-top mixture (43% g, 39% t, 14% q), mass around 125 GeV, higher total pT, pT at medium radius. LHA and girth penalties against D2 and compact-core bonuses give a middling neuron (mean 0.649). The formula splits them between g and t and is right only 71.1% of the time — this is where gluon/top confusion lives.
- `✓·✓✓·✓` **Extremely collimated one-prong quarks** — 6.9% of jets, neuron 0.00, formula right for 80%. Mostly quark jets (77%), very light (mean 30.8 GeV), with one dominant particle (about 412 GeV) and about 95% of the pT in the innermost ring. Small LHA and large D2 fail, and 'mass < 80.4' (-6.345) overwhelms the other bonuses, so the neuron is off and does nothing. The formula calls them q and is right 79.6% of the time.
- `✓·✓✓✓✓` **Collimated light quark/gluon jets** — 2.8% of jets, neuron 0.00, formula right for 79%. Mostly quark jets (60%) with gluons (31%), very light (mean 29.4 GeV) and core-dominated (92% innermost), slightly higher total pT. As in the previous group, 'mass < 80.4' (-6.533) switches the neuron off. The formula calls them q (73.3%) and is right 79.1% of the time; the gluons are the main error.
- `✓✓✓✓·✓` **Narrow light quark/gluon mix** — 2.2% of jets, neuron 0.02, formula right for 66%. A mixture of quarks (42%) and gluons (35%) with some W and Z, mass around 57 GeV, a hard leader and about 87% of the pT in the core, failing the low-D2 test. The mass and girth penalties dominate, so the neuron is nearly always off (on 6%). The formula calls them q (58%) and is right only 65.5% of the time — quark/gluon confusion.
- `·✓··✓✓` **Wide tops with compact core** — 1.2% of jets, neuron 0.69, formula right for 77%. Mostly tops (71%) with gluons (22%), heavy (mean 145.6 GeV), wide, pT spread to medium-to-large radius. The LHA penalty (-2.157) is partly offset by low D2 and a small compact-core bonus, giving a middling neuron (mean 0.687). The formula calls them t and is right 77.2% of the time.
- `·✓✓·✓·` **Tops with a harder leader** — 0.9% of jets, neuron 1.35, formula right for 80%. Mostly tops (72%) with gluons (16%), heavy (mean 152 GeV), with a harder leading particle than typical tops. LHA (-1.794) and girth (-0.181) against D2 (+0.814) leave the neuron fairly high (mean 1.352), lowering g and q. The formula calls them t and is right 80.2% of the time.
- `·✓✓✓·✓` **Core-heavy gluons near 90 GeV** — 0.5% of jets, neuron 0.29, formula right for 82%. Mostly gluons (78%), mass near 90 GeV (mean 89.5 GeV) with high total pT, core-heavy (about two thirds of the pT innermost) and failing the low-D2 test. The girth penalty (-1.608) cancels the compact-core bonus, so the neuron is small (mean 0.288). The formula calls them g and is right 81.7% of the time.

### neuron 5: Hard-core, few-particle jets (major)

- **What it measures:** Rises when a few of the hardest particles carry most of the pT (fewer particles in total) and for mass above 61.6 GeV; it is also shaped by many thresholds on the total pT between about 900 and 1020 GeV. Quark and Z jets sit highest, W jets next, top and gluon jets lowest (AUC 0.27 for g: small for g).
- *computed — its value:* largest for q (1.44), then Z (1.40), then W (1.13), then t (0.56), then g (0.50); it separates g jets from the rest best (AUC 0.27: small for g)
- **How the class scores use it:** It raises the W (+11%) and Z (+13%) scores and lowers the g (-8%) and t (-10%) scores: a compact, few-particle jet with some mass is boson-like, not gluon- or top-like. The q score hardly uses it, although quark jets sit high on it.
- *computed — used by:* raises the score of W (+11%), Z (+13%); lowers the score of g (-8%), t (-10%); does not (or hardly) enter the score of q (share of each class score’s average input)

```
z = -1.06
if sum_pt_top40 > 905: z += 0.014 × (sum_pt_top40 − 905)
if log_sum_pt > 6.91: z += -32.90 × (log_sum_pt − 6.91)
if log_sum_pt > 6.85: z += 12.70 × (log_sum_pt − 6.85)
if sum_pt_top40 > 1010: z += -0.019 × (sum_pt_top40 − 1010)
if sum_pt_top40 < 1010: z += 0.022 × (1010 − sum_pt_top40)
if mass > 61.60: z += 0.019 × (mass − 61.60)
if sum_pt_top50 < 1020: z += -0.022 × (1020 − sum_pt_top50)
if mass_top30 > 68.90: z += 0.026 × (mass_top30 − 68.90)
if sum_pt_top50 > 1020: z += 0.011 × (sum_pt_top50 − 1020)
if mass_top50 > 90.50: z += -0.021 × (mass_top50 − 90.50)
if mass_top50 > 156: z += -0.166 × (mass_top50 − 156)
if n_particles < 61.70 and e2 < 0.037: z += 1.27 × (61.70 − n_particles) × (0.037 − e2)
if z_top30_slots > 0.933: z += -5.52 × (z_top30_slots − 0.933)
if sum_pt_top50 > 1060: z += -0.0061 × (sum_pt_top50 − 1060)
if max_dr > 0.435: z += 20.40 × (max_dr − 0.435)
if mass_top30 > 107: z += -0.024 × (mass_top30 − 107)
if mass_over_sum_pt > 0.089: z += -8.94 × (mass_over_sum_pt − 0.089)
if sum_pt_top10 > 840: z += 0.0034 × (sum_pt_top10 − 840)
if mass_top10 < 62.50: z += 0.0054 × (62.50 − mass_top10)
if girth2_top30 < 0.019 and tau32 < 0.866: z += 92.70 × (0.019 − girth2_top30) × (0.866 − tau32)
if mass_over_sum_pt_sq > 0.029: z += -444 × (mass_over_sum_pt_sq − 0.029)
if n_particles < 64.00 and mass_top5 > 11.10: z += -0.00026 × (64.00 − n_particles) × (mass_top5 − 11.10)
if mass > 173: z += -0.107 × (mass − 173)
if log_sum_pt > 7.14: z += 11.40 × (log_sum_pt − 7.14)
if sum_pt_top3 > 318 and n_dr_0p1_0p2 > 7.87: z += 7.6e-05 × (sum_pt_top3 − 318) × (n_dr_0p1_0p2 − 7.87)
if max_dr > 0.278 and tau21 < 0.582: z += -2.61 × (max_dr − 0.278) × (0.582 − tau21)
if z_top30_slots < 0.864: z += -7.78 × (0.864 − z_top30_slots)
if sum_pt_top10 > 994: z += -0.0032 × (sum_pt_top10 − 994)
if mass_top50 > 157 and z_dr_0p05_0p1 > 0.589: z += 1.55 × (mass_top50 − 157) × (z_dr_0p05_0p1 − 0.589)
if sum_pt_top3 > 794: z += -0.0031 × (sum_pt_top3 − 794)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `sum_pt_top40 > 905`; 2: `log_sum_pt > 6.91`; 3: `log_sum_pt > 6.85`; 4: `sum_pt_top40 > 1.01e+03`; 5: `sum_pt_top40 < 1.01e+03`; 6: `mass > 61.6`):

- `✓✓✓✓·✓` **High-pT W/Z-led mixture** — 39.5% of jets, neuron 0.88, formula right for 86%. The largest group (39.49%): a mixture of W (33%), Z (32%), gluons (20%) and some tops, mean mass 97.4 GeV, high total pT (1105 GeV) with average pT sharing. The 905 GeV and middle total-pT bonuses are cancelled by the higher total-pT and 'top-40 > 1010' penalties, so the mass bonus (+0.685) and intercept leave a moderate neuron (mean 0.884) that raises W and Z and lowers g and t. The formula's decisions follow the mix and are right 86.3% of the time.
- `✓✓✓·✓✓` **Mid-pT heavy mixed jets** — 14.9% of jets, neuron 1.28, formula right for 83%. A mixture with no dominant class (30% t, 25% Z, 22% W, 15% g), mean mass 112 GeV, total pT near 1023 GeV but less than 1010 GeV in the top 40 particles. The 905 GeV, middle-pT, 'top-40 < 1010' and mass tests add up to a fairly high neuron (mean 1.285), raising W and Z and lowering t. The formula calls them t most often (29.6%) and is right 82.6% of the time.
- `✓✓✓✓··` **High-pT light quark jets** — 13.3% of jets, neuron 1.26, formula right for 77%. Mostly quark jets (53%) with gluons (36%), light (mean 39.7 GeV, below 61.6), high total pT, one dominant particle and about 84% of the pT in the core. Same pT pattern as the largest group but no mass bonus; the neuron is moderately high (mean 1.256), raising W and Z. The formula calls them q (65.9%) and is right 76.6%, with gluons the usual error.
- `✓·✓·✓✓` **Lower-pT heavy top-led jets** — 12.9% of jets, neuron 1.00, formula right for 79%. Mostly tops (44%) with W and Z (19% each), mean mass 109 GeV, total pT below 1010 GeV. The 905 GeV cut, lower total-pT cut, 'top-40 < 1010' (+1.03) and mass bonus give a neuron near 1 (mean 0.996). The formula calls them t (45.8%) and is right 78.7% of the time.
- `✓·✓·✓·` **Lower-pT light quark jets** — 5.3% of jets, neuron 1.55, formula right for 75%. Mostly quark jets (72%) with gluons (13%), light (mean 37.5 GeV), total pT below 1010 GeV, core-dominated with one hard particle. The 905 GeV, middle-pT and 'top-40 < 1010' bonuses without penalties make the neuron high (mean 1.555), raising W and Z and lowering g and t. The formula calls them q and is right 75.4% of the time.
- `····✓✓` **Low-pT heavy tops and gluons** — 5.1% of jets, neuron 0.23, formula right for 72%. Mostly tops (63%) with gluons (26%), mean mass 118 GeV, low total pT (870 GeV), soft leader and pT spread outward. The 'top-40 < 1010' test adds a large +4.24 plus the mass bonus, but the neuron is on for only about half (mean 0.235), since all higher pT cuts fail. The formula calls them t and is right 71.5% of the time.
- `··✓·✓✓` **Many-particle heavy tops** — 2.5% of jets, neuron 0.69, formula right for 78%. Mostly tops (64%) with gluons (26%), heavy (mean 141.8 GeV), pT thinly shared (leader about 112 GeV), so the top 40 carry less than 905 GeV. The 'top-40 < 1010' (+2.983) and mass (+1.532) bonuses give a middling neuron (mean 0.694). The formula calls them t and is right 77.5% of the time.
- `✓✓✓·✓·` **Light quarks near 1 TeV** — 2.4% of jets, neuron 1.82, formula right for 76%. Mostly quark jets (64%) with gluons (23%), light (mean 41.2 GeV), total pT near 1012 GeV, core-heavy. The pT bonuses add up with only a small penalty, so the neuron reaches its highest mean here (1.818), raising W and Z and lowering g and t. The formula calls them q and is right 76.3% of the time.
- `····✓·` **Low-pT light quark/gluon mix** — 1.7% of jets, neuron 0.15, formula right for 67%. An even quark-gluon mixture (46% q, 45% g), light (mean 41.2 GeV), low total pT (797 GeV), core-heavy. Only 'top-40 < 1010' passes (+4.981); the neuron is usually off (on 23%). The formula calls them g slightly more often and is right only 67.4% of the time — a hard quark/gluon split.
- `✓···✓✓` **Lower-pT heavy tops** — 1.3% of jets, neuron 0.14, formula right for 79%. Mostly tops (74%), mean mass 105.7 GeV, total pT near 930 GeV. Although the 'top-40 < 1010' (+1.978) and mass (+0.842) bonuses pass, the higher pT cuts fail and the neuron is often off (on 30.8%, mean 0.14). The formula calls them t and is right 78.8% of the time.

### neuron 8: Busy, wide radiation pattern (major)

- **What it measures:** Grows with the number and pT share of particles at 0.2 <= ΔR < 0.4, with the minor-axis width lam2 and with the total particle count: radiation spread over a broad area. Top jets sit far highest (mean 6.60 for t, AUC 0.91), gluon jets next, quark jets lower, Z and W jets near zero.
- *computed — its value:* largest for t (6.60), then g (2.24), then q (1.00), then Z (0.28), then W (0.08); it separates t jets from the rest best (AUC 0.91: large for t)
- **How the class scores use it:** It lowers the W (-34%) and Z (-37%) scores, because a two-prong boson is compact with an empty outer ring, and raises the t score (+10%). The g and q scores hardly use it.
- *computed — used by:* raises the score of t (+10%); lowers the score of W (-34%), Z (-37%); does not (or hardly) enter the score of g, q (share of each class score’s average input)

```
z = 0.672
if mass > 101: z += -0.107 × (mass − 101)
if mass > 80.40: z += 0.058 × (mass − 80.40)
if mass_over_sum_pt < 0.099: z += -46.70 × (0.099 − mass_over_sum_pt)
if girth < 0.097: z += 24.60 × (0.097 − girth)
if mass_over_sum_pt > 0.075 and sum_pt < 1110: z += 0.355 × (mass_over_sum_pt − 0.075) × (1110 − sum_pt)
if mass_top50 > 82.60: z += -0.044 × (mass_top50 − 82.60)
if n_dr_0p2_0p4 < 20.50: z += -0.061 × (20.50 − n_dr_0p2_0p4)
if mass > 91.20: z += 0.048 × (mass − 91.20)
if mass_over_sum_pt > 0.089: z += 34.00 × (mass_over_sum_pt − 0.089)
if mass_over_sum_pt_sq < 0.013: z += -70.90 × (0.013 − mass_over_sum_pt_sq)
if lam2 < 0.0015: z += -585 × (0.0015 − lam2)
if mass_top50 > 98.10: z += 0.035 × (mass_top50 − 98.10)
if girth2_top30 < 0.0076: z += 162 × (0.0076 − girth2_top30)
if girth2_top20 > 0.0081: z += 130 × (girth2_top20 − 0.0081)
if z_dr_0p2_0p4 < 0.091: z += 6.20 × (0.091 − z_dr_0p2_0p4)
if sum_pt < 1010: z += 0.015 × (1010 − sum_pt)
if n_particles > 50.70: z += 0.068 × (n_particles − 50.70)
if e2 > 0.026: z += -20.90 × (e2 − 0.026)
if mass < 64.60: z += 0.033 × (64.60 − mass)
if mass > 140: z += -0.037 × (mass − 140)
if sum_pt_top50 < 1080: z += -0.0021 × (1080 − sum_pt_top50)
if girth2_top40 > 0.0052 and sum_pt_top30 < 912: z += 0.710 × (girth2_top40 − 0.0052) × (912 − sum_pt_top30)
if n_particles > 51.10 and z_top50_slots > 0.971: z += -2.94 × (n_particles − 51.10) × (z_top50_slots − 0.971)
if sum_pt_top40 < 995: z += 0.0044 × (995 − sum_pt_top40)
if sum_pt_top40 < 967 and log_sum_pt < 6.82: z += 0.068 × (967 − sum_pt_top40) × (6.82 − log_sum_pt)
if z_dr_0p1_0p2 < 0.144: z += 1.52 × (0.144 − z_dr_0p1_0p2)
if D2 < 1.81: z += 0.305 × (1.81 − D2)
if sum_pt_top40 < 1010 and max_dr < 0.392: z += -0.085 × (1010 − sum_pt_top40) × (0.392 − max_dr)
if sum_pt < 1010 and n_real_top50 < 43.50: z += -0.0012 × (1010 − sum_pt) × (43.50 − n_real_top50)
if lam2 < 0.0014 and n_dr_0p05_0p1 > 4.52: z += 17.50 × (0.0014 − lam2) × (n_dr_0p05_0p1 − 4.52)
if C2 > 0.072: z += 4.39 × (C2 − 0.072)
if mass > 85.70 and log_sum_pt < 6.91: z += 0.112 × (mass − 85.70) × (6.91 − log_sum_pt)
if sum_pt_top40 > 1060: z += 0.0013 × (sum_pt_top40 − 1060)
if n_dr_0p2_0p4 < 15.90 and z_dr_0p1_0p2 > 0.300: z += 0.150 × (15.90 − n_dr_0p2_0p4) × (z_dr_0p1_0p2 − 0.300)
if z_dr_0p1_0p2 > 0.212 and mean_phi > 0.00054: z += -1950 × (z_dr_0p1_0p2 − 0.212) × (mean_phi − 0.00054)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass > 101`; 2: `mass > 80.4`; 3: `mass_over_sum_pt < 0.0988`; 4: `girth < 0.0968`; 5: `mass_over_sum_pt > 0.0754 and sum_pt < 1.11e+03`; 6: `mass_top50 > 82.6`):

- `··✓✓··` **Light narrow quark/gluon jets** — 33.5% of jets, neuron 0.38, formula right for 75%. The largest group (33.47%): mostly quark jets (46%) with gluons (31%) and some W, light (mean 49.3 GeV), narrow and core-heavy with a hard leader. Only the low m/pT penalty (-2.434) and the small-girth bonus (+1.708) pass, so the neuron is small (mean 0.379) and trims W and Z slightly. The formula calls them q and is right 74.9% of the time.
- `·✓✓✓✓✓` **Z-mass compact jets** — 20.7% of jets, neuron 0.44, formula right for 88%. Mostly Z jets (77%), mass between 80.4 and 101 GeV (mean 90.1 GeV), typical two-prong spread. The bonuses only slightly exceed the penalties, so the neuron is small (mean 0.438, on 46.8%) with a mild cut to W and Z. The formula calls them Z and is right 88% of the time.
- `✓✓··✓✓` **Heavy wide top jets** — 17.2% of jets, neuron 7.97, formula right for 84%. Mostly tops (81%) with gluons (11%), heavy (mean 155.9 GeV), wide, high m/pT, soft leader and pT spread far out. The 'mass > 80.4' (+4.381) and 'm/pT > 0.0754 with pT < 1110' (+3.67) bonuses roughly cancel the 'mass > 101' and top-50 mass penalties, and the base value makes the neuron very large (mean 7.972). It strongly lowers W (-6.976) and Z (-7.474) and raises t: a veto on boson labels. The formula calls them t and is right 83.9% of the time.
- `··✓✓✓·` **W jets below 80 GeV** — 9.3% of jets, neuron 0.50, formula right for 88%. Mostly W jets (80%), mass below 80.4 GeV (mean 78.1 GeV), compact two-prong jets with slightly lower total pT. The small-girth bonus nearly cancels the low m/pT penalty, so the neuron is mostly off (on 21.4%). The formula calls them W and is right 87.6% of the time.
- `·✓✓✓✓·` **W jets just above 80** — 6.2% of jets, neuron 0.45, formula right for 83%. Mostly W jets (70%), mass just above 80.4 GeV (mean 82 GeV) with the top-50 mass not above 82.6 GeV, typical two-prong spread. Bonuses and penalties nearly cancel; the neuron is mostly off (on 29.6%). The formula calls them W and is right 82.6% of the time.
- `✓✓·✓✓✓` **Mid-heavy narrow mixed jets** — 2.6% of jets, neuron 4.96, formula right for 64%. A mixture of tops (39%), gluons (33%) and quarks (22%), mass above 101 GeV (mean 114.9 GeV), fairly narrow girth but high m/pT. 'mass > 80.4' (+2.002) and the m/pT-with-lower-pT test (+1.532) outweigh the penalties, giving a large neuron (mean 4.957) that strongly lowers W and Z and raises t. The formula calls them t (44.2%) or g and is right only 64.5% of the time — a confused group.
- `·✓✓✓·✓` **High-pT Z/gluon mixture** — 2.6% of jets, neuron 0.64, formula right for 84%. A Z-gluon mixture (51% Z, 31% g), mass near the Z (mean 91.2 GeV) but high total pT (1219.5 GeV), pT fairly concentrated. Failing the m/pT-with-lower-pT test leaves small bonuses and penalties; the neuron is middling (mean 0.643), cutting W and Z a little. The formula calls them Z (53.1%) or g and is right 83.5% of the time.
- `✓✓···✓` **Very heavy high-pT gluons/tops** — 2.5% of jets, neuron 2.92, formula right for 78%. A gluon-top mixture (54% g, 39% t), very heavy (mean 181 GeV), high total pT (1240 GeV), wide. 'mass > 101' (-8.562) and top-50 mass (-4.04) penalties outweigh 'mass > 80.4' (+5.836), but the neuron still sits high (mean 2.921), lowering W and Z. The formula calls them g (61.6%) and is right 77.5% of the time.
- `·✓✓✓··` **High-pT W/gluon split** — 1.5% of jets, neuron 0.64, formula right for 91%. An even W-gluon mixture (49% W, 44% g), mass near the W (mean 83.1 GeV), high total pT (1200.6 GeV). The small-girth bonus (+1.089) roughly cancels the low m/pT penalty (-1.351); the neuron is middling (mean 0.638). The formula calls them W (53.1%) or g and gets them right 90.6% of the time, so other terms separate these well.
- `✓✓✓✓·✓` **Very high-pT heavy gluons** — 1.3% of jets, neuron 2.15, formula right for 83%. Mostly gluons (84%), mass around 116 GeV, very high total pT (1351.7 GeV), fairly narrow. 'mass > 80.4' (+2.076) and the girth bonus roughly cancel the penalties, and the base value keeps the neuron on (mean 2.153), lowering W and Z. The formula calls them g and is right 83.4% of the time.

### neuron 10: Spread-out hard particles, heavy mass (major)

- **What it measures:** Grows when the hardest particles sit far from the jet axis (large girth of the 5 hardest, little pT within ΔR < 0.05, large LHA and e2) and for mass above 121 GeV. Top jets sit highest (AUC 0.85), W, Z and gluon jets in the middle, quark jets lowest.
- *computed — its value:* largest for t (2.30), then Z (1.10), then W (1.02), then g (1.02), then q (0.66); it separates t jets from the rest best (AUC 0.85: large for t)
- **How the class scores use it:** Only the t score uses it, raising it (+27%): three spread-out prongs in a heavy jet are the main positive top signature; freezing it costs 1.736 points.
- *computed — used by:* raises the score of t (+27%); does not (or hardly) enter the score of g, q, W, Z (share of each class score’s average input)

```
z = 4.78
if girth2_top5 < 0.025: z += -69.30 × (0.025 − girth2_top5)
if mass < 121: z += -0.032 × (121 − mass)
if e2 < 0.066: z += -24.80 × (0.066 − e2)
if mass < 86.40: z += 0.050 × (86.40 − mass)
if z_dr_0_0p05 > 0.767: z += -10.40 × (z_dr_0_0p05 − 0.767)
if mass < 80.40: z += 0.050 × (80.40 − mass)
if z_dr_0p2_0p4 < 0.089: z += 9.17 × (0.089 − z_dr_0p2_0p4)
if mass > 144: z += -0.107 × (mass − 144)
if girth < 0.123: z += -6.56 × (0.123 − girth)
if n_dr_0p2_0p4 < 13.10: z += -0.062 × (13.10 − n_dr_0p2_0p4)
if mass_top50 > 137: z += 0.087 × (mass_top50 − 137)
if girth2_top5 < 0.024 and sum_pt_top3 < 655: z += 0.107 × (0.024 − girth2_top5) × (655 − sum_pt_top3)
if mass < 120 and tau21 < 0.464: z += 0.102 × (120 − mass) × (0.464 − tau21)
if lam1 > 0.0022: z += -51.80 × (lam1 − 0.0022)
if mass_top10 < 81.30: z += -0.0081 × (81.30 − mass_top10)
if girth2_top30 < 0.0053: z += 198 × (0.0053 − girth2_top30)
if e2 < 0.067 and z_dr_0p1_0p2 < 0.218: z += -37.50 × (0.067 − e2) × (0.218 − z_dr_0p1_0p2)
if max_dr < 0.402: z += -3.11 × (0.402 − max_dr)
if mass < 63.00: z += -0.032 × (63.00 − mass)
if n_dr_0p2_0p4 < 5.96: z += -0.084 × (5.96 − n_dr_0p2_0p4)
if sum_pt_top10 > 677: z += -0.001 × (sum_pt_top10 − 677)
if dr_0 < 0.064 and n_dr_0p2_0p4 > 2.93: z += 0.885 × (0.064 − dr_0) × (n_dr_0p2_0p4 − 2.93)
if mass > 162: z += -0.059 × (mass − 162)
if sum_pt_top50 < 959: z += -0.0086 × (959 − sum_pt_top50)
if m012 < 47.40: z += -0.0024 × (47.40 − m012)
if mass < 114 and D2 < 2.16: z += -0.0061 × (114 − mass) × (2.16 − D2)
if z_dr_0p2_0p4 < 0.085 and max_dr > 0.265: z += 11.60 × (0.085 − z_dr_0p2_0p4) × (max_dr − 0.265)
if max_dr < 0.240: z += 8.14 × (0.240 − max_dr)
if mass_top50 > 162 and D2 > -0.418: z += 0.012 × (mass_top50 − 162) × (D2 − -0.418)
if sum_pt_top10 < 671: z += 0.00093 × (671 − sum_pt_top10)
if mass_top50 > 172 and sum_pt < 1240: z += -0.00032 × (mass_top50 − 172) × (1240 − sum_pt)
if lam1 > 0.0052 and pt_dispersion > 0.276: z += -194 × (lam1 − 0.0052) × (pt_dispersion − 0.276)
if mass_top10 > 89.10: z += 0.0085 × (mass_top10 − 89.10)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `girth2_top5 < 0.0253`; 2: `mass < 121`; 3: `e2 < 0.0663`; 4: `mass < 86.4`; 5: `z_dr_0_0p05 > 0.767`; 6: `mass < 80.4`):

- `✓✓✓✓✓✓` **Light core-heavy quark/gluon jets** — 30.8% of jets, neuron 0.47, formula right for 76%. The largest group (30.84%): mostly quark jets (47%) with gluons (30%) and W (16%), light (mean 48.1 GeV), with about three quarters of the pT in the innermost ring. All tests pass; the compact-hardest-five, mass < 121, e2 and core-share penalties outweigh the low-mass bonuses, so the neuron is small (mean 0.469) and adds only a little to t. The formula calls them q and is right 75.7% of the time.
- `✓✓✓···` **86-121 GeV Z jets** — 21.1% of jets, neuron 1.56, formula right for 85%. Mostly Z jets (63%) with tops (15%) and gluons (14%), mass between 86.4 and 121 GeV (mean 95.5 GeV), typical two-prong spread. Only the three compactness/mass penalties apply and the intercept keeps the neuron on (mean 1.559), raising t (+1.535). The formula still calls them Z and is right 85.3% of the time.
- `✓·✓···` **Heavy tops and gluons** — 12.7% of jets, neuron 2.23, formula right for 80%. Mostly tops (66%) with gluons (26%), mass above 121 GeV (mean 154.7 GeV), wide. Only the compact-hardest-five (-0.877) and e2 (-0.448) penalties apply, so the neuron is high (mean 2.232), raising t. The formula calls them t and is right 80.2% of the time; gluons are the main error.
- `✓✓✓✓·✓` **W jets below 80 GeV** — 12.0% of jets, neuron 1.49, formula right for 82%. Mostly W jets (66%) with gluons (15%) and quarks (11%), mass below 80.4 GeV (mean 74.7 GeV), compact two-prong spread. The penalties are partly offset by the low-mass bonuses, and the neuron is on (mean 1.491), adding to t. The formula calls them W and is right 82.4% of the time.
- `✓✓✓✓··` **W jets, 80-86 GeV** — 7.7% of jets, neuron 1.34, formula right for 82%. Mostly W jets (69%) with some tops and Z, mass between 80.4 and 86.4 GeV (mean 82.5 GeV). Similar to the sub-80 W group with a smaller mass bonus; the neuron is on (mean 1.34), adding to t. The formula calls them W and is right 82.5% of the time.
- `✓✓✓·✓·` **Core-heavy Z-mass jets** — 5.3% of jets, neuron 0.25, formula right for 84%. Mostly Z jets (62%) with gluons (21%), mass around 93.5 GeV but with a hard leader and most of the pT within 0.05 of the axis. The extra core-share penalty (-0.743) drops the neuron to small values (mean 0.25, on 41.2%). The formula calls them Z and is right 84.3% of the time.
- `✓✓✓✓✓·` **Core-heavy W-mass jets** — 3.2% of jets, neuron 0.25, formula right for 76%. Mostly W jets (50%) with Z (21%) and gluons (15%), mass 80.4-86.4 GeV, hard leader and most pT within 0.05 of the axis. The core-share penalty (-0.831) keeps the neuron small (mean 0.25). The formula calls them W and is right only 75.5% of the time, confusing some with Z and gluons.
- `··✓···` **Very wide heavy tops** — 2.4% of jets, neuron 1.95, formula right for 85%. Mostly tops (77%) with gluons (18%), heavy (mean 174.8 GeV), wide, soft leader and pT spread out among many particles. Only a small e2 penalty (-0.244) applies; the neuron is high (mean 1.947), raising t. The formula calls them t and is right 84.8% of the time.
- `✓·····` **Heavy tops, large e2** — 2.3% of jets, neuron 2.85, formula right for 95%. Almost pure tops (94%), heavy (mean 168.8 GeV), wide, with large e2. Only the compact-hardest-five penalty (-0.453) applies, so the neuron reaches its highest mean here (2.854), adding +2.809 to t. The formula calls them t and is right 95.1% of the time.
- `······` **Very heavy, very wide tops** — 2.1% of jets, neuron 2.31, formula right for 91%. Mostly tops (86%), very heavy (mean 180.2 GeV) and very wide, with pT pushed far from the axis. No test passes, so the neuron sits at its intercept (mean 2.307), raising t. The formula calls them t and is right 90.8% of the time.

### neuron 0: W-side mass, below the Z (moderate)

- **What it measures:** Pushed up for jets lighter than 80.4 GeV (and m/pT below about 0.077) and cut back sharply for masses between 80.4 and 91.2 GeV, the Z side of the W peak; overall it falls as mass and width grow. W jets sit far highest on it (mean 1.78, AUC 0.96), quark and gluon jets low, Z and top jets lowest.
- *computed — its value:* largest for W (1.78), then q (0.37), then g (0.25), then Z (0.12), then t (0.09); it separates W jets from the rest best (AUC 0.96: large for W)
- **How the class scores use it:** It raises the W score (+7%) and lowers the Z score (-14%): being high on this scale is evidence for a W rather than a Z. The g, q and t scores hardly use it.
- *computed — used by:* raises the score of W (+7%); lowers the score of Z (-14%); does not (or hardly) enter the score of g, q, t (share of each class score’s average input)

```
z = 0.972
if mass > 80.40: z += -0.154 × (mass − 80.40)
if mass > 91.20: z += 0.156 × (mass − 91.20)
if mass_over_sum_pt_sq < 0.0083: z += 539 × (0.0083 − mass_over_sum_pt_sq)
if mass_over_sum_pt > 0.077: z += -65.80 × (mass_over_sum_pt − 0.077)
if mass_over_sum_pt > 0.084: z += 72.10 × (mass_over_sum_pt − 0.084)
if girth < 0.057: z += -48.80 × (0.057 − girth)
if girth2_top40 < 0.0062: z += -238 × (0.0062 − girth2_top40)
if mass_top50 < 81.90: z += -0.025 × (81.90 − mass_top50)
if girth2_top20 < 0.0063: z += -146 × (0.0063 − girth2_top20)
if lam1 < 0.0059: z += -187 × (0.0059 − lam1)
if log_sum_pt < 7.02: z += 2.53 × (7.02 − log_sum_pt)
if z_top30_slots > 0.918: z += -3.34 × (z_top30_slots − 0.918)
if LHA < 0.255: z += 3.98 × (0.255 − LHA)
if n_dr_0p2_0p4 < 10.20: z += 0.037 × (10.20 − n_dr_0p2_0p4)
if girth2_top40 < 0.006 and girth2_top3 < 0.0029: z += 41900 × (0.006 − girth2_top40) × (0.0029 − girth2_top3)
if sum_pt < 1010 and z_dr_0p2_0p4 < 0.207: z += -0.038 × (1010 − sum_pt) × (0.207 − z_dr_0p2_0p4)
if mass > 80.40 and n_dr_0p2_0p4 < 6.83: z += -0.010 × (mass − 80.40) × (6.83 − n_dr_0p2_0p4)
if n_particles < 47.80: z += 0.0098 × (47.80 − n_particles)
if mass_top50 < 80.00 and z_dr_0p05_0p1 < 0.208: z += 0.039 × (80.00 − mass_top50) × (0.208 − z_dr_0p05_0p1)
if log_sum_pt < 6.99 and sum_pt_top40 > 961: z += 0.045 × (6.99 − log_sum_pt) × (sum_pt_top40 − 961)
if z_dr_0_0p05 > 0.878: z += -3.23 × (z_dr_0_0p05 − 0.878)
if sum_pt < 1020 and z_dr_0p1_0p2 > 0.097: z += -0.013 × (1020 − sum_pt) × (z_dr_0p1_0p2 − 0.097)
if girth2_top40 < 0.0042: z += 51.00 × (0.0042 − girth2_top40)
if z_top30_slots > 0.916 and C2 > 0.059: z += -69.50 × (z_top30_slots − 0.916) × (C2 − 0.059)
if n_dr_0p2_0p4 < 9.29 and z_top50_slots < 0.987: z += -2.01 × (9.29 − n_dr_0p2_0p4) × (0.987 − z_top50_slots)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass > 80.4`; 2: `mass > 91.2`; 3: `mass_over_sum_pt_sq < 0.00825`; 4: `mass_over_sum_pt > 0.0769`; 5: `mass_over_sum_pt > 0.0836`; 6: `girth < 0.0567`):

- `··✓··✓` **Light narrow quark and gluon jets** — 31.7% of jets, neuron 0.50, formula right for 74%. The largest group (31.7% of jets): mostly quarks with many gluons (48% q, 32% g), light (mean mass 47.8 GeV) and very narrow; one hard leading particle carries more than usual and about three quarters of the pT sits in the innermost ring, far more core-heavy than the average jet. Only the low m/pT² test (+3.186) and the small-girth test (-1.553) pass, so the neuron is modest (mean 0.501) and nudges W up and Z down only a little. The formula calls them q in most cases and is right about three times in four (74.5%), with quark/gluon confusion the main error.
- `✓✓·✓✓·` **Heavy wide top-like jets** — 27.4% of jets, neuron 0.00, formula right for 80%. About a quarter of jets (27.35%): mostly tops (62%) with a sizeable gluon share (21%), heavy (mean 145 GeV) and wide; the pT is shared among many particles with a soft leader and spread well away from the axis. Both mass cuts and both m/pT cuts pass, and the large negative amounts from 'mass > 80.4' and 'm/pT > 0.0769' outweigh the positive ones, so the neuron is almost always zero and contributes nothing. The formula calls them t and is right 80% of the time; the gluons in this group are the usual mistakes.
- `✓·✓✓✓·` **Z-mass window jets, neuron cut** — 8.7% of jets, neuron 0.06, formula right for 90%. Mostly Z jets (86%) with mass just below the Z (mean 88.9 GeV, between 80.4 and 91.2), typical two-prong spread with the pT sitting at small-to-medium distance from the axis. The 'mass > 80.4' test (-1.307) and 'm/pT > 0.0769' (-0.705) cut the neuron back more than the two small positive tests add, so it is usually off (on for 16.4%) and barely affects the scores. The formula still calls them Z (right 89.7%) from other terms.
- `✓·✓✓··` **W peak, just above 80 GeV** — 6.3% of jets, neuron 1.53, formula right for 87%. Mostly W jets (73%) with some Z (18%), mass just above the W (mean 83.2 GeV), typical two-prong jets with average pT sharing and pT concentrated at small-to-medium radius. The low m/pT² test adds +0.994, only partly cancelled by the 'mass > 80.4' and 'm/pT > 0.0769' penalties, so the neuron is clearly on (mean 1.528) and adds to W while taking a large bite out of Z (-2.101). The formula calls them W and is right 86.8% of the time; the Z jets here are the ones it tends to misread as W.
- `··✓✓··` **W jets below 80 GeV** — 5.1% of jets, neuron 2.15, formula right for 92%. Mostly W jets (90%), mass just below the W (mean 78.8 GeV) but with m/pT above 0.0769 (slightly lower total pT); two-prong jets with typical pT sharing. The low m/pT² test (+1.106) passes and only a tiny m/pT penalty applies, so the neuron is almost always on (mean 2.148), pushing W up (+1.611) and Z strongly down (-2.953). The formula calls them W and is right 92% of the time.
- `✓✓✓✓✓·` **Above-Z heavy boson jets** — 4.8% of jets, neuron 0.00, formula right for 95%. Mostly Z jets (87%) with some gluons (9%), mass above 91.2 GeV (mean 94.1 GeV), typical two-prong pT sharing and spread. All mass and m/pT tests but girth pass; the -2.115 from 'mass > 80.4' dominates, so the neuron is off (on 0.0) and has no effect. The formula calls them Z from other terms and is right 94.6% of the time.
- `··✓···` **Clean W below mass cut** — 4.0% of jets, neuron 2.09, formula right for 86%. Mostly W jets (80%), mass below 80.4 GeV (mean 76.8 GeV) and m/pT below 0.0769; typical two-prong jets, a bit more compact than W jets in general. Only the low m/pT² test passes (+1.534), so the neuron is high (mean 2.093), adding to W (+1.57) and strongly subtracting from Z (-2.878). The formula calls them W and is right 86.3% of the time.
- `✓·✓✓·✓` **Collimated W/Z mixture, narrow girth** — 1.8% of jets, neuron 0.75, formula right for 72%. A mixture: 40% W, 35% Z, 14% g, mass around the W (mean 84 GeV) but unusually collimated, with a hard leader and about 85% of the pT within 0.05 of the axis. The low m/pT² bonus (+0.978) is reduced by the mass, m/pT and small-girth penalties, leaving a middling neuron (mean 0.749) that leans W over Z. The formula splits them between W and Z and is right only 72.3% of the time — a weak spot.
- `✓·✓··✓` **High-pT collimated gluon/W mix** — 1.6% of jets, neuron 0.71, formula right for 83%. A mixture led by gluons (44% g, 35% W, 15% Z) with W-like mass (mean 84.1 GeV) but high total pT (1229.8 GeV) and a very core-heavy pT profile with a hard leader. Low m/pT² gives +1.835 but the mass and small-girth tests take away about 1.2, so the neuron is middling (mean 0.712), mildly favouring W over Z. The formula calls them g in about half the cases and W in most of the rest, and is right 83.3% of the time.
- `✓·✓···` **High-pT W jets above 80** — 1.5% of jets, neuron 1.57, formula right for 89%. Mostly W jets (68%) with some Z (18%), mass just above 80.4 GeV (mean 83.3 GeV) but with higher total pT (1135 GeV), so m/pT stays below 0.0769; typical two-prong spread. The low m/pT² bonus (+1.525) outweighs the small 'mass > 80.4' penalty, so the neuron is on (mean 1.567), raising W and cutting Z (-2.155). The formula calls them W and is right 88.7% of the time.

### neuron 3: Sparse jet, empty outer ring (moderate)

- **What it measures:** Rises for jets with few particles, little activity at 0.2 <= ΔR < 0.4, a thin minor axis (small lam2) and low m/pT. W jets and quark jets sit highest, Z jets in the middle, gluon jets low and top jets almost at zero (AUC 0.18 for top: small for t).
- *computed — its value:* largest for W (1.02), then q (0.77), then Z (0.50), then g (0.22), then t (0.03); it separates t jets from the rest best (AUC 0.18: small for t)
- **How the class scores use it:** It raises the W and Z scores (+4% each) and lowers the g score (-9%): a sparse, clean jet looks like a boson or a quark, not a gluon. The q and t scores hardly use it.
- *computed — used by:* raises the score of W (+4%), Z (+4%); lowers the score of g (-9%); does not (or hardly) enter the score of q, t (share of each class score’s average input)

```
z = -0.185
if n_dr_0p2_0p4 < 4.94 and z_top50_slots > 0.979: z += 10.60 × (4.94 − n_dr_0p2_0p4) × (z_top50_slots − 0.979)
if lam2 < 0.00062: z += 1350 × (0.00062 − lam2)
if mass_over_sum_pt_sq < 0.0073: z += 94.70 × (0.0073 − mass_over_sum_pt_sq)
if tau21 < 0.424 and lam1 < 0.016: z += -255 × (0.424 − tau21) × (0.016 − lam1)
if n_particles < 46.10 and sum_pt_top40 > 841: z += 0.00013 × (46.10 − n_particles) × (sum_pt_top40 − 841)
if n_dr_0p1_0p2 < 14.40: z += 0.017 × (14.40 − n_dr_0p1_0p2)
if girth2_top5 < 0.00012: z += -7230 × (0.00012 − girth2_top5)
if mass_over_sum_pt_sq < 0.0075 and girth2_top15 > 0.0049: z += 412000 × (0.0075 − mass_over_sum_pt_sq) × (girth2_top15 − 0.0049)
if n_particles < 45.40 and mass_top30 > 73.00: z += -0.0015 × (45.40 − n_particles) × (mass_top30 − 73.00)
if n_dr_0p2_0p4 < 5.19 and dr_0 < 0.042: z += -5.37 × (5.19 − n_dr_0p2_0p4) × (0.042 − dr_0)
if lam2 < 0.00035: z += 1180 × (0.00035 − lam2)
if z_dr_0p2_0p4 < 0.0014: z += 233 × (0.0014 − z_dr_0p2_0p4)
if n_dr_0p2_0p4 < 5.16 and sum_pt_top30 < 991: z += -0.0014 × (5.16 − n_dr_0p2_0p4) × (991 − sum_pt_top30)
if max_dr < 0.293 and tau21 > 0.430: z += -15.50 × (0.293 − max_dr) × (tau21 − 0.430)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `n_dr_0p2_0p4 < 4.94 and z_top50_slots > 0.979`; 2: `lam2 < 0.000624`; 3: `mass_over_sum_pt_sq < 0.00728`; 4: `tau21 < 0.424 and lam1 < 0.0159`; 5: `n_particles < 46.1 and sum_pt_top40 > 841`; 6: `n_dr_0p1_0p2 < 14.4`):

- `······` **Busy heavy jets, neuron off** — 15.0% of jets, neuron 0.00, formula right for 82%. Mostly tops (68%) with gluons (21%), heavy (mean 154 GeV) and wide, many particles with pT spread out to large radius. None of the six sparseness/narrowness tests pass, so the neuron is off and adds nothing. The formula calls them t and is right 81.5% of the time.
- `✓✓✓✓✓✓` **Sparse two-prong W jets** — 10.5% of jets, neuron 1.61, formula right for 93%. Mostly W jets (77%) with some Z (12%), mean mass 78.3 GeV, few particles and little activity in the outer ring, two-prong pT spread. All tests pass; sparseness, lam2 and particle-count bonuses outweigh the -0.585 of the tau21/lam1 test, so the neuron is high (mean 1.609), adding to W and Z and taking 1.207 from g. The formula calls them W and is right 93.1% of the time.
- `✓✓✓·✓✓` **Very narrow light quark jets** — 8.0% of jets, neuron 1.37, formula right for 80%. Mostly quark jets (74%), very light (mean 29.6 GeV) and extremely collimated: one dominant particle and about 88% of the pT in the core. Everything but the two-prong tau21/lam1 test passes, so the neuron is high (mean 1.37), lowering g and raising W/Z. The formula still calls them q (91.7%) and is right 79.5% of the time.
- `··✓··✓` **Narrow gluon jets, busy** — 7.4% of jets, neuron 0.16, formula right for 77%. Mostly gluons (68%) with quarks (15%), mean mass 67.7 GeV, narrow but with more particles and outer activity than the sparse groups. Only low m/pT² (+0.297) and the inner-ring count (+0.09) pass, so the neuron is small (mean 0.156) with a tiny effect. The formula calls them g and is right 76.7% of the time.
- `·✓✓·✓✓` **Narrow quark jets, some activity** — 6.9% of jets, neuron 0.87, formula right for 73%. Mostly quark jets (61%) with gluons (18%) and W (12%), light (mean 42.8 GeV), one dominant particle and nearly 87% of the pT in the core. The outer-ring sparseness test fails but lam2, m/pT², particle-count and inner-ring tests add up to a middling neuron (mean 0.871), lowering g. The formula calls them q and is right 72.7% of the time.
- `·····✓` **Busy heavy top/gluon jets** — 5.7% of jets, neuron 0.00, formula right for 79%. Mostly tops (54%) with gluons (30%), heavy (mean 138 GeV), wide, many particles. Only the tiny inner-ring count test passes; the neuron is essentially off (on 1.5%) and adds nothing. The formula calls them t in 55% of cases and is right 78.7%, with gluons the main confusion.
- `✓✓·✓✓✓` **Sparse Z jets at 91 GeV** — 4.6% of jets, neuron 0.79, formula right for 98%. Almost pure Z (97%), mass right at the Z (mean 91.2 GeV), two-prong with most pT at small-to-medium radius and a quiet outer ring. The sparseness, lam2 and count tests pass while m/pT² fails; the neuron is on (mean 0.794), lowering g and raising W and Z. The formula calls them Z and is right 97.7% of the time.
- `·✓✓✓✓✓` **W jets with harder leader** — 4.5% of jets, neuron 0.51, formula right for 78%. Mostly W jets (57%) with Z (21%) and quarks (14%), mean mass 77.5 GeV, more pT in the leading particle than usual and a core-heavy profile, but some outer activity. The outer-ring test fails; the other bonuses outweigh the tau21/lam1 penalty, giving a middling neuron (mean 0.508). The formula calls them W and is right 77.6% of the time.
- `···✓··` **Two-prong-like heavy mixture, off** — 3.5% of jets, neuron 0.00, formula right for 71%. Mostly tops (45%) with gluons (28%) and Z (14%), mass around 112 GeV, pT at medium radius. Only the tau21/lam1 test passes and its amount is negative, so the neuron is off. The formula calls them t about half the time and is right only 71.4% — a mixed group.
- `·✓✓··✓` **Narrow high-pT gluon jets** — 2.7% of jets, neuron 0.42, formula right for 80%. Mostly gluons (70%) with quarks (18%), mean mass 55 GeV, higher total pT (1153 GeV), core-heavy. lam2, m/pT² and the inner-ring count give a small neuron (mean 0.416), a mild push away from g. The formula still calls them g and is right 80% of the time.

### neuron 6: One-prong, outside the Z mass (moderate)

- **What it measures:** Follows one-prong-ness (large D2 and τ21, a round rather than elongated pT pattern) and is pushed down for masses between about 91 and 120 GeV and for m/pT above 0.0513. Quark jets sit highest, gluon jets next, top jets in between, Z and W jets near zero.
- *computed — its value:* largest for q (1.56), then g (1.26), then t (0.89), then Z (0.21), then W (0.16); it separates q jets from the rest best (AUC 0.81: large for q)
- **How the class scores use it:** It raises the q (+7%) and g (+3%) scores and lowers the Z score (-15%): a one-prong jet away from the Z mass is not a Z. The W and t scores hardly use it.
- *computed — used by:* raises the score of g (+3%), q (+7%); lowers the score of Z (-15%); does not (or hardly) enter the score of W, t (share of each class score’s average input)

```
z = 0.607
if mass < 120: z += -0.038 × (120 − mass)
if mass < 101: z += -0.055 × (101 − mass)
if mass < 173: z += 0.015 × (173 − mass)
if mass_over_sum_pt > 0.051: z += -30.50 × (mass_over_sum_pt − 0.051)
if mass < 91.20: z += 0.054 × (91.20 − mass)
if width < 0.0096: z += -177 × (0.0096 − width)
if mass < 86.10: z += 0.030 × (86.10 − mass)
if n_dr_0p2_0p4 < 16.10: z += -0.046 × (16.10 − n_dr_0p2_0p4)
if lam1 < 0.0074: z += 137 × (0.0074 − lam1)
if lam1 > 0.0081: z += 116 × (lam1 − 0.0081)
if e2 < 0.048: z += 15.70 × (0.048 − e2)
if mass_top10 < 85.30: z += 0.0075 × (85.30 − mass_top10)
if mass_top50 < 71.70: z += 0.035 × (71.70 − mass_top50)
if mass_over_sum_pt > 0.040 and z_dr_0_0p05 < 0.945: z += 8.95 × (mass_over_sum_pt − 0.040) × (0.945 − z_dr_0_0p05)
if mass_over_sum_pt > 0.048 and lam2 < 0.0025: z += 5870 × (mass_over_sum_pt − 0.048) × (0.0025 − lam2)
if mass_over_sum_pt > 0.053 and n_dr_0p2_0p4 < 19.00: z += 0.954 × (mass_over_sum_pt − 0.053) × (19.00 − n_dr_0p2_0p4)
if mass_over_sum_pt > 0.050 and n_dr_0p1_0p2 < 17.30: z += -1.11 × (mass_over_sum_pt − 0.050) × (17.30 − n_dr_0p1_0p2)
if mass_over_sum_pt > 0.052 and z_dr_0p1_0p2 < 0.282: z += 44.80 × (mass_over_sum_pt − 0.052) × (0.282 − z_dr_0p1_0p2)
if girth2_top20 > 0.0024 and max_dr < 0.425: z += 357 × (girth2_top20 − 0.0024) × (0.425 − max_dr)
if girth2_top3 > 0.0096 and D2 < 5.09: z += 20.30 × (girth2_top3 − 0.0096) × (5.09 − D2)
if sum_pt_top10 > 625: z += 0.00049 × (sum_pt_top10 − 625)
if e2 > 0.056: z += -67.50 × (e2 − 0.056)
if m012 > 20.40: z += -0.011 × (m012 − 20.40)
if log_sum_pt < 6.83: z += 6.54 × (6.83 − log_sum_pt)
if lam1 > 0.024: z += 94.10 × (lam1 − 0.024)
if e2 > 0.055 and max_dr < 0.366: z += -1540 × (e2 − 0.055) × (0.366 − max_dr)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass < 120`; 2: `mass < 101`; 3: `mass < 173`; 4: `mass_over_sum_pt > 0.0513`; 5: `mass < 91.2`; 6: `width < 0.00959`):

- `✓✓✓✓✓✓` **Sub-91 GeV W-led jets** — 44.8% of jets, neuron 0.26, formula right for 82%. The largest group (44.8%): a mixture led by W (42%), then Z (27%) and gluons (15%), mass below 91.2 GeV (mean 78.8 GeV) with m/pT above 0.0513, typical spread. All mass tests pass; the mass < 120/101 penalties and the m/pT and width penalties cancel the mass < 173 and < 91.2 bonuses, leaving the neuron small (mean 0.264, on 47.6%) with a slight push away from Z. The formula calls them W most often and is right 81.5% of the time.
- `✓✓✓·✓✓` **Light one-prong quark jets** — 20.0% of jets, neuron 1.81, formula right for 78%. Mostly quark jets (60%) with gluons (29%), very light (mean 37.1 GeV), with m/pT below 0.0513, one dominant particle and about 85% of the pT in the core. Failing the m/pT test removes its penalty, and 'mass < 91.2' (+2.93) and 'mass < 173' (+1.967) outweigh the other penalties: the neuron is high (mean 1.815), adding to g and q and cutting Z (-1.758). The formula calls them q and is right 78.2% of the time.
- `··✓✓··` **Top-mass wide jets** — 14.7% of jets, neuron 1.13, formula right for 82%. Mostly tops (74%) with gluons (18%), mass between 120 and 173 GeV (mean 152 GeV), wide, pT spread outward. Only 'mass < 173' (+0.299) and the m/pT penalty (-3.025) pass, yet the neuron is often on (mean 1.128), adding a little to g and q and lowering Z. The formula calls them t and is right 82.5% of the time.
- `✓✓✓✓·✓` **Z window, 91-101 GeV** — 8.8% of jets, neuron 0.22, formula right for 89%. Mostly Z jets (77%) with gluons (12%), mass between 91.2 and 101 GeV (mean 93.5 GeV), typical two-prong spread. Failing 'mass < 91.2' removes its bonus, so the penalties hold the neuron low (mean 0.221), a small push away from Z. The formula still calls them Z and is right 89.1% of the time.
- `···✓··` **Very heavy wide jets** — 5.0% of jets, neuron 1.22, formula right for 86%. Mostly tops (69%) with gluons (25%), mass above 173 GeV (mean 187.8 GeV), wide. Only the m/pT penalty (-3.751) passes; the neuron is on for most (mean 1.219), lowering Z. The formula calls them t and is right 86.1% of the time.
- `✓·✓✓··` **101-120 GeV mixed jets** — 3.7% of jets, neuron 1.29, formula right for 67%. A mixture led by tops (48%) with gluons (29%) and quarks (19%), mass between 101 and 120 GeV (mean 110.6 GeV), lower total pT. The 'mass < 173' bonus (+0.902) against the m/pT (-1.905) and 'mass < 120' penalties leaves a fairly high neuron (mean 1.29), mildly helping g and q and cutting Z. The formula calls them t (57.3%) and is right only 67.1% of the time.
- `✓·✓✓·✓` **High-pT narrow heavy gluons** — 1.1% of jets, neuron 1.20, formula right for 79%. Mostly gluons (78%), mass 101-120 GeV (mean 108.2 GeV), high total pT (1258.8 GeV) and narrow width. Similar to the previous group plus a small narrow-width penalty; the neuron is on (mean 1.196), cutting Z. The formula calls them g and is right 79.3% of the time.
- `✓✓✓✓··` **Low-pT wide 91-101 GeV** — 1.1% of jets, neuron 0.79, formula right for 65%. Mostly tops (57%) with gluons (22%) and quarks (17%), mass between 91.2 and 101 GeV (mean 96.8 GeV), low total pT and wide. The m/pT (-1.677) and mass penalties are outweighed by 'mass < 173' (+1.102), so the neuron is fairly on (mean 0.788). The formula calls them t and is right only 64.7% of the time — often wrong.
- `✓✓✓✓✓·` **Low-pT wide light jets** — 0.5% of jets, neuron 1.44, formula right for 62%. A gluon-top mixture (42% g, 40% t, 17% q), mass below 91.2 GeV (mean 82.6 GeV), very low total pT (761.8 GeV) and wide. All mass tests pass but not the narrow-width test; the neuron is high (mean 1.435), helping g and q. The formula calls them t about half the time and is right only 62% — a confused group.
- `··✓✓·✓` **Very high-pT narrow gluons** — 0.3% of jets, neuron 1.33, formula right for 88%. Mostly gluons (88%), mass 120-173 GeV (mean 132.6 GeV) but very high total pT (1515 GeV), narrow. 'mass < 173' (+0.583) against the m/pT and width penalties gives a high neuron (mean 1.332), cutting Z. The formula calls them g and is right 87.7% of the time.

### neuron 7: Mass in the 91-101 GeV window (moderate)

- **What it measures:** Switches on mostly for mass between 91.2 and 101 GeV, helped by an elongated two-prong pattern (large eccentricity, small τ21 and D2) and a compact jet. Almost only Z jets sit high on it (mean 2.18 for Z, AUC 0.91); all other types stay near zero.
- *computed — its value:* largest for Z (2.18), then W (0.11), then g (0.07), then t (0.06), then q (0.04); it separates Z jets from the rest best (AUC 0.91: large for Z)
- **How the class scores use it:** It raises the Z score (+9%) and lowers the W (-6%) and t (-3%) scores: a mass just above the Z peak points to a Z. The g and q scores hardly use it.
- *computed — used by:* raises the score of Z (+9%); lowers the score of W (-6%), t (-3%); does not (or hardly) enter the score of g, q (share of each class score’s average input)

```
z = -0.238
if mass < 91.20: z += -0.242 × (91.20 − mass)
if mass < 101: z += 0.087 × (101 − mass)
if girth2_top40 < 0.013: z += 240 × (0.013 − girth2_top40)
if girth2_top20 < 0.008: z += -461 × (0.008 − girth2_top20)
if width < 0.0094: z += 344 × (0.0094 − width)
if mass_top50 < 98.10 and D2 < 1.61: z += -0.467 × (98.10 − mass_top50) × (1.61 − D2)
if mass < 101 and max_dr < 0.391: z += 0.905 × (101 − mass) × (0.391 − max_dr)
if mass < 91.20 and max_dr < 0.392: z += -1.32 × (91.20 − mass) × (0.392 − max_dr)
if mass < 101 and D2 < 1.61: z += 0.362 × (101 − mass) × (1.61 − D2)
if girth2_top40 < 0.008: z += -318 × (0.008 − girth2_top40)
if girth2_top20 < 0.0064: z += 273 × (0.0064 − girth2_top20)
if z_dr_0p2_0p4 < 0.093: z += -8.94 × (0.093 − z_dr_0p2_0p4)
if girth < 0.086: z += -16.30 × (0.086 − girth)
if mass < 80.40: z += 0.037 × (80.40 − mass)
if mass_top20 < 66.00: z += 0.026 × (66.00 − mass_top20)
if e2 < 0.028: z += 47.00 × (0.028 − e2)
if D2 < 1.82 and n_dr_0p2_0p4 < 9.16: z += 0.136 × (1.82 − D2) × (9.16 − n_dr_0p2_0p4)
if n_dr_0p2_0p4 < 13.00 and z_1st < 0.504: z += 0.140 × (13.00 − n_dr_0p2_0p4) × (0.504 − z_1st)
if z_top50_slots < 0.991: z += -36.20 × (0.991 − z_top50_slots)
if z_dr_0p2_0p4 < 0.0047: z += 173 × (0.0047 − z_dr_0p2_0p4)
if D2 < 1.79 and girth2_top50 < 0.0079: z += -504 × (1.79 − D2) × (0.0079 − girth2_top50)
if C2 < 0.056: z += -10.90 × (0.056 − C2)
if n_dr_0p2_0p4 < 12.90 and planar_flow < 0.549: z += 0.060 × (12.90 − n_dr_0p2_0p4) × (0.549 − planar_flow)
if mass < 91.20 and pt_dispersion < 0.340: z += -0.120 × (91.20 − mass) × (0.340 − pt_dispersion)
if n_dr_0p2_0p4 < 1.99: z += -0.288 × (1.99 − n_dr_0p2_0p4)
if mass < 91.20 and z_dr_0p05_0p1 > 0.393: z += -0.127 × (91.20 − mass) × (z_dr_0p05_0p1 − 0.393)
if D2 < 1.77 and girth2_top50 < 0.0061: z += 659 × (1.77 − D2) × (0.0061 − girth2_top50)
if mass_top30 < 76.10 and D2 < 1.61: z += 0.210 × (76.10 − mass_top30) × (1.61 − D2)
if max_dr < 0.196: z += -8.83 × (0.196 − max_dr)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass < 91.2`; 2: `mass < 101`; 3: `girth2_top40 < 0.0127`; 4: `girth2_top20 < 0.00798`; 5: `width < 0.00943`; 6: `mass_top50 < 98.1 and D2 < 1.61`):

- `✓✓✓✓✓·` **Light narrow jets, window missed** — 42.7% of jets, neuron 0.15, formula right for 76%. The largest group (42.72%): a mixture led by quarks (36%) with gluons (28%), W (19%) and Z (14%), light (mean 58 GeV) and core-heavy. The -8.038 from 'mass < 91.2' outweighs the mass < 101, girth and width bonuses, so the neuron is mostly off (on 16%) with negligible effect. The formula calls them q most often and is right 75.7% of the time.
- `✓✓✓✓✓✓` **W-peak two-prong jets** — 21.2% of jets, neuron 0.88, formula right for 90%. Mostly W jets (57%) with Z (29%), mass near the W (mean 81 GeV), compact two-prong jets with small D2. All tests pass, and the two-prong test (-4.553) and 'mass < 91.2' (-2.47) mostly cancel the compactness bonuses; the neuron is on for 44.6% (mean 0.882), nudging toward Z and away from W. The formula still calls them W and is right 89.5% of the time.
- `······` **Heavy wide jets, neuron off** — 19.7% of jets, neuron 0.00, formula right for 83%. Mostly tops (76%) with gluons (17%), heavy (mean 159.6 GeV) and wide, pT spread outward. None of the tests pass, so the neuron is off and contributes nothing. The formula calls them t and is right 83.1% of the time.
- `·✓✓✓✓✓` **Z window, compact two-prong** — 4.2% of jets, neuron 2.88, formula right for 94%. Almost pure Z (92%), mass inside the 91.2-101 GeV window (mean 92.9 GeV), compact two-prong jets. 'mass < 101', girth and width bonuses beat the two-prong and top-20 girth penalties, giving a high neuron (mean 2.884) that raises Z (+2.614) and lowers W and t. The formula calls them Z and is right 94.3% of the time.
- `·✓✓✓✓·` **Z window, one-prong-like mix** — 2.9% of jets, neuron 0.94, formula right for 80%. Z-led mixture (49% Z, 33% g), mass in the window (mean 94.3 GeV), higher total pT and more pT near the axis than typical Z jets; not two-prong (fails the D2 test). Without the two-prong penalty the window and compactness bonuses give a fairly high neuron (mean 0.942), raising Z. The formula calls them Z (55.7%) and is right 79.9% — gluons here are pushed toward Z.
- `··✓···` **Heavy gluon/top mixture** — 2.3% of jets, neuron 0.05, formula right for 64%. A mixture of gluons (38%), tops (37%) and quarks (19%), mass around 118 GeV, above the window. Only the top-40 girth test adds (+0.365); the neuron is mostly off (on 14.9%). The formula splits them between g and t and is right only 63.9% of the time — one of the weakest groups.
- `·✓✓·✓✓` **Z window, wide two-prong** — 1.3% of jets, neuron 3.63, formula right for 96%. Almost pure Z (95%), mass in the window (mean 93.3 GeV), two-prong with pT a little further out (fails the top-20 girth test). The top-20 girth penalty is absent, so the neuron is high (mean 3.627), raising Z (+3.287) and lowering W and t. The formula calls them Z and is right 96% of the time.
- `··✓✓··` **Heavy compact gluon jets** — 1.3% of jets, neuron 0.01, formula right for 76%. Mostly gluons (63%) with tops (18%) and quarks (15%), mass around 118 GeV, pT fairly concentrated. The two girth tests cancel (+0.712, -0.818), so the neuron is almost always off. The formula calls them g and is right 75.5% of the time.
- `··✓✓✓·` **Very high-pT narrow gluons** — 1.3% of jets, neuron 0.09, formula right for 83%. Mostly gluons (83%), mass around 114 GeV, very high total pT (1339.8 GeV), narrow. The girth bonuses and penalty roughly cancel; the neuron is mostly off (on 20.8%). The formula calls them g and is right 83.3% of the time.
- `✓✓✓·✓✓` **Z just below 91 GeV** — 0.8% of jets, neuron 3.83, formula right for 95%. Mostly Z jets (92%) with mass just below 91.2 GeV (mean 89.6 GeV), two-prong, pT a little further from the axis than W jets. 'mass < 91.2' costs only -0.393 here while the window and compactness bonuses add about 2.5, so despite the two-prong penalty (-3.091) the neuron is high (mean 3.835), raising Z (+3.476) and lowering W. The formula calls them Z and is right 95.4% of the time — it separates these Z jets from W jets of similar mass.

### neuron 9: Light one-prong jet, off the W mass (moderate)

- **What it measures:** Large when the hardest 50 particles have mass below 135 GeV, and it follows τ21 (one-prong-ness); it is pushed down for mass between 63 and 80.4 GeV, the W side. Quark jets sit highest, gluon jets next, top, W and Z jets low.
- *computed — its value:* largest for q (2.03), then g (1.26), then t (0.34), then W (0.19), then Z (0.16); it separates q jets from the rest best (AUC 0.82: large for q)
- **How the class scores use it:** It raises the q (+17%) and g (+10%) scores and lowers the W score slightly (-3%): a light, one-prong jet off the W mass is a light-QCD jet. The Z and t scores hardly use it.
- *computed — used by:* raises the score of g (+10%), q (+17%); lowers the score of W (-3%); does not (or hardly) enter the score of Z, t (share of each class score’s average input)

```
z = -0.968
if mass_top50 < 135: z += 0.041 × (135 − mass_top50)
if mass > 80.40: z += 0.097 × (mass − 80.40)
if mass > 63.00: z += -0.053 × (mass − 63.00)
if girth2_top15 < 0.021: z += -74.40 × (0.021 − girth2_top15)
if girth2_top40 < 0.006: z += 346 × (0.006 − girth2_top40)
if girth < 0.043: z += -70.70 × (0.043 − girth)
if LHA < 0.210: z += 14.30 × (0.210 − LHA)
if mass > 145: z += -0.054 × (mass − 145)
if sum_pt < 951: z += 0.020 × (951 − sum_pt)
if log_sum_pt < 6.85: z += -17.50 × (6.85 − log_sum_pt)
if width > 0.026: z += -240 × (width − 0.026)
if girth2_top15 < 0.018 and n_particles > 40.20: z += 1.25 × (0.018 − girth2_top15) × (n_particles − 40.20)
if girth > 0.098: z += 12.60 × (girth − 0.098)
if girth < 0.028: z += -26.60 × (0.028 − girth)
if z_top50_slots < 0.973: z += -34.80 × (0.973 − z_top50_slots)
if lam2 > 0.0015: z += -90.90 × (lam2 − 0.0015)
if girth2_top40 < 0.0061 and sum_pt < 1020: z += 1.71 × (0.0061 − girth2_top40) × (1020 − sum_pt)
if sum_pt_top40 < 965: z += 0.0028 × (965 − sum_pt_top40)
if n_dr_0p1_0p2 > 21.20: z += -0.027 × (n_dr_0p1_0p2 − 21.20)
if mass_top40 < 120 and max_dr > 0.380: z += 0.052 × (120 − mass_top40) × (max_dr − 0.380)
if log_sum_pt < 6.85 and dr_7 < 0.078: z += 159 × (6.85 − log_sum_pt) × (0.078 − dr_7)
if log_sum_pt < 6.85 and z_top20_slots > 0.898: z += 172 × (6.85 − log_sum_pt) × (z_top20_slots − 0.898)
if sum_pt_top40 < 965 and z_top30_slots > 0.970: z += -0.275 × (965 − sum_pt_top40) × (z_top30_slots − 0.970)
if e2 > 0.066: z += -45.40 × (e2 − 0.066)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass_top50 < 135`; 2: `mass > 80.4`; 3: `mass > 63`; 4: `girth2_top15 < 0.0208`; 5: `girth2_top40 < 0.00603`; 6: `girth < 0.0435`):

- `✓✓✓✓··` **Z-mass jets, W-side penalty** — 34.0% of jets, neuron 0.06, formula right for 83%. The largest group (34.03%): mostly Z jets (49%) with tops (18%), W (14%) and gluons (12%), mean mass 96.5 GeV, typical spread. Top-50 mass and 'mass > 80.4' bonuses are cancelled by 'mass > 63' (-1.769) and the girth penalty, so the neuron is mostly off (on 12.8%). The formula calls them Z and is right 82.9% of the time.
- `✓··✓✓✓` **Light one-prong quark/gluon jets** — 23.2% of jets, neuron 2.62, formula right for 76%. Mostly quark jets (58%) with gluons (30%), light (mean 39.3 GeV, below 63), narrow, one dominant particle and about 83% of the pT in the core. The top-50 mass test (+3.93) and top-40 compactness (+1.593) outweigh the girth penalties, making the neuron high (mean 2.62): it adds to g and q and lowers W. The formula calls them q and is right 75.9% of the time, gluons being the main error.
- `·✓✓···` **Top-mass wide jets** — 10.1% of jets, neuron 0.23, formula right for 90%. Mostly tops (85%), mass right at the top (mean 173.8 GeV), wide, top-50 mass above 135 GeV, pT spread far out. 'mass > 80.4' (+9.044) and 'mass > 63' (-5.852) leave a net gain that is largely offset by a negative base value, so the neuron is small (mean 0.225). The formula calls them t and is right 90% of the time.
- `✓·✓✓✓·` **W-side 63-80 GeV jets** — 9.6% of jets, neuron 0.33, formula right for 82%. Mostly W jets (70%) with gluons (14%), mass between 63 and 80.4 GeV (mean 76.4 GeV), compact two-prong spread. The top-50 mass bonus (+2.448) is cut by 'mass > 63' and the girth penalty, so the neuron is mostly off (on 35.6%), as intended for the W side. The formula calls them W and is right 82% of the time.
- `·✓✓✓··` **Heavy tops, compact core** — 5.8% of jets, neuron 0.41, formula right for 80%. Mostly tops (64%) with gluons (27%), heavy (mean 159.7 GeV), top-50 mass above 135 GeV. 'mass > 80.4' (+7.672) against 'mass > 63' (-5.104) and a girth penalty leaves a small neuron (mean 0.411). The formula calls them t and is right 79.8% of the time.
- `✓✓✓✓✓·` **80-135 GeV mixed jets** — 5.3% of jets, neuron 0.07, formula right for 84%. A W-led mixture (45% W, 30% g, 18% Z), mean mass 86.7 GeV, higher total pT. Bonuses and penalties nearly cancel, so the neuron is mostly off (on 19.3%). The formula calls them W (50.9%) or g and is right 83.9% of the time.
- `✓·✓✓✓✓` **Narrow gluons on W side** — 4.6% of jets, neuron 0.84, formula right for 71%. A gluon-led mixture (45% g, 28% W, 17% q), mass 63-80.4 GeV (mean 71.4 GeV), narrow and core-heavy with a hard leader. The top-50 mass bonus (+2.687) and top-40 compactness beat the penalties; the neuron is on for most (mean 0.837), raising g and q. The formula calls them g (48.8%) or W and is right only 70.8% of the time — gluon/W confusion.
- `✓·✓✓··` **W jets, less compact** — 4.2% of jets, neuron 0.15, formula right for 89%. Mostly W jets (81%), mass 63-80.4 GeV (mean 78.7 GeV), less compact than the previous W group, slightly lower total pT. Top-50 mass bonus cancelled by 'mass > 63' and girth penalties; the neuron is mostly off (on 11.2%). The formula calls them W and is right 88.6% of the time.
- `✓✓✓✓✓✓` **High-pT narrow heavy gluons** — 1.1% of jets, neuron 0.26, formula right for 82%. Mostly gluons (67%) with W and Z, mean mass 88.5 GeV, high total pT (1293 GeV), narrow and core-heavy. All tests pass and roughly cancel; the neuron is small (mean 0.258). The formula calls them g and is right 81.5% of the time.
- `✓··✓✓·` **Light low-pT quark/gluon jets** — 0.9% of jets, neuron 2.79, formula right for 64%. A quark-gluon mixture (46% q, 36% g, 10% t), light (mean 57.3 GeV), low total pT, with pT mainly just outside the core. The top-50 mass (+3.243) and top-40 compactness bonuses give a high neuron (mean 2.792), raising g and q. The formula calls them q (63.5%) and is right only 63.7% of the time — a poorly resolved group.

### neuron 12: Lightness: mass below 80 GeV (moderate)

- **What it measures:** Essentially on for jets lighter than 80.4 GeV, but pushed down for very light jets (hardest-50 mass below 60.1 GeV), very narrow jets and large C2. Quark jets sit highest (AUC 0.79), gluon jets next, W, top and Z jets low.
- *computed — its value:* largest for q (1.27), then g (0.60), then W (0.31), then t (0.18), then Z (0.17); it separates q jets from the rest best (AUC 0.79: large for q)
- **How the class scores use it:** It raises the q (+7%), g (+3%) and Z (+3%) scores and lowers the W (-4%) and t (-4%) scores: small corrections that credit light jets to the light-QCD scores and fine-tune the W/Z balance below the W mass.
- *computed — used by:* raises the score of g (+3%), q (+7%), Z (+3%); lowers the score of W (-4%), t (-4%) (share of each class score’s average input)

```
z = 0.119
if mass < 80.40: z += 0.113 × (80.40 − mass)
if C2 > 0.058: z += -13.40 × (C2 − 0.058)
if mass_top50 < 60.10: z += -0.046 × (60.10 − mass_top50)
if girth < 0.049: z += -23.50 × (0.049 − girth)
if mass < 84.70 and z_dr_0p1_0p2 < 0.065: z += -0.312 × (84.70 − mass) × (0.065 − z_dr_0p1_0p2)
if planar_flow > 0.266: z += -0.490 × (planar_flow − 0.266)
if mass_top40 < 94.40 and sum_pt_top2 < 471: z += -4.3e-05 × (94.40 − mass_top40) × (471 − sum_pt_top2)
if mass_top20 > 127 and C2 > 0.060: z += -1.34 × (mass_top20 − 127) × (C2 − 0.060)
if mass_top30 > 137: z += 0.035 × (mass_top30 − 137)
if log_sum_pt < 6.86: z += -6.56 × (6.86 − log_sum_pt)
if LHA > 0.400: z += 15.10 × (LHA − 0.400)
if z_dr_0_0p05 > 0.918: z += -7.28 × (z_dr_0_0p05 − 0.918)
if mass_top20 > 127: z += 0.040 × (mass_top20 − 127)
if mass < 91.20 and z_dr_0p05_0p1 > 0.320: z += 0.058 × (91.20 − mass) × (z_dr_0p05_0p1 − 0.320)
if z_dr_0p1_0p2 > 0.685 and min_pair_mass > 0.762: z += -1.78 × (z_dr_0p1_0p2 − 0.685) × (min_pair_mass − 0.762)
if LHA > 0.406 and lam2 < 0.0037: z += 12700 × (LHA − 0.406) × (0.0037 − lam2)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass < 80.4`; 2: `C2 > 0.0576`; 3: `mass_top50 < 60.1`; 4: `girth < 0.0488`; 5: `mass < 84.7 and z_dr_0p1_0p2 < 0.0652`; 6: `planar_flow > 0.266`):

- `·✓···✓` **Heavy wide top-led jets** — 23.6% of jets, neuron 0.06, formula right for 80%. Nearly a quarter of jets (23.59%): mostly tops (54%) with gluons (23%) and Z (14%), heavy (mean 136 GeV) and wide, pT spread outward. Only the large-C2 (-0.702) and planar-flow (-0.172) penalties pass, so the neuron is almost always off. The formula calls them t and is right 80.5% of the time.
- `······` **Z-mass jets, small C2** — 16.1% of jets, neuron 0.24, formula right for 92%. Mostly Z jets (62%) with W (20%) and tops (11%), mean mass 96.5 GeV, clean two-prong spread with small C2. No test passes; the neuron sits at its small base value (mean 0.238) with tiny effects on the scores. The formula calls them Z and is right 91.6% of the time.
- `✓·✓✓✓✓` **Light narrow quark/gluon jets** — 13.5% of jets, neuron 1.61, formula right for 78%. A quark-gluon mixture (50% q, 42% g), light (mean 39.3 GeV), narrow and core-heavy. 'mass < 80.4' adds +4.64 and the very-light, narrow and ring penalties take off about 2.6, so the neuron is high (mean 1.611), raising g, q and Z a little and lowering W and t. The formula calls them q (57.6%) or g and is right 78.3% of the time.
- `✓✓✓✓✓✓` **One dominant particle, quarks** — 8.8% of jets, neuron 1.26, formula right for 75%. Mostly quark jets (69%) with gluons (15%), light (mean 38.3 GeV), one dominant particle (about 374 GeV) and about 91% of the pT in the innermost ring. Same as the previous group plus a small large-C2 penalty; the neuron is high (mean 1.259). The formula calls them q and is right 74.8% of the time.
- `·····✓` **Planar Z-mass mixture** — 7.2% of jets, neuron 0.08, formula right for 80%. A Z-led mixture (39% Z, 24% t, 18% W, 13% g), mean mass 96 GeV, with high planar flow. Only the small planar-flow penalty passes; the neuron is small (mean 0.08). The formula calls them Z (41.4%) and is right 79.6% of the time.
- `·✓····` **Heavy mixed jets, large C2** — 5.0% of jets, neuron 0.39, formula right for 82%. A top-led mixture (46% t, 23% Z, 17% g), mean mass 140 GeV, wide. Only the large-C2 penalty (-0.491) passes; the neuron is mostly off (on 29.1%). The formula calls them t and is right 82.1% of the time.
- `✓·····` **Clean W jets below 80** — 4.0% of jets, neuron 0.32, formula right for 95%. Almost pure W (94%), mass just below 80.4 GeV (mean 78.7 GeV), small C2 and not narrow. Only 'mass < 80.4' passes (+0.192), so the neuron is small but on (mean 0.323), slightly lowering W. The formula still calls them W and is right 94.7% of the time.
- `✓✓·✓✓✓` **Narrow sub-80 GeV mixture** — 3.1% of jets, neuron 0.20, formula right for 63%. A mixture of W (32%), gluons (30%), quarks (26%) and Z (10%), mean mass 71.3 GeV, narrow and core-heavy with a hard leader. 'mass < 80.4' (+1.028) is cancelled by the C2, girth and other penalties; the neuron is mostly off (on 36.8%). The formula spreads its calls over W, q and g and is right only 63% of the time — a genuinely hard group.
- `✓····✓` **Planar W jets below 80** — 2.6% of jets, neuron 0.38, formula right for 79%. Mostly W jets (69%) with small shares of all others, mean mass 76.8 GeV, high planar flow. 'mass < 80.4' (+0.411) minus a small planar-flow penalty gives a small neuron (mean 0.38). The formula calls them W and is right 79% of the time.
- `✓✓···✓` **Planar W jets, large C2** — 1.8% of jets, neuron 0.11, formula right for 78%. Mostly W jets (63%) with gluons (19%), mean mass 76.8 GeV, slightly lower total pT, larger C2. The small mass bonus is cancelled by the C2 and planar-flow penalties; the neuron is mostly off (on 31.9%). The formula calls them W and is right 78.1% of the time.

### neuron 13: High pT, mass below the top (moderate)

- **What it measures:** Grows with the total jet pT and is pushed down for mass above 143 GeV (and hardest-50 mass above 98.1 GeV), while mass above 74.9 GeV pushes it up. All non-top types sit at similar, high values; top jets sit lowest (AUC 0.19 for t: small for t).
- *computed — its value:* largest for g (2.37), then Z (2.16), then W (1.97), then q (1.97), then t (1.01); it separates t jets from the rest best (AUC 0.19: small for t)
- **How the class scores use it:** Only the t score uses it, lowering it strongly (-38%): a high-pT jet whose mass is short of the top is not a top. It is the main negative top handle.
- *computed — used by:* lowers the score of t (-38%); does not (or hardly) enter the score of g, q, W, Z (share of each class score’s average input)

```
z = 2.37
if mass > 143: z += -0.162 × (mass − 143)
if mass > 74.90: z += 0.025 × (mass − 74.90)
if log_sum_pt < 7.02: z += -5.92 × (7.02 − log_sum_pt)
if sum_pt < 1010: z += -0.026 × (1010 − sum_pt)
if sum_pt < 1060: z += -0.0092 × (1060 − sum_pt)
if mass_top50 > 98.10: z += -0.033 × (mass_top50 − 98.10)
if mass_top50 > 137: z += 0.090 × (mass_top50 − 137)
if sum_pt_top40 < 1050: z += 0.0065 × (1050 − sum_pt_top40)
if mass_over_sum_pt_sq < 0.0095: z += 104 × (0.0095 − mass_over_sum_pt_sq)
if sum_pt_top50 < 1010: z += 0.01 × (1010 − sum_pt_top50)
if mass_over_sum_pt > 0.171: z += 312 × (mass_over_sum_pt − 0.171)
if mass_over_sum_pt_sq > 0.029: z += -815 × (mass_over_sum_pt_sq − 0.029)
if mass_top10 > 57.10: z += 0.015 × (mass_top10 − 57.10)
if mass > 173: z += 0.159 × (mass − 173)
if sum_pt_top40 < 1030 and D2 < 4.94: z += -0.0012 × (1030 − sum_pt_top40) × (4.94 − D2)
if n_dr_0p2_0p4 < 3.96: z += -0.133 × (3.96 − n_dr_0p2_0p4)
if n_particles < 46.40: z += -0.013 × (46.40 − n_particles)
if n_particles > 46.00: z += 0.013 × (n_particles − 46.00)
if log_sum_pt < 6.81: z += 17.30 × (6.81 − log_sum_pt)
if sum_pt < 1070 and tau21 > 0.241: z += 0.004 × (1070 − sum_pt) × (tau21 − 0.241)
if mass > 161 and D2 < 6.47: z += -0.0053 × (mass − 161) × (6.47 − D2)
if sum_pt_top50 < 953 and D2 < 4.76: z += 0.0022 × (953 − sum_pt_top50) × (4.76 − D2)
if mass_top50 > 169: z += -0.046 × (mass_top50 − 169)
if sum_pt > 1250 and dr_7 < 0.080: z += -0.041 × (sum_pt − 1250) × (0.080 − dr_7)
if sum_pt > 1250: z += -0.0016 × (sum_pt − 1250)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass > 143`; 2: `mass > 74.9`; 3: `log_sum_pt < 7.02`; 4: `sum_pt < 1.01e+03`; 5: `sum_pt < 1.06e+03`; 6: `mass_top50 > 98.1`):

- `·✓✓·✓·` **W/Z jets, medium pT** — 21.7% of jets, neuron 2.13, formula right for 91%. An even W/Z mix (46% Z, 45% W), mean mass 85.6 GeV, total pT between 1010 and 1060 GeV, typical two-prong spread. The mass > 74.9 bonus and two small pT penalties leave the base value to carry the neuron (mean 2.135), which lowers the t score by 1.935. The formula splits them W/Z almost evenly and is right 90.7% of the time.
- `·✓✓✓✓·` **W/Z/top, lower pT** — 12.7% of jets, neuron 1.29, formula right for 79%. A mixture of Z (34%), W (31%) and tops (18%), mean mass 85.4 GeV, total pT below 1010 GeV. All three low-pT tests pass, taking about 2.5 off, so the neuron is lower (mean 1.29) and lowers t less. The formula calls them W or Z about equally and is right 78.7% of the time.
- `··✓✓✓·` **Light low-pT quark jets** — 12.0% of jets, neuron 1.29, formula right for 71%. Mostly quark jets (60%) with gluons (22%), light (mean 44.5 GeV, below 74.9), total pT below 1010 GeV, core-heavy. The low-pT penalties bring the neuron down to a mean of 1.288, lowering t. The formula calls them q and is right 70.6% of the time — quark/gluon confusion.
- `··✓·✓·` **Light quarks, medium pT** — 9.0% of jets, neuron 2.41, formula right for 70%. Mostly quark jets (59%) with gluons (19%) and W (13%), light (mean 43.9 GeV), total pT between 1010 and 1060 GeV, one hard leader and core-heavy. Only two small pT penalties apply, so the neuron is high (mean 2.412), lowering t. The formula calls them q and is right 70.2% of the time.
- `✓✓✓✓✓✓` **Heavy low-pT tops** — 7.3% of jets, neuron 0.53, formula right for 90%. Mostly tops (90%), heavy (mean 165.4 GeV, above 143), total pT below 1010 GeV, wide. Every test passes; 'mass > 143' (-3.623) and the top-50 mass and low-pT penalties outweigh 'mass > 74.9', so the neuron is small (mean 0.534) and barely lowers t. The formula calls them t and is right 90% of the time.
- `·✓✓···` **W/Z jets, higher pT** — 6.0% of jets, neuron 2.66, formula right for 88%. An even W/Z mix (42% Z, 41% W), mean mass 86.2 GeV, total pT between 1060 and about 1120 GeV. Only the mass bonus and one small pT penalty apply, so the neuron is high (mean 2.662), lowering t by 2.413. The formula splits them W/Z and is right 87.6% of the time.
- `······` **Very high-pT light gluons** — 5.4% of jets, neuron 2.90, formula right for 83%. Mostly gluons (74%) with quarks (21%), light (mean 51.6 GeV), very high total pT (1256 GeV), core-heavy. No test passes; the base value alone makes the neuron high (mean 2.895), lowering t. The formula calls them g and is right 83.2% of the time.
- `·✓✓✓✓✓` **Mid-mass low-pT tops** — 4.9% of jets, neuron 1.24, formula right for 74%. Mostly tops (68%) with gluons (18%) and quarks (13%), mass between 74.9 and 143 GeV (mean 121 GeV), low total pT. All pT and top-50 mass penalties apply against the mass bonus (+1.142), leaving a middling neuron (mean 1.241) that still lowers t. The formula calls them t and is right 73.5% of the time.
- `·✓····` **Very high-pT gluon/boson mix** — 4.8% of jets, neuron 2.91, formula right for 88%. A mixture led by gluons (43% g, 27% W, 25% Z), mean mass 86.8 GeV, very high total pT (1242 GeV). Only the mass bonus passes, so the neuron is high (mean 2.91), lowering t. The formula calls them g (45.9%) and is right 87.5% of the time.
- `✓✓✓·✓✓` **Heavy tops, medium pT** — 3.8% of jets, neuron 1.13, formula right for 88%. Mostly tops (87%), heavy (mean 170 GeV), total pT between 1010 and 1060 GeV. 'mass > 143' (-4.382) and top-50 mass (-2.254) outweigh 'mass > 74.9' (+2.35), yet the neuron stays on (mean 1.133), lowering t by about 1. The formula calls them t and is right 88.5% of the time.

### neuron 14: Mass just above the Z (moderate)

- **What it measures:** Large for mass between 91.2 and 136 GeV, especially with m/pT between 0.0907 and 0.0984. Z jets sit highest (AUC 0.88), gluon and top jets well below, quark and W jets lowest.
- *computed — its value:* largest for Z (1.52), then g (0.52), then t (0.41), then q (0.16), then W (0.15); it separates Z jets from the rest best (AUC 0.88: large for Z)
- **How the class scores use it:** Only the W score uses it, lowering it (-14%): a jet heavier than the Z peak is not a W. The Z score hardly uses it even though Z jets sit highest on it.
- *computed — used by:* lowers the score of W (-14%); does not (or hardly) enter the score of g, q, Z, t (share of each class score’s average input)

```
z = 0.205
if mass_over_sum_pt < 0.091: z += -165 × (0.091 − mass_over_sum_pt)
if mass_over_sum_pt < 0.098: z += 116 × (0.098 − mass_over_sum_pt)
if mass < 91.20: z += -0.132 × (91.20 − mass)
if mass < 136: z += 0.030 × (136 − mass)
if girth2_top50 < 0.0094: z += -207 × (0.0094 − girth2_top50)
if lam2 < 0.0024: z += 433 × (0.0024 − lam2)
if lam1 < 0.0063: z += 260 × (0.0063 − lam1)
if girth2_top20 < 0.017 and z_top50_slots > 0.969: z += -1310 × (0.017 − girth2_top20) × (z_top50_slots − 0.969)
if mass_top40 < 80.70: z += -0.026 × (80.70 − mass_top40)
if max_dr > 0.249: z += -2.43 × (max_dr − 0.249)
if n_dr_0p2_0p4 < 21.40: z += 0.019 × (21.40 − n_dr_0p2_0p4)
if sum_pt_top50 > 978: z += -0.0031 × (sum_pt_top50 − 978)
if log_sum_pt > 6.94: z += 5.53 × (log_sum_pt − 6.94)
if girth2_top20 < 0.016 and tau21 < 0.637: z += -94.90 × (0.016 − girth2_top20) × (0.637 − tau21)
if n_dr_0p2_0p4 < 19.90 and n_dr_0p1_0p2 < 21.30: z += -0.0011 × (19.90 − n_dr_0p2_0p4) × (21.30 − n_dr_0p1_0p2)
if lam1 < 0.0062 and z_top50_slots > 0.987: z += 8090 × (0.0062 − lam1) × (z_top50_slots − 0.987)
if max_dr > 0.201 and mass_top10 < 52.10: z += 0.040 × (max_dr − 0.201) × (52.10 − mass_top10)
if z_top50_slots < 0.959: z += 89.60 × (0.959 − z_top50_slots)
if m012 > 36.20: z += -0.011 × (m012 − 36.20)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass_over_sum_pt < 0.0907`; 2: `mass_over_sum_pt < 0.0984`; 3: `mass < 91.2`; 4: `mass < 136`; 5: `girth2_top50 < 0.00935`; 6: `lam2 < 0.00238`):

- `✓✓✓✓✓✓` **Bulk: light, low m/pT** — 63.0% of jets, neuron 0.36, formula right for 81%. Most jets (63.01%): a mixture of W (32%), quarks (26%), Z (20%) and gluons (19%), mass below 91.2 GeV (mean 65.4 GeV) with low m/pT. All tests pass and the large amounts cancel ('m/pT < 0.0907' -4.607 against '< 0.0984' +4.132, 'mass < 91.2' -3.407 against '< 136' +2.139), so the neuron is mostly off (on 37.4%), slightly lowering W. The formula calls them W or q most often and is right 80.6% of the time.
- `······` **Heavy wide tops, nothing passes** — 11.0% of jets, neuron 0.26, formula right for 89%. Mostly tops (85%), heavy (mean 169 GeV), high m/pT, wide. No test passes; the neuron is mostly off (on 31.7%), slightly lowering W. The formula calls them t and is right 88.9% of the time.
- `✓✓·✓✓✓` **Z jets above 91, high pT** — 6.5% of jets, neuron 1.78, formula right for 93%. Mostly Z jets (74%) with gluons (21%), mass between 91.2 and 136 GeV (mean 94.9 GeV), higher total pT so m/pT below 0.0907. Without the 'mass < 91.2' penalty, the '< 0.0984' and '< 136' bonuses win, making the neuron high (mean 1.777) and cutting W by 2.444. The formula calls them Z and is right 92.8% of the time.
- `·····✓` **Heavy tops, thin minor axis** — 5.5% of jets, neuron 0.50, formula right for 78%. Mostly tops (61%) with gluons (29%), heavy (mean 164.5 GeV), small lam2. Only the lam2 bonus (+0.453) passes; the neuron is small (mean 0.503), lowering W slightly. The formula calls them t and is right 77.9% of the time.
- `···✓·✓` **91-136 GeV high-m/pT mixture** — 5.0% of jets, neuron 0.95, formula right for 70%. Mostly tops (52%) with gluons (27%) and quarks (18%), mass 91.2-136 GeV (mean 115.4 GeV), m/pT above 0.0984. 'mass < 136' and lam2 bonuses give a middling neuron (mean 0.946), lowering W. The formula calls them t (61.3%) and is right only 70% of the time.
- `·✓·✓✓✓` **Z jets, m/pT 0.091-0.098** — 3.0% of jets, neuron 1.72, formula right for 80%. Mostly Z jets (61%) with gluons (18%) and tops (10%), mass 91.2-136 GeV (mean 97 GeV), m/pT between 0.0907 and 0.0984. The target window: '< 0.0984', '< 136' and lam2 bonuses give a high neuron (mean 1.723), cutting W by 2.369. The formula calls them Z and is right 80.2% of the time.
- `···✓··` **Wide 91-136 GeV mixture** — 2.6% of jets, neuron 0.69, formula right for 69%. Mostly tops (54%) with gluons (31%) and quarks (12%), mass 91.2-136 GeV (mean 117.5 GeV), low total pT, wider minor axis. Only 'mass < 136' (+0.559) passes; the neuron is middling (mean 0.685), lowering W. The formula calls them t (64.2%) and is right only 68.6% of the time.
- `·✓✓✓✓✓` **Low-pT Z/top below 91** — 1.1% of jets, neuron 1.62, formula right for 80%. A Z-top mixture (47% Z, 35% t), mass below 91.2 GeV (mean 87.4 GeV), low total pT, m/pT between 0.0907 and 0.0984. The '< 0.0984' and '< 136' bonuses outweigh the 'mass < 91.2' penalty, giving a high neuron (mean 1.62) that cuts W. The formula calls them Z (47.9%) or t and is right 79.8% of the time.
- `✓✓✓✓✓·` **Light Z/gluon mixture, wide** — 0.7% of jets, neuron 0.97, formula right for 73%. A mixture of Z (35%), gluons (32%), quarks (12%) and W (12%), mean mass 82.6 GeV, low m/pT, wider minor axis. Without the lam2 bonus the mass and m/pT amounts leave a middling neuron (mean 0.969), cutting W. The formula calls them g (38.4%) or Z and is right only 72.7% of the time.
- `··✓✓·✓` **Very low-pT light mixture** — 0.3% of jets, neuron 0.72, formula right for 63%. A top-led mixture (50% t, 31% g, 17% q), mean mass 82.4 GeV but very low total pT (766 GeV), so m/pT is high. 'mass < 136' (+1.623) outweighs 'mass < 91.2' (-1.158); the neuron is middling (mean 0.721), lowering W. The formula calls them t and is right only 62.7% of the time — often wrong.

### neuron 2: Total pT in the hardest particles (minor)

- **What it measures:** Follows the total pT carried by the 20-30 hardest particles and rises when the 30 hardest carry more than 0.919 of the jet pT; jets lighter than 91.2 GeV are pushed down. It varies little between jet types: slightly highest for gluons and Z jets, lowest for top jets.
- *computed — its value:* largest for g (0.56), then Z (0.46), then q (0.36), then W (0.32), then t (0.25); it separates t jets from the rest best (AUC 0.32: small for t)
- **How the class scores use it:** Only the Z score uses it, lowering it slightly (-3%); it is a small correction.
- *computed — used by:* lowers the score of Z (-3%); does not (or hardly) enter the score of g, q, W, t (share of each class score’s average input)

```
z = 0.112
if z_top30_slots > 0.919: z += 7.92 × (z_top30_slots − 0.919)
if mass < 91.20: z += -0.019 × (91.20 − mass)
if sum_pt > 1090: z += -0.011 × (sum_pt − 1090)
if sum_pt > 1010: z += 0.005 × (sum_pt − 1010)
if mass_over_sum_pt < 0.073: z += 23.70 × (0.073 − mass_over_sum_pt)
if lam2 < 0.00096: z += -408 × (0.00096 − lam2)
if log_sum_pt > 7.05: z += 11.70 × (log_sum_pt − 7.05)
if mass_top40 > 158: z += -0.046 × (mass_top40 − 158)
if sum_pt_top50 > 1110 and C2 > 0.096: z += 0.754 × (sum_pt_top50 − 1110) × (C2 − 0.096)
if sum_pt_top50 > 1030 and mean_phi > 3.2e-05: z += 3.93 × (sum_pt_top50 − 1030) × (mean_phi − 3.2e-05)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `z_top30_slots > 0.919`; 2: `mass < 91.2`; 3: `sum_pt > 1.09e+03`; 4: `sum_pt > 1.01e+03`; 5: `mass_over_sum_pt < 0.0732`; 6: `lam2 < 0.000964`):

- `✓✓·✓·✓` **W/Z jets, medium pT** — 15.1% of jets, neuron 0.37, formula right for 93%. Mostly W jets (63%) with Z (33%), mass near the W (mean 83.5 GeV), total pT between 1010 and 1090 GeV, typical two-prong spread. The 30-hardest-share test (+0.518) and the 1010 GeV cut (+0.125) outweigh the small mass and lam2 penalties, so the neuron sits modestly on (mean 0.368), barely touching q and Z. The formula calls them W and is right 93.2% of the time.
- `✓✓·✓✓✓` **Narrow light quark jets** — 9.9% of jets, neuron 0.41, formula right for 72%. Mostly quark jets (60%) with gluons and W, light (mean 42.3 GeV), one dominant hard particle and nearly 80% of the pT in the core. The low m/pT bonus (+0.773) and 30-hardest-share (+0.557) balance the -0.949 of 'mass < 91.2', leaving a small neuron (mean 0.41). The formula calls them q and is right 71.6% of the time; quark/gluon mix-ups are the main errors.
- `✓✓··✓✓` **Narrow light quarks, lower pT** — 8.9% of jets, neuron 0.21, formula right for 74%. Mostly quark jets (70%) with some gluons (14%), very light (mean 38.4 GeV) and core-dominated with one hard leader, total pT below 1010 GeV. Same balance as the previous group without the 1010 GeV bonus, so the neuron is small (mean 0.215) with little effect on the scores. The formula calls them q and is right 73.9% of the time.
- `✓✓···✓` **W/Z jets, lower pT** — 7.6% of jets, neuron 0.24, formula right for 84%. Mostly W jets (46%) with many Z (36%) and some tops (12%), mean mass 82.5 GeV, total pT below 1010 GeV, typical two-prong spread. Only the 30-hardest-share test adds (+0.512), minus small mass and lam2 penalties; the neuron is small (mean 0.239). The formula splits them W vs Z and is right 84.2% of the time.
- `······` **Heavy wide tops, nothing passes** — 7.6% of jets, neuron 0.10, formula right for 80%. Mostly tops (75%) with gluons (18%), heavy (mean 149 GeV) and wide, lower total pT, soft leader and pT spread far from the axis. No test passes; the neuron stays at its small base value (mean 0.104) and does almost nothing. The formula calls them t and is right 79.6% of the time, with gluons the usual confusion.
- `✓✓✓✓✓✓` **High-pT narrow gluon-led mixture** — 7.4% of jets, neuron 0.76, formula right for 81%. A mixture led by gluons (49% g, 23% W, 22% q), light (mean 57 GeV), high total pT (1227 GeV) and core-heavy with a hard leader. All tests pass; the 'sum_pt > 1090' penalty (-1.48) is more than offset by the other pT and m/pT bonuses, so the neuron is fairly high (mean 0.759), a small push toward q and away from Z. The formula calls them g about half the time and is right 80.9%.
- `✓··✓·✓` **Above-91 GeV Z jets** — 5.5% of jets, neuron 0.54, formula right for 92%. Mostly Z jets (82%), mass above 91.2 GeV (mean 98.8 GeV), typical two-prong spread, total pT above 1010 GeV. The 30-hardest-share (+0.505) and 1010 GeV cut (+0.151) put the neuron on (mean 0.535), taking a little from Z. The formula calls them Z and is right 91.5% of the time.
- `✓·····` **Heavy tops, few-particle core** — 4.4% of jets, neuron 0.30, formula right for 85%. Mostly tops (83%), heavy (mean 137 GeV), lower total pT, with the 30 hardest particles carrying most of the pT. Only the 30-hardest-share test adds (+0.265), so the neuron is small (mean 0.301). The formula calls them t and is right 85.2% of the time.
- `···✓··` **Heavy tops and gluons, mid-pT** — 4.0% of jets, neuron 0.20, formula right for 80%. Mostly tops (62%) with many gluons (27%), heavy (mean 153 GeV) and wide, total pT between 1010 and 1090 GeV, pT spread far from the axis. Only the 1010 GeV cut adds (+0.149); the neuron is small (mean 0.195). The formula calls them t and is right 79.9% of the time, with gluons the main confusion.
- `··✓✓··` **High-pT heavy gluon jets** — 3.1% of jets, neuron 1.17, formula right for 83%. Mostly gluons (70%) with tops (25%), heavy (mean 155 GeV), high total pT (1233 GeV), pT shared among many particles (the 30 hardest carry less than 91.9%). The 1010 GeV bonus (+1.116) against the 1090 GeV penalty (-1.546) leaves the intercept to carry the neuron (mean 1.167), the largest push here toward q and away from Z. The formula calls them g and is right 83.1% of the time.

### neuron 11: Mass 80-91 GeV, clean two-prong (minor)

- **What it measures:** Large for mass between 80.4 and 91.2 GeV, especially with few particles at 0.2 <= ΔR < 0.4 and an elongated (two-prong) pattern; very narrow jets are pushed down. W jets sit highest (AUC 0.82), Z jets next, top, quark and gluon jets low.
- *computed — its value:* largest for W (1.68), then Z (1.07), then t (0.38), then q (0.27), then g (0.25); it separates W jets from the rest best (AUC 0.82: large for W)
- **How the class scores use it:** It raises the W score (+8%) and lowers the q score (-7%): a clean two-prong jet at the W mass is a W, not a quark jet. The g, Z and t scores hardly use it.
- *computed — used by:* raises the score of W (+8%); lowers the score of q (-7%); does not (or hardly) enter the score of g, Z, t (share of each class score’s average input)

```
z = -0.037
if mass < 91.20: z += 0.064 × (91.20 − mass)
if mass < 80.40: z += -0.056 × (80.40 − mass)
if girth2_top30 < 0.0064: z += -306 × (0.0064 − girth2_top30)
if e2 < 0.026: z += 72.10 × (0.026 − e2)
if n_dr_0p2_0p4 < 9.59 and n_dr_0p1_0p2 < 22.00: z += 0.0051 × (9.59 − n_dr_0p2_0p4) × (22.00 − n_dr_0p1_0p2)
if z_dr_0p2_0p4 < 0.0063: z += 124 × (0.0063 − z_dr_0p2_0p4)
if mass_top50 < 89.60 and girth2_top15 < 0.0036: z += 4.37 × (89.60 − mass_top50) × (0.0036 − girth2_top15)
if n_dr_0p2_0p4 < 9.84 and girth2 < 0.0057: z += -30.50 × (9.84 − n_dr_0p2_0p4) × (0.0057 − girth2)
if n_dr_0p2_0p4 < 8.15 and z_dr_0p2_0p4 < 0.061: z += 1.02 × (8.15 − n_dr_0p2_0p4) × (0.061 − z_dr_0p2_0p4)
if mass < 80.40 and z_dr_0p2_0p4 < 0.034: z += -0.540 × (80.40 − mass) × (0.034 − z_dr_0p2_0p4)
if z_top5_slots > 0.545: z += -1.80 × (z_top5_slots − 0.545)
if z_dr_0_0p05 < 0.099: z += 5.36 × (0.099 − z_dr_0_0p05)
if mass < 106 and planar_flow < 0.368: z += 0.071 × (106 − mass) × (0.368 − planar_flow)
if n_dr_0p2_0p4 < 10.70 and z_dr_0p05_0p1 > 0.593: z += -0.331 × (10.70 − n_dr_0p2_0p4) × (z_dr_0p05_0p1 − 0.593)
if mass < 80.40 and D2 < 3.33: z += -0.019 × (80.40 − mass) × (3.33 − D2)
if mass < 103 and mass_top10 > 45.10: z += 0.00068 × (103 − mass) × (mass_top10 − 45.10)
if mass < 80.40 and sum_pt_top2 < 467: z += -6.8e-05 × (80.40 − mass) × (467 − sum_pt_top2)
if mass < 98.70 and D2 < 1.30: z += 0.033 × (98.70 − mass) × (1.30 − D2)
if max_dr < 0.296: z += 3.27 × (0.296 − max_dr)
if mass < 98.90 and n_dr_0p2_0p4 > 10.10: z += -0.003 × (98.90 − mass) × (n_dr_0p2_0p4 − 10.10)
if z_dr_0p05_0p1 > 0.851: z += 6.62 × (z_dr_0p05_0p1 − 0.851)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `mass < 91.2`; 2: `mass < 80.4`; 3: `girth2_top30 < 0.00644`; 4: `e2 < 0.0258`; 5: `n_dr_0p2_0p4 < 9.59 and n_dr_0p1_0p2 < 22`; 6: `z_dr_0p2_0p4 < 0.00633`):

- `······` **Heavy busy jets, no tests** — 23.7% of jets, neuron 0.28, formula right for 80%. Nearly a quarter of jets (23.69%): mostly tops (68%) with gluons (18%), heavy (mean 150.4 GeV), wide and busy with pT spread outward. No test passes, so the neuron sits at its small intercept (mean 0.281), a slight push to W. The formula calls them t and is right 80.2% of the time.
- `✓✓✓✓✓·` **Light narrow jets, busy periphery** — 13.2% of jets, neuron 0.28, formula right for 71%. A quark-gluon mixture (41% q, 35% g, 16% W), light (mean 52.2 GeV), core-heavy but with some pT in the 0.2-0.4 ring. 'mass < 91.2' (+2.506) and e2 bonuses are offset by 'mass < 80.4' and the girth penalty, so the neuron stays small (mean 0.278). The formula calls them q (52.2%) or g and is right only 71.1% of the time.
- `✓✓✓✓✓✓` **Very light one-prong quarks** — 11.9% of jets, neuron 0.35, formula right for 80%. Mostly quark jets (65%) with gluons (22%), very light (mean 35 GeV), one dominant particle and about 78% of the pT in the core. All tests pass; the bonuses exceed the penalties but a negative base value leaves the neuron small (mean 0.355). The formula calls them q and is right 80.3% of the time.
- `✓✓✓✓··` **Light gluon-led mixture** — 7.6% of jets, neuron 0.24, formula right for 70%. A gluon-led mixture (45% g, 28% q, 18% W), mass around 64 GeV, core-heavy but with more particles in the outer rings. The ring tests fail; mass and e2 bonuses nearly cancel the penalties, so the neuron is small (mean 0.241). The formula calls them g (49.3%) and is right only 69.9% of the time.
- `✓✓✓·✓✓` **Clean two-prong W below 80** — 6.8% of jets, neuron 2.39, formula right for 95%. Almost pure W (93%), mass just below 80.4 GeV (mean 78.2 GeV), clean two-prong jets with a quiet outer ring. 'mass < 91.2' and the two quiet-ring tests add about 1.9 with small penalties, so the neuron is high (mean 2.391), raising W (+1.42) and lowering q. The formula calls them W and is right 94.6% of the time.
- `✓···✓✓` **Z jets 80-91 GeV, quiet** — 5.5% of jets, neuron 2.09, formula right for 95%. Mostly Z jets (84%) with W (11%), mass between 80.4 and 91.2 GeV (mean 88.6 GeV), quiet outer ring, pT concentrated at 0.05-0.1. The quiet-ring tests and a small mass bonus make the neuron high (mean 2.089), which raises W (+1.24) even though these are Z jets; the formula still calls them Z and is right 94.8% of the time, so other terms override it.
- `✓·✓·✓✓` **Clean W jets 80-91 GeV** — 4.8% of jets, neuron 2.33, formula right for 94%. Mostly W jets (85%) with Z (11%), mass between 80.4 and 91.2 GeV (mean 82.6 GeV), quiet outer ring. The mass and quiet-ring bonuses give a high neuron (mean 2.332), raising W and lowering q. The formula calls them W and is right 94.2% of the time.
- `····✓✓` **Quiet Z jets above 91** — 3.8% of jets, neuron 1.69, formula right for 97%. Almost pure Z (96%), mass above 91.2 GeV (mean 93.4 GeV), clean two-prong with a quiet outer ring. Only the two quiet-ring tests pass (+0.383, +0.535), yet the neuron is fairly high (mean 1.69), raising W. The formula calls them Z and is right 97.3% of the time.
- `✓···✓·` **Z-mass jets, busier edge** — 3.2% of jets, neuron 0.69, formula right for 87%. Mostly Z jets (74%) with tops (15%), mass between 80.4 and 91.2 GeV (mean 88.3 GeV), with more pT in the 0.2-0.4 ring. Only the mass and ring-count tests add a little; the neuron is small (mean 0.686). The formula calls them Z and is right 87.2% of the time.
- `····✓·` **Heavier Z/top, busier edge** — 2.6% of jets, neuron 0.38, formula right for 82%. Mostly Z jets (60%) with tops (21%), mean mass 100.2 GeV, busier outer ring. Only the ring-count test passes (+0.161); the neuron is small (mean 0.375). The formula calls them Z and is right 81.7% of the time.

### neuron 15: Narrow hard core (weak) (minor)

- **What it measures:** Grows linearly with the pT of the 30 hardest particles and with pT concentrated close to the axis (large share within ΔR < 0.05, small LHA). It is small for all types: slightly highest for quark jets, lowest for top jets.
- *computed — its value:* largest for q (0.31), then g (0.21), then W (0.19), then Z (0.17), then t (0.11); it separates q jets from the rest best (AUC 0.65: large for q)
- **How the class scores use it:** It raises the Z score slightly (+2%); the g, q, W and t scores hardly use it.
- *computed — used by:* raises the score of Z (+2%); does not (or hardly) enter the score of g, q, W, t (share of each class score’s average input)

```
z = -3.06
z += 0.0024 × sum_pt_top30
if girth2_top50 < 0.013: z += -245 × (0.013 − girth2_top50)
if girth2_top50 < 0.013 and z_dr_0p2_0p4 < 0.129: z += 1850 × (0.013 − girth2_top50) × (0.129 − z_dr_0p2_0p4)
if log_sum_pt < 7.02: z += 6.82 × (7.02 − log_sum_pt)
if girth < 0.123: z += 9.18 × (0.123 − girth)
if z_dr_0p1_0p2 < 0.177: z += 4.55 × (0.177 − z_dr_0p1_0p2)
if girth < 0.050: z += -38.80 × (0.050 − girth)
if girth2_top5 < 0.0071: z += 68.90 × (0.0071 − girth2_top5)
if z_dr_0p2_0p4 < 0.019: z += -30.70 × (0.019 − z_dr_0p2_0p4)
if lam2 < 0.0021: z += 184 × (0.0021 − lam2)
if mass_top10 > 26.60: z += -0.0081 × (mass_top10 − 26.60)
if sum_pt < 1000: z += -0.0075 × (1000 − sum_pt)
if girth2_top5 < 0.0018 and n_dr_0p2_0p4 > 2.31: z += -28.90 × (0.0018 − girth2_top5) × (n_dr_0p2_0p4 − 2.31)
if z_dr_0p1_0p2 < 0.127 and sum_pt_top3 < 758: z += -0.006 × (0.127 − z_dr_0p1_0p2) × (758 − sum_pt_top3)
if girth2_top5 < 0.006 and max_dr < 0.332: z += -1640 × (0.006 − girth2_top5) × (0.332 − max_dr)
if z_dr_0p1_0p2 < 0.117 and planar_flow < 0.818: z += 5.76 × (0.117 − z_dr_0p1_0p2) × (0.818 − planar_flow)
if girth2_top5 < 0.0073 and sum_pt_top40 < 975: z += 1.23 × (0.0073 − girth2_top5) × (975 − sum_pt_top40)
if girth > 0.086: z += 3.75 × (girth − 0.086)
if sum_pt_top50 > 1120: z += -0.0021 × (sum_pt_top50 − 1120)
if sum_pt < 1000 and tau32 < 0.664: z += -0.034 × (1000 − sum_pt) × (0.664 − tau32)
if z_dr_0p05_0p1 > 0.849: z += -6.44 × (z_dr_0p05_0p1 − 0.849)
if girth < 0.051 and z_dr_0p2_0p4 > 0.067: z += -7980 × (0.051 − girth) × (z_dr_0p2_0p4 − 0.067)
h = max(0, z)
```

Combinations of its strongest if-statements (1: `sum_pt_top30`; 2: `girth2_top50 < 0.0135`; 3: `girth2_top50 < 0.0128 and z_dr_0p2_0p4 < 0.129`; 4: `log_sum_pt < 7.02`; 5: `girth < 0.123`; 6: `z_dr_0p1_0p2 < 0.177`):

- `✓✓✓✓✓✓` **Compact light mixed jets** — 47.0% of jets, neuron 0.34, formula right for 77%. Nearly half of jets (47.05%): a mixture of quarks (33%), W (26%), Z (20%) and gluons (17%), mean mass 64 GeV, compact with a strong core. The top-30 pT term (+2.4) and compactness bonuses outweigh the girth-top-50 penalty (-2.212); the neuron is small (mean 0.338), slightly raising Z and lowering W and t. The formula calls them q most often and is right 76.7% of the time.
- `✓✓✓✓✓·` **Two-prong W/Z, busier ring** — 19.9% of jets, neuron 0.04, formula right for 88%. A Z-W mixture (47% Z, 34% W, 11% t), mean mass 88 GeV, with more pT at 0.1-0.2 from the axis. Failing the 0.1-0.2 ring test removes a bonus, so the neuron is mostly off (on 15.3%). The formula calls them Z (48.3%) or W and is right 88.2% of the time.
- `✓··✓··` **Heavy wide tops, off** — 10.9% of jets, neuron 0.00, formula right for 87%. Mostly tops (85%), heavy (mean 163.7 GeV), wide, pT spread out. Only the top-30 pT term and the pT test pass; the neuron is off (on 0.4%). The formula calls them t and is right 87.1% of the time.
- `✓✓✓·✓✓` **High-pT compact gluons** — 10.5% of jets, neuron 0.08, formula right for 85%. Mostly gluons (65%) with quarks (13%) and W (12%), mean mass 72.7 GeV, high total pT (1265.6 GeV), core-heavy. Bonuses and the girth-top-50 penalty roughly cancel, so the neuron is mostly off (on 28.2%). The formula calls them g and is right 84.6% of the time.
- `✓··✓✓✓` **Heavy tops, empty 0.1-0.2 ring** — 2.3% of jets, neuron 0.56, formula right for 69%. Mostly tops (60%) with gluons (22%) and quarks (16%), mean mass 136 GeV, lower total pT, with pT concentrated within 0.1 and little at 0.1-0.2. Top-30 pT, pT, girth and ring bonuses pass with no penalty, giving a middling neuron (mean 0.557), a small push toward Z and away from t. The formula calls them t and is right only 68.9% of the time.
- `✓··✓·✓` **Heavy tops, quiet inner ring** — 2.2% of jets, neuron 0.09, formula right for 89%. Mostly tops (89%), heavy (mean 167 GeV), with pT sitting at 0.05-0.1 from the axis. Similar bonuses give only a small neuron (mean 0.088). The formula calls them t and is right 89.1% of the time.
- `✓··✓✓·` **Mid-heavy tops and gluons** — 2.1% of jets, neuron 0.03, formula right for 73%. Mostly tops (67%) with gluons (22%), mean mass 127 GeV, lower total pT. The neuron is nearly always off (on 8.8%). The formula calls them t and is right 73.4% of the time.
- `✓✓✓·✓·` **High-pT gluon/Z mix** — 1.6% of jets, neuron 0.00, formula right for 83%. A gluon-led mixture (43% g, 29% Z, 16% W), mean mass 107.3 GeV, high total pT (1236.4 GeV). The top-30 pT term and girth bonuses are offset by the girth-top-50 penalty; the neuron is off (on 0.9%). The formula calls them g and is right 82.7% of the time.
- `✓·····` **Very heavy high-pT gluon/top** — 1.1% of jets, neuron 0.00, formula right for 81%. A gluon-top mixture (54% g, 40% t), very heavy (mean 198.9 GeV), high total pT, wide. Only the top-30 pT term passes; the neuron is off (on 0.0). The formula calls them g (58.6%) or t and is right 80.9% of the time.
- `✓✓·✓✓✓` **Mixed mid-mass, compact core** — 0.6% of jets, neuron 0.63, formula right for 69%. A four-way mixture (37% t, 23% g, 22% q, 18% Z), mean mass 106.3 GeV, lower total pT, pT concentrated at 0.025-0.05. Most bonuses pass with a small girth-top-50 penalty; the neuron is middling (mean 0.632), a small push toward Z. The formula calls them t most often and is right only 69.1% of the time.
