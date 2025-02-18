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
        self.tg=0
        self.th=0
        self.ti=0
        self.tk=0
        self.numin=0
        self.nmode=False
        self.wordlist=[]
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
        for i in range(768):
            self.wordlist.append('')
    def rcore_t_s(self):
        self.t=self.stack.pop()
    def rcore_s_t(self):
        self.stack.append(self.t)
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
    def rcore_not(self):
        if self.tk == 0:
            self.tk=1
        else:
            self.tk=0
    def rcore_or(self):
        if self.ti == 0 and self.tk == 0:
            self.tk=0
        else:
            self.tk=1
    def rcore_and(self):
        if self.ti != 0 and self.tk != 0:
            self.tk=1
        else:
            self.tk=0
    def rcore_xor(self):
        if self.ti == 0 and self.tk == 0:
            self.tk=0
        elif self.ti != 0 and self.tk != 0:
            self.tk=0
        else:
            self.tk=1
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
    def rmath_t_ti_add(self):
        self.t=self.t+self.ti
    def rmath_t_ti_mul(self):
        self.t=self.t*self.ti
    def rmath_t_ti_idiv(self):
        self.t=self.t//self.ti
    def rmath_t_ti_mod(self):
        self.t=self.t%self.ti
    def rmath_t_ti_pow(self):
        from math import floor
        self.t=floor(pow(self.t,self.ti))
    def rmath_t_ti_log(self):
        from math import floor,log
        self.t=floor(log(self.t,self.ti))
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
            d.append(a)
            self.buf_in_get()
            a=self.buf_in_pop()
        while a >= 48 and a <= 57:
            b=b*10+(a-48)
            self.buf_in_get()
            a=self.buf_in_pop()
        self.t=a
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
        if gch[0] >= 48 and gch[0] <= 57:
            self.nmode=True
            self.numin=self.numin*16+(gch[0]-48)
        elif gch[0] >= 97 and gch[0] <= 102:
            self.nmode=True
            self.numin=self.numin*16+(gch[0]-87)
        elif self.nmode == True:
            self.nmode=False
            self.stack.append(self.numin)
            self.numin=0
        else:
            pass
        if self.nmode == True:
            pass
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
        elif gch==b'n':
            self.rcore_not()
        elif gch==b'N':
            self.rcore_and()
        elif gch==b'o':
            self.rcore_or()
        elif gch==b'O':
            self.rcore_xor()
        elif gch==b's':
            self.rcore_t_s()
        elif gch==b'S':
            self.rcore_s_t()
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
            self.rmath_t_ti_add()
        elif gch==b'*':
            self.rmath_t_ti_mul()
        elif gch==b'/':
            self.rmath_t_ti_idiv()
        elif gch==b'%':
            self.rmath_t_ti_mod()
        elif gch==b'p':
            self.rmath_t_ti_pow()
        elif gch==b'l':
            self.rmath_t_ti_log()
        elif gch==b'u':
            self.rxtra_t_uptime_s()
        elif gch==b'U':
            self.rxtra_t_uptime_ns()
        elif gch==b'r':
            self.rxtra_t_randint()
        elif gch==b'R':
            self.rxtra_t_randseed()
        elif gch==b'x':
            self.rxtio_t_in_char()
        elif gch==b'X':
            self.rxtio_t_in_int()
        elif gch==b'y':
            self.rxtio_t_out_char()
        elif gch==b'Y':
            self.rxtio_t_out_int()
        else:
            pass
        return ret
    def run_pair(self,cmp):
        runw=0
        if ord(cmp[0]) >= 48 and ord(cmp[0]) <= 57:
            if ord(cmp[1]) >= 48 and ord(cmp[1]) <= 57:
                self.stack.append((ord(cmp[0])-48)*16+(ord(cmp[1])-48))
            elif ord(cmp[1]) >= 97 and ord(cmp[1]) <= 102:
                self.stack.append((ord(cmp[0])-48)*16+(ord(cmp[1])-87))
            else:
                pass
        elif ord(cmp[0]) >= 97 and ord(cmp[0]) <= 102:
            if ord(cmp[1]) >= 48 and ord(cmp[1]) <= 57:
                self.stack.append((ord(cmp[0])-87)*16+(ord(cmp[1])-48))
            elif ord(cmp[1]) >= 97 and ord(cmp[1]) <= 102:
                self.stack.append((ord(cmp[0])-87)*16+(ord(cmp[1])-87))
            else:
                pass
        elif cmp[0]=='"':
            self.stack.append(ord(cmp[1])%128)
        elif ord(cmp[0]) >= 65 and ord(cmp[0]) <= 70:
            wnum=(ord(cmp[0])-65)*128+ord(cmp[1])%128
            for lc in range(len(self.wordlist[wnum])):
                cmdch = self.wordlist[wnum][lc]
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
        self.tg=0
        self.th=0
        self.ti=0
        self.tk=0
        self.numin=0
        self.nmode=False
        if len(line) == 0:
            pass
        elif line[0]==':' and (ord(line[1]) >= 65 and ord(line[1]) <= 70) and ord(line[2]) < 128:
            wnum=(ord(line[1])-65)*128+ord(line[2])%128
            self.wordlist[wnum]=line[4:]
        elif line[0]=='"' and len(line) > 1:
            for i in range(len(line)-1):
                self.stack.append(ord(line[len(line)-i-1]))
        elif line[0]=='#':
            pass
        elif line[0]==';' and len(line) > 2:
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
