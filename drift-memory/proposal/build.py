import json,re,subprocess
M=json.load(open('meta.json'))
A={'memgpt':'2310.08560','mem0':'2504.19413','amem':'2502.12110','rag':'2005.11401','faulty':'2605.12978','cliff':'2608.22752','reclaim':'2606.25449','dpm':'2604.20158','uac':'2606.16707','memfit':'2610.00872','projectmem':'2606.12329','locomo':'2402.17753','longmemeval':'2410.10813','timem':'2601.02845','lightmem':'2510.18866','trajwiki':'2608.00967','chronomem':'2607.27773','shepherd':'2605.10913','deltamem':'2606.03083','ssgm':'2603.11768','rd':'2607.08032','zep':'2501.13956','mnemis':'2602.15313','selroute':'2604.02431','budgetmem':'2602.06025','justmem':'2609.19877','tiermem':'2602.17913','render':'2608.23568','bm25s':'2407.03618','agentzero':'2608.29606','laundering':'2607.29167','memtrust':'2601.07004','memcut':'2610.21405','toki':'2606.06240','ama':'2601.20352','indictalk':'2607.23242','memagentbench':'2507.05257'}
OTHER={
'driftnomore':'V. Dongre \\textit{et al.}, ``Drift no more? Context equilibria in multi-turn LLM interactions,\'\' arXiv:2510.07777, 2025.',
'memora':'M. N. Uddin \\textit{et al.}, ``From recall to forgetting: Benchmarking long-term memory for personalized agents,\'\' in \\textit{Findings of ACL}, 2026, arXiv:2604.20006.',
'realm':'Y. Song \\textit{et al.}, ``Retrieval-driven memory reconsolidation for long-term LLM agents,\'\' arXiv:2609.16053, 2026.',
'allmem':'C. Lv \\textit{et al.}, ``All-Mem: Agentic lifelong memory via dynamic topology evolution,\'\' arXiv:2603.19595, 2026.',
'humanmem':'D. Kerestecioglu \\textit{et al.}, ``Human-inspired memory architecture for LLM agents,\'\' arXiv:2605.08538, 2026.',
'h264':'T. Wiegand, G. J. Sullivan, G. Bjøntegaard and A. Luthra, ``Overview of the H.264/AVC video coding standard,\'\' \\textit{IEEE Trans. Circuits Syst. Video Technol.}, vol. 13, no. 7, pp. 560--576, 2003.',
'apex':'P. Banerjee \\textit{et al.}, ``APEX-MEM: Agentic semi-structured memory with temporal reasoning,\'\' in \\textit{Proc. ACL}, 2026. [Online]. Available: \\url{https://aclanthology.org/2026.acl-long.749/}',
'anchormem':'Z. Shen \\textit{et al.}, ``AnchorMem: Anchored facts with associative contexts,\'\' in \\textit{Findings of ACL}, 2026. [Online]. Available: \\url{https://aclanthology.org/2026.findings-acl.1736/}',
'iva':'E. Butts and S. Daher, ``Consistent conversational state for virtual agents: Slot-based memory for accurate fact retrieval,\'\' in \\textit{Proc. ACM IVA}, 2026, doi: 10.1145/3806774.3832787.',
'cortexdb':'CortexDB, ``Event sourcing,\'\' documentation. [Online]. Available: \\url{https://cortexdb.ai/docs/concepts/event-sourcing}',
'sdpi':'Y. Polyanskiy and Y. Wu, ``Strong data-processing inequalities for channels and Bayesian networks,\'\' in \\textit{Convexity and Concentration}, Springer, 2017, pp. 211--249, arXiv:1508.06025.',
'aksharantar':'Y. Madhani \\textit{et al.}, ``Aksharantar: Open Indic-language transliteration datasets and models for the next billion users,\'\' in \\textit{Findings of EMNLP}, 2023, arXiv:2205.03018.',
'llama3':'A. Grattafiori \\textit{et al.}, ``The Llama 3 herd of models,\'\' arXiv:2407.21783, 2024.'}
def ini(n):
    p=n.split(); return ' '.join(x[0]+'.' for x in p[:-1])+' '+p[-1]
def fmt(k):
    if k in OTHER: return OTHER[k]
    m=M[A[k]]; au=m['au']
    a=(ini(au[0])+' \\textit{et al.}') if len(au)>3 else (', '.join(ini(x) for x in au[:-1])+(' and ' if len(au)>1 else '')+ini(au[-1]) if len(au)>1 else ini(au[0]))
    t=m['t'].replace('--','--').replace('&','\\&')
    return f"{a}, ``{t},'' arXiv:{A[k]}, {m['y']}."
body=open('body.tex').read(); order=[]
for k in re.findall(r'\[@(\w+)\]',body):
    if k not in order: order.append(k)
missing=[k for k in order if k not in A and k not in OTHER]; assert not missing,missing
num={k:i+1 for i,k in enumerate(order)}
body=re.sub(r'\[@(\w+)\]',lambda m:f'[{num[m.group(1)]}]',body)
refs='\n'.join(f'\\noindent [{num[k]}] {fmt(k)}\\par' for k in order)
body=body.replace('@@REFS@@',refs)
open('paper.tex','w').write(open('preamble.tex').read()+body)
print(len(order),'refs')
r=subprocess.run(['./tectonic','--keep-logs','paper.tex'],capture_output=True,text=True)
print(r.returncode, r.stderr[-2500:])
