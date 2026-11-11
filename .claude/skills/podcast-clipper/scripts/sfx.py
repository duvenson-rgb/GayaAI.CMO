#!/usr/bin/env python3
"""Synthesized SFX library. Write a cue list as JSON [[time, "name", dB], ...] and run:
  sfx.py CUES.json OUT.wav DURATION
names: whoosh, whoosh_short, whoosh_long, pop, pop_hi, ding, ding_hi, chime, beep, tick, soft_click,
       impact, impact_short, buzz, shutter, low_tone, swell"""
import sys, json, wave, numpy as np
SR=48000; rng=np.random.default_rng(7)
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-np.maximum(t-a,0)/d)
def lp(x,al):
    y=np.zeros_like(x); acc=0.0
    for i in range(len(x)): acc+=al*(x[i]-acc); y[i]=acc
    return y
def whoosh(dur=.45,f0=300,f1=3000):
    n=int(SR*dur); t=np.arange(n)/SR; x=rng.standard_normal(n); fc=f0+(f1-f0)*np.sin(np.pi*t/dur)**2
    a=1-np.exp(-2*np.pi*fc/SR); y=np.zeros(n); acc=0.0
    for i in range(n): acc+=a[i]*(x[i]-acc); y[i]=acc
    y-=lp(y,.02); y*=np.sin(np.pi*t/dur)**1.5; return y/np.max(np.abs(y))
def pop(f=900,dur=.09): n=int(SR*dur); t=np.arange(n)/SR; fr=f*np.exp(-t*25)+f*.4; return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,.002,.03)
def tone(f,dur,a=.004,d=.25,h=((1,1),)): n=int(SR*dur); t=np.arange(n)/SR; return sum(k2*np.sin(2*np.pi*f*k1*t) for k1,k2 in h)*env(n,a,d)
def beep(f=1800,dur=.08): n=int(SR*dur); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*np.minimum(1,np.minimum(t/.004,(dur-t)/.01))
def tick(): n=int(SR*.03); t=np.arange(n)/SR; return (np.sin(2*np.pi*3200*t)+.5*rng.standard_normal(n))*np.exp(-t/.004)
def click(f=2400): n=int(SR*.04); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)*.6+rng.standard_normal(n)*.25)*np.exp(-t/.006)
def impact(dur=1.2):
    n=int(SR*dur); t=np.arange(n)/SR; f=55+90*np.exp(-t*12)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.35)+lp(rng.standard_normal(n),.08)*np.exp(-t/.05)*.8)/1.3
def buzz(dur=.35):
    n=int(SR*dur); t=np.arange(n)/SR; y=np.sign(np.sin(2*np.pi*110*t))*.5+np.sign(np.sin(2*np.pi*116*t))*.5
    return lp(y,.25)*np.minimum(1,np.minimum(t/.005,(dur-t)/.03))*.8
def shutter():
    n=int(SR*.12); t=np.arange(n)/SR; x=rng.standard_normal(n); return (x*np.exp(-t/.008)+np.roll(x*np.exp(-t/.01),int(SR*.05))*.7)*.6
def swell(dur=.8):
    n=int(SR*dur); t=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*t) for f in (220,330,440))/3*np.sin(np.pi*t/dur)**2
LIB={"whoosh":lambda:whoosh(),"whoosh_short":lambda:whoosh(.3,500,5000),"whoosh_long":lambda:whoosh(.7,200,2500),
 "pop":lambda:pop(900),"pop_hi":lambda:pop(1300,.07),"ding":lambda:tone(1320,1.0,d=.28,h=((1,1),(2.01,.35),(3.02,.15))),
 "ding_hi":lambda:tone(1560,1.0,d=.28,h=((1,1),(2.01,.35))),"chime":lambda:tone(880,2.2,a=.005,d=.7,h=((1,1),(1.5,.35),(2,.15))),
 "beep":lambda:beep(),"tick":tick,"soft_click":lambda:click(),"impact":lambda:impact(),"impact_short":lambda:impact(.7),
 "buzz":lambda:buzz(),"shutter":shutter,"low_tone":lambda:tone(170,1.0,a=.01,d=.35,h=((1,1),(2,.3))),"swell":lambda:swell()}
if __name__=="__main__":
    cues=json.load(open(sys.argv[1])); dur=float(sys.argv[3]); out=np.zeros(int(SR*dur))
    for t,name,db in cues:
        s=LIB[name]()*10**(db/20); i=int(t*SR); j=min(len(out),i+len(s)); out[i:j]+=s[:j-i]
    w=wave.open(sys.argv[2],"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(np.stack([out,out],1),-1,1)*32767).astype(np.int16).tobytes()); w.close()
    print("peak",round(float(abs(out).max()),3))
