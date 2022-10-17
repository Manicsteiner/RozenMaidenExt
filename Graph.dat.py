import os,sys,struct

from PIL import Image

def main():
    if not os.path.exists("Graph.dat"):
        print("File not exist")
        return
    data = open("Graph.dat", 'rb')
    os.system("mkdir Graph")
    data.seek(20,0)
    filetotal = struct.unpack("<I",data.read(4))[0]
    flnamestart = filetotal*20+36
    
    for i in range (filetotal):
        data.seek(36+i*20,0)
        #print("start pointer " + str(data.tell()))
        fstart,flength,dr0,dr1,namepl = struct.unpack("<5I",data.read(20))
        data.seek(flnamestart+namepl,0)
        #filename = getFileName(struct.unpack("s",data.read(35))[0])
        filename = getFileName(b'' + data.read(35))
        if filename.endswith(".png"):
            wrfile = open("Graph/"+filename, 'wb')
            data.seek(fstart)
            wrfile.write(data.read(flength))
            wrfile.close()
            print("complete pic" + str(i))
            continue
        data.seek(fstart+32,0)
        #filedata = data.read(flength)
        width, height = struct.unpack(">2H",data.read(4))
        img = Image.new('RGBA', (width, height))
        data.seek(fstart+128,0)
        for y in range(height):
            for x in range(width):
                color = data.read(4)
                img.putpixel((x, y), (color[1], color[2], color[3], color[0]))
        img.save("Graph/" + filename + '.png', 'png')
        print("complete pic" + str(i))
        #print("final pointer " + str(data.tell()))
    data.close()
    print("Complete!")

def getFileName(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    rstr1 = str(s.replace(b"\xFF",b"").replace(b"\x90",b"").replace(b"\x80",b""),encoding = "sjis")
    #returnstr = str(s.replace(b"\x00",b""),encoding = "sjis")
    rstr2 = rstr1.rsplit('.', -1)[0]
    rstr3 = rstr1.rsplit('.', -1)[1]
    if rstr3.startswith("PNG"):
        return rstr2+".png"
    else:
        return rstr2

if __name__ =="__main__":
    main()
