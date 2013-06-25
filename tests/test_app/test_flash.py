#! /usr/bin/env python
# file: test_flash.py

# Tests for the flash.py application controller.
# FLASh v1.2.6
# http://ccb.jhu.edu/software/FLASH/
# using test_mafft.py as a guide

from cogent.util.unit_test import TestCase, main
from cogent.app.flash import Flash, default_assemble
from subprocess import Popen, PIPE, STDOUT
from os import getcwd, remove, rmdir, mkdir, path
#from tempfile import mkdtemp#, tempdir

__author__ = "Michael Robeson"
__copyright__ = "Copyright 2007-2013, The Cogent Project"
__credits__ = ["Michael Robeson"]
__license__ = "GPL"
__version__ = "1.5.3-dev"
__maintainer__ = "Michael Robeson"
__email__ = "robesonms@ornl.gov"
__status__ = "Development"

class GenericFlash(TestCase):
    
    def setUp(self):
        """Flash general setup fo all tests"""

        self.temp_dir = '/tmp/test_for_flash/'
        try:
            mkdir(self.temp_dir)
        except OSError:
            pass        

        self.temp_dir_spaces = '/tmp/test for flash/'
        try:
            mkdir(self.temp_dir_spaces)
        except OSError:
            pass
        
        try:
            # create fastq files'
            p1 = path.join(self.temp_dir,'reads1.fastq')
            #print 'p1', p1
            reads1 = open(p1,'w')
            reads1.write(reads1_string) # bottom of file
            reads1.close()
            self.test_fn1 = self.temp_dir + 'reads1.fastq'
            self.test_fn1_space = self.temp_dir_spaces + 'reads1.fastq'

            p2 = path.join(self.temp_dir,'reads2.fastq')
            #print 'p2', p2
            reads2 = open(p2,'w')
            reads2.write(reads2_string) # bottom of file
            reads2.close()
            self.test_fn2 = self.temp_dir + 'reads2.fastq'
            self.test_fn2_space = self.temp_dir_spaces + 'reads2.fastq'

        except OSError:
            pass

    def writeTmpFastq(self, fw_reads_path, rev_reads_path):
        """write forward and reverse reads data to temp fastq files"""
        fq1 = open(fw_reads_path, "w+")
        fq1.write(reads1_string)
        fq1.close()
        fq2 = open(rev_reads_path, "w+")
        fq2.write(reads2_string)
        fq2.close()

class FlashTests(GenericFlash):
    """Tests for FLASh application controller."""

    def check_version(self):
        """ Set up some objects / data for use by tests"""

        # Check if flash version is supported for this test
        accepted_version = (1,2,5)
        command = "flash --version"
        version_cmd = Popen(command, shell=True, universal_newlines=True,\
               stdout=PIPE,stderr=STDOUT)
        stdout = version_cmd.stdout.read()
        #print stdout
        version_string = stdout.strip().split('\n')[0].split('v')[1]
        #print version_string
        try:
            version = tuple(map(int, version_string.split('.')))
            #print version
            pass_test = version == accepted_version
        except ValueError:
            pass_test = False
            version_string = stdout
        self.assertTrue(pass_test,\
            "Unsupported flash version. %s is required, but running %s." \
            %('.'.join(map(str, accepted_version)), version_string))


    def test_base_command(self):
        """ flash base command should return correct BaseCommand """

        c = Flash()
        # test base command
        self.assertEqual(c.BaseCommand,\
            ''.join(['cd "', getcwd(), '/"; ', 'flash']))
        # test turning on a parameter
        c.Parameters['-M'].on('500')
        self.assertEqual(c.BaseCommand,\
            ''.join(['cd "', getcwd(), '/"; ', 'flash -M 500']))

        # test turning on another parameter via synonym
        # '--phred-offset' should use '-p'
        c.Parameters['--phred-offset'].on('33')
        self.assertEqual(c.BaseCommand,\
            ''.join(['cd "', getcwd(), '/"; ', 'flash -M 500 -p 33']))

    def test_changing_working_dir(self):
        c = Flash(WorkingDir='/temp/flash_test')
        self.assertEqual(c.BaseCommand,\
            ''.join(['cd "', '/temp/flash_test', '/"; ', 'flash'])) 
        c = Flash()
        c.WorkingDir = '/temp/flash_test2'
        self.assertEqual(c.BaseCommand,\
            ''.join(['cd "', '/temp/flash_test2', '/"; ', 'flash'])) 

    def test_default_assemble(self):
        """default_assemble: should work as expected"""
        self.writeTmpFastq(self.test_fn1, self.test_fn2)
        #print 'default 1: ', self.test_fn1
        #print 'default 2: ', self.test_fn2
        res = default_assemble(self.test_fn1, self.test_fn2, '/tmp','out')#, HALT_EXEC=True)
        #res = default_assemble('/tmp/test_for_flash/reads1.fastq', '/tmp/test_for_flash/reads2.fastq', '/tmp', 'out', HALT_EXEC=True)
        #print res['Assembled'].read()
        
        # test file contents are valid:
        #expected_assembled = # set to string at bottom of file
        #expected_nc1 = # set to string at bottom of file
        #expected_nc2 = # set to string at bottom of file
        #expected_nhist = # set to string at bottom of file
        #expected_hist = # set to string at bottom of file
        
        #self.assertEqual(res['Assembled'].read(), expected_assembled)
        #self.assertEqual(res['UnassembledReads1'].read(), expected_nc1)
        #self.assertEqual(res['UnassembledReads2'].read(), expected_nc2)
        #self.assertEqual(res['NumHist'].read(), expected_nhist)
        #self.assertEqual(res['Histogram'].read(), expected_hist)
        



reads1_string ="""@MISEQ03:64:000000000-A2H3D:1:1101:14358:1530 1:N:0:TCCACAGGAGT
TNCAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTGAAACTGACACTGAGGGGCGAAAGCGGGGGGGGCAAACG
+
?#5<????DDDDDDDDEEEEFFHHHHHHHHHHHHHHDCCHHFGDEHEH>CCE5AEEHHHHHHHHHHHHHHHHHFFFFHHHHHHEEADEEEEEEEEEEEEEEEEEEEEEEE?BEEEEEEEEEEEAEEEE0?A:?EE)8;)0ACEEECECCECAACEE?>)8CCC?CCA8?88ACC*A*::A??:0?C?.?0:?8884>'.''..'0?8C?C**0:0::?ECEE?############################
@MISEQ03:64:000000000-A2H3D:1:1101:14206:1564 1:N:0:TCCACAGGAGT
TACGTAGGGTGCGAGCGTTAATCGGAATTACTGGGCGTAAAGCGTGCGCAGGCGGTTTTGTAAGTCAGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCGTTTGAAACTACAAGGCTAGAGTGTAGCAGAGGGGGGTAGAATTCCACGTGTAGCGGTGAAATGCGTAGAGATGGGGAGGAATACCAATGGCGAAGGCAGCCCCCGGGGTTAACACTGACGCCAAGGCACGAAAGCGGGGGGGGCAAACG
+
?????BB?DDDDDD@DDCEEFFH>EEFHHHHHHGHHHCEEFFDC5EECCCCCCDECEHF;?DFDDFHDDBBDF?CFDCCFEA@@::;EEEEEEEECBA,BBE?:>AA?CA*:**0:??A:8*:*0*0**0*:?CE?DD'..0????:*:?*0?EC*'.)4.?A***00)'.00*0*08)8??8*0:CEE*0:082.4;**?AEAA?#############################################
@MISEQ03:64:000000000-A2H3D:1:1101:14943:1619 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCGACCACCTGGACTGAAACTGACACTGAGGGGCGAAAGCGGGGGGGGCAAAAG
+
?AAAABBADDDEDEDDGGGGGGIIHHHIIIIIIIHHHCCHHFFEFHHHDCDH5CFHIIHIIIIHHHHHHHHHHHHHHHHHHHGGGEGGGGDDEGEGGGGGGGGGGGGGGEEEGCCGGGGGGEGCEEEECE?ECGE.84.8CEEGGGE:CCCC0:?C<8.48CC:C??.8.8?C:*:0:*9)??CCEE**)0'''42<2C8'8..8801**0*.1*1?:?EEEC?###########################
@MISEQ03:64:000000000-A2H3D:1:1101:15764:1660 1:N:0:TCCACAGGAGT
TACGAAGGGGGCTAGCGTTGCTCGGAATCACTGGGCGTAAAGCGCACGTAGGCGGATTGTTAAGTCAGGGGTGAAATCCTGGAGCTCAACTCCAGAACTGCCTTTGATACTGGCGATCTTGAGTCCGGGAGAGGTGAGTGGAACTGCGAGTGTAGAGGTGAAATTCGTAGATATTCGCAAGAACACCAGTGGCGAAGGCGGCTCACTGGCCCGGAACTGACGCTGAGGGGCGAAAGCTGGGGGAGCAAACG
+
???????@DDDDDDBDFEEFEFHEHHHHHHHHHHHHHEHHHHFEHHHHAEFHGEHAHHHHHHHHHHHHHHH=@FEFEEFEFEDAEEEFFE=CEBCFFFCECEFEFFFCEEEFFCD>>FFFEFF*?EED;?8AEE08*A*1)?E::???;>2?*01::A?EEEFEEE?:C.8:CE?:?8EE8AECEFE?C0::8'488DE>882)*1?A*8A########################################
@MISEQ03:64:000000000-A2H3D:1:1101:15211:1752 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGGGGTGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATGGGAAGGAACACCAGGGGCGAAGGCGACCACCTGGACTGATACTGACACTGGGGTGGGAAAGGGGGGGGAGGAAAAG
+
?????<B?DBBDDDBACCEEFFHFHHHHHHHHHHHHH5>EFFFEAACEC7>E5AFEFHHHHHHF=GHFGHFHHHHFHFHH;CED8@DDDE=4@EEEEECE=CECECEECCBB34,=CAB,40:?EEEE:?AAAE8'.4'..8*:AEEECCCA::A################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:15201:1774 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTGATACTGACACTGAGGTGCGAAAGCGGGGGGGGCAAACG
+
?????BB?DDDDDDBDEEEEFFHFHHHHHHHHHHHFH>CEHDGDDCDE5CCEACFHHHHHHHHFFHHHHHHHHFHHFHHHHHHDEBFEEE@DEEEEEEEEEEEEEEBBCBECEEEEEEEEEEEEEEE?ACCEEEA)84)0.?EEE:AEACA?0?CEDD'.4?A:ACA)0'80:A:?*0*0)8CEEEEE?*0*)88888A'.5;2A)*0000*8:*0:?CEEEE?A*?A#######################
@MISEQ03:64:000000000-A2H3D:1:1101:15976:1791 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTCGTTAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATGGGAAGGAACACCGGGGGGGAGGGGGGCTCTCGGGTCCTTTTCGGCGGCTGGGGGCGGAAGGCAGGGGGGGCAACCG
+
?????BB?DDDDDDDDEEEEFFIFHHHHHHIIIHIFHCCHF@F>CECHCDDECCFEADEHHHHHHHHFGHHHHHHFHHHHHHF8:<DEEEADEEFFFFFFABEFFEFFECBCEEFEFFFFEACEEEEE*10*1??.08.888AEF?EEEC1:1:??>>'88AC?::?AA##################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:16031:1840 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCGACCACCTGGACGGATACTGACACTGAGGGGCGAAAGGGTGGGGAGAAAAAG
+
?????BB?DDDDDDDDGFEGGGIHHHHIIIIIIIHFE>CFFFFDCHCH>>CE-5EEIIHHHIHHHHHHHHHHGHFDFHFHEHGBEEEEGGEDGGGGEGGEGGGGGCEGCCEEGGG><CEECCGCEEEG?C:1?EG.8<.88CCCEEGE?C?C*:1:<>'.8?8:C:?00.0?:?*1::*9CC?EEEG*?##############################################################
@MISEQ03:64:000000000-A2H3D:1:1101:12964:1852 1:N:0:TCCACAGGAGT
TNCAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGCAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGAAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCAACCACCGGGACTGAAACTGAACCGGAGGGGGGAAAGCGGGGGGGGAAAACG
+
?#55????DDDDDDDDEEEEFFHHBHHHFFGHHFHDC+5>C/?E7DCHCCCD5AECFHHHFHHHHHHHHHFFFFFHFFDFEFF5)@=DEFDEFEEFF;AEAABC,4BECCC=B,5?C8?CC?CC*:?E010:?EA)0.)08C?A:?A########################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17245:1906 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAGGGAACACAAGGGGCGAAGGCGACCACCGGGACGGAAACTGCAACTGGGGGGGGAAAGCGGGGGGGGAAACAG
+
AAA??BB?DDDDDDDDGGEGGGIHGHIIIIIIHF?CFCCDFFFDCHEHC>DH5AFEHIHHHHHHHHHHHHHHFFFFFHHHHHGDBEEGGGGGGG@EGEGGGGGGGCGEGACC>EGEGGGGC:C0CEEG:0::CEE)88)08?:CECCE:C*10*104A.4CE:*:?C8)'8CC##############################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:18171:1983 1:N:0:TCCACAGGAGT
GACGTAGGAGGCGAGCGTTGTCCGGATTCATTGGGCGTAAAGAGCGCGCAGGCGGCTTGGTAAGTCGGATGTGAAATCCCGAGGCTCAACCTCGGGTCTGCATCCGATACTGCCCGGCTAGAGGTAGGTAGGGGAGATCGGAATTCCTGGTGTAGCGGTGAAATGCGCAGATATCAGGAGGAACACCGGGGGCGAAGGCGGATCTCTGGGCCTTCCCTGACGCTCAGGCGCGAAAGCGGGGGGGGCGAACG
+
??????B?DDDDDDDDFFEFFFIHFEEEHHIHHHFHHEHHFGFFFHCEHEHCDECCEFFE4DDFDBEEEEEFFFFEEFFCE8B>BEFEEFFCEFE>8>EFFE*A?A?ADDAAEE8E>;>EA:??1*:?111?C<88AA08?ACECF:*:?*08:0:8<.4?EE*A:))'..0*01*?:08?A*?CA#################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:14225:2009 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTGAAACGGACACTGAGGGGCGAAAGCGGGGGGGGCAAACG
+
?????BB?DDDDDDBDEEEEFFHHHHIIIIHHIIIIHHEHIFGEHHHHCCEHAEFHIIHIIIIHHHHHHHHHHFHHHHHHHHFFFEFFFFFEFFFFFFEFFFFFFEFFFEFCACEFFFFFF:C?CEEE*?:AAEE88;088?AEFCEAEECEEEFE>?).?ECCEEE8?4AFFE0?*0088ACFFFAAC*0?C888>>CD?D;8CE*:*:A?CF*::)0?DD?:::?########################
@MISEQ03:64:000000000-A2H3D:1:1101:16656:2052 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCGACCACCGGGACTGAAACTGACACTGAGGGGGGAAAGCGGGGGGGGAAAACA
+
?????BB?BDDDDDDDGFFEGGIIHHIIIIIHHHHIHCCFFDEEEHEHFFEH5AFHHIHIHIHGGHHHHHHHFHHFHHHHHHGEG@EGEGGEGGGGCEGGEGGGGEGGACECGGGGGGGGEGGCCEGG?CCCEGC088)0.?EGG?EC*::C*:??<8.48?C:?C808.8CEE#############################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:18209:2060 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGTAGGCGGCTCAGCAAGTCAGGGGTGAAATCCCGGGGCTCAACCCCGGAACTGCCCTTGAAACTGCTAAGCTAGAATCTTGGAGAGGCGAGTGGAATTCCGAGTGTAGAGGGGAAATTCGTAGATATTCGGAAGAACACCAGGGGCGAAGGCGACCCCCTGGACAAGCATTGACGCTGAGGGGGGAAAGCGGGGGGGGCAAAAG
+
?????BB?BDDDDDDDECEEFFHHHHAHFHHHHHHHHCCHHH=@DEEHFHFCGHHB)?ECGHHH?DHHHHHCCCFFHHHFEEEEEEEEEEEEEB)>EDACEECEECEEECEE:*0A:AEAECA:0::ACE??E?.8'4.88?EC*00:08).0:*00?)..8AAAAA*0)0::?::?0A8)?C:?A#################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:13824:2095 1:N:0:TCCACAGGAGT
TACGTAGGGGGCTAGCGTTGTCCGGAATCATTGGGCGTAAAGCGCGTGTAGGCGGCCCGGTAAGTCCGCTGTGAAAGTCGGGGGCTCAACCCTCGAAAGCCGGGGGATACTGTCGGGCTAGAGTACGGAAGAGGCGAGTGGAATTCCTGGTGTAGCGGTGAAATGCGCAGATATCAGGAGGAACACCCATTGCGAAGGCAGCTCGCTGGGACGTTACTGAGGCTGAGACCGGAAAGGGGGGGGGGCAAAAG
+
??A??BBADDDDDDBDFEEFFFHHHHHFHHHIHHFHHCCHHFHDCCDEEHHFIHAHHHHH@EFFDFFEBDEDEFFECBBEEEED?28CCFFECE;EF8?ECD;'488?EEFCE:A>>?>EECEE::A8E8.8?8).'.'08AEE*?:*::*001:?<D.'8??*:*))'''01***10*088CEEEEA8C#############################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17839:2106 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACAACCGGGACGGAAACTGACACTGAGGGGCGAAAGCGGGGGGGGCAAAAG
+
AAA?ABB?DDDDDDDEGFEGGFHIHHIIIIIIIIDFH5CFHHGHEH=DC>CE5AEEHFHIHIFHHHHHHHHHFHHFHHHHHHGGGGGEEGGGGGDEGGGGGGGGGGGGGCE>AEGEGGGGEEECEGEE1:??CEC08>.88CEEECG*:C?CC:?0.4.4CE?CECC?)4?CC:*11?:?)CCEGG).9*1:?8<2<<C####################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17831:2124 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGGGGGGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTGAAACTGACACTGAGGGGCGAAAGCGGGGGGAGCAAACG
+
AAAAABB?DDDDDDDDGFGFGGIIHHIIIIIHIIDFH>CFHHGDCFDH>CDHAEFEHIEFFGGHHHHHHHFH=CFFHHHHEHG8DEEGEGGGGGDEEEEGEEGGGCGGEEECCACCEGGGCEE::?CE0?CCEGE'.<'..4CEGEGGEEEE*::C>20>?C?*1:C..'8:??*:*?*0)??9CEG8?*1*8'4.44?58<28?C#############################################
@MISEQ03:64:000000000-A2H3D:1:1101:12555:2129 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTCGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACGAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACGGAAACTGACACTGAGGTGCGAAAGCGTGGGGACCAACCG
+
????ABBADDDDDEDDGGGGGGIIHHIIIIIHIIHHHFFHHHFHHHHH>CDHAEFHFGHHFHHHHHHHHHFHHFHFFHHHHHGBEEAD;DGGGGEGGGCGCEEEGEGGGCE>>>CEDGDGE:C:CGGG:?C??EE08<)0?ECEGEGCCECEEGGGGG08CECE?CE8)4?CC:*:*:0989*9CEC8C*:?C'842.8'.4.2?E9?*:?'.8).::::?CC:*110*0C8C<8??C#############
@MISEQ03:64:000000000-A2H3D:1:1101:13627:2170 1:N:0:TCCACAGGAGT
GACAGAGGGTGCAAACGTTGTTCGGAATTACTGGGCATAAAGAGCACGTAGGTGGTCTGCTAAGTCACGTGTGAAATCCCCCGGCTCAACCGGGGAATTGCGCGTGATACTGGCCGGCTCGAGGTGGGTAGGGGGGAGCGGAACTCCAGGGGGAGCGGGGAAATGCGTAGATATCTGGAGGAACACCGGGGGCGAAAGCGGCTCACGGGACCCAATCTGACACTGAGGGGCGAAAGCTAGGGTGGCAAACG
+
?????BB?DDDDDDDDEFFFFFHHHHHIHIIHIIFHCEHIIHBFHIHHAAFH5CF@FHHHGHIIGHHHHFHIHIIIHIIIHHHHHHHHHHFHHHFFEFEFEDBE<>BBEEFECECE?D'..2AD)8A>40?AED''''.4<D>>AC**1?).2'888D'5<EACEEEAEDEFEE:*??*08A?AAC)58'4>2<>D8A:A82'.*:*.'?>E)AA####################################
@MISEQ03:64:000000000-A2H3D:1:1101:11781:2223 1:N:0:TCCACAGGAGT
TACGTAGGGCGCAAGCGTTATCCGGAATTATTGGGCGTAAAGAGCTCGTAGGCGGTTTGTCGCGTCTGCCGTGAAAGTCCGGGGCTCAACTCCGGATCTGCGGTGGGTACGGGCAGACTAGAGTGATGTAGGGGAGATTGGAATTCCTGGTGTAGCGGGGAAATGCGCAGATATCAGGAGGAACACCGATGGCGAAGGCAGGTCTCTGGGCATTAACTGACGCTGAGGAGCGAAAGCAGGGGGGGCGAACG
+
???A?BB?DDDDDDDDEEECFFHHHHHIHHHIIIHHHECEHFCFHGGH>CFEFEHHHHHFFDFHCDEFFHHEBFFFF?BBEEEEEEEFFFBEEEEAEDEFEDD.8A8.ACEDDD;AEFFFFEF:*1:?ACCFFD8<AE?EFFFF:EEEEFFFA:CEDD'.8??CEF?ADDDFF:C:?::?AEEFFFA>8'08:2448DE?E?8:*:*1A***0*:AA*?AEEEEE?#########################
@MISEQ03:64:000000000-A2H3D:1:1101:17996:2254 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCGACCACCGGGCCTGAAACTGACACTGAGGGGGGAAAGCGGGGGGGGAAAACG
+
?????BB?DDDDDDDDGGGGGGIHHHHIIIIHHHFFH>CHFHGHHHEHCCCE5AFEHIHHHHHHHHHHHHHHHHHHHHHHHHGGEEGGEGEGGGEGEGGGCGGGGGGGECGEECGAECGGEEEC**CE?C::CCC.8<)08?CCC:CCCEC?CC?:8>'4<?.1C:8082CCGG*:*:0C8?EC*0C89.?############################################################
@MISEQ03:64:000000000-A2H3D:1:1101:13712:2276 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTGATACTGACACTGAGGGGGGAAAGCGGGGGGGGAAAACG
+
?????BBADDDDDDDDGGEGGGIHHHHIIIIIIIIIHCCHHDCECHEHCDEH-AFEHIHIHHIHHHHHHHHHHHFFFHHHHHGEGEDDEEDDDGGGGGEGGGGGEEEGEEGEGGGGGGGCEGEGCEGG:C::CEE)88.8?EGGG:C?:?:C??:*52'.888:CEE).2CCGE*C??:C.?EGGGGC9*118>>.4>C''.8<CC*?*:**00*01?:CEGCC###########################
@MISEQ03:64:000000000-A2H3D:1:1101:15819:2301 1:N:0:TCCACAGGAGT
TACGTAGGGTGCGAGCGTTAATCGGAATTACTGGGCGTAAAGCGTGCGCAGGCGGTGAGTTAAGTCTGCTGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGGGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCGACCACCTGGACTGAAACTGACACTGAGGGGCGAAAGCGGGGGGGGCAAACG
+
?????BB?DEDDDDDDFDEEFFHHHEFHHIIIIIIHHCHHFHHHCEEACCHHHEH)<<CCDGFFDFFFBCB@DFHFHFHHEEFB8@EEEFFEEFFFFFFFFFEFCEFFFCAAC?EF??AC???0*:?C*:::?EE)0>'.42AAECEFE:*0:AAC?D'..8C?:?A)).0001*11::??8A**?A################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:11958:2304 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAAGCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGGGGAATTTCCTGTGTAGCGGGGAAATGCGTAGATATAGGAAGGAACACCAGGGGCGAAGGCGACCACCGGGACTGAAACTGACACTGAGGGGCGAAAGCGTGGGGGGCAAACG
+
????ABBADDDDDDDDEEEEFFHHHHHIFHHIIIHFEECEFGDECECE5>C:55EEHIHIFGHFGHHHHHFHFFHHFHHHHHFBFEEDEEFFFFEFFFEFEFABEEFFFEEBEFFEFF=::AE*:AEE0?:?CFE8A>'.<?EEE??E?A??CEEF<>'.8AC?ECE)848?0**::AAC???EEE)*0)084'48<'8'882<CA).2<408?*1:??EEE#############################
@MISEQ03:64:000000000-A2H3D:1:1101:19110:2311 1:N:0:TCCACAGGAGT
TACAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGGGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTAAAACTGACACTGAGGGGCGAAAGCGGGGGGGGCAAACG
+
????9BB?BBBBBBBBEEECFAFHHHHHHHFHHHHHHCCEFF/CDCCE>DCH5AECFHHHFHHHHHHHHHHHGFHHCFHHHHHEEEDEDEED@EEEEEEEEEEEEEEEEE;;BEEE?EEEEEE?*?CA?EE::?8'.''..?CEE*::/:?A:C?E??82?CCEEEE))4?EEEEA:?*80?AEEC#################################################################
""" 

reads2_string = """@MISEQ03:64:000000000-A2H3D:1:1101:14358:1530 2:N:0:TCCACAGGAGT
ACGGACTACAAGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTGAGCCCGGGGATTTCACATCCAACTTAACAACCCACATACCCGCCTTTTCGCCCAGGTAATCC
+
?????@@BDDBDDDBBCFFCFFHIIIIIIIIFGHHHHEHHHIIIHHHHHFHIIHIGHHIDGGHHHHIIIIICEFHIHHCDEHHHHHHFHHCFHDF?FHHFHHHFFDFFFDEDDD..=DDDE@<BFEEFCFFCECE==CACFE?*0:*CCAA?:*:*:0*A?A80:???A?*00:**0*1*:C??C?A?01*0?);>>'.8::A?###############################################
@MISEQ03:64:000000000-A2H3D:1:1101:14206:1564 2:N:0:TCCACAGGAGT
ACGGACTACAGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGTGCATGAGCGTCAGTGTTAACCCAGGGGGCTGCCTTCGCCATTGGTATTCCTCCACATCTCTACGCATTTCACTGCTACACGTGGAATTCTACCCCCCTCTGCTACACTCTAGCCTTGTAGTTTCAAACGCAGTTCCCAGGTTGAGCCCGGGGCTTTCACATCTGCCTTACAAAACCGCCTGCGCACGCTTTACGCCCCGTAATTC
+
?????@@BDDBDDD?@CFFFFFHHHHHFFHHHHHHHHHHH@FFHEDFFH@FHBGCDHHHBFHHHHHHHEHHHHDCCEFFDFFFEE:=?FF?DFDFDFFF==BEE=DBDDEEEEEB,4??EE@EEE,3,3*3,?:?*0ACCEDD88:***?*0:*0***0*?C?00:AE:?EE:*A8'.?:CAA?A80*0*??AA88;28;C##################################################
@MISEQ03:64:000000000-A2H3D:1:1101:14943:1619 2:N:0:TCCACAGGAGT
ACGGACTACAGGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCAAGGTTGAGCCCGGGGCTTTCACATCCAACTTACAAAACCACCTACCCGACCTTTACGCCCAGAAATTC
+
?????@@BDDDDDD?AFFFFFFIIHHIHIIHIIIIHIHHHHHHHHHHHHHHHHHHIHHHIIHHIHIIIIII?EFEGHHHHHIIHHDHHFD@FFEHFHFHFHFHFFFFFFFFEEEEFFFDEB<E@EFEEABA=B=CAEFEEFEA?A:*AC::??:**10??:00::*??EC*?:?C*::A*?C*1:8A################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:15764:1660 2:N:0:TCCACAGGAGT
ACGGACTACCGGGGTATCTAATCCTGTTTGCTCCCCTAGCTTTCGCACCTCAGCGTCAGTACCGGGCCAGTGAGCCGCCTTCGCCACTGGTGTTCTTGCGAATATCTACGAATTTCACCTCTACACTCGCAGTTCCACTCACCTCTCCCGGACTCAAGACCGCCAGTACCAAAGGCAGTTCTGGAGTTGAGCTCCAGGTTTTCACCCCTGCTTTAAAAATCCCCCAACGCGGCCTTTCCCCCCAGTGACTC
+
?????@=BB?BBBB<?>ACFFCECFCHCFHH=CGHHDFH=E?ACDEHHCCFFGHHDHH@CBEFHHCHHHF,5@?DF)4<C3D4DD+=,BD5;DE=DBDE=<E<;?E?B;3?;A?;;;EBBC:??EEEEE?;AA*:A??#################################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:15211:1752 2:N:0:TCCACAGGAGT
ACGGACTACCGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTGAGCCCGGGGATTTCCCATACAACTTAACAAACCACTTACGCGGGTTTTCGCCCCACAAATTC
+
?????@@BB-<@BBBBEA?FFFA8ACFCBHHHGHHHHBHHHHFCDDD7CHHFE?CCDDCFGBHHHGGHFGFGFFHFDCDHHC?=CDHFFDCDDDF,EFF5?BFEDBBDB@@EEACCE;,?::@BEEEEACC*??//:AA*8AAAEE?ECC#####################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:15201:1774 2:N:0:TCCACAGGAGT
ACGGACTACCGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTAAGCCCGGGGATTTCCAATCCAACTAAACAAAACACACACCCGCTCTTTACGCCCACCATTTC
+
?????@=BBBBBBB<=CFFFFFFHFCFCEHHDGHHEFEHHHHHHHHHHHFHHGC-AEGFCGHHHFFHFHHBFGDEDDCEDDH+DDDHHF,,7D@DFDFFFBFFEDEDEEDE:@:B?C;,3@<><EEEE*BEEC?E*0AEEEEE*8*:CCE:CA*?*A?:AAA#########################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:15976:1791 2:N:0:TCCACAGGAGT
ACGGACTACAAGGGTTTCTAATCCCGTTTGCTCCCCTAGCTTTCGCACCTCAGCGTCAGAAATGGACCAGAGAGCCGCCTTCGCCACCGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTGAGCCCGGGGTTTTCCAATCCAATTTAACGACCAACCACGCGGCGCTTTAGGCCCGGTAATGC
+
?<???@=BBBBBBB556CFFBCEFFEHHHHHHHHHE=EHHHHHHHHHHHHHHHFHHEDCGFHHHHHHHHH;A?EFHHHHHHHHH+=EHHC)8@+?BFFFDFEEEEE;DDEEEEBCEECEEEBEEEEEEEEEEE:?*/:ACEE)*8*:C:A*0?:A*:C?A:?**:AECE?*?:*:C:????C#####################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:16031:1840 2:N:0:TCCACAGGAGT
ACGGACTACTGGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTTAACAATACTCTAGCTTGTCAGTTTTAAATGCAGTCCCCAGGTTGAGCCCGGGGCTTTCACATCAAATTTACAAAACCACCCACGCGCGTTCTACGCCGGACAATCC
+
?????==<BBBBBBBBFFFFF?FFF?FFFHHFEFFHHHH:@>CHEDHHHFFFGBCCDDFGGHHHHEHHHHH5AE+C*>==+EDHHDEFCFCDF3@.D=,CFH=,@,4DFFE:=DDDDEB:)1:1;;?B;BE;??,?EE;AEE??**0*/:0??:***:?E*:8?A*:CEE#################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:12964:1852 2:N:0:TCCACAGGAGT
ACGGACTACTCGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCAACCACCCTCTACCATACTCTAGCTTGTAAGTTTTGAATGCAGTTCCAAGGTTGAGCCCGGGGCTTTCACACCCAACTTAACAACCCACCTACGCGGCATTTACGCCCACTACTTC
+
?????@=BBBB9?=55AACCC?ECFFFHB>FFHGFHFHHHHHHHHHHHHFHHHGGGHHHGGHHHHHHDDFEGH;EBCEHD+AFE@C+@F=.7D+@CDCFFHHFFFD?DF@E+=:BDDB;D=@BE?BCE*,33,,?,3;;:?).0**::***0/*/0A??:*:****00/**8*0?AE:?AAC**0):??C#############################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17245:1906 2:N:0:TCCACAGGAGT
ACGGACTACAGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTGAGCCCGGGGCTTTCAAATCCAACTTAACAAACAACCAACCGGCGCTTTACGCCCAGTAATTC
+
?????@@BDDDDBDABEFFFFFHHHHHHHHGGHGHHHHHHEH@FEHEEHHHFHHH=EGHHHHDGHHHHFHHGGHHHCCEDEHHHHHHHHHDFHHF=DBDFHFD?BB.BF;@DDDD.=DD*>6)@==ABAACBB5=B,=,88A)???:E*::::??*:**1**8??CCCEE8A:A::AAACAC??A)1:0**1*)48;'42A?EA**1?*1*0::??:ACEF##############################
@MISEQ03:64:000000000-A2H3D:1:1101:18171:1983 2:N:0:TCCACAGGAGT
ACGGACTACCGGGGTTTCTAATCCTGTTCGCTCCCCACGCTTTCGCGCCTGAGCGTCAGGTAAGGCCCAGAGATCCGCCTTCGCCACCGGTGTTCCTCCTGATATCTGCGCATTTCACCGCTACACCAGGAATTCCGATCTCCCCTACATACCTCTAGCCGGGCAGTATCGGATGCAGACCCGAGGTTGAGCCCCGGGATTTCACATCGGCTTACCAAAGCGCCCGGCGCCCCCTTTACGCCCCAGAAACC
+
?????@@BDBDDDD=BCFFFFFIIIIHHFEHHHHIHIHHHEFCGDEHHHEFFEGC>EEHI?EHHGHHHHFH+C=,,?FHDDHFEE@EFE=1;A;EECCE==BEB,BBC=@@<?EE:?E:8>24;:CEAA8?CC*??:0?;*1?AE?CE*10:0*1:CAA*;22;2A#####################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:14225:2009 2:N:0:TCCACAGGAGT
ACGGACTACAGGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTGAGCCCGGGGCTTTCACATCCAACTTAACAAACAACCACGCCGCGCTTTAGCCCAGGTAATTC
+
?????@@BDDDDDD??CFFFFFHIHHHHIIIIHIIHIHHHHHIHHHHHHFFHHIHHHIHHHHHIIHIHIIIFFFEGHHEDEHHHHDHHHHCFFDFFHHHHHHFFFFFFF@EDEED=DDEED@EBFCEEEFECCCEEEFB<CA888:AEEFEFEA??CCEFF:?:ACCFFE?E:AC?:*:?EFE*:):???::A).;D>D>8:?################################################
@MISEQ03:64:000000000-A2H3D:1:1101:16656:2052 2:N:0:TCCACAGGAGT
ACGGACTACCCGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCCCCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCAAGGTTGAGCCCGGGGCTTTCACACCCAACTTAACAAACCACCTACGCGCGCTTTACGCCCAGCATTTC
+
?????@@BDDDDDD<@CFFFFFIHHFHHFHHHHHHHIHHHHHFHCEHHHHIIFHHAFHHHFFHIIHHIIIHGHFEH<DDEDH;DEHHHHHFFH;FFHFHFFFFD?FBFF=BDEDDDFEEAE@BEFFFF<BE=B,=,5?*).;>8A:*:::?E?*::A::?AE8AEFEEEC?A:CE?AEA:EF*008:?EF*:C)8;D228A0:??:*.8A8):*:*1::CE##############################
@MISEQ03:64:000000000-A2H3D:1:1101:18209:2060 2:N:0:TCCACAGGAGT
ACGGACTACTAGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGCGTCAATACTTGTCCAGCGAGTCCCCTTCGCCACTGGTGTTCTTCGGAATATCTACGAATTTCACCTCTACACCCGGAATTCCACTCCCCCTTCCAAGATTCCAGCTTAGCAGTTTCAAGGGCAGTTCCGGGGTTGGCACCCGGGATTTCACCCCTGCCTTGCTCAACCCCCCACGGGGCCTTTACCCCCAGCATTCC
+
=9<=9<7<@@@@@@<@A8A>C>8E>-8AE;C99CEEECC>>EECE@CCDE,C@E++5>E-A=E-C@@=@5@C>C<D-5A5CC<CD+<4DE3=<C+4==+<@D++2:9DEE1<9DE########################################################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:13824:2095 2:N:0:TCCACAGGAGT
ACGGACTACCAGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCGTCTCAGCGTCAGTAACGTCCCAGCGAGCTGCCTTCGCAATGGGTGTTCCTCCTGATATCTGCGCATTTCACCGCTACACCAGGAATTCCACTCCCCCCTTCCGTACCCTAGCCCGACAGTACCCCCCGGCTTCCGAGGCTTGACCCCCCGCCTTTCACACCGGACTTACCGGGCCGCCTACCCGGCCTTTCGCCCCACCGTTTC
+
??<??@@BBBBBBBBBCFCFFFHHHHHHBHHGHHHHHCHHEH>GDEHCA:DFGHHEEEEFFHHHHHHDHED7<CHEGHFFDFFHEDHHHDDDE@D??DD;=B,,5B,,56)):?;BEE?*1::):?**8AEAC*?*:?#################################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17839:2106 2:N:0:TCCACAGGAGT
ACGGACTACAAGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGAAGTTCCAAGTTTGAGCCCGGGGCTTTCACATCCAATTTAAAAAACAACCAACGCGCGCTTCACCCCAGGTAATAC
+
?????@@BBBBBBB<5ACFFFFHHHHHHHHHHHHHHHHHHHHFFHHHHHHHHHGHHHFHGHHHHFGHHHHH?EFEECCEEEHHHEHHHHHDFHDFDHDHHHHFFDFFFHFEDDDD,5DD@BB<EEEEECBB?B3B;,?,3?E8CE?*?A*/:/:::??AE::**0:AEE##################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17831:2124 2:N:0:TCCACAGGAGT
ACGGACTACAAGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTCGAATGCAGTTCCCAGGTTGAGCCCGGGCCTTCAACCTCCACTTTACAAAACAACCAAACGCCGCTTACCGCCACGAAATCC
+
?????@=BBBBBBB5<CFFFFCFHHHHHFHHHHHHHHHHHHHFHEEHHEHFGHGHFGDF?EEFHHHHDGHH=EHEGCCEEEHHHHHH@FFCFH+CFHCFHHHHHFFFHHFE:DDD,=EBDEBE<EEEE?;B?B?E?CEEEEEE8A?CC#######################################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:12555:2129 2:N:0:TCCACAGGAGT
ACGGACTACCGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCCCGTCAGTTTTGAATGCATTTCCCAGGTTGAGCCCGGGGCTTTCAAACCCAACTAAACAAACAACCAACGCGCGTTTTCCGCCACGTAATTC
+
?????@@BDDDDDDDDEFFFFFHHHFHIIIHHHIIHHHHHEHFHEHHHHIFGHHIHIHFHI=FHFIHIIIHDFHHHHEHEDHHHHHHHHHHHH@FBFFFFFFFEFDEFE6@:@ACBEFFEEB@BCB=A<<A?C:A::C8AEE)0?A*?A:*:**10?1**1.4A88?EE?#################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:13627:2170 2:N:0:TCCACAGGAGT
ACGGACTACTAGGGTATCTAATCCCGTTTGCTACCCTAGCTTTCGCACCTCAGTGTCAGATTGGGTCCAGTGAGCCGCTTTCGCCACCGGTGTTCCTCCAGATATCTACGCATTTCACCGCTCCACCTGGAGTTCCGCTCACCCCTACCCACCTCGAGCCGGCCAGTATCCCGCGCAATTCCCCGTTTGAGCCGGGGGTTTTCCCAAGGGTCTTAACAGCCCACCTACGTCCCCTTTATGCCAGGTAATTC
+
?????@=BD?BBDD?58ACFFCHHHHHHHHFGHHHEEFHHHHHCDEEEECFDGFHDGHHHHFFFHEHHHHHHHFFFHAEHFFEHHHHFHH<DE:C--@F-CCF=,,4BDFE:@E,BBED@:)2>=C?;BC=?C,==*3.84?EC?88A8A:A?*8?###############################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:11781:2223 2:N:0:TCCACAGGAGT
ACGGACTACTGGGGTATCTAATCCTGTTCGCTCCCCATGCTTTCGCTCCTCAGCGTCAGTTAATGCCCAGAGACCTGCCTTCGCCATCGGTGTTCCTCCTGATATCTGCGCATTTCACCGCTACACCAGGAATTCCAATCTCCCCTACATCACTCTAGTCTGCCCGTACCCACCGCAGATCCGGAGTTGAGCCCCGGACTTTCACGGCAGACGCGCAAACCGCCCACAGAGCTCTTTCCCCCCAAAAATCC
+
?????@@BDDDDDDBDCFFFFFHHHHHHHHHHHEHEHDFHHHHHHEDEEHHHFHHHHEHHHHHFGHHHHDD;EFFHCFECAGFEEE+@E@3?E:DFFFHBDHC?BBDFFE8;=DD,,=DEE<@),==?B*44=,=,4**0*0:CA*A?::*0::?0AC:CE*?:*8.4AE?*8?)'82;*?0?####################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:17996:2254 2:N:0:TCCACAGGAGT
ACGGACTACCAGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTGGAGCCCGGGGCTTTACAATCAAACTTAACAAACCCCCTACGCGCGCTTTAGCCCCACAATTTC
+
?9???@@BBDDDDD<BEFFFFFHHHHCEFHGGHHHHHAEHEHFHEEHHCBFHFFHEGHFCGGFCGHHFHHFGHHHHDHHECEDEHDDHH?@?FDFDHHHFHFFDDHDFFFEEEEEDEDB=>BBEE=BECEEEE,B=?CBACE)*0**?C?*:*0:*:?:A:??**::?E**80::::??:CAC:C8C################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:13712:2276 2:N:0:TCCACAGGAGT
ACGGACTACTGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGAAGTTCCAAGGTTAAGCCGGGGGCTTTCACATCCAACTAACCAAACCACTAACCGCCGCTTTAGGCCCAGCAATTC
+
?????@@BDDDDDDBDEFFFFFHFHHHIFFHIHIIHHEHHHHFHHHEHCFHHDFGGHIIHIHFGHHHGFHF-AEEGHHHHEGFHHHDFHB?FHEHCF?FDDFH??BFFFF=DDEEEFFEDE8>:BECCAEEAECE,ABAACEA*0**?*01?001*::*A**0:*::CE1*8:?**11:*CE#####################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:15819:2301 2:N:0:TCCACAGGAGT
ACGGACTACCGGGGTTTCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGAAGTTCCCAGGTTGACCCCGGGGCTTTCACAGCAGCCTTAACTCACCCCCTGCCAACCCTTTACTCCCCGAAATTC
+
?9???@=BDDDDDD<@CFFFFFHHHBFFHHHFGHHHHHHHEHFGEHHHHEDGD?FCGHHFHHHHHHHHBDF?FHHHFHH@DHHHH+DHHDCFHDFDFBFFDFFEDFEEDEEDEEC=CCEEEBEEFCEFEEFEE?:CEE*8CA800*:E*:AA::***1??*:**1::CF##################################################################################
@MISEQ03:64:000000000-A2H3D:1:1101:11958:2304 2:N:0:TCCACAGGAGT
ACGGACTACTGGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGTGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTGAGCCCGGGCCTTTAAAATCCAACTTAAAAAACAACTAACCGCCGCTTTCCGCCCAGAAATCC
+
?????@@BDBDDD@@BFFFFFFHFHHHHFHHHHHHHHHHHHHHHHHHHHHFHHHHHFGH=CGEH=FHFGHFEFHEHHCEEEHHHDCEFHH.?FDFFHHHHBFHFFHFFFFEEEEEEEEEEB@EEEECE;CC?BCEEEC;;CEA*8:AE**00::C0A::?:*0*AEE?E?*A**:C?*:?:?**0)00::**?8>'8';ACA*0*0C?:?******::??E?CE###########################
@MISEQ03:64:000000000-A2H3D:1:1101:19110:2311 2:N:0:TCCACAGGAGT
ACGGACTACCAGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTCAGTGTCAGTATCAGTCCAGGGGGTCGCCTTCGCCACTGGTGTTCCTTCCTATATCTACGCATTTCACCGCTACACAGGAAATTCCACCACCCTCTACCATACTCTAGCTTGTCAGTTTTGAATGCAGTTCCCAGGTTAAGCCCGGGGCTTTCCAACCCAACTTAACAAACCACCTACCCCCGCTTTACGCCCAGAAATTC
+
?????@=BDDDDDD<5CFFFFFHHHHHF>CGFHHHHHHHEEHFHEHHHHHHHGAFGHHHHH-5AF5AFHHD+5*5CCCDDHFFHEEHFHHBFF:BDD4?=.=DEFFEBEDEBEEECEFFEE<::CEAACE?:A*1:*C88?AE.?:*::**1:**11*01***1?C??:?0?:C:C**1*1::*:8A?10*1?##########################################################
"""

if __name__ == '__main__':
    main()