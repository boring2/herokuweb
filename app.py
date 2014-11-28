#coding=utf-8
'''
Created on 2014-11-26

@author: boring2
'''

import urllib
import socket
from bs4 import BeautifulSoup
import re
import HTMLParser
import os
import sys
import web
socket.setdefaulttimeout(5)
urls = (
        "/","mainfun"
        )

render = web.template.render("templates/",cache=False,base="layout")
app = web.application(urls,globals())
class mainfun:
    def GET(self):
        return render.index('')
    
    def POST(self):
        url = web.input().searchinput
        url = 'http://' + url
        try:
            content = urllib.urlopen(url).read()
            index_begin = content.find('charset=')
            index_begin += len('charset=')
            index_end = content.find('"',index_begin)
            charset = content[index_begin:index_end]
            if not charset:
                charset = "utf-8"
            repx = '<meta.*(content=\".*\")*.*name=\"[kK]eywords\".*(content=\".*\")*.*'
            m = re.search(repx, content)
            if m is not None:
                m2 = m.group()
                m3 = re.search('content=\"(.*)\"', m2)
                if m3 is not None:
                    keywords=m3.group(1).split('"')[0].decode(charset)
            else:
                keywords = "没有找到关键字"
            
            soup = BeautifulSoup(content,from_encoding="gb18030")
            title = soup.html.title
            yourip =  web.ctx.env['REMOTE_ADDR']
            if title:
                title = title.string
            else:
                title = '没找到标题,可输入完整地址再试试'
        except socket.timeout:
            print("连接超时请检查网络，请重试")
            return render.index({'title':"连接超时请检查网络",'yourip':"",'charset':"","keywords":""})
        except UnicodeDecodeError:
            return render.index({'title':"抱歉,无法识别改网页编码",'yourip':"",'charset':"","keywords":""})
        except IOError:
            return render.index({'title':"请检查域名是否正确",'yourip':"",'charset':"","keywords":""})
        except HTMLParser.HTMLParseError:
            return render.index({'title':"抱歉不支持该网页",'yourip':"",'charset':"","keywords":""})
        except:
            return render.index({'title':"发生不可预知错误",'yourip':"",'charset':"","keywords":""})
        return render.index({'title':title,'yourip':yourip,"charset":charset.encode("utf-8"),"keywords":keywords})
if __name__ == "__main__":
    port = os.environ.get("PORT", "5001")
    sys.argv[1] = port
    app.run()
