# Ez Automation

Template to make a bot. 




## Description

When you launch the bot you will have a graphical interface to configure the information you want to retrieve from the window.  

Manage the global states of the bot:
- PLAY : in the future close all cv2 windows
- RECORD: State you want to be to analyze the game
- REPLAY: state to read img you saved (autoscreenshot, screenshot etc)


You can manage the states of the bot:
- WAITING: base state of the bot, doing nothing.
- PLAYING: look in the game Class loop
- add  more in the enum GameState class


Manage some options :
- toggle freeze (stop image update)
- toggle auto screenshot (3s)
- toggle show cv2 windows for regions
- toggle fps

You can configure:
- the name of the window to retrieve (the basic screenshot)
- creation of region (a part of screen)
- detection of pixels OR/ AND 
- detection of text/int 
- image detection OR/AND
- mask detection (manualy)
- action
- combo actions (soon)

## Getting Started

- Start the bot
- Configure/window 
- Configure/region
- Configure what you want 
- configure the algorithm for your bot in Game Class


### Installing

Require python 3.10
````shell
 pip install -r requirements.txt
````


### Usage

````shell
 python main.py
````

Use what you have set up like this in the main loop of game/game.py class :
````python
if self.state == GameState.PLAYING:
    print('scan wave: ', self.dpc.checkTcrScan('wave'))
    print('check pixel evt1On: ', self.dpc.checkPixel("evt1On"))
    print('check image evt1: ', self.dpc.checkImageMatch('evt1'))
    print('check mask greenBar: ', self.dpc.checkMaskDetection('greenBar'))
    print('do action closeUp')
    self.doClick('closeUpgrade')
    self.doKey('up')
````
