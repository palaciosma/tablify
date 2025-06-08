# Internal imports
from .extractor import openai_ext, deepseek_ext
from .analyzer import deepseek_analyzer


PROCESSOR_REGISTRY = {
    "extract": deepseek_ext,
    "analyze": deepseek_analyzer
}