import os
from dataclasses import fields
from time import sleep

import cv2

from app.my_dataclasses import WindowConfig, RegionConfigs, ImageMatchConfigs, PixelConfigs, TcrScanConfigs, \
    MaskDetectionConfigs, ActionConfigs
from util.InputHandler import getMenus, getMenusElements, updateValueOfKey, askQuestion
from util.json_function import getJson, toJson
from util.pixel import getImgRectangle


class ConfigController():
    clicks = []

    game = None
    window: WindowConfig = None
    regions: RegionConfigs = None
    matchImages: ImageMatchConfigs = None
    pixels: PixelConfigs = None
    tcrScans: TcrScanConfigs = None
    maskDetections: MaskDetectionConfigs = None
    actions: ActionConfigs = None

    def __init__(self, game):
        self.window = WindowConfig.from_dict(getJson("window"), )
        self.regions = RegionConfigs.from_dict(getJson("regions"))
        self.matchImages = ImageMatchConfigs.from_dict(getJson("matchImages"))
        self.pixels = PixelConfigs.from_dict(getJson("pixels"))
        self.tcrScans = TcrScanConfigs.from_dict(getJson("tcrScans"))
        self.maskDetections = MaskDetectionConfigs.from_dict(getJson("maskDetections"))
        self.actions = ActionConfigs.from_dict(getJson("actions"))
        self.game = game

    def apply(self, obj, hint: str, withOutDict: bool = False):
        myDc = getattr(self, hint)

        for field in fields(myDc):
            if withOutDict:
                value = getattr(myDc.dict, field.name)
            else:
                value = getattr(myDc, field.name)
            setattr(obj, field.name, value)

    def set(self, model, obj, save=False, load=False):
        myDc = getattr(self, model)
        for field in fields(myDc):
            setattr(myDc, field.name, getattr(obj, field.name))
        if load:
            self.load(model)
        if save:
            return self.save(model)
        return myDc

    def setKey(self, model, key, value, save=False, load=False):
        myDc = getattr(self, model)
        setattr(myDc, key, value)
        if load:
            self.load(model)
        if save:
            return self.save(model)
        return myDc

    def saveOnly(self, model, reload=False):
        myDc = getattr(self, model)
        if reload:
            self.load(model)
        toJson(model, myDc.to_dict())
        return myDc

    def save(self, model):
        myDc = getattr(self, model)
        toJson(model, myDc.to_dict(), "json_data/")
        return myDc

    def load(self, model):

        if model == "window":
            self.game.wc.loadConfig()
        elif model == "regions":
            self.game.regions = getattr(self, model)
            self.game.cv2Controller.refreshRegion = True
        elif model == "matchImages":
            self.game.dpc.loadMatchImages()
        elif model == "pixels":
            self.game.dpc.loadPixels()
        elif model == "tcrScans":
            self.game.dpc.loadTcrScans()
        elif model == "maskDetections":
            self.game.dpc.loadMaskDetections()
        elif model == "actions":
            self.game.actions = self.actions

    def update(self, model, name: str, value):
        if model == "window":
            self.window = value
        else:
            getattr(self, model).update(name, value)
        self.save(model)

    def updateValue(self, model, name: str = "", key="", value=""):
        if model == "window":
            setattr(self.window, key, value)
        else:
            setattr(getattr(self, model).get(name), key, value)
        self.save(model)

    def addClick(self, click):
        if len(self.clicks) == 2:
            self.clicks.pop()
        self.clicks.append(click)

    def getLastClick(self):
        if len(self.clicks) != 0:
            return self.clicks[0]
        else:
            return None

    def getRectangle(self):
        if len(self.clicks) == 2:
            return {
                "x": self.clicks[0]['x'],
                "y": self.clicks[0]['y'],
                "w": abs(self.clicks[1]['x'] - self.clicks[0]['x']),
                "h": abs(self.clicks[1]['y'] - self.clicks[0]['y']),
                "region": self.clicks[0]['region']
            }
        else:
            return None

    def getMainMenu(self):
        stopped = False
        while not stopped:
            response = getMenus("Configuration", getMenusElements(names=[
                "Window",
                "Regions",
                "MatchImages",
                "Pixel",
                "TcrScan",
                "Mask Detection",
                "Action",
                "Back"
            ]))
            match response:
                case 'Window':
                    self.configWindow()
                case 'Regions':
                    self.configRegion()
                case 'MatchImages':
                    self.configMatchImages()
                case 'Pixel':
                    self.configPixel()
                case 'TcrScan':
                    self.configTcrScan()
                case 'Mask Detection':
                    print('Not implemented yet')
                    sleep(1)
                    # self.configMaskDetection()

                case 'Action':
                    self.configAction()
                case 'Back':
                    return
                case _:
                    return

    def configMaskDetection(self):
        maskDetections = getJson("maskDetection")
        stopped = False
        while not stopped:
            response = getMenus("Mask Detection", getMenusElements(names=[
                "Add Mask Detection",
                "Update",
                "Delete",
                "Test",
                "Back",
            ]))
            match response:
                case 'Add Mask Detection':
                    maskDetections = self.addMaskDetection(maskDetections)
                case 'Update':
                    maskDetections = self.updateMaskDetection(maskDetections)
                case 'Delete':
                    maskDetections = self.deleteMaskDetection(maskDetections)
                case 'Test':
                    self.testMaskDetection(maskDetections)
                case 'Back':
                    stopped = True
                case _:
                    stopped = True
            self.saveMaskDetection(maskDetections)

    def addMaskDetection(self, maskDetections):
        stoppedName = False
        name = ""
        while not stoppedName:
            name = input("Name: ")
            if name == "":
                return maskDetections
            if name not in maskDetections:
                stoppedName = True

        stopped = False
        return maskDetections

    def updateMaskDetection(self, maskDetections):
        return maskDetections

    def deleteMaskDetection(self, maskDetections):
        stopped = False
        while not stopped:
            name = getMenus("Delete Mask ", getMenusElements(names=list(maskDetections.keys()) + ["Back"]))
            if name == "Back" or name == "": return maskDetections
            del maskDetections[name]
        return maskDetections

    def testMaskDetection(self, maskDetections):
        pass

    def saveMaskDetection(self, maskDetections):
        toJson("maskDetection", maskDetections, "json_data/")
        self.game.dpc.loadMaskDetections()

    def configAction(self):
        actions = getJson("action")
        stopped = False
        while not stopped:
            response = getMenus("Action", getMenusElements(names=[
                "Add Action",
                "Update",
                "Delete",
                "Test",
                "Back"
            ]))
            match response:
                case 'Add Action':
                    actions = self.addAction(actions)
                case 'Update':
                    actions = self.updateAction(actions)

                case 'Delete':
                    actions = self.deleteAction(actions)
                case 'Test':
                    self.testAction(actions)
                case 'Back':
                    stopped = True
                case _:
                    stopped = True
            self.saveActions(actions)

    def addAction(self, actions):
        stoppedName = False
        name = ""
        while not stoppedName:
            name = input("Name: ")
            if name == "":
                return actions
            if name not in actions:
                stoppedName = True
        type_ = getMenus("Type", getMenusElements(names=["Keyboard", "Mouse", "Cancel"]))
        newAction = {
            "type": type_,
        }
        if type_ == "" or type_ == "Cancel": return actions
        match type_:
            case 'Keyboard':
                stoppedChar = False
                value = ""
                while not stoppedChar:
                    value = input("Key : ")
                    if value != "" and len(value) == 1:
                        stoppedChar = True
                    newAction['key'] = value
            case 'Mouse':
                print('pass click')
                self.clicks = []
                stoppedClick = False
                while not stoppedClick:
                    click = self.getLastClick()
                    if click is not None:
                        stoppedClick = True
                        newAction['x'] = click['x']
                        newAction['y'] = click['y']
                        newAction['region'] = click['region']
                    sleep(0.01)
        newAction['delay'] = askQuestion("Delay (s): ", 0.1, float)
        newAction['sleepAfter'] = askQuestion("Sleep after (s): ", 0.1, float)
        actions[name] = newAction
        return actions

    def updateAction(self, actions):
        stoppedName = False
        while not stoppedName:
            name = getMenus("Update Action", getMenusElements(names=list(actions.keys()) + ["Back"]))
            if name == "Back" or name == "": return actions
            action = actions[name]
            stopped = False
            while not stopped:
                response = getMenus(f"Update Action {name}", getMenusElements(obj=action, names=["Back"]))
                if response == "Back" or response == "":
                    stopped = True
                    break
                for key in action.keys():
                    if response == key:
                        updateValueOfKey(action, key)

                        break

                actions[name] = action
                self.saveActions(action)
        return actions

    def deleteAction(self, actions):
        stopped = False
        while not stopped:
            name = getMenus("Delete Action ", getMenusElements(names=list(actions.keys()) + ["Back"]))
            if name == "Back" or name == "": return actions
            del actions[name]
        return actions

    def testAction(self, actions):
        stopped = False
        while not stopped:
            name = getMenus("Test Action", getMenusElements(names=list(actions.keys()) + ["Back"]))
            if name == "Back" or name == "": return
            action = actions[name]
            print('Select the game window')
            for i in range(0, 3):
                print(f"action in {3 - i}s")
                sleep(1)
            self.game.doAction(name)

    def saveActions(self, actions):
        toJson("action", actions)
        self.game.actions = actions

    def configTcrScan(self):
        tcrScans = getJson("tcrScan")
        stopped = False
        while not stopped:
            response = getMenus("Tcr Scan", getMenusElements(names=[
                "Add Scan",
                "Delete",
                "Update",
                "Check",
                "Back"
            ]))
            match response:
                case 'Add Scan':
                    tcrScans = self.addTcrScan(tcrScans)
                case 'Delete':
                    tcrScans = self.deleteTcrScan(tcrScans)
                case 'Update':
                    tcrScans = self.updateTcrScan(tcrScans)
                case 'Check':
                    self.checkTcrScan(tcrScans)
                case 'Back':
                    stopped = True
                case _:
                    stopped = True
            self.saveTcrScan(tcrScans)

    def addTcrScan(self, tcrScans):
        stoppedNewName = False
        name = ""
        match_ = ""
        while not stoppedNewName:
            name = input('Name: ')
            if name != "" and name not in tcrScans:
                break
            else:
                print("Name already exists")
        type_ = getMenus("Type", getMenusElements(names=["int", "string"]))
        self.clicks = []
        stopped = False
        print('Click on the top left corner  and then the bottom right corner where to scan in regions or root')

        while not stopped:
            newTcrScan = self.getRectangle()
            if newTcrScan is not None:
                newTcrScan['type'] = type_
                tcrScans[name] = newTcrScan
                return tcrScans
            sleep(0.01)
        return tcrScans

    def deleteTcrScan(self, tcrScans):
        stopped = False
        while not stopped:
            name = getMenus("Delete Pixel ", getMenusElements(names=list(tcrScans.keys()) + ["Back"]))
            if name == "Back" or name == "": return tcrScans
            del tcrScans[name]
        return tcrScans

    def updateTcrScan(self, tcrScans):
        stoppedName = False
        while not stoppedName:
            name = getMenus("Update Tcr Scan ", getMenusElements(names=list(tcrScans.keys()) + ["Back"]))
            if name == "Back" or name == "": return tcrScans
            stopped = False
            tcrScan = tcrScans[name]
            while not stopped:
                response = getMenus(f"Update Tcr Scan {name}", getMenusElements(obj=tcrScan, names=["Back"]))
                if response == "Back" or response == "":
                    stopped = True
                    break
                for key in tcrScan.keys():
                    if response == key:
                        updateValueOfKey(tcrScan, key)

                        break

                tcrScans[name] = tcrScan
                self.saveTcrScan(tcrScans)
        return tcrScans

    def checkTcrScan(self, tcrScans):
        stopppedName = False
        while not stopppedName:
            name = getMenus("Check Tcr Scan ", getMenusElements(names=list(tcrScans.keys()) + ["Back"]))
            if name == "Back" or name == "": return tcrScans
            print(f'{name} : {self.game.dpc.checkTcrScan(name)}')
            sleep(2)

        pass

    def saveTcrScan(self, tcrScans):
        toJson("tcrScan", tcrScans, "json_data/")
        self.game.dpc.loadTcrScans()

    def configPixel(self):

        pixels = getJson("pixel")
        stopped = False
        while not stopped:
            response = getMenus("Pixels", getMenusElements(names=[
                "Add Category",
                "Delete",
                "Update",
                "Check",
                "Back"
            ]))
            match response:

                case 'Add Category':
                    stoppedNewName = False
                    name = ""
                    match_ = ""
                    while not stoppedNewName:
                        name = input('Name: ')
                        if name != "" and name not in pixels:
                            break
                        else:
                            print("Name already exists")
                    stoppedNewName = False
                    while not stoppedNewName:
                        match_ = input('Match AND/OR: ')
                        if match_ == "AND" or match_ == "OR":
                            break
                        else:
                            print("Type must be AND or OR")
                    pixels[name] = {
                        "match_type": match_,
                        "pixels": []
                    }

                case 'Delete':
                    pixels = self.deletePixel(pixels)
                case 'Update':
                    pixels = self.updatePixel(pixels)
                case 'Check':
                    pixels = self.checkPixel(pixels)
                case 'Back':
                    stopped = True
                case _:
                    stopped = True
            self.savePixel(pixels)

    def savePixel(self, pixels):
        toJson("pixel", pixels, "json_data/")
        self.game.dpc.loadPixels()

    def deletePixel(self, pixels):
        stopped = False
        while not stopped:
            name = getMenus("Delete Pixel ", getMenusElements(names=list(pixels.keys()) + ["Back"]))
            if name == "Back" or name == "": return pixels
            del pixels[name]
        return pixels

    def updatePixel(self, pixels):
        stoppedName = False
        while not stoppedName:
            name = getMenus("Update: Pixel", getMenusElements(names=list(pixels.keys()) + ["Back"]))
            if name == "Back" or name == "": return pixels
            stopped = False
            while not stopped:
                response = getMenus(f"Update pixels {name}", getMenusElements(names=[
                    "Add Pixel",
                    "Delete",
                    "Back"
                ]))
                match response:
                    case 'Add Pixel':
                        pixels = self.addPixelToPixel(pixels, name)
                    case 'Delete':
                        pixels = self.deletePixelFromPixel(pixels, name)
                    case 'Back':
                        stopped = True
                    case _:
                        stopped = True
                self.savePixel(pixels)
        return pixels

    def deletePixelFromPixel(self, pixels, name):
        pixelResponse = getMenus("Delete Image", getMenusElements(
            names=[f"pixel_{idx}" for idx, pixel in enumerate(pixels[name]['pixels'])] + ["Back"]))
        if pixelResponse == "Back" or pixelResponse == "": return pixels
        for idx, pixel in enumerate(pixels[name]['pixels']):
            pixelName = f"pixel_{idx}"
            if pixelName == pixelResponse:
                del pixels[name]['pixels'][idx]
        return pixels

    def addPixelToPixel(self, pixels, name):
        pixel = pixels[name]
        print('Click on a region or root window')
        self.clicks = []
        stopped = False
        while not stopped:
            lastClick = self.getLastClick()
            if lastClick is not None:
                lastClick['color'] = tuple(
                    (int(lastClick['color'][0]), int(lastClick['color'][1]), int(lastClick['color'][2])))
                lastClick['tolerance'] = 20
                pixel['pixels'].append(lastClick)
                pixels[name] = pixel
                return pixels
            sleep(0.01)
        return pixels

    def checkPixel(self, pixels):
        stopppedName = False
        while not stopppedName:
            name = getMenus("Check Pixel ", getMenusElements(names=list(pixels.keys()) + ["Back"]))
            if name == "Back" or name == "": return pixels
            print(f'Pixel {name} : {self.game.dpc.checkPixel(name)}')
            sleep(2)

    def configMatchImages(self):
        stopped = False
        matchImages = getJson('matchImages', 'json_data/')

        while not stopped:
            response = getMenus("Match Images", getMenusElements(names=[
                "Add Match",
                "Delete",
                "Update",
                "Check",
                "Back"
            ]))
            match response:
                case 'Add Match':
                    stoppedNewName = False
                    while not stoppedNewName:
                        name = input('Name: ')
                        if name != "" and name not in matchImages:
                            stoppedNewName = True
                            matchImages[name] = []
                            os.makedirs(os.path.dirname(f"img/{name}/"))
                        else:
                            print("Name already exists")

                case 'Delete':
                    matchImages = self.deleteMatchImage(matchImages)
                case 'Update':
                    matchImages = self.updateMatchImage(matchImages)
                case 'Check':
                    self.checkMatchImages(matchImages)
                case 'Back':
                    return
                case _:
                    return
            self.saveMatchImages(matchImages)

    def checkMatchImages(self, matchImages):
        stopppedName = False
        while not stopppedName:
            name = getMenus("Check Match Image ", getMenusElements(names=list(matchImages.keys()) + ["Back"]))
            if name == "Back" or name == "": return matchImages
            print(f'{name} : {self.game.dpc.checkImageMatch(name)}')
            sleep(2)

    def saveMatchImages(self, matchImages):
        toJson('matchImages', matchImages, 'json_data/')
        self.game.dpc.loadMatchImages()

    def deleteMatchImage(self, matchImages):
        stopped = False
        while not stopped:
            name = getMenus("Delete Match Image ", getMenusElements(names=list(matchImages.keys()) + ["Back"]))
            if name == "Back" or name == "": return matchImages
            os.rmdir(f"img/{name}")
            del matchImages[name]
        return matchImages

    def updateMatchImage(self, matchImages):
        stoppedName = False
        while not stoppedName:
            name = getMenus("Update: Select Match Image", getMenusElements(names=list(matchImages.keys()) + ["Back"]))
            if name == "Back" or name == "": return matchImages
            stopped = False
            while not stopped:
                response = getMenus(f"Update Match Image {name}", getMenusElements(names=[
                    "Add Image",
                    "Delete",
                    "Back"
                ]))
                match response:
                    case 'Add Image':
                        matchImages = self.addMatchImage(matchImages, name)
                    case 'Delete':
                        matchImages = self.deleteImageOfMatchImage(matchImages, name)
                    case 'Back':
                        stopped = True
                    case _:
                        stopped = True
                self.saveMatchImages(matchImages)
        return matchImages

    def addMatchImage(self, matchImages, name):
        match = matchImages[name]
        print('Click on the top left corner  and then the bottom right corner of the image in a region or root window')
        self.clicks = []
        stopped = False
        while not stopped:
            newRegion = self.getRectangle()
            if newRegion is not None:
                img = getImgRectangle(self.game.regions.applyRegion(newRegion['region']), newRegion)
                path = f"img/{name}/"
                fullPath = path + f"{len(match)}.png"
                # create directory if not exists

                cv2.imwrite(fullPath, img)
                match.append({"region": newRegion['region'], "path": fullPath})
                matchImages[name] = match
                return matchImages
            sleep(0.01)
        return matchImages

    def deleteImageOfMatchImage(self, matchImages, name):
        stopped = False
        while not stopped:
            params = {image['path']: f"{image['region']}" for image in matchImages[name]}
            imagePath = getMenus("Delete Image", getMenusElements(obj=params, names=["Back"]))
            if imagePath == "Back" or imagePath == "": return matchImages
            for idx, image in enumerate(matchImages[name]):
                if image['path'] == imagePath:
                    os.remove(imagePath)
                    del matchImages[name][idx]
        return matchImages

    def updateRegion(self, regions):
        nameStopped = False
        while not nameStopped:
            configRegions = [{"name": regionName, "value": idx} for idx, regionName in enumerate(regions)]
            name = getMenus("Update Regions", getMenusElements(names=list(regions.keys()) + ["Back"]))
            if name in ("Back", ""): return;
            region = regions[name]
            stopped = False
            while not stopped:

                response = getMenus(f"Edit Regions {name}", getMenusElements(obj=region, names=["Back"]))
                if response == "Back" or response == "":
                    stopped = True
                    break
                for key in region.keys():
                    if response == key:
                        updateValueOfKey(region, key, int if key != "ratio" else float)
                        break

                regions[name] = region
                self.saveRegion(regions)
                self.game.toggleFreeze(double=True)

    def saveRegion(self, regions):
        toJson('region', regions, 'json_data/')
        self.game.regions.dict = regions
        self.game.cv2Controller.refreshRegion = True

    def deleteRegion(self, regions):
        stopped = False
        while not stopped:
            name = getMenus("Delete Regions", getMenusElements(names=list(regions.keys()) + ["Back"]))
            if name == "Back" or name == "": return regions
            del regions[name]
            self.saveRegion(regions)
            self.game.toggleFreeze(double=True)

    def addNewRegion(self, regions):
        stopped = False
        name = input('Enter region name: ')
        while name in regions or name == "":
            if name == "":
                return
            print('Regions name already exists, please enter a new name')
            name = input('Enter region name: ')
        ratio = float(input('Enter ratio: '))
        print('Click on the top left corner  and then the bottom right corner of the region in the root window')
        self.clicks = []
        while not stopped:
            newRegion = self.getRectangle()
            if newRegion is not None:
                newRegion['ratio'] = ratio
                regions[name] = newRegion
                self.saveRegion(regions)
                self.game.toggleFreeze(double=True)
                return
            sleep(0.01)

    def configRegion(self):
        regions = getJson('region')
        stopped = False
        while not stopped:
            response = getMenus("Regions", getMenusElements(names=["New", "Update", "Delete", "Back"]))
            match response:
                case 'Update':
                    self.updateRegion(regions)
                case 'New':
                    self.addNewRegion(regions)
                case 'Delete':
                    self.deleteRegion(regions)
                case 'Back':
                    return
                case _:
                    return

    def configWindow(self):
        windowConfig = getJson('window')
        stopped = False
        while not stopped:
            response = getMenus(f"Edit Window", getMenusElements(obj=windowConfig, names=["Back"]))
            print(response)
            if response in ("Back", ""): return;
            for key in windowConfig.keys():
                if response == key:
                    updateValueOfKey(windowConfig, key)
                    break
            toJson('window', windowConfig, 'json_data/')
            self.game.wc.loadConfig()
            self.game.toggleFreeze(double=True)
