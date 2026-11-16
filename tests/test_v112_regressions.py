"""Independent counterexamples found during the V11.2 audit."""
import json
import shutil
import unittest
from unittest.mock import patch
from agent import intelligence_evidence as ev
from agent.intelligence import Intelligence,validate_model
from agent.knowledge import dump_frontmatter
from bench.evaluate_intelligence import corpus
from tests.test_autonomy import make_root


class AuditRegressions(unittest.TestCase):
    def setUp(self):
        self.root=make_root();self.addCleanup(shutil.rmtree,self.root);_,self.docs=corpus();self.brain=Intelligence(self.root)
    def test_model_property_must_be_supported_by_the_cited_passage(self):
        selected=ev.passages(self.docs);light=next(p for p in selected if p['document_id']=='lighting' and 'SpotLight' in p['text'])
        model={'diagnosis':'Hypothèse à tester.','claims':[],'uncertainties':[],'priorities':[],
               'procedures':[{'problem':'collision','why':'Proposition à comparer.','conditions':'Laboratoire isolé.',
                    'steps':['Inspecter CanCollide.','Consigner le parcours témoin.'],'passage_ids':[light['id']],'rollback':'Restaurer les copies.'}]}
        result=validate_model(model,selected,self.docs,ev.analyze('Roblox collisions'))
        self.assertEqual(result['procedures'],[],'An identifier elsewhere in the bundle cannot support this citation.')
    def test_unknown_claim_engine_cannot_hide_an_unreal_source(self):
        d={**self.docs[0],'engine':'Unreal','text':'Nanite is restricted to Unreal in this authored negative test fixture.'}
        import hashlib
        d['sha256']=hashlib.sha256(d['text'].encode()).hexdigest();p=ev.passages([d])[0]
        c=ev.verify({'text':d['text'],'kind':'SOURCE_SUPPORTED','engine':'unknown','version':'unknown','passage_ids':[p['id']]},[p],[d],ev.analyze('Roblox geometry'))
        self.assertNotEqual(c['support'],'SOURCE_SUPPORTED')
    def test_long_question_must_fit_the_mcp_context_budget(self):
        result=self.brain.brief('x'*2000,500)
        self.assertLessEqual(len(json.dumps(result,ensure_ascii=False)),1800)
    def test_brief_preserves_abstention_for_an_unknown_exact_fps(self):
        question='Quel FPS exact donne B3 dans Roblox ?'
        result=self.brain.run(question,documents=self.docs)
        self.assertTrue(result['abstained']);self.assertTrue(result['facts'])
        with patch.object(self.brain,'run',return_value=result):brief=self.brain.brief(question,8000)
        self.assertTrue(brief['abstained_from_established_facts'])
    def test_each_secondary_quote_keeps_its_actual_source_url(self):
        urls=['https://create.roblox.com/docs/fixture-collision','https://docs.blender.org/manual/fixture-export']
        folder=self.root/'knowledge';folder.mkdir()
        meta={'id':'citation-pair','title':'Two source fixture','sources':urls,'source_tier':4,'engine_version':'unknown'}
        body='\n> « A collision passage from the authored Roblox test document. »\n> — [source]('+urls[0]+')\n\n> « An export passage from the authored Blender test document. »\n> — [source]('+urls[1]+')\n'
        (folder/'pair.md').write_text(dump_frontmatter(meta)+body,encoding='utf-8')
        docs=ev.documents(self.root);export=next(d for d in docs if 'export passage' in d['text'])
        self.assertEqual(export['url'],urls[1]);self.assertEqual(export['engine'],'Blender')
    def test_quality_weighting_precedes_candidate_truncation(self):
        original={**self.docs[0],'id':'original','title':'Original reference','text':'CanCollide collision behavior is recorded here.','independent':True}
        secondary={**self.docs[0],'id':'secondary','title':'CanCollide collision CanCollide collision','text':'CanCollide collision behavior appears in an editorial note.','independent':False}
        selected=ev.retrieve('Roblox collision',[original,secondary],1,queries=['CanCollide collision'])
        self.assertEqual(selected[0]['document_id'],'original')
    def test_identical_source_cache_records_do_not_double_evidence(self):
        import hashlib,time
        folder=self.root/'lab/ocean/sources';folder.mkdir(parents=True)
        text='An authored CanCollide collision source for the duplicate-cache test.'
        record={'url':'https://create.roblox.com/docs/fixture','text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
                'version':'unknown','at':time.time(),'published':None,'truncated':False,'provider':'roblox'}
        (folder/'a.json').write_text(json.dumps(record));(folder/'b.json').write_text(json.dumps(record))
        self.assertEqual(len(ev.documents(self.root)),1)
    def test_wrong_type_source_snapshot_is_isolated_with_a_diagnostic(self):
        folder=self.root/'lab/ocean/sources';folder.mkdir(parents=True)
        (folder/'corrupt.json').write_text(json.dumps({'url':'https://create.roblox.com/docs/fixture','text':3,'text_sha256':'bad'}))
        diagnostics=[];self.assertFalse(ev.documents(self.root,diagnostics));self.assertTrue(diagnostics)


if __name__=='__main__':unittest.main()
