# Ô'🍅
This program is an Finite-state automaton (FSA) editor.

## Load specificaton
*All the information come from [Instruction/Projet](Instruction/Projet).*

The program need to contains the following features :
- [X] FSA Editing, which means :
  - [X] Adding
  - [X] Importation/Exportation with a file
  - [X] Editing
  - [X] Removing
- [ ] Check if a word can be read by the FSA
- [X] Check if an AEF is complete
- [X] Transform an AEF into an complete AEF
- [X] Check if an AEF is deterministic
- [ ] Transform an AEF into a deterministic one
- [X] Do the folow operation
    - [X] Complement of an AEF
    - [X] Mirror of an AEF
    - [X] Product of two AEFs
    - [X] Concatenation of two AEFs 
- [X] Extract a regular expression from an AEF. For example, a\*b is a regular exepression.
- [X] Find AEF admited language. For example, {a*b} is a language
- [ ] Check if two AEF are equivalen (they recognized same language)
- [X] Transform an AEF into an trim one
- [ ] Transform an AEF into a minimal one. The new AEF will recognized the same language, with the minmal number of state. Which means that no state can be removed from the AEF and without change the know language
- [ ] The interface need to be in the shell

## Optional feature
- [X] Export the FSA in an image (.png)
- [ ] A GUI for editing the FSA

## FSA save file (.csv)
The program use the .oto extension to save your Finite-State automaton. The strucuture is the same as a CSV file with the follow header :
```
Header : Names of the state, first event, second event, thrid event, [...], EI, EF
EI: Etat Initial (0 : false, 1: true)
EF: Etat Final (0 : false, 1: true)
Note: The "Names of the state" column is "etat"
```

**Example 1 :**\
This example represent an AEF reading an binary number with an even number of 1

[even.csv](Sample/Examples/even.csv)
```
etat;0;1;EI;EF
q_even;q_even;q_odd;1;1
q_odd;q_odd;q_even;0;0
```

We can represent this AEF with the folowing graph :\
![Even AEF graph](Sample/Examples/otomate.png)

**Example 2 :**\
Other abstract example : 

[abstract.csv](Sample/Examples/abstract.csv)
```
etat;a;b;c;d;e;f;g;h;i;k;EI;EF
q0;q0;;;;;q1;;;;;1;1
q1;;q1;;;;;q2;;;;0;0
q2;;;q2;;;;;q3;;;0;1
q3;;;;q3;;;;;q4;q0,q1;0;0
q4;;;;;q4;;;;;;0;1
```
We can represent this AEF with the folowing graph :\
![Abstract AEF graph](Sample/Examples/otomate1.png)

You will find more examples in [Sample/Examples](Sample/Examples)
