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
    print("Totaly " + str(filetotal) + " files")
    datanamestart = filetotal*20+36
    
    for i in range (filetotal):
        data.seek(36+i*20,0)
        fstart,dataength,dr0,dr1,namepl = struct.unpack("<5I",data.read(20))
        data.seek(datanamestart+namepl,0)
        filename = getFileName(b'' + data.read(35))
        if filename.endswith(".PNG"):
            wrfile = open("Graph/"+filename, 'wb')
            data.seek(fstart)
            wrfile.write(data.read(dataength))
            wrfile.close()
            print("complete pic" + str(i))
            continue
        else:
            filename = filename.rsplit('!', 1)[0]
        data.seek(fstart+8,0)
        filenum = struct.unpack(">I",data.read(4))[0]
        for j in range(filenum):
            data.seek(fstart+16+36*j,0)
            filestart,filelength = struct.unpack(">2I",data.read(8))
            data.seek(fstart+32+36*j,0)
            width, height = struct.unpack(">2H",data.read(4))
            img = Image.new('RGBA', (width, height))
            data.seek(fstart+filestart,0)
            for y in range(height):
                for x in range(width):
                    color = data.read(4)
                    img.putpixel((x, y), (color[1], color[2], color[3], color[0]))
            if filenum==1:
                while os.path.exists("Graph/" + filename + ".png"):
                    filename = filename + "_1"
                img.save("Graph/" + filename + ".png", 'png')
                break
            img.save("Graph/" + filename + "_" + str(j) + ".png", 'png')
        print("complete pic " + str(i+1))
    data.close()
    print("Complete!")

def getFileName(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    rstr1 = str(s.replace(b"\x00",b"!"),encoding = "sjis",errors = "ignore")
    rstr2 = rstr1.rsplit('!', -1)[0]
    return rstr2

if __name__ =="__main__":
    main()
