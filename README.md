## sicilianquiz

a roundabout way to better my understanding of directed acyclic word graphs so i can create an implementation of a late 80's [scrabble solving algorithm](https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf)

### plan
repurpose the dawg implementation [by Steve Hanov](http://stevehanov.ca/blog/index.php?id=115) to accept words as algebraic lines of the defence to quiz myself <br/>
insert each line into the dawg as a single word with each move labeled either W for white, V for black, and ending with X
(to confront the case where two similar pieces can make the same move) <br/>
ie. Najdorf
  1. e4 c5
  2. nf3 d6
  3. d4 cxd4
  4. nxd4 nf6
  5. nc3 a6
    
becomes:
  We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3Va6X(Najdorf)
<br/>

computer 'randomly' suggests nth move, player enters theirs- both are verified to exist as substrings in the dawg and the game continues until a line's end is reached <br/>
quiz the user to name the line through multiple choice

### TODO:
   - ~~test partial strings given one opening~~
   - ~~implement functions in the dawg for partial lines and test with multiple openings~~
   - create a system for randomizing the computers moves 
   - add rest of the variations
   - build class for game without quiz
   - build quiz
