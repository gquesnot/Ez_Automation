# Ez Automation

Template to make a bot. 




## Description

When you launch the bot you will have a graphical interface to configure the information you want to retrieve from the window.
You can also manage the states of the bot.

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

### Dependencies



### Installing

Require python 3.10
````shell
 pip install -r requirements.txt
````

### Executing program

### Usage

````shell
 python main.py
````

Use what you have set up like this:
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
