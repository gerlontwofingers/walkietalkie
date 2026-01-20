from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import requests
import torch
from urllib.parse import urlparse

class GetImage:
    def __init__(self, path: str):
        self.path = path
        self.image = self._get_image()
    
    def _is_url(self):
        return urlparse(self.path).scheme != ""
    
    def _get_image(self):
        if self._is_url():
            return Image.open(requests.get(self.path, stream=True).raw).convert("RGB")
        else:
            return Image.open(self.path).convert("RGB")

class Captionator:
    def __init__(self):
        pass
    
    def initialize(self):
        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b", use_fast=True)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b",
            dtype=torch.float16
        )
        self.model.to("cuda" if torch.cuda.is_available() else "cpu")
    
    def get_caption(self, image: Image):
        inputs = self.processor(images=image, return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(**inputs)
        return self.processor.decode(generated_ids[0], skip_special_tokens=True)

    def query(self, image: Image, query: str) -> str:
        # prompt = "Question: What is a dinosaur holding? Answer:"
        inputs = self.processor(image, text=query, return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(**inputs, max_new_tokens=10)
        return self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        # print(generated_text)

