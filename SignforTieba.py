#!/bin/evn python
# coding:utf-8

import json
import time
import hashlib
import asyncio
from http.cookies import SimpleCookie
from lxml import etree

import aiohttp


class TiebaSign:
	def __init__(self, cookies):
		if isinstance(cookies, str):
			cookies = SimpleCookie(cookies)
		self._session = aiohttp.ClientSession(cookies=cookies)
		self._tbs = ''

	async def close(self):
		await self._session.close()
		
	@staticmethod
	def __add_sign(data):
		buffer = ''.join('='.join((key, data[key]))
						for key in sorted(data.keys())
						if key != 'sign' and isinstance(data[key], str)
						) + 'tiebaclient!!!'
		data['sign'] = hashlib.md5(buffer.encode('utf-8')).hexdigest()
		
	def post(self, url, data=None, need_tbs=False, **kwargs):
		data = {key: value if isinstance(value, str) else str(value)
				for key, value in data.items()
				} if data is not None else {}
		if need_tbs:
			data['tbs'] = self._tbs
		self.__add_sign(data)
		return self._session.post(url, data=data, **kwargs)
		
	async def run(self):
		self._tbs = await self.get_tbs()
		forums = await self.get_liked_forums()
		for i in range(len(forums)):
			await asyncio.gather(self.sign(forums[i]))
		
	async def get_tbs(self):
		async with self._session.get('http://tieba.baidu.com/dc/common/tbs') as res:
			data = json.loads(await res.text())
		return data['tbs']
	
	async def get_liked_forums(self):
		async with self._session.get('http://tieba.baidu.com/f/like/mylike') as res:
			html = etree.HTML(await res.text())
		return html.xpath('//tr/td[1]/a/text()')
		
	async def sign(self, forum_name):
		async with self.post('http://c.tieba.baidu.com/c/c/forum/sign', {
					'kw': forum_name
					}, True) as res:
						data = json.loads(await res.text())
						if data['error_code'] != '0':
							print(f'{forum_name}: {data["error_msg"]}"')
						else:
							print('签到成功，经验+%s'% data["user_info"]["sign_bonus_point"])
async def main():
	with open('cookie.txt') as f:
		cookies = f.read()
	tieba_sign = TiebaSign(cookies)
	try:
		await tieba_sign.run()
	finally:
		await tieba_sign.close()
		
if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main())
