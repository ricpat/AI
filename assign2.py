# 2014B1A70213P Richa Patel
import turtle
import sys
import timeit

t = turtle
screen = t.Screen()
tdraw = t.Turtle()

X = 0
Y = 200
STEP_SIZE = 100
GRID_SIZE = 4

S = [[0] * 4 for _ in range(4)]
H_TURN = [True]  # True to show its humans turn to play/action
GAME_ON = [False]
NEW = [True]
utility_value = [0]
isAlphaBeta = [0]  # value is 1 if alpha beta pruning is selected
results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # will store the results
game_counts = [0,0,0,0] # no of games, no of times M wins, times H wins, total time


def firstscreen():
    tdraw.reset()
    tdraw.penup()
    tdraw.goto(-100, 0)
    tdraw.pendown()
    tdraw.write("Click to play!!", font=("Arial", 60, "normal"))
    tdraw.penup()
    tdraw.goto(-150, -50)
    tdraw.pendown()
    tdraw.write("Expand the screen for better view", font=("Arial", 30, "normal"))
    tdraw.penup()
    tdraw.goto(0, 0)


def drawGrid():
    tdraw.speed(8)
    tdraw.pensize(2)
    tdraw.penup()
    tdraw.goto(X, Y)
    tdraw.pendown()
    tdraw.forward(STEP_SIZE * GRID_SIZE)
    tdraw.right(90)
    tdraw.forward(STEP_SIZE * GRID_SIZE)
    tdraw.right(90)
    tdraw.forward(STEP_SIZE * GRID_SIZE)
    tdraw.right(90)
    tdraw.forward(STEP_SIZE * GRID_SIZE)
    drawColumns()
    drawRows()
    tdraw.goto(0, 220)
    tdraw.pensize(3)
    tdraw.color('red')
    tdraw.pendown()
    tdraw.goto(400, 220)
    tdraw.penup()
    tdraw.color('black')
    tdraw.goto(0,0)


def drawColumns():
    for i in range(2):
        tdraw.right(90)
        tdraw.forward(STEP_SIZE)
        tdraw.right(90)
        tdraw.forward(STEP_SIZE * GRID_SIZE)
        tdraw.left(90)
        tdraw.forward(STEP_SIZE)
        tdraw.left(90)
        tdraw.forward(STEP_SIZE * GRID_SIZE)


def drawRows():
    tdraw.left(180)
    for i in range(2):
        tdraw.forward(STEP_SIZE)
        tdraw.right(90)
        tdraw.forward(STEP_SIZE * GRID_SIZE)
        tdraw.left(90)
        tdraw.forward(STEP_SIZE)
        tdraw.left(90)
        tdraw.forward(STEP_SIZE * GRID_SIZE)
        tdraw.right(90)
    tdraw.penup()


def drawNewText():
    tdraw.penup()
    tdraw.goto(-100, -300)
    tdraw.pendown()
    tdraw.write("New Game: MiniMax      New Game: AlphaBeta", font=("Arial", 30, "normal"))
    tdraw.penup()
    tdraw.goto(115, -350)
    tdraw.pendown()
    tdraw.write("Press key 'Q' to exit", font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(0, 0)


def stampAt(i, j, h):
    tdraw.shape('circle')
    tdraw.goto(X + (j * STEP_SIZE) + (STEP_SIZE / 2), Y - (i * STEP_SIZE) - (STEP_SIZE / 2))
    tdraw.shapesize(STEP_SIZE / 20.7)
    if h:
        tdraw.color('blue')
    else:
        tdraw.color('green')
    tdraw.stamp()
    tdraw.shape('classic')
    tdraw.shapesize(1)
    tdraw.color('black')


def get_clicked_block(x, y):
    if 0 < x < 100:
        n = 0
        if 100 < y < 200:
            return n + 0
        if 0 < y < 100:
            return n + 1
        if 0 > y > -100:
            return n + 2
        if -100 > y > -200:
            return n + 3
    if 100 < x < 200:
        n = 10
        if 100 < y < 200:
            return n + 0
        if 0 < y < 100:
            return n + 1
        if 0 > y > -100:
            return n + 2
        if -100 > y > -200:
            return n + 3
    if 200 < x < 300:
        n = 20
        if 100 < y < 200:
            return n + 0
        if 0 < y < 100:
            return n + 1
        if 0 > y > -100:
            return n + 2
        if -100 > y > -200:
            return n + 3
    if 300 < x < 400:
        n = 30
        if 100 < y < 200:
            return n + 0
        if 0 < y < 100:
            return n + 1
        if 0 > y > -100:
            return n + 2
        if -100 > y > -200:
            return n + 3
    return -1


def valid_block(i, j):
    if S[i][j] == 0:
        x = S[i - 1][j]
        if i == 0 or (x != 0):
            return True
    return False


def displayMinMaxResults():
    game_counts[3] += results[3]
    results[1] = sys.getsizeof(S)  # memory of each node
    results[4] = results[0]/results[3]
    x = -400
    y = 200
    tdraw.goto(x, y)
    tdraw.pendown()
    tdraw.write("R1 : %d nodes" % results[0], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y - 50)
    tdraw.write("R2 : %d bytes/node" % results[1], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y - 100)
    tdraw.write("R3 : %d nodes (stack)" % results[2], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y - 150)
    tdraw.write("R4 : %d miliseconds" % results[3], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y - 200)
    tdraw.write("R5 : %d nodes/milliseconds" % results[4], font=("Arial", 20, "normal"))
    tdraw.penup()
    display_analysis(x, y-250)


def displayAlphaBetaResults():
    game_counts[3] += results[7]
    if results[0] != 0:
        n1 = results[0]
        n2 = results[5]
        results[6] = ((n1-n2)*100)/n1
        results[8] = n1/n2
    x = -400
    y = 200
    tdraw.goto(x, y)
    tdraw.pendown()
    tdraw.write("R6 : %d nodes" % results[5], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y-50)
    # compared to last minmax game played
    tdraw.write("R7 : %d percentage" % results[6], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y-100)
    tdraw.write("R8 : %d miliseconds" % results[7], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y-150)
    tdraw.write("R9 : %d ratio" % results[7], font=("Arial", 20, "normal"))
    tdraw.penup()
    display_analysis(x,y-200)

def display_analysis(x,y):
    results[9] = game_counts[3]/game_counts[0]
    results[10] = game_counts[1]
    results[11] = (game_counts[1]*100)/game_counts[0]
    tdraw.goto(x, y)
    tdraw.pendown()
    tdraw.write("R10 : %d miliseconds" % results[9], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y-50)
    tdraw.write("R11 : %d wins by M" % results[10], font=("Arial", 20, "normal"))
    tdraw.penup()
    tdraw.goto(x, y-100)
    tdraw.write("R12 : %d percentage wins" % results[11], font=("Arial", 20, "normal"))
    tdraw.penup()

def draw_line(i1, j1, i2, j2):
    tdraw.goto(X + (j1 * STEP_SIZE) + (STEP_SIZE / 2), Y - (i1 * STEP_SIZE) - (STEP_SIZE / 2))
    tdraw.pendown()
    tdraw.goto(X + (j2 * STEP_SIZE) + (STEP_SIZE / 2), Y - (i2 * STEP_SIZE) - (STEP_SIZE / 2))
    tdraw.up()


def draw_win_line():
    if S[3][0] != 0 and S[3][0] == S[2][1] and S[2][1] == S[1][2]:
        draw_line(3, 0, 1, 2)
    if S[2][0] != 0 and S[2][0] == S[1][1] and S[1][1] == S[0][2]:
        draw_line(2, 0, 0, 2)
    if S[2][1] != 0 and S[2][1] == S[1][2] and S[1][2] == S[0][3]:
        draw_line(2, 1, 0, 3)
    if S[3][1] != 0 and S[3][1] == S[2][2] and S[2][2] == S[1][3]:
        draw_line(3, 1, 1, 3)
    if S[1][0] != 0 and S[1][0] == S[2][1] and S[2][1] == S[3][2]:
        draw_line(1, 0, 3, 2)
    if S[0][0] != 0 and S[0][0] == S[1][1] and S[1][1] == S[2][2]:
        draw_line(0, 0, 2, 2)
    if S[1][1] != 0 and S[1][1] == S[2][2] and S[2][2] == S[3][3]:
        draw_line(1, 1, 3, 3)
    if S[0][1] != 0 and S[0][1] == S[1][2] and S[1][2] == S[2][3]:
        draw_line(0, 1, 2, 3)
    # alignments in rows or columns
    for c in range(0, 4):
        if S[0][c] != 0 and S[0][c] == S[1][c] and S[1][c] == S[2][c]:
            draw_line(0, c, 2, c)
        if S[1][c] != 0 and S[1][c] == S[2][c] and S[2][c] == S[3][c]:
            draw_line(1, c, 3, c)
    for r in range(0, 4):
        if S[r][0] != 0 and S[r][0] == S[r][1] and S[r][1] == S[r][2]:
            draw_line(r, 0, r, 2)
        if S[r][1] != 0 and S[r][1] == S[r][2] and S[r][2] == S[r][3]:
            draw_line(r, 1, r, 3)


def display_result():
    i = utility_value[0]
    tdraw.goto(150, 250)
    tdraw.pendown()
    if i == 0:
        tdraw.write("Draw", font=("Arial", 30, "normal"))
        tdraw.penup()
    else:
        if i == -1:
            game_counts[2]+=1
            tdraw.write("you won!", font=("Arial", 30, "normal"))
        else:
            game_counts[1]+=1
            tdraw.write("you lost!", font=("Arial", 30, "normal"))
        tdraw.penup()
        draw_win_line()
    if isAlphaBeta[0] == 0:
        displayMinMaxResults()
    else:
        displayAlphaBetaResults()


def game_over():
    display_result()
    GAME_ON[0] = False  # Game not on
    drawNewText()
    H_TURN[0] = True


def successor_function(s, col, h):
    # count the number of nodes
    if isAlphaBeta[0] == 0:
        results[0] = results[0] + 1
    else:
        results[5] = results[5] + 1
    # make new state for successor
    s_new = [[0] * 4 for _ in range(4)]
    for x in range(0, 4):
        for y in range(0, 4):
            s_new[x][y] = s[x][y]
    for i in range(0, 4):
        if s[i][col] == 0:
            if h:
                s_new[i][col] = -1
            else:
                s_new[i][col] = 1
            # stampAt(i, col, h) #uncomment to see nodes explored
            return s_new
    return s_new


def terminal_test(s):
    # eigth diagonal allignments
    if s[3][0] != 0 and s[3][0] == s[2][1] and s[2][1] == s[1][2]:
        utility_value[0] = s[3][0]
        return True
    if s[2][0] != 0 and s[2][0] == s[1][1] and s[1][1] == s[0][2]:
        utility_value[0] = s[2][0]
        return True
    if s[2][1] != 0 and s[2][1] == s[1][2] and s[1][2] == s[0][3]:
        utility_value[0] = s[2][1]
        return True
    if s[3][1] != 0 and s[3][1] == s[2][2] and s[2][2] == s[1][3]:
        utility_value[0] = s[2][1]
        return True
    if s[1][0] != 0 and s[1][0] == s[2][1] and s[2][1] == s[3][2]:
        utility_value[0] = s[1][0]
        return True
    if s[0][0] != 0 and s[0][0] == s[1][1] and s[1][1] == s[2][2]:
        utility_value[0] = s[0][0]
        return True
    if s[1][1] != 0 and s[1][1] == s[2][2] and s[2][2] == s[3][3]:
        utility_value[0] = s[1][1]
        return True
    if s[0][1] != 0 and s[0][1] == s[1][2] and s[1][2] == s[2][3]:
        utility_value[0] = s[0][1]
        return True
    # alignments in rows or columns
    for c in range(0, 4):
        if s[0][c] != 0 and s[0][c] == s[1][c] and s[1][c] == s[2][c]:
            utility_value[0] = s[0][c]
            return True
        if s[1][c] != 0 and s[1][c] == s[2][c] and s[2][c] == s[3][c]:
            utility_value[0] = s[1][c]
            return True
    for r in range(0, 4):
        if s[r][0] != 0 and s[r][0] == s[r][1] and s[r][1] == s[r][2]:
            utility_value[0] = s[r][0]
            return True
        if s[r][1] != 0 and s[r][1] == s[r][2] and s[r][2] == s[r][3]:
            utility_value[0] = s[r][1]
            return True
    # grid is full without any alignment i.e. draw
    n = 0
    for c in range(0, 4):
        for r in range(0, 4):
            if s[r][c] == 0:
                n = n + 1
                break
    if n == 0:
        utility_value[0] = 0
        return True
    return False


def MIN_VALUE(s, stack):
    if terminal_test(s):
        if results[2] < stack:
            results[2] = stack  # see max growth of stack exceeds max value
        return utility_value[0]
    min_val = 1000
    for col in range(0, 4):
        if s[3][col] == 0:  # check if col has space
            x = MAX_VALUE(successor_function(s, col, True), stack + 1)
            if min_val > x:
                min_val = x
    return min_val


def MAX_VALUE(s, stack):
    if terminal_test(s):
        if results[2] < stack:
            results[2] = stack  # see max growth of implicit stack
        return utility_value[0]
    max_val = -1000
    for col in range(0, 4):
        if s[3][col] == 0:  # check if col has space
            x = MIN_VALUE(successor_function(s, col, False), stack + 1)
            if max_val < x:
                max_val = x
    return max_val


def MIN_VALUEAlphaBeta(s, a, b):
    if terminal_test(s):
        return utility_value[0]
    min_val = 1000
    for col in range(0, 4):
        if s[3][col] == 0:  # check if col has space
            x = MAX_VALUEAlphaBeta(successor_function(s, col, True), a, b)
            if min_val > x:
                min_val = x
            if min_val <= a:
                break
            if min_val < b:
                b = min_val
    return min_val


def MAX_VALUEAlphaBeta(s, a, b):
    if terminal_test(s):
        return utility_value[0]
    max_val = -1000
    for col in range(0, 4):
        if s[3][col] == 0:  # check if col has space
            x = MIN_VALUEAlphaBeta(successor_function(s, col, False), a, b)
            if max_val < x:
                max_val = x
            if max_val >= b:
                break;
            if a < max_val:
                a = max_val
    return max_val


def make_next_move():
    max_child = 0
    max_val = -1000
    for col in range(0, 4):
        if S[3][col] == 0:
            x = MIN_VALUE(successor_function(S, col, False), 0)
            if max_val < x:
                max_val = x
                max_child = col
    i = 0
    j = max_child
    for row in range(0, 4):
        if S[row][j] == 0:
            i = row
            break
    stampAt(i, max_child, False)
    S[i][j] = 1
    if terminal_test(S):
        game_over()


def make_next_move_alphabeta():
    max_child = 0
    max_val = -1000
    a = -9999
    b = 9999
    for col in range(0, 4):
        if S[3][col] == 0:
            x = MIN_VALUEAlphaBeta(successor_function(S, col, False), a, b)
            if max_val < x:
                max_val = x
                max_child = col
            if max_val >= b:
                break;
            if a < max_val:
                a = max_val
    i = 0
    j = max_child
    for row in range(0, 4):
        if S[row][j] == 0:
            i = row
            break
    stampAt(i, max_child, False)
    S[i][j] = 1
    if terminal_test(S):
        game_over()


def human_move(i, j):
    stampAt(i, j, True)
    S[i][j] = -1
    if terminal_test(S):
        game_over()
    else:
        if isAlphaBeta[0] == 0:
            start_time = timeit.default_timer()
            make_next_move()  # computer's chance to play. append time taken by the move
            results[3] += (timeit.default_timer() - start_time) * 1000  # time in miliseconds

        else:
            start_time = timeit.default_timer()
            make_next_move_alphabeta()
            results[7] += (timeit.default_timer() - start_time) * 1000
    H_TURN[0] = True


def new_game():
    game_counts[0] +=1; #track of number of games played
    GAME_ON[0] = True
    drawGrid()
    if isAlphaBeta[0] == 0:
        for i in range(0, 5):
            results[i] = 0
        # make_next_move() # uncomment this to calulate the first move
    else:
        for i in range(0, 4):
            results[i + 5] = 0
        # make_next_move_alphabeta()
    for x in range(0, 4):
        for y in range(0, 4):
            S[x][y] = 0
    stampAt(0, 0, False)
    S[0][0] = 1
    # first move takes arount 20 seconds to calculate and is always at 0,0.
    # this step has been done for ease of testing.
    H_TURN[0] = True


def clicked(x, y):
    if NEW[0]:  # First time
        H_TURN[0] = False
        tdraw.reset()
        NEW[0] = False
        new_game()
    elif not GAME_ON[0]:
        if (-100 < x < 500) and (-200 > y > -300):
            if -100 < x < 200:
                isAlphaBeta[0] = 0
            else:
                isAlphaBeta[0] = 1
            H_TURN[0] = False
            tdraw.reset()
            new_game()
    elif H_TURN[0] and GAME_ON[0]:
        tdraw.goto(x, y)
        if (0 < x < 400) and (200 > y > -200):
            n = get_clicked_block(x, y)
            if (n != -1) and valid_block(n % 10, n / 10):
                H_TURN[0] = False
                human_move(n % 10, n / 10)


def play_game():
    screen.onclick(clicked)
    screen.onkey(screen.bye, "q")  # press q to quit
    screen.listen()
    firstscreen()
    t.mainloop()


print 'Option 1: Display the empty board \n' \
      'Option 2: Play the game using Minimax algorithm or Alpha Beta pruning \n' \
      'Option 3: Show all results R1-R12. \n'

while True:
    op = raw_input("Next option? : ")
    if op == '1':
        drawGrid()
    elif op == '2':
        play_game()
    elif op == '3':
        for i in range(0, 12):
            print "R %d : " % (i+1),
            print results[i]
        break
    else:
        continue