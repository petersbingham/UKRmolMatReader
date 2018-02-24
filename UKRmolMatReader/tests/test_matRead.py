import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import UKRmolMatReader as matRead

import unittest

class test_water_mats(unittest.TestCase):
    def runTest(self):
        matRead.nw.mode = matRead.nw.mode_norm
        mr = matRead.RfortMatReader("water_inel_B1_10ch.19")
        kmats = mr.readkMats()
        #self.assertEqual(oChanDesc[0],[4,1024])
        #self.assertEqual(oChanDesc[1],[10,1799])
        expectMat = matRead.nw.matrix(\
          [[-0.44319103+0.j,  0.17810525+0.j,  0.00342772+0.j, -0.03147134+0.j],
           [ 0.17810525+0.j, -0.00818044+0.j,  0.09482788+0.j, -0.00245007+0.j],
           [ 0.00342772+0.j,  0.09482788+0.j, -0.03620601+0.j,  0.01289757+0.j],
           [-0.03147134+0.j, -0.00245007+0.j,  0.01289757+0.j, -0.00201263+0.j]])
        print kmats[sorted(kmats.keys())[0]]
        self.assertTrue(matRead.nw.np.allclose(kmats[sorted(kmats.keys())[0]],expectMat))
        
if __name__ == "__main__":
    #Just for debug
    b = test_water_mats()
    b.runTest()
