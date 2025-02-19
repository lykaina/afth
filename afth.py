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
        self.stack=[]
        self.stack2=[]
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
        self.varlist=[]
        self.bigarray=[]
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
    def wordnum_encode(self,s=b''):
        scale=[2444,232180,21827364,2051774660]
        wn=scale[3]
        if len(s) < 2 or len(s) > 5:
            pass
        elif len(s)==2:
            wn=(s[0]-65)*94+(s[1]-33)
        elif len(s)==3:
            wn=scale[0]+(s[0]-65)*94*94+(s[1]-33)*94+(s[2]-33)
        elif len(s)==4:
            wn=scale[1]+(s[0]-65)*94*94*94+(s[1]-33)*94*94+(s[2]-33)*94+(s[3]-33)
        elif len(s)==5:
            wn=scale[2]+(s[0]-65)*94*94*94*94+(s[1]-33)*94*94*94+(s[2]-33)*94*94+(s[3]-33)*94+(s[4]-33)
        else:
            pass
        return wn
    def wordnum_decode(self,wn=2051774660):
        scale=[2444,232180,21827364,2051774660]
        if wn>=scale[3]:
            return b'A!!!!!'
        elif wn < scale[0]:
            return (chr(wn//94+65)+chr(wn%94+33)).encode()
        elif wn < scale[1]:
            return (chr((wn-scale[0])//(94*94)+65)+chr(((wn-scale[0])//94)%94+33)+chr((wn-scale[0])%94+33)).encode()
        elif wn < scale[2]:
            return (chr((wn-scale[1])//(94*94*94)+65)+chr(((wn-scale[1])//(94*94))%94+33)+chr(((wn-scale[1])//94)%94+33)+chr((wn-scale[1])%94+33)).encode()
        else:
            return (chr((wn-scale[2])//(94*94*94*94)+65)+chr(((wn-scale[2])//(94*94*94))%94+33)+chr(((wn-scale[2])//(94*94))%94+33)+chr(((wn-scale[2])//94)%94+33)+chr((wn-scale[2])%94+33)).encode()
    def varnum_encode(self,s=b''):
        scale=[94,8930,839514,78914410]
        wn=scale[3]
        if len(s) < 1 or len(s) > 4:
            pass
        elif len(s)==1:
            n=(s[0]-33)
        elif len(s)==2:
            n=scale[0]+(s[0]-33)*94+(s[1]-33)
        elif len(s)==3:
            n=scale[1]+(s[0]-33)*94*94+(s[1]-33)*94+(s[2]-33)
        elif len(s)==4:
            n=scale[2]+(s[0]-33)*94*94*94+(s[1]-33)*94*94+(s[2]-33)*94+(s[3]-33)
        else:
            pass
        return n
    def varnum_decode(self,n=78914410):
        scale=[94,8930,839514,78914410]
        if n>=scale[3]:
            return b'!!!!!'
        elif n < scale[0]:
            return (chr(n+33)).encode()
        elif n < scale[1]:
            return (chr(((n-scale[0])//94)%94+33)+chr((n-scale[0])%94+33)).encode()
        elif n < scale[2]:
            return (chr(((n-scale[1])//(94*94))%94+33)+chr(((n-scale[1])//94)%94+33)+chr((n-scale[1])%94+33)).encode()
        else:
            return (chr(((n-scale[2])//(94*94*94))%94+33)+chr(((n-scale[2])//(94*94))%94+33)+chr(((n-scale[2])//94)%94+33)+chr((n-scale[2])%94+33)).encode()
    def wordlist_append(self,s,cs):
        self.wordlist.append([self.wordnum_encode(s.encode()),cs])
    def varlist_append(self,s,n):
        self.varlist.append([self.varnum_encode(s.encode()),n])
    def make_wordlist(self):
        self.wordlist_append('NUL',' ')
        self.wordlist_append('A+','sLs+S')
        self.wordlist_append('A-','s-Ls+S')
        self.wordlist_append('A*','sLs*S')
        self.wordlist_append('A/','sLs/S')
        self.wordlist_append('A%','sLs%S')
        self.wordlist_append('Ic','wS')
        self.wordlist_append('Oc','sy')
        self.wordlist_append('Id','WS')
        self.wordlist_append('Od','sY')
        self.wordlist_append('Ih','mS')
        self.wordlist_append('Oh','sM')
        self.wordlist_append('END','_q')
        self.wordlist_append('ABS','s|S')
        self.wordlist_append('NEG','s|-S')
    def make_varlist(self):
        self.varlist.append([2147483647,0])
    def make_bigarray(self):
        i=0
        for i in range(16384):
            self.bigarray.append(0)
    def rcore_t_s(self):
        self.t=self.stack.pop()
    def rcore_s_t(self):
        self.stack.append(self.t)
    def rcore_t_s2(self):
        self.t=self.stack2.pop()
    def rcore_s2_t(self):
        self.stack2.append(self.t)
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
    def rcore_quit(self):
        from sys import exit as sys_exit
        sys_exit(self.t)
    def rcore_quit_ifkz(self):
        from sys import exit as sys_exit
        if self.tk==0:
            sys_exit(self.t)
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
    def rbarr_t_b_tl(self):
        self.t=self.bigarray[self.ti]
    def rbarr_b_t_tl(self):
        self.bigarray[self.ti]=self.t
    def rbarr_t_wordnum_tl_b(self):
        i=0
        t=self.t % 4
        tl=self.tl
        d=chr(self.bigarray[ti]%128)
        for i in range(t+1):
            d=d+chr(self.bigarray[tl+i+1])
        self.t=self.wordnum_encode(d.encode())
        self.tl=tl+i+1
    def rbarr_t_varnum_tl_b(self):
        d=''
        i=0
        t=self.t % 4
        tl=self.tl
        for i in range(t+1):
            d=d+chr(self.bigarray[tl+i])
        self.t=self.varnum_encode(d.encode())
        self.tl=tl+i+1
    def rbarr_word_b(self):
        t=self.t
        wn=self.bigarray[t]
        t=t+1
        d=''
        c=chr(self.bigarray[t]%128)
        while ord(c) >= 33 and ord(c) <= 127:
            t=t+1
            d=d+c
            c=chr(self.bigarray[t]%128)
        d=d+c
        self.wordlist.append([wn,d])
        self.t=t
    def rbarr_var_b(self):
        t=self.t
        vn=self.bigarray[t]
        t=t+1
        v=self.bigarray[t]
        self.varlist.append([vn,v])
        self.t=t
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
    def rmeta_t_var(self):
        t=self.t
        i=0
        vnum=0
        for i in range(len(self.varlist)):
            if t == self.varlist[i][0]:
                vnum=i
        self.t=self.wordlist[vnum][1]
    def run_char_meta(self,gmch=b' '):
        _ret=0
        if gmch==b' ':
            pass
        elif gmch==b's':
            self.rcore_t_s()
        elif gmch==b'S':
            self.rcore_s_t()
        elif gmch==b't':
            self.rcore_t_s2()
        elif gmch==b'T':
            self.rcore_s2_t()
        elif gmch==b'f':
            self.rcore_t_f()
        elif gmch==b'F':
            self.rcore_f_t()
        elif gmch==b'g':
            self.rcore_t_g()
        elif gmch==b'G':
            self.rcore_g_t()
        elif gmch==b'h':
            self.rcore_t_h()
        elif gmch==b'H':
            self.rcore_h_t()
        elif gmch==b'i':
            self.rcore_t_i()
        elif gmch==b'I':
            self.rcore_i_t()
        elif gmch==b'j':
            self.rcore_jnz_r()
        elif gmch==b'J':
            self.rcore_jnz_a()
        elif gmch==b'k':
            self.rcore_t_k()
        elif gmch==b'K':
            self.rcore_k_t()
        elif gmch==b'l':
            self.rcore_t_l()
        elif gmch==b'L':
            self.rcore_l_t()
        elif gmch==b'q':
            self.rcore_quit()
        elif gmch==b'Q':
            self.rcore_quit_ifkz()
        elif gmch==b'n':
            self.rcore_not_tk()
        elif gmch==b'a':
            self.rcore_and_tk()
        elif gmch==b'o':
            self.rcore_or_tk()
        elif gmch==b'x':
            self.rcore_xor_tk()
        elif gmch==b'N':
            self.rcore_not_tl()
        elif gmch==b'A':
            self.rcore_and_tl()
        elif gmch==b'O':
            self.rcore_or_tl()
        elif gmch==b'X':
            self.rcore_xor_tl()
        elif gmch==b'z':
            self.rcore_zte()
        elif gmch==b'Z':
            self.rcore_ztg()
        elif gmch==b'_':
            self.rcore_t_zero()
        elif gmch==b'^':
            self.rcore_t_inc()
        elif gmch==b'v':
            self.rcore_t_dec()
        elif gmch==b'<':
            self.rcore_t_shl()
        elif gmch==b'>':
            self.rcore_t_shr()
        elif gmch==b'|':
            self.rcore_t_abs()
        elif gmch==b'-':
            self.rcore_t_flipsign()
        elif gmch==b'+':
            self.rmath_t_tl_add()
        elif gmch==b'*':
            self.rmath_t_tl_mul()
        elif gmch==b'/':
            self.rmath_t_tl_idiv()
        elif gmch==b'%':
            self.rmath_t_tl_mod()
        elif gmch==b'p':
            self.rmath_t_tl_pow()
        elif gmch==b'P':
            self.rmath_t_tl_log()
        elif gmch==b'b':
            self.rbarr_t_b_tl()
        elif gmch==b'B':
            self.rbarr_b_t_tl()
        elif gmch==b'c':
            self.rbarr_t_wordnum_tl_b()
        elif gmch==b'C':
            self.rbarr_t_varnum_tl_b()
        elif gmch==b'd':
            self.rbarr_word_b()
        elif gmch==b'D':
            self.rbarr_var_b()
        elif gmch==b'u':
            self.rxtra_t_uptime_s()
        elif gmch==b'U':
            self.rxtra_t_uptime_ns()
        elif gmch==b'r':
            self.rxtra_t_randint()
        elif gmch==b'R':
            self.rxtra_t_randseed()
        elif gmch==b'w':
            self.rxtio_t_in_char()
        elif gmch==b'W':
            self.rxtio_t_in_int()
        elif gmch==b'y':
            self.rxtio_t_out_char()
        elif gmch==b'Y':
            self.rxtio_t_out_int()
        elif gmch==b'm':
            self.rxtio_t_in_hex()
        elif gmch==b'M':
            self.rxtio_t_out_hex()
        elif gmch==b'E':
            self.rmeta_t_var()
        else:
            pass
        return _ret
    def rmeta_run_word_t(self):
        _t=self.t
        _i=0
        _runw=0
        _wnum=0
        for _i in range(len(self.wordlist)):
            if _t == self.wordlist[i][0]:
                _wnum=_i
        for _lc in range(len(self.wordlist[wnum][1])):
            _cmdch = self.wordlist[_wnum][1][_lc]
            _runw=_runw+self.run_char_meta(_cmdch.encode())
            self.buf_out()
        self.t=_runw%256
    def run_char(self,gch=b' '):
        ret=0
        if gch==b' ':
            pass
        elif gch==b's':
            self.rcore_t_s()
        elif gch==b'S':
            self.rcore_s_t()
        elif gch==b't':
            self.rcore_t_s2()
        elif gch==b'T':
            self.rcore_s2_t()
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
        elif gch==b'q':
            self.rcore_quit()
        elif gch==b'Q':
            self.rcore_quit_ifkz()
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
        elif gch==b'b':
            self.rbarr_t_b_tl()
        elif gch==b'B':
            self.rbarr_b_t_tl()
        elif gch==b'c':
            self.rbarr_t_wordnum_tl_b()
        elif gch==b'C':
            self.rbarr_t_varnum_tl_b()
        elif gch==b'd':
            self.rbarr_word_b()
        elif gch==b'D':
            self.rbarr_var_b()
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
        elif gch==b'm':
            self.rxtio_t_in_hex()
        elif gch==b'M':
            self.rxtio_t_out_hex()
        elif gch==b'e':
            self.rmeta_run_word_t()
        elif gch==b'E':
            self.rmeta_t_var()
        else:
            pass
        return ret
    def run_tri(self,cmp):
        runw=0
        if cmp[0]==';':
            pass
        elif cmp[0]=="'" and len(cmp)>=2:
            self.stack.append(ord(cmp[1])%128)
        elif cmp[0]=='<':
            vn=varnum_decode(cmp[1:].encode())
            vln=0
            for i in range(len(self.varlist)):
                if self.varlist[i][0]==vn:
                    vln=i
            self.stack.append(self.varlist[vln][1])
        elif cmp[0]=='>':
            vn=varnum_decode(cmp[1:].encode())
            vln=0
            for i in range(len(self.varlist)):
                if self.varlist[i][0]==vn:
                    vln=i
            self.varlist[vn][1]=self.stack.pop()
        elif cmp[0]=='=':
            vn=varnum_encode(cmp[1:].encode())
            vln=0
            for i in range(len(self.varlist)):
                if self.varlist[i][0]==vn:
                    vln=i
            self.varlist[vn][1]=self.stack.pop()
            self.stack.append(self.varlist[vln][1])
        elif cmp[0]=='+' and len(cmp) >= 2:
            v=0
            vstop=False
            for i in range(len(cmp)-1):
                if vstop==True:
                    pass
                elif ord(cmp[1+i]) >= 48 and ord(cmp[1+i]) <= 57:
                    v=v*16+(ord(cmp[1+i])-48)
                elif ord(cmp[1+i]) >= 65 and ord(cmp[1+i]) <= 70:
                    v=v*16+(ord(cmp[1+i])-55)
                elif ord(cmp[1+i]) >= 97 and ord(cmp[1+i]) <= 102:
                    v=v*16+(ord(cmp[1+i])-87)
                else:
                    vstop=True
            self.stack.append(v)
        elif ord(cmp[0]) >= 65 and ord(cmp[0]) <= 90:
            wn=self.wordnum_encode(cmp.encode())
            wnum=0
            for i in range(len(self.wordlist)):
                if self.wordlist[i][0]==wn:
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
        elif line[0]==':' and (ord(line[1]) >= 65 and ord(line[1]) <= 90):
            lines=line.split(' ')
            self.wordlist_append(lines[0][1:],lines[1])
        elif line[0]=='$' and ord(line[1]) >= 33 and ord(line[1]) <= 127:
            lines=line.split(' ')
            vname=lines[0][1:]
            v=0
            vstop=False
            for i in range(len(lines[1])):
                if vstop==True:
                    pass
                elif ord(lines[1][i]) >= 48 and ord(lines[1][i]) <= 57:
                    v=v*16+(ord(lines[1][i])-48)
                elif ord(lines[1][i]) >= 65 and ord(line[1][i]) <= 70:
                    v=v*16+(ord(lines[1][i])-55)
                elif ord(lines[1][i]) >= 97 and ord(lines[1][i]) <= 102:
                    v=v*16+(ord(lines[1][i])-87)
                else:
                    vstop=True
            self.varlist_append(vname,v)
        elif line[0]=='"' and len(line) >= 2:
            line2=line[1:]
            for i in range(len(line2)):
                self.stack.append(ord(line2[len(line2)-i-1]))
        elif line[0]=='!':
            for lc in range(len(line)-1):
                cmdch = line[lc+1]
                runl=self.run_char(cmdch.encode())
                self.buf_out()
        elif line[0]=='#':
            pass
        elif len(line)%4 == 3:
            runp=0
            lines=line.split(' ')
            for i in range(len(lines)):
                cmdtri=lines[i]
                runp=runp+self.run_tri(cmdtri)
            runl=runp%256
        else:
            pass
        if self.j==False:
            self.lnum=self.lnum+1
        return runl
    def run_file(self):
        runf=0
        self.make_wordlist()
        self.make_varlist()
        self.make_bigarray()
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
