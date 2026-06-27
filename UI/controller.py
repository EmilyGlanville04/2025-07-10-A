import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._categoryValue = None

    def handleCreaGrafo(self, e):
        categoria = self._view._ddcategory.value
        startDate = self._view._dp1.value
        endDate = self._view._dp2.value
        if categoria is None:
            self._view.create_alert("Selezionare una categoria")
            return
        categoria = int(self._view._ddcategory.value)
        self._model.buildGraph(categoria,startDate,endDate)
        n,m = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato: {n} nodi e {m} archi"))
        self.fillDDProducts()
        self._view.update_page()

    def handleBestProdotti(self, e):
        self._view.txt_result.controls.clear()
        top5 = self._model.getTop5Prodotti()
        self._view.txt_result.controls.append(
            ft.Text("Top 5 prodotti più venduti:")
        )
        for prodotto, score in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{prodotto} - score: {score}")
            )
        self._view.update_page()

    def handleCercaCammino(self, e):
        startProduct = self._view._ddProdStart.value
        if startProduct is None:
            self._view.create_alert("Selezionare un prodotto")
            return
        endProduct= self._view._ddProdEnd.value
        if endProduct is None:
            self._view.create_alert("Selezionare un prodotto")
            return
        lunghezza = self._view._txtInLun.value
        if lunghezza is None:
            self._view.create_alert("Selezionare una lunghezza")
            return
        lunghezza = int(lunghezza)
        nodoStart = self._model.getNodeById(int(startProduct))
        nodoEnd = self._model.getNodeById(int(endProduct))
        cammino, peso = self._model.trovaCammino(nodoStart, nodoEnd, lunghezza)
        if not cammino:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))
            for nodo in cammino:
                self._view.txt_result.controls.append(ft.Text(f"→ {nodo}"))
        self._view.update_page()




    def fillDDCategory(self):
        categorie = self._model.getCategorie()
        for c in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(key=str(c.category_id),
                text=c.category_name))
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.value = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.value = datetime.date(last.year, last.month, last.day)

    def fillDDProducts(self):
        self._view._ddProdStart.options.clear()
        self._view._ddProdEnd.options.clear()
        for nodo in self._model.getNodes():
            option = ft.dropdown.Option(key=str(nodo.product_id), text=nodo.product_name)
            self._view._ddProdStart.options.append(option)
            self._view._ddProdEnd.options.append(option)
        self._view.update_page()
