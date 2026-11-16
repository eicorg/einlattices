### Preinjector Survey and Lattice 

Erdong Wang

*lattice_OUTPAR_sep.xlsx*

This is a **PARMELA v3.4** generated survey and lattice file. It starts from the electron source and ends at the exit of the Linac. It includes a total of 14 Linac structures plus a drift space able to take two more 3-meter structures. The point in the survey file labeled **<- connect to LTR** is the end of the lattice file. 

Only the main beamline is included. 

Diagnostics lines and components are not included. 

Correctors are in units of Gauss-cm and BPMs are zero length; dimensions are left to engineers to decide. 

Vacuum ports and pumps are not included. 

##### Attention: 

1. In **survey**: The *solenoid* is a single element which has two coils; in **requirements**, these solenoids are split into two lines, powered by two power supplies. 
2. In **survey**: If a *cell* is labeled as *fringe*, it is not a real component. These are fringe fields modeled as cells. 
3. In **survey**: If the *solenoid* is labeled *doublet/triplet/corrector*, these components are TBD. Both solenoids and quads work from a beam dynamics point of view. The final decision will be based on test results or engineering layout. This will be decided after 2-3 iterations.