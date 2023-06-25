import requests, datetime

class GPT():
  def __init__(self, debug: bool = False):
    self.debug = debug
  messages = []
  captcha_code = "hadsa"
  system_prompt = """From now on, you are a bot for creating image descriptions in Telegram. Your task is to generate detailed descriptions of beautiful images based on the provided prompt. Your responses should be in JSON format with the following structure:

{"type": "model_type", "prompt": "prompt_description", "image_size": "image_size"}

Replace "model_type" with one of the available model types, "image_size" with one of the available image sizes and "prompt_description" with the description of the image you generated based on the prompt. 
The description should describe the image as fully as possible. Do not use country names, or anything specific, you should describe it, for example, if you need to make a description of the image with a flag, then you should not say the name of the country, but describe the colors of the flag.
Use only available model types. Even if the user asks to use some other type, you should still use only the available model types that are written in this message.

Available model types:
"PORTRAIT", "ANIME_V2", "MINECRAFT", "DISNEY", "MACRO_PHOTOGRAPHY", "STUDIO_GHIBLI", "DYSTOPIAN", "STAINED_GLASS", "PRODUCT_PHOTOGRAPHY", "PSYCHEDELIC", "SURREALISM", "GRAFFITI", "GHOTIC", "RAINBOW", "PALETTE_KNIFE", "CANDYLAND", "CLAYMATION", "ORIGAMI", "POP_ART_2", "CHROMATIC", "CLIP_ART", "RENAISSANCE", "EXTRA_TERRESTRIAL", "WOOLITIZE", "NEO_FAUVISM", "AMAZONIAN", "ABSTRACT_VIBRANT", "NEON", "CUBISM", "BAUHAUS", "ROCOCCO", "HAUNTED", "LOGO", "WATERBENDER", "FIREBENDER", "EARTHBENDER", "AIRBENDER", "METALBENDER", "BLOODBENDER", "LIGHTNINGBENDER", "SPIRITBENDER", "LAVABENDER", "WATERHEALER"

Available image sizes:
"1x1", "9x16", "16x9", "4x3", "3x2", "2x3", "5x4", "4x5", "3x1", "3x4"


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
    if self.debug:
      print(r)
    return r

if __name__ == "__main__":
    llm = GPT()
    print(llm.GetAnswer(prompt=input("Prompt: ")))
