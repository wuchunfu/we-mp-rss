
import os
from core.config import cfg
if cfg.get("WERSS_AUTH_WEB", "") == True:
    from driver.wx import WX_API 
else:
    from driver.wx_api import WeChat_api as WX_API