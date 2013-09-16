#!/usr/bin/python

from time import time

import AStar

class AStarPathFinding :
    
    colors = [
        ' - ', # 0 - empty
        ' I ', # 1 - input
        ' O ', # 2 - output
        ' | ', # 3 - wall
        ' @ '  # 4 - path
    ]
    pathlines = []

    def initMap( self, w, h ) :
        self.mapdata = []
        self.mapw = w
        self.maph = h
        self.startpoint = [ 0, 1 ]
        self.endpoint = [ w - 1 , h - 2 ]
        
        size = w * h;
        for i in range( size ):
            self.mapdata.append( 0 )

        self.mapdata[ ( self.startpoint[ 1 ] * w ) + self.startpoint[ 0 ] ] = 1
        self.mapdata[ ( self.endpoint[ 1 ] * w ) + self.endpoint[ 0 ] ] = 2

    def drawMap( self ) :
        if len( self.pathlines ) :
            for p in self.pathlines :
                self.mapdata[ ( p[ 1 ] * self.mapw ) + p[ 0 ] ] = 4
        x = 0
        y = 0
        rect = [ 0, 0, self.mapw, self.maph ]
        o = ''
        for p in self.mapdata :
            if p == -1 :
                p = 0
            x += 1
            o += self.colors[ p ]
            if x >= self.mapw :
                x = 0
                y += 1
                print o
                o = ''
    
    def findPath( self ) :
        
        astar = AStar.AStar( AStar.SQ_MapHandler( self.mapdata, self.mapw, self.maph ) )
        start = AStar.SQ_Location( self.startpoint[ 0 ],self.startpoint[ 1 ] )
        end = AStar.SQ_Location( self.endpoint[ 0 ], self.endpoint[ 1 ] )

        s = time()
        p = astar.findPath( start, end )
        e = time()

        if not p :
            print "No path found!"
        else :
            print "Found path in %d moves and %f seconds." % ( len( p.nodes ), ( e - s ) )
            self.pathlines = []
            self.pathlines.append( ( start.x, start.y ) )
            for n in p.nodes :
                self.pathlines.append( ( n.location.x, n.location.y ) )
            self.pathlines.append( ( end.x, end.y ) )
    
    def drawWall( self, x, y ) :
        self.updateMap( x, y, 3 )
    
    def updateMap( self, x, y, v ) :
        p = ( y * self.mapw ) + x
        if self.mapdata[ p ] != 1 and self.mapdata[ p ] != 2 :
            if v == 0 :
                self.mapdata[ p ] = -1
            else :
                self.mapdata[ p ] = v


'''
game = AStarPathFinding()
game.initMap( 11, 8 )
game.drawWall( 0, 4 )
game.drawWall( 1, 5 )
game.drawWall( 2, 5 )
game.drawWall( 2, 4 )
game.drawWall( 3, 5 )
game.drawWall( 3, 4 )
game.drawWall( 3, 3 )
game.drawWall( 3, 2 )
game.findPath()
game.drawMap()
'''