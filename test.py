import json

from app.my_dataclasses import WindowConfig, RegionConfigs, ImageMatchConfigs, PixelConfigs, PixelConfigType, \
    TcrScanConfigs, MaskDetectionConfig, ActionConfigs, MaskDetectionConfigs
from util.json_function import getJson

regions = RegionConfigs.from_dict(getJson("regions"))

pixels = PixelConfigs.from_dict(getJson("pixels"))
print(pixels)
datas = pixels
datas.get('evt1On').pixels.pop()
print(pixels)
print(datas)
