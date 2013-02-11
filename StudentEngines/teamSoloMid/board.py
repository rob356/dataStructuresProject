"""
A class for a square on the quoridor game board

Author: Robert Holt (rgh7614@rit.edu)
"""

class BoardSquare:
    """
    The BoardSquare Class. Represents one quoridor game board square.
    
    player: The ID of a player in this square. 0 for no player.
    
    top,left,right,down: These are True if there is a valid path in that
                         direction. IT is changed to False if the path
                         is blocked by a wall, or the edge of the board.
    r: The row the square is in.
    
    c: The column the square is in.
    """
    __slots__=('top','left','right','down','r','c')
    
    def __init__(self,r,c):
        """
        Constructs and returns an instance of BoardSquare
        
        Takes the square's row(r) and column(c) as input
        """
        self.top=True
        self.left=True
        self.right=True
        self.down=True
        self.r = r
        self.c = c
    
    def __str__(self):
        """
        Returns the string representation of the square.
        Really just prints out every variable.
        """
        return "| Top="+str(self.top)+",Left="+str(self.left)+",Right="+str(self.right)+",Down="+str(self.down)+",r="+str(self.r)+",c="+str(self.c)+" "
    
class PlayerBoard:
    __slots__=('pos','walls','destinations')
    
    def __init__(self,pos,walls):
        self.pos = pos
        self.walls = walls
        print(str(walls))