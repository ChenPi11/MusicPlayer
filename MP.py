'''                                                      LICENSE
BSD 2-Clause License

Copyright (c) 2022, ChenPi11
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''
#moudle:pyaudio,numpy
import wave,pyaudio,os,struct,math,sys,time,platform
import numpy as np
from threading import *

e={"0":0,
   ".1":262,".2":294,".3":330,".4":350,".5":392,".6":440,".7":494,
   "1":523,"2":578,"3":659,"4":698,"5":784,"6":880,"7":988,
   "1.":1046,"2.":1175,"3.":1318,"4.":1400,"5.":1568,"6.":1760,"7.":1976}
#by book_rain@CSDN----------------------------------------------------------------
# volume x_db
def c(sfl,sfr,wf,time):
    db = math.pow(10, -3/20)
    framerate = 44100
    sample_width = 2
    bits_width = sample_width*8
    # seconds, long of data
    duration = time/1000
    # frequeny of sinewave
    sinewav_frequency_l = sfl
    sinewav_frequency_r = sfr
    # max value of samples, depends on bits_width
    max_val = 2**(bits_width-1) - 1
    volume = max_val*db
    #多个声道生成波形数据
    x = np.linspace(0, duration, num=int(duration*framerate))
    y_l = np.sin(2 * np.pi * sinewav_frequency_l * x) * volume
    y_r = np.sin(2 * np.pi * sinewav_frequency_r * x) * volume
    # 将多个声道的波形数据转换成数组
    y = zip(y_l,y_r)
    y = list(y)
    y = np.array(y,dtype=int)
    y = y.reshape(-1)
    # 最终生成的一维数组
    sine_wave = y
    for i in sine_wave:
        data = struct.pack('<h', int(i))
        wf.writeframesraw(data)
#---------------------------------------------------------------------------------
error=False
que=[]
echos=[]
start=0

#init
cls=None
def WindowsInit():
    try:
        global cls
        def _cls():
            os.system("cls")
        cls=_cls
    except Exception as e:
        print("Error on init",platform.system(),e.__class__.__name__+":",e)
        global error
        error=True
def LinuxInit():
    try:
        global cls
        def _cls():
            os.system("clear")
        cls=_cls
    except Exception as e:
        print("Error on init",platform.system(),e.__class__.__name__+":",e)
        global error
        error=True
if("windows" in platform.system().lower()):
    WindowsInit()
else:
    LinuxInit()

def core(f):
    global e,que,echos
    for i in f:
        if(i.strip()==""):
            continue
        if(i.strip().split(" ")[0]=="echo"):
            try:
                echos.append(Echo(i.strip().split(" ")[1],0,i.strip().split(" ")[2]))
            except:
                try:
                    echos.append(Echo(i.strip().split(" ")[1],0))
                except:
                    pass
            continue
        if(i.strip().split(" ")[0]=="#"):
            continue
        else:
            l=0
            r=0
            try:
                l=e[i.strip().split(" ")[0]]
            except:
                pass
            try:
                r=e[i.strip().split(" ")[1]]
            except:
                pass
            try:
                if(len(i.strip().split(" ")[0])>1):
                    if(i.strip().split(" ")[0][0]=="r"):
                        l=int(i.strip().split(" ")[0][1:])
            except:
                pass
            try:
                if(len(i.strip().split(" ")[1])>1):
                    if(i.strip().split(" ")[1][0]=="r"):
                        r=int(i.strip().split(" ")[1][1:])
            except:
                pass
            que.append([l,r,int(int(i.strip().split(" ")[2]))])
            try:
                echos.append(Echo(i.strip().split(" ")[3],int(int(i.strip().split(" ")[2]))))
            except:
                echos.append(Echo("",int(int(i.strip().split(" ")[2]))))
    f.close()

class Echo:
    text=""
    sleep=""
    color=""
    def __init__(self,text,sleep,color="white"):
        self.text=text.replace("\\n","\n").replace("\\t","\t").replace("|","").replace("~"," ").replace("\\|","|").replace("\\~","~")
        self.sleep=sleep
        self.color=color
    def play(self):
        print(self.text,end='',flush=True)
        time.sleep(self.sleep/1000)
if(not error):
    fpath=sys.argv[1]
    fname=os.path.splitext(os.path.basename(fpath))[0]
    #open
    channel_num = 2
    framerate = 44100
    sample_width = 2
    wf = wave.open(fname+".wav","wb")
    wf.setnchannels(channel_num)
    wf.setframerate(framerate)
    wf.setsampwidth(sample_width)
    #mix
    try:
        core(open(fpath,"r",encoding="GBK"))
        for i in range(len(que)):
            c(que[i][0],que[i][1],wf,que[i][2])
            print(str(i+1)+" "*(len(str(len(que)))-len(str(i+1)))+"/"+str(len(que))+" "+str(int((i+1)/len(que)*100))+"%")
        wf.close()
    except Exception as e:
        print("Error",e.__class__.__name__+":",e)
        error=True
    #play
    def TextPlayer():
        global echos
        for i in echos:
            i.play()
    cls()
    Thread(target=TextPlayer,daemon=True).start()
    chunk = 1024
    wf = wave.open(fname+".wav","rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
    data = wf.readframes(chunk)
    i=0
    start=time.time()
    while(len(data)>0):
        stream.write(data)
        data = wf.readframes(chunk)
        i+=1
        time.sleep((((time.time()-start))-(i*chunk/framerate))/1000)
    stream.stop_stream()
    stream.close()
    p.terminate()
