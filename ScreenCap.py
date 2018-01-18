# -*- coding: utf-8 -*-

from aip import AipOcr
import os
from PIL import Image
import time
from selenium import webdriver
import requests
import bs4
import webbrowser
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

log_file = "./logger.log"
logging.basicConfig(filename = log_file)

begin = time.time() #记个时
app_id = '10696812'
api_key = '7U3wZ40ELR8M7GtuG1n2aQkV'
secret_key = '******************** ' #注册一个账号就可以了

client = AipOcr(app_id, api_key, secret_key)

def just_do_it(demo = False, browser = False):
    '''
    adb获取屏幕，百度Ocr识别文字，爬虫得到百度首页数据。统计结果。支持webdrvier，直接打开网页。
    '''

    # adb 截图
    # os.system('chcp 65001')
    path = os.path.abspath('./Plugin/adb.exe')
    os.system(str(path) + ' shell screencap -p /storage/emulated/0/ScreenShot.png')
    os.system(str(path) + ' pull /storage/emulated/0/ScreenShot.png Images/ScreenShot.png')
    if demo:
        image = Image.open('Images/demo.jpg')
    else:
        image = Image.open('Images/ScreenShot.png')

    if image.width > image.height:
        image = image.transpose(Image.ROTATE_270) # 方向检测
    box = (50, 350, 1000, 1160) #没有做分辨路适配，本来就用模拟器调的，没有多的手机调，/wx
    image.crop(box).save('Images/Crop.png')

    res = client.basicGeneral(file('Images/Crop.png', 'rb').read(), {'detect_direction': True})
    image.close()
    words = res['words_result']
    all_words = ' '.join([i['words'] for i  in words])
    question = ''
    No = ''
    if len(words)> 3:
        for item in words[:len(words)-3]:
            question += item['words']
        while True:
            if question[0] in [unicode(i) for i in range(9)]:
                No += (question[0])
                question = question.replace(question[0], '', 1)
            else:
                break
        answers = []
        for item in words[len(words)-3:]:
            answers.append(item['words'])

        if browser:
            webbrowser.open('https://www.baidu.com/s?ie=UTF-8&wd={0}'.format(question.encode('GBK')), new = 0, autoraise = True)

        # 爬去信息
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
        res = requests.get('https://www.baidu.com/s', params=dict(
            ie='UTF-8',
            wd=question.encode('utf-8')
        ), headers=headers, timeout=5)
        soup = bs4.BeautifulSoup(res.content, 'lxml')
        res =  soup.find(id='content_left').decode()

        print u'Q:{}.A:{}.'.format(question, ','.join(answers))
        result = []
        for answer in answers:
            result.append(res.count(answer))
        logging.info( '结果统计完成!用时:%s' % str(time.time() - begin)+'............')
        print u'\033[1;35m {0}{1}:\n {2}\n \033[0m'.format(No,','.join(answers),result)
    else:
        logging.info('Not that a long list.%s' % all_words )
        if browser:
            webbrowser.open('https://www.baidu.com/s?ie=UTF-8&wd={0}'.format(all_words.encode('GBK')), new = 0, autoraise = True)






if __name__ == '__main__':
    #启动选项

    if 'demo' in sys.argv:
        just_do_it(True,True)

    browser = False
    if raw_input('Open browser?(yes,no)').lower() == 'yes':
        browser= True

    while raw_input('Input \'quit\' to Quit. ').lower()!='quit':
        try:
            just_do_it(browser = browser)
        except Exception as e:
            # print u'好像出了点小问题,hahaha.'
            pass
