import raylibpy as raylib
from classes import Grid

width, height = 700,500
raylib.set_config_flags(raylib.FLAG_WINDOW_RESIZABLE)
raylib.init_window(width,height,"wave fuction collapse")



tileSize = 20
tileActualSize = 10

def draw():
    raylib.begin_drawing()
    raylib.clear_background(raylib.Color(0,0,0,255))
    grid.draw()
    raylib.draw_fps(10,10)
    raylib.end_drawing()

def processInput():
    if raylib.is_key_pressed(raylib.KEY_F11):
        raylib.toggle_borderless_windowed()

gridSize = 1920//tileSize,1080//tileSize

#0 = open 1 = closed
tiles = {
    1:{
        "name":"straight1",
        "edges":[0,1,0,1],
        "frequency":10
        },
    2:{
        "name":"straight2",
        "edges":[1,0,1,0],
        "frequency":10
        },
    3:{
        "name":"corner1",
        "edges":[0,0,1,1],
        "frequency":1
        },
    4:{
        "name":"corner2",
        "edges":[1,0,0,1],
        "frequency":1
        },
    5:{
        "name":"corner3",
        "edges":[1,1,0,0],
        "frequency":1
        },
    6:{
        "name":"corner4",
        "edges":[0,1,1,0],
        "frequency":1
        },
    7:{
        "name":"empty",
        "edges":[1,1,1,1],
        "frequency":100
        },    
    8:{
        "name":"roomMiddle",
        "edges":[2,2,2,2],
        "frequency":20
        },
    9:{
        "name":"T-cross1",
        "edges":[0,0,0,1],
        "frequency":1
        },
    10:{
        "name":"T-cross2",
        "edges":[1,0,0,0],
        "frequency":1
        },
    11:{
        "name":"T-cross3",
        "edges":[0,1,0,0],
        "frequency":1
        },
    12:{
        "name":"T-cross4",
        "edges":[0,0,1,0],
        "frequency":1
        },
    13:{
        "name":"X-cross",
        "edges":[0,0,0,0],
        "frequency":1
        },
    14:{
        "name":"roomCorner1",
        "edges":[3,1,1,3],
        "frequency":1
        },
    15:{
        "name":"roomCorner2",
        "edges":[1,1,3,4],
        "frequency":1
        },
    16:{
        "name":"roomCorner3",
        "edges":[1,4,4,1],
        "frequency":1
        },
    17:{
        "name":"roomCorner4",
        "edges":[4,3,1,1],
        "frequency":1
        },
    18:{
        "name":"roomEntrance1",
        "edges":[4,2,4,0],
        "frequency":1
        },
    19:{
        "name":"roomEntrance2",
        "edges":[2,3,0,3],
        "frequency":1
        },
    20:{
        "name":"roomEntrance3",
        "edges":[3,0,3,2],
        "frequency":1
        },
    21:{
        "name":"roomEntrance4",
        "edges":[0,4,2,4],
        "frequency":1
        },
    22:{
        "name":"roomWall1",
        "edges":[1,4,2,4],
        "frequency":2
        },
    23:{
        "name":"roomWall2",
        "edges":[4,2,4,1],
        "frequency":2
        },
    24:{
        "name":"roomWall3",
        "edges":[2,3,1,3],
        "frequency":2
        },
    25:{
        "name":"roomWall4",
        "edges":[3,1,3,2],
        "frequency":2
        },
    # 26:{
    #     "name":"emptyCorner1",
    #     "edges":[3,4,2,2],
    #     "frequency":1
    #     },
    # 27:{
    #     "name":"emptyCorner2",
    #     "edges":[4,2,2,4],
    #     "frequency":1
    #     },
    # 28:{
    #     "name":"emptyCorner3",
    #     "edges":[2,2,4,3],
    #     "frequency":1
    #     },
    # 29:{
    #     "name":"emptyCorner4",
    #     "edges":[2,3,3,2],
    #     "frequency":1
    #     },
    }

for key in tiles:
    tiles[key]["image"] = raylib.load_texture("images/"+tiles[key]["name"]+".png")
grid = Grid(gridSize,tiles,tileSize,tileActualSize)
i = 0
per = 0
while grid.solve() and not raylib.window_should_close():
    i+=1
    new = max(int((i/(gridSize[0]*gridSize[1]))*100),1)
    if new != per:
        per = new
        print(" |"+ "█"*round(per/2)+"-"*round((100-per)/2),end = f"| {per}%\r")
    draw()
    processInput()





while not raylib.window_should_close():
    draw()
    processInput()
