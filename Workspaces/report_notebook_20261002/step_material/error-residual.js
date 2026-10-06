if (!lab.dlw?.ready?.coefficient) throw Error("先运行二阶主系数。");
const {a,K,ell,Omega,profile}=lab.dlw;
function residual(z, hh, scheme) {
  const cache = new Map();
  function node(j) {
    if (cache.has(j)) return cache.get(j);
    const c=profile(z+ell*hh*j), plus=profile(z+ell*hh*(j+1));
    const minus=profile(z+ell*hh*(j-1));
    // 差分重构：D=δ₀u，W=v−δ₀u。
    const D=c.v.map((_,n) => (plus.u[n]-minus.u[n])/(2*hh));
    const W=c.v.map((v,n) => v-D[n]);
    const Ax=K*(c.u[0]+2*a)*c.u[1];
    const Hx=Ax + (scheme==="SD" ? hh*hh*K*(W[0]/16-1/4)*W[1] : 0);
    const out={...c,D,W,Ax,Hx}; cache.set(j,out); return out;
  }
  // r1 位于交错中点；r2 位于节点 j=0。
  const plus=node(1/2), minus=node(-1/2), c=node(0);
  let r1=Omega*(plus.u[1]-minus.u[1])/hh+(plus.Hx-minus.Hx)/hh;
  r1 += K*K*(scheme==="SD"
    ? (plus.u[2]-minus.u[2])/hh+(plus.W[2]+minus.W[2])/2
    : (plus.v[2]+minus.v[2])/2);
  let r2=Omega*c.v[1];
  if (scheme==="SD") {
    const pp=node(1), mm=node(-1);
    r2 += (pp.Hx-mm.Hx)/(2*hh)
      + K*(c.u[1]*c.W[0]+(c.u[0]+2*a)*c.W[1]-4*c.u[1])
      + K*K*(c.D[2]+(pp.W[2]-2*c.W[2]+mm.W[2])/4);
  } else {
    r2 += K*(c.u[1]*c.v[0]+(c.u[0]+2*a)*c.v[1]-4*c.u[1])
      + K*K*c.D[2];
  }
  return [r1,r2];
}
Object.assign(lab.dlw,{residual,ready:{prepare:true,config:true,profile:true,coefficient:true,residual:true}});
