// Offline orthographic surface rasterizer. Each method is an open sheet.
// Rasterize its visible front layer once, then composite the three layers
// by per-pixel depth. This avoids repeated alpha on shared triangle edges.
const fs=require('fs');
const meta=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const buf=fs.readFileSync(meta.vertices);
const vertices=new Float32Array(buf.buffer,buf.byteOffset,buf.length/4);
const outputs=[new Uint8ClampedArray(meta.width*meta.height*4),new Uint8ClampedArray(meta.width*meta.height*4)];
function scene(s){
 const bx=s.bounds[0],by=s.bounds[1],w=s.bounds[2]-bx+1,h=s.bounds[3]-by+1,n=w*h,layers=[];
 for(const mesh of s.meshes){
  const depth=new Float32Array(n);depth.fill(Infinity);
  const rgb=new Uint8ClampedArray(n*3),alpha=new Uint8ClampedArray(n),grid=new Uint8ClampedArray(n);
  const offset=mesh.offset,cols=mesh.cols,rows=mesh.rows;
  function triangle(ia,ib,ic){
   const a=offset+ia*9,b=offset+ib*9,c=offset+ic*9;
   const ax=vertices[a]-bx,ay=vertices[a+1]-by,bx0=vertices[b]-bx,by0=vertices[b+1]-by,cx=vertices[c]-bx,cy=vertices[c+1]-by;
   const det=(by0-cy)*(ax-cx)+(cx-bx0)*(ay-cy);if(Math.abs(det)<1e-12)return;
   const x0=Math.max(0,Math.floor(Math.min(ax,bx0,cx))),x1=Math.min(w-1,Math.ceil(Math.max(ax,bx0,cx)));
   const y0=Math.max(0,Math.floor(Math.min(ay,by0,cy))),y1=Math.min(h-1,Math.ceil(Math.max(ay,by0,cy)));
   for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){
    const px=x+.5,py=y+.5;
    const u=((by0-cy)*(px-cx)+(cx-bx0)*(py-cy))/det;
    const v=((cy-ay)*(px-cx)+(ax-cx)*(py-cy))/det;
    const t=1-u-v;if(u< -1e-7||v< -1e-7||t< -1e-7)continue;
    const dz=u*vertices[a+2]+v*vertices[b+2]+t*vertices[c+2],i=y*w+x;
    if(dz>=depth[i])continue;
    depth[i]=dz;
    for(let k=0;k<3;k++)rgb[i*3+k]=255*(u*vertices[a+3+k]+v*vertices[b+3+k]+t*vertices[c+3+k]);
    alpha[i]=255*(u*vertices[a+6]+v*vertices[b+6]+t*vertices[c+6]);
    const xx=(u*vertices[a+7]+v*vertices[b+7]+t*vertices[c+7])*8;
    const yy=(u*vertices[a+8]+v*vertices[b+8]+t*vertices[c+8])*6;
    const dist=Math.min(Math.abs(xx-Math.round(xx)),Math.abs(yy-Math.round(yy)));
    grid[i]=255*Math.max(0,1-dist/.014);
   }
  }
  for(let r=0;r<rows-1;r++)for(let c=0;c<cols-1;c++){
   const a=r*cols+c,b=a+1,d=a+cols,cc=d+1;triangle(a,b,cc);triangle(a,cc,d);
  }
  layers.push({depth,rgb,alpha,grid});
 }
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const i=y*w+x;let order=[0,1,2].filter(k=>Number.isFinite(layers[k].depth[i]));
  order.sort((a,b)=>layers[b].depth[i]-layers[a].depth[i]);
  if(!order.length)continue;
  for(let mode=0;mode<2;mode++){
   let rr=0,gg=0,bb=0,aa=0;
   for(const k of order){
    const l=layers[k],a=l.alpha[i]/255,shade=mode?1-.32*l.grid[i]/255:1;
    rr=l.rgb[i*3]*shade*a+rr*(1-a);gg=l.rgb[i*3+1]*shade*a+gg*(1-a);bb=l.rgb[i*3+2]*shade*a+bb*(1-a);aa=a+aa*(1-a);
   }
   if(aa===0)continue;
   const j=((y+by)*meta.width+(x+bx))*4;
   outputs[mode][j]=rr/aa;outputs[mode][j+1]=gg/aa;outputs[mode][j+2]=bb/aa;outputs[mode][j+3]=255*aa;
  }
 }
}
for(const s of meta.scenes){scene(s);if(global.gc)global.gc();}
for(let i=0;i<2;i++)fs.writeFileSync(meta.outputs[i],outputs[i]);
console.log('Rendered per-pixel transparent surfaces:',meta.case);
