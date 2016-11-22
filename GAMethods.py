import random

def getIndividualPoint(simulator):
    pointList = simulator.generateNPoints()
    #print "\n\n --------------------------------\n"
    #print pointList[0].value
    #pointList[0].evaluateObjectives()
    #print pointList[0].objectives
    ind = [1 if i[1] == True else 0 for i in pointList[0].value]
    #print ind
    return ind

def evaluateObjectives(model, ind1):
    cost = evaluateCost(ind1, model)
    featureRichness = evaluateFeatureRichness(ind1)
    constraintsFailed = evaluateConstraintsFailed(ind1, model)
    return (cost, constraintsFailed,featureRichness)


def evaluateCost(ind1, model):
    """ Code for calculating cost of the given point goes here """
    # value = [[id1,True],[id2,True],[id3,False]...]
    # print 'find cost'
    return sum([model.treeNodeMap[model.nodeOrder[i]].cost if ind1[i] == 1 else 0 for i in range(len(ind1))])


def evaluateConstraintsFailed(ind1, model):
    """ Code for calculating how many constraints the point failed goes here """
    constraints_list = model.crossTreeConstraints
    leaves = [model.nodeOrder[i] for i in range(len(ind1)) if ind1[i] is 1]
    #leaves = [n[0] for n in self.value if n[1] is True]
    violations = 0
    for constraint in constraints_list:
        clauses = constraint.clauses
        isTrue = False
        for clause in clauses:
            node_id = clause[1:] if clause[0] == '~' else clause
            if (clause[0] == '~' and node_id not in leaves) or (clause[0] != '~' and node_id in leaves):
                isTrue = isTrue or True
        if not isTrue:
            violations += 1
            for index in xrange(len(ind1)):
                node_id = model.nodeOrder[index]
                if ind1[index] == 1:
                    if node_id in model.featureFailureCount:
                        model.featureFailureCount[node_id] += 1
                    else:
                        model.featureFailureCount[node_id] = 1
    return violations


def evaluateFeatureRichness(ind1):
    """ Code for calculating Feature Richness of a point goes here """
    return sum(ind1)

def printPopulation(pop):
    for i in pop:
        print str(i) + " : " + str(i.fitness.values)


def getOrRelationshipChoiceString(numberOfChild):
    binaryString = ""
    for i in xrange(numberOfChild):
        if random.random() < 0.5:
            binaryString += "1"
        else:
            binaryString += "0"
    if binaryString.find("1") != -1:
        # print binaryString
        return binaryString
    else:
        index = random.choice(xrange(numberOfChild))
        binaryString = ""
        for i in xrange(numberOfChild):
            if i != index:
                binaryString += "0"
            else:
                binaryString += "1"
        # print binaryString
        return binaryString

def dfs_mutate(treeNode, point, parentDecision, nodeDecisions, isMutated):
    if parentDecision and treeNode.type == "Mandatory":
        point.append([treeNode.id, nodeDecisions[treeNode.id]])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions,isMutated)
    elif parentDecision and treeNode.type == "Optional":
        if not isMutated:
            if random.random() < 0.8:
                parentDecision = nodeDecisions[treeNode.id]
                point.append([treeNode.id, nodeDecisions[treeNode.id]])
            else:
                isMutated = True
                parentDecision = not nodeDecisions[treeNode.id]
                point.append([treeNode.id, not nodeDecisions[treeNode.id]])
            for i in xrange(len(treeNode.children)):
                dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
        else:
            if random.random() < 0.5:
                parentDecision = True
                point.append([treeNode.id, True])
            else:
                parentDecision = False
                point.append([treeNode.id, False])
            for i in xrange(len(treeNode.children)):
                dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
    elif parentDecision and treeNode.type == "Featured Group":
        if isMutated:
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                index = random.choice(xrange(len(treeNode.children)))
                for i in xrange(len(treeNode.children)):
                    if index == i:
                        parentDecision = True
                        point.append([treeNode.children[i].id, True])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                choiceString = getOrRelationshipChoiceString(len(treeNode.children))
                for i in xrange(len(treeNode.children)):
                    if choiceString[i] == '1':
                        parentDecision = True
                        point.append([treeNode.children[i].id, True])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
        else:
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                if random.random() < 0.8:
                    isMutated = False
                    for i in xrange(len(treeNode.children)):
                        parentDecision = nodeDecisions[treeNode.children[i].id]
                        point.append([treeNode.children[i].id, nodeDecisions[treeNode.children[i].id]])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, False)
                else:
                    isMutated = True
                    index = random.choice(xrange(len(treeNode.children)))
                    for i in xrange(len(treeNode.children)):
                        if index == i:
                            parentDecision = True
                            point.append([treeNode.children[i].id, True])
                            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, True)
                        else:
                            parentDecision = False
                            point.append([treeNode.children[i].id, False])
                            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, True)
            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                for i in xrange(len(treeNode.children)):
                    if random.random() < 0.8:
                        parentDecision = nodeDecisions[treeNode.children[i].id]
                        point.append([treeNode.children[i].id, nodeDecisions[treeNode.children[i].id]])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
                    else:
                        parentDecision = not nodeDecisions[treeNode.children[i].id]
                        point.append([treeNode.children[i].id, (not nodeDecisions[treeNode.children[i].id])])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, True)

    elif parentDecision and treeNode.type == "Group":
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
    elif parentDecision and treeNode.type == "Root":
        point.append([treeNode.id, True])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, False)
    elif not parentDecision:
        if treeNode.type == "Mandatory" or treeNode.type == "Optional":
            point.append([treeNode.id, False])
        elif treeNode.type == "Featured Group":
            for i in xrange(len(treeNode.children)):
                point.append([treeNode.children[i].id, False])
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)


def dfs(treeNode, point, parentDecision):
    if parentDecision and treeNode.type == "Mandatory":
        point.append([treeNode.id, True])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs(treeNode.children[i], point, parentDecision)
    elif parentDecision and treeNode.type == "Optional":
        if random.random() < 0.5:
            parentDecision = True
            point.append([treeNode.id, True])
        else:
            parentDecision = False
            point.append([treeNode.id, False])
        for i in xrange(len(treeNode.children)):
            dfs(treeNode.children[i], point, parentDecision)
    elif parentDecision and treeNode.type == "Featured Group":
        if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
            index = random.choice(xrange(len(treeNode.children)))
            for i in xrange(len(treeNode.children)):
                if index == i:
                    parentDecision = True
                    point.append([treeNode.children[i].id, True])
                    dfs(treeNode.children[i], point, parentDecision)
                else:
                    parentDecision = False
                    point.append([treeNode.children[i].id, False])
                    dfs(treeNode.children[i], point, parentDecision)
        elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
            choiceString = getOrRelationshipChoiceString(len(treeNode.children))
            for i in xrange(len(treeNode.children)):
                if choiceString[i] == '1':
                    parentDecision = True
                    point.append([treeNode.children[i].id, True])
                    dfs(treeNode.children[i], point, parentDecision)
                else:
                    parentDecision = False
                    point.append([treeNode.children[i].id, False])
                    dfs(treeNode.children[i], point, parentDecision)
    elif parentDecision and treeNode.type == "Group":
        for i in xrange(len(treeNode.children)):
            dfs(treeNode.children[i], point, parentDecision)
    elif parentDecision and treeNode.type == "Root":
        point.append([treeNode.id, True])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs(treeNode.children[i], point, parentDecision)
    elif not parentDecision:
        if treeNode.type == "Mandatory" or treeNode.type == "Optional":
            point.append([treeNode.id, False])
        elif treeNode.type == "Featured Group":
            for i in xrange(len(treeNode.children)):
                point.append([treeNode.children[i].id, False])
        for i in xrange(len(treeNode.children)):
            dfs(treeNode.children[i], point, parentDecision)



def matePoints(model, ind1, ind2):
    """ Logic for mate/crossover goes here  """
    ind1[len(ind1)-3] = 1
    ind2[len(ind2) - 3] = 1


def mutatePoints(model, ind1):
    """ Logic for mutation goes here """
    nodeDecisions = {}
    for index in range(len(ind1)):
        nodeDecisions[model.nodeOrder[index]] = (ind1[index]==1)
    point = []
    dfs_mutate(model.root , point, True, nodeDecisions, False)
    ind = [1 if i[1] == True else 0 for i in point]
    print str(ind1) + " ---> " + str(ind)
    ind1[len(ind1) - 1] = 1

