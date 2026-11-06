# Coding Evidence

Evidence used by the coding workflow to assess declared acceptance claims.

## Language

**Evidence record**:
A retained observation of a check, its outcome, supporting artifacts and source context. A record can remain useful for diagnosis without qualifying as passing acceptance evidence.
_Avoid_: Proof of completion

**Source fingerprint**:
A content identity for the repository files associated with a check. It distinguishes file contents from the commit used to describe their provenance.
_Avoid_: Commit fingerprint

**Stable source binding**:
An association between a check and complete, matching observations of repository content before and after execution. It is a prerequisite for using a record as passing code acceptance evidence.
_Avoid_: Guaranteed execution snapshot
