import gtk
import pango
import gobject
import math
import random
import datetime
import bz2
import base64

NUM_RANGE = 15
MAX_MINUTES = 10
QUEST_RANGE = 4

open("data.tdf",'a').close()
class App(object):

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("eval.glade")
        builder.connect_signals(self)
        
        
        self.window = builder.get_object("window")
        self.entry = builder.get_object("entry")
        self.drawingArea = builder.get_object("drawingArea")
        self.timeLabel = builder.get_object("timeLabel")
        self.questionLabel = builder.get_object("questionLabel")
        self.textWindow = builder.get_object("textWindow")
        self.textView = builder.get_object("textView")
        
        self.drawingArea.connect("expose-event",self.expose)
        
        
        fd = pango.FontDescription()
        fd.set_size(pango.SCALE*35)
        self.entry.modify_font(fd)
        
        self.window.show_all()
        
        self.seconds = 0
        self.minutes = 0
        
        gobject.timeout_add(1000, self.timerCall)
        self.num1 = 0
        self.num2 = 0
        self.questNum = 0
        self.rightAns = 0
        self.attempts = 0
        


        
        self.genNew()
    def start(self):
        gtk.main()
        
    def destroy(self,data=None):
        print 'des'
        gtk.main_quit()
        
    def expose(self,widget=None,data=None):
        ht = self.drawingArea.get_allocation().height
        wd = self.drawingArea.get_allocation().width
        
        
        cr = widget.window.cairo_create()
        cr.translate(wd/2,ht/2)
        cr.scale(wd/100.0,ht/100.0)
        
        cr.set_source_rgb(.5,.5,1)
        cr.set_line_width(3.5)
        cr.arc(0,0, 30, -math.pi/2,2*math.pi*self.seconds/60 - math.pi/2)
        cr.stroke()
        
        cr.set_source_rgb(0,0,0.0)
        cr.set_line_width(3.5)
        cr.arc(0,0, 33.5, -math.pi/2,2*math.pi*self.minutes/MAX_MINUTES - math.pi/2)
        cr.stroke()
        text = "%d/%d"%(self.questNum,QUEST_RANGE)
        x,y,w,h, = cr.text_extents(text)[:4]
        cr.move_to(-w/2,-h/2)
        cr.show_text(text)
        cr.stroke()
    def timerCall(self,data=None):
        self.seconds += 1
        if(self.seconds == 60):
            self.seconds = 0
            self.minutes += 1
        if(self.minutes == MAX_MINUTES):
            self.finish()
        self.drawingArea.queue_draw()
        
        text = "%dm %ds \nRemaining " % (MAX_MINUTES - self.minutes,60 - self.seconds)
        self.timeLabel.set_text(text)
        return True
        
    def genNew(self,data=None):
        self.num1 = random.randint(1,NUM_RANGE)
        self.num2 = random.randint(1,NUM_RANGE)
        text = "%d x %d" % (self.num1,self.num2)
        self.questionLabel.set_text(text)
        self.questNum += 1
        self.entry.set_text('')
        
    def nextClick(self,data=None):
        self.entry.set_text('0')
        self.answerClick()
        self.entry.set_text('')
    def answerClick(self,data=None):
        text = self.entry.get_text()
        try:
            ans = int(text)
            self.attempts += 1
            if(ans == self.num1*self.num2):
                self.rightAns += 1
            
            if(self.attempts == QUEST_RANGE):
                self.finish()
            self.genNew()
            
            
        except ValueError:
             md = gtk.MessageDialog(None, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
         gtk.BUTTONS_CLOSE, "Please Enter a  Valid Number")
             md.run()
             md.destroy()
    def finish(self):
        text = "%d out of %d answers correct on %s" % (self.rightAns,self.attempts,datetime.datetime.now().strftime("%d/%m/%y %H:%M"))
        fileObj = open("data.tdf",'a')
        fileObj.write(base64.b64encode(text ) + '\n')
        fileObj.close()
        
        md = gtk.MessageDialog(None, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
        gtk.BUTTONS_CLOSE, "Test Complete\n%d out of %d answers correct." % (self.rightAns,self.attempts))
        
        md.run()
        md.destroy()
    
        self.questNum = 0
        self.rightAns = 0
        self.attempts = 0
        self.minutes = 0
        self.seconds = 0
    def statsShow(self,data=None):
    
        f = open("data.tdf")
        lines = '\n'.join([base64.b64decode(line) for line in f.readlines()])
        f.close()
        self.textView.get_buffer().set_text(lines)

        self.textWindow.get_visible()
        if(self.textWindow.get_visible()):
            self.textWindow.hide()
        else:
            self.textWindow.show()
            
        
app = App()
app.start()
