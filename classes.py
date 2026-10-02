import random
import numpy as np
import sys
import raylibpy as raylib

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Tile():
    def __init__(self,tileData,key):
        self.type = tileData[key]
        self.name = tileData["name"]
        self.edges = tileData["edges"]
        self.north = self.edges[0]
        self.east = self.edges[1]
        self.south = self.edges[2]
        self.west = self.edges[3]
        self.calculateValidNeigbours(tileData)

    def calculateValidNeigbours(self,tiles): # rotation not accounted
        self.validNorth = []
        self.validEast = []
        self.validSouth = []
        self.validWest = []

        for key in tiles:
            edges = tiles[key]["edges"]
            if self.north == edges[SOUTH]:
                self.validNorth.append(key)
            if self.east == edges[WEST]:
                self.validEast.append(key)
            if self.south == edges[NORTH]:
                self.validSouth.append(key)
            if self.west == edges[EAST]: 
                self.validWest.append(key)


class Grid():
    def __init__(self,size,tiles,tileSize,tileActualSize ):

        # tiles
        self.tiles = tiles
        self.tileSize = tileSize
        self.tileActualSize = tileActualSize

        self.updated = []
        # grid
        self.gridWidth = size[0]
        self.gridHeight= size[1]
        self.cachedTexture = raylib.load_render_texture(self.gridWidth*self.tileActualSize,self.gridHeight*self.tileActualSize)
        self.grid = np.full((self.gridWidth,self.gridHeight),0)

        # calculation grids
        print(list(self.tiles.keys()))
        self.possibilities = np.full((self.gridWidth,self.gridHeight,len(self.tiles)),list(self.tiles.keys()))
        self.entropy = np.full((self.gridWidth,self.gridHeight),len(self.tiles))
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if (x+y)%2==0:
                    self.calculatePossibilities((x,y))

    def solve(self): # done
        position = self.findNextPosition()
        if position == -1:
            return False
        choices = self.possibilities[position][self.possibilities[position]!=-1]
        weights = [self.tiles[tileId]["frequency"] for tileId in choices]
        try:
            choice = random.choices(choices,weights = weights,k=1)[0]
            self.grid[position] = choice
            self.possibilities[position] = [-1 for i in range(len(self.tiles)-1)] + [choice]
            # print(self.possibilities[position])
            self.entropy[position] = -1
        except:
            self.grid[position] = -1
            self.entropy[position] = -1
        self.calculatePossibilities(position)
        self.calculateEntropy()
        return True

    def calculateEntropy(self):  #done
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if self.entropy[x,y] != -1:
                    self.entropy[x,y] = np.count_nonzero(self.possibilities[x,y]!=-1)

    def calculatePossibilities(self,origin):
        """origin is a tuple in the form (x,y)"""
        self.updated = [] 
        stack :list[tuple] = [
                (min(origin[0] + 1,self.gridWidth-1), origin[1]),
                (origin[0], min(origin[1] + 1,self.gridHeight-1)),
                (max(origin[0] - 1,0), origin[1]),
                (origin[0], max(origin[1] - 1,0)),
            ]
        self.updated = stack.copy()
        while len(stack) > 0:
            changes :list[tuple] = self.updatePosition(stack[0])
            if changes:
                stack += changes
            if not stack[0] in self.updated:
                self.updated.append(stack[0])
            stack.pop(0)
        # print()

    def updatePosition(self,position) -> list[tuple]:
        """position is a tuple in the form (x,y)\n
        returns a list of the tile positions that have been changed
        """
        removes = []
        surroundingEdges = self.getSurroundingEdges(position)
        for possibility in self.possibilities[position]:
            if possibility == -1:
                continue
            for i in range(4):
                # print(self.tiles[possibility]["edges"][i])
                # print(surroundingEdges[i])
                # print()
                if not self.tiles[possibility]["edges"][i] in surroundingEdges[i]:
                    removes.append(possibility)
                    break

        for remove in removes:
            self.possibilities[position][self.possibilities[position]==remove] = -1

        if len(removes)> 0:
            return [
                (min(position[0] + 1,self.gridWidth-1), position[1]),
                (position[0], min(position[1] + 1,self.gridHeight-1)),
                (max(position[0] - 1,0), position[1]),
                (position[0], max(position[1] - 1,0)),
            ]
        else:
            return 


    def getSurroundingEdges(self,position) -> list[list[int]]: #done
        x,y = position
        edges = []
        edges.append(self.getTileEdgesInDirection((x,y+1),SOUTH))
        edges.append(self.getTileEdgesInDirection((x+1,y),WEST))
        edges.append(self.getTileEdgesInDirection((x,y-1),NORTH))
        edges.append(self.getTileEdgesInDirection((x-1,y),EAST))

        return edges

    def getTileEdgesInDirection(self,position,direction):
        if 0 <= position[0] < self.gridWidth:
            if 0 <= position[1] < self.gridHeight:
                side = []
                for possibility in self.possibilities[position]:
                    if possibility == -1:
                        continue
                    thisEdge = self.tiles[possibility]["edges"][direction]
                    if not thisEdge in side:
                        side.append(thisEdge)
                if side:
                    return side
                else:
                    return[0,1,2,3,4]

            
        return [0,1,2,3,4]

    def findMatchingEdges(self,position,target) -> list: #done
        """rotation not yet accounted for"""
        matches = []
        for tileID in self.possibilities[position]:
            tile = self.tiles[tileID]
            currentEdges = tile["edges"]
            correct = True
            for i in range(4):
                if target[i] == -1: #can be any edge
                    continue
                if currentEdges[i] != target[i]:
                    correct = False
                    break

            if correct:
                matches.append(tileID)

        return matches        

    def findNextPosition(self): # done
        options = []
        minimum = sys.maxsize
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                value = self.entropy[x,y]
                if value == -1: #already filled
                    continue
                elif value < minimum:
                    options = []
                    options.append((x,y))
                    minimum = value
                elif value == minimum:
                    options.append((x,y))

        if len(options) == 0:
            return -1
        position = random.choice(options)
        return position

    def draw(self):
        raylib.begin_texture_mode(self.cachedTexture)
        for update in self.updated:
            x,y = update
            raylib.draw_rectangle(x*self.tileActualSize,y*self.tileActualSize,self.tileActualSize,self.tileActualSize,raylib.Color(0,0,0,255))
            raylib.begin_blend_mode(raylib.BLEND_ADDITIVE)
            ids = []
            for i in range(len(self.tiles)):
                tileID = self.possibilities[x,y][i]
                if tileID != -1:
                    ids.append(tileID)
            if not ids:    
                raylib.draw_rectangle(x*self.tileActualSize,y*self.tileActualSize,self.tileActualSize,self.tileActualSize,raylib.Color(0,255,255,255))
            for tileID in ids:
                try:
                    raylib.draw_texture_pro(self.tiles[tileID]["image"],raylib.Rectangle(0,0,self.tileActualSize,-self.tileActualSize),raylib.Rectangle(x*self.tileActualSize,y*self.tileActualSize,self.tileActualSize,self.tileActualSize),raylib.Vector2(0,0),0,raylib.Color(255,255,255,255//len(ids)))
                except:
                    pass
            raylib.end_blend_mode()

        raylib.end_texture_mode()
        raylib.draw_texture_pro(self.cachedTexture.texture,raylib.Rectangle(0,0,self.tileActualSize*self.gridWidth,-self.tileActualSize*self.gridHeight),raylib.Rectangle(0,0,self.tileSize*self.gridWidth,self.tileSize*self.gridHeight),raylib.Vector2(0,0),0,raylib.Color(255,255,255,255))

        # for x in range(self.gridWidth):
        #     for y in range(self.gridHeight):
        #         tileID = self.grid[x,y]
        #         if tileID == 0:
        #             #raylib.draw_rectangle(x*self.tileSize,y*self.tileSize,self.tileSize-1,self.tileSize-1,(255,0,255,255))
        #             continue
        #         if tileID == -1:
        #             raylib.draw_rectangle(x*self.tileSize,y*self.tileSize,self.tileSize-1,self.tileSize-1,(0,255,255,255))
        #             continue
        #         # raylib.draw_texture_ex(self.tiles[tileID]["image"],(x*self.tileSize,y*self.tileSize),0,0.99,(255,255,255,255))
        #         raylib.draw_texture_pro(self.tiles[tileID]["image"],(0,0,10,-10),(x*self.tileSize,y*self.tileSize,self.tileSize,self.tileSize),(0,0),0,(255,255,255,255))
