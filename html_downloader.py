#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
import urllib.request
import urllib.parse
import urllib.error
from lxml import etree

class HtmlDownloader:
    def __init__(self):
        self.agents = [
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
            "Mozilla/4.79 [en] (compatible; MSIE 7.0; Windows NT 5.0; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)"
        ]

    def download(self, url):
        try:
            headers = {'User-Agent': self.process_request()}
            req = urllib.request.Request(url, None, headers=headers)
            response = urllib.request.urlopen(req, timeout=15)
            text = response.read().decode('utf-8')
            html_t = etree.HTML(text)
            response.close()
            return html_t  
        except:
            raise

    def process_request(self):
        user_agent_n = random.choice(self.agents)
        if user_agent_n:
            return user_agent_n
