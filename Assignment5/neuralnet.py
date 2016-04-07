import sys
sys.path.insert(0, "./lib/")
from lib_arff import arff
import math

THRES = 0.5


def sigmod(x):
    return 1.0 / (1 + math.exp(-x))


def neural_output(feature_vector, weight_vector):
    sum = 0.0
    for (feature, weight) in zip(feature_vector, weight_vector):
        sum += feature * weight
    print(sum)
    return sigmod(sum)


def get_class(classes, v):
    if v < THRES:
        return classes[0]
    else:
        return classes[1]

# TODO: implement backpropagation
def BackProp(weight_vector):
    return

def neural_net(file_name, folds, learning_rate, epochs):
    try:
        data = arff.load(open(file_name, 'rb'))
        weight_vector = [0.1]*61
        print()
        for ins in data["data"]:
            feature_vector = ins[:60] + [1.0]
            output = neural_output(feature_vector, weight_vector)
            print(output)
            print(get_class(data["attributes"][-1][1], output), ins[60])
    except Exception as e:
        print("Error loading file: " + str(e))
        import traceback
        traceback.print_stack()
    return


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python neuralnet.py trainfile num_folds learning_rate num_epochs")
        exit(1)
    file_name = sys.argv[1]
    folds = int(sys.argv[2])
    learning_rate = float(sys.argv[3])
    epochs = int(sys.argv[4])
    print("filename is %s\nfolds is %d\nlearning_rate is %f\nepoch is %d" % (file_name, folds, learning_rate, epochs))
    neural_net(file_name, folds, learning_rate, epochs)
