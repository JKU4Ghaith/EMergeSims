# Importing Emerge
import emerge as em
from emerge.plot import plot_ff
import numpy as np
# Define the geometry of waveguide
wg_length = 40
wg_width = 20
wg_height = 20
# Define the excitation position
excitation_z_pos = -10
# Define the operating frequency
f = 10e6
# Setting up the simulation model
model = em.Simulation('ParallelPlateWG')

# Creating geometries
box = em.geo.Box(wg_width, wg_height, wg_length, (-wg_width/2,-wg_height/2,-wg_length/2))

excitation_plate = em.geo.XYPlate(wg_width,wg_height,(-wg_width/2,-wg_height/2,excitation_z_pos))
excitation_plate.foreground()   # Giving the excitation sheet a higher priority

# Committing geometry: every face has its tag
model.commit_geometry()
model.view()
# Generating mesh. Be aware that the mesh size is frequency dependent, so set
# the model frequency before mesh generation to the maximum operating frequency
model.mw.set_frequency(f)
model.generate_mesh()

# Assigning names
top_plate = box.face('front')
bottom_plate = box.face('back')
left_boundary = box.face('left')
right_boundary = box.face('right')
front_boundary = box.face('top')
back_boundary = box.face('bottom')

# Setting boundaries
# Note that ports in EMerge are considered as boundary conditions
model.mw.bc.PEC(front_boundary)
model.mw.bc.PEC(back_boundary)

model.mw.bc.PMC(left_boundary)
model.mw.bc.PMC(right_boundary)

model.mw.bc.AbsorbingBoundary(top_plate)
model.mw.bc.AbsorbingBoundary(bottom_plate)

port1 = model.mw.bc.LumpedPort(face=excitation_plate, width=wg_width, height=wg_height, direction=em.YAX, port_number=1, Z0=376)

# Display geometries
model.display.add_object(obj=top_plate, color='red', opacity=1, show_edges=True)
model.display.add_object(obj=bottom_plate, color='red', opacity=1, show_edges=True)

model.display.add_object(obj=left_boundary, color='yellow', opacity=0.5, show_edges=True)
model.display.add_object(obj=right_boundary, color='yellow', opacity=0.5, show_edges=True)

model.display.add_object(obj=front_boundary, color='black', opacity=1, show_edges=True)
model.display.add_object(obj=back_boundary, color='black', opacity=1, show_edges=True)

model.display.add_object(obj=excitation_plate, color='blue', opacity=1)

model.view(plot_mesh=True)

# Run simulation
data = model.mw.run_sweep()

# View results
model.display.add_object(box)
model.display.animate().add_surf(*data.field[0].cutplane(ds=0.5,y=0).scalar('Ey','complex'),cmap="rainbow")
model.display.show()