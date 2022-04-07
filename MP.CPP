/* ChenPi Music Player MS-DOS Mode v1.0
 * encoding GBK(cp936)
 * edit by Turbo C++ v3.0
*/
#include <stdio.h>
#include <dos.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#define bool unsigned char
#define true (1)
#define false (0)

#define NOTE_S 12
#define DELAY_S 11
#define TEXT_S 256

unsigned long StrToUnsignedLong(char* str)
{
    long ll=atol(str);
    if(ll>0){return (unsigned long)ll;}
    else    {return 0;}
}
void ZeroMem(char cs[],int L)//Clear Memory(memory,length of memory)
{
    for(int i=0;i<L;i++)
    {
        cs[i]=0;
    }
}
char* strrpc(char* str,char* oldstr,char* newstr)
{
    char bstr[256];
    ZeroMem(bstr,256);
    for(int i = 0;i < strlen(str);i++)
    {
        if(!strncmp(str+i,oldstr,strlen(oldstr)))
        {
            strcat(bstr,newstr);
            i+=strlen(oldstr);
        }
        strncat(bstr,str + i,1);
    }
    strcpy(str,bstr);
    return str;
}
unsigned long denote(char cs[])//decode note(note id) -> rate of note
{
    if(strcmp(cs,"0")==0)return 0;//stop
    else if(strcmp(cs,".1")==0)return 262;
    else if(strcmp(cs,".2")==0)return 294;
    else if(strcmp(cs,".3")==0)return 330;
    else if(strcmp(cs,".4")==0)return 350;
    else if(strcmp(cs,".5")==0)return 392;
    else if(strcmp(cs,".6")==0)return 440;
    else if(strcmp(cs,".7")==0)return 494;
    else if(strcmp(cs,"1")==0)return 523;
    else if(strcmp(cs,"2")==0)return 578;
    else if(strcmp(cs,"3")==0)return 659;
    else if(strcmp(cs,"4")==0)return 698;
    else if(strcmp(cs,"5")==0)return 784;
    else if(strcmp(cs,"6")==0)return 880;
    else if(strcmp(cs,"7")==0)return 998;
    else if(strcmp(cs,"1.")==0)return 1046;
    else if(strcmp(cs,"2.")==0)return 1175;
    else if(strcmp(cs,"3.")==0)return 1318;
    else if(strcmp(cs,"4.")==0)return 1400;
    else if(strcmp(cs,"5.")==0)return 1568;
    else if(strcmp(cs,"6.")==0)return 1760;
    else if(strcmp(cs,"7.")==0)return 1976;
    else if(strlen(cs)>1)
    {
        if(cs[0]=='r')
        {
            return StrToUnsignedLong(cs+1);
        }
        else
        {
            return 0;//error
        }
    }
    else return 0;//error
}
void beep(unsigned long h,unsigned long dly)//beep(rate,delay)
{
    if(h==0)
    {
        nosound();
    }
    else
    {
        sound(h);
    }
    delay(dly);
}
struct Note
{
    unsigned long v;//rate(Hz)
    unsigned long t;//delay time(ms)
    char text[256];//print text
};
bool readline(FILE* fp,char buff[],unsigned long length)
{
    ZeroMem(buff,length);
    int l=0;
    char c=0;
    while(1)
    {
        c=fgetc(fp);
        if(c==EOF)
        {
            return false;
        }
        if(c!=1 && c)
        {
            if(c=='\n'){return true;}
            else if(l<length)
            {
                buff[l]=c;
                l++;
            }
            else{return true;}
        }
    }
}
//Chinese:音符："伴奏音 主旋律 时长" -> 会忽略伴奏音，只播放主旋律
Note split(char line[])
{
    char sNote[NOTE_S];   char sDelay[DELAY_S];   char sText[TEXT_S];
    ZeroMem(sNote,NOTE_S);ZeroMem(sDelay,DELAY_S);ZeroMem(sText,TEXT_S);
    unsigned char mode=0;
    int sI=0;
    for(int i=0;i<strlen(line);i++)
    {
        if(line[i])
        {
            if(line[i]==' ')
            {
                mode++;sI=0;
            }
            else if(mode==0)
            {
                sNote[sI]=line[i];
                sI++;
            }
            else if(mode==2)
            {
                sDelay[sI]=line[i];
                sI++;
            }
            else if(mode==3)
            {
                sText[sI]=line[i];
                sI++;
            }
        }
    }
    Note n;
    if(strcmp(sNote,"#")!=0)
    {
        n.v=denote(sNote);
        n.t=StrToUnsignedLong(sDelay);
        strcpy(n.text,sText);
    }
    else
    {
        n.v=0;
        n.t=0;
        strcpy(n.text,"");
    }
    return n;
}
int main(int argc,char* argv[])//MusicPlayer MS-DOS
{
    /*WARNING:
     * length of ANY line <=276!
     * only GBK text file!
     * main melody note -> strlen<=11!
     * main melody time -> strlen<=10!
     * text             -> strlen<=255!
     * usage:mp.exe <music file(text)>
     * don't press Control-C when playing!
     * if you press Control-C,input "mp.exe" to stop sound.
    */
    if(argc>1)
    {
        printf("open %s...\n",argv[1]);
    }
    else
    {
        printf("usage:mp.exe <music file(text)>\n");
        nosound();
        return 0;
    }
    FILE* f;
    f=fopen(argv[1],"r");
    //-----------------main--------------
    char data[276];
    while(readline(f,data,276))
    {
        Note n=split(data);
        printf(strrpc(strrpc(strrpc(strrpc(strrpc(strrpc(strrpc(n.text,"\\n","\n"),"\\t","\t"),"|",""),"\\|","|"),"~"," "),"\\|","|"),"\\~","~"));
        beep(n.v,n.t);
    }
    //------------------------------------

    printf("\n");
    fclose(f);
    nosound();
    return 0;
}
