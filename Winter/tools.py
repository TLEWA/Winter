from PIL import Image

class Color(object):
    def __init__(self, RGB):
        self.R = RGB[0]
        self.G = RGB[1]
        self.B = RGB[2]

    def change(self, RGB):
        self.R = RGB[0]
        self.G = RGB[1]
        self.B = RGB[2]

    def to_string(self):
#        print(self.R,str(hex(self.R))[-2:],str(hex(self.R)))
#        print(self.G,str(hex(self.G))[-2:], str(hex(self.G)))
#        print(self.B,str(hex(self.B))[-2:], str(hex(self.B)))
        return str(hex(self.R))[-2:].replace('x','0')+str(hex(self.G))[-2:].replace('x','0')+str(hex(self.B)[-2:].replace('x','0'))

    def __eq__(self, other):
        return [self.R,self.G,self.B] == [other.R,other.G,other.B]

class RGB_Map(object):
    def __init__(self,RGB_array):
        self.RGB = RGB_array

class PNG(object):
    def __init__(self,png,width,height,x,y):
        self.png = png.resize((width,height))
        self.RGB = RGB_Map([[Color(self.png.getpixel((j, i))) for i in range(height)] for j in range(width)])
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Board(object):
    def __init__(self,board_arr):
        self.board = board_arr
    def cut(self,start_x,start_y,end_x,end_y):
        return RGB_Map([i[start_y:end_y] for i in self.board.RGB[start_x:end_x]])
int()