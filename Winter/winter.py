import httpx
import asyncio
from tools import *
import get_board
import random
import draw
import png
import file

def find_different(RGB1, RGB2, x, y): #原序列，图片序列
    different_list = []

    for i in range(len(RGB1.RGB)):
        for j in range(len(RGB1.RGB[i])):
            if RGB1.RGB[i][j] != RGB2.RGB[i][j]:
#                print(RGB1.RGB[i][j].R,RGB2.RGB[i][j].R)
#                print(RGB1.RGB[i][j].G,RGB2.RGB[i][j].G)
#                print(RGB1.RGB[i][j].B,RGB2.RGB[i][j].B)
                different_list.append([i+x,j+y,RGB1.RGB[i][j],RGB2.RGB[i][j]])
    return different_list

#my_board=get_board.get_board()

#my_png = png.init_png("C:/Users/asus/Desktop/PNG/6AEU]1Y]HSZE[40TD`SD8]T_tmb.jpg",100,100,1,1)
#
#print(len(find_different(my_board.cut(my_png.x,my_png.y,my_png.x+my_png.width,my_png.y+my_png.height),my_png.RGB)))

png_list = file.init_pngs()
token_list = file.init_tokens()
uid_list = file.init_uids()
different_list,different_p = [],0
different_map = [[0 for i in range(600)] for j in range(1000)]
my_board = 0

async def update_different():
    while True:
        my_board = await get_board.get_board()
        if my_board==0:
#            print(1122222)
            await asyncio.sleep(31)
            continue

        new_different_list = []
        for mypng in png_list:
            cut = my_board.cut(mypng.x,mypng.y,mypng.x+mypng.width,mypng.y+mypng.height)
            mylist = find_different(cut,mypng.RGB,mypng.x,mypng.y)
            for i in mylist:
                new_different_list.append(i)
#        print(new_different_list)
        random.shuffle(new_different_list)

        global different_list,different_p
        different_list = new_different_list
        different_p = 0

        for i in new_different_list:
#            print(type(i))
            different_map[i[0]][i[1]]=1

        print("当前剩余 dirrerent:",len(different_list))
        await asyncio.sleep(31)

async def paint_loop(uid,token):
#    print(uid,token)
    while True:
        try:
            global different_list,different_p

#            print(different_list[different_p])
            x = different_list[different_p][0]
            y = different_list[different_p][1]
            color = different_list[different_p][3]
#            print(x, y)
            different_p+=1
            while different_map[x][y]==0:
#                print(x,y)
                x = different_list[different_p][0]
                y = different_list[different_p][1]
                color = different_list[different_p][3]
                different_p += 1

    #        print(x,y)

            code = 0
            num=0
            while code==0 and num<=3:
                code = await draw.paint(x, y, color, uid, token)
                num+=1
            different_map[x][y] = 0
            print("ACC")
            await asyncio.sleep(31)
        except:
#            print("NO！！！")
            await asyncio.sleep(31)


async def main():
    client = httpx.AsyncClient()

    tasks = []
    task = asyncio.create_task(update_different())

    tasks.append(task)
    for i in range(len(uid_list)):
        task = asyncio.create_task(paint_loop(uid_list[i], token_list[i]))
        tasks.append(task)

    for i in tasks:
        await i

    print(1)

if __name__ == "__main__":
    asyncio.run(main())
