'''
Afth Interpreter v0.1-alpha Library

Copyright (c) 2025 Sara Berman

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
'''

class AFTH:
    def __init__(self,fname):
        from sys import stdin, stdout
        self.fname=fname
        self.stack=[0,0,0]
        self.ibuf=b''
        self.obuf=b''
        self.lnum=0
        self.lchar=0
        self.stdin=stdin
        self.stdout=stdout
        self.flst=[]
        self.j=False
        self.t=0
        self.tf=0
        self.tg=0
        self.th=0
        self.ti=0
        self.tk=0
        self.tl=0
        self.numin=0
        self.nmode=False
        self.wordlist=[]
        self.varis=[]
        self.var=[]
    def buf_in(self):
        _in=self.stdin.read(1)
        if _in == None or _in == '':
            pass
        else:
            self.ibuf=self.ibuf+_in.encode()
    def buf_in_pop(self):
        _r=self.ibuf[0]
        if len(self.ibuf) > 1:
            self.ibuf=self.ibuf[1:]
        else:
            self.ibuf=b''
        #if _r == 13:
        #    _r = 10
        #else:
        #    pass
        return _r
    def buf_in_get(self):
        while self.ibuf == b'':
            self.buf_in()
    def buf_out(self):
        while len(self.obuf) > 1:
            self.stdout.write(chr(self.obuf[0]))
            self.obuf=self.obuf[1:]
        if len(self.obuf) == 1:
            self.stdout.write(chr(self.obuf[0]))
            self.obuf=b''
    def buf_out_put(self,chin):
        if chin.encode() == b'\n':
            self.obuf=self.obuf+b'\n'
        else:
            self.obuf=self.obuf+chin.encode()
    def open_file(self):
        befile = open(self.fname,'rt')
        befile_lst = befile.readlines()
        befile.close()
        del befile
        flst = []
        i=0
        for i in range(len(befile_lst)):
            flst.append(befile_lst[i].strip('\n').strip('\r'))
        del befile_lst
        self.flst=flst
        del flst
    def make_wordlist(self):
        self.wordlist.append(['  ',' '])
        self.wordlist.append(['A+','sLs+S'])
        self.wordlist.append(['A-','s-Ls+S'])
        self.wordlist.append(['A*','sLs*S'])
        self.wordlist.append(['A/','sLs/S'])
        self.wordlist.append(['A%','sLs%S'])
        self.wordlist.append(['Ci','wS'])
        self.wordlist.append(['Co','sy'])
        self.wordlist.append(['Ii','WS'])
        self.wordlist.append(['Io','sY'])
    def make_varlist(self):
        for i in range(128):
            self.varis.append(False)
            self.var.append(0)
    def rcore_t_s(self):
        self.t=self.stack.pop()
    def rcore_s_t(self):
        self.stack.append(self.t)
    def rcore_t_f(self):
        self.t=self.tf
    def rcore_f_t(self):
        self.tf=self.t
    def rcore_t_g(self):
        self.t=self.tg
    def rcore_g_t(self):
        self.tg=self.t
    def rcore_t_h(self):
        self.t=self.th
    def rcore_h_t(self):
        self.th=self.t
    def rcore_t_i(self):
        self.t=self.ti
    def rcore_i_t(self):
        self.ti=self.t
    def rcore_t_k(self):
        self.t=self.tk
    def rcore_k_t(self):
        self.tk=self.t
    def rcore_t_l(self):
        self.t=self.tl
    def rcore_l_t(self):
        self.tl=self.t
    def rcore_zte(self):
        if self.t == 0:
            self.tk=1
        else:
            self.tk=0
    def rcore_ztg(self):
        if self.t > 0:
            self.tk=1
        else:
            self.tk=0
    def rcore_not_tk(self):
        if self.tk == 0:
            self.tk=1
        else:
            self.tk=0
    def rcore_or_tk(self):
        if self.tl == 0 and self.tk == 0:
            self.tk=0
        else:
            self.tk=1
    def rcore_and_tk(self):
        if self.tl != 0 and self.tk != 0:
            self.tk=1
        else:
            self.tk=0
    def rcore_xor_tk(self):
        if self.tl == 0 and self.tk == 0:
            self.tk=0
        elif self.tl != 0 and self.tk != 0:
            self.tk=0
        else:
            self.tk=1
    def rcore_not_tl(self):
        if self.tk == 0:
            self.tl=1
        else:
            self.tl=0
    def rcore_or_tl(self):
        if self.tl == 0 and self.tk == 0:
            self.tl=0
        else:
            self.tl=1
    def rcore_and_tl(self):
        if self.tl != 0 and self.tk != 0:
            self.tl=1
        else:
            self.tl=0
    def rcore_xor_tl(self):
        if self.tl == 0 and self.tk == 0:
            self.tl=0
        elif self.tl != 0 and self.tk != 0:
            self.tl=0
        else:
            self.tl=1
    def rcore_jnz_r(self):
        if self.tk != 0:
            self.lnum=self.lnum+self.t
            self.j=True
        else:
            pass
    def rcore_jnz_a(self):
        if self.tk != 0:
            self.lnum=self.t
            self.j=True
        else:
            pass
    def rcore_t_zero(self):
        self.t=0
    def rcore_t_inc(self):
        self.t=self.t+1
    def rcore_t_dec(self):
        self.t=self.t-1
    def rcore_t_shl(self):
        self.t=self.t*2
    def rcore_t_shr(self):
        self.t=self.t//2
    def rcore_t_abs(self):
        self.t=abs(self.t)
    def rcore_t_flipsign(self):
        self.t=self.t*-1
    def rmath_t_tl_add(self):
        self.t=self.t+self.tl
    def rmath_t_tl_mul(self):
        self.t=self.t*self.tl
    def rmath_t_tl_idiv(self):
        self.t=self.t//self.tl
    def rmath_t_tl_mod(self):
        self.t=self.t%self.tl
    def rmath_t_tl_pow(self):
        from math import floor
        self.t=floor(pow(self.t,self.tl))
    def rmath_t_tl_log(self):
        from math import floor,log
        self.t=floor(log(self.t,self.tl))
    def rxtra_t_uptime_s(self):
        from time import monotonic
        self.t=monotonic()
    def rxtra_t_uptime_ns(self):
        from time import monotonic_ns
        self.t=monotonic_ns()%1000000000
    def rxtra_t_randseed(self):
        from random import seed
        seed(self.t)
    def rxtra_t_randint(self):
        from random import randint
        self.t=randint(0,self.t-1)
    def rxtio_t_in_char(self):
        self.buf_in_get()
        self.t=self.buf_in_pop()
    def rxtio_t_in_int(self):
        a=0
        b=0
        d=[]
        self.buf_in_get()
        a=self.buf_in_pop()
        while a < 48 or a > 57:
            self.buf_in_get()
            a=self.buf_in_pop()
        while a >= 48 and a <= 57:
            d.append(a)
            self.buf_in_get()
            a=self.buf_in_pop()
        for i in range(len(d)):
            b=b*10+(d[i]-48)%10
        self.t=b
    def rxtio_t_out_char(self):
        self.buf_out_put(chr(abs(self.t)%128))
    def rxtio_t_out_int(self):
        from math import floor,log
        a=self.t
        j=0
        l=0
        s=0
        o=''
        if a != 0:
            l=floor(log(abs(a),10))
            s=a//abs(a)
        else:
            l=0
            s=1
        if s == -1:
            o=o+'-'
        else:
            pass
        for j in range(l+1):
            o=o+chr(48+(abs(a)//pow(10,l-j))%10)
        o=o+' '
        self.buf_out_put(o)
    def rxtio_t_in_hex(self):
        a=0
        b=0
        d=[]
        self.buf_in_get()
        a=self.buf_in_pop()
        while not ((a >= 48 and a <= 57) or (a >= 65 and a <= 70) or (a >= 97 and a <= 102)):
            self.buf_in_get()
            a=self.buf_in_pop()
        while (a >= 48 and a <= 57) or (a >= 65 and a <= 70) or (a >= 97 and a <= 102):
            d.append(a)
            self.buf_in_get()
            a=self.buf_in_pop()
        for i in range(len(d)):
            if d[i] >= 48 and d[i] <= 57:
                b=b*16+(d[i]-48)
            elif d[i] >= 65 and d[i] <= 70:
                b=b*16+(d[i]-55)
            elif d[i] >= 97 and d[i] <= 102:
                b=b*16+(d[i]-87)
            else:
                pass
        self.t=b
    def rxtio_t_out_hex(self):
        from math import floor,log
        a=self.t
        j=0
        l=0
        s=0
        o=''
        if a != 0:
            l=floor(log(abs(a),16))
            s=a//abs(a)
        else:
            l=0
            s=1
        if s == -1:
            o=o+'-'
        else:
            pass
        for j in range(l+1):
            n=(abs(a)//pow(16,l-j))%16
            if n >= 10:
                o=o+chr(97+n)
            else:
                o=o+chr(48+n)
        o=o+' '
        self.buf_out_put(o)
    def run_char(self,gch=b' '):
        ret=0
        if len(self.stack) == 0:
            self.stack=[0,0,0]
        elif len(self.stack) == 1:
            self.stack=[0,0,self.stack[0]]
        elif len(self.stack) == 2:
            self.stack=[0,self.stack[0],self.stack[1]]
        else:
            pass
        if gch==b' ':
            pass
        elif gch==b's':
            self.rcore_t_s()
        elif gch==b'S':
            self.rcore_s_t()
        elif gch==b'f':
            self.rcore_t_f()
        elif gch==b'F':
            self.rcore_f_t()
        elif gch==b'g':
            self.rcore_t_g()
        elif gch==b'G':
            self.rcore_g_t()
        elif gch==b'h':
            self.rcore_t_h()
        elif gch==b'H':
            self.rcore_h_t()
        elif gch==b'i':
            self.rcore_t_i()
        elif gch==b'I':
            self.rcore_i_t()
        elif gch==b'j':
            self.rcore_jnz_r()
        elif gch==b'J':
            self.rcore_jnz_a()
        elif gch==b'k':
            self.rcore_t_k()
        elif gch==b'K':
            self.rcore_k_t()
        elif gch==b'l':
            self.rcore_t_l()
        elif gch==b'L':
            self.rcore_l_t()
        elif gch==b'n':
            self.rcore_not_tk()
        elif gch==b'a':
            self.rcore_and_tk()
        elif gch==b'o':
            self.rcore_or_tk()
        elif gch==b'x':
            self.rcore_xor_tk()
        elif gch==b'N':
            self.rcore_not_tl()
        elif gch==b'A':
            self.rcore_and_tl()
        elif gch==b'O':
            self.rcore_or_tl()
        elif gch==b'X':
            self.rcore_xor_tl()
        elif gch==b'z':
            self.rcore_zte()
        elif gch==b'Z':
            self.rcore_ztg()
        elif gch==b'_':
            self.rcore_t_zero()
        elif gch==b'^':
            self.rcore_t_inc()
        elif gch==b'v':
            self.rcore_t_dec()
        elif gch==b'<':
            self.rcore_t_shl()
        elif gch==b'>':
            self.rcore_t_shr()
        elif gch==b'|':
            self.rcore_t_abs()
        elif gch==b'-':
            self.rcore_t_flipsign()
        elif gch==b'+':
            self.rmath_t_tl_add()
        elif gch==b'*':
            self.rmath_t_tl_mul()
        elif gch==b'/':
            self.rmath_t_tl_idiv()
        elif gch==b'%':
            self.rmath_t_tl_mod()
        elif gch==b'p':
            self.rmath_t_tl_pow()
        elif gch==b'P':
            self.rmath_t_tl_log()
        elif gch==b'u':
            self.rxtra_t_uptime_s()
        elif gch==b'U':
            self.rxtra_t_uptime_ns()
        elif gch==b'r':
            self.rxtra_t_randint()
        elif gch==b'R':
            self.rxtra_t_randseed()
        elif gch==b'w':
            self.rxtio_t_in_char()
        elif gch==b'W':
            self.rxtio_t_in_int()
        elif gch==b'y':
            self.rxtio_t_out_char()
        elif gch==b'Y':
            self.rxtio_t_out_int()
        elif gch==b'e':
            self.rxtio_t_in_hex()
        elif gch==b'E':
            self.rxtio_t_out_hex()
        else:
            pass
        return ret
    def run_pair(self,cmp):
        runw=0
        if cmp[0]=='"':
            self.stack.append(ord(cmp[1])%128)
        elif cmp[0]=='<':
            if varis[cmp[1]%128]==True:
                self.stack.append(var[cmp[1]%128])
            else:
                pass
        elif cmp[0]=='>':
            if varis[cmp[1]%128]==True:
                var[cmp[1]%128]=self.stack.pop()
            else:
                pass
        elif cmp[0]=='=':
            if varis[cmp[1]%128]==True:
                var[cmp[1]%128]=self.stack.pop()
                self.stack.append(var[cmp[1]%128])
            else:
                pass
        elif ord(cmp[0]) >= 65 and ord(cmp[0]) <= 90:
            wnum=0
            for i in range(len(self.wordlist)):
                if self.wordlist[i][0]==cmp:
                    wnum=i
            for lc in range(len(self.wordlist[wnum][1])):
                cmdch = self.wordlist[wnum][1][lc]
                runw=runw+self.run_char(cmdch.encode())
                self.buf_out()
        else:
            pass
        return runw%256
    def run_line(self,line):
        runl=0
        #ln=self.lnum
        self.j=False
        self.t=0
        self.tf=0
        self.tg=0
        self.th=0
        self.ti=0
        self.tk=0
        self.tl=0
        if len(line) == 0:
            pass
        elif line[0]==':' and (ord(line[1]) >= 65 and ord(line[1]) <= 90) and ord(line[2]) < 128 and len(line) >= 5:
            wname=line[1]+line[2]
            self.wordlist.append([wname,line[4:]])
        elif line[0]=='$' and ord(line[1]) < 128 and len(line) >= 4:
            vnum=ord(line[1])%128
            self.varis[vnum]=True
            v=0
            vstop=False
            for i in range(len(line)-3):
                if vstop==True:
                    pass
                elif ord(line[4+i]) >= 48 and ord(line[4+i]) <= 57:
                    v=v*16+(ord(line[4+i])-48)
                elif ord(line[4+i]) >= 97 and ord(line[4+i]) <= 102:
                    v=v*16+(ord(line[4+i])-87)
                else:
                    vstop=True
            self.var[vnum]=v
        elif line[0]=='=' and len(line) >= 2:
            v=0
            vstop=False
            for i in range(len(line)-1):
                if vstop==True:
                    pass
                elif ord(line[1+i]) >= 48 and ord(line[1+i]) <= 57:
                    v=v*16+(ord(line[1+i])-48)
                elif ord(line[1+i]) >= 97 and ord(line[1+i]) <= 102:
                    v=v*16+(ord(line[1+i])-87)
                else:
                    vstop=True
            self.stack.append(v)
        elif line[0]=='"' and len(line) >= 2:
            for i in range(len(line)-1):
                self.stack.append(ord(line[len(line)-i-1]))
        elif line[0]==';':
            pass
        elif line[0]=='#':
            pass
        elif line[0]=='!' and len(line) > 2:
            runp=0
            for i in range((len(line)-1)//2):
                cmdpair=line[1+(i*2):3+(i*2)]
                runp=runp+self.run_pair(cmdpair)
            runl=runp%256
        elif ord(line[0]) >= 65 and ord(line[0]) <= 70:
            wnum=(ord(line[0])-65)*128+ord(line[1])%128
            for lc in range(len(wordlist[wnum])):
                cmdch = wordlist[wnum][lc]
                runl=self.run_char(cmdch.encode())
                self.buf_out()
        else:
            for lc in range(len(line)):
                cmdch = line[lc]
                runl=self.run_char(cmdch.encode())
                self.buf_out()
        if self.j==False:
            self.lnum=self.lnum+1
        return runl
    def run_file(self):
        runf=0
        self.make_wordlist()
        self.make_varlist()
        l=0
        while l < len(self.flst) and l > -1:
            line = self.flst[l]
            runf=self.run_line(line)
            l=self.lnum
        return runf

def main(file):
    import gc
    from sys import exit as sys_exit
    afth=AFTH(file)
    afth.open_file()
    gc.collect()
    r=afth.run_file()
    del afth
    gc.collect()
    sys_exit(abs(r)%256)
