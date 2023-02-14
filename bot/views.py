from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse=WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(requests):
    return HttpResponse("<h1>LineBot APP</h1>")

@csrf_exempt    
def callback(request):
    words=['早安~你好，今天好嗎?','天氣很不錯!','我準備去上班','肚子好餓']
    if request.method=='POST':
        signature=request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')
        try:
            events=parse.parse(body,signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event,MessageEvent):
                if isinstance(event.message,TextMessage):
                    text=event.message.text
                    print(text)

                    #程式練習(使用者輸入樂透=>給予六個號碼跟一個特別號)
                    if '電影' in text:
                        message='https://movies.yahoo.com.tw/movie_comingsoon.html'
                    elif '台北捷運' in text:
                        message='https://www.metro.taipei/cp.aspx?n=91974F2B13D997F1'
                    elif "台中捷運" in text:
                        image_url='https://www.bing.com/images/search?view=detailV2&ccid=7R9jkAuK&id=09CD6BD8F813CFBA280368B9FEC1E6CDA15EF5F2&thid=OIP.7R9jkAuKkjWtvJP1DU30FAHaG1&mediaurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.ed1f63900b8a9235adbc93f50d4df414%3frik%3d8vVeoc3mwf65aA%26riu%3dhttp%253a%252f%252fassets-us2.piliapp.com%252fs3pxy%252fmrt_taiwan%252ftaichung%252fmap3%25402x.png%26ehk%3ddYR5kPtUdQx7be3l9RrZrqCzdcvGyf04JosFnKA5oyY%253d%26risl%3d%26pid%3dImgRaw%26r%3d0&exph=1420&expw=1540&q=%e5%8f%b0%e4%b8%ad%e6%8d%b7%e9%81%8b%e8%b7%af%e7%b7%9a%e5%9c%96&simid=607992207923372544&FORM=IRPRST&ck=195B4045C0781722522E65DC166D05BF&selectedIndex=8&ajaxhist=0&ajaxserp=0.png'
                        line_bot_api.reply_message(event.reply_token,
                             ImageSendMessage(original_content_url=img_url,
                             preview_image_url=img_url))

                    elif  "樂透" in text:
                        message=lotto()

                    elif '早安' in text:
                        message='早安你好'
                    else:
                        message = random.choice(words)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=message)
                    )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='無法解析')
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    

def lotto():
    numbers = sorted(random.sample(range(1, 50), 6))
    result = ' '.join(map(str, numbers))
    n = random.randint(1, 50)

    return (f'{result} 特別號:{n}')

