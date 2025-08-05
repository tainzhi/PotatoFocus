import json5
from typing import Dict, Any
from util import SETTINGS_FILE

class Settings:
    
    def __init__(self):
        self.settings_path = SETTINGS_FILE
        self.settings: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        if self.settings_path.exists():
            with open(self.settings_path, 'r') as f:
                self.settings = json5.load(f) #type: ignore
        # print(f"Settings load settings: {self.settings}")


    def save(self):
        # print(f"Settings save settings: {self.settings}")
        with open(self.settings_path, 'w') as f:
            json5.dump(self.settings, f) #type: ignore
    
    def getWorkTimeInMinue(self) -> int:
        return self.settings.get("work_time_in_minute", 25)
    
    def setWorkTimeInMinue(self, value: int):
        # print(f"Settings setWorkTimeInMinue: {value}")
        self.settings["work_time_in_minute"] = value
    
    def getBreakTimeInMinue(self) -> int:
        return self.settings.get("break_time_in_minute", 5)
    
    def setBreakTimeInMinue(self, value: int):
        self.settings["break_time_in_minute"] = value
    
    # 是否在休息后继续工作
    def getContinuousWorkAfterBreak(self) -> bool:
        return self.settings.get("continuous_work_after_break", False)
    
    def setContinuousWorkAfterBreak(self, value: bool):
        self.settings["continuous_work_after_break"] = value
        
        # 默认连续工作4个番茄钟之后，长时间休息
    def getContinuousWorkCount(self) -> int:
        return self.settings.get("continuous_work_count", 4)
    
    def setContinuousWorkCount(self, value: int):
        self.settings["continuous_work_count"] = value
        
    def getLongBreakTimeInMinue(self) -> int:
        return self.settings.get("long_break_time_in_minute", 15)
    
    def setLongBreakTimeInMinue(self, value: int):
        self.settings["long_break_time_in_minute"] = value
    
    def getUseImageDownloadedFromPixabay(self) -> bool:
        return self.settings.get("use_image_downloaded_from_pixabay", True)
    
    def setUseImageDownloadedFromPixabay(self, value: bool):
        self.settings["use_image_downloaded_from_pixabay"] = value
    
    def getPixabayApiKey(self) -> str:
        return self.settings.get("pixabay_api_key", "")
    
    def setPixabayApiKey(self, value: str):
        self.settings["pixabay_api_key"] = value
    
    def getPixabayMostUsedPerImage(self) -> int:
        return self.settings.get("pixabay_most_used_per_image", 10)
    
    def setPixabayMostUsedPerImage(self, value: int):
        self.settings["pixabay_most_used_per_image"] = value