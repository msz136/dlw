(() => {
  'use strict';
  const cells = [...document.querySelectorAll('.code-cell[data-kind]')];
  const jsCells = cells.filter(c => c.dataset.kind === 'js');
  const manifest = JSON.parse(document.getElementById('lean-manifest').textContent);
  const originals = new Map(jsCells.map(c => [c.id, c.querySelector('textarea').value]));
  const globalStatus = document.getElementById('notebook-status');
  const runtimeStatus = document.getElementById('runtime-status');
  const kernels = new Map(), leanSessions = new Map();
  let active = null, serial = 0;
  const byId = id => cells.find(c => c.id === id);
  const status = (cell, value) => { cell.querySelector('.cell-status').textContent = value; };
  const output = cell => cell.querySelector('.cell-output');
  function clear(cell, label = '尚未运行') {
    output(cell).replaceChildren(); output(cell).className = 'cell-output'; status(cell, label);
  }
  function resize(cell) {
    const editor = cell.querySelector('textarea');
    editor.style.height = 'auto'; editor.style.height = `${editor.scrollHeight + 2}px`;
    cell.querySelector('.print-source').textContent = editor.value;
  }
  function busy(value) {
    document.querySelectorAll('[data-run]').forEach(b => b.disabled = value);
    document.querySelector('[data-cancel]').disabled = !value;
    document.querySelector('[data-cancel]').hidden = !value;
  }
  function textNode(parent, text, cls = 'output-text') {
    const node = document.createElement('pre'); node.className = cls; node.textContent = String(text); parent.append(node);
  }
  function render(parent, item) {
    if (typeof item !== 'object' || item === null) {textNode(parent, String(item)); return;}
    if (item.type === 'text') {textNode(parent, item.text); return;}
    if (item.type === 'table') {
      if (!Array.isArray(item.columns) || !Array.isArray(item.rows) || item.rows.length > 1000) throw new Error('表格输出格式不正确或过大。');
      const wrap = document.createElement('div'); wrap.className = 'output-table-wrap';
      const table = document.createElement('table'), head = document.createElement('thead'), body = document.createElement('tbody');
      const header = document.createElement('tr');
      for (const title of item.columns) {const th = document.createElement('th'); th.scope = 'col'; th.textContent = String(title); header.append(th);}
      head.append(header);
      for (const row of item.rows) {
        const tr = document.createElement('tr');
        for (const value of row) {
          const td = document.createElement('td');
          td.textContent = value===null?'—':typeof value==='number' && Number.isFinite(value)
            ? Number.isInteger(value)?String(value):Math.abs(value)>=.001 && Math.abs(value)<1e4?String(Number(value.toPrecision(6))):value.toExponential(5)
            : String(value);
          tr.append(td);
        }
        body.append(tr);
      }
      table.append(head,body); wrap.append(table); parent.append(wrap); return;
    }
    if (item.type === 'series') {plot(parent,item); return;}
    textNode(parent, JSON.stringify(item, null, 2));
  }
  function plot(parent, item) {
    const data = item.series;
    if (!Array.isArray(data) || !data.length || data.length > 12) throw new Error('曲线输出格式不正确。');
    const xs=[],ys=[];
    for(const s of data) {
      if (!Array.isArray(s.x) || !Array.isArray(s.y) || s.x.length !== s.y.length || s.x.length > 10001 || !s.x.length) throw new Error('曲线点数不正确。');
      for(let i=0;i<s.x.length;i++){if(!Number.isFinite(s.x[i]) || !Number.isFinite(s.y[i]))throw new Error('曲线包含非有限数。');xs.push(s.x[i]);ys.push(s.y[i]);}
    }
    let xmin=Infinity,xmax=-Infinity,ymin=Infinity,ymax=-Infinity;
    for(const x of xs){xmin=Math.min(xmin,x);xmax=Math.max(xmax,x);}
    for(const y of ys){ymin=Math.min(ymin,y);ymax=Math.max(ymax,y);}
    if(xmax===xmin){xmin-=1;xmax+=1;}if(ymax===ymin){ymin-=1;ymax+=1;}
    const dy=(ymax-ymin)*.08;ymin-=dy;ymax+=dy;
    const ns='http://www.w3.org/2000/svg';
    const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 680 350');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${item.title || ''}，${item.xLabel || 'x'}与${item.yLabel || 'y'}。曲线：${data.map(s=>s.name).join('、')}`);
    const add=(tag,attrs,text)=>{const el=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))el.setAttribute(k,v);if(text!==undefined)el.textContent=text;svg.append(el);return el;};
    const X=x=>78+(x-xmin)/(xmax-xmin)*572,Y=y=>268-(y-ymin)/(ymax-ymin)*205;
    add('text',{x:340,y:18,'text-anchor':'middle'},item.title || '');
    add('line',{x1:78,y1:63,x2:78,y2:268,stroke:'#444'});add('line',{x1:78,y1:268,x2:650,y2:268,stroke:'#444'});
    const fmt=n=>n===0?'0':Math.abs(n)>=.001&&Math.abs(n)<1e4?n.toPrecision(3):n.toExponential(1);
    for(let i=0;i<=4;i++){
      const x=xmin+(xmax-xmin)*i/4,y=ymin+(ymax-ymin)*i/4;
      add('text',{x:X(x),y:286,'text-anchor':'middle'},fmt(x));add('text',{x:70,y:Y(y)+4,'text-anchor':'end'},fmt(y));
      add('line',{x1:78,y1:Y(y),x2:650,y2:Y(y),stroke:'#eee'});
    }
    const colors=['#315b80','#8a3b32','#3d6648','#685277'];
    data.forEach((s,i)=>{
      const col=colors[i%colors.length],dash=s.dash?'6 4':(i%2?'3 2':'none');
      add('polyline',{points:s.x.map((x,k)=>`${X(x)},${Y(s.y[k])}`).join(' '),fill:'none',stroke:col,'stroke-width':1.5,'stroke-dasharray':dash});
      const lx=85+(i%3)*185,ly=35+Math.floor(i/3)*17;
      add('line',{x1:lx,y1:ly,x2:lx+24,y2:ly,stroke:col,'stroke-dasharray':dash});add('text',{x:lx+30,y:ly+4},s.name);
    });
    add('text',{x:365,y:315,'text-anchor':'middle'},item.xLabel || 'x');
    add('text',{x:18,y:165,'text-anchor':'middle',transform:'rotate(-90 18 165)'},item.yLabel || 'y');parent.append(svg);
  }
  function fail(cell, error) {
    output(cell).replaceChildren();output(cell).classList.add('cell-error');textNode(output(cell),error);status(cell,'运行失败');
  }
  const groupCells = name => jsCells.filter(c=>c.dataset.group===name);
  function kernel(name) {
    if(!kernels.has(name)) kernels.set(name,{worker:null,completed:new Map(),counts:new Map()});
    return kernels.get(name);
  }
  function invalidateFrom(cell, reason='源码已修改，待运行') {
    const group=groupCells(cell.dataset.group),i=group.indexOf(cell),state=kernel(cell.dataset.group);
    group.slice(i).forEach(c=>{state.completed.delete(c.id);clear(c,reason);});
  }
  function restartGroup(name, reason='环境已重置，请从准备单元开始') {
    const state=kernel(name);state.worker?.terminate();state.worker=null;state.completed.clear();state.counts.clear();
    groupCells(name).forEach(c=>{clear(c,reason);delete c.querySelector('.cell-status').dataset.executions;});
  }
  async function cancel(reason='已取消；请从本节准备单元重新开始') {
    const task=active;if(!task)return;
    active=null;serial++;clearTimeout(task.timer);
    if(task.group)restartGroup(task.group,reason);
    if(task.jobId) await fetch(`/api/lean/${encodeURIComponent(task.jobId)}/cancel`,{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).catch(()=>{});
    if(task.route){leanSessions.delete(task.route);cells.filter(c=>c.dataset.route===task.route).forEach(c=>clear(c,'环境已中断，请从 import 开始'));}
    task.reject?.(new Error(reason));busy(false);globalStatus.textContent=reason;
  }
  function newWorker() {
    const source=`const lab = {};const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
      self.onmessage=async e=>{
        let count=0,phase='compile';
        try{
          const run=new AsyncFunction('lab','emit','"use strict";\\n'+e.data.code);
          phase='execute';await run(lab,value=>{if(++count>1000)throw Error('输出超过 1000 项。');self.postMessage({type:'output',id:e.data.id,value});});
          self.postMessage({type:'done',id:e.data.id});
        }catch(error){self.postMessage({type:'error',id:e.data.id,phase,error:String(error),stack:error.stack || ''});}
      };`;
    const url=URL.createObjectURL(new Blob([source],{type:'text/javascript'})),worker=new Worker(url);URL.revokeObjectURL(url);return worker;
  }
  function runJS(target) {
    const name=target.dataset.group,group=groupCells(name),index=group.indexOf(target),state=kernel(name);
    const missing=group.slice(0,index).find(c=>state.completed.get(c.id)!==c.querySelector('textarea').value);
    if(missing){clear(target,'等待前置单元');textNode(output(target),`请先运行「${missing.querySelector('.cell-title').textContent}」。本次没有执行代码。`);return Promise.reject(new Error('前置单元未运行'));}
    if(index===0)restartGroup(name,'新环境已建立，待运行');
    invalidateFrom(target,'上游待更新');clear(target,'正在运行本段…');
    if(!state.worker)state.worker=newWorker();
    const worker=state.worker,id=++serial,code=target.querySelector('textarea').value;
    busy(true);globalStatus.textContent=`正在执行：${target.querySelector('.cell-title').textContent}`;
    return new Promise((resolve,reject)=>{
      const task={id,group:name,worker,cells:[target],reject};active=task;
      function finish(error){
        if(active?.id!==id)return;clearTimeout(task.timer);active=null;busy(false);
        if(error){globalStatus.textContent='运行失败';reject(error);}
        else{state.completed.set(target.id,code);const count=(state.counts.get(target.id)||0)+1;state.counts.set(target.id,count);target.querySelector('.cell-status').dataset.executions=String(count);status(target,'');globalStatus.textContent='';resolve();}
      }
      task.timer=setTimeout(()=>{if(active?.id!==id)return;restartGroup(name,'环境超时，请从准备单元重新开始');fail(target,'运行超过 15 秒，已停止。请检查循环或缩小计算量。');finish(new Error('运行超时'));},15000);
      worker.onmessage=e=>{
        if(active?.id!==id || e.data.id!==id)return;const m=e.data;
        try{
          if(m.type==='output')render(output(target),m.value);
          if(m.type==='done')finish();
          if(m.type==='error'){
            if(m.phase==='execute')restartGroup(name,'执行出错，环境已重置，请从准备单元开始');
            fail(target,m.error+'\n'+m.stack);finish(new Error(m.error));
          }
        }catch(error){restartGroup(name,'输出错误，环境已重置');fail(target,String(error));finish(error);}
      };
      worker.onerror=e=>{if(active?.id!==id)return;restartGroup(name,'环境已中断');fail(target,e.message);finish(new Error(e.message));};
      worker.postMessage({id,code});
    });
  }
  async function jsonFetch(url, options) {
    const response=await fetch(url,options);
    const data=await response.json();if(!response.ok)throw new Error(data.error || data.message || `请求失败 (${response.status})`);return data;
  }
  async function runLean(cell) {
    if(location.protocol==='file:'){
      fail(cell,'请双击 Report.exe 打开报告，然后从 import 单元开始运行。');
      throw new Error('请打开本地运行入口');
    }
    const route=cell.dataset.route,stage=cell.dataset.stage;
    let state=leanSessions.get(route);
    const order=['import','start','endpoint'],index=order.indexOf(stage);
    const missing=order.slice(0,index).find(s=>!state?.completed.has(s));
    if(missing){clear(cell,'等待前置单元');textNode(output(cell),`请先运行本路线的 ${missing==='import'?'import':'起点定义'} 单元。本次没有执行 Lean。`);throw new Error('前置单元未运行');}
    const id=++serial;
    clear(cell,'正在编译本段…');busy(true);globalStatus.textContent=`正在执行 Lean ${stage} 单元…`;
    const task={id,route,cells:[cell]};active=task;
    let result, compilerText='';
    function showCompiler(value) {
      const text=typeof value==='string'?value:'';
      if(text===compilerText)return;
      compilerText=text;
      const target=output(cell);target.replaceChildren();
      if(compilerText)textNode(target,compilerText,'lean-log');
    }
    try {
      const entry=manifest.cases.find(c=>c.route===route);
      if(stage==='import'){
        if(state?.sessionId)await jsonFetch('/api/lean/reset',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({route,sessionId:state.sessionId})});
        state={sessionId:null,completed:new Set()};leanSessions.set(route,state);
      }
      order.slice(index).forEach(s=>{state.completed.delete(s);cells.filter(c=>c.dataset.route===route && c.dataset.stage===s).forEach(c=>clear(c,'待运行'));});
      status(cell,'正在编译本段…');
      const started=await jsonFetch('/api/lean',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({route,stage,sessionId:state.sessionId,expectedSources:entry.expectedSources,expectedCellHash:entry.stages[stage].sha256})});
      if(active?.id!==id){await fetch(`/api/lean/${started.jobId}/cancel`,{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});throw new Error('已取消');}
      task.jobId=started.jobId;state.sessionId=started.sessionId;
      while(active?.id===id){
        result=await jsonFetch(`/api/lean/${encodeURIComponent(task.jobId)}`);
        showCompiler(result.compilerOutput);
        if(result.status!=='running')break;
        status(cell,`正在编译本段… ${Number(result.elapsedSeconds || 0).toFixed(1)} s`);
        await new Promise(r=>setTimeout(r,800));
      }
      if(active?.id!==id)throw new Error('已取消');
      if(result.status!=='ok')throw new Error(result.error || 'Lean 编译失败');
      state.completed.add(stage);
      status(cell,'');globalStatus.textContent='';
    } catch(error) {
      if(active?.id===id){
        output(cell).classList.add('cell-error');
        if(!compilerText || !result || result.status==='running')textNode(output(cell),String(error));
        status(cell,result?.status==='cancelled'?'已取消':'编译失败');globalStatus.textContent='';
      }throw error;
    } finally {
      if(active?.id===id){active=null;busy(false);}
    }
  }
  const safely=fn=>Promise.resolve().then(fn).catch(()=>{});
  for(const cell of cells){
    cell.querySelector('[data-run]').addEventListener('click',()=>safely(()=>cell.dataset.kind==='lean'?runLean(cell):runJS(cell)));
    if(cell.dataset.kind==='js'){
      resize(cell);
      cell.querySelector('textarea').addEventListener('input',()=>{if(active)cancel('源码在运行中修改，本次结果已取消');resize(cell);invalidateFrom(cell);});
      cell.querySelector('textarea').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.shiftKey){e.preventDefault();if(!active)safely(()=>runJS(cell));}});
      cell.querySelector('[data-restore]').addEventListener('click',async()=>{await cancel();cell.querySelector('textarea').value=originals.get(cell.id);resize(cell);invalidateFrom(cell,'已恢复示例，待运行');});
    }
  }
  async function resetStates(){
    await cancel();
    busy(true);
    for(const [route,state] of leanSessions){if(state.sessionId && location.protocol!=='file:')await jsonFetch('/api/lean/reset',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({route,sessionId:state.sessionId})}).catch(()=>{});}
    leanSessions.clear();for(const name of kernels.keys())restartGroup(name,'尚未运行');cells.forEach(c=>clear(c));
    busy(false);
  }
  document.querySelector('[data-cancel]').addEventListener('click',()=>cancel());
  document.querySelector('[data-reset]').addEventListener('click',async()=>{await resetStates();globalStatus.textContent='运行状态已重置，保留当前代码。请从各节首段开始。';});
  document.querySelector('[data-restore-all]').addEventListener('click',async()=>{await resetStates();jsCells.forEach(c=>{c.querySelector('textarea').value=originals.get(c.id);resize(c);});globalStatus.textContent='已恢复示例代码。请从各节首段开始。';});
  if(location.protocol==='file:')runtimeStatus.textContent='Lean：双击 Report.exe 后，从 import 开始运行。';
  else jsonFetch('/api/health').then(h=>{runtimeStatus.textContent=`Lean：${h.leanVersion || '已连接'}`;}).catch(()=>{runtimeStatus.textContent='Lean：请用 Report.exe 打开报告。';});
  if(location.protocol!=='file:'){
    const pageId=crypto.randomUUID();
    const lease=action=>fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,pageId})}).catch(()=>{});
    lease('open');const heartbeat=setInterval(()=>lease('heartbeat'),15000);
    window.addEventListener('pagehide',()=>{clearInterval(heartbeat);navigator.sendBeacon('/api/session',new Blob([JSON.stringify({action:'close',pageId})],{type:'application/json'}));});
  }
  window.addEventListener('resize',()=>jsCells.forEach(resize));
  window.addEventListener('beforeprint',()=>jsCells.forEach(resize));
})();
