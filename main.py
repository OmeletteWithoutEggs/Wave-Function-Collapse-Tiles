import raylibpy as raylib
from classes import Grid

width, height = 1920,1080
raylib.set_config_flags(raylib.FLAG_WINDOW_RESIZABLE|raylib.FLAG_FULLSCREEN_MODE)
raylib.init_window(width,height,"wave fuction collapse")

tileSize = 20

def draw():
    raylib.begin_drawing()
    raylib.clear_background(raylib.Color(0,0,0,255))
    grid.draw()
    raylib.draw_fps(10,10)
    raylib.end_drawing()

gridSize = 1920//tileSize,1080//tileSize

#0 = open 1 = closed
tiles = {
    1:{
        "name":"straight1",
        "edges":[0,1,0,1],
        },
    2:{
        "name":"straight2",
        "edges":[1,0,1,0],
        },
    # 3:{
    #     "name":"corner1",
    #     "edges":[0,0,1,1],
    #     },
    # 4:{
    #     "name":"corner2",
    #     "edges":[1,0,0,1],
    #     },
    # 5:{
    #     "name":"corner3",
    #     "edges":[1,1,0,0],
    #     },
    # 6:{
    #     "name":"corner4",
    #     "edges":[0,1,1,0],
    #     },
    7:{
        "name":"empty",
        "edges":[1,1,1,1],
        },    
    # 8:{
    #     "name":"roomMiddle",
    #     "edges":[2,2,2,2],
    #     },
    # 9:{
    #     "name":"T-cross1",
    #     "edges":[0,0,0,1],
    #     },
    # 10:{
    #     "name":"T-cross2",
    #     "edges":[1,0,0,0],
    #     },
    # 11:{
    #     "name":"T-cross3",
    #     "edges":[0,1,0,0],
    #     },
    # 12:{
    #     "name":"T-cross4",
    #     "edges":[0,0,1,0],
    #     },
    # 13:{
    #     "name":"X-cross",
    #     "edges":[0,0,0,0],
    #     },
    14:{
        "name":"roomCorner1",
        "edges":[3,1,1,3],
        },
    15:{
        "name":"roomCorner2",
        "edges":[1,1,3,4],
        },
    16:{
        "name":"roomCorner3",
        "edges":[1,4,4,1],
        },
    17:{
        "name":"roomCorner4",
        "edges":[4,3,1,1],
        },
    18:{
        "name":"roomEntrance1",
        "edges":[4,2,4,0],
        },
    19:{
        "name":"roomEntrance2",
        "edges":[2,3,0,3],
        },
    20:{
        "name":"roomEntrance3",
        "edges":[3,0,3,2],
        },
    21:{
        "name":"roomEntrance4",
        "edges":[0,4,2,4],
        },
    22:{
        "name":"roomWall1",
        "edges":[1,4,2,4],
        },
    23:{
        "name":"roomWall2",
        "edges":[4,2,4,1],
        },
    24:{
        "name":"roomWall3",
        "edges":[2,3,1,3],
        },
    25:{
        "name":"roomWall4",
        "edges":[3,1,3,2],
        },
    # 26:{
    #     "name":"emptyCorner1",
    #     "edges":[3,4,2,2],
    #     },
    # 27:{
    #     "name":"emptyCorner2",
    #     "edges":[4,2,2,4],
    #     },
    # 28:{
    #     "name":"emptyCorner3",
    #     "edges":[2,2,4,3],
    #     },
    # 29:{
    #     "name":"emptyCorner4",
    #     "edges":[2,3,3,2],
    #     },
    }

for key in tiles:
    tiles[key]["image"] = raylib.load_texture("images/"+tiles[key]["name"]+".png")
grid = Grid(gridSize,tiles,tileSize)
i = 0
while grid.solve() and not raylib.window_should_close():
    i+=1
    per = max(int((i/(gridSize[0]*gridSize[1]))*100),1)
    print(str(per)+"%")
    draw()



while not raylib.window_should_close():
    draw()
