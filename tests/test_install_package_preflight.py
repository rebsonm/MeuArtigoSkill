"""Skill-only ZIP diagnostic; all fixtures are synthetic."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys,tempfile,unittest,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from check_install_package import diagnose

class SkillInstallTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.p=Path(self.t.name)/"sample.zip"
        self.skill="---\nname: meu-artigo\ndescription: Scientific research Skill\n---\n"
    def write(self,files):
        with ZipFile(self.p,"w",ZIP_DEFLATED) as z:
            for k,v in files.items():z.writestr(k,v)
    def test_valid_root_skill(self):
        self.write({"SKILL.md":self.skill,"VERSION":"0.9.0-beta.4"})
        self.assertTrue(diagnose(self.p)["valid"])
    def test_source_checkout_rejected(self):
        self.write({"MeuArtigoSkill-main/SKILL.md":self.skill,"MeuArtigoSkill-main/VERSION":"beta"})
        self.assertEqual(diagnose(self.p)["kind"],"SOURCE_CHECKOUT")
    def test_unknown_zip_rejected(self):
        self.write({"unrelated.txt":"no"})
        self.assertFalse(diagnose(self.p)["valid"])
    def test_bad_zip_rejected(self):
        self.p.write_text("bad zip")
        self.assertFalse(diagnose(self.p)["valid"])
    def test_missing_file_rejected(self):
        self.assertEqual(diagnose(self.p)["reason"],"FILE_NOT_FOUND")
    def test_invalid_skill_yaml_rejected(self):
        self.write({"SKILL.md":"no metadata"})
        self.assertEqual(diagnose(self.p)["reason"],"INVALID_ENTRYPOINT")
    def test_real_built_skill_is_recognized(self):
        from build_skill_bundle import package
        from version_info import read_version
        with tempfile.TemporaryDirectory() as folder:
            name=Path(folder)/f"MeuArtigoSkill-v{read_version(ROOT)}.zip"
            package(ROOT,name)
            self.assertTrue(diagnose(name)["valid"])
            with ZipFile(name) as z:
                names=set(z.namelist())
                self.assertNotIn("tests/test_bundle_release.py",names)
                self.assertNotIn("scripts/release_audit.py",names)
                self.assertNotIn("docs/PROTOCOLO-BETA-USUARIOS.md",names)
                self.assertNotIn("benchmarks/public_review_reference_v1.json",names)
    def test_cli_json(self):
        self.write({"SKILL.md":self.skill})
        proc=subprocess.run([sys.executable,str(ROOT/"scripts/check_install_package.py"),str(self.p),"--json"],capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["kind"],"SKILL")

if __name__=="__main__":unittest.main()
