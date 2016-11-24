import sys
import numpy as np
from parser import SPLOTParser
from Simulator import Simulator

def main():
    assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"
    modelFile = sys.argv[1]
    model = SPLOTParser().parse(modelFile)
    model.printTree(model.root, 0)
    print "\n\n ALL CROSS TREE CONSTRAINTS"
    model.printCrossTreeConstraints()
    print "\n Generating Tree level Constraints using grammar ... "
    model.generateTreeStructureConstraints(model.root)
    print "\n\n ALL TREE STRUCTURE CONSTRAINTS"
    model.printTreeConstraints()
    #print "\n\n"
    #model.printStatistics()

    simulator = Simulator(model)
    n = 1000
    cost = []
    violations = []
    num_features = []

    print "\n\nGENERATING " + str(n) + " POINTS"
    count = 0
    points = simulator.generateNPoints(n)
    for i,point in enumerate(points):
        # print '*******POINT '+str(i)+' ********'
        point.evaluateObjectives()
        #print point.objectives
        if point.objectives.constraintsFailed == 0:
            count += 1
        cost.append(point.objectives.cost)
        violations.append(point.objectives.constraintsFailed)
        num_features.append(point.objectives.featureRichness)

    print 'Mean cost', np.mean(cost)
    print 'Var cost', np.var(cost)
    print 'Mean violations', np.mean(violations)
    print 'Var violations', np.var(violations)
    print 'Mean num of features', np.mean(num_features)
    print 'Var num of features', np.var(num_features)
    print 'count =', count
    # plt.scatter(cost,num_features)
    # plt.show()
    # plt.scatter(violations,num_features)
    # plt.show()

if __name__ == "__main__":
    main()