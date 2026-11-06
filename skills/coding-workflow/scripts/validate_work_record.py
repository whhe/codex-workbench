#!/usr/bin/env python3
"""Contract-Driven Kernel: validate one canonical work record."""
from __future__ import annotations
import argparse, json
from pathlib import Path

MODES={"light","standard","deep"}; TYPES={"fact","assumption","prediction"}
STATUSES={"passed","failed","partial","not_run","not_applicable","blocked","unknown","not_ready"}

def validate(data:dict)->list[str]:
 e=[]
 for key in ("schema_version","work_id","raw_request","outcome","scope","claims","acceptance","risk","completion_requirements","authority"):
  if key not in data:e.append("missing: "+key)
 if data.get("risk",{}).get("mode") not in MODES:e.append("invalid risk.mode")
 ids=set()
 for i,c in enumerate(data.get("claims",[])):
  cid=c.get("claim_id")
  if not cid:e.append(f"claims[{i}] missing claim_id")
  elif cid in ids:e.append("duplicate claim_id: "+cid)
  ids.add(cid)
  if c.get("type") not in TYPES:e.append(f"claims[{i}] invalid type")
  statement=c.get("statement")
  if not isinstance(statement,str) or not statement.strip():e.append(f"claims[{i}] statement must be a nonempty string")
 for i,a in enumerate(data.get("acceptance",[])):
  if a.get("claim_id") not in ids:e.append(f"acceptance[{i}] unknown claim_id")
 for name,r in data.get("completion_requirements",{}).items():
  if not isinstance(r,dict):e.append(f"completion_requirements.{name} must be object");continue
  if not isinstance(r.get("required"),bool):e.append(f"completion_requirements.{name}.required must be bool")
  if r.get("status","not_run") not in STATUSES:e.append(f"completion_requirements.{name} invalid status")
  for cid in r.get("claims",[]):
   if cid not in ids:e.append(f"completion_requirements.{name} unknown claim_id: {cid}")
 if data.get("authority",{}).get("required"):
  auth=data.get("authority",{})
  for key in ("actor","target","scope"): 
   if not auth.get(key):e.append("deep authority missing: "+key)
  if auth.get("readback_required") is not True:e.append("deep authority requires readback_required=true")
 return e

def main()->int:
 p=argparse.ArgumentParser();p.add_argument("record");a=p.parse_args()
 try:data=json.loads(Path(a.record).read_text(encoding="utf-8"));errors=validate(data)
 except Exception as ex:errors=[str(ex)]
 print(json.dumps({"valid":not errors,"errors":errors},ensure_ascii=False));return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
