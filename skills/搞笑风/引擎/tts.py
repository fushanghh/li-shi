import asyncio,sys,os,edge_tts,urllib.parse
p=os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
import urllib.parse as U
if p and '@' in p:
    sch,rest=p.split('://',1);ui,host=rest.rsplit('@',1)
    u,pw=ui.split(':',1)
    p=f"{sch}://{U.quote(u,safe='')}:{U.quote(pw,safe='')}@{host}"
for k in list(os.environ):
    if 'proxy' in k.lower(): os.environ.pop(k)
async def m(text,out,voice='zh-CN-XiaoyiNeural',rate='+8%'):
    c=edge_tts.Communicate(text,voice,rate=rate,proxy=p)
    await c.save(out)
asyncio.run(m(sys.argv[1],sys.argv[2],*(sys.argv[3:])))
