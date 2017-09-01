import sys
import random
from enum import Enum

'''
 how to do enums in python
 no return types

'''

class Strategy(Enum):
    random=0
    stupid=1
    greedy=2
    max_point=3
    look_ahead=4
    learning=5


strategy_assignment={'w':Strategy.greedy, 'b':Strategy.greedy}

moving_taxonomy = {"kn":[[2,1],[1,2],[-2,-1],[-2,1],[-1,-2],[-1,2],[2,-1]],
                   "bs":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7]],
                   "rk":[[0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
                   "pw":[[1,0],[-1,0]],
                   "qn":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7],
                        [0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
                   "kk":[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                   }

eating_taxonomy = {
    "kn":[[2,1],[1,2],[-2,-1],[-2,1],[-1,-2],[-1,2],[2,-1]],
    "bs":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7]],
    "rk":[[0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
    "pw":[[1,1],[1,-1],[-1,1],[-1,-1]],
    "qn":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7],
          [0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
    "kk":[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                   }

value_taxonomy={
    "kn":3,
    "bs":3,
    "rk":5,
    "pw":1,
    "qn":10,
    "kk":20
}


can_jump=set(["kn"])
polarity={"pw":{"b":1, "w":-1}}

debug=False


class piece:

    def __init__(self,id,loc):
        self.id=id
        self.position=loc
        self.type=id[1:3]
        self.color=id[0]
        self.active=True

class cell:
    def __init__(self):
        self.piece=None

    def to_text(self):
        if self.piece==None:
            return "      ."
        else:
            return self.piece.id+"  ."

class game:
    def __init__(self):
        self.board=[[cell() for i in range(8)] for j in range(8)]

    def printBoard(self):
        for row in self.board:
            for this_cell in row:
                print(this_cell.to_text(),end=" ")
            print()
        print()

    def add_piece(self,apiece,coords):
        coords
        if self.board[coords[0]][coords[1]].piece!=None:
            return
        self.board[coords[0]][coords[1]].piece=apiece
        apiece.position=coords

    def generate_path(self,x,y):
        #print "BEGIN", x, y
        i=0
        j=0
        result=[]
        if x[0]==y[0]:
            i=0
        if x[0]>y[0]:
            i=-1
        if x[0]<y[0]:
            i=1
        if x[1]==y[1]:
            j=0
        if x[1]>y[1]:
            j=-1
        if x[1]<y[1]:
            j=1
        steps=0
        temp=x
        #print i, j
        while True:
            temp=(temp[0]+i,temp[1]+j)
            if debug:
                print("       source", x,  "  target ", y, temp)
            result.append(temp)
            steps+=1
            if temp==y or steps>=10:
                return result
            #print result
        return result

    def is_in_board(self,i):
        if i[0]>=0 and i[0]<=7 and i[1]>=0 and i[1]<=7:
            return True
        return False
    

    #NEED TO DEBUG THIS
    def move_at_random_to_empty(self,color_set):
        possible_moves=[]
        for apiece in color_set:
            original_position=apiece.position
            for offset in moving_taxonomy[apiece.type]:
                is_blocked=False
                if apiece.type in can_jump:
                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                else:
                    if debug==True:
                        print(apiece.id)

                    if apiece.type in polarity and offset[0]*polarity[apiece.type][apiece.color] < 0:
                        continue

                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                    for i in self.generate_path(original_position,new_coordinates):
                        if self.is_in_board(i)==False:
                            is_blocked=True
                            break
                        elif  i!= new_coordinates and  self.board[i[0]][i[1]].piece!=None:
                            is_blocked = True
                            break
                if is_blocked==False and self.is_in_board(new_coordinates)==True and self.board[new_coordinates[0]][new_coordinates[1]].piece == None:
                    #print apiece.id, new_coordinates, original_position
                    possible_moves.append((apiece,new_coordinates,original_position))
        if len(possible_moves)>0:
            chosen_move=possible_moves[random.randint(0,len(possible_moves)-1)]
            best_move=move(chosen_move)
            return best_move









        
    def execute_move(self,chosen_move,color_set,opponent_set):                
            new_coordinates=chosen_move.target
            apiece=chosen_move.piece
            original_position=chosen_move.source
            apiece.position=new_coordinates
            if self.board[new_coordinates[0]][new_coordinates[1]].piece != None and self.board[new_coordinates[0]][new_coordinates[1]].piece in opponent_set:
                opponent_set.remove(self.board[new_coordinates[0]][new_coordinates[1]].piece)
            self.board[new_coordinates[0]][new_coordinates[1]].piece=apiece
            self.board[original_position[0]][original_position[1]].piece=None
            print(self.board[new_coordinates[0]][new_coordinates[1]].piece.id, original_position, "->", new_coordinates)



    def simulate_move(self,chosen_move,color_set,opponent_set):                
        new_active=set()
        new_passive=set()
        for a_piece in color_set:
            new_active.add( piece(a_piece.id,a_piece.position))
        for a_piece in color_set:
            if a_piece.id == chosen_move.piece.id:
                a_piece.position=chosen_move.target
                break
        for a_piece in opponent_set:
            if a_piece.position != chosen_move.target:
                new_passive.add(piece(a_piece.id, a_piece.position))
        return new_active, new_passive




    def calculate_moves(self,color_set,opponent_set,strategy_type):
        best_moves=[]
        if strategy_type is Strategy.greedy:
            capturing_moves=self.move_to_capture(color_set,opponent_set)
            if capturing_moves != None:
                best_moves+=[capturing_moves]
            if len(best_moves) == 0:
                best_moves+=[self.move_at_random_to_empty(color_set)]
            return best_moves
        elif strategy_type is Strategy.stupid:
            best_moves.append(self.move_at_random_to_empty(color_set))
            return best_moves
        else:
            capturing_moves=self.move_to_capture(color_set,opponent_set)
            if capturing_moves != None:
                best_moves+=[capturing_moves]
            if len(best_moves) == 0:
                best_moves+=[self.move_at_random_to_empty(color_set)]
            return best_moves


    def calculate_all_moves(self,color_set,opponent_set):
        possible_moves=[]
        lay_of_the_land={}
        for arow in range(len(self.board)):
            for acol in range(len(self.board[arow])):
                acel=self.board[arow][acol]
                if acel.piece is not None:
                    lay_of_the_land[(arow,acol)]=acel.piece.id
                    if debug:
                        print((arow,acol),acel.piece.id)
        #print(lay_of_the_land)
        for apiece in color_set:
            my_color=apiece.color
            if debug:
                print(apiece.id)

            original_position=apiece.position
            for offset in eating_taxonomy[apiece.type]:
                is_blocked=False
                if apiece.type in can_jump:
                    ## We are assuming that can_jump and polarity do not overlap
                    new_coordinates=(apiece.position[0]+offset[0],apiece.position[1]+offset[1])
                else:
                    if apiece.type in polarity and offset[0]*polarity[apiece.type][apiece.color] < 0:
                        continue
                    new_coordinates=(apiece.position[0]+offset[0],apiece.position[1]+offset[1])
                    for i in self.generate_path(original_position,new_coordinates):
                        if self.is_in_board(i) is False:
                            is_blocked=True
                            break
                        elif i!= new_coordinates and (i[0],i[1]) in lay_of_the_land:
                            is_blocked=True
                            break
                if is_blocked == False and  self.is_in_board(new_coordinates)==True:
                    if new_coordinates in lay_of_the_land:
                        if lay_of_the_land[new_coordinates][0]!=my_color:
                            possible_moves.append((apiece,new_coordinates,original_position))
        for apiece in color_set:
            my_color=apiece.color
            if debug:
                print(apiece.id)
            original_position=apiece.position
            for offset in moving_taxonomy[apiece.type]:
                is_blocked=False
                if apiece.type in can_jump:
                    new_coordinates=(apiece.position[0]+offset[0],apiece.position[1]+offset[1])
                else:
                    if apiece.type in polarity and offset[0]*polarity[apiece.type][apiece.color] < 0:
                        continue
                    new_coordinates=(apiece.position[0]+offset[0],apiece.position[1]+offset[1])
                    for i in self.generate_path(original_position,new_coordinates):
                        if self.is_in_board(i) is False:
                            is_blocked=True
                            break
                        elif i!= new_coordinates and (i[0],i[1]) in lay_of_the_land:
                            if debug:
                                print("blocked by",lay_of_the_land[(i[0],i[1])])
                            is_blocked=True
                            break
                    if debug:
                        print(is_blocked)
                if is_blocked == False and  self.is_in_board(new_coordinates)==True:
                    if not (new_coordinates in lay_of_the_land):
                        possible_moves.append((apiece,new_coordinates,original_position))

        return possible_moves

            

    def move_to_capture(self,color_set,opponent_set):
        possible_moves=[]
        for apiece in color_set:
            my_color=apiece.color
            original_position=apiece.position
            for offset in eating_taxonomy[apiece.type]:
                is_blocked=False
                if apiece.type in can_jump:
                    ## We are assuming that can_jump and polarity do not overlap
                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                else:
                    if apiece.type in polarity and offset[0]*polarity[apiece.type][apiece.color] < 0:
                        continue
                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                    for i in self.generate_path(original_position,new_coordinates):
                        if self.is_in_board(i)==False:
                            is_blocked=True
                            break
                        elif i!= new_coordinates and self.board[i[0]][i[1]].piece!=None:
                            is_blocked=True
                            break
                if is_blocked == False and  self.is_in_board(new_coordinates)==True and self.board[new_coordinates[0]][new_coordinates[1]].piece != None  and self.board[new_coordinates[0]][new_coordinates[1]].piece.color != my_color:
                    #print apiece.id, new_coordinates, original_position
                    possible_moves.append((apiece,new_coordinates,original_position))
        if len(possible_moves)>0:
            chosen_move=possible_moves[random.randint(0,len(possible_moves)-1)]
            best_move=move(chosen_move)
            return best_move
        else:
            return None

    def score_pieces(self,piece_set,needed_condition):
        this_score=0
        found_condition=False
        for piece in piece_set:
            if piece.type in value_taxonomy:
                this_score+=value_taxonomy[piece.type]
            if piece.type == needed_condition:
                found_condition=True
        if found_condition== True:
            return this_score
        else:
            return 0


random.seed()
this_game = game()
whites=set()
blacks=set()
playing_order=["w","b"]
playing_set={"w":whites, "b":blacks}

original_layout=(("bkn1",[0,1]),("bkn2",[0,6]),("bbs1",[0,2]),("bbs2",[0,5]),("brk1",[0,0]),("brk2",[0,7]),("bpw1",[1,0]),("bpw2",[1,7]),("bpw3",[1,1]),("bpw4",[1,6]),("bpw5",[1,2]),("bpw6",[1,5]),("bpw7",[1,3]),("bpw8",[1,4]),
                 ("bkk1",[0,3]),("bqn1",[0,4]),
                 ("wkn1",[7,1]),("wkn2",[7,6]),("wbs1",[7,2]),("wbs2",[7,5]),("wrk1",[7,0]),("wrk2",[7,7]),("wpw1",[6,0]),("wpw2",[6,7]),("wpw3",[6,1]),("wpw4",[6,6]),("wpw5",[6,2]),("wpw6",[6,5]),("wpw7",[6,3]),("wpw8",[6,4]),
                 ("wkk1",[7,3]),("wqn1",[7,4])
                 )
##  Set up the game  ###
for xpiece in original_layout:
    team=playing_set[xpiece[0][0]]
    apiece=piece(xpiece[0],None)
    team.add(apiece)
    this_game.add_piece(apiece,xpiece[1])


class move:    
    def __init__(self,triplet):
        self.piece=triplet[0]
        self.target=triplet[1]
        self.source=triplet[2]
        self.score=0

    def to_string(self):
        return self.piece.id +" " + str(self.source) + " -> " + str(self.target)


### Start the game  ####
movement_number=0
this_game.printBoard()


while len(whites)>0 and len(blacks)>0:
    active_color=playing_order[movement_number%len(playing_order)]
    passive_color=playing_order[(movement_number+1)%len(playing_order)]
    print("Turn of", active_color,  movement_number, len(whites), len(blacks))
    active_set=playing_set[active_color]
    passive_set=playing_set[passive_color]

    ''' 
    Modify these 3 lines for a search based approach:
    '''


    #all_moves=this_game.calculate_moves(active_set,passive_set,strategy_assignment[active_color])
    #best_move=all_moves[0]
    #this_game.execute_move(best_move,active_set,passive_set)

    '''
    Search
    '''
    all_moves=this_game.calculate_all_moves(active_set,passive_set)
    #You have simulate
    #scored_moves=this_game.score_moves(all_moves,active_set,passive_set)
    best_move=move(all_moves[0])
    this_game.execute_move(best_move,active_set,passive_set)

    
    #best_move=this_game.rank_by_score(all_moves,passive_set)[0][0]

    #this_game.execute_move(best_move,active_set,passive_set)

    active_score=this_game.score_pieces(active_set,"kk")
    passive_score=this_game.score_pieces(passive_set,"kk")
    print("Scores:", active_color+str(active_score), passive_color+str(passive_score))
    this_game.printBoard()    
    if passive_score == 0:
        print(passive_color, "Loses Game... Game over!!!")
        break
    movement_number+=1

