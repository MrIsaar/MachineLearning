from unittest import TestCase
from svm import svm
class TryTesting(TestCase):

    def test_basic(self):
        """Tests 4 points in a square, no test of margin breaking points
        """
        examples = [[2,2,1],[2,-2,1],[-2,2,-1],[-2,-2,-1]]
    
        c = [(100/873),(500/873),(700/873)]
        Svm = svm(examples,10,0.1,2,c[0],"sgd")

        count = 0
        total = 0
        for example in examples:
            pred = Svm.prediction(example)
            if example[-1:][0] * pred >= 0:
                count +=1
            else:
                message = "pred:" + str(pred) + " sample: " + str(example) + "weight:" + str(Svm.w)
                self.fail(message)
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
    def test_marginBreakers(self):
        """Tests 4 points in a square, all points are within 1 unit
        """
        examples = [[0.5,0.5,1],[0.5,-0.5,1],[-0.5,0.5,-1],[-0.5,-0.5,-1]]
    
        c = [(100/873),(500/873),(700/873)]
        Svm = svm(examples,10,0.1,2,c[0],"sgd")

        count = 0
        total = 0
        for example in examples:
            pred = Svm.prediction(example)
            if example[-1:][0] * pred >= 0:
                count +=1
            else:
                message = "pred:" + str(pred) + " sample: " + str(example) + "weight:" + str(Svm.w)
                self.fail(message)
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
    def test_closedata(self):
        """Tests points that are barely seperated
        """
        examples = [[1,1,1],[1,-1,1],[-1,1,-1],[-1,-1,-1], [0,1,-1]]
    
        c = [(100/873),(500/873),(700/873)]
        Svm = svm(examples,10,0.1,2,c[0],"sgd")

        count = 0
        total = 0
        for example in examples:
            pred = Svm.prediction(example)
            if example[-1:][0] * pred >= 0:
                count +=1
            else:
                message = "pred:" + str(pred) + " sample: " + str(example) + "weight:" + str(Svm.w)
                self.fail(message)
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
        
    def test_bais(self):
        """tests that the prediction accounts for bias
        """
        examples = [[1,2,1],[0,3,1],[2,3,-1],[2,4,-1]]
        
        c = [(100/873),(500/873),(700/873)]
        Svm = svm(examples,10,0.1,2,c[0],"sgd")

        count = 0
        total = 0
        for example in examples:
            pred = Svm.prediction(example)
            if example[-1:][0] * pred >= 0:
                count +=1
            else:
                message = "pred:" + str(pred) + " label: " + str(example[-1:][0]) + " bias: " + str(Svm.bias)
                self.fail(message)
            total +=1
    #print("correct spliting: ",str(count),"/",str(total))
        self.assertTrue(count == total)
        
    