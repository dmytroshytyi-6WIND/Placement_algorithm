#Authors: Dmytro Shytyi
#Site: https://dmytro.shytyi.net
#mail: contact.dmytro@shytyi.net
#Licence: GPL

import contextlib as __stickytape_contextlib

@__stickytape_contextlib.contextmanager
def __stickytape_temporary_dir():
    import tempfile, shutil
    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)


with __stickytape_temporary_dir() as (__stickytape_working_dir):

    def __stickytape_write_module(path, contents):
        import os, os.path, errno

        def make_package(path):
            parts = path.split('/')
            partial_path = __stickytape_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    open(os.path.join(partial_path, '__init__.py'), 'w').write('\n')

        make_package(os.path.dirname(path))
        full_path = os.path.join(__stickytape_working_dir, path)
        with open(full_path, 'w') as (module_file):
            module_file.write(contents)


    import sys as __stickytape_sys
    __stickytape_sys.path.insert(0, __stickytape_working_dir)
    __stickytape_write_module('env.py', 'import networkx as nx\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nimport random\nimport pylab\nfrom matplotlib.pyplot import pause\nfrom clustering2 import findCentroids\npylab.ion()\n\n\n#return tuple of tuple (X,(Y,Z)) where :\n#X - random node from domain Y\n#Y - domain where X is located. And to X new node will be added, \n#Z - length between new node and  X.\ndef randomDomainShortestPath(G,domains,numberTacker,numberTotal):\n    chsdNodes={}\n         #take random node from each domain and calculate \n    for domain in np.arange(0,numberTacker):\n        domainNode=random.choice(domains.get(str(domain)))\n        shortestPath=nx.shortest_path_length(G,source=domain,target=domainNode)\n        newNodeLength=random.randint(1, 10)\n        totalLength=shortestPath+newNodeLength\n        chsdNodes[(domainNode,(domain,newNodeLength))]=totalLength\n            #chsdNodes[str(random.choice(domain))]=x.shortest_path_length(G,source=0,target=4)\n    nodeDomainLength=min(chsdNodes, key=chsdNodes.get)\n    return nodeDomainLength\n\n#this function returns a node(that has shortest path to one of the tackers) to add to graph with next information (X(Y,Z))look function RandomDataShortestPath to find details\ndef randomDomainBalanced(G,domains,numberTacker,numberTotal,branchesMaxPerNode):\n    import operator\n    chsdNodes={}\n    #for each domain we get the node that has the shortest lentgh to the root node(tacker) of the domain \n    for domain in np.arange(0,numberTacker):\n        domainNode=0\n        #find paths weights\n        mylength=nx.single_source_dijkstra_path_length(G,domain)\n        #sort path weights \n        slength = sorted(mylength.items(), key=operator.itemgetter(1))\n        if debug:\n            print(\'mylength\',mylength)\n        for node in slength:\n            if len(G.neighbors(node[0])) <= branchesMaxPerNode:\n                domainNode=node[0]\n                shortestPath=node[1]\n                if debug:\n                    print (domainNode)\n                    print (shortestPath)\n                break\n        newNodeLength=random.randint(1, 10)\n        totalLength=shortestPath+newNodeLength\n        #add node to the dictionary of nodes with length to the tacker\n        chsdNodes[(domainNode,(domain,newNodeLength))]=totalLength\n        if debug:\n            print (\'Nodes - each node for each domain ready to be choosed by shortest weight \',chsdNodes)\n    nodeDomainLength=min(chsdNodes, key=chsdNodes.get)\n    return nodeDomainLength\n\ndef graphInitRand(numberTacker=3,numberNodes=20,branchesMaxPerNode=10):\n    numberTotal=numberTacker + numberNodes\n    G=nx.Graph()\n    domains={} #dictionary of lists, lists are domains\n    for tacker in np.arange(0,numberTacker):\n        G.add_node(tacker,type=\'t\',domain=str(tacker))\n        domains[\'%s\' % tacker] = [tacker]\n        print (\'tacker \', tacker,\'=\',tacker) \n    if debug:\n        print (domains)\n    for node in np.arange(numberTacker,numberTotal):\n#        nodeDomainLength=randomDomainShortestPath(G,domains,numberTacker,numberTotal)\n        nodeDomainLength=randomDomainBalanced(G,domains,numberTacker,numberTotal,branchesMaxPerNode)\n        if debug:\n            print (nodeDomainLength)\n        #add new node to networkx\n        G.add_node(node,type=\'c\',domain=str(nodeDomainLength[1][0]))\n        #add new edge to networkx\n        G.add_edge(node,nodeDomainLength[0],weight=nodeDomainLength[1][1])\n        #add new node to the domain(our structure)\n        domains[str(nodeDomainLength[1][0])].append(node)\n        #print(G.nodes(data=True))\n\n        #connect separated domains\n        #numbTacker = numberTacker - 1\n    for domaina in np.arange(numberTacker):\n        for domainb in np.arange(numberTacker):\n            if not (domains.get(str(domaina)) == domains.get(str(domainb))):\n                nodeDomainA=random.choice(domains.get(str(domaina)))\n                nodeDomainB=random.choice(domains.get(str(domainb)))\n                G.add_edge(nodeDomainA,nodeDomainB,weight=20)\n    return domains,G\n\ndef graphInit():\n    G = nx.Graph()\n    #NODES\n    #Types: c=cluster,c=tacker+clusted\n    G.add_node(\'a\',type=\'t\',domain=\'2\')\n    G.add_node(\'b\',type=\'c\',domain=\'0\')\n    G.add_node(\'c\',type=\'t\',domain=\'0\')\n    G.add_node(\'d\',type=\'c\',domain=\'0\')\n    G.add_node(\'e\',type=\'c\',domain=\'2\')\n    G.add_node(\'f\',type=\'c\',domain=\'1\')\n    G.add_node(\'g\',type=\'t\',domain=\'1\')\n    G.add_node(\'h\',type=\'c\',domain=\'0\')\n    G.add_node(\'i\',type=\'c\',domain=\'1\')\n    G.add_node(\'k\',type=\'c\',domain=\'2\')\n    G.add_node(\'l\',type=\'c\',domain=\'2\')\n    #EDGES\n    G.add_edge(\'a\',\'b\',weight=\'10\')\n    G.add_edge(\'a\',\'c\',weight=\'15\')\n    G.add_edge(\'a\',\'d\',weight=\'20\')\n    G.add_edge(\'a\',\'e\',weight=\'10\')\n    G.add_edge(\'a\',\'f\',weight=\'30\')\n    G.add_edge(\'g\',\'h\',weight=\'12\')\n    G.add_edge(\'g\',\'i\',weight=\'18\')\n    G.add_edge(\'g\',\'k\',weight=\'30\')\n    G.add_edge(\'g\',\'l\',weight=\'20\')\n    G.add_edge(\'b\',\'l\',weight=\'100\')\n\n    return G\n\n\n#def connect_to\n#def genClusters(n,G):\n\n##################################################################\n##################################################################\n#CLUSTERING\n##################################################################\n##################################################################\n#findCentroids(G,totalTackerDomain)\n\n#####################################################################\n#####################################################################\n#ALG\n#####################################################################\n#####################################################################\n\ndef assignOrphanClusters(G,orphanClusterSet,totalTackerDomain,tackerDomain):\n    #we add ONLY 1 node per tackerdomain(TO ACHIEVE LOAD-BALANCE between domains) for 1 step\n    tackerDomain=(tackerDomain+1)%totalTackerDomain\n    if (tackerDomain == 0):\n        tackerDomain =+ 1\n    #for each orpan OpenStack cluster from orphanCluster list.\n    if debug:\n        print (\'------------------------domain:\',tackerDomain)\n        print (\'orphanSet: \', orphanClusterSet)\n    for cl in orphanClusterSet:\n        if debug:\n            print (\'cluster: \', cl)\n            #discover connected to current cluster vertexes(other clusters)\n        for neigh in G.neighbors(cl):\n            if debug:\n                print (\'NEIGHS: \', G.neighbors(cl))\n                print (\'neigh: \',neigh)\n            #if vertex connected to current cluster located in different domain\n            attrs=nx.get_node_attributes(G,\'domain\')\n            neighAttr=attrs.get(neigh,\'WARNING\')\n            if debug:\n                print (\'NeighAttr: \',neighAttr)\n                print (\'domain: \',tackerDomain)\n            if (int(neighAttr) == int(tackerDomain)):\n                if debug:\n                    print (\'============================CARAMBA\')\n                    print (\'DOMAIN: \',G.node[cl][\'domain\'])\n                G.node[cl][\'domain\']=str(tackerDomain)\n                orphanClusterSet.remove(cl)\n                return G,orphanClusterSet, tackerDomain\n    return G, orphanClusterSet, tackerDomain\n\n\ndef drawGraph(G,pos,totalTackerDomain):\n#####################################################################\n#####################################################################\n#INITIALIZE COLORS FOR NODES\n###################################################################\n###################################################################\n#color_map = dict()\n  \n    color_map = {   \'0\': \'#FF0000\',\n                    \'1\': \'#00FFFF\',\n                    \'2\': \'#FFFF00\',\n                    \'3\': \'#0FFF12\',\n                    \'4\': \'#35BA66\',\n                    \'5\': \'#98U243\',\n                    \'6\': \'#164566\',\n                    \'7\': \'#245525\',\n                    \'8\': \'#465455\',\n                    \'9\': \'#877998\',\n                }\n     \n    if totalTackerDomain <= 10:\n        node_colors = [color_map[G.node[node][\'domain\']] for node in G]\n    \n    red_edges=[]\n    #red_edges = [(\'A\', \'C\'), (\'E\', \'C\')]\n    #edge_colours = [\'black\' if not edge in red_edges else \'red\'\n    #                                for edge in G.edges()]\n    black_edges = [edge for edge in G.edges() if edge not in red_edges]\n\n\n\n\n###################################################################\n###################################################################\n#DRAW THE GRAPH\n###################################################################\n###################################################################\n\n\n\n    #######EDGES+LABELS\n\n    #nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color=\'r\', arrows=True, with_labels=True)\n    edge_labels = nx.get_edge_attributes(G,\'weight\')\n    nx.draw_networkx_edges(G, pos, edgelist=black_edges, with_labels=True)\n    if weightShow:\n        #nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels.get(\'weight\'))\n        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)\n\n    #####NODES+LABELS\n\n    #nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap(\'jet\'), node_color = values, with_labels=True)\n    if totalTackerDomain <= 10:\n        nx.draw_networkx_nodes(G, pos, node_color = node_colors, with_labels=True)\n    else:\n        nx.draw_networkx_nodes(G, pos, with_labels=True)\n    \n    node_labels = nx.get_node_attributes(G,\'type\')\n\n    if nodesNames:\n        nx.draw_networkx_labels(G, pos)\n    else:\n        nx.draw_networkx_labels(G, pos, labels = node_labels)\n\n\n    plt.show()\n\n\n\n\n####################################################################\n####################################################################\n#MAIN_PROGRAM\n####################################################################\n####################################################################\n\ndef exec(iterationsm = 5, debugm = 0, nodesNamesm = 1, weightShowm = 1, drawGraphm = 1, totalTackerDomainm = 5, NumberOfNodes = 500, allowedNeighbours=5,nodesm = [] , edgesm = []):\n    ##############################\n    #initialization_part\n    #############################\n    #\n    #console debug\n    global debug\n    debug=debugm\n    #Name of the nodes(a,b,c)= 1 | type of the nodes (t,c) = 0\n    global nodesNames\n    nodesNames=nodesNamesm\n    #show weights on the graph\n    global weightShow\n    weightShow=weightShowm\n    global totalTackerDomain\n    totalTackerDomain=totalTackerDomainm\n    #G=graphInit()\n    #arguments(numberOfDomains,NumberOfNodes,allowedNeighbours)\n    if len(nodesm) > 0:\n        G = nx.Graph()\n        for node in nodesm:\n            G.add_node(str(node),type=\'c\',domain=\'0\')\n        for edge in edgesm:\n            G.add_edge(str(edge[0]),str(edge[1]),weight=int(edge[2]))\n       \n    else:\n        domain,G=graphInitRand(totalTackerDomain,NumberOfNodes,allowedNeighbours)\n        #orphanClusterSet = [\'c\',\'d\',\'b\',\'h\']\n        orphanClusterSet=domain[\'0\']\n\n    tackerDomain=0\n\n\n\n    ###############################\n    #execution_part\n    ###############################\n    #pylab.show()\n\n    # Need to create a layout when doing\n    # separate calls to draw nodes and edges\n    pos = nx.spring_layout(G)\n    #pos = nx.fruchterman_reingold_layout(G)\n    if drawGraphm:\n        drawGraph(G,pos,totalTackerDomain)\n        pause(1)\n    \n\n    ###################################\n    ###################################\n    #centroids\n    M=G.copy()\n    result=findCentroids(M,totalTackerDomain,iterationsm)\n    """\n    if drawGraphm:\n        input("Press Enter to continue...")\n        pause(5)\n        while (orphanClusterSet):\n            #keep assigning orphan clusters until orphan cluster list is not empty.\n            G,orphanClusterSet,tackerDomain=assignOrphanClusters(G,orphanClusterSet,totalTackerDomain,tackerDomain)\n            drawGraph(G,pos)\n            pause (5)\n\n        input("Press Enter to continue...")\n    """\n    if debug:\n        print (G.nodes(data=True))\n                \n    return result\n        ####################################################################\n    ####################################################################\n    #TO SHOW DATA FROM GRAPH\n    ####################################################################\n    ####################################################################\n\n    #print (\'NODES+ATTRIBUTES:\')\n    #print (G.nodes(data=True))\n    #print (nx.number_of_edges(G))\n    #An nbunch is any iterable container of nodes that is not itself a node in the graph. (e.g. a list, set, graph, file, etc..)\n    #print (\'EDGES\')\n    #print (G.edges(data=True))\n    #return the attribute dictionaryasociated with edge (u,v)\n    #print (\'EDGE+ATTRIBUTES\')\n    #print(G.get_edge_data(\'b\', \'a\', \'weight\'))\n\n#exec(debugm = 0,nodesNamesm = 1, weightShowm = 1, totalTackerDomainm = 5, NumberOfNodes = 500, allowedNeighbours=5)\n\n\n\n\n\n\n\n\n')
    __stickytape_write_module('clustering2.py', 'import networkx as nx\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nimport random\nimport pylab\nfrom matplotlib.pyplot import pause\npylab.ion()\n\n\n#get random element from the list and delete it from list\ndef randPopFrom (listNodes):\n    return listNodes.pop(random.randrange(len(listNodes)))\n\ndef getCentroids(G,centroidsNumber=4,centroids=[]):\n    #copy structure from G to myNodes to perform operations on that.\n    myNodes=G.nodes(data=True)\n    myNodesNew=[]\n    #centroidsNumber=4\n    graphs=[]\n    #dictionary of lists, lists are domains\n    domains={}\n    \n    if not centroids:\n        #delete from stack nodes, and add them to the "tackerNodes list" - initial list of centroids.\n        for centroid in range (0,centroidsNumber):\n            currentCentroid=randPopFrom(myNodes)\n            centroids.append(currentCentroid)\n            domains[\'%s\' % centroid] = [currentCentroid[0]]\n            #print (\'currentCentroid\',currentCentroid[0])\n    else:\n        for centroid in range (0,centroidsNumber):\n            centroids.append(centroids[centroid])\n            domains[\'%s\' % centroid] = [centroids[centroid]]\n\n    #    graphs [\'%s\' % centroid] = []\n\n    #print (\'centroids\',centroids)\n    #while exists not assigned nodes to the clusters\n    while (myNodes):\n        randNode = randPopFrom(myNodes)\n        randNodeToClustersLength=nx.single_source_dijkstra_path_length(G,randNode[0])\n        #if debug:\n        #    print(centroids)\n        shortestPath=999\n    #connect random node by sp to the closest centroid\n    #    for centroid in centroids:\n    #        print (centroid)\n    #        if randNodeToClustersLength[centroid[0]] < shortestPath:\n    #            shortestPath=randNodeToClustersLength[centroid[0]]\n    #            spToDomain=centroid[1].get(\'domain\')\n\n\n    #connect random node by sp to the closes domain.\n        for domain in domains:\n            #print (\'domain \', domain, \' has:\', domains.get(domain))\n            for nodex in domains.get(domain):\n                #print (\'NODE\',nodex)\n                #print  (randNodeToClustersLength[nodex])\n                #print (shortestPath)\n                if (randNodeToClustersLength[nodex] < shortestPath):\n                    shortestPath=randNodeToClustersLength[nodex]\n                    #spToDomain=centroid[1].get(\'domain\')\n                    spToDomain=domain\n        #print (\'randNode\',randNode)\n        #print (spToDomain)\n        randNode[1][\'domain\'] = str(spToDomain)\n        domains[\'%s\' % spToDomain].append(randNode[0])\n\n    #convert connected component into several domains subgraphs to calculate closeness\n    for domain in domains:\n        graphs.append(G.subgraph (domains.get(domain)))\n        #print (graphs[int(domain)].nodes(data=True))\n        #print (graphs[int(domain)].nodes())\n    res = []\n    avCloseness = 0\n    for graph in graphs:\n        closeness_dict=nx.closeness_centrality (graph,distance=\'weight\')\n#        closeness_dict=nx.betweenness_centrality (graph,weight=\'weight\')\n        if closeness_dict:\n            maximum = max(closeness_dict, key=closeness_dict.get)\n            res.append (maximum)\n            avCloseness = avCloseness + closeness_dict[maximum]\n    avCloseness = avCloseness/len(graphs)\n    return res, avCloseness\n\nimport itertools\nimport operator\n\ndef most_common(L):\n    # get an iterable of (item, iterable) pairs\n    SL = sorted((x, i) for i, x in enumerate(L))\n    # print \'SL:\', SL\n    groups = itertools.groupby(SL, key=operator.itemgetter(0))\n    # auxiliary function to get "quality" for an item\n    def _auxfun(g):\n        item, iterable = g\n        count = 0\n        min_index = len(L)\n        for _, where in iterable:\n            count += 1\n            min_index = min(min_index, where)\n        # print \'item %r, count %r, minind %r\' % (item, count, min_index)\n        return count, -min_index\n        #pick the highest-count/earliest item\n    return max(groups, key=_auxfun)[0]\n\ndef findCentroids (G,n,iterations):\n    result=[]\n    avCloseness=0\n    for i in range (0,iterations):\n        resPrev,avCl=getCentroids(G,n,[]) \n        resPrev = set(resPrev)\n        resNext=set([])\n        #print (resNext)\n        cnt=0\n        while (resNext != resPrev ):\n            resPrev=resNext\n            resNext,avClosenessNext=getCentroids(G,n,list(resPrev))\n            resNext = set(resNext)\n            cnt += 1\n            print (avClosenessNext)\n        print (\'iterations to converge:\',cnt)\n        #print (resNext)\n        if avCloseness < avClosenessNext:\n            avCloseness = avClosenessNext\n            result=resNext\n            print (\'highest-found\', avCloseness)\n        #print (result)\n    print("FINISHED")\n#    print (\'RESULT OF PLACEMENT ALGORITHM. THE TACKER SHOULD BE PLACED ON NODES: \',most_common(result))\n    print (\'RESULT OF PLACEMENT ALGORITHM. THE TACKER SHOULD BE PLACED ON NODES: \')\n    print (\'res\',result)\n    print (\'avCloseness:\', avCloseness)\n    return result\n')
    import tkinter as tk
    from tkinter import filedialog
    import csv
    from env import exec
    nodes = []
    edges = []

    def fileOpen():
        global edges
        global nodes
        window.filename = filedialog.askopenfilename(initialdir='./', title='Select file')
        nodes = []
        edges = []
        with open(window.filename) as (csvfile):
            reader = csv.reader(csvfile)
            for row in reader:
                nodes.append(row[0])
                nodes.append(row[1])
                edges.append(row)

            nodes = set(nodes)
            nodes = list(nodes)


    window = tk.Tk()
    window.title('Placement algorithm by Dmytro Shytyi')
    window.geometry('400x400')
    labelTackerNodesNum = tk.Label(text='Number of Tacker Nodes to place: [1,5..22..]')
    labelTackerNodesNum.grid(column=0, row=0)
    v = tk.IntVar()
    entry_fieldTackerNodesNum = tk.Entry(textvariable=v)
    entry_fieldTackerNodesNum.grid(column=1, row=0)
    v.set(3)
    labelDebug = tk.Label(text='Enable debug in the console')
    labelDebug.grid(column=0, row=1)
    v = tk.IntVar()
    entry_fieldDebug = tk.Entry(textvariable=v)
    entry_fieldDebug.grid(column=1, row=1)
    v.set(0)
    labelNodesNames = tk.Label(text='Show Vertex numbers/types(tacker/openstack): [1 | 0]')
    labelNodesNames.grid(column=0, row=2)
    v = tk.IntVar()
    entry_fieldNodesNames = tk.Entry(textvariable=v)
    entry_fieldNodesNames.grid(column=1, row=2)
    v.set(1)
    labelWeights = tk.Label(text='Show weights of the edges: [1 | 0]')
    labelWeights.grid(column=0, row=3)
    v = tk.IntVar()
    entry_fieldWeights = tk.Entry(textvariable=v)
    entry_fieldWeights.grid(column=1, row=3)
    v.set(1)
    labelDrawGraph = tk.Label(text='Draw the graph: [1 | 0]')
    labelDrawGraph.grid(column=0, row=4)
    v = tk.IntVar()
    entry_fieldDrawGraph = tk.Entry(textvariable=v)
    entry_fieldDrawGraph.grid(column=1, row=4)
    v.set(1)
    labelIter = tk.Label(text='Number of algorithm iterations: [2,5..50]')
    labelIter.grid(column=0, row=5)
    v = tk.IntVar()
    entry_fieldIter = tk.Entry(textvariable=v)
    entry_fieldIter.grid(column=1, row=5)
    v.set(5)
    labelsimul = tk.Label(text='Simulation parameters')
    labelsimul.grid(column=3, row=0)
    labelNumberOfNodes = tk.Label(text='Number of all nodes in the graph')
    labelNumberOfNodes.grid(column=3, row=1)
    v = tk.IntVar()
    entry_fieldNumberOfNodes = tk.Entry(textvariable=v)
    entry_fieldNumberOfNodes.grid(column=4, row=1)
    v.set(60)
    labelAllowedNeighbours = tk.Label(text='Number of neighbours per node(degree)')
    labelAllowedNeighbours.grid(column=3, row=2)
    v = tk.IntVar()
    entry_fieldAllowedNeighbours = tk.Entry(textvariable=v)
    entry_fieldAllowedNeighbours.grid(column=4, row=2)
    v.set(10)
    labelsimul = tk.Label(text='This program has 2 modes. Data generated using the model or using the user file')
    labelsimul.grid(column=0, row=11)
    labelsimul2 = tk.Label(text="To configure model parameters refer to simulation parameters section'")
    labelsimul2.grid(column=0, row=12)
    labelsimul3 = tk.Label(text="User file has format: 'Node name 1','Node name 2','latency'")
    labelsimul3.grid(column=0, row=13)
    labelsimul4 = tk.Label(text='You may want to disable displaying the graph depending on number of nodes')
    labelsimul4.grid(column=0, row=14)
    buttonFileOpen = tk.Button(text='Open user file', command=fileOpen)
    buttonFileOpen.grid(column=3, row=10)

    def algStart():
        global edges
        global nodes
        number_nodes = int(entry_fieldNumberOfNodes.get())
        allowedNeighboursm = int(entry_fieldAllowedNeighbours.get())
        iterations = int(entry_fieldIter.get())
        NodesNames = int(entry_fieldNodesNames.get())
        debug = int(entry_fieldDebug.get())
        weights = int(entry_fieldWeights.get())
        tacker_nodes = int(entry_fieldTackerNodesNum.get())
        drawGraph = int(entry_fieldDrawGraph.get())
        if len(nodes) < 1:
            nodes = []
            edges = []
        placementList = exec(iterationsm=iterations, debugm=debug, nodesNamesm=NodesNames, weightShowm=weights, drawGraphm=drawGraph, totalTackerDomainm=tacker_nodes, NumberOfNodes=number_nodes, allowedNeighbours=allowedNeighboursm, nodesm=nodes, edgesm=edges)
        labelWeights = tk.Label(text='The pacement of the nodes (result) is:')
        labelWeights.grid(column=0, row=6)
        result = tk.Text(master=window, height=5)
        result.grid(column=1, row=6)
        result.insert(tk.END, str(placementList))


    button1 = tk.Button(text='Start the algorithm', command=algStart)
    button1.grid(column=2, row=10)
    window.mainloop()
