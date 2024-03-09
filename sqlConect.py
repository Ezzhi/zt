import sqlite3

db_file = "scrapML.db" #nombre de la base de datos, se puede cambiar de aca

conn = sqlite3.connect(db_file)
c = conn.cursor()

def closeSQL():
    conn.commit()
    conn.close()

def buscarExistenciaResultsML(idML):
    try:        
        
        fila = c.execute("SELECT price, priceAnt, priceMin FROM itemsML WHERE pub_id = '"+idML+"'")
        return fila.fetchone()
        
    except sqlite3.Error as e:
        print(e)


def insertarItem(itemML, pub_idML, titleML, priceML, priceAnt, priceMin, linkML, fechaML, tabla, itemEdit):
    
    if (itemEdit == True):
        c.execute("UPDATE itemsML SET price="+priceML+", priceAnt="+priceAnt+", priceMin="+priceMin+" WHERE pub_id ='"+pub_idML+"'")
    else:
        c.execute("INSERT INTO itemsML(pub_id, price, priceAnt, priceMin) VALUES (?, ?, ?, ?)", (pub_idML, priceML, priceAnt, priceMin))

    c.execute("INSERT INTO itemsML_Total(item, pub_id, title, price, link, date, category) VALUES (?, ?, ?, ?, ?, ?, ?)", (itemML, pub_idML, titleML, priceML, linkML, fechaML, tabla))
    
