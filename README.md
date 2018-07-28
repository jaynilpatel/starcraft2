# StarCraft2 AI Bot

An attempt to implement a deep learning model (CNN) in the strategic game, Starcraft 2. The goal here is to build a model which can learn the tactics for playing and winning the game against the built-in another bot. A library known as PySC2 was extensively used in order to interact with game objects using python.

The first part was to generate the training data. This was made possible by writing a script that takes random decisions in the game yet following certain rules for the game. The decisions were not totally random, since some of the decisions were hardcoded. The game was simulated for a particular game map (Abyssal Reef LE).

To help visualize the what was going on, a graphical representation was created using OpenCV. This helped to visualize the position of the game objects and the number of tools and utilities left at a particular moment. For the games that were won, this graphical representation was stored as training data. This was done for about 100 successful game and thus resulted in 13.2 Gb worth of data. 

The second part was to train the CNN model using this data. The training data which was generated for 100 successful games was fed in CNN. The resultant model is now able to win most of the games at medium difficulty.
