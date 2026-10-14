"""Regression suite: python -m unittest agent.test_gateway_regressions -v"""
import unittest
from agent.gateway import Command, Gateway
from agent.telemetry import RecordingGatewayContext


def cmd(server="slides", tool="query", args=None, headers=None, kind="mcp", fields=(), lease=None):
    return Command(cmd_id="cmd:0001", kind=kind, raw=f"{server}.{tool}",
                   server=server, tool=tool, args=args or {}, headers=headers or {},
                   fields=fields, lease_id=lease, call_index=1)


def gw(scopes=frozenset({"wiki.read"}), leases=()):
    ctx = RecordingGatewayContext(act="learner:sv-0417", sub="agent:vlearn-tutor",
        scopes=scopes, credits=100, round=1, call_index=1, leases=leases)
    return Gateway(ctx)

class GatewayRegressionTests(unittest.TestCase):
    def test_clean_read_is_allowed(self):
        self.assertIn(gw().decide(cmd()).verdict, ("forward", "rewrite"))

    def test_cross_learner_write_is_denied(self):
        g = gw(frozenset({"wiki.read", "wiki.write:progress"}))
        c = cmd("progress", "record_mastery", {"learner": "Learner:sv-0392"},
                {"if-match": "sha256:x", "idempotency-key": "k"})
        self.assertEqual(g.decide(c).verdict, "deny")

    def test_valid_write_is_allowed(self):
        g = gw(frozenset({"wiki.read", "wiki.write:progress"}))
        c = cmd("progress", "record_mastery", {"learner": "Learner:sv-0417"},
                {"if-match": "sha256:x", "idempotency-key": "k"})
        self.assertIn(g.decide(c).verdict, ("forward", "rewrite"))

    def test_get_frame_needs_lease(self):
        self.assertEqual(gw().decide(cmd("slides", "get_frame")).verdict, "deny")

    def test_deprecated_search_rewritten(self):
        r = gw().decide(cmd("slides", "search", {"q": "lecture"}))
        self.assertEqual((r.verdict, r.call.tool), ("rewrite", "query"))

    def test_catalog_mask_is_narrowed(self):
        r = gw().decide(cmd("glossary", "list_terms", fields=("*",)))
        self.assertEqual(r.call.fields, ("term",))

    def test_a2a_unverified_peer_is_denied(self):
        self.assertEqual(gw().decide(cmd("curriculum-analyst", "which_days_cover",
            kind="a2a", headers={"aud": "curriculum-analyst"})).verdict, "deny")

    def test_a2a_verified_card_and_audience(self):
        g = gw()
        g.note_card("curriculum-analyst", {"verified": True, "skills": ["which_days_cover"]})
        c = cmd("curriculum-analyst", "which_days_cover", kind="a2a",
                headers={"aud": "curriculum-analyst"})
        self.assertIn(g.decide(c).verdict, ("forward", "rewrite"))

if __name__ == "__main__":
    unittest.main()
