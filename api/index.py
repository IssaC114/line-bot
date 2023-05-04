import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import openai

app = Flask(__name__)

line_bot_api = LineBotApi('tuJK6H6vmCfza8sfGG8ARXxxkeFxLKuBJxua+Ucg9IbJi+hM/0aw0KyNWgepqZVVSHmMLQmJXn0jxIJW0O1deku1tuQUMPx7BHJgQ7l4Ci1rRATFSD+5pGfmMYf35BVcNbYbCPEwiScJQ4HJ/vqGAgdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('72fb67decf0b6155beac93cfe8bd50bb')

openai.api_key = os.environ("OPENAI_API_KEY")
input_text = "今天天氣很好，請用中文回答。請做一首跟天氣有關的詩"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 50

@app.route("/")
def home():
    return "LINE BOT is running."

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)),
        max_tokens=output_length,
    )
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()