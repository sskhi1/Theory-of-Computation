Finite Automaton Project
Part 1: Automatic Conversion to Finite Automaton
This section of the project involves constructing a non-deterministic finite automaton (NFA) based on a given regular expression.

Input Format
The program receives a single line of input from standard input, containing a regular expression.
The regular expression may include:
Lowercase Latin letters (a-z) and digits (0-9).
| (union) for representing alternatives.
* for denoting repetition of the preceding expression any number of times.
Parentheses ( and ) for grouping expressions.
No special symbol for the empty string (ε) is included, but empty parentheses () can be used to represent it.
Task Description
Construct a non-deterministic finite automaton (NFA) that represents the given regular expression.
The NFA should meet the following constraints:
The automaton should have at most one more state than the length of the expression.
The automaton must not include ε-transitions.
Output Format
The program should output the constructed NFA to standard output in the following format:

The first line should contain three integers separated by spaces:
n: the number of states in the automaton.
a: the number of accepting states.
t: the total number of transitions.
The second line should list the a integers representing the indices of the accepting states.
For each state, output the following information on a new line:
The first number indicates how many transitions (ki) originate from that state.
This should be followed by ki pairs, each consisting of a transition symbol and the destination state index.
Example
Input 1:
(a|b)*(c|())

Output 1:
2 2 3
0 1
3 a 0 b 0 c 1
0


Input 2:
(ab*c(0|1)*)*

Output 2:
3 2 6
0 2
1 a 1
2 b 1 c 2
3 0 2 1 2 a 1

Program Name
Name this program build with an appropriate extension based on the programming language you are using (e.g., build.py for Python).

Part 2: Automaton Simulation
This section of the project involves simulating the operation of the NFA constructed in Part 1 on a given input string.

Input Format
The first line of input is the string to be tested.
Subsequent lines describe the automaton in the same format as the output from Part 1.
Task Description
The program should simulate the operation of the automaton on the input string.
For each character in the input string, determine whether the automaton is in an accepting state after reading that character.
Output Format
Output a string of the same length as the input string.
For each character position i:
Output Y if the automaton is in at least one accepting state after reading the first i characters.
Output N if it is not.
Example
Input 1:
aababacab
2 2 3
0 1
3 a 0 b 0 c 1
0

Output 1:
YYYYYYYNN

Input 2:
abbc1acabbbbc001cabc
3 2 6
0 2
1 a 1
2 b 1 c 2
3 0 2 1 2 a 1

Output 2:
NNNYYNYNNNNNYYYYNNNN

Program Name
Name this program run with an appropriate extension based on the programming language you are using (e.g., run.py for Python).
