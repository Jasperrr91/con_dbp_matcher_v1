import sys

from package.wrapper import match_text

#text = "is it correct to say that alan turing and noam chomsky are the giants in theoretical computer science"
input_text = sys.argv[1:]

the_winner = match_text(input_text, verbose=True)

for x,y in the_winner.items():
    print(x,y)