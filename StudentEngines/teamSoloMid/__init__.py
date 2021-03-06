"""
Student Quoridor Engine Module        
Author: Adam Oest (amo9149@rit.edu)
    
This is where you will be able to define all the
methods that control the flow of execution of the game
"""
from Model.interface import PlayerMove
from Engine.security import GameException
from .engineData import EngineData 
from .myQueue import *
from .myStack import *
from copy import deepcopy
from copy import copy
import random


"""
Quoridor II: Student Engine
Author: Adam Oest (amo9149@rit.edu)

Implement the methods in the order you see them

Author: YOUR NAME HERE (your email address)
Author: YOUR NAME HERE (your email address)
Author: YOUR NAME HERE (your email address)
"""

def init(logger, config, studentModel):
    """
        Part 1 - 4
    
        The system calls this function once at the beginning of the game.
        The student engine uses this function to initialize its data
        structures to the initial game state.

        Parameters
            logger: a reference to the logger object. The player model uses
                logger.write(msg) and logger.error(msg) to log diagnostic
                information.
                
            config: a Python 'dict' structure that has mapped all the
                parameter names to their values, as specified in the
                config.cfg file.
        
            studentModel: reference to a StudentEngineModel object. See
                the documentation for that class in the file
                Model/interface.py. This engine calls the methods in
                that object.
        returns:
            a data structure that stores all of the engine's needed data
    """
    
    # Modify the EngineData class in engineData.py as needed, and create
    # additional files/classes for your board data
    engineData = EngineData(logger, config, studentModel)
    
    return engineData

def last_move(engineData, playerMove):
    """
        Parts 1 and 2 only; in parts 3 and 4, this engine will be controlling
        the players.
        
        The system calls this function after a player makes a valid move in
        the game. The student engine updates its data structure with the
        information about the move.

        Parameters
            engineData: this engine's data, originally built by this
                        module in init()
        
            playerMove: the instance of PlayerMove that describes the
                        move just made
        
        returns:
            this player module's updated (engineData) data structure
    """
    
    # Update your engineData board state here, incorporating the last move.
    
    #Assuming all moves are walls for part 1
    if not playerMove.move:
        if playerMove.r1 == playerMove.r2:
            if playerMove.r1 != 9:
                engineData.board[playerMove.r1][playerMove.c1].top = False
                engineData.board[playerMove.r2][playerMove.c2 - 1].top = False
            if playerMove.r1 != 0:
                engineData.board[playerMove.r1 - 1][playerMove.c1].down = False
                engineData.board[playerMove.r2 - 1][playerMove.c2 - 1].down = False
            engineData.wallsH.append([playerMove.r1,playerMove.c2 - 1])
        else:
            if playerMove.c1 != 9:
                engineData.board[playerMove.r1][playerMove.c1].left = False
                engineData.board[playerMove.r1 + 1][playerMove.c1].left = False
            if playerMove.c1 != 0:
                engineData.board[playerMove.r1][playerMove.c1 - 1].right = False
                engineData.board[playerMove.r1 + 1][playerMove.c1 - 1].right = False
            engineData.wallsV.append([playerMove.r2 - 1,playerMove.c1])
        engineData.players[playerMove.playerId-1].walls -= 1
                
    else:
        engineData.players[playerMove.playerId - 1].pos = [playerMove.r2,playerMove.c2]

    return engineData

def get_neighbors(engineData, r, c):
    """
        Part 1
    
        This function is used only in part 1 mode. The system calls it after
        all PRE_MOVEs have been made. (See the config.cfg file.)

        Parameters
            engineData: the data originally built by this module in init()
            r: row coordinate of starting position for this player's piece
            c: column coordinate of starting position for this player's piece
        
        returns:
            a list of coordinate pairs (a list of lists, e.g. [[0,0], [0,2]],
            not a list of tuples) denoting all the reachable neighboring squares
            from the given coordinate. "Neighboring" means exactly one move
            away.
    """
    
    # Use your engineData object to get a list of neighbors    
    
    neighbors = []
    if engineData.board[r][c].top:
        neighbors.append([r-1,c])
    if engineData.board[r][c].right:
        neighbors.append([r,c+1])
    if engineData.board[r][c].down:
        neighbors.append([r+1,c])
    if engineData.board[r][c].left:
        neighbors.append([r,c-1])
    
    return neighbors

def get_shortest_path(engineData, r1, c1, destinations):
    """
        Part 1
    
        This function is only called in part 1 mode. The engine calls it when
        a shortest path is requested by the user via the graphical interface.

        Parameters
            engineData: the data originally built by this module in init()
            r1: row coordinate of starting position
            c1: column coordinate of starting position
            r2: row coordinate of destination position
            c2: column coordinate of destination position
        
        returns:
            a list of coordinates that form the shortest path from the starting
            position to the destination, inclusive. The format is an ordered
            list of coordinate pairs (a list of lists, e.g.,
            [[0,0], [0,1], [1,1]], not a list of tuples).
            If there is no path, an empty list, [], should be returned.
    """
    
    # Use your engineData object to find a shortest path using breadth-first
    # search (BFS).
    # You will probably find the get_neighbors function helpful.
    
    # Replace the line below with your computations.
    source = (r1,c1)
    #destination = engineData.board[r2][c2]
    # 'prime' the dispenser with the source 
    dispenser = Queue()
    enqueue(source, dispenser)

    # construct the predecessors data structure
    predecessors = {}
    predecessors[source] = None

    # loop until either the destination is found or the dispenser 
    # is empty (no path)
    while not emptyQueue(dispenser):
        current = front(dispenser)
        #current = (currentSquare.r,currentSquare.c)
        dequeue(dispenser)
        if current in destinations:
            break
        # loop over all neighbors of current
        neighbors = []
        neighborCoords = get_neighbors(engineData,current[0],current[1])
        for x in neighborCoords:
            neighbors.append((engineData.board[x[0]][x[1]].r,engineData.board[x[0]][x[1]].c))
        
        for neighbor in neighbors:
            # process unvisited neighbors
            if neighbor not in predecessors:
                predecessors[neighbor] = current
                enqueue(neighbor, dispenser)

    # construct the path using a stack and traversing from the destination
    # node back to the source node using Node's previous
    stack = Stack()
    destination = [i for i in destinations if i in predecessors]
    if destination != []:
        tmp = destination[0]
        while tmp != source:
            push(tmp, stack)
            tmp = predecessors[tmp]
        push(source, stack)
        
    pathSquares = []
    while not emptyStack(stack):
        pathSquares.append(top(stack)) 
        pop(stack)   
    
    path = []
    for jump in pathSquares:
        path.append([jump[0],jump[1]])

    return path
        

def validate_move(engineData, playerMove):
    """
        Check to see if the given move is valid for the given game state.
        
        In part 2 this function is called by the system.
        In parts 3 and 4 the function is called internally by the player
        engine itself from next_move().

        Parameters
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerMove: the instance of PlayerMove that describes the
                        move just made
        Returns: a bool representing whether or not the given move is valid
    """
    if not playerMove.move:
        if engineData.players[playerMove.playerId - 1].walls <= 0:
            print("Move: "+str(playerMove))
            engineData.logger.error("No walls remaining for player " + str(playerMove.playerId))
            return False
        if ((playerMove.r1 - playerMove.r2 == 0) and (playerMove.c2 - playerMove.c1 != 2)) or ((playerMove.c1 - playerMove.c2 == 0) and (playerMove.r2 - playerMove.r1 != 2)):
            engineData.logger.error("["+str(playerMove.r1)+","+str(playerMove.c1)+"]->["+str(playerMove.r2)+","+str(playerMove.c2)+"] is not a valid wall placement")
            return False
        if playerMove.r1 < 0 or playerMove.r2 <= 0 or playerMove.r1 >= 9 or playerMove.r2 > 9 or playerMove.c1 < 0 or playerMove.c2 <= 0 or playerMove.c1 >= 9 or playerMove.c2 > 9:
            engineData.logger.error("Wall ["+str(playerMove.r1)+","+str(playerMove.c1)+"]->["+str(playerMove.r2)+","+str(playerMove.c2)+"] is outside the board")
            return False
        if playerMove.r1 == playerMove.r2:
            if [playerMove.r1,playerMove.c2 - 1] in engineData.wallsH or [playerMove.r1,playerMove.c2 - 1] in engineData.wallsV:
                engineData.logger.error("Wall intersects another wall")
                return False
            else:
                if [playerMove.r1,playerMove.c2] in engineData.wallsH or [playerMove.r1,playerMove.c1] in engineData.wallsH:
                    engineData.logger.error("Wall intersects another wall")
                    return False
        if playerMove.c1 == playerMove.c2:
            if [playerMove.r2 - 1,playerMove.c1] in engineData.wallsH or [playerMove.r2 - 1,playerMove.c1] in engineData.wallsV:
                engineData.logger.error("Wall intersects another wall")
                return False
            else:
                if [playerMove.r1,playerMove.c1] in engineData.wallsV or [playerMove.r2,playerMove.c2] in engineData.wallsV:
                    engineData.logger.error("Wall intersects another wall")
                    return False
        engineDataWithWall = copy(engineData)
        engineDataWithWall.players = deepcopy(engineData.players)
        for x in range(0,len(engineData.board)):
            engineDataWithWall.board[x] = deepcopy(engineData.board[x])
        last_move(engineDataWithWall,playerMove)
        for player in engineData.players:
            if get_shortest_path(engineDataWithWall,player.pos[0],player.pos[1],player.destinations) == []:
                engineData.logger.error("Wall blocks player path")
                return False
        
    else:
        if playerMove.r1 != engineData.players[playerMove.playerId-1].pos[0] or playerMove.c1 != engineData.players[playerMove.playerId-1].pos[1]:
            engineData.logger.error("Initial position is not correct")
            return False
        if playerMove.r2 < 0 or playerMove.r2 >= 9 or playerMove.c2 < 0 or playerMove.c2 >= 9:
            engineData.logger.error("Player cannot move outside board")
            return False
        neighbors = get_neighbors(engineData,playerMove.r1,playerMove.c1)
        if [playerMove.r2,playerMove.c2] not in neighbors:
            validMoves = deepcopy(neighbors)
            for otherPlayer in engineData.players:
                if id == playerMove.playerId:
                    continue
                else:
                    if otherPlayer.pos in neighbors:
                        validMoves.remove(otherPlayer.pos)
                        newNeighbors = get_neighbors(engineData,otherPlayer.pos[0],otherPlayer.pos[1])
                        newNeighbors.remove([playerMove.r1,playerMove.c1])
                        for otherPlayerJump in engineData.players:
                            if otherPlayerJump.pos in newNeighbors:
                                newNeighbors.remove(otherPlayerJump.pos)
                        if [playerMove.r1-2,playerMove.c1] in newNeighbors:
                            validMoves.append([playerMove.r1-2,playerMove.c1])
                        elif [playerMove.r1,playerMove.c1+2] in newNeighbors:
                            validMoves.append([playerMove.r1,playerMove.c1+2])
                        elif [playerMove.r1+2,playerMove.c1] in newNeighbors:
                            validMoves.append([playerMove.r1+2,playerMove.c1])
                        elif [playerMove.r1,playerMove.c1-2] in newNeighbors:
                            validMoves.append([playerMove.r1,playerMove.c1-2])
                        else:
                            for neighbor in newNeighbors:
                                validMoves.append(neighbor)
            if [playerMove.r2,playerMove.c2] not in validMoves:
                if (validMoves == []) and ([playerMove.r2,playerMove.c2] == [playerMove.r1,playerMove.c1]) and (engineData.players[playerMove.playerId - 1].walls == 0):
                    return True
                else:
                    engineData.logger.error("["+str(playerMove.r2)+","+str(playerMove.c2)+"] does not connect to ["+str(playerMove.r1)+","+str(playerMove.c1)+"]")
                    return False
        for player in engineData.players:
            if (playerMove.r2 == player.pos[0]) and (playerMove.c2 == player.pos[1]):
                engineData.logger.error("A player is already in that spot")
                return False
  
    return True

def initialize_player(engineData, playerNum):
    """
        Part 3 and 4
        The system calls this function when it wants the student engine
        to initialize a specific player module via its init() function.
        
        Reference file for init(): StudentPlayers/RenameYourPlayer/__init__.py
        
        Parameters
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerNum: the number of the player (in [0 .. n-1] for n players)

        returns: the engine data, modified
    """
    
    # Step 1
    # Fetch the reference to the model from your engineData.
    numWallsDict = engineData.config['NUM_WALLS']
    engineData.model.setPlayerData(playerNum, engineData.model.getPlayerModule(playerNum).init(engineData.logger, playerNum, numWallsDict[len(engineData.players)], engineData.model.playerHomes))
    
    
    # Step 2
    # Get the player module from the model using model.getPlayerModule.
    
    # Step 3
    # Call the chosen player module's init function with the appropriate data.
    #
    # Tips:
    # logger was already given to you in your own init method
    # numWalls depends on the number of players and is accessible through the
    #     NUM_WALLS key in the config dictionary
    # playerHomes may only include home locations for active players in the game
    #     and it must be a tuple, not a list.
    
    # Step 4
    # Save the player data using StudentEngineModel's setPlayerData method.
    # The StudentEngineModel object should have been saved when your init
    # function was called.
    
    return engineData

def next_move(engineData):
    """
        Part 3 and 4
        
        Ask the module of the player whose turn it is for its next move
        (player's move function.)
        Check the move for validity. If invalid, exit_due_to_error is called.
        If valid, all player modules are notified of the move via last_move.

        Process the next move, sending it to the engine
                      and notifying other players
        
                      
        Parameters
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerNum: the number of the player (in [0 .. n-1] for n players)

        returns: the engine data, modified by the actions described above
    """
    
    # Step 1
    # Get playerMove object from the current player using player module's move
    # function.
    # (At this point you do not need to record any player's playerData.)
    if len(engineData.preMoves) > 0:
        engineData.logger.write('processing PRE_MOVE')
        playerMove = engineData.preMoves.pop(0)
    else:
        # Get move from player  
        engineData.logger.write('processing player move')
        playerModule = engineData.model.getPlayerModule(engineData.currentPlayer)
        playerMove = playerModule.move(engineData.model.getPlayerData(engineData.currentPlayer)) 
    
    # Step 2
    # Validate the move.

    # Step 3
    # If it is invalid:
    #     Call exit_due_to_error (contained in this file).
    # else:
    #     Update your engineData board state.
    #     Call the makeMove function in your model object.
    #         The StudentEngineModel object should have been saved when your
    #         init function was called.
    #
    #     Notify all players of this move by doing the following
    #         for each player:
    #             Call player.last_move(playerData, playerMove).
    #             Save the player's returned playerData using
    #                                           model.setPlayerData
    #
    #     [ !!! Obtain playerData using model.getPlayerData ??? ]
    
    if playerMove.playerId != engineData.currentPlayer:
        exit_due_to_error("Invalid player id, exiting...")
    
    if validate_move(engineData, playerMove) == True:
        last_move(engineData, playerMove)
        engineData.model.makeMove(playerMove)
        for playerNum in range(1,len(engineData.model.playerHomes)+1):
            playerModule = engineData.model.getPlayerModule(playerNum)
            playerData = playerModule.last_move(engineData.model.getPlayerData(playerNum), playerMove)
            engineData.model.setPlayerData(playerNum, playerData)
    else:
        if len(engineData.preMoves) > 0:
            print("exiting...")
            exit_due_to_error("Invalid Pre-Move, exiting...")
        else:
            print("exiting...")
            exit_due_to_error("Player "+str(engineData.currentPlayer)+" made an invalid move, exiting...")
            
    if engineData.currentPlayer == len(engineData.model.playerHomes):
        engineData.currentPlayer = 1
    else:
        engineData.currentPlayer += 1
    
    # Safety tip: rather than passing the playerMove object, pass a copy of it
    # by calling playerMove.getCopy() to ensure that there is no harm done if
    # the original object gets modified.

    # Development tip: Disable AUTO_PLAY in config.cfg while developing this.

    return engineData

def exit_due_to_error(message):
    """
        Part 3 and 4: Exit the program 
                      after a player makes an illegal move
        This is an INTERNAL function called from next_move above, when
        that function has determined that the move chosen by the player
        violates the rules of the game.

        Parameters
            message: the error message to be displayed in the user interface
    """
    
    # NOTE: You do not need to edit the code in this function at all!
    
    raise GameException(message)

def generate_board(engineData):
    """    
        Part 4: Generate a symmetric board configuration
        
        engineData: your engine state
        
        moveExecFunction: call with moves
        
        returns: your engine state
    """
    # Hint: disable AUTO_PLAY while developing this
        
    
    # numWalls equals the value of the STUDENT_ENGINE_WALLS config parameter
    # this controls how many PlayerMoves you generate in this function
    # note that this number should always be even due to the asymmetry of the
    # game board
    numWalls = engineData.config['STUDENT_ENGINE_WALLS']
    
    isGood = False
    
    while not isGood:
        isGood = True
        walls = []
        allWalls = []
        noCollideCenterH = []
        noCollideCenterV = []
        for x in range(0,numWalls):
            startRow = random.randrange(1,4)
            startCol = random.randrange(0,4)
            walls.append([startRow,startCol,startRow,startCol+2])
            startCol += 2
            if startCol+2 > 9:
                startCol = 1
                startRow += 1
        for wall in walls:
            allWalls.append(wall)
            allWalls.append([9-wall[2],9-wall[3],9-wall[0],9-wall[1]])
            if len(engineData.players) == 4:
                if wall[0] == wall[2]:
                    allWalls.append([wall[1],9-wall[0],wall[3],9-wall[2]])
                    allWalls.append([9-wall[3],wall[2],9-wall[1],wall[0]])
                else:
                    allWalls.append([wall[3],9-wall[2],wall[1],9-wall[0]])
                    allWalls.append([9-wall[1],wall[0],9-wall[3],wall[2]])
        for wall in allWalls:
            if wall[0] == wall[2]:
                noCollideCenterH.append([wall[0],wall[1]+1])
            else:
                noCollideCenterV.append([wall[0]+1,wall[1]])
        for wall in allWalls:
            if wall[0] == wall[2]:
                if [wall[0],wall[3] - 1] in noCollideCenterH or [wall[0],wall[3] - 1] in noCollideCenterV:
                    isGood = False
                    break
                else:
                    if [wall[0],wall[3]] in noCollideCenterH or [wall[0],wall[1]] in noCollideCenterH:
                        isGood = False
                        break
            if wall[1] == wall[3]:
                if [wall[2] - 1,wall[1]] in noCollideCenterH or [wall[2] - 1,wall[1]] in noCollideCenterV:
                    isGood = False
                    break
                else:
                    if [wall[0],wall[1]] in noCollideCenterV or [wall[2],wall[3]] in noCollideCenterV:
                        isGood = False
                        break
                
    playerMoves = []
    currentPlayer = 1    
    for wall in allWalls:
        print(wall)
        playerMoves.append(PlayerMove(currentPlayer, False, wall[0], wall[1], wall[2], wall[3]))
        if currentPlayer == len(engineData.players):
            currentPlayer = 1
        else:
            currentPlayer += 1
    
    for move in playerMoves: 
        last_move(engineData, move)
        engineData.model.makeMove(move)
        for playerNum in range(1,len(engineData.model.playerHomes)+1):
            playerModule = engineData.model.getPlayerModule(playerNum)
            playerData = playerModule.last_move(engineData.model.getPlayerData(playerNum), move)
            engineData.model.setPlayerData(playerNum, playerData)
    
    # Generate PlayerMoves to be made
    
    # For each move:
    #     call model.makeMove(playerMove)
    #     notify players of this move
    
    return engineData
    