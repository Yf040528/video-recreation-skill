import json
from pathlib import Path
from .prompt_compiler import compile_prompt

PRESENCE_KEYS=("hand","product","clothing","temple")

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding="utf-8")

def validate_job(job_path: Path, verbose=False):
    j=load(job_path)
    errors=[]
    if not j.get("job_id"): errors.append("missing job_id")
    if "global_master" not in j: errors.append("missing global_master")
    if not j.get("shots"): errors.append("missing shots")
    ids=set()
    for s in j.get("shots",[]):
        sid=s.get("id")
        if not sid: errors.append("shot missing id"); continue
        if sid in ids: errors.append(f"duplicate shot id: {sid}")
        ids.add(sid)
        pm=s.get("presence_map")
        if not isinstance(pm,dict): errors.append(f"{sid}: missing presence_map"); continue
        for k in PRESENCE_KEYS:
            if k not in pm: errors.append(f"{sid}: presence_map missing {k}")
            elif not isinstance(pm[k],bool): errors.append(f"{sid}: presence {k} must be boolean")
        if len(s.get("creative_delta",[])) < 2:
            errors.append(f"{sid}: creative_delta must contain >=2 major changes")
    if errors:
        raise SystemExit("VALIDATION FAILED\\n- "+"\\n- ".join(errors))
    if verbose: print(f"VALID: {j['job_id']} / {len(j['shots'])} shots")
    return j

def build_job(job_path: Path):
    j=validate_job(job_path); base=job_path.parent
    for folder in ("tasks","prompts","outputs","qa"):
        (base/folder).mkdir(exist_ok=True)
    for s in j["shots"]:
        pm=s["presence_map"]
        task={
            "task_id":s["id"],"job_id":j["job_id"],"mode":j.get("mode","RECREATED_SHOT"),
            "source":s["source"],"semantic_function":s["semantic_function"],
            "presence_map":pm,"global_master":j["global_master"],
            "mandatory_replacements":s.get("mandatory_replacements",[]),
            "preserve":s.get("preserve",[]),"creative_delta":s["creative_delta"],
            "output_contract":{
                "asset_count":1,"independent_asset":True,"collage":False,
                "output":f"outputs/{s['id']}.png"
            }
        }
        dump(base/"tasks"/f"{s['id']}.json",task)
        (base/"prompts"/f"{s['id']}.txt").write_text(compile_prompt(task),encoding="utf-8")
    print(f"BUILT {len(j['shots'])} independent tasks")

def build_queue(job_path: Path):
    j=validate_job(job_path); base=job_path.parent
    build_job(job_path)
    q=[]
    for s in j["shots"]:
        sid=s["id"]
        q.append({
            "task_id":sid,
            "prompt_file":f"prompts/{sid}.txt",
            "source_file":s["source"],
            "expected_output":f"outputs/{sid}.png",
            "asset_count":1,
            "status":"WAITING_FOR_GENERATOR"
        })
    dump(base/"generation_queue.json",q)
    print("QUEUE READY:",base/"generation_queue.json")

def aggregate_qa(job_path: Path):
    j=validate_job(job_path); base=job_path.parent
    report=[]; retry=[]
    for s in j["shots"]:
        sid=s["id"]; out=base/"outputs"/f"{sid}.png"; qp=base/"qa"/f"{sid}.json"
        if not out.exists():
            row={"task_id":sid,"status":"FAIL","reason":["MISSING_OUTPUT"]}
            retry.append(sid)
        elif not qp.exists():
            row={"task_id":sid,"status":"WAITING_VISUAL_QA","reason":["NO_VISUAL_QA_RESULT"]}
        else:
            q=load(qp)
            failed=[k for k,v in q.get("checks",{}).items() if v is not True]
            row={"task_id":sid,"status":"PASS" if not failed else "FAIL","reason":failed}
            if failed: retry.append(sid)
        report.append(row)
    dump(base/"qa_report.json",report)
    dump(base/"retry_queue.json",retry)
    print("QA REPORT:",base/"qa_report.json")
    print("RETRY QUEUE:",base/"retry_queue.json")
