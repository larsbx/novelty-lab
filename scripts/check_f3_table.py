#!/usr/bin/env python3
"""Rebuild the F3 Cayley-Dickson basis tensor and check its canonical digest."""
import hashlib, json

P=3
def add(x,y): return tuple((a+b)%P for a,b in zip(x,y))
def neg(x): return tuple((-a)%P for a in x)
def sub(x,y): return add(x,neg(y))
def conj(x):
    if len(x)==1: return x
    h=len(x)//2; return conj(x[:h])+neg(x[h:])
def mul(x,y):
    if len(x)==1: return (x[0]*y[0]%P,)
    h=len(x)//2; a,b=x[:h],x[h:]; c,d=y[:h],y[h:]
    return sub(mul(a,c),mul(conj(d),b))+add(mul(d,a),mul(b,conj(c)))
B=[tuple(1 if i==j else 0 for i in range(8)) for j in range(8)]
TABLE=[[list(mul(B[i],B[j])) for j in range(8)] for i in range(8)]
EXPECTED="747ace028b8a34fb95f5b7c39e99f3004e39ad4fb3401a7caa3b6e3a4e2e2f4b"
payload=json.dumps({"modulus":P,"table":TABLE},sort_keys=True,separators=(",",":")).encode()
actual=hashlib.sha256(payload).hexdigest()
if actual!=EXPECTED: raise SystemExit(f"tensor digest mismatch: {actual}")
print(f"verified F3 tensor provenance {actual}")
