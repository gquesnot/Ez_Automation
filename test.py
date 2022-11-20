from baseclass.my_dataclass.pixel_config import PixelConfigs
from baseclass.my_dataclass.region_config import RegionConfigs
from util.json_function import get_json

regions = RegionConfigs.from_dict(get_json("regions"))

pixels = PixelConfigs.from_dict(get_json("pixels"))
print(pixels)
datas = pixels
datas.get('evt1On').pixels.pop()
print(pixels)
print(datas)
