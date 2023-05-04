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

app = Flask(__name__)

line_bot_api = LineBotApi('tuJK6H6vmCfza8sfGG8ARXxxkeFxLKuBJxua+Ucg9IbJi+hM/0aw0KyNWgepqZVVSHmMLQmJXn0jxIJW0O1deku1tuQUMPx7BHJgQ7l4Ci1rRATFSD+5pGfmMYf35BVcNbYbCPEwiScJQ4HJ/vqGAgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('72fb67decf0b6155beac93cfe8bd50bb')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()