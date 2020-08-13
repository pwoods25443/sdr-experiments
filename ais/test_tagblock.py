import unittest
from datetime import datetime
from click.testing import CliRunner
from tagblock import tagblock
from tagblock import add_tagblock
from tagblock import format_tagblock_t
from tagblock import extract_nmea
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from ais import stream as ais_stream

NMEA=[
    '!AIVDM,1,1,,A,15NTES0P00J>tC4@@FOhMgvD0D0M,0*49',
    '!AIVDM,1,1,,B,15O0TWP1h0J>uK:@@MgCA9TD00Ru,0*32',
    '!AIVDM,2,1,7,A,55PH6Ml000000000000<OCGK;<0000000000000k10613t0002P00000,0*5E',
    '!AIVDM,2,2,7,A,000000000000000,2*23'
]

class TestTagblockCli(unittest.TestCase):

    def test_basic_cli(self):
        runner = CliRunner()
        result = runner.invoke(tagblock, input="\n".join(NMEA))
        self.assertFalse(result.exception)
        output = result.output.split('\n')[:-1]
        self.assertEqual(len(output), len(NMEA))
        for item_in, item_out in zip(NMEA, output):
            self.assertTrue(len(item_in) < len(item_out))
            self.assertTrue(item_out.endswith(item_in))

    # make sure that our sample nmea messages parse correctly
    def test_nmea(self):
        for sentence in NMEA:
            tagblock, nmea = ais_stream.parseTagBlock(sentence)
            self.assertEqual(sentence, nmea)
            self.assertTrue(ais_stream.checksum.isChecksumValid(nmea))

    def test_add_tagblock(self):
        station = 'station'
        for sentence in NMEA:
            tagblock, nmea = ais_stream.parseTagBlock(add_tagblock(sentence, station))
            self.assertTrue(ais_stream.checksum.isChecksumValid(nmea))
            self.assertEqual(station, tagblock['tagblock_station'])
            # self.assertEqual(tagblock, '')
            c = format_tagblock_t(datetime.fromtimestamp(tagblock['tagblock_timestamp']))
            self.assertEqual(c, tagblock['tagblock_T'])

    def test_extract_nmea(self):
        for sentence in NMEA:
            nmea = extract_nmea("extra {}text".format(sentence))
            assert nmea == sentence


if __name__ == '__main__':
    unittest.main()
