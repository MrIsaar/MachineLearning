if __name__ == '__main__':
    from ID3Constructor import ID3setup
    import os
    CSVfile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/train.csv"
    dataDescFile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/data-desc.txt"

    print (__file__)
    dirname = os.path.dirname(os.path.dirname(__file__))
    print(dirname)
    filename = dirname + '/car/train.csv'
    print(filename)
    #ID3setup(CSVfile,dataDescFile,)