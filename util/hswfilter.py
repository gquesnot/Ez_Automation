class HsvFilter:

    def __init__(self, h_min=0, s_min=0, v_min=0, h_max=0, s_max=0, v_max=0,
                 s_add=0, s_sub=0, v_add=0, v_sub=0, canny_on=0, canny_kernel=0, canny_ratio=0, max_threshold=0,
                 low_threshold=0,
                 blur_on=0, blur_kernel=0, blur_ratio=0, r=10, g=10, b=50, datas=None):
        self.h_min = h_min
        self.s_min = s_min
        self.v_min = v_min
        self.h_max = h_max
        self.s_max = s_max
        self.v_max = v_max
        self.s_add = s_add
        self.s_sub = s_sub
        self.v_add = v_add
        self.v_sub = v_sub
        self.canny_on = canny_on
        self.canny_kernel = canny_kernel
        self.canny_ratio = canny_ratio
        self.max_threshold = max_threshold
        self.low_threshold = low_threshold
        self.blur_on = blur_on
        self.blur_kernel = blur_kernel
        self.blur_ratio = blur_ratio
        self.R = r
        self.G = g
        self.B = b
        if datas is not None:
            for k, v in datas.items():
                setattr(self, k, v)
