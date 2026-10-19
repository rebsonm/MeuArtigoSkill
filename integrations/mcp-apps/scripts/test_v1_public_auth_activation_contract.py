#!/usr/bin/env python3
"""Source-only acceptance; cannot prove third-party OAuth login or host UI."""
from pathlib import Path
import unittest

S=Path(__file__).with_name("v1-enable-authenticated-users.sh").read_text()


class MultiuserActivationContract(unittest.TestCase):
    def test_exact_deployed_runtime_and_two_modes(self):
        for text in (
            'EXPECTED_SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"',
            'MEU_ARTIGO_MCP_MULTIUSER=YES',
            'MEU_ARTIGO_MCP_PRIVATE_PILOT=YES',
            'MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL',
            'MEU_ARTIGO_AUTH_MODE=auth0',
            'MEU_ARTIGO_AUTH_RESOURCE=$RESOURCE',
            'V1_MULTIUSER=ALL_AUTHENTICATED_AUTH0_SUBJECTS',
            '--apply', '--rollback', 'V1_MULTIUSER=DENY_ALL_RESTORED',
        ):
            self.assertIn(text, S)

    def test_only_pilot_gates_are_cleared_and_never_scope_or_auth(self):
        self.assertIn("Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=\n", S)
        self.assertIn("Environment=MEU_ARTIGO_MCP_PILOT_SUBS=\n", S)
        self.assertIn("grep -zFxq 'MEU_ARTIGO_AUTH_MODE=auth0'", S)
        self.assertIn("grep -zFxq 'MEU_ARTIGO_MCP_MULTIUSER=YES'", S)
        self.assertIn("ANONYMOUS_NOT_401", S)
        self.assertIn("V1_OAUTH_SCOPE=mcp:read", S)
        self.assertNotIn("MEU_ARTIGO_AUTH_MODE=none", S)
        self.assertNotIn("MEU_ARTIGO_MCP_BEARER=", S)
        self.assertNotIn("Environment=MEU_ARTIGO_AUTH_MODE=", S)
        self.assertNotIn("systemctl restart meu-artigo-mcp.service", S)

    def test_atomic_override_and_rollback(self):
        for text in (
            '[[ ! -e "$DROPIN" ]]',
            'OTHER_DROPIN_UNREVIEWED',
            'systemctl daemon-reload',
            'systemctl restart "$SERVICE"',
            'V1_MULTIUSER_AUTO_REVERT=DENY_ALL',
            'rm -f -- "$DROPIN"',
            'V1_OTHER_SERVICES=UNCHANGED',
            'V1_PUBLIC_DIRECTORY=NOT_PUBLISHED',
            'V1_LIVE_USER_LOGIN=NOT_YET_VERIFIED',
        ):
            self.assertIn(text, S)
        self.assertNotIn("MEU_ARTIGO_MCP_PRIVATE_PILOT=NO", S)


if __name__ == "__main__":
    unittest.main()
