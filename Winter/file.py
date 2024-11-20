from tools import *
import png
import draw

#def init_tokens():
#    tokens = []
#    with open("tokens.txt","r") as f:
#        for line in f.readlines():
#            split_list = line.split(' ')
##            print(split_list[0],split_list[1][:-1:])
#            tokens.append(draw.get_token(split_list[0],split_list[1][:-1:]))
#    return tokens

#def init_uids():
#    uids = []
#    with open("tokens.txt","r") as f:
#        for line in f.readlines():
#            split_list = line.split(' ')
#            uids.append(split_list[1][:-1:])
#    return uids

def init_tokens():
    tokens = []
    with open("token_list.txt","r") as f:
        for line in f.readlines():
            split_list = line.split(' ')
            tokens.append(split_list[1][:-1:])
    return tokens

def init_uids():
    uids = []
    with open("token_list.txt","r") as f:
        for line in f.readlines():
            split_list = line.split(' ')
            uids.append(split_list[0])
    return uids

def init_pngs():
    png_list=[]
    with open("png_list.txt","r") as f:
        for line in f.readlines():
            png_attr = line.split(' ')
            my_png = png.init_png("./pngs/"+png_attr[0],int(png_attr[1]),int(png_attr[2]),int(png_attr[3]),int(png_attr[4]))
            png_list.append(my_png)
    return png_list

def init_tokenlist():
    tokens = []
    uids = []
    with open("tokens.txt","r") as f:
        for line in f.readlines():
            split_list = line.split(' ')
            print(split_list[0],split_list[1][:-1:])
            try:
                tokens.append(draw.get_token(split_list[0],split_list[1][:-1:])["data"])
                uids.append(split_list[1][:-1:])
            except:
                continue
    with open("token_list.txt","w") as f:
        for i in range(len(tokens)):
            print(uids[i],tokens[i])
            f.write(str(uids[i]) + ' ' + str(tokens[i]) + '\n')
    return 0