from baseclass.my_dataclass.pixel_config import PixelConfigs
from baseclass.my_dataclass.region_config import RegionConfigs
from util.json_function import getJson

regions = RegionConfigs.from_dict(getJson("regions"))

pixels = PixelConfigs.from_dict(getJson("pixels"))
print(pixels)
datas = pixels
datas.get('evt1On').pixels.pop()
print(pixels)
print(datas)
