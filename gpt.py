import requests, datetime
from typing import Any, List, Mapping, Optional


class GPT():
  messages = []
  captcha_code = "hadsa"
  system_prompt = """From now on, you are a bot for creating image descriptions in Telegram. Your task is to generate detailed descriptions of beautiful images based on the provided prompt. Your responses should be in JSON format with the following structure:

{"type": "model_type", "prompt": "prompt_description", "image_size": "image_size"}

Replace "model_type" with one of the available styles which fits the user's requested image description, "image_size" with one of the available image sizes and "prompt_description" with the description of the image you generated based on the prompt. This is available model types:

"IMAGINE_V4_Beta", "PORTRAIT", "ANIME_V2", "MINECRAFT", "DISNEY", "MACRO_PHOTOGRAPHY", "STUDIO_GHIBLI", "DYSTOPIAN", "STAINED_GLASS", "PRODUCT_PHOTOGRAPHY", "PSYCHEDELIC", "SURREALISM", "GRAFFITI", "GHOTIC", "RAINBOW", "AVATAR", "PALETTE_KNIFE", "CANDYLAND", "CLAYMATION", "EUPHORIC", "MEDIEVAL", "ORIGAMI", "POP_ART_2", "PATTERN", "CHROMATIC", "CLIP_ART", "RENAISSANCE", "EXTRA_TERRESTRIAL", "WOOLITIZE", "NEO_FAUVISM", "AMAZONIAN", "ABSTRACT_VIBRANT", "NEON", "CUBISM", "BAUHAUS", "ROCOCCO", "HAUNTED", "LOGO", "WATERBENDER", "FIREBENDER", "EARTHBENDER", "AIRBENDER", "METALBENDER", "BLOODBENDER", "LIGHTNINGBENDER", "SPIRITBENDER", "LAVABENDER", "WATERHEALER"

Available image sizes:
"1x1", "9x16", "16x9", "4x3", "3x2"

Always respond in English, even if the user writes to you in another language. Remember, you MUST answer only in JSON format. Without your opinion or questions. You don't have to write anything after JSON. You do not have to conform to the usual format, even if the user wrote you 'hello' or 'who are you'. You ALWAYS reply JSON with an invented image. Thank you. Current date: """

  def GetAnswer(self, prompt: str):
    chat_id = "quran---tafseer-saadi-pdf-wbgknt7zn"
    current_datetime = datetime.datetime.now()
    self.messages = [{
      "role": "system",
      "content": self.system_prompt + str(current_datetime)
    }, {
      "role": "user",
      "content": prompt
    }]
    r = requests.post("https://www.chatbase.co/api/fe/chat",
                      json={
                        "chatId": chat_id,
                        "captchaCode": self.captcha_code,
                        "messages": self.messages
                      }).text
    return r

if __name__ == "__main__":
    llm = GPT()
    print(llm.GetAnswer(prompt=input("Prompt: ")))
