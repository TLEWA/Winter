import httpx
import time

def get_token(paste, uid):
    cnt=0
    while cnt<=1:
        try:
            print(1)
            url = 'https://pbdv.ishpduwu.link/paintboard/gettoken'

            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://oi-search.com/paintboard",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
            }

            body = {'uid': uid, 'paste': paste}

            response = httpx.post(url, data=body, headers=header, timeout=60)

            print(uid)
            if response.status_code == 200:
                print(response.text)
            if response.status_code == 200 and response.json()["status"]==200:
                print(response.text)
                return response.json()
            cnt+=1
        except:
            continue

async def paint(x,y,color,uid,token):
    try:
#        print(1,x,y,color.to_string(),uid,token)
        url = 'https://pbdv.ishpduwu.link/paintboard/paint'

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://oi-search.com/paintboard",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        body = {
            'x': x,
            'y': y,
            'color': color.to_string(),
            'uid': uid,
            'token': token
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=body, headers=header)

        if response.status_code == 200:
            print(response.text)
            return 1
        return 0
    except:
        return 0
