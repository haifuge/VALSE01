import pypyodbc

class DBOperator():
    conn=pypyodbc.connect("Driver={SQL Server};"
                      "Server=108.52.45.69,1434;"
                      "Database=test;"
                      "uid=sa;"
                      "pwd=64212917@Asiankitchen")
    # sql: query string, n: number of columns in query string
    def ExecSql(self, sql, n):
        cursor=self.conn.cursor()
        #comm=("select * from Customers")
        comm=(sql)
        cursor.execute(comm)
        results=cursor.fetchone()
        dataset=[]
        while results:
            item=[]
            for i in range(n):
                item.append(results[i])
            dataset.append(item)
            # print("Your customer "+str(results[0])+" " + results[1]+" lives in "+results[2])
            results=cursor.fetchone()
        self.conn.close()
        return dataset


#  mapId, personId, eventId, map_x, map_y, date_time, map_url
# test changes.