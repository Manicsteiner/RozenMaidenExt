import os,sys,struct

#from PIL import Image

def main():
    if not os.path.exists("Sound.dat"):
        print("File not exist")
        return
    data = open("Sound.dat", 'rb')
    os.system("mkdir Sound")
    data.seek(20,0)
    filetotal = struct.unpack("<I",data.read(4))[0]
    print("Totaly " + str(filetotal) + " files")
    flnamestart = filetotal*20+36
    
    for i in range (filetotal):
        data.seek(36+i*20,0)
        fstart,flength,dr0,dr1,namepl = struct.unpack("<5I",data.read(20))
        data.seek(flnamestart+namepl,0)
        filename = getFileName(b'' + data.read(35))
        wrfile = open("Sound/"+filename, 'wb')
        data.seek(fstart)
        wrfile.write(data.read(flength))
        wrfile.close()
        print("complete sound " + str(i+1))
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
