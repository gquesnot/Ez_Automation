class HsvFilter:

    def __init__(self, hMin=0, sMin=0, vMin=0, hMax=0, sMax=0, vMax=0,
                 sAdd=0, sSub=0, vAdd=0, vSub=0, cannyOn=0, cannyKernel=0, cannyRatio=0, maxThreshold=0, lowThreshold=0,
                 blurOn=0, blurKernel=0, BlurRatio=0, r=10, g=10, b=50, datas=None):
        self.HMin = hMin
        self.SMin = sMin
        self.VMin = vMin
        self.HMax = hMax
        self.SMax = sMax
        self.VMax = vMax
        self.SAdd = sAdd
        self.SSub = sSub
        self.VAdd = vAdd
        self.VSub = vSub
        self.CannyOn = cannyOn
        self.CannyKernel = cannyKernel
        self.CannyRatio = cannyRatio
        self.MaxThreshold = maxThreshold
        self.LowThreshold = lowThreshold
        self.BlurOn = blurOn
        self.BlurKernel = blurKernel
        self.BlurRatio = BlurRatio
        self.R = r
        self.G = g
        self.B = b
        if datas is not None:
            for k, v in datas.items():
                setattr(self, k, v)
