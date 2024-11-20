import file
pngs = file.init_pngs()
i = 1
for png in pngs:
    png.png.save(str(i)+'.png')
    i+=1