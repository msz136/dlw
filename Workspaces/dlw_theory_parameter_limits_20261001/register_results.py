"""Minimal topic-only insertions after fresh reads of shared index files."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
progress='''> **2026-10-01（T01：DLW 两结构参数的谱范围限制）：** 独立理论研究完成，用户阅读报告为[DLW：两个结构参数的谱范围限制](Workspaces/dlw_theory_parameter_limits_20261001/report.html)，专属目录Workspaces/dlw_theory_parameter_limits_20261001/。固定Γ≠1的正则N=1连续Gram谱族、精确x/t、共同物理a/h；两个有界常数在整段谱域和细化时共用。完整证明最佳归一化相位剩余CΓΔA²/8、唯一最优点及可行性；给精确正则条件、有限h积分式与显式h⁴统一余项，十倍相位首项门槛为尺度比R≤5+2√5。Γ=2、|α|≤1、|β|≤2上，精确有理认证：[1,2]且h≤1/50的固定最优常数至少十倍相位改善；[1,10]且h≤1/500的整个参数盒均不能十倍相位改善。固定有限h的有理乘子不能整段匹配指数相位。物理新证明：静态∫v_h dx=4 logχ/h及自然插值u两切片下界；共同物理初值后v质量误差守恒为零，静态相位质量见证完全取消。另从物理源推得共同初值领先u初速比例≥(R−1)/(R²+1)，R∈(5−√14,5+√14)时排除十倍；R=2至少为1/5，尽管相位允许1/32。F的五阶复极点也排除单谱领先u初速的完整消去。严格区分相位、静态族偏差、共同初值初速与有限正时间场误差；最后者仍缺存在性/传播与统一余项，未宣称双场演化十倍收益。预测与证书条件先冻结，再完成14项精确代数、2项精确有理区间认证与4组端点/中点公式核对；零新PDE、零参数扫描。两个独立代理完成交叉证明审查，有限h证书另经Fraction精确重算一致。项目查重完成，外部原创性未判定。自包含HTML的22编号公式/187数学片段、1280/390宽窄屏、链接均通过。仅修改本题目录/HTML与本条进度、索引，未改共享求解器、ideas.json或其他分支。

'''
index='''**T01：DLW 两结构参数的谱范围限制（2026-10-01）：**

- [DLW：两个结构参数的谱范围限制](Workspaces/dlw_theory_parameter_limits_20261001/report.html)（完整相位范围定理、有限h认证、物理质量见证的守恒取消与共同初值初速限制；不等同有限时间双场误差结论）
- @Workspaces/dlw_theory_parameter_limits_20261001/REPORT.md@、@finite_h_review.md@、@physical_bridge_review.md@（主稿、有限h完整证明与独立物理审查）
- @Workspaces/dlw_theory_parameter_limits_20261001/THEORY_FREEZE.json@、@CERTIFICATE_CONTRACT.json@（核对前冻结的预测、指标及两个有限h区间证书条件）
- @Workspaces/dlw_theory_parameter_limits_20261001/verify_theory.py@、@theory_validation.json@（14项精确代数、2项有理区间认证、4组定向公式核对；零PDE演化）
- @Workspaces/dlw_theory_parameter_limits_20261001/build_report.py@、@report_source.html@、@manifest.json@、@delivery_manifest.json@（主稿生成、自包含数学资源及交付哈希）
- @Workspaces/dlw_theory_parameter_limits_20261001/check_report.cjs@、@html_validation.json@、@report_1280.png@、@report_390.png@、@report_physical.png@（22编号公式、187数学片段、宽窄屏及链接检查）；@register_results.py@、@registration.json@（本题共享索引最小修改记录）

'''
index=index.replace('@',chr(96))
changes=[]
for name,topic,entry in [('PROGRESS_LOG.md','> **2026-10-01（T01：DLW 两结构参数的谱范围限制）：**',progress),('FILE_INDEX.md','**T01：DLW 两结构参数的谱范围限制（2026-10-01）：**',index)]:
    path=ROOT/name
    for attempt in range(3):
        original=path.read_bytes()
        text=original.decode('utf-8')
        newline='\r\n' if '\r\n' in text else '\n'
        content=entry.replace('\n',newline)
        if topic in text:
            start=text.index(topic)
            if name=='PROGRESS_LOG.md':
                end=text.find(newline+newline,start)
            else:
                end=text.find(newline+newline+'**',start+len(topic))
            if end<0:raise RuntimeError('Cannot safely locate own topic block')
            end+=2*len(newline)
            updated=text[:start]+content+text[end:]
            preserved=text[:start]+text[end:]
        elif name=='PROGRESS_LOG.md':
            updated=content+text
            preserved=text
        else:
            split=text.index(newline+newline)+2*len(newline)
            updated=text[:split]+content+text[split:]
            preserved=text
        if path.read_bytes()!=original:continue
        path.write_bytes(updated.encode('utf-8'))
        assert updated.replace(content,'',1)==preserved
        changes.append({'file':name,'before_sha256':hashlib.sha256(original).hexdigest(),'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'other_content_preserved':True})
        break
    else:raise RuntimeError('Shared file changed repeatedly; retry later')
(HERE/'registration.json').write_text(json.dumps({'status':'passed','changes':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'passed','shared_files':[v['file'] for v in changes],'other_content_preserved':True}))

