import sys
import re

class PromptNormalizer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {"default": "", "multiline": True}),
                "remove_comma": ("BOOLEAN", {"default": False,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)

    FUNCTION = "execute"
    CATEGORY = "StringUtils"

    def execute(self, string, remove_comma):
        result = re.sub("(//.*|#.*)", "", string, flags=re.MULTILINE)
        result = re.sub("(\r\n|\n|\r)", " ", result, flags=re.MULTILINE)
        result = re.sub("/\*.*?\*/", "", result, flags=re.MULTILINE)
        result = re.sub("(  +)", " ", result, flags=re.MULTILINE)
        result = re.sub("(^ +| +$)", "", result, flags=re.MULTILINE)
        result = re.sub("(,$)", "", result, flags=re.MULTILINE)
        if remove_comma:
            result = re.sub("(,)", "", result, flags=re.MULTILINE)
        return (result,)


class StringSplitter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {"default": "", "multiline": True,}),
                "delimiter": ("STRING", {"default": "",}),
                "remove_last_comma": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING","INT",)
    RETURN_NAMES = ("STRING","Count",)
    OUTPUT_IS_LIST = (False,False,)

    FUNCTION = "execute"
    CATEGORY = "StringUtils"

    def execute(self, string, delimiter, remove_last_comma):
        lines = string.split(delimiter)
        result = ""
        for line in lines:
            str = re.sub("(^ +| +$)", "", line, flags=re.MULTILINE)
            if remove_last_comma:
                str = re.sub("(,$)", "", str, flags=re.MULTILINE)
            result += str + "\n"

        return (result, len(lines),)


class StringSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "string": ("STRING", {"default": "", "multiline": True,}),
            "line_num": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1,}),
        }}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    CATEGORY = "StringUtils"

    def execute(self, string, line_num):
        lines = string.split('\n')
        selected = ""

        if len(lines) == 0:
            selected = string
        else:
            selected = lines[line_num % len(lines)]

        return (selected, )


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "PromptNormalizer": PromptNormalizer,
    "StringSplitter": StringSplitter,
    "StringSelector": StringSelector,
}


# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptNormalizer": "Prompt Normalizer",
    "StringSplitter": "String Splitter",
    "StringSelector": "String Line Selector"
}
