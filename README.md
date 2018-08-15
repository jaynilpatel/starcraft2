# StarCraft2 AI Bot

An attempt to implement a deep learning model (CNN) in the strategic game, Starcraft 2. The goal here is to build a model which can learn the tactics for playing and winning the game against the another bot (built-in). A library known as PySC2 was extensively used as an API in order to interact with game objects using python.

The first part of this project was to generate the training data. This was made possible by writing a script that takes random decisions in the game yet following certain policies for the game. The decisions were not totally random, since some of the decisions were hardcoded. The game was simulated for a particular game map (Abyssal Reef LE).

To help visualize what was going on, a graphical representation was created using OpenCV. This helped to visualize the position of the game objects and the number of tools and utilities left at a particular moment. For the games that were won, this graphical representation was stored as training data. This was done for about 100 successful games and thus resulted in 13.2 Gb worth of data. 

The second part was to train the CNN model using this data. The training data which was generated for 100 successful games was fed in CNN. The resultant model is now able to win most of the games at medium difficulty.

#### Before you start the game:
 1. First, you will need to download/install StarCraft II. Grab the client, and install the game from here: [Clients](https://us.battle.net/account/download/).
 1. Download Map Packs from Blizzard s2client: [Map Packs](https://github.com/Blizzard/s2client-proto#map-packs)
    1. Download ```Ladder 2017 Season 1```
    1. Once you have the maps archive, extract them to a Maps directory from within your StarCraft II directory (C:\Program Files (x86)\StarCraft II\Maps). Now the hierarchy will be:  
        ```
        Program Files(x86)
        -StarCraft II
        --Maps
        ---Ladder2017Season1
        ----AbyssalReefLE.SC2Map
        ```
 1. Clone this repository.
 1. Download the trained model: [Model](https://drive.google.com/open?id=1t_3Jn2YH8JxcXH2asQA11skVr6rm9xFt)
    1. Extract the archive to get ```BasicCNN-30-epochs-0.0001-LR-4.2```.
    1. Place this in the same directory as ```ai-bot.py``` (inside the repository).
 1. Download the training data if you want to train your own network : [Data](https://drive.google.com/open?id=1rIkBJbLvlWS4aw7RA0vaivK6TMzrmE8J)
    1. Extract the archive to get ```train_data``` folder.
    1. Place this in the same directory as ```ai-bot.py``` 
 
 #### Use the trained model
 
 Open ```ai-bot.py``` and set ```use_model=True```
 ```
 run_game(maps.get("AbyssalReefLE"),[
    Bot( Race.Protoss, OurCustomBot(use_model=True)),
    Computer( Race.Terran, Difficulty.Medium)
], realtime=False)
 ```
 
#### Set gameplay in real time

Open ```ai-bot.py``` and set ```realtime=True```
 ```
 run_game(maps.get("AbyssalReefLE"),[
    Bot( Race.Protoss, OurCustomBot(use_model=True)),
    Computer( Race.Terran, Difficulty.Medium)
], realtime=True)
 ```

## Setup Game

Install ```virtualenv``` by running the following pip command:
```
C:\Users\USERNAME>pip3 install --user --upgrade virtualenv
Collecting virutalenv
[...]
Successfully installed virtualenv
```
Open command prompt on Windows in the same directory where  ```env``` folder exist (inside the repository). Now to run the game, start the environment :
```
# start the environment
YOUR REPOSITORY PATH>env\Scripts\activate
```
This will activate the enviroment. Now run ```ai-bot.py```
```
(env) YOUR REPOSITORY PATH>python ai-bot.py
```
