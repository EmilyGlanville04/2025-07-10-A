from database.DB_connect import DBConnect
from model.categories import Categories
from model.product import Products


class DAO():

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def getCategorie():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.* 
                    from categories c  """
        cursor.execute(query)
        for row in cursor:
            results.append(Categories(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPrdotti(category):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select  distinct p.*
                    from products p 
                    where p.category_id =%s """
        cursor.execute(query,(category,))
        for row in cursor:
            results.append(Products(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVenditeByProdotto(category,startDate,endDate):
        conn = DBConnect.get_connection()
        results = {}
        cursor = conn.cursor(dictionary=True)
        query = """SELECT oi.product_id, COUNT(*) AS nVendite
                    FROM order_items oi, orders o, products p
                    WHERE oi.order_id = o.order_id
                      AND oi.product_id = p.product_id
                      AND p.category_id = %s
                      AND o.order_date BETWEEN %s AND %s
                    GROUP BY oi.product_id"""
        cursor.execute(query, (category,startDate, endDate,))
        for row in cursor:
            results[row["product_id"]]=row["nVendite"]
        cursor.close()
        conn.close()
        return results









