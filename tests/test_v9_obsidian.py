import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from agent import knowledge, obsidian
from agent.storage import atomic_write


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'source';self.dest=Path(self.tmp.name)/'bundle'
        self.note=self.root/'knowledge'/'rig'/'fixture.md';self.note.parent.mkdir(parents=True)
        self.note.write_text(knowledge.dump_frontmatter({'id':'vdn-fixture','title':'Rig','source_tier':1})+'\n# Rig\nOriginal evidence.')

    def test_simulation_has_no_writes(self):
        r=obsidian.sync(self.root,self.dest)
        self.assertEqual(r['state'],'simulation');self.assertFalse(self.dest.exists())

    def test_apply_twice_no_duplicate_and_personal_settings_preserved(self):
        settings=self.dest/'knowledge'/'.obsidian'/'settings.json';settings.parent.mkdir(parents=True)
        settings.write_text('personal')
        r=obsidian.sync(self.root,self.dest,apply=True)
        self.assertEqual(r['written'],1)
        self.assertEqual(obsidian.sync(self.root,self.dest,apply=True)['state'],'unchanged')
        self.assertEqual(len(list((self.dest/'knowledge').rglob('fixture.md'))),1)
        self.assertEqual(settings.read_text(),'personal')
        self.assertEqual((self.dest/'knowledge'/'rig'/'fixture.md').read_bytes(),self.note.read_bytes())

    def test_user_conflict_blocks_entire_sync(self):
        obsidian.sync(self.root,self.dest,apply=True)
        target=self.dest/'knowledge'/'rig'/'fixture.md';target.write_text('user changes')
        self.note.write_text(self.note.read_text()+'\nNew evidence')
        (self.note.parent/'new.md').write_text('new note')
        r=obsidian.sync(self.root,self.dest,apply=True)
        self.assertEqual(r['state'],'conflict');self.assertEqual(r['written'],0)
        self.assertEqual(target.read_text(),'user changes');self.assertFalse((target.parent/'new.md').exists())

    def test_untracked_target_never_overwritten(self):
        target=self.dest/'knowledge'/'rig'/'fixture.md';target.parent.mkdir(parents=True);target.write_text('user note')
        self.assertEqual(obsidian.sync(self.root,self.dest,apply=True)['state'],'conflict')
        self.assertEqual(target.read_text(),'user note')

    def test_update_has_backup_and_rollback_restores_it(self):
        obsidian.sync(self.root,self.dest,apply=True);original=self.note.read_text()
        self.note.write_text(original+'\nNew version')
        r=obsidian.sync(self.root,self.dest,apply=True)
        self.assertEqual(obsidian.rollback(self.dest,r['transaction'])['state'],'rollback_simulation')
        obsidian.rollback(self.dest,r['transaction'],apply=True)
        self.assertEqual((self.dest/'knowledge'/'rig'/'fixture.md').read_text(),original)
        self.assertTrue(list((self.dest/'.vdn-sync'/'backups').rglob('*.md')))

    def test_rollback_creation_archives_instead_of_deleting(self):
        r=obsidian.sync(self.root,self.dest,apply=True)
        obsidian.rollback(self.dest,r['transaction'],apply=True)
        self.assertTrue(list((self.dest/'.vdn-sync'/'archives').rglob('fixture.md')))
        self.assertFalse((self.dest/'knowledge'/'rig'/'fixture.md').exists())

    def test_rollback_refuses_user_changes(self):
        r=obsidian.sync(self.root,self.dest,apply=True)
        target=self.dest/'knowledge'/'rig'/'fixture.md';target.write_text('personal')
        self.assertEqual(obsidian.rollback(self.dest,r['transaction'],apply=True)['state'],'conflict')
        self.assertEqual(target.read_text(),'personal')

    def test_interruption_resumes_without_duplicate(self):
        def interrupted(path,*args,**kwargs):
            if path.name=='fixture.md':raise KeyboardInterrupt()
            return atomic_write(path,*args,**kwargs)
        with patch('agent.obsidian.atomic_write',side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):obsidian.sync(self.root,self.dest,apply=True)
        r=obsidian.sync(self.root,self.dest,apply=True)
        self.assertTrue(r['resumed']);self.assertEqual(r['state'],'committed')
        self.assertEqual(obsidian.sync(self.root,self.dest,apply=True)['state'],'unchanged')

    def test_interruption_after_write_before_manifest_is_recovered(self):
        def interrupted(path,*args,**kwargs):
            if path.name=='manifest.json':raise KeyboardInterrupt()
            return atomic_write(path,*args,**kwargs)
        with patch('agent.obsidian.atomic_write',side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):obsidian.sync(self.root,self.dest,apply=True)
        self.assertEqual(obsidian.sync(self.root,self.dest,apply=True)['state'],'committed')

    def test_source_removal_does_not_delete_destination(self):
        obsidian.sync(self.root,self.dest,apply=True);self.note.unlink()
        obsidian.sync(self.root,self.dest,apply=True)
        self.assertTrue((self.dest/'knowledge'/'rig'/'fixture.md').exists())

    def test_unsafe_paths_and_symlink_refused(self):
        for path in ('../outside','/etc/passwd','knowledge/../../outside'):
            with self.assertRaises(ValueError):obsidian.safe_path(self.dest,path)
        elsewhere=Path(self.tmp.name)/'elsewhere';elsewhere.mkdir()
        self.dest.mkdir()
        try:(self.dest/'knowledge').symlink_to(elsewhere,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest('symlinks unavailable')
        with self.assertRaises(ValueError):obsidian.sync(self.root,self.dest,apply=True)

    def test_source_destination_overlap_refused(self):
        with self.assertRaises(ValueError):obsidian.sync(self.root,self.root/'export',apply=True)

    def test_tampered_transaction_refused(self):
        def interrupt(path,*args,**kwargs):
            if path.name=='fixture.md':raise KeyboardInterrupt()
            return atomic_write(path,*args,**kwargs)
        with patch('agent.obsidian.atomic_write',side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):obsidian.sync(self.root,self.dest,apply=True)
        path=next((self.dest/'.vdn-sync'/'transactions').glob('*.json'))
        record=json.loads(path.read_text());record['operations'][0]['content']='tampered'
        path.write_text(json.dumps(record))
        with self.assertRaises(ValueError):obsidian.sync(self.root,self.dest,apply=True)
        self.assertFalse((self.dest/'knowledge'/'rig'/'fixture.md').exists())

    def test_windows_crlf_bytes_survive_copy_backup_and_rollback(self):
        original=self.note.read_bytes().replace(b'\n',b'\r\n');self.note.write_bytes(original)
        obsidian.sync(self.root,self.dest,apply=True)
        target=self.dest/'knowledge'/'rig'/'fixture.md'
        self.assertEqual(target.read_bytes(),original)
        self.note.write_bytes(original+b'\r\nNew evidence\r\n')
        r=obsidian.sync(self.root,self.dest,apply=True)
        obsidian.rollback(self.dest,r['transaction'],apply=True)
        self.assertEqual(target.read_bytes(),original)
