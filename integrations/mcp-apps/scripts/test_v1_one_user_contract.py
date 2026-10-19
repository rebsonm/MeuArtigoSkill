#!/usr/bin/env python3
"""Offline fail-closed contract for a single authorized private pilot identity.

This checks source-only safety. It does NOT impersonate a real Auth0 user,
install a systemd override or prove a real ChatGPT MCP connection.
"""
from pathlib import Path
import unittest

SCRIPT=Path(__file__).with_name("v1-allow-one-researcher.sh")


class SingleUserPilotContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=SCRIPT.read_text(encoding="utf-8")

    def test_deny_all_base_and_one_user_only(self):
        s=self.source
        for phrase in (
            "PINNED_SHA=",
            "Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=YES",
            "Environment=MEU_ARTIGO_MCP_MULTIUSER=YES",
            "Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL",
            "EnvironmentFile=$ALLOW_ENV",
            "V1_SINGLE_PILOT=ONE_APPROVED_IDENTITY_ACTIVE",
            "V1_SINGLE_PILOT_PUBLIC_RELEASE=NO",
            "--rollback",
            "AUTO_REVERT=DENY_ALL",
        ):
            self.assertIn(phrase,s)
        self.assertNotIn("MEU_ARTIGO_MCP_PRIVATE_PILOT=NO",s)
        self.assertNotIn("MEU_ARTIGO_MCP_PILOT_SUBS=*",s)

    def test_identity_not_taken_from_cli_or_echoed(self):
        s=self.source
        self.assertIn("read -r -s",s)
        self.assertIn('[[ "$#" -eq 1 ]]',s)
        self.assertIn('[[ "$SUB" =~',s)
        self.assertIn('printf \'MEU_ARTIGO_MCP_PILOT_SUBS=%s\\n\' "$SUB"',s)
        self.assertIn("chmod 0600",s)
        self.assertIn("unset SUB",s)
        self.assertNotIn('echo "$SUB"',s)
        self.assertNotIn('printf "%s" "$SUB"',s)

    def test_only_new_private_service_is_restarted(self):
        s=self.source
        self.assertIn('systemctl restart "$SERVICE"',s)
        self.assertNotIn("systemctl restart meu-artigo-mcp.service",s)
        self.assertNotIn("systemctl restart meu-artigo-e05-tunnel.service",s)
        self.assertIn("E05_NOT_ACTIVE",s)
        self.assertIn("LEGACY_NOT_ACTIVE",s)
        self.assertIn("ANONYMOUS_ACCESS_NOT_DENIED",s)
        self.assertIn('grep -zFxq "MEU_ARTIGO_MCP_PILOT_SUBS=$SUB"',s)
        self.assertIn('rm -f -- "$TEMP_ENV"',s)
        self.assertIn('rm -f -- "$TEMP_CONF"',s)

if __name__=="__main__":
    unittest.main()
