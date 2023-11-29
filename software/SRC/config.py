import PyQt5.QtGui as QtGui

# display: corresponding to the visual status
ALLWIN = 0
TRANSS = 1
SAGITA = 3
VIEW3D = 4


## init value setting

# system manager
lower2Dvalue = 0
upper2Dvalue = 100
lower3Dvalue = 0
upper3Dvalue = 100

# landmarks
lm_color = [255, 0, 0] #red
lm_radius = 10
lm_visible = 1
lm_opacity = 1

# meshes
mesh_colors = [[255,255,0], [128,0,128], [69,130,30], [0,255,0], [0,0,255], [0,255,255]]
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
to_color = [0, 255, 255]
to_visible = 1
to_opcaity = 1

# progress
pg_start = 30
pg_middle = 75
pg_end = 100

#tableWidget
text_margin = 1.2
min_margin = 60


