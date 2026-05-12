!!Beam parameters
beam_BAR.bmad  - beam paramenters from BAR at P2 (D2 interface point)
beam_pre_inj.bmad  - beam parameters from the pre-injector

!!Lattices
LTR_dump.bmad  - Beamline from pre-injector to the dump
LTR_main.bmad  - Beamline from pre-injector to RCS injection
LTR_P1.bmad  - Beamline from pre-injector to P1 (D1 interface point) when BAR is in use
LTR_P2.bmad  - Beamline from P2 to RCS injection when BAR is in use
LTR_P2_dump.bmad  - Beamline from P2 to the dump when BAR is in use
RCS_lattice.bmad - RCS lattice section with the injection kicker

When BAR is active both LTR_P1.bmad and LTR_P2.bmad are used instead of the other lattices
If the BAR beams goes to the dump, use LTR_P1.bmad and LTR_P2_dump.bmad

