# インポートするライブラリ
import os
import re 
from random import randint

from flask import Flask, request, abort
from linebot import (
   LineBotApi, WebhookHandler
)

from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__) 
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"] 
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/test", methods=['GET', 'POST'])
def test():
    return 'I\'m alive!'

@app.route("/callback", methods=['POST'])
def callback():
   signature = request.headers['X-Line-Signature']
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    入力の変数の定義
    '''
    input_line = event.message.text

    '''
    主機構
    '''
    if re.fullmatch(r'(@|＠)すごろく', input_line):
        sugoroku_num = randint(3,8)
        output_line = "出た目は「{}」です！\n頑張ってください！🚌💨".format(sugoroku_num)
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=output_line)
                    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
