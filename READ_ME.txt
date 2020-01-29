If it ain't broke, don't fix it.

reversi_ai.py:
    Code for training neural networks to play game Reversi. Has lots of neat features.
    Bells and Whistles included as stock.

    dependencies: time, random, threading, copy and neural_network.py


pong.py:
    Code for two player pong game. player one controls are up and down arrows, player two controls are w and s keys.

    dependencies: sys, pygame, time, random


pong_ai_v1.py:
    code for training ai as defined in neural_network.py to play pong. multi-threaded solution. These threads are
    used to prevent low processing power meaning Neural Network evaluation does not cause frames in pong game to drop.
    Whether or not neural network will effectively run on processor with diff. clock speed after being trained
    remains to be seen. Any correspondence re. this would be gratefully received

    dependencies: sys, pygame, time, threading


pong_ai_v2.py:
    code to allow human player to play simple AI using trajectory prediction. multi-threaded solution. These threads are 
    used to stop frames in pong game dropping as result of trajectory calc.
    
    dependencies: sys, pygame, time, random, threading, os


neural_network.py:
    implementation of moderate level neural network. Designed to be importable.

    Network objects can be defined with parameter for dimensions (code can handle n layers of m1, m2, .. , mn sizes),
    boolean for if weights are known, name as string, generation as integer, project name as string.

    dependencies: NumPy, pathlib, os and pygame
