#!/usr/bin/env python3
"""Regression tests for Coding Workflow Contract-Driven Kernel."""
from __future__ import annotations
import json,shlex,subprocess,sys,tempfile,unittest
from pathlib import Path
from validate_work_record import validate
ROOT=Path(__file__).resolve().parents[1];PY=sys.executable
class Tests(unittest.TestCase):
 def runio(self,script,payload):
  with tempfile.TemporaryDirectory() as d:
   i=Path(d)/'i.json';o=Path(d)/'o.json';i.write_text(json.dumps(payload));p=subprocess.run([PY,str(ROOT/'scripts'/script),str(i),'--output',str(o)],capture_output=True,text=True);return p,json.loads(o.read_text()) if o.exists() else None
 def test_policy_routes(self):
  self.assertEqual(self.runio('risk_router.py',{'signals':{}})[1]['mode'],'light')
  self.assertEqual(self.runio('risk_router.py',{'signals':{'multi_step_interaction':True}})[1]['mode'],'standard')
  self.assertEqual(self.runio('risk_router.py',{'signals':{'multi_step_interaction':True,'cross_view_state':True}})[1]['mode'],'standard')
  self.assertEqual(self.runio('risk_router.py',{'signals':{'authorization_boundary':True}})[1]['mode'],'deep')
  self.assertEqual(self.runio('risk_router.py',{'signals':{'long_term_use_claim':True}})[1]['mode'],'standard')
  self.assertEqual(self.runio('risk_router.py',{'signals':{'long_term_use_claim':True,'persistent_state':True}})[1]['mode'],'standard')
 def test_work_record(self):
  p=subprocess.run([PY,str(ROOT/'scripts/validate_work_record.py'),str(ROOT/'assets/work-record.example.json')]);self.assertEqual(p.returncode,0)
 def test_work_record_requires_claim_statement(self) -> None:
  example=(ROOT/'assets/work-record.example.json').read_text()
  self.assertEqual(validate(json.loads(example)),[])
  for label,value in (('missing',None),('null',None),('empty',''),('whitespace',' \t\n'),('number',42)):
   with self.subTest(statement=label):
    record=json.loads(example)
    if label=='missing':record['claims'][0].pop('statement')
    else:record['claims'][0]['statement']=value
    self.assertIn('claims[0] statement must be a nonempty string',validate(record))
 def test_evidence_conflict_blocks(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   base=Path(d);repo=base/'repo';repo.mkdir()
   subprocess.run(['git','init','-q',str(repo)],check=True)
   records=[]
   for number,code in enumerate((1,0)):
    output=base/f'e{number}.json'
    command=shlex.join([PY,'-c',f'raise SystemExit({code})'])
    result=subprocess.run([PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',str(repo),'--output',str(output)],capture_output=True,text=True)
    self.assertEqual(result.returncode,code,result.stderr)
    records.append(json.loads(output.read_text()))
   source=base/'input.json';index=base/'index.json';decision=base/'decision.json'
   source.write_text(json.dumps({'acceptance_claims':['C1'],'evidence_records':records}))
   subprocess.run([PY,str(ROOT/'scripts/evidence_index.py'),str(source),'--output',str(index)],check=True,capture_output=True)
   payload={'mode':'standard','evidence_index':json.loads(index.read_text()),'completion_requirements':{'artifact':{'required':True,'status':'passed','claims':['C1']}},'authority':{}}
   source.write_text(json.dumps(payload))
   result=subprocess.run([PY,str(ROOT/'scripts/completion_gate.py'),str(source),'--output',str(decision)],capture_output=True,text=True)
   self.assertEqual(result.returncode,2)
   self.assertEqual(json.loads(decision.read_text())['status'],'blocked')
 def test_optional_not_run_does_not_block(self):
  payload={'mode':'standard','evidence_index':{'claims':{'C1':{'passed':['E1'],'failed':[],'conflict':False}}},'completion_requirements':{'artifact':{'required':True,'status':'passed','claims':['C1']},'production':{'required':False,'status':'not_run','claims':[]}},'authority':{},'acceptance_reference':{'status':'active'}}
  p,o=self.runio('completion_gate.py',payload);self.assertEqual(p.returncode,0);self.assertEqual(o['status'],'accepted')
 def test_strict_acceptance_reference_binding_requires_registry_coverage(self):
  payload={'mode':'standard','schema_version':3,'acceptance_reference_registry':'/missing/acceptance_references.json','acceptance_reference_bindings':[{'claim_id':'C1','acceptance_reference_id':'O1','verified':True}],'acceptance_claims':['C1'],'evidence_index':{'claims':{'C1':{'passed':['E1'],'failed':[],'conflict':False}}},'completion_requirements':{'artifact':{'required':True,'status':'passed','claims':['C1']}},'authority':{}}
  p,o=self.runio('completion_gate.py',payload);self.assertEqual(p.returncode,2);self.assertEqual(o['status'],'provisional')
  self.assertEqual(o['missing_reference_claims'],['C1'])
  payload['acceptance_references']=[{'source':'Existing contract','coverage':['C1'],'verified':True,'independent':True}]
  p,o=self.runio('completion_gate.py',payload);self.assertEqual(p.returncode,0);self.assertEqual(o['status'],'accepted')
  self.assertEqual(o['missing_reference_claims'],[]);self.assertTrue(o['acceptance_reference_errors'])
if __name__=='__main__':unittest.main()
