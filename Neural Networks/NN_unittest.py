from unittest import TestCase
from neuralNetwork import NNet
from neuralNetwork import splitExamples

class Dualtest(TestCase):
    
    def test_basic(self):
        """Tests 4 points in a square, no test of margin breaking points
        """
        examples = [[2.0,2.0,1.0],[2.0,-2.0,1.0],[-2.0,2.0,-1.0],[-2.0,-2.0,-1.0]]
    
        c = [(100/873),(500/873),(700/873)]
        nNet = NNet(examples,100,0.1,2)

        count = 0
        total = 0
        split = splitExamples(examples)
        for i in range(len(split)):
            x = split[0][i]
            y = split[1][i]
            pred = nNet.prediction(x)
            if y * pred >= 0.0:
                count +=1
            else:
                
                self.fail()
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
    def test_marginBreakers(self):
        """Tests 4 points in a square, all points are within 1 unit
        """
        examples = [[0.5,0.5,1],[0.5,-0.5,1],[-0.5,0.5,-1],[-0.5,-0.5,-1]]
    
        c = [(100/873),(500/873),(700/873)]
        nNet = NNet(examples,10,0.1,2)

        count = 0
        total = 0
        split = splitExamples(examples)
        for i in range(len(split)):
            x = split[0][i]
            y = split[1][i]
            pred = nNet.prediction(x)
            if y * pred >= 0.0:
                count +=1
            else:
               
                self.fail()
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
    def test_closedata(self):
        """Tests points that are barely seperated
        """
        examples = [[1,1,1],[1,-1,1],[-1,1,-1],[-1,-1,-1], [0,1,-1]]
        message = ""
        c = [(100/873),(500/873),(700/873)]
        nNet = NNet(examples,10,0.1,2)

        count = 0
        total = 0
        split = splitExamples(examples)
        for i in range(len(split)):
            x = split[0][i]
            y = split[1][i]
            pred = nNet.prediction(x)
            if y * pred >= 0.0:
                count +=1
            
                 #+ "\n"
                #self.fail(message)
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        if(count != total):
            self.fail()
        self.assertTrue(count == total)
        
        
    def test_dataset(self):
        """tests that the prediction accounts for bias
        """
        examples = [[6.8248, 5.2187, -2.5425, 0.5461, -1], [-0.74324, -0.32902, -0.42785, 0.23317, 1.0], [-1.6637, 3.2881, -2.2701, -2.2224, 1.0], [-1.4174, -2.2535, 1.518, 0.61981, 1.0], [-0.071503, 3.7412, -4.5415, -4.2526, 1.0], [5.1129, -0.49871, 0.62863, 1.1189, -1], [-2.9138, -9.4711, 9.7668, -0.60216, 1.0], [-1.0112, 2.9984, -1.1664, -1.6185, 1.0], [2.9421, 7.4101, -0.97709, -0.88406, -1], [4.3848, -3.0729, 3.0423, 1.2741, -1]]
        
        c = [(100/873),(500/873),(700/873)]
        nNet = NNet(examples,10,0.1,2)

        count = 0
        total = 0
        split = splitExamples(examples)
        for i in range(len(split)):
            x = split[0][i]
            y = split[1][i]
            pred = nNet.prediction(x)
            if y * pred >= 0.0:
                count +=1
            else:
           
                self.fail()
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
    def test_almost(self):
        "test for a non linearly seperable "
        examples = [[-1,0,1],[3,0,1],[4,0,1],[5,0,1],[7,0,1],[1,0,-1],[-3,0,-1]]
        
        c = [(100/873),(500/873),(700/873)]
        nNet = NNet(examples,10,0.1,2)

        count = 0
        total = 0
        misses = []
        split = splitExamples(examples)
        for i in range(len(split)):
            x = split[0][i]
            y = split[1][i]
            pred = nNet.prediction(x)
            if y * pred >= 0.0:
                count +=1
            else:
                misses.append(example)
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count >= total - 2)
        
    def test_bais(self):
        """tests that the prediction accounts for bias
        """
        examples = [[1,2,1],[3,0,1],[2,3,-1],[2,4,-1]]
        
        c = [(100/873),(500/873),(700/873)]
        nNet = NNet(examples,10,0.1,2)

        count = 0
        total = 0
        split = splitExamples(examples)
        for i in range(len(split)):
            x = split[0][i]
            y = split[1][i]
            pred = nNet.prediction(x)
            if y * pred >= 0.0:
                count +=1
            else:
            
                self.fail()
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)