#!/usr/bin/env python3
"""Run a command and emit a redacted, source-bound EvidenceRecord v2."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, re, shlex, signal, subprocess, sys
import math
from datetime import datetime, timezone
from pathlib import Path

from evidence import bind_source, source_snapshot

CLEANUP_TIMEOUT_SECONDS = 5.0

RULES = [
    ("quoted_credential", re.compile(r'''(?i)((?:authorization|api[_-]?key|token|secret|password)["']?\s*[:=]\s*)(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')''')),
    ("authorization_header", re.compile(r"(?i)(authorization\s*[:=]\s*)(?:(?:bearer|basic)\s+)?[^\s]+")),
    ("api_key", re.compile(r"(?i)((?:api[_-]?key|token|secret|password)\s*[:=]\s*)[^\s]+")),
    ("private_key", re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.S)),
]

def digest_bytes(value: bytes) -> str: return "sha256:" + hashlib.sha256(value).hexdigest()
def redact(text: str) -> tuple[str, dict[str, int]]:
    counts = {}
    for name, pattern in RULES:
        text, count = pattern.subn(lambda m: (m.group(1) if m.lastindex else "") + "[REDACTED]", text)
        if count: counts[name] = count
    return text, counts


def capture_output(value: bytes | str | None, limit: int) -> tuple[bytes, dict[str, int], bool]:
    """Normalize and redact complete output before applying a UTF-8 byte limit."""
    text = value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
    redacted, counts = redact(text)
    encoded = redacted.encode("utf-8")
    bounded = encoded[:limit].decode("utf-8", errors="ignore").encode("utf-8")
    return bounded, counts, len(encoded) > limit


def run_command(argv: str | list[str], workdir: str, shell: bool, timeout: float) -> tuple[subprocess.CompletedProcess[bytes], bool]:
    """Collect output, killing the inherited process group on timeout."""
    proc = subprocess.Popen(argv, cwd=workdir, shell=shell, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            return subprocess.CompletedProcess(argv, proc.returncode, stdout, stderr), False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = proc.communicate(timeout=CLEANUP_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired as error:
                raise RuntimeError("timeout cleanup incomplete: captured pipes remain open; no evidence record written") from error
            return subprocess.CompletedProcess(argv, 124, stdout, stderr), True
    finally:
        # A detached descendant can retain pipes after the group is killed.
        for stream in (proc.stdout, proc.stderr):
            if stream is not None:
                stream.close()
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=CLEANUP_TIMEOUT_SECONDS)


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--claim-id",required=True); p.add_argument("--command",required=True)
    p.add_argument("--shell",action="store_true"); p.add_argument("--workdir",default=os.getcwd())
    p.add_argument("--acceptance-reference-id",default=""); p.add_argument("--scope-file",action="append",default=[])
    p.add_argument("--timeout",type=float,default=300.0); p.add_argument("--max-output-bytes",type=int,default=2_000_000)
    p.add_argument("--scope-test",action="append",default=[]); p.add_argument("--output",required=True)
    a=p.parse_args()
    if a.max_output_bytes < 0:
        p.error("--max-output-bytes must be nonnegative")
    if not math.isfinite(a.timeout) or a.timeout <= 0:
        p.error("--timeout must be a finite positive number")
    if sys.platform != "darwin" and not sys.platform.startswith("linux"):
        p.error("evidence command execution supports macOS/Linux only; reliable timeout cleanup is unavailable on this platform")
    started=datetime.now(timezone.utc).isoformat()
    before=source_snapshot(a.workdir)
    argv=a.command if a.shell else shlex.split(a.command)
    try:
        proc, timed_out = run_command(argv, a.workdir, a.shell, a.timeout)
    except (OSError, subprocess.SubprocessError, RuntimeError) as error:
        p.exit(2, f"evidence execution failed: {error}\n")
    after=source_snapshot(a.workdir)
    command, rc0=redact(a.command)
    stdout, rc1, stdout_truncated=capture_output(proc.stdout,a.max_output_bytes)
    stderr, rc2, stderr_truncated=capture_output(proc.stderr,a.max_output_bytes)
    output=Path(a.output); output.parent.mkdir(parents=True,exist_ok=True)
    stdout_path=output.with_suffix(output.suffix+".stdout"); stderr_path=output.with_suffix(output.suffix+".stderr")
    stdout_path.write_bytes(stdout); stderr_path.write_bytes(stderr)
    source=bind_source(before, after)
    record={"schema_version":2,"evidence_id":"E-"+hashlib.sha256((started+a.command).encode()).hexdigest()[:16],"claim_id":a.claim_id,
      "command":command,"shell":a.shell,"workdir":str(Path(a.workdir).resolve()),"exit_code":proc.returncode,
      "stdout":{"path":str(stdout_path.resolve()),"digest":digest_bytes(stdout),"bytes":len(stdout),"truncated":stdout_truncated},
      "stderr":{"path":str(stderr_path.resolve()),"digest":digest_bytes(stderr),"bytes":len(stderr),"truncated":stderr_truncated},
      "redaction":{"applied":bool(rc0 or rc1 or rc2),"rules":sorted(set(rc0)|set(rc1)|set(rc2)),"count":sum(rc0.values())+sum(rc1.values())+sum(rc2.values())},
      "environment":{"python":sys.version.split()[0],"platform":platform.platform()},"source":source,
      "scope":{"files":a.scope_file,"tests":a.scope_test,"interfaces":[]},"independent_acceptance_reference":a.acceptance_reference_id,
      "result":"blocked" if timed_out else ("passed" if proc.returncode==0 else "failed"),"timed_out":timed_out,"started_at":started,"finished_at":datetime.now(timezone.utc).isoformat()}
    record["source_fingerprint"]=before.get("fingerprint", "") if source["binding"] == "stable" else ""
    output.write_text(json.dumps(record,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"evidence_id":record["evidence_id"],"claim_id":a.claim_id,"exit_code":proc.returncode,"result":record["result"],"output":str(output.resolve())},ensure_ascii=False))
    return proc.returncode
if __name__=="__main__": raise SystemExit(main())
