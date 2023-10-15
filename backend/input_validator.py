from pydantic import BaseModel, field_validator, model_validator
from typing import List, Dict

class InputSetting(BaseModel):
    mode: str
    box_prompt: List
    text_prompt: str
    point_prompt: List
    point_label: List

    @field_validator("mode")
    def method_is_valid(cls, method: str) -> str:
        allowed_set = {"everything", "box", "text", "points"}
        if method not in allowed_set:
            raise ValueError(f"must be in {allowed_set}, got '{method}'")
        return method

    @model_validator(mode='before')
    def model_is_valid(cls, values: Dict) -> Dict:
        mode = values.get("mode")
        box_prompt = values.get("box_prompt")
        text_prompt = values.get("text_prompt")
        point_prompt = values.get("point_prompt")
        point_label = values.get("point_label")
        if mode == "box":
            if len(box_prompt) < 4:
                raise ValueError(f"Invalid box_prompt {box_prompt}")
            else:
                for ele in box_prompt:
                    if ele < 0 or ele > 1:
                        raise ValueError(f"Invalid box_prompt {box_prompt}")
                # Check for correct bounding boxes
        elif mode == "text":
            if len(text_prompt) <= 0:
                raise ValueError(f"Invalid text_prompt {box_prompt}")
        elif mode == "points":
            if len(point_prompt) != len(point_label):
                raise ValueError(f"Point_prompt and point_label length does not match")
            # Check values in point_label (skip)
            # Check values in point_prompt (skip)
        return values