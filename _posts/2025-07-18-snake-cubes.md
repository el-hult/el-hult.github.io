---
title: "Snake squares puzzle chatbots for now"
tags: ['llm','chatbot','puzzle','recreational-mathematics']
---

I visited some friends recently, and they had a [snake cube](https://en.wikipedia.org/wiki/Snake_cube) toy on the table. I sat down with it for a little while, and considering I have been doing a little [Advent of Code](https://adventofcode.com/) programming, I thought it would be fun to think about how to solve it programmatically. For a small snake cube, say $$3 \times 3 \times 3$$, it would be trivial to do an exhaustive search, but what happens as the snake grows considerably? The search space grows exponentially. And how far can one come with pen and paper? It thought it would be fun to formalize the problem, simplify it a little (to only do 2D, i.e. *snake squares*) and see how far current chatbots can take it. Spoiler: both Gemini Pro 2.5 and ChatGPT free tier fail miserablly and provide invalid solutions claiming they are valid. Below is the task I gave them, with some very minor language tweaks for this blog post. I also gave the problem in LaTeX format instead of markdown.

---

### Definition of Snake Square Toys

A *snake square* (a wooden toy analogous to a snake cube, but designed for tiling an $$n \times n$$ square in the plane) is described by a sequence of distances $$d_0, d_1, \ldots, d_m$$.


- $$d_0$$: Represents the length of the first straight segment. This segment starts with an end-block and concludes with a turning-block.
- $$d_m$$: Represents the corresponding length of the final straight segment.
- $$d_i$$ for $$0 < i < m$$: All other segments $$d_i$$ begin and end with a turning-block, and may contain straight blocks in between. 

For every segment, we require $$d_i \ge 2$$. The total number of unit blocks in the snake square, which must cover an $$n \times n$$ square, is given by the formula

$$N=n^2=d_0 + \sum_{i=1}^{m} (d_i - 1)$$


### Palindromic Equivalence of Snake Square Toys

Two snake squares described by sequences $$(d_0, \ldots, d_m)$$ and $$(d'_0, \ldots, d'_{m'})$$ are *equivalent* if one sequence can be obtained from the other by reversing the order of segments. That is, if $$m = m'$$ and $$d_j = d'_{m-j}$$ for all $$j \in \{0, \ldots, m\}$$. This implies that a snake square viewed from one end is equivalent to viewing it from the other end.


### Solutions, Equivalent solutions, and Realized Solution


The turning blocks in the snake square can be rotated either right (clockwise) or left (counter-clockwise). A solution for a snake square is introduced by specifying a sequence of turn types for each turning block:

$$\mathcal{L} = (t_1, t_2, \ldots, t_m)$$

where $$t_j \in \{L, R\}$$ signifies a 'Left turn' or a 'Right turn', respectively.


When combined with the snake's structure, a solution can be written as:

$$(d_0, t_1, d_1, t_2, d_2, \ldots, t_m, d_m)$$


Two solutions are equivalent by considering the symmetry group of rigid motions of the square. Rotations to not change the solution, but flipping the square over on the table is equivalent to switching all the turns $$L \leftrightarrow R$$. Thus, every solutions has a equivalent solution considering this symmetry. The solution starting with $$R$$ is the representative we seek if asking for *distinct solutions*.


A *realized solution* is formed by adding a specific starting position $$(x_1, y_1)$$ and a starting direction (e.g., North, South, West, East) to a solution sequence. As the snake is laid out in the plane, for each segment $$d_k$$, the snake moves $$d_k - 1$$ steps forward in its current direction, and then at the turning block, it turns $$t_k$$ (L for counter-clockwise, R for clockwise) by 90 degrees. This process generates a sequence of coordinates $$((x_i, y_i))_{i=1}^N$$ that the snake's blocks occupy. We number the coordinates such that the top-left corner is $$(1,1)$$, the top-right is $$(n,1)$$, the bottom-left is $$(1,n)$$, and the bottom-right is $$(n,n)$$.

### Validity of a Solution


A solution $$\mathcal{L}$$ for a snake square is considered \textbf{valid} if there exists at least one Realized Solution (i.e., a specific starting position and direction) such that the sequence of coordinates $$((x_i, y_i))_{i=1}^N$$ visits every coordinate in the $$n \times n$$ square exactly once, without any overlaps.

### Example


- The sequence $$(3, 3, 3, 2, 2)$$ describes a particular snake square toy.
- The sequence $$(3, R, 3, R, 3, R, 2, R, 2)$$ is a solution for this snake square.
- If we consider a realized solution starting at $$(1,1)$$ facing East, this particular realized solution visits every coordinate in a $$3 \times 3$$ square exactly once (forming a clockwise inward spiral). Therefore, the solution $$(3, R, 3, R, 3, R, 2, R, 2)$$ is considered valid.
- There is no other distinct valid solution for this snake square. The start of the sequence is $$(3,3,3)$$, implying we must start in a corner for the snake to fit in the square. To get the representative solution, we must start with a R turn. From there on, all turns are decided considering the snake must fit in the square and not self-overlap.

# Prroblem
How many valid distinct solutions are there for the snake $$(3,2,3,2,3)$$?

---

I find the answer to be 1. The chatbots claimed either 2 or 3. Gemini even made a python program to verify it.

Within this formalization there are many other fun challenges: 

- For a given snake square, is there any valid solution?
- If a snake square has valid solutions, how many are there?
- How many distinct snake squares with valid solutions are there for a given $$n$$?
- If given a snake square $$(d_0, \ldots, d_m)$$, and a partial solution $$(d_0, t_1, d_1, \ldots, t_k, d_k)$$, how many continuations $$(d_{k+1}, t_{k+1}, \ldots, d_m)$$ are there which make the solution valid?
- What invariants are there on a (partial) solution making it simple to verify it is valid or not, without computing the full path in the plane for each possible starting position and direction?
- Are there any substantial difference between this 2D problem and the more general 3D snake cube problem? It seems to me that the problem setup just means changing the turns into $$t_j\in \{L, R, U, D\}$$ for left, right, up and down, and the realized solution needs 6 cardinal directions instead of 4, and the solution path is in 3D. It is clear that one cannot "flip the solution over" as we do with a 2D cube lying on a table, so the symmetries are different when talking about distinct solutions. But mostly, it seems to not change.
- Is there some pen and paper solutions to the problem, or must we use computer search?
- When developing a software solver, is it better to enumerate all possible solutions, and for each of them check if they are valid, or should one start with hamiltonian paths in the plane and then check how many distinct snake squares they correspond to? Which approach is more ameanable to heuristics for pruning the search space?

There also seems to be some way to find recursive solutions for some snake squares. There is a $$n \times n$$ snake square solution that begins $$(n, R, n, R, ...)$$ where the rest of the solution (and snake) is given by solving a $$(n-1) \times (n-1)$$ snake square, starting from outside one of the corners, with a given direction. While we can recursively decompose the problem like this, it has broken some if the symmetries of the subproblem snake square.

---

P.S. After completing this post I did a little google searching. Most results were ads and spam, but on arXiv I found a paper that exactly considers this problem. They state that it is open whether the the complexity of establishing if a valid solutions exist is NP-hard, and prove that some variations on the problems are indeed NP-hard. The work was part of some course work for a group of students. It was fun to skim it. Read it on [arXiv](https://arxiv.org/abs/2407.10323).
I take this paper as evidence that this problem is fun, interesting and not at all trivial.
