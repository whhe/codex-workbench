#!/usr/bin/env python3
"""Compatibility and security tests for Coding Workflow runtime assets."""
from __future__ import annotations
import contextlib,io,json,os,shlex,signal,subprocess,sys,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch

import evidence_runner
ROOT=Path(__file__).resolve().parents[1];PY=sys.executable
class Tests(unittest.TestCase):
 def run_json(self,script,payload):
  with tempfile.TemporaryDirectory() as d:
   i=Path(d)/'in.json';o=Path(d)/'out.json';i.write_text(json.dumps(payload));p=subprocess.run([PY,str(ROOT/'scripts'/script),str(i),'--output',str(o)],capture_output=True,text=True);return p,json.loads(o.read_text()) if o.exists() else None
 def test_routing(self):
  self.assertEqual(self.run_json('risk_router.py',{'signals':{}})[1]['mode'],'light')
  self.assertEqual(self.run_json('risk_router.py',{'signals':{'intended_reuse':True}})[1]['mode'],'standard')
  self.assertEqual(self.run_json('risk_router.py',{'signals':{'production_target':True}})[1]['mode'],'deep')
  self.assertEqual(self.run_json('risk_router.py',{'signals':{'semantic_input':True,'cross_view_state':True}})[1]['mode'],'standard')
 def test_quality_unknown(self):self.assertEqual(self.run_json('quality_vector.py',{'functional':{'status':'passed'}})[1]['quality_vector']['gui']['status'],'unknown')
 def test_evidence_v2_redaction(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json';cmd=[PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',f'{PY} -c "print(\'api_key=SECRET123\')"','--workdir',d,'--output',str(out)];p=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(p.returncode,0);rec=json.loads(out.read_text());self.assertNotIn('SECRET123',Path(rec['stdout']['path']).read_text());self.assertEqual(subprocess.run([PY,str(ROOT/'scripts/validate_evidence.py'),str(out)]).returncode,0)
 def test_json_credentials_and_command_are_redacted(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json'
   secret='fixture-sensitive-value'
   command=shlex.join([PY,'-c',f"print('token={secret}'); print({json.dumps({'password': secret})!r})"])
   result=subprocess.run([PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',d,'--output',str(out)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   record=json.loads(out.read_text())
   self.assertNotIn(secret,out.read_text())
   self.assertNotIn(secret,Path(record['stdout']['path']).read_text())
   self.assertTrue(record['redaction']['applied'])
   self.assertIn('[REDACTED]',record['command'])
 def test_basic_authorization_is_redacted_everywhere(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json';secret='dXNlcjpwYXNz'
   command=shlex.join([PY,'-c',f"import sys; print('Authorization: Basic {secret}'); print('authorization: basic {secret}',file=sys.stderr)"])
   result=subprocess.run([PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',d,'--output',str(out)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   record=json.loads(out.read_text())
   self.assertNotIn(secret,out.read_text())
   self.assertIn('[REDACTED]',record['command'])
   for stream in ('stdout','stderr'):
    content=Path(record[stream]['path']).read_text()
    self.assertNotIn(secret,content)
    self.assertIn('[REDACTED]',content)
   self.assertTrue(record['redaction']['applied'])
 def test_reject_inconsistent_pass(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'e';f.write_text(json.dumps({'schema_version':1,'evidence_id':'E','claim_id':'C','command':'x','workdir':d,'exit_code':1,'stdout_digest':'x','stderr_digest':'y','environment':{},'scope':{},'independent_acceptance_reference':'','result':'passed','started_at':'x','finished_at':'y'}));self.assertNotEqual(subprocess.run([PY,str(ROOT/'scripts/validate_evidence.py'),str(f)]).returncode,0)
 def test_timeout_is_blocked(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json';cmd=[PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',f'{PY} -c "import time; time.sleep(1)"','--workdir',d,'--timeout','0.01','--output',str(out)];p=subprocess.run(cmd,capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertEqual(json.loads(out.read_text())['result'],'blocked')
 def test_timeout_after_output_preserves_blocked_evidence(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json'
   command=shlex.join([PY,'-u','-c',"import sys,time; print('ready',flush=True); print('error',file=sys.stderr,flush=True); time.sleep(2)"])
   result=subprocess.run([PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',d,'--timeout','0.3','--output',str(out)],capture_output=True,text=True)
   self.assertEqual(result.returncode,124,result.stderr)
   record=json.loads(out.read_text())
   self.assertEqual(record['result'],'blocked')
   self.assertTrue(record['timed_out'])
   self.assertIn('ready',Path(record['stdout']['path']).read_text())
   self.assertIn('error',Path(record['stderr']['path']).read_text())
   self.assertEqual(subprocess.run([PY,str(ROOT/'scripts/validate_evidence.py'),str(out)],capture_output=True).returncode,0)
 @unittest.skipUnless(sys.platform == 'darwin' or sys.platform.startswith('linux'), 'POSIX runner only')
 def test_timeout_stops_descendants_before_they_write(self) -> None:
  for shell in (False,True):
   with self.subTest(shell=shell),tempfile.TemporaryDirectory() as d:
    base=Path(d);out=base/'e.json';ready=base/'ready';sentinel=base/'late-write'
    child="import os,sys,time; from pathlib import Path; Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(1.5); Path(sys.argv[2]).write_text('escaped')"
    parent=f"import subprocess,time; subprocess.Popen({[PY,'-c',child,str(ready),str(sentinel)]!r}); print('started',flush=True); time.sleep(10)"
    command=shlex.join([PY,'-u','-c',parent])
    args=[PY,'-B',str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',d,'--timeout','0.7','--output',str(out)]
    if shell:args.append('--shell')
    try:
     result=subprocess.run(args,capture_output=True,text=True,timeout=10)
     self.assertEqual(result.returncode,124,result.stderr)
     self.assertTrue(ready.exists(),'child must start for this check to discriminate')
     record=json.loads(out.read_text())
     self.assertEqual(record['result'],'blocked')
     self.assertIn('started',Path(record['stdout']['path']).read_text())
     time.sleep(1.6)
     self.assertFalse(sentinel.exists(),'child wrote after its evidence command timed out')
    finally:
     if ready.exists():
      try:os.kill(int(ready.read_text()),signal.SIGKILL)
      except ProcessLookupError:pass
 @unittest.skipUnless(sys.platform == 'darwin' or sys.platform.startswith('linux'), 'POSIX runner only')
 def test_detached_pipe_holder_fails_within_cleanup_bound(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   base=Path(d);out=base/'e.json';ready=base/'detached-pid'
   child="import os,sys,time; from pathlib import Path; Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(30)"
   parent=f"import subprocess,time; subprocess.Popen({[PY,'-c',child,str(ready)]!r},start_new_session=True); time.sleep(30)"
   command=shlex.join([PY,'-c',parent])
   started=time.monotonic()
   try:
    result=subprocess.run([PY,'-B',str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',d,'--timeout','0.7','--output',str(out)],capture_output=True,text=True,timeout=10)
    self.assertTrue(ready.exists(),'detached pipe holder must start')
    self.assertNotEqual(result.returncode,0)
    self.assertIn('timeout cleanup incomplete',result.stderr)
    self.assertLess(time.monotonic()-started,9)
    self.assertFalse(out.exists(),'incomplete cleanup must not emit evidence')
   finally:
    if ready.exists():
     try:os.kill(int(ready.read_text()),signal.SIGKILL)
     except ProcessLookupError:pass
 def test_invalid_timeout_rejects_before_launch(self) -> None:
  for value in ('nan','inf','-inf','0','-1'):
   with self.subTest(timeout=value),tempfile.TemporaryDirectory() as d:
    args=['evidence_runner.py','--claim-id','C1','--command','unused','--timeout='+value,'--output',str(Path(d)/'e.json')]
    with patch.object(sys,'argv',args),patch.object(evidence_runner,'source_snapshot') as snapshot,patch.object(subprocess,'Popen') as launch,contextlib.redirect_stderr(io.StringIO()):
     with self.assertRaises(SystemExit) as error:evidence_runner.main()
     self.assertEqual(error.exception.code,2)
     snapshot.assert_not_called();launch.assert_not_called()
 def test_unsupported_platform_rejects_before_sampling_or_launch(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json'
   args=['evidence_runner.py','--claim-id','C1','--command','unused','--output',str(out)]
   with patch.object(sys,'argv',args),patch.object(sys,'platform','win32'),patch.object(evidence_runner,'source_snapshot') as snapshot,patch.object(subprocess,'Popen') as launch,contextlib.redirect_stderr(io.StringIO()) as stderr:
    with self.assertRaises(SystemExit) as error:evidence_runner.main()
    self.assertEqual(error.exception.code,2)
    self.assertIn('macOS/Linux only',stderr.getvalue())
    snapshot.assert_not_called();launch.assert_not_called()
   self.assertFalse(out.exists())
 def test_redaction_precedes_byte_limited_utf8_storage(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'e.json'
   private='-----BEGIN PRIVATE KEY-----\nTOP_SECRET_MATERIAL'+('x'*100)+'\n-----END PRIVATE KEY-----'
   command=shlex.join([PY,'-c',f"import sys; print({private!r}); print('你好'*100,file=sys.stderr)"])
   result=subprocess.run([PY,str(ROOT/'scripts/evidence_runner.py'),'--claim-id','C1','--command',command,'--workdir',d,'--max-output-bytes','64','--output',str(out)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   record=json.loads(out.read_text())
   self.assertEqual(Path(record['stdout']['path']).read_text(),'[REDACTED]\n')
   self.assertFalse(record['stdout']['truncated'])
   self.assertTrue(record['stderr']['truncated'])
   self.assertTrue(record['redaction']['applied'])
   for name in ('stdout','stderr'):
    content=Path(record[name]['path']).read_bytes()
    self.assertEqual(len(content),record[name]['bytes'])
    self.assertLessEqual(len(content),64)
    content.decode('utf-8')
   self.assertEqual(subprocess.run([PY,str(ROOT/'scripts/validate_evidence.py'),str(out)],capture_output=True).returncode,0)
if __name__=='__main__':unittest.main()
