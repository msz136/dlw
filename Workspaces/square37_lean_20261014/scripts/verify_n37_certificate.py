"""Independent rational reconstruction, SAT and polygon clipping for n=37.

The source certificate is interpreted only as centers and half-angle parameters.
No source verifier or source separating axes are used.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, itertools, json, math

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'references/n37/n-37.cert'
COMMIT = 'b8c930338ee3577a43faccb52472c6975ab7eccd'
PATH = 'packing/resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-37.cert'
DOT = lambda a,b: a[0]*b[0]+a[1]*b[1]
SUB = lambda a,b: (a[0]-b[0],a[1]-b[1])
CROSS = lambda a,b: a[0]*b[1]-a[1]*b[0]

def vertices(s):
    c,u,v=s['c'],s['u'],s['v']
    return [(c[0]+a*u[0]/2+b*v[0]/2,c[1]+a*u[1]/2+b*v[1]/2)
            for a,b in [(1,1),(-1,1),(-1,-1),(1,-1)]]

def clip(poly, cutter):
    # Independent Sutherland-Hodgman clipping against four oriented polygon edges.
    for a,b in zip(cutter,cutter[1:]+cutter[:1]):
        if not poly: break
        edge=SUB(b,a)
        side=lambda p:CROSS(edge,SUB(p,a))
        out=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            sp,sq=side(p),side(q)
            if sp>=0: out.append(p)
            if (sp<0 and sq>=0) or (sp>=0 and sq<0):
                t=sp/(sp-sq)
                out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
        poly=out
    return poly

def area2(poly):
    return abs(sum((CROSS(p,q) for p,q in zip(poly,poly[1:]+poly[:1])),F(0)))

def main():
    lines=[l for l in SOURCE.read_text().splitlines() if l.strip() and not l.startswith('#')]
    n,rawL=lines[0].split(); n=int(n); originalL=F(rawL)
    # The published decimal upper bound is simpler to present and strictly larger.
    L=F('659861960924437/100000000000000')
    assert n==37 and originalL<=L and len(lines)==n+1
    squares=[];wall_margins=[]; original_wall_margins=[]
    for i,line in enumerate(lines[1:]):
        x,y,t=map(F,line.split());u=((1-t*t)/(1+t*t),2*t/(1+t*t));v=(-u[1],u[0]);c=(x,y)
        assert DOT(u,u)==1 and DOT(v,v)==1 and DOT(u,v)==0 and CROSS(u,v)==1
        hx=(abs(u[0])+abs(v[0]))/2;hy=(abs(u[1])+abs(v[1]))/2
        w=[x-hx,y-hy,L-x-hx,L-y-hy]
        wo=[x-hx,y-hy,originalL-x-hx,originalL-y-hy]
        assert min(w)>=0 and min(wo)>=0
        wall_margins.extend(w);original_wall_margins.extend(wo)
        squares.append({'c':c,'u':u,'v':v,'q':t,'walls':w})
    pairs=[];gaps=[];clips=[]
    for i,j in itertools.combinations(range(n),2):
        a,b=squares[i],squares[j];d=SUB(b['c'],a['c']);choices=[]
        for owner in (i,j):
            for axis in ('u','v'):
                v=squares[owner][axis];sign=1 if DOT(v,d)>=0 else -1;normal=tuple(sign*z for z in v)
                required=sum(abs(DOT(normal,s[k])) for s in (a,b) for k in ('u','v'))/2
                gap=DOT(normal,d)-required
                choices.append((gap,owner,axis,sign,normal,required))
        gap,owner,axis,sign,normal,required=max(choices,key=lambda z:z[0]);assert gap>=0,(i,j,gap)
        gaps.append(gap)
        pairs.append({'i':i,'j':j,'owner':owner,'axis':axis,'sign':sign,'nx':str(normal[0]),'ny':str(normal[1]),'margin':str(gap),'required':str(required)})
        intersection=clip(vertices(a),vertices(b));ar=area2(intersection)
        assert ar==0,(i,j,ar)
        clips.append({'i':i,'j':j,'vertices':len(intersection),'twice_area':str(ar)})
    certificate={'schema':'rational-oriented-unit-squares-v1','count':n,'L':str(L),'original_L':str(originalL),'source':{'repository':'jlevy/squares','commit':COMMIT,'path':PATH,'url':f'https://raw.githubusercontent.com/jlevy/squares/{COMMIT}/{PATH}','sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},'squares':[{'i':i,'cx':str(s['c'][0]),'cy':str(s['c'][1]),'q':str(s['q']),'ux':str(s['u'][0]),'uy':str(s['u'][1]),'vx':str(s['v'][0]),'vy':str(s['v'][1]),'wall_margins':list(map(str,s['walls']))} for i,s in enumerate(squares)],'pairs':pairs}
    out=BASE/'certificates/n37_rational_sat.json';out.write_text(json.dumps(certificate,indent=2),encoding='utf8')
    report={'source':certificate['source'],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'n':n,'L':str(L),'original_L':str(originalL),'unit_square_checks':n,'pair_sat_checks':len(pairs),'pair_clip_checks':len(clips),'wall_checks':len(wall_margins),'all_pass':True,'all_pairs_strictly_separated':all(g>0 for g in gaps),'min_pair_margin':str(min(gaps)),'min_pair_margin_float':float(min(gaps)),'min_wall_margin':str(min(wall_margins)),'min_original_wall_margin':str(min(original_wall_margins)),'clips':clips}
    (BASE/'analysis/n37_exact_verification.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('clips','source')},indent=2))
    print('certificate',out)

if __name__=='__main__':main()
