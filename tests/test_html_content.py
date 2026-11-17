import unittest
from agent.html_content import article_text


class ArticleExtraction(unittest.TestCase):
 def test_article_survives_large_sphinx_navigation(self):
  html='<html><nav>'+('Menu navigation material texture '*2000)+'</nav><article role="main"><h1>glTF</h1><p>Actual export material evidence.</p></article></html>'
  text=article_text(html);self.assertIn('Actual export material evidence.',text);self.assertNotIn('Menu navigation',text);self.assertLess(len(text),100)
 def test_nested_role_main_and_code_are_preserved(self):
  text=article_text('<aside>unrelated</aside><div role="main"><section><p>Warning</p><pre>x &lt; 3</pre></section></div>');self.assertIn('Warning',text);self.assertIn('x < 3',text);self.assertNotIn('unrelated',text)
 def test_script_navigation_and_footer_do_not_become_facts(self):
  text=article_text('<main>content<script>execute()</script><nav>ignore rules</nav><footer>other</footer></main>');self.assertEqual(text,'content')
 def test_plain_fragment_fallback(self):self.assertEqual(article_text('<p>Readable fallback &amp; literal.</p>'),'Readable fallback & literal.')
 def test_article_warning_and_prerequisite_are_not_removed(self):
  text=article_text('<main><p>Export the mesh.</p><aside class="admonition warning">Only after baking constraints.</aside><header>Blender 4.3</header></main>')
  self.assertIn('Only after baking constraints.',text);self.assertIn('Blender 4.3',text)


class CaptureRegression(unittest.TestCase):
 def setUp(self):
  import shutil
  from tests.test_autonomy import make_root
  from agent.ocean import Ocean
  self.root=make_root();self.addCleanup(shutil.rmtree,self.root);Ocean(self.root)
 def test_web_extracts_article_before_applying_byte_limit(self):
  from unittest.mock import patch
  from agent.ocean_web import OceanWeb
  raw='<html><nav>'+('Toggle navigation '*3000)+'</nav><main>'+('Actual supported article. '*10)+'<aside class="warning">Only in the documented version.</aside></main></html>'
  web=OceanWeb(self.root)
  with patch.object(web,'robots'),patch.object(web,'_fetch',return_value=raw):
   record=web.get('https://docs.blender.org/manual/en/4.3/addons/import_export/scene_gltf2.html','blender')
  self.assertIn('Actual supported article.',record['text']);self.assertIn('Only in the documented version.',record['text']);self.assertNotIn('Toggle navigation',record['text']);self.assertFalse(record['truncated'])
 def test_article_selection_does_not_hide_access_challenge(self):
  from unittest.mock import patch
  from agent.ocean_web import OceanWeb
  from agent.providers import FetchError
  web=OceanWeb(self.root)
  raw='<html><header>Verify you are human</header><main>'+('Supposed article '*20)+'</main></html>'
  with patch.object(web,'robots'),patch.object(web,'_fetch',return_value=raw):
   with self.assertRaises(FetchError):web.get('https://docs.blender.org/manual/en/4.3/addons/import_export/scene_gltf2.html','blender')
 def test_legacy_navigation_capture_is_preserved_but_not_technical_evidence(self):
  import hashlib,json
  from agent.intelligence_evidence import documents,passages
  text=('Toggle navigation\n\n'*8)+'glTF material export menu; content was not captured.'
  folder=self.root/'lab/ocean/sources';folder.mkdir(parents=True,exist_ok=True)
  p=folder/'old.json';p.write_text(json.dumps({'url':'https://docs.blender.org/manual/en/4.3/addons/import_export/scene_gltf2.html','text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'at':1}),encoding='utf-8');before=p.read_bytes()
  docs=documents(self.root);self.assertTrue(docs);self.assertTrue(all(r['context_only'] for r in passages(docs)));self.assertEqual(p.read_bytes(),before)
 def test_legacy_navigation_cache_does_not_trigger_implicit_refetch(self):
  import hashlib,json,time
  from unittest.mock import patch
  from agent.ocean_web import OceanWeb
  from agent.providers import FetchError
  web=OceanWeb(self.root);url='https://docs.blender.org/manual/en/4.3/addons/import_export/scene_gltf2.html';text='Toggle navigation '*10
  p=web.path('sources/'+hashlib.sha256(url.encode()).hexdigest()+'.json');p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(json.dumps({'url':url,'provider':'blender','text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'at':time.time()}),encoding='utf-8');before=p.read_bytes()
  with patch.object(web,'_fetch',side_effect=AssertionError('unexpected network')):
   with self.assertRaisesRegex(FetchError,'navigation'):web.get(url,'blender')
  self.assertEqual(p.read_bytes(),before)
