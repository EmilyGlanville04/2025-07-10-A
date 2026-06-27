import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph= nx.DiGraph()
        self._idMapProdotti = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getCategorie()

    def buildGraph(self,categoria,startDate, endDate):
        self._graph.clear()
        self._idMapProdotti.clear()
        id_categoria = int(categoria)
        prodotti = DAO.getPrdotti(categoria)
        for p in prodotti:
            self._idMapProdotti[p.product_id]=p
        self._graph.add_nodes_from(prodotti)
        nvendite = DAO.getVenditeByProdotto(id_categoria, startDate, endDate)
        for i in range(len(prodotti)):
            for j in range(i+1, len(prodotti)):
                nodoA = prodotti[i]
                nodoB = prodotti[j]
                venditeA = nvendite.get(nodoA.product_id,0)
                venditeB = nvendite.get(nodoB.product_id,0)
                if venditeA > 0 and venditeB > 0:
                    peso = venditeA + venditeB
                    if venditeA>venditeB:
                        self._graph.add_edge(nodoA,nodoB,weight=peso)
                    elif venditeB>venditeA:
                        self._graph.add_edge(nodoB,nodoA,weight=peso)
                    else:
                        self._graph.add_edge(nodoA, nodoB, weight=peso)
                        self._graph.add_edge(nodoB, nodoA, weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Prodotti(self):
        top5 = []
        for nodo in self._graph.nodes:
            peso_uscenti=0
            peso_entranti=0
            for _, _, dati in self._graph.out_edges(nodo, data=True):
                peso_uscenti += dati["weight"]
            for _, _, dati in self._graph.in_edges(nodo, data=True):
                peso_entranti += dati["weight"]
            score = peso_uscenti - peso_entranti
            top5.append((nodo, score))
        top5.sort(key=lambda x: x[1], reverse=True)
        return top5[:5]

    def getNodes(self):
        return list(self._graph.nodes)

    def trovaCammino(self,nodoStart,nodoEnd,N):
        self._best_cammino = []
        self._best_peso = 0
        cammino_parziale = [nodoStart]
        self._ricorsione(cammino_parziale,nodoEnd,N,0)
        return self._best_cammino, self._best_peso


    def _ricorsione(self,parziale,nodoEnd, N,peso_attuale):
        ultimo = parziale[-1]
        if len(parziale) ==N:
            if ultimo == nodoEnd and peso_attuale > self._best_peso:
                self._best_peso=peso_attuale
                self._best_cammino=parziale.copy()
            return
        for vicino in self._graph.successors(ultimo):
            if vicino not in parziale:
                peso_arco = self._graph[ultimo][vicino]["weight"]
                parziale.append(vicino)
                self._ricorsione(parziale,nodoEnd,N,peso_attuale+peso_arco)
                parziale.pop()

    def getNodeById(self, product_id):
        return self._idMapProdotti[product_id]