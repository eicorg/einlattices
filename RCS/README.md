# einlattices
This repository contains the lattice files for the EIC EIN subproject
-Sep 11, 2026: added RCSV6S0 lattices for 18 GeV. Modifications include:
     * increasing RF drift space in straight to accomodate two 5 cell RF cavities
     * increase in drift between arc matching quads
     * increase of aperture to 100 mm from 40 mm for all quads surrounding RF cavities.
-Oct 12, 2026: RCSV6S0 arc cell adjustment (MADX, BMAD, ELEGANT):
     * added CLOB drift (0.0126+0.05 m) between BPM and corrector in each arc half-cell (replaces CLO there)
     * VACT shortened by 0.025 m and DSQ shortened by 0.025 m (cell length unchanged)
-Oct 13, 2026: RCSV6S0 arc BPM move and RF cavity fix (MADX, BMAD, ELEGANT):
     * arc BPM moved to the end of each half-cell (... DSQ, BPM, QLO, quad); its old 0.02 m slot is now the drift SBM
     * DSQ shortened by a further 0.02 m (0.059654-0.025-0.02 m; cell length unchanged)
     * injection straight RF slots corrected from "RFC_D, RFC" to "RFC_D, RFC_D" in the MADX file, matching BMAD (8 cavities, all in the extraction straight)
     * ELEGANT file rewritten to mirror the BMAD/MADX line structure, with MAXAMP apertures instead of ECOL elements
