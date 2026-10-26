"""Read-only audit of saved plotting arrays; never imports or runs a solver."""
from pathlib import Path
import csv, hashlib, json
import numpy as np
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
DATA=PROJECT/'report_refresh_20261024/natural_selection_20261025/figures/data'
PLOTS=PROJECT/'spatial_ad_uv_20261025'
CASES=['A','D','Gaussian','Sinusoidal']
WINDOWS={'A':[-5,5],'D':[-30,30],'Gaussian':[-18,18],'Sinusoidal':[-12,12]}
SECTIONS={'A':[-5,5],'D':[-8,8],'Gaussian':[-18,18],'Sinusoidal':[-12,12]}
METHODS={'endpoint':'Endpoint-SD','centered':'Centered-SD','fd':'FD'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mdiff(a,b):return float(np.max(abs(a-b)))
def section(y,z,degree):
    hit=np.flatnonzero(abs(y)<1e-12)
    if len(hit):return z[hit[np.argmin(abs(y[hit]))]]
    ix=np.sort(np.argsort(abs(y),kind='stable')[:degree+1]);yn=y[ix]
    sn=(yn-yn.mean())/(yn.max()-yn.min())
    w=np.array([1/np.prod(sn[j]-np.delete(sn,j)) for j in range(len(ix))]);w/=abs(w).max()
    t=w/(-yn);return np.tensordot(t/t.sum(),z[ix],axes=(0,0))
def triangle_heights(x,y,z,ix,iy):
    """Heights of the a-b-c / a-c-d mesh used by pixel_surfaces.py."""
    li=np.clip(np.searchsorted(x[ix],x,side='right')-1,0,len(ix)-2)
    lj=np.clip(np.searchsorted(y[iy],y,side='right')-1,0,len(iy)-2)
    u=((x-x[ix[li]])/(x[ix[li+1]]-x[ix[li]]))[None,:]
    v=((y-y[iy[lj]])/(y[iy[lj+1]]-y[iy[lj]]))[:,None]
    a=z[iy[lj,None],ix[None,li]];b=z[iy[lj,None],ix[None,li+1]]
    c=z[iy[lj[:,None]+1],ix[None,li+1]];dd=z[iy[lj[:,None]+1],ix[None,li]]
    return np.where(u>=v,a*(1-u)+b*(u-v)+c*v,a*(1-v)+c*u+dd*(v-u))

table=list(csv.DictReader((PROJECT/'report_refresh_20261024/table2_final_field_errors.csv').open(encoding='utf-8-sig')))
tab={(r['case'],r['space'],q):float(r['error_'+q]) for r in table for q in ['u','v']}
result={'scope':'saved-array comparisons only; no solver or exact-solution reevaluation','cases':[],'images':[]}
for c in CASES:
    path=DATA/(c+'.npz');d=np.load(path);meta=json.loads((DATA/(c+'.json')).read_text())
    rec={'case':c,'prepared_sha256':sha(path),'all_113_saved_arrays_finite':all(np.isfinite(d[k]).all() for k in d.files),'fields':[]}
    mx=(d['x']>=WINDOWS[c][0])&(d['x']<=WINDOWS[c][1]);ms=(d['x']>=SECTIONS[c][0])&(d['x']<=SECTIONS[c][1])
    for p,name in METHODS.items():
        src=meta['methods'][p]['sources'][0];raw=np.load(ROOT/src['path'])
        rx=np.flatnonzero(np.isin(raw['x'],d['x']))
        assert np.array_equal(raw['x'][rx],d['x'])
        for q,yk in [('u','y'),('v','yv')]:
            y=d[p+'_y_'+q];ry=np.flatnonzero(np.isin(raw[yk],y))
            assert np.array_equal(raw[yk][ry],y)
            native=raw[q][np.ix_(ry,rx)]
            val=d[p+'_final_'+q];ref=d[p+'_ref_final_'+q];err=d[p+'_error_final_'+q]
            e=abs(err[:,mx]);lin=abs(d[p+'_line_error_final_'+q][ms])
            vmax=max(tab[c,n,q] for n in METHODS.values());vmin=max(vmax*1e-4,1e-13)
            r={'method':name,'field':q,'artifact':src['path'],'artifact_hash_matches':sha(ROOT/src['path'])==src['sha256'],
               'prepared_vs_native_max_difference':mdiff(val,native),'error_vs_num_minus_ref_max_difference':mdiff(err,val-ref),
               'section_reconstruction_max_difference':mdiff(section(raw[yk],raw[q][:,rx],11),d[p+'_line_final_'+q]),
               'section_error_definition_max_difference':mdiff(d[p+'_line_error_final_'+q],d[p+'_line_final_'+q]-d['exact_native_final_'+q]),
               'section_degree11_vs15_max':mdiff(section(raw[yk],raw[q][:,rx],11),section(raw[yk],raw[q][:,rx],15)),
               'native_y_interval':[float(y.min()),float(y.max())],
               'map_shape':list(e.shape),'map_maximum':float(e.max()),'table_maximum':tab[c,name,q],
               'map_maximum_over_table':float(e.max()/tab[c,name,q]),'log_color_limits':[vmin,vmax],
               'under_color_fraction':float(np.mean(e<vmin)),'zero_value_count':int(np.sum(e==0)),
               'section_maximum_display_window':float(lin.max())}
            if q=='v' and c in ['Gaussian','Sinusoidal']:
                r['section_error_axis_upper_limit']=max(1e-10,max(float(abs(d[pp+'_line_error_final_v'][ms]).max()) for pp in METHODS)*1.3)
                r['fraction_of_error_axis_height']=float(lin.max()/r['section_error_axis_upper_limit'])
            peak=np.unravel_index(e.argmax(),e.shape)
            iy=np.unique(np.r_[np.linspace(0,e.shape[0]-1,min(121,e.shape[0])).round().astype(int),peak[0]])
            ix=np.unique(np.r_[np.linspace(0,e.shape[1]-1,min(181,e.shape[1])).round().astype(int),peak[1]])
            r['original_3d_max_preserved']=float(e[np.ix_(iy,ix)].max())==float(e.max())
            r['original_3d_selected_fraction']=len(iy)*len(ix)/e.size
            # Original Matplotlib surfaces use quad polygons, so this is a
            # bilinear undersampling diagnostic, not a pixel-render residual.
            xe=d['x'][mx]
            zx=np.array([np.interp(xe,xe[ix],row) for row in e[np.ix_(iy,ix)]])
            zz=np.array([np.interp(y,y[iy],zx[:,j]) for j in range(e.shape[1])]).T
            r['original_3d_bilinear_sampling_residual_over_peak']=mdiff(e,zz)/float(e.max())
            # Current plain overlays really use this diagonal triangle mesh.
            piy=np.unique(np.r_[np.linspace(0,len(y)-1,min(241,len(y))).round().astype(int),peak[0]])
            pix=np.arange(len(xe));zz=triangle_heights(xe,y,e,pix,piy)
            residual=abs(zz-e);j=np.unravel_index(residual.argmax(),residual.shape)
            r['plain_3d_triangle_sampling_residual_over_peak']=float(residual.max()/e.max())
            r['plain_3d_max_residual_location']=[float(xe[j[1]]),float(y[j[0]])]
            r['plain_3d_native_and_triangle_heights_at_max_residual']=[float(e[j]),float(zz[j])]
            if c=='D':
                i=np.argmin(abs(xe+10));r['native_column_peak_near_minus10']=[[float(xe[k]),float(e[:,k].max())] for k in range(i-2,i+3)]
            rec['fields'].append(r)
    result['cases'].append(rec)

manifests=[(PLOTS/'figures/manifest.json',PLOTS/'figures'),(PLOTS/'figures/3d_manifest.json',PLOTS/'figures'),
           (PLOTS/'figures/exact_3d_manifest.json',PLOTS/'figures'),(PLOTS/'surface_only_20261025/manifest.json',PLOTS/'surface_only_20261025/figures')]
lookup={}
for mp,base in manifests:
    for m in json.loads(mp.read_text()):
        for ext in ['png','pdf']:
            if ext in m:lookup[(base/m[ext]).resolve()]=(m[ext+'_sha256'],mp)
soup=BeautifulSoup((ROOT/'dlw-paper.html').read_text(encoding='utf-8'),'html.parser')
for f in soup.select(r'#section-5\.1 figure, #section-5\.2 figure'):
    path=(ROOT/f.img['src']).resolve();known=lookup.get(path)
    result['images'].append({'figure':f['id'],'path':str(path.relative_to(ROOT)),'exists':path.exists(),'manifest_found':known is not None,
                             'hash_matches_manifest':bool(known and sha(path)==known[0])})
out=HERE/'plot_data_checks.json';out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'output':str(out),'fields_checked':sum(len(c['fields']) for c in result['cases']),'images_checked':len(result['images']),
                  'all_image_hashes_match':all(r['hash_matches_manifest'] for r in result['images']),
                  'max_prepared_vs_native_difference':max(r['prepared_vs_native_max_difference'] for c in result['cases'] for r in c['fields']),
                  'max_error_definition_difference':max(r['error_vs_num_minus_ref_max_difference'] for c in result['cases'] for r in c['fields']),
                  'max_section_reconstruction_difference':max(r['section_reconstruction_max_difference'] for c in result['cases'] for r in c['fields'])},indent=2))
