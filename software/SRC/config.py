import numpy as np
import vtk


# 所有颜色注意vtk渲染和qt渲染的区别，乘除255

# display: corresponding to the visual status
ALLWIN = 0
AXIAL = 1
SAGITA = 2
CORNAL = 3
VIEW3D = 4
VIEWORDER = [0,2,3,1]
initial_2Dcolor = np.array([0,0,0])
bottom_3Dcolor = np.array([1, 1, 1])
top_3Dcolor = np.array([0.75294118, 0.75294118, 1 ])

# 使用Unicode字符表示立方
cubic = "³"


## init value setting

# system manager
minimum = -2000
maximum = 2000
lower2Dvalue = -800
upper2Dvalue = 500
lower3Dvalue = -400
upper3Dvalue = 300
volume_color1 = [1, 1, 1]
volume_color2 = [1, 1, 1]
volume_color3 = [1, 1, 1]
volume_opacity = 1

# dicoms
axialMtx = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
sagittalMtx = np.array(	[0, 0,-1, 0, 1, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 1])
cornalMtx = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, -1,0, 0, 0, 0, 0, 1])
axialNormal = np.array([0, 0, 1])
sagittalNormal = np.array([1, 0, 0])
cornalNormal = np.array([0, 1, 0])
ParallelScale = 120
zoom = 1.2
scroll_list = [0, 1, 2]

# landmarks
lm_color = [1, 0, 0] #red
lm_radius = 100
lm_visible = 1
lm_opacity = 1

# meshes
mesh_colors = [[1, 0.9, 0.8], [0.4, 0.7, 0.8], [0,1,0], [0,0,1], [1,1,0], [0,1,1]]
mesh_visible = 0
mesh_opacity = 1

# implants
ip_radius = 5
ip_colors = [[0,1,0], [0,0,1], [0,1,1]]
ip_opacity = 0.5
ip_visible = 2
ip_dash_length = 8
ip_line_rate = 2
ip_cylinder_res = 36

# tool 
to_color = [1, 1, 0]
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


# registration
numOfLight = 12



