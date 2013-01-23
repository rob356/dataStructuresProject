"""
Quoridor II: Student Computer Engine

A sample class you may use to hold your state data
Author: Adam Oest (amo9149@rit.edu)

Author: Robert Holt (rgh7614@rit.edu)
"""

from .board import BoardSquare,PlayerBoard

class EngineData(object):
    """The EngineData Class
    logger: a reference to the logger object. The player model uses
            logger.write(msg) and logger.error(msg) to log diagnostic
            information.
                
    config: a Python 'dict' structure that has mapped all the
            parameter names to their values, as specified in the
            config.cfg file.
        
    model: reference to a StudentEngineModel object. See
           the documentation for that class in the file
           Model/interface.py. This engine calls the methods in
           that object.
           
    board: The game board represented as a 2D array
    """
    
    # Add other slots as needed
    __slots__ = ('logger', 'config', 'model', 'board', 'wallsH', 'wallsV', 'players', 'preMoves', 'currentPlayer')
    
    def __init__(self, logger, config, model):
        """
            Constructs and returns an instance of EngineData
            
            Takes the logger, config, and model as input and
            constructs the game board.
        """
        
        self.logger = logger
        self.config = config
        self.model = model
        self.wallsH = []
        self.wallsV = []
        self.preMoves = config['PRE_MOVE']
        self.currentPlayer = 1
        
        # initialize any other slots you require here
        
        maxR = 9
        maxC = 9
        boardData = []
        
        for r in range(0,maxR):
            rowData = []
            for c in range(0,maxC):
                newSquare = BoardSquare(r,c)
                if r == 0:
                    newSquare.top = False
                if c == 0:
                    newSquare.left = False
                if r == maxR - 1:
                    newSquare.down = False
                if c == maxC - 1:
                    newSquare.right = False
                rowData.append(newSquare)
            boardData.append(rowData)
            
        self.players = []
        wallsDict = config['NUM_WALLS'] #FIX ME LATER
        for home in model.playerHomes:
            self.players.append(PlayerBoard(home,wallsDict[len(model.playerHomes)]))
            
        self.board = boardData
        
    def __str__(self):
        """
        __str__: EngineData -> string
        Returns a string representation of the EngineData object.
            self - the EngineData object
        """
        boardText = ""
        for r in self.board:
            rowText = "Row: "
            for c in r:
                rowText = rowText + str(c)
            boardText = "\n" + boardText
        
        result = "EngineData= " \
                    + "logger: " + str(self.logger) \
                    + ", config: " + str(self.config) \
                    + ", model: " + str(self.model) \
                    + ", Board: " + boardText
                
        # add any more string concatenation for your other slots here
                
        return result