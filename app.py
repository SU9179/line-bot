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

line_bot_api = LineBotApi('tg3RN7iVlsXh/n8OaoS2t2AjrX8jviQ7jblf3WgMIvlmvsfxYE7iYyFLBisPu3gqTNWxNprXfyjNfHFB1fB2UweuH2/uvVbUC+8ZvnXABC7FHVovhuM88qoJrkASuaEH8Al8A0fz2L5k9zRozBmtPQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a3b366d834d6e87daf5c66826093255e')


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