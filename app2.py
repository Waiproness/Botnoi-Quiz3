from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    PostbackAction, MessageAction, URIAction,
    QuickReply, QuickReplyButton, CameraAction,
    CarouselTemplate, CarouselColumn
)

app = Flask(__name__)

# --- ใส่ค่า Key ของคุณตรงนี้ ---
CHANNEL_ACCESS_TOKEN = 'KqWz9VIdMHSSqP7g8BQJ4Rp1fOsTptezMoBcQLPx8Nyb7oe0ckg0s+eIxxwVuz4k7U7bmZkzZckST/uvyvwkl/6kVZVpMjJQOKre78NZ14yle+mySPqPjGocCOn8Ixn2j+0n5TTVvt2gk7D5egeATAdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'c0ee0445757470abdd63b6c4004876cb'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST']) 
def callback():
    # รับค่า Signature เพื่อตรวจสอบความปลอดภัย
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# --- ฟังก์ชันตอบกลับเมื่อมีข้อความเข้า ---
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_from_user = event.message.text.lower().strip() # แปลงเป็นตัวพิมพ์เล็ก

    # 1. ตอบกลับแบบ Text
    if text_from_user == "text":
        reply_msg = TextSendMessage(text="สวัสดีครับ! นี่คือข้อความธรรมดา")
        line_bot_api.reply_message(event.reply_token, reply_msg)

    # 2. ตอบกลับแบบ Button (Template)
    elif text_from_user == "button":
        buttons_template = TemplateSendMessage(
            alt_text='นี่คือ Button Template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://via.placeholder.com/1024x1024.png?text=Button',
                title='เมนูเลือกได้',
                text='กรุณาเลือกรายการ',
                actions=[
                    MessageAction(label='บอกรัก', text='รักนะ'),
                    URIAction(label='เปิด Google', uri='https://google.com')
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    # 3. ตอบกลับแบบ Quick Reply (ปุ่มลอยข้างล่าง)
    elif text_from_user == "quick":
        quick_reply_msg = TextSendMessage(
            text="เลือกเมนูด่วนได้เลย!",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="สวัสดี", text="สวัสดี")),
                    QuickReplyButton(action=CameraAction(label="ถ่ายรูป")),
                    QuickReplyButton(action=MessageAction(label="บอทเก่งไหม", text="เก่งมาก"))
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, quick_reply_msg)

    # 4. ตอบกลับแบบ Carousel (สไลด์ด้านข้าง)
    elif text_from_user == "carousel":
        carousel_template = TemplateSendMessage(
            alt_text='นี่คือ Carousel',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://via.placeholder.com/1024x1024.png?text=Item1',
                        title='สินค้าชิ้นที่ 1',
                        text='รายละเอียดสินค้า 1',
                        actions=[
                            MessageAction(label='ซื้อชิ้นที่ 1', text='ซื้อ 1'),
                            URIAction(label='ดูรายละเอียด', uri='https://google.com')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://via.placeholder.com/1024x1024.png?text=Item2',
                        title='สินค้าชิ้นที่ 2',
                        text='รายละเอียดสินค้า 2',
                        actions=[
                            MessageAction(label='ซื้อชิ้นที่ 2', text='ซื้อ 2'),
                            URIAction(label='ดูรายละเอียด', uri='https://google.com')
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template)
    
    else:
        # กรณีพิมพ์อย่างอื่นมา ให้ตอบกลับวิธีใช้
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ลองพิมพ์คำว่า: text, button, quick, หรือ carousel ดูสิครับ")
        )

if __name__ == "__main__":
    app.run(port=8080)