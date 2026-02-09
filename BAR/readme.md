
# Beam Accumulator Ring (BAR) Design Updates

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
  **1.66e-3 rad** relative to the stored orbit.

- The same applies to the **extracted beam**.

- Updated the **D1/D2 bend angle** to:  
  `0.120 + 1.66e-3 rad`

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

