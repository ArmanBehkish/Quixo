# Quixo Agent
 ***AGENT PLAYING QUIXO GAME*** 

 ***PROBLEM DEFENITION***: Quixo game is played on a 5*5 Board with cubes each having either 'X', 'O' or Neutral face. Each player can take a peice on the boarder (if his own or neutral) remove and put at the corresponding row/col end slinding that row/col to fill the gap. Winner is the first one completing a row/column/diagonal.  
 > Based on [HERE] (https://www.ultraboardgames.com/quixo/game-rules.php)  
 > **The player to make a line with his/her opponent's symbol loses the game, even if he/she makes a line with his/her own symbol at the same time.**


***IMPLEMENTATION***: Based on experiences with RL and the nature of Quixo game (which is a perfect information, turn-based, diterministic and Zero-Sum game), seems best algorithm to implement the agent is MinMax tree search and it's variations. 

1. A **Manual Player** is implemented so that user can play with agent to better understand different conditions of the game.
2. It is implemented a **simple MinMax algorithm** to work with GAME class, and the make_move() abstract method. The agent only **receives the DEPTH of tree**, which is usually works well with ***depth = 3***. 
3. Made sure the algorithm have the **same result whether the agent plays first or second**. This is accomplished by how the minmax() method is implemented.
4. A method **check_loops()** to set a threshold for loops and the agent returns a random move if a fix move is repeated for a certain number of times.  
5. To check the terminal nodes, 3 conditions are checked (whether there is a winner; no moves remains; or depth limit is reached).  
6. Tried a number of ways for the **static evaluation of terminal nodes**, got the best results with this two:
   - **Number of peices player has in the center positions** (9 central positions), each  +1 points.  
   - **Whether there is a winner**(+10 points) or loser (-10) points.  
7. **alpha-beta pruning to speed up the agent**.  
8.  **added a memory** , it saves the value of node after each recursive call to minmax (alphabeta), so that previously visited nodes do not have to be recalculated. This also solved the loop problem.
9. In the alphabeta method, first **sort the possible moves** (actions) so that alpha-beta pruning cut the unnecessary branches sooner and speed-up the test. (**only do this sort in the top two levels of the tree**). ascending for maximizer player and descending for minimizer player.  
10. Also tried monte carlo roll-out (i.e. playing 10 random games) for static evaluation of terminal nodes. It was too slow to see the results or be useful in this case.


***RESULTS***:  

The most complete agent could get to 95% win rate.
Here are the test resutls:

| Agent | First/Second Player | Depth | Memory | %WINS | seconds/game |
|------|------|------|------|------|------|
| AlphaBeta | First | 3 | Yes | 81 | ***8.5*** |
| AlphaBeta | First | 4 | Yes | ***95*** | 53 |
| AlphaBeta | Second | 3 | No | 72 | 45 |
| AlphaBeta | Second | 3 | Yes | 71 | 9.5 |
| AlphaBeta | Second | 4 | Yes | 90 | 60 |



