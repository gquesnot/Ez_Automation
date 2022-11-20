import os
from time import sleep, time
from typing import Any

import cv2
import numpy as np
from termcolor import colored

from util.threadclass import ThreadClass


class IA(ThreadClass):
    yolo_dir = ""
    confidence = 0.6
    threshold = 0.4
    region: str = "base"
    labels = []
    net: Any = None
    model: Any = None
    ln: Any = None
    game: 'Game' = None
    img: Any = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.yolo_dir = os.path.join("ia", "models")
        with open(os.path.join(self.yolo_dir, "coco-dataset.labels"), 'r') as f:
            self.labels = f.read().splitlines()
            self.colors = np.random.randint(0, 255, size=(len(self.labels), 3),
                                            dtype="uint8")
        self.weights_path = os.path.join(self.yolo_dir, "yolov4-tiny.weights")
        self.config_path = os.path.join(self.yolo_dir, "yolov4-tiny.cfg")
        self.load_model()
        self.check_gpu()
        sleep(0.4)

        # self.checkGpu()

    def parse_outputs(self, layer_outputs):
        boxes = []
        confidences = []
        class_i_ds = []
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                label = self.labels[class_id]
                if confidence > self.confidence:
                    box = detection[0:4] * np.array([self.img.shape[1], self.img.shape[0], self.img.shape[1],
                                                     self.img.shape[0]])
                    (center_x, center_y, width, height) = box.astype("int")
                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_i_ds.append(class_id)
        return class_i_ds, confidences, boxes

    def run(self):
        region = self.game.regions.get_region(self.region)
        while not self.stopped:
            t = time()
            if self.game.screen_shot is not None and not self.game.screen_shot.size == 0:

                self.img = self.game.get_screenshot_copy()
                if region is not None:
                    self.img = self.game.regions.apply_region(self.region, screenshot=self.img)

                mat = cv2.UMat(self.img)

                blob = cv2.dnn.blobFromImage(mat, 1 / 255, (416, 416),
                                             swapRB=True)

                self.net.setInput(blob)
                layer_outputs = self.net.forward(self.ln)
                class_ids, scores, boxes = self.parse_outputs(layer_outputs)

                # classIds, scores, boxes = self.model.detect(self.img, confThreshold=self.confidence, nmsThreshold=self.threshold)
                # print(classIds, scores, boxes)
                if len(class_ids) > 0:

                    for i in range(len(boxes)):
                        box = boxes[i]
                        class_id = class_ids[i]
                        score = scores[i]
                        cv2.rectangle(self.img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                                      color=(0, 255, 0), thickness=2)
                        print(class_id, self.labels[class_id], score)
                        text = '%s: %.2f' % (self.labels[class_id], score)
                        cv2.putText(self.img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    color=(0, 255, 0), thickness=2)
                self.game.im_save.update('draw_img', self.img)
            if t - time() != 0:
                print('FPS: %.2f' % (1 / (time() - t)))
            sleep(0.01)

    def set_region(self, hint):
        self.region = hint

    def load_model(self):
        """
        Load the model
        """
        print(self.yolo_dir, self.weights_path, self.config_path)
        # list dir in yoloDir
        print(os.listdir(self.yolo_dir))
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
        # self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
        # self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
        # self.model = cv2.dnn_DetectionModel(self.net)
        # self.model.setInputParams(size=(416,416), scale=1 / 255, swapRB=True)

        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def check_gpu(self):
        """
        Check if the GPU is available
        """
        build_info = str("\n".join(cv2.getBuildInformation().split()))
        # print(cv2.getBuildInformation())
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
