from imaginepy import AsyncImagine, Style, Ratio
import telebot
from background import keep_alive
import os, json
from gpt import GPT
from concurrent.futures import ThreadPoolExecutor
import asyncio
from deep_translator import GoogleTranslator

# Створюємо екземпляр бота з використанням токену
token = os.environ['token']
bot = telebot.TeleBot(token)
llm = GPT()


# Функція для перекладу повідомлення
def translate_message(message, target_language):
  try:
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_message = translator.translate(message)
    return translated_message
  except Exception as e:
    print(e)
    return message


# Описуємо обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
  user_language = message.from_user.language_code
  bot.send_message(
    message.chat.id,
    translate_message("Welcome! Please, enter your prompt:", user_language))


# Описуємо обробник введення промпта
@bot.message_handler(
  func=lambda message: message.chat.id == message.from_user.id)
def generate_image(message):
  # Отримуємо вибраний тип зображення та розмір для поточного користувача
  prompt = message.text
  user_language = message.from_user.language_code

  ratio_mapping = {
    "1x1": Ratio.RATIO_1X1,
    "9x16": Ratio.RATIO_9X16,
    "16x9": Ratio.RATIO_16X9,
    "4x3": Ratio.RATIO_4X3,
    "3x2": Ratio.RATIO_3X2,
    "2x3": Ratio.RATIO_2X3,
    "5x4": Ratio.RATIO_5X4,
    "4x5": Ratio.RATIO_4X5,
    "3x1": Ratio.RATIO_3X1,
    "3x4": Ratio.RATIO_3X4
  }

  async def generate_image_sync():
    img_data = None
    bot.send_message(
      message.chat.id,
      translate_message("Your image is generating, please wait.",
                        user_language))
    try:
      image_json = json.loads(llm.GetAnswer(prompt=prompt))
      image_size = image_json["image_size"]
      gpt_prompt = image_json["prompt"]
      type = image_json["type"]
    except:
      bot.send_message(
        message.chat.id,
        translate_message(
          "Sorry, gpt-4 doesn't understand your prompt. Please change your question.",
          user_language))
      return
    try:
      if image_json["image_size"] not in ratio_mapping:
        bot.send_message(
          message.chat.id,
          translate_message(
            "Error with image ratio. Available ratios: 1x1, 16x9, 9x16, 4x3, 3x2",
            user_language))
        return
      imagine = AsyncImagine(style=eval(f"""Style.{type}"""))
      img_data = await imagine.sdprem(prompt=gpt_prompt,
                                style=eval(f"""Style.{type}"""),
                                ratio=ratio_mapping[image_size])
    except:
      imagine = AsyncImagine(style=Style.ANIME_V2)
      img_data = await imagine.sdprem(prompt=gpt_prompt,
                                style=Style.ANIME_V2,
                                ratio=ratio_mapping[image_size])

    if img_data is None:
      bot.send_message(
        message.chat.id,
        translate_message("Failed to create your image. Bot will be updated in two-three days. Please wait, sorry.",
                          user_language))
      return

    img_data = await imagine.upscale(image=img_data)

    if img_data is None:
      bot.send_message(
        message.chat.id,
        translate_message("An error occurred while upscaling the image.",
                          user_language))
      return
    
    await imagine.close()

    try:
      bot.send_photo(message.chat.id, photo=img_data)
    except Exception as e:
      print(e)
      bot.send_message(
        message.chat.id,
        translate_message("An error occurred while sending the image.",
                          user_language))
  
  asyncio.run(generate_image_sync())


# Запускаємо бота
keep_alive()
bot.polling(non_stop=True, interval=0)
