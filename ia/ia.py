import os
from time import sleep, time
from typing import Any

import cv2
import numpy as np
from termcolor import colored

from util.threadclass import ThreadClass


class IA(ThreadClass):
    yoloDir = ""
    confidence = 0.6
    threshold = 0.4
    region: str = "base"
    labels = []
    net: Any = None
    model: Any = None
    ln: Any=  None
    game: 'Game' = None
    img: Any = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.yoloDir = os.path.join("ia", "models")
        with open(os.path.join(self.yoloDir, "coco-dataset.labels"), 'r') as f:
            self.labels = f.read().splitlines()
            self.colors = np.random.randint(0, 255, size=(len(self.labels), 3),
                                            dtype="uint8")
        self.weightsPath = os.path.join(self.yoloDir, "yolov4-tiny.weights")
        self.configPath = os.path.join(self.yoloDir, "yolov4-tiny.cfg")
        self.loadModel()
        self.checkGpu()
        sleep(0.4)

        #self.checkGpu()


    def parseOutputs(self, layerOutputs):
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                label = self.labels[classID]
                if confidence > self.confidence:
                    box = detection[0:4] * np.array([self.img.shape[1], self.img.shape[0], self.img.shape[1],
                                                     self.img.shape[0]])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        return classIDs, confidences, boxes

    def run(self):
        region = self.game.regions.getRegion(self.region)
        while not self.stopped:
            t = time()
            if self.game.screenShot is not None and not self.game.screenShot.size == 0:

                self.img = self.game.getScreenshotCopy()
                if region is not None:
                    self.img = self.game.regions.applyRegion(self.region, screenshot=self.img)


                mat  = cv2.UMat(self.img)

                blob = cv2.dnn.blobFromImage(mat, 1 / 255, (416, 416),
                                             swapRB=True)

                self.net.setInput(blob)
                layerOutputs = self.net.forward(self.ln)
                classIds, scores, boxes = self.parseOutputs(layerOutputs)

                #classIds, scores, boxes = self.model.detect(self.img, confThreshold=self.confidence, nmsThreshold=self.threshold)
                #print(classIds, scores, boxes)
                if len(classIds) > 0:

                    for i in range(len(boxes)):

                        box = boxes[i]
                        classId = classIds[i]
                        score= scores[i]
                        cv2.rectangle(self.img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                                      color=(0, 255, 0), thickness=2)
                        print(classId, self.labels[classId], score)
                        text = '%s: %.2f' % (self.labels[classId], score)
                        cv2.putText(self.img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    color=(0, 255, 0), thickness=2)
                self.game.imSave.update('draw_img', self.img)
            if t - time() != 0:
                print('FPS: %.2f' % (1 / (time() - t)))
            sleep(0.01)



    def setRegion(self, hint):
        self.region = hint

    def loadModel(self):
        """
        Load the model
        """
        print(self.yoloDir, self.weightsPath, self.configPath)
        #list dir in yoloDir
        print(os.listdir(self.yoloDir))
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        #self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
        #self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
        #self.model = cv2.dnn_DetectionModel(self.net)
        #self.model.setInputParams(size=(416,416), scale=1 / 255, swapRB=True)

        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]



    def checkGpu(self):
        """
        Check if the GPU is available
        """
        build_info = str("\n".join(cv2.getBuildInformation().split()))
        #print(cv2.getBuildInformation())
        if cv2.ocl.haveOpenCL():
            print(colored("[OKAY] OpenCL is working!", "green"))
        else:
            print(
                colored("[WARNING] OpenCL acceleration is disabled!", "yellow"))
        if "CUDA:YES" in build_info:
            print(colored("[OKAY] CUDA is working!", "green"))
        else:
            print(
                colored("[WARNING] CUDA acceleration is disabled!", "yellow"))
