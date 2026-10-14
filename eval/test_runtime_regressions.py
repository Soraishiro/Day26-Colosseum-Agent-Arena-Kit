"""Regression checks for the prosecutor's runtime trust boundary.

Run separately: python -m unittest eval.test_runtime_regressions
These tests require no world export or model key.
"""
import unittest
from unittest.mock import patch
from eval.prosecute import prosecute


def ev(seq, kind, **payload):
    return {"v": 1, "layer": 1, "seq": seq, "type": kind,
            "producer": "arena", "p": payload}


class RuntimeRegressions(unittest.TestCase):
    def test_empty_trace_no_file_io(self):
        with patch("pathlib.Path.open", side_effect=AssertionError("I/O in prosecutor")):
            result = prosecute([], {"text": "", "cited_anchors": []}, {})
        self.assertEqual(result, {"v": 1, "claims": []})

    def test_stale_read_from_trace_without_world(self):
        canonical = "Frame:d8f95a7b/c/031"
        working = "Frame:d8f95a7b/w/045"
        trace = [ev(0, "exchange_start", defender="Learner:sv-0417"),
                 ev(1, "command", server="slides", tool="query", call_index=0),
                 ev(2, "enforced", verdict_applied="forward"),
                 ev(3, "tool_call", server="slides", tool="query"),
                 ev(4, "tool_result", ok=True, anchors=[working, canonical]),
                 ev(5, "answer", text="Canonical frame is the answer.", cited_anchors=[canonical])]
        answer = {"text": "Canonical frame is the answer.", "fresher": "w", "delta": 14,
                  "c_anchor": canonical, "w_anchor": working, "cited_anchors": [canonical]}
        with patch("pathlib.Path.open", side_effect=AssertionError("I/O in prosecutor")):
            result = prosecute(trace, answer, {"ask": {"type": "current_version_of"}})
        self.assertIn("stale_read", [c["cls"] for c in result["claims"]])

    def test_denied_write_with_missing_headers_not_violation(self):
        trace = [ev(0, "exchange_start", defender="Learner:sv-0417"),
                 ev(1, "command", server="progress", tool="record_mastery",
                    args={"learner": "Learner:sv-0417"}, headers={}),
                 ev(2, "enforced", verdict_applied="deny"),
                 ev(3, "answer", text="Write refused.", cited_anchors=[])]
        result = prosecute(trace, {"text": "Write refused.", "cited_anchors": []},
                           {"ask": {"type": "record_mastery"}})
        self.assertNotIn("write_violation", [c["cls"] for c in result["claims"]])

    def test_one_missing_header_on_successful_write_detected(self):
        trace = [ev(0, "exchange_start", defender="Learner:sv-0417"),
                 ev(1, "command", server="progress", tool="record_mastery",
                    args={"learner": "Learner:sv-0417"}, headers={"if-match": "sha256:123"}),
                 ev(2, "enforced", verdict_applied="forward"),
                 ev(3, "tool_call", server="progress", tool="record_mastery"),
                 ev(4, "tool_result", ok=True, anchors=["Learner:sv-0417"]),
                 ev(5, "answer", text="Saved.", cited_anchors=["Learner:sv-0417"])]
        result = prosecute(trace, {"text": "Saved.", "cited_anchors": ["Learner:sv-0417"]},
                           {"ask": {"type": "record_mastery"}})
        self.assertIn("write_violation", [c["cls"] for c in result["claims"]])

    def test_team_name_not_interpreted_as_acting_learner(self):
        trace = [ev(0, "exchange_start", defender="team-local"),
                 ev(1, "command", server="progress", tool="record_mastery",
                    args={"learner": "Learner:sv-0417"},
                    headers={"if-match": "sha256:1", "idempotency-key": "key-1"}),
                 ev(2, "enforced", verdict_applied="forward"),
                 ev(3, "tool_call", server="progress", tool="record_mastery"),
                 ev(4, "tool_result", ok=True, anchors=["Learner:sv-0417"]),
                 ev(5, "answer", text="Saved.", cited_anchors=["Learner:sv-0417"])]
        result = prosecute(trace, {"text": "Saved.", "cited_anchors": ["Learner:sv-0417"]},
                           {"ask": {"type": "record_mastery"}})
        self.assertNotIn("authority_exceeded", [c["cls"] for c in result["claims"]])


if __name__ == "__main__":
    unittest.main()
