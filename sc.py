#---coding:utf-8---
from PIL import Image,ImageFile
from fpdf import FPDF
import os,sys,time
import threading
bookname=sys.argv[1]
startime=time.strftime("%H:%M:%S")
threads=[]
mw = 221
mw = 234
mh = 312
sumpage=100
front="http://211.79.206.2:8080/ocp/include/viewBookXmml.php?no=180201074458987&viewType=0&version=146/br"
os.system("rm /root/undone/*")
os.system("rm /root/zazhi/*")
os.system("rm /root/zazhi/done/*")
def download(urlstr,fname):
    os.system('aria2c --max-tries=0 --retry-wait=3 --save-session=/root/undone/'+fname+'.session -s 1 -j 1 -x 1 -c -d /root/zazhi -o '+fname+' --user-agent "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Name" "'+urlstr+'"')
def hc(p):
    global mw,mh
    toImage = Image.new('RGB', (mw * 8, mh * 8))
    try:
        for x in range(p*8, (p+1)*8):
          for y in range(0, 8):
                fname = "/root/zazhi/%s%s" % (y,str(x).zfill(5))
                fromImage = Image.open(fname)
                toImage.paste(fromImage, ((x-8*p)*mw,y*mh))
        toImage.save('/root/zazhi/done/%s.jpg' % p)
    except IOError as e:
        print fname,p
for col in range(0,sumpage*8):
    for row in range(0,8):
#        print threading.active_count()
        urlstr=front+str(row).zfill(5)+str(col).zfill(5)+'00003'
        fname=str(row)+str(col).zfill(5)
        td=threading.Thread(target=download,args=(urlstr,fname))
        td.start()
        threads.append(td)
    while True:
        if threading.active_count()<56:
            break
for t in threads:
    t.join()
size=1
while size:
  os.system("find /root/undone/ -name '*' -type f -size 0c | xargs -n 1 rm -f")
  lr=os.listdir("/root/undone")
  size=len(lr)
  for file in lr:
    os.system("rm -f /root/zazhi/"+file)
    os.system("aria2c --save-session=/root/undone/"+file+" -i /root/undone/"+file)
for p in range(0,sumpage):
    td=threading.Thread(target=hc,args=(p,))
    td.start()
    threads.append(td)
    while True:
        if threading.active_count()<20:
            break
for t in threads:
    t.join()
pdf = FPDF(unit = "pt", format = [mw*8, mh*8])
for page in range(0,sumpage) :
    file=os.path.join('/root/zazhi/done/',str(page)+'.jpg')
    pdf.add_page()
    pdf.image(file,0,0)
pdf.output("/root/"+bookname+".pdf", "F")
os.system("gdrive upload -p 0BxiMW05er8ZBUUdOX2dnWTRnOTA /root/"+bookname+".pdf")
os.system("rm /root/"+bookname+".pdf")
print "start:"+startime,"end:"+time.strftime("%H:%M:%S")
