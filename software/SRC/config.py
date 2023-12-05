import numpy as np

# display: corresponding to the visual status
ALLWIN = 0
TRANSS = 1
SAGITA = 3
VIEW3D = 4


## init value setting

# system manager
minimum = -1000
maximum = 2000
lower2Dvalue = -100
upper2Dvalue = 500
lower3Dvalue = -100
upper3Dvalue = 500

# dicoms
axialMtx = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
sagittalMtx = np.array(	[0, 0,-1, 0, 1, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 1])
cornalMtx = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, -1,0, 0, 0, 0, 0, 1])

# landmarks
lm_color = [255, 0, 0] #red
lm_radius = 10
lm_visible = 1
lm_opacity = 1

# meshes
mesh_colors = [[200,200,180], [69,130,30], [0,255,0], [0,0,255], [255,255,0], [0,255,255]]
mesh_visible = 1
mesh_opacity = 1

# implants
ip_radius = 5
ip_colors = [[0,255,0], [0,0,255], [0,255,255]]
ip_opacity = 0.5
ip_visible = 2
ip_dash_length = 8
ip_line_rate = 2
ip_cylinder_res = 36

# tool 
to_color = [255, 255, 0]
to_visible = 1
to_opcaity = 1
to_matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

# progress
pg_start = 30
pg_middle = 75
pg_end = 100

#tableWidget
text_margin = 1.2
min_margin = 60


