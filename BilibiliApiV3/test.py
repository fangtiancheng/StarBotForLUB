import asyncio
import requests
from PIL import Image
from io import BytesIO
import base64
from utils.config import set_credential
from utils.utils import get_credential
from utils.network import request
from painter.DynamicPicGenerator import DynamicPicGenerator

async def dynamic_update(event):
    """
    动态更新事件
    """

    dynamic_id = event["desc"]["dynamic_id"]
    dynamic_type = event["desc"]["type"]
    bvid = event['desc']['bvid'] if dynamic_type == 8 else ""
    rid = event['desc']['rid'] if dynamic_type in (64, 256) else ""

    action_map = {
        1: "转发了动态",
        2: "发表了新动态",
        4: "发表了新动态",
        8: "投稿了新视频",
        64: "投稿了新专栏",
        256: "投稿了新音频",
        2048: "发表了新动态"
    }
    url_map = {
        1: f"https://t.bilibili.com/{dynamic_id}",
        2: f"https://t.bilibili.com/{dynamic_id}",
        4: f"https://t.bilibili.com/{dynamic_id}",
        8: f"https://www.bilibili.com/video/{bvid}",
        64: f"https://www.bilibili.com/read/cv{rid}",
        256: f"https://www.bilibili.com/audio/au{rid}",
        2048: f"https://t.bilibili.com/{dynamic_id}"
    }
    base64str = await DynamicPicGenerator.generate(event)
    return base64str, action_map.get(dynamic_type, "发表了新动态")

async def main():
    set_credential('', '', '')
    dynamic_url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?type_list=268435455"
    credential = get_credential()
    latest_dynamic = await request('GET', url=dynamic_url, credential=credential)
    new_num = latest_dynamic["new_num"]
    for i, detail in enumerate(latest_dynamic["cards"]):
        dynamic_id = detail['desc']['dynamic_id']
        base64str, info = await dynamic_update(detail)
        img = Image.open(BytesIO(base64.b64decode(base64str)))
        img.save('%02d.png'%i)

if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(main()))
