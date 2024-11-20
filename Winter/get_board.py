import httpx
from tools import *

async def get_board():
    print(111)

    try:

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://pbdv.ishpduwu.link/paintboard",
        }

        async with httpx.AsyncClient() as client:
            board = await client.get("https://pbdv.ishpduwu.link/paintboard/board",headers=header)

        lines = board.text.split('\n')
    #    print(lines)

        x=0
        color_list = [[Color((0,0,0)) for i in range(600)] for j in range(1000)]

        for line in lines:
            y=0
            RGBs = [line[i:i+6] for i in range(0, len(line), 6)]
            for RGB in RGBs:
                R = int(RGB[0:2],16)
                G = int(RGB[2:4], 16)
                B = int(RGB[4:6], 16)

                color_list[x][y]=Color((R,G,B))

                y += 1
            x += 1

        return Board(RGB_Map(color_list))
    except:
        return 0