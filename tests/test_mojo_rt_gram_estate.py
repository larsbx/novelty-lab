"""Exact independent consumer oracle for pinned Mojo Gram/exterior invariants.

Reads byte-identical upstream fixture, reconstructs Gram determinants and
3x3 coordinate minors using plain Python integers. This is deliberately
non-authoritative with respect to the estate Mojo mathematical kernels.
"""
import hashlib
import itertools
import pathlib
import tomllib
import unittest

from experiments.rt.independent_reference import SplitQuadratic8, triple_spread_defect

GUARDS_CONTRACT = "Immutable Mojo Gram/minor source and 18-case exact differential vectors"

ROOT=pathlib.Path(__file__).parents[1]
SOURCE="3bb94d317b8f0712591b33f9657cf3a0e54207cd"
FIXTURE=ROOT/"tests/fixtures/gram_geometry_v1.txt"
FIXTURE_BLOB="bd33bd5b82077a7a70a5a65f372809ea54a1f6ce"


def det3(rows):
    a,b,c=rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def coordinate_rank2(p,x,y,z):
    return int(all(det3([[v[i] for v in (x,y,z)],
                          [v[j] for v in (x,y,z)],
                          [v[k] for v in (x,y,z)]])%p==0
                   for i,j,k in itertools.combinations(range(8),3)))


class TestMojoGramEstate(unittest.TestCase):
    def test_pinned_canonical_source(self):
        m=tomllib.loads((ROOT/"vendored.toml").read_text(encoding="utf-8"))
        packages={p["name"]:p for p in m["package"]}
        for name in ("finite_exact","projective_limits","parallel_fold"):
            pkg=packages[name]
            self.assertEqual(pkg["commit"],SOURCE)
            self.assertEqual(pkg["root"],"vendor/mojo")
        self.assertIn("projective_limits/gram_geometry.mojo",packages["projective_limits"]["files"])
        self.assertEqual(
            dict((d["id"],d) for d in tomllib.loads((ROOT/"ESTATE.toml").read_text())["dep"])["finite-math-kernels"]["rev"],
            SOURCE,
        )

    def test_18_exact_vectors_and_falsifiers(self):
        data=FIXTURE.read_bytes()
        git_sha=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        self.assertEqual(git_sha,FIXTURE_BLOB)
        lines=[line.split("\t") for line in data.decode().splitlines() if line and not line.startswith("#")]
        self.assertEqual(len(lines),18)
        for c in lines:
            self.assertEqual(len(c),11)
            _,ptext,label,rawx,rawy,rawz,g2,g3,rank,norm_ratio,defect=c
            p=int(ptext)
            x,y,z=(tuple(map(int,v.split(","))) for v in (rawx,rawy,rawz))
            f=SplitQuadratic8(p)
            def gram(a,b): return (f.polar(a,b)*pow(2,-1,p))%p
            def gram2(a,b): return (f.norm(a)*f.norm(b)-gram(a,b)**2)%p
            G=[[gram(a,b) for b in (x,y,z)] for a in (x,y,z)]
            gram3=det3(G)%p
            r2=coordinate_rank2(p,x,y,z)
            den=f.norm(x)*f.norm(y)*f.norm(z)%p
            normalized=None if den==0 else gram3*pow(den,-1,p)%p
            s=[f.spread(x,y),f.spread(y,z),f.spread(z,x)]
            td=None if r2==0 or any(value is None for value in s) else triple_spread_defect(*s,p)
            self.assertEqual(gram2(x,y),int(g2),(p,label,"gram2"))
            self.assertEqual(gram3,int(g3),(p,label,"gram3"))
            self.assertEqual(r2,int(rank),(p,label,"rank"))
            self.assertEqual(normalized,None if norm_ratio=="rejected" else int(norm_ratio))
            self.assertEqual(td,None if defect=="rejected" else int(defect))
            if label=="radical":
                self.assertEqual((gram3,r2),(0,0))
            if label=="tangent":
                self.assertEqual(gram2(x,y),0)


if __name__=="__main__":
    unittest.main()
