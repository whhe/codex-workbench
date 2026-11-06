#!/usr/bin/env python3
"""Behavioral regressions for the merged workflow decisions."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from completion_gate import evaluate
from risk_router import classify, ROOT
from task_storage import task_directory
from validate_acceptance_reference_registry import validate as validate_registry


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = json.loads((ROOT / 'references/risk-policy.json').read_text())
        self.completion = {
            'mode': 'standard',
            'evidence_index': {'claims': {'C1': {'passed': ['E1'], 'failed': [], 'conflict': False}}},
            'completion_requirements': {'behavior': {'required': True, 'status': 'passed', 'claims': ['C1']}},
        }

    def test_local_state_and_failed_fixes_do_not_force_deep(self) -> None:
        for signal in ('persistent_state', 'concurrency', 'migration', 'permissions', 'retry_semantics'):
            with self.subTest(signal=signal):
                decision = classify({'signals': {signal: True, 'failed_fix_count': 3}}, self.policy)
                self.assertEqual(decision['mode'], 'standard')
                self.assertIn('recovery', decision['required_adapters'])
        self.assertEqual(classify({'failed_fix_count': 3}, self.policy)['mode'], 'light')

    def test_actual_impact_routes_deep(self) -> None:
        for signal in self.policy['rules']['deep_engineering']:
            with self.subTest(signal=signal):
                self.assertEqual(classify({signal: True}, self.policy)['mode'], 'deep')

    def test_required_pass_without_claims_remains_provisional(self) -> None:
        for mode in ('standard', 'deep'):
            for claims in (None, []):
                with self.subTest(mode=mode, claims=claims):
                    requirement = {'required': True, 'status': 'passed'}
                    if claims is not None:
                        requirement['claims'] = claims
                    data = {'mode': mode, 'completion_requirements': {'behavior': requirement}}
                    result = evaluate(data)
                    self.assertEqual(result['status'], 'provisional')
                    self.assertEqual(result['unsupported_conditions'], ['behavior'])
        data = copy.deepcopy(self.completion)
        data['completion_requirements']['optional'] = {'required': False, 'status': 'passed', 'claims': []}
        data['completion_requirements']['unused'] = {'required': True, 'status': 'not_applicable', 'claims': []}
        result = evaluate(data)
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(result['unsupported_conditions'], [])

    def test_standard_does_not_require_registry(self) -> None:
        self.assertEqual(evaluate(self.completion)['status'], 'accepted')

    def test_deep_accepts_direct_independent_reference_without_external_authority(self) -> None:
        data = copy.deepcopy(self.completion)
        data['mode'] = 'deep'
        self.assertEqual(evaluate(data)['status'], 'provisional')
        data['acceptance_references'] = [{'source': 'Existing contract', 'coverage': ['C1'], 'independent': True, 'verified': True}]
        self.assertEqual(evaluate(data)['status'], 'accepted')
        data['acceptance_references'][0]['independent'] = False
        self.assertEqual(evaluate(data)['status'], 'provisional')

    def test_registry_validation_and_gate_reject_the_same_invalid_registry(self) -> None:
        reference = {
            'acceptance_reference_id': 'R1', 'owner': 'Owner', 'reviewer': 'Reviewer',
            'version': '1', 'status': 'active', 'source': 'Existing contract',
            'source_digest': 'contract-digest', 'frozen_at': '2026-01-01T00:00:00Z',
            'coverage': ['C1'], 'known_gaps': [],
        }
        invalid_entries = []
        for update in ({'frozen_at': ''}, {'review_after': '2000-01-01T00:00:00Z'},
                       {'coverage': 'C1'}, {'owner': ''}, {'status': []}, {'review_after': 3}):
            invalid_entries.append([dict(reference, **update)])
        invalid_entries.extend([
            [reference, dict(reference)],
            [reference, {'acceptance_reference_id': 'unused'}],
            [reference, None],
        ])
        cases = [('valid', {'acceptance_references': [reference]}, True)]
        cases.extend((f'invalid-{i}', {'acceptance_references': entries}, False)
                     for i, entries in enumerate(invalid_entries))
        cases.extend([('root-list', [], False), ('entries-null', {'acceptance_references': None}, False)])
        with tempfile.TemporaryDirectory() as temporary:
            registry = Path(temporary) / 'references.json'
            for label, contents, valid in cases:
                with self.subTest(case=label):
                    registry.write_text(json.dumps(contents))
                    result = subprocess.run(
                        [sys.executable, '-B', str(ROOT / 'scripts/validate_acceptance_reference_registry.py'),
                         str(registry), '--require-active'], capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, 0 if valid else 1, result.stderr)
                    self.assertEqual(json.loads(result.stdout)['valid'], valid)
                    self.assertEqual(not validate_registry(contents, require_active=True), valid)
                    data = copy.deepcopy(self.completion)
                    data.update(mode='deep', acceptance_reference_registry=str(registry),
                                acceptance_reference_bindings=[{'claim_id': 'C1', 'acceptance_reference_id': 'R1', 'verified': True}])
                    gate = evaluate(data)
                    self.assertEqual(gate['status'], 'accepted' if valid else 'provisional')
                    if not valid:
                        self.assertTrue(any(error.startswith('invalid_acceptance_reference_registry:')
                                            for error in gate['acceptance_reference_errors']))

    def test_direct_references_do_not_require_registry_validation(self) -> None:
        data = copy.deepcopy(self.completion)
        data.update(mode='deep', acceptance_reference_registry='/unused/registry.json',
                    acceptance_references=[{'source': 'Existing contract', 'coverage': ['C1'],
                                            'independent': True, 'verified': True}])
        self.assertEqual(evaluate(data)['status'], 'accepted')

    def test_reference_diagnostics_only_block_when_required_coverage_is_missing(self) -> None:
        cases = [
            ('optional-missing-registry', 'standard', 'C2', None, 'accepted'),
            ('direct-alternative', 'deep', 'C1', True, 'accepted'),
            ('unverified-alternative', 'deep', 'C1', False, 'provisional'),
            ('no-alternative', 'deep', 'C1', None, 'provisional'),
            ('optional-missing-entry', 'standard', 'C2', None, 'accepted'),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            for name, mode, claim, verified, expected in cases:
                with self.subTest(case=name):
                    registry = Path(temporary) / f'{name}.json'
                    if name == 'optional-missing-entry':
                        registry.write_text(json.dumps({'acceptance_references': []}))
                    data = copy.deepcopy(self.completion)
                    data['completion_requirements']['optional'] = {'required': False, 'status': 'failed', 'claims': ['C2']}
                    data['evidence_index']['claims']['C2'] = {'passed': [], 'failed': ['E2'], 'conflict': True}
                    data.update(mode=mode, acceptance_reference_registry=str(registry),
                                acceptance_reference_bindings=[{'claim_id': claim, 'acceptance_reference_id': 'R1', 'verified': True}])
                    if verified is not None:
                        data['acceptance_references'] = [{'source': 'Existing independent contract', 'coverage': ['C1'],
                                                         'independent': True, 'verified': verified}]
                    result = evaluate(data)
                    self.assertEqual(result['status'], expected)
                    self.assertEqual(result['missing_reference_claims'], ['C1'] if expected == 'provisional' else [])
                    self.assertIn(f'invalid_acceptance_reference_binding:{claim}', result['acceptance_reference_errors'])
                    if name != 'optional-missing-entry':
                        self.assertTrue(any(error.startswith('invalid_acceptance_reference_registry:')
                                            for error in result['acceptance_reference_errors']))

    def test_external_execution_needs_authority_and_readback(self) -> None:
        data = copy.deepcopy(self.completion)
        data['external_action'] = True
        self.assertEqual(evaluate(data)['status'], 'blocked')
        data['authority'] = {'authorized': True, 'actor': 'user', 'target': 'test system', 'scope': ['update']}
        self.assertEqual(evaluate(data)['status'], 'provisional')
        data['authority']['readback_verified'] = True
        self.assertEqual(evaluate(data)['status'], 'accepted')

    def test_required_failure_blocks_optional_failure_does_not(self) -> None:
        data = copy.deepcopy(self.completion)
        data['completion_requirements']['optional'] = {'required': False, 'status': 'failed', 'claims': ['C2']}
        data['evidence_index']['claims']['C2'] = {'passed': [], 'failed': ['E2'], 'conflict': True}
        self.assertEqual(evaluate(data)['status'], 'accepted')
        data['completion_requirements']['optional']['required'] = True
        self.assertEqual(evaluate(data)['status'], 'blocked')

    def test_failed_evidence_blocks_even_if_level_claims_pass(self) -> None:
        data = copy.deepcopy(self.completion)
        data['evidence_index']['claims']['C1'] = {'passed': [], 'failed': ['E1'], 'conflict': False}
        self.assertEqual(evaluate(data)['status'], 'blocked')

    def test_verification_and_authority_require_literal_true(self) -> None:
        for value in ('false', 'true', 1):
            for field in ('verified', 'independent'):
                with self.subTest(value=value, field=field):
                    data = copy.deepcopy(self.completion)
                    data.update(mode='deep', acceptance_references=[{
                        'source': 'Contract', 'coverage': ['C1'], 'verified': True, 'independent': True,
                        field: value,
                    }])
                    self.assertEqual(evaluate(data)['status'], 'provisional')
            for field, expected in (('authorized', 'blocked'), ('readback_verified', 'provisional')):
                with self.subTest(value=value, field=field):
                    data = copy.deepcopy(self.completion)
                    data.update(external_action=True, authority={
                        'actor': 'user', 'target': 'test', 'scope': ['update'],
                        'authorized': True, 'readback_verified': True, field: value,
                    })
                    self.assertEqual(evaluate(data)['status'], expected)

    def test_storage_rejects_repository_paths_and_symlink_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = base / 'repo'
            repo.mkdir()
            external = base / 'data'
            result = task_directory(repo, 'task-1', external)
            self.assertNotIn(repo.resolve(), result.parents)
            self.assertEqual(result, task_directory(repo, 'task-1', external))
            with self.assertRaises(ValueError):
                task_directory(repo, 'task-1', repo)
            alias = base / 'alias'
            alias.symlink_to(repo, target_is_directory=True)
            with self.assertRaises(ValueError):
                task_directory(repo, 'task-1', alias)
            with self.assertRaises(ValueError):
                task_directory(repo, '../escape', external)


if __name__ == '__main__':
    unittest.main()
