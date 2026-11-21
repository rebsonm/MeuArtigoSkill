"""Synthetic-only regressions for optional conceptual RAG pilot; no user sources."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

_here=Path(__file__).resolve()
_module_dir=(_here.parent if (_here.parent/"rag.py").is_file() else _here.parents[1]/"experimental"/"conceptual_rag")
sys.path.insert(0, str(_module_dir))
import rag
import pdf_to_md


class ToyEncoder:
    """Only tests ranking math; NOT a semantic model."""
    def encode(self, texts, normalize_embeddings=True):
        out=[]
        for text in texts:
            s=text.casefold()
            x=3.0 if ('questionário' in s or 'survey' in s or 'quantitativ' in s) else 0.1
            y=3.0 if ('entrevista' in s or 'qualitativ' in s) else 0.1
            z=(x*x+y*y)**0.5
            out.append([x/z,y/z])
        return out


class ConceptualRAGTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory(); self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.lib=self.root/'02_Biblioteca_MD';self.lib.mkdir()
        self.idx=self.root/'04_Indice_Semantico'

    def source(self, sid, page1, rights='PRIVATE_AUTHORIZED',status='HUMAN_REVIEWED'):
        md=self.lib/(sid+'.md');s=f'# {sid}\n\n<!-- source_page: 1 -->\n\n{page1}\n'
        md.write_text(s,encoding='utf-8')
        (self.lib/(sid+'.md.meta.json')).write_text(json.dumps({
            'schema':'MEU_ARTIGO_MD_SOURCE_V1','source_id':sid,'title':sid,
            'rights_status':rights,'extraction_status':status,'page_count':1,
            'md_sha256':hashlib.sha256(s.encode()).hexdigest()}),encoding='utf-8')
        return md

    def test_lexical_retrieves_with_provenance_and_read_only(self):
        self.source('A01','A pesquisa quantitativa utiliza questionário para mensurar respostas observadas.')
        self.source('B01','A pesquisa qualitativa utiliza entrevista para compreender experiências.')
        before={x.name:x.read_bytes() for x in self.lib.iterdir()}
        man=rag.create_index(self.lib,self.idx)
        self.assertEqual(man['retrieval'],'LEXICAL_ONLY')
        self.assertEqual(man['source_count'],2)
        response=rag.search(self.idx,'questionário quantitativa')
        self.assertEqual(response['hits'][0]['source_id'],'A01')
        self.assertEqual(response['hits'][0]['page'],1)
        self.assertEqual(response['hits'][0]['evidence_type'],'RETRIEVED_TEXT_NOT_SEMANTICALLY_VALIDATED')
        self.assertFalse(response['scientific_quality_validated'])
        self.assertTrue(response['read_only'])
        self.assertEqual(before,{x.name:x.read_bytes() for x in self.lib.iterdir()})

    def test_private_source_without_manual_review_is_blocked(self):
        self.source('A01','Texto fictício.',status='REVIEW_REQUIRED')
        with self.assertRaisesRegex(ValueError,'NOT_AUTHORIZED_OR_REVIEWED'):
            rag.create_index(self.lib,self.idx)
        self.assertFalse(self.idx.exists())

    def test_unclear_rights_are_blocked(self):
        self.source('A01','Texto fictício.',rights='NOT_REVIEWED')
        with self.assertRaisesRegex(ValueError,'NOT_AUTHORIZED_OR_REVIEWED'):
            rag.create_index(self.lib,self.idx)

    def test_sha_mismatch_is_blocked(self):
        p=self.source('A01','Texto fictício.')
        p.write_text(p.read_text()+'adulterado')
        with self.assertRaisesRegex(ValueError,'HASH_MISMATCH'):
            rag.create_index(self.lib,self.idx)

    def test_hybrid_index_and_model_unavailable_honesty(self):
        self.source('A01','Uma abordagem quantitativa utiliza questionários aplicados.')
        self.source('B01','Uma abordagem qualitativa utiliza entrevistas individuais.')
        man=rag.create_index(self.lib,self.idx,encoder=ToyEncoder())
        self.assertEqual(man['retrieval'],'HYBRID_LOCAL')
        a=rag.search(self.idx,'entrevista qualitativa',encoder=ToyEncoder())
        self.assertEqual(a['retrieval_mode'],'HYBRID_LOCAL')
        self.assertEqual(a['hits'][0]['source_id'],'B01')
        b=rag.search(self.idx,'entrevista qualitativa')
        self.assertEqual(b['retrieval_mode'],'LEXICAL_ONLY')
        self.assertIn('VECTOR_INDEX_PRESENT_BUT_NO_LOCAL_QUERY_ENCODER',b['warnings'])

    def test_index_tamper_detected(self):
        self.source('A01','Texto fictício.')
        rag.create_index(self.lib,self.idx)
        (self.idx/'chunks.jsonl').write_text('alterado')
        with self.assertRaisesRegex(ValueError,'INDEX_DIGEST_MISMATCH'):
            rag.search(self.idx,'texto')

    def test_create_only_guard_prevents_silent_reindex_overwrite(self):
        self.source('A01','Texto fictício.')
        rag.create_index(self.lib,self.idx)
        with self.assertRaisesRegex(ValueError,'CREATE_NEW_INDEX_DIRECTORY_REQUIRED'):
            rag.create_index(self.lib,self.idx)

    def test_pdf_to_md_never_claims_reviewed_or_authorized(self):
        try: import fitz
        except ImportError:self.skipTest('PyMuPDF optional for PDF smoke')
        pdf=self.root/'sample.pdf'
        doc=fitz.open(); page=doc.new_page()
        page.insert_text((72,72),'Synthetic methods example. ' * 12)
        doc.save(str(pdf));doc.close()
        old=pdf.read_bytes()
        path=self.lib/'P01.md'
        output=pdf_to_md.convert(pdf,path,source_id='P01',title='Fictional Methodology')
        self.assertEqual(output['pages'],1)
        self.assertEqual(pdf.read_bytes(),old)
        self.assertIn('<!-- source_page: 1 -->',path.read_text())
        meta=json.loads((self.lib/'P01.md.meta.json').read_text())
        self.assertEqual(meta['extraction_status'],'REVIEW_REQUIRED')
        self.assertEqual(meta['rights_status'],'NOT_REVIEWED')
        with self.assertRaisesRegex(ValueError,'NOT_AUTHORIZED_OR_REVIEWED'):
            rag.create_index(self.lib,self.idx)

if __name__=='__main__':unittest.main()
