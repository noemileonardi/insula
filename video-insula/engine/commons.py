import re
import sys, json, urllib.parse, urllib.request
UA={'User-Agent':'InsulaVideoTool/1.0 (educational video project)'}
import time,urllib.error
def _open(req):
    for i in range(6):
        try: return urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            if e.code!=429: raise
            time.sleep(int(e.headers.get('retry-after') or 15)+2)
    raise SystemExit('rate limited')
def get(url):
    return json.load(_open(urllib.request.Request(url,headers=UA)))
def search(q, n=12):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action='query',generator='search',gsrnamespace=6,gsrsearch=q,gsrlimit=n,prop='imageinfo',iiprop='url|size|extmetadata',iiurlwidth=1080,format='json'))
    d=get(u)
    for p in (d.get('query',{}).get('pages',{}) or {}).values():
        ii=p['imageinfo'][0]; m=ii.get('extmetadata',{})
        print(p['title'][:70],'|',ii['width'],'x',ii['height'],'|',m.get('LicenseShortName',{}).get('value'),re.sub('<[^>]+>','',m.get('Artist',{}).get('value',''))[:40],'|',ii.get('thumburl'))
if __name__=='__main__':
    if sys.argv[1]=='search': search(sys.argv[2])
    else:
        url,out=sys.argv[2],sys.argv[3]
        open(out,'wb').write(_open(urllib.request.Request(url,headers=UA)).read()); print('ok',out)
