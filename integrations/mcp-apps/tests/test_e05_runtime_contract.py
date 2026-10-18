"""Executable E05 launcher contract with synthetic credentials; never accesses VPS."""
import getpass
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts/e05-vps-runtime-launch.sh"
BOOTSTRAP = ROOT / "scripts/e05-vps-autonomous-bootstrap.sh"

FAKE_TUNNEL = '''#!/usr/bin/env python3
import json, os, sys
mode = sys.argv[1]
if mode == 'doctor':
    if os.getenv('FAKE_REQUIRE_LEGACY_PROFILE_ENV') == 'yes':
        if not os.getenv('CONTROL_PLANE_API_KEY', '').startswith('sk-SYNTHETIC'):
            print(json.dumps({'result':'fail','failed_checks':['control_plane_api_key'],
                'checks':[{'id':'config_source','status':'PASS'},
                          {'id':'profile_load','status':'PASS'},
                          {'id':'control_plane_api_key','status':'FAIL'}]}))
            sys.exit(2)
    if os.getenv('FAKE_DOCTOR') == 'fail':
        print(json.dumps({'result':'fail','failed_checks':['control_plane_api_key'],
                          'checks':[{'id':'config_source','status':'PASS'},
                                    {'id':'profile_load','status':'PASS'},
                                    {'id':'control_plane_api_key','status':'FAIL'}]}))
        sys.exit(2)
    print(json.dumps({'result':'ok','failed_checks':[],
                      'checks':[{'id':'config_source','status':'PASS'},
                                {'id':'profile_load','status':'PASS'},
                                {'id':'control_plane_api_key','status':'PASS'}]}))
    sys.exit(0)
if mode == 'run':
    if os.getenv('FAKE_REQUIRE_LEGACY_PROFILE_ENV') == 'yes':
        assert os.getenv('CONTROL_PLANE_API_KEY', '').startswith('sk-SYNTHETIC')
    assert '--profile-file' in sys.argv
    assert any(a.startswith('--control-plane.api-key=file:') for a in sys.argv)
    print('FAKE_TUNNEL_RUN=OK')
    sys.exit(0)
sys.exit(55)
'''

class E05RuntimeContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="e05-offline-contract-")
        self.addCleanup(self.tmp.cleanup)
        d = Path(self.tmp.name)
        self.profile = d / 'e05-profile.yaml'
        self.profile.write_text('config_version: 1\n', encoding='utf8')
        self.binary = d / 'tunnel-client'
        self.binary.write_text(FAKE_TUNNEL, encoding='utf8')
        self.binary.chmod(0o755)
        self.credentialdir = d / 'credentials'
        self.credentialdir.mkdir()
        self.credential = self.credentialdir / 'control_plane_api_key'
        self.credential.write_text('sk-' + 'SYNTHETIC' * 5, encoding='ascii')
        self.launcher = d / 'launch.sh'
        original = LAUNCHER.read_text()
        synthetic = (original
            .replace('CLIENT=/opt/meu-artigo-e05/bin/tunnel-client', 'CLIENT=' + str(self.binary))
            .replace('PROFILE=/opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml', 'PROFILE=' + str(self.profile))
            .replace('== meuartigo-e05', '== ' + getpass.getuser()))
        self.launcher.write_text(synthetic, encoding='utf8')

    def run_launcher(self, extra_env=None, args=()):
        env = os.environ.copy()
        env['CREDENTIALS_DIRECTORY'] = str(self.credentialdir)
        if extra_env: env.update(extra_env)
        return subprocess.run(['bash',str(self.launcher),*args],env=env,text=True,
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=8)

    def test_same_profile_and_credential_doctor_and_run(self):
        p=self.run_launcher()
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('E05_RUNTIME_LOCAL_CONTRACT=PASS',p.stdout)
        self.assertIn('FAKE_TUNNEL_RUN=OK',p.stdout)
        self.assertNotIn('sk-SYNTHETIC',p.stdout+p.stderr)

    def test_legacy_profile_env_reference_resolves_from_protected_file(self):
        # The original E05 profile resolves env:CONTROL_PLANE_API_KEY
        # before the explicit file: flag is applied. The caller environment
        # may have no key or a stale value; LoadCredential stays authoritative.
        case = {'FAKE_REQUIRE_LEGACY_PROFILE_ENV': 'yes',
                'CONTROL_PLANE_API_KEY': 'stale-synthetic-not-secret'}
        probe = self.run_launcher(case, args=('--doctor-only',))
        self.assertEqual(probe.returncode, 0, probe.stderr)
        self.assertIn('E05_RUNTIME_DOCTOR_ONLY=PASS', probe.stdout)
        self.assertNotIn('SYNTHETIC', probe.stdout + probe.stderr)
        run = self.run_launcher(case)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('FAKE_TUNNEL_RUN=OK', run.stdout)
        self.assertNotIn('SYNTHETIC', run.stdout + run.stderr)

    def test_real_doctor_only_mode_does_not_start_tunnel(self):
        p = self.run_launcher(args=('--doctor-only',))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('E05_RUNTIME_DOCTOR_ONLY=PASS', p.stdout)
        self.assertNotIn('FAKE_TUNNEL_RUN=OK', p.stdout)
        self.assertEqual(self.run_launcher(args=('--other',)).returncode, 78)

    def test_no_npm_git_checkout_in_isolated_reactivation(self):
        script = (ROOT / 'scripts/e05-vps-activate-only.sh').read_text()
        self.assertIn('E05_ACTIVATE_REAL_SYSTEMD_DOCTOR=PASS', script)
        self.assertIn('E05_ACTIVATE_PINNED_SOURCE=VERIFIED', script)
        self.assertIn('LoadCredential=control_plane_api_key:$KEY', script)
        self.assertIn('RestartPreventExitStatus=78', script)
        self.assertIn('E05_ACTIVATE_ROLLBACK=ORIGINAL_WRAPPER_RESTORED_SERVICE_STOPPED', script)
        self.assertIn('LAUNCHER_BLOB=4fd0918974c03265df920d300ee3e69357ca6ea3', script)
        self.assertNotIn('npm ci', script)
        self.assertNotIn('git switch', script)
        self.assertNotIn('git reset --hard', script)
        self.assertNotIn('curl | bash', script)
        # Regression: systemd's non-root principal cannot traverse /root.
        self.assertIn('probe="$(mktemp -d /run/.e05-doctor-', script)
        self.assertIn('chown root:meuartigo-e05 "$probe"', script)
        self.assertIn('chmod 0750 "$probe"', script)
        self.assertIn('install -m 0750 -o root -g meuartigo-e05 -- "$work/launcher" "$probe/launcher"', script)
        self.assertIn('runuser -u meuartigo-e05 -- test -r "$probe/launcher"', script)
        self.assertIn('-- /bin/bash "$probe/launcher" --doctor-only', script)
        self.assertNotIn('-- /bin/bash "$work/launcher" --doctor-only', script)
        self.assertIn('rmdir "$probe"', script)

    def test_key_missing_or_invalid_rejects(self):
        self.credential.unlink()
        p=self.run_launcher()
        self.assertEqual(p.returncode,78)
        self.assertNotIn('FAKE_TUNNEL_RUN',p.stdout)
        self.credential.write_text('BAD-KEY',encoding='ascii')
        self.assertEqual(self.run_launcher().returncode,78)

    def test_official_doctor_fail_prevents_run(self):
        p=self.run_launcher({'FAKE_DOCTOR':'fail'})
        self.assertEqual(p.returncode,78)
        self.assertIn('DOCTOR_LOCAL_CONTRACT_FAILED',p.stderr)
        self.assertIn('E05_RUNTIME_DOCTOR_CONTROL_PLANE_API_KEY=FAIL',p.stderr)
        self.assertNotIn('sk-SYNTHETIC',p.stderr)
        self.assertNotIn('FAKE_TUNNEL_RUN',p.stdout)

    def test_profile_and_credential_directory_missing(self):
        self.profile.unlink()
        self.assertEqual(self.run_launcher().returncode,78)
        self.assertEqual(self.run_launcher({'CREDENTIALS_DIRECTORY':''}).returncode,78)

    def test_bootstrap_sources_launcher_and_prevents_config_restart_loop(self):
        source=BOOTSTRAP.read_text()
        self.assertIn('e05-vps-runtime-launch.sh',source)
        self.assertIn('RestartPreventExitStatus=78',source)
        self.assertIn('LoadCredential=control_plane_api_key:/etc/meu-artigo-e05/runtime-key',source)
        self.assertIn('install -m 0755 -o root -g root -- "$SOURCE_LAUNCHER" "$WRAPPER"',source)
        self.assertNotIn('exec "__TUNNEL_CLIENT_BIN__" run --profile ',source)
        self.assertNotIn('git reset --hard',source)
        self.assertNotIn('chown -R',source)

if __name__ == '__main__': unittest.main()
