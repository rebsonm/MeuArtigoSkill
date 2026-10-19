#!/usr/bin/env python3
"""Offline safety contract for non-destructive v1 UI runtime swap.

Does not connect to VPS, Auth0, ChatGPT, Google Drive or an actual user account.
"""
from pathlib import Path
import unittest

S=Path(__file__).with_name("v1-deploy-reviewed-ui-hotfix.sh").read_text(encoding="utf8")

class DeploymentContract(unittest.TestCase):
    def test_only_three_pinned_files_and_separate_runtime(self):
        for required in (
            'SOURCE_SHA="4365456fd63cb6090dac7e79dd1cadaf0732da2c"',
            'ORIGINAL_SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"',
            'STAGE="/opt/meu-artigo-v1-ui-hotfix-20261019"',
            'cp -a -- "$ROOT" "$STAGE"',
            "assets/research_site.html",
            "integrations/mcp-apps/server.mjs",
            "integrations/mcp-apps/ui_output_schema.mjs",
            'git hash-object "$dest.new"',
            'SOURCE_BLOB_NOT_PINNED',
            'HOTFIX_ALREADY_PRESENT',
        ): self.assertIn(required,S)
        self.assertNotIn("MEU_ARTIGO_GOOGLE_CLIENT_SECRET=",S)
        self.assertNotIn("git reset --hard",S)

    def test_auth_mcp_e05_and_public_directory_still_protected(self):
        for required in (
            'AUTHENTICATED_USER_OVERRIDE_MISSING',
            'MEU_ARTIGO_AUTH_MODE=auth0',
            'MEU_ARTIGO_MCP_MULTIUSER=YES',
            'MEU_ARTIGO_MCP_PRIVATE_PILOT=',
            'ANONYMOUS_NOT_401',
            'OAUTH_DISCOVERY_NOT_200',
            'LEGACY_CHANGED',
            'E05_CHANGED',
            'V1_E05_LEGACY=UNCHANGED',
            'V1_PUBLIC_DIRECTORY=NOT_PUBLISHED',
            'V1_HOST_CSP=NOT_INDEPENDENTLY_VERIFIED',
        ): self.assertIn(required,S)
        self.assertNotIn('systemctl restart meu-artigo-mcp.service',S)
        self.assertNotIn('systemctl restart meu-artigo-e05-tunnel.service',S)
        self.assertNotIn('MEU_ARTIGO_AUTH_MODE=none',S)

    def test_rollback_after_runtime_switch(self):
        for required in (
            '--apply',
            '--rollback',
            '# MEU_ARTIGO_REVIEWED_UI_HOTFIX',
            'ExecStart=',
            'systemctl daemon-reload',
            'systemctl restart "$SERVICE"',
            'V1_UI_HOTFIX_AUTO_ROLLBACK=ORIGINAL_RUNTIME',
            'V1_UI_HOTFIX=ROLLED_BACK_TO_ORIGINAL_RUNTIME',
            'rm -rf -- "$STAGE"',
            "npm run test:host-projection-ui",
            "npm run test:e05-synthetic",
            "npm run test:e05-csp",
            "npm run test:ui-resource-contract",
        ): self.assertIn(required,S)

if __name__=="__main__":unittest.main()
