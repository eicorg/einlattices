
# Beam Accumulator Ring (BAR) Design Updates

## V9.6 2026-07-05
- Updated the BAR lattice and survey files following Mike's requested component relocations.
- Shifted BPMs, quadrupoles, correctors, flags, beam instrumentation, and other components to match the requested layout.
- Added the dedicated RF BPM and relocated ICT02 to the RF straight.
- For BPM02, Q04F, and Q09F, the implemented shifts differ slightly from the original requested values. These changes were adjusted to preserve the symmetry of the BAR lattice, since BPM and quadrupole locations are constrained by the lattice symmetry.
- because the quadrupoles, kickers, and sextupoles moved, the quadrupoles and bend dipoles gradients changed slightly too, as well as kicker settings for injeciton-extraction
- ITL and ETL had to be slightly retuned (some element locations might have changed) because the optics in the BAR ring changed and ITL and ETL had to be re-matched to the new BAR optics.
- (small change on 2026-07-21) I moved the DCCT 30 cm upstream so that it's now 50 cm from the RF cavity.  

## V9.5 2026-07-01
- This is an updated lattice with pass methods like in Elegant for CSBEND, KQUAD, KSEXT, EKICKER, DRIFT elements
- Fringe fields in dipole bends and in quadrupoles are also included now, using Elegant's methods
- The quadrupoles required 10 fringe integrals for the fringe model, I used the results from Radia simulation for unchanged and re-machined MIT Bates quadrupoles
- These methods are re-implemented in PyAT and match Elegant to machine precision
- After this change the quadrupoles had to be retuned to go back to roughly the same optics functions.
- Additionally the gradient in the dipole bends had to be adjusted, which means the gap slope in the dipole magnets had to be modified accordingly
- Additionally, the WCM is removed now, because it became clear it would not be able to measure the bunch length, the bunch length is too short for existing wall current monitors.
- Because of switching to Elegant's pass methods and fringe field models, only .lte file will be provided for the BAR ring going forward. MAD-X does not have equivalent pass methods and fringe models. In ITL and ETL, madx files will continue to be provided, at least for now. 

## V9.4 2026-05-06
- Included Flags, ICTs, and WCM in the ITL, ETL, BAR lattice files

## V9.3 2026-05-06
- Added ICTs and WCM 

## Change on 2026-04-30
- Added ITL_parameters_table.csv and ETL_parameters_table.csv

## Change in V9.2 on 2026-04-21
- Switched back to 98MHz, h=12, and RF Cavity voltage V=100kV
- Added BAR_parameters_table.csv per Yi-Kai's request

## Change in V9.1 on 2026-04-14
- Added flags in the survey data

## Change in V9 on 2026-02-20
- Changed RF voltage to 155kV to be in agreement with the cost estimate submitted to EIC for Director's review.

## Changes in V9 on 2026-02-17
- Switched to new RF cavity: 49.25311707MHz and h=6; V=100kV.

## Changes Relative to V5/V6

### Orbit and Geometry
- Changed the distance from the stored to the injected/extracted orbit to  
  `INJECTION_ORBIT_TO_STORED_ORBIT_OFFSET = 0.036235 m`.

- Moved Q1 away from the septum; the center of Q1 is now **1.85 m** from the center of the septum.

- This allowed the **80 mrad dipole** to be moved past Q1, as the pipe now clears Q1 (assuming a **1-inch diameter pipe** in that region).

- The **80 mrad dipole** was later removed completely.

### Magnet Layout and Strengths
- To reduce the load on ITL/ETL quadrupoles that were near the maximum allowed gradient (~**16.9 T/m**), **one additional quadrupole** was added to each TL.

- The **BAR 45-degree dipole** is now a **sector dipole** (zero entrance/exit angles) with:
  - Body gradient: **−1.29 T/m**
  - Gap slope: **3 degrees**

### Survey and Element Keywords
- In the survey data:
  - Correctors now use the keyword `CORRECTOR`
  - The three kickers and the septum use the keyword `KICKER`

### Injection / Extraction Hardware Spacing
- Increased spacing around **BIUF1** and **BIUF3**, moving them farther from the quadrupole and corrector to reduce eddy currents and field distortions.

- **BIUF2** was also moved farther away from the quadrupole.

### Injection and Extraction Optics
- Matched the reference-trajectory angle of the injected beam to the actual slope of the injection bump.

- As a result, the beam leaving the septum during **injection** is at  
  **1.75e-3 rad** relative to the stored orbit.

- The same applies to the **extracted beam**.

- Updated the **D1/D2 bend angle** to:  
  `0.120 + 1.75e-3 rad`

- The injection bump slope actually is not exactly 1.75mrad, it's more like 1.73mrad, but I want to fix the D1/D2 at 121.75mrad and the injected beam slope
  at 1.75mrad moving forward. We will neglect small injection bump slope changes from now on (e.g., around +-0.1mrad).   

### Kicker Configuration
- Revised the extraction kicker scheme: the extraction bump now starts from **BIUF3**, allowing a reduced kick in **BIUF1**.

- All kickers are now **< 4 mrad** during injection and extraction.

### Correctors and Sextupoles
- In the new BAR lattice, sufficient space was found to relocate correctors:
  - Moved them between the quadrupole and the 45-degree dipole in the **septum and RF straights**
  - Two correctors per straight
  - Removed two correctors at the **10 and 2 o’clock** locations

- First, moved one **SD sextupole** from **4 o’clock** to **2 o’clock**.
- 2026-02-09 --- did a mirror reflection of SDs around the vertical (X) axis.
  This will allow to place a flag at the 2 o'clock location which has a small betax and large dispersion.
  Energy spread-dominated beam size.
  I believe this is also better, because the injected beam still has large amplitude at 2 o'clock,
  so the kick from the sextupole was at large amplitude. Removing the sextupole from 2 o'clock and placing it at
  10 o'clock is better. At 10 o'clock, the injected beam's amplitude will be smaller.
  I also had to move BPMs because of that.

- This improved:
  - **DA** by ~**50%**
  - **MA** by ~**×2**  
  (both after accounting for lattice errors)

### BPMs and Phase Advance
- Moved **two BPMs** to reduce the maximum phase gap from **139°** to **124°** in those areas.

### Naming Conventions
- Updated **CXYSQ corrector** names to include skew family and polarity:
  - Families: **A**, **B**
  - Polarities: **F**, **D**

### Spin Dynamics
- Identified an error in the spin-resonance check: **V5 and V6** were located exactly on the  
  `G * gamma + nu_y = 3` resonance.

- Updated the working point to:
  - `nu_x = 2.4150`
  - `nu_y = 1.4553`

- The new working point also provides **20–50% better DA and MA**.

