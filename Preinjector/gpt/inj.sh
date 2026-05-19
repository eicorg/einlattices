#!/bin/zsh

# dftrans -o traj.gdf result.gdf time x y z
#gdfa -o std.gdf au1.gdf time avgx avgy avgz stdx stdy stdz nemixrms nemiyrms nemirrms avgG
#/home/wange/Project/GPT/gpt322mpi-rhel65/bin/gdfa -o tout.gdf au1_550.gdf time avgz avgy avgx avgG avgfEz avgfEy avgfEx avgfBx avgfBy avgfBz
#stdx stdy stdz nemixrms nemiyrms nemirrms stdG rmax 
/home/wange/Project/GPT/gpt322mpi-rhel65/bin/gdfa -o screen.gdf au1_550.gdf position avgx avgy avgz avgG  stdx stdy   nemixrms nemiyrms nemirrms rmax CSalphax CSalphay CSbetax CSbetay
gdftrans -o traj.gdf au1_550.gdf time x y z
gdf2a -o traj.txt traj.gdf
#gdf2dxf -l -o tranjec.dxf au1.gdf y z
/home/wange/Project/GPT/gpt322mpi-rhel65/bin/gdf2a -o screen.txt screen.gdf
#gdf2a -o std.txt std.gdf
#/home/wange/Project/GPT/gpt322mpi-rhel65/bin/gdf2a -o tout.txt tout.gdf
