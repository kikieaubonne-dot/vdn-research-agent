"""Recovery policy fixtures, distinct from the real whole-suite image trial."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from agent import mission
from scripts import eponge_recovery as recovery, eponge_guard as guard, eponge_validate as validator


class ExecutableRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.source=self.root/'source';self.source.mkdir();(self.source/'eponge.py').write_text("print('trusted fixture')\n")
        self.pin=self.root/'pin.json';guard.write(self.root,'pin.json',{'schema':'vdn.validation-baseline/1','files':validator.inventory(self.source)})
        self.validation=self.root/'validation';self.validation.mkdir();(self.validation/'tests.log').write_text('AUTHORED successful validator protocol fixture, not a real model/game result\n')
        guard.write(self.validation,'validation.json',{'state':'PASS','suite':'offline','exit_code':0,'pinned_inputs_changed':False,'manifest_sha256':recovery.sha(self.pin),'log_sha256':recovery.sha(self.validation/'tests.log')})
        self.image=self.root/'image';self.ws=self.root/'failed-workspace';(self.ws/'runtime/config').mkdir(parents=True)
        (self.ws/'runtime/config/fixture.json').write_text('{"counter":7}')
        (self.ws/'runtime/ledger.json').write_text('{"http_calls":31,"date":"2026-11-16"}')
        guard.write(self.ws,'mission.json',{**mission.DEFAULT,'enabled':True})
        mission.write_checkpoint(self.ws,{'schema':'vdn.mission-checkpoint/2','id':'3ef9d89e-cbd6-4cf1-ab5c-e4bb39023a0b','steps':{'one':{'state':'DONE','attempts':1,'result':{'state':'fixture'}}},'baseline_protected':{'config/fixture.json':recovery.sha(self.ws/'runtime/config/fixture.json')}})

    def seal(self):return recovery.seal(self.source,self.pin,self.validation,self.image,True)['image_sha256']

    def test_explicit_approval_and_apply_required(self):
        with self.assertRaises(PermissionError):recovery.seal(self.source,self.pin,self.validation,self.image)
        self.assertFalse(self.image.exists())
        h=self.seal()
        with self.assertRaises(PermissionError):recovery.recover(self.ws,self.image,h,self.root/'new')
        self.assertFalse((self.root/'new').exists())

    def test_changed_source_or_failed_validation_cannot_be_approved(self):
        (self.source/'eponge.py').write_text('unvalidated source change')
        with self.assertRaises(ValueError):self.seal()
        self.assertFalse(self.image.exists())

    def test_recovery_preserves_runtime_and_checkpoints_and_stays_disabled(self):
        h=self.seal();before=recovery.tree(self.ws/'runtime');cp=(self.ws/'checkpoint.json').read_bytes();dest=self.root/'new'
        result=recovery.recover(self.ws,self.image,h,dest,True)
        self.assertEqual(result['state'],'RECOVERED_DISABLED')
        self.assertEqual(before,recovery.tree(dest/'runtime'))
        self.assertEqual(before,recovery.tree(self.ws/'runtime'))
        self.assertEqual(cp,(dest/'checkpoint.json').read_bytes())
        self.assertFalse(json.loads((dest/'mission.json').read_text())['enabled'])
        self.assertEqual(json.loads((dest/'control.json').read_text())['state'],'STOPPED')
        guard.verify_code(dest)
        with self.assertRaises(ValueError):recovery.recover(self.ws,self.image,h,dest,True)

    def test_corrupt_image_refused_before_any_destination_write(self):
        h=self.seal();(self.image/'files/eponge.py').write_text('unapproved code')
        with self.assertRaises(ValueError):recovery.recover(self.ws,self.image,h,self.root/'new',True)
        self.assertFalse((self.root/'new').exists())

    def test_modified_approval_manifest_is_not_authorized_by_old_fingerprint(self):
        h=self.seal();record=json.loads((self.image/'image.json').read_text());record['approval']='MODEL_APPROVED';guard.write(self.image,'image.json',record)
        with self.assertRaises(ValueError):recovery.check_image(self.image,h)

    def test_data_corruption_is_not_repaired_by_switching_executable(self):
        h=self.seal();(self.ws/'runtime/config/fixture.json').write_text('corrupt reliable input')
        with self.assertRaises(ValueError):recovery.recover(self.ws,self.image,h,self.root/'new',True)
        self.assertFalse((self.root/'new').exists())
