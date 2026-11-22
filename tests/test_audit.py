import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from date_validation_claim_audit.audit import audit, evidence, matches
from date_validation_claim_audit.phrases import DATEVALIDATION, NODATEVALIDATION, GENERIC_NAMES

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual(tuple(map(lambda x: len(set(x)), (DATEVALIDATION, NODATEVALIDATION, GENERIC_NAMES))), (50, 24, 24))
        for phrase in DATEVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(matches(phrase)[0])
        for phrase in NODATEVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(matches(phrase)[0], [])
        self.assertEqual(matches('```\nvalidate date\n```\n\n`check-date`')[0], ['check date'])
    def test_library_routes(self):
        sources = ['import datetime as d\nd.datetime.strptime()', 'from datetime import date as d\nd.fromisoformat()', 'import datetime\ndatetime.datetime.strptime()', 'import datetime\ndatetime.datetime.fromisoformat()', 'import datetime\ndatetime.date.fromisoformat()', 'import dateutil.parser as p\np.isoparse()', 'from dateutil.parser import parse as p\np()', 'import dateutil.parser as p\np.parse()', 'from dateutil.parser import isoparse as p\np()', 'import arrow as a\na.get(value)', 'from arrow import get as g\ng(value)', 'import pendulum as p\np.from_format()', 'from pendulum import parse as p\np()', 'import pendulum as p\np.parse()', 'from pendulum import from_format as p\np()', 'import dateparser as d\nd.parse()', 'from dateparser import parse as p\np()', 'from maya import parse as p\np()', 'import maya as m\nm.parse()', 'import delorean as d\nd.parse()', 'from delorean import parse as p\np()', 'from django.utils.dateparse import parse_date as p\np()', 'import django.utils.dateparse\ndjango.utils.dateparse.parse_date()']
        for source in sources:
            with self.subTest(source=source): self.assertTrue(evidence(source))
        for name in GENERIC_NAMES:
            with self.subTest(name=name):
                self.assertTrue(evidence('x.' + name + '()'))
                self.assertTrue(evidence('from foo import ' + name + ' as f\nf()'))
    def test_not_evidence(self):
        cases = ['import datetime', 'strptime()', 'fromisoformat()', 'parse()', 'isoparse()', 'get()', 'from_format()', 'parse_date()', 'x.strptime()', 'x.fromisoformat()', 'x.parse()', 'x.isoparse()', 'x.get()', 'x.from_format()', 'x.parse_date()', 'import datetime\ndatetime.date(2023,2,30)', 'import datetime\ndatetime.datetime(2023,2,1)', 'import datetime\ndatetime.datetime.now()', 'import datetime\ndatetime.datetime.today()', 'import datetime\ndatetime.datetime.utcnow()', 'import datetime\ndatetime.date.today()', 'import datetime\ndatetime.datetime.strftime()', 'import datetime\ndatetime.date.isoformat()', 'import datetime\ndatetime.datetime.isoformat()', 'import datetime\ndatetime.datetime.fromtimestamp()', 'import datetime\ndatetime.date.fromtimestamp()', 'import datetime\ndatetime.datetime.fromordinal()', 'import datetime\ndatetime.date.fromordinal()', 'import datetime\ndatetime.datetime.combine()', 'import arrow\narrow.get()', 'import arrow\narrow.now()', 'import pendulum\npendulum.now()', 'import maya\nmaya.now()', 'import delorean\ndelorean.now()', 'import calendar\ncalendar.monthrange()', 'import calendar\ncalendar.isleap()', 'import dateutil\ndateutil.tz()', 'tzinfo()', 'import django\ndjango.utils.dateparse.parse_datetime()', 'import django\ndjango.utils.dateparse.parse_time()', 'import re\nre.match("date", x)', 'import re\nre.search("date", x)', 'import re\nre.fullmatch("date", x)', 'import validators\nvalidators.email(x)', 'import validators\nvalidators.url(x)', 'import validators\nvalidators.ipv4(x)', 'import validators\nvalidators.ipv6(x)', 'obj.validate_email()', 'obj.validate_phone()', 'obj.extract()', 'import subprocess\nsubprocess.run(["validator"])', '"validate date"', 'import arrow\narrow.get', 'invalid ! syntax', 'import arrow\narrow = x\narrow.get(x)', 'from arrow import get\ndef get(): pass\nget(x)', 'def validate_date(): pass\nx.validate_date()']
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))
        self.assertTrue(evidence('x = object()\nx.validate_date()'))
        self.assertFalse(evidence('import arrow\nwith x as arrow: pass\narrow.get(x)'))
    def test_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'README.md').write_text('validate date')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_x.py').write_text('import arrow\narrow.get(x)')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'MEDIUM')
            (p/'app.py').write_text('import arrow\narrow.get(x)')
            self.assertEqual(audit(p)['findings'], [])
            (p/'README.md').write_text('does not validate date')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')
            self.assertEqual(audit(p, ['app.py'])['findings'], [])
            (p/'app.py').unlink(); (p/'tests/test_x.py').unlink()
            self.assertEqual(audit(p)['findings'], [])
    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'README.md').write_text('validate date')
            cmd=[sys.executable, '-m', 'date_validation_claim_audit']
            result=subprocess.run(cmd+['audit', tmp, '--json'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2); self.assertEqual(json.loads(result.stdout)['findings'][0]['severity'], 'HIGH')
            self.assertEqual(subprocess.run(cmd+['audit', tmp, '--fail-on', 'bad'], capture_output=True).returncode, 1)
            self.assertEqual(subprocess.run(cmd+['--version'], capture_output=True, text=True).stdout.strip(), '0.1.0')
    def test_self_audit(self):
        self.assertEqual(audit(Path(__file__).resolve().parents[1])['findings'], [])

if __name__ == '__main__': unittest.main()
