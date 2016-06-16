from bs4 import BeautifulSoup
from Tkinter import *
from PIL import ImageTk, Image
import urllib2, cStringIO

board = raw_input('board:')
pages = int(raw_input('pages:'))
imgsize = 150
baseurl = "http://boards.4chan.org/"+board+"/"
root  = Tk()

loadedimg = []
bigimg = []
for page in range(1,pages+1):
    print page
    if(page>1):
        pageurl = baseurl + str(page) +"/"
    else:
        pageurl = baseurl
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(pageurl, headers=hdr)

    response = urllib2.urlopen(req)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    subsoups = []
    replylinks = soup.find_all('a',attrs={'class':"replylink"},text="Reply")
    for link in replylinks:
        print str(baseurl+link.get('href'))
        req = urllib2.Request(str(baseurl+link.get('href')), headers=hdr)
        subsoups.append(BeautifulSoup(urllib2.urlopen(req).read(),'html.parser'))

    for ind, subsoup in enumerate(subsoups):
        imgs = subsoup.find_all('a', attrs={"class":"fileThumb"})
        print "thread "+ str(ind) + "/"+ str(len(subsoups)-1)+":"
        print "images " +str(len(imgs))
        for img in imgs:
            url = str("https:"+img.find_all('img')[0].get('src'))
            rawthumb = Image.open(cStringIO.StringIO(urllib2.urlopen(url).read()))
            resizedthumb = rawthumb.resize((imgsize,imgsize), Image.ANTIALIAS)

            loadedimg.append( ImageTk.PhotoImage(resizedthumb))
            bigimg.append(str("https:"+img.get('href')))


frame = Frame(root,width = imgsize*10, height = 900)
frame.grid(row = 0, column = 0)
canvas = Canvas(frame, bg='#FFFFFF', width = imgsize*10, height = 900,scrollregion = (0,0,1000,int((len(loadedimg))/10)*imgsize))
scroll = Scrollbar(frame)
scroll.pack(side = RIGHT,fill = Y)

canvas.config(yscrollcommand=scroll.set)
scroll.config(command=canvas.yview)

canvas.pack()

for i, img in enumerate(loadedimg):
    #panel = Label(canvas, image = img, width = 90, height = 90)
    #panel.grid(row = int(i/10), column = i%10)
    canvas.create_image(i%10*imgsize+imgsize/2,int(i/10)*imgsize+imgsize/2, image= img)

ypos = 0
yposmax = (float(((len(loadedimg))/10)*imgsize)-imgsize*6)/float(((len(loadedimg))/10)*imgsize)
def down(event):
    global ypos
    if(ypos<yposmax):
        ypos=ypos+10.0/i
    canvas.yview_moveto(ypos)
def up(event):
    global ypos
    if(ypos>0):
        ypos=ypos-10.0/i
    canvas.yview_moveto(ypos)
def scrollup(event):
    global ypos
    if(ypos>0):
        ypos=ypos-1.0/i
    canvas.yview_moveto(ypos)
def scrolldown(event):
    global ypos
    if(ypos<yposmax):
        ypos=ypos+1.0/i
    canvas.yview_moveto(ypos)


root.bind_all("<Button-4>",scrollup)
root.bind_all("<Button-5>",scrolldown)
root.bind_all("<Down>",down)
root.bind_all("<Up>",up)

class MiniWindow:
    def __init__(self, x , y):
        global ypos
        yheight = ypos*int(len(loadedimg)/10)*imgsize
        y=y+yheight
        #print ypos,yheight
        imgroot = Toplevel()
        url =   bigimg[int(x/imgsize)+10*int(y/imgsize)]
        img  = Image.open(cStringIO.StringIO(urllib2.urlopen(url).read()))
        #print x/imgsize+10*y/imgsize
        finalimage = ImageTk.PhotoImage(img)
        #print int(x/imgsize)+10*int(y/imgsize)
        minican = Canvas(imgroot, bg = '#FFFFFF', width = img.size[0], height  = img.size[1])
        minican.grid(row = 0,column = 0)
        minican.create_image(img.size[0]/2,img.size[1]/2, image = finalimage)
        imgroot.mainloop()

mini = None
def clicked(event):
    global mini
    print "press",event.x,event.y
    mini = MiniWindow(event.x, event.y)


canvas.bind("<Button-1>", clicked)


root.mainloop()
