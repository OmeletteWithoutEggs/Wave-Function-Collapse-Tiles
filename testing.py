tiles = {
    1:{
        "edges":[0,1,0,1]
    },
    2:{
        "edges":[1,0,1,0]
    },
    3:{
        "edges":[1,1,1,1]
    },
    4:{
        "edges":[0,0,0,0]
    }

}


def findMatches(target):
    matches = []
    for tileID in tiles:
        tile = tiles[tileID]
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

print(findMatches([-1,-1,-1,-1]))