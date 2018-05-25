import random

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

line_bot_api = LineBotApi('G4WumVD0m/ro9kCBsWl2/68YzTgzLrS5tMQDIe02gHhwJ62eqy/BN9EUKX8F4V6RmcySsnZPxl+/QzikfXQwg2iH+AC25wheupPotxQ8m+u3N+Srz0lfYVwJ1xMh8kA1wm9Pavra0QYNoGc7VDh6yAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d83d5a73c4ac43b5f6dd5a09d4c7c39f')

breakfast_list = ['美式早午餐','樂活堡','麥味登','萊客堡','萊姆斯','摩斯漢堡']
lunch_list = ['歐姆萊斯','白屋','紅油抄手','滿食記','田園美食屋']
dinner_list = ['歐姆萊斯','白屋','紅油抄手','滿食記','田園美食屋']
drink_list = ['夏克緹','立橙','清心','ifresh','花茶大師']

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
    
    if '推薦' in event.message.text and '早餐' in event.message.text:
        breakfast_list.add(event.message.text)
        message = TextSendMessage('感謝大大分享')
    elif '早餐' in event.message.text:
        ran = random.randint(0,len(breakfast_list)-1)
        #message = TextSendMessage(text=breakfast_list[ran])
        message = TextSendMessage(text=str(breakfast_list))
    elif '午餐' in event.message.text:
        ran = random.randint(0,len(lunch_list)-1)
        message = TextSendMessage(text=lunch_list[ran])
    elif '晚餐' in event.message.text:
        ran = random.randint(0,len(dinner_list)-1)
        message = TextSendMessage(text=dinner_list[ran])
    elif '飲料' in event.message.text:
        ran = random.randint(0,len(drink_list)-1)
        message = TextSendMessage(text=drink_list[ran])
    else:
        message = TextSendMessage(text='搜尋地區美食請輸入: [地區](早.午.晚.宵夜)餐')
    
    line_bot_api.reply_message(event.reply_token,message)
        
if __name__ == "__main__":
	app.run()
