import requests as rq
import sqlite3

db_file = "scrapML.db" #nombre de la base de datos, se puede cambiar de aca
conn = sqlite3.connect(db_file)
c = conn.cursor()
#----------------------------------------------------------------
listSearch = [["fideos",""],["","MLA437468"]]
numPages = 10
#----------------------------------------------------------------
def closeSQL():
    conn.commit()
    conn.close()

def buscarExistenciaResultsML(idML):
    try:        
        fila = c.execute("SELECT price, priceAnt, priceMin FROM itemsML WHERE pub_id = '"+idML+"'")
        return fila.fetchone()        
    except sqlite3.Error as e:
        print(e)

def insertarItem(pub_idML, priceML, priceAnt, priceMin, linkML, itemEdit):    
    if (itemEdit == True):
        c.execute("UPDATE itemsML SET price="+str(priceML)+", priceAnt="+str(priceAnt)+", priceMin="+str(priceMin)+" WHERE pub_id ='"+pub_idML+"'")
    else:
        c.execute("INSERT INTO itemsML(pub_id, price, priceAnt, priceMin) VALUES (?, ?, ?, ?)", (pub_idML, priceML, priceAnt, priceMin))
    c.execute("INSERT INTO itemsML_Total(pub_id, price, link) VALUES (?, ?, ?)", (pub_idML, priceML, linkML))    

def calcDesc(priceAct, priceAnt):
    result = priceAnt - priceAct
    result = result / priceAnt
    result = int(result * 100)
    return result

def searchLinkML(numPages, link):
        all_results=[]
        
        for pages in range(numPages):
            bucleLink = False
            while bucleLink == False:
                try:
                    result=rq.get(link + str(pages*50)).json()
                    all_results += result["results"]
                    bucleLink = True
                except Exception:
                    print("perfom_search error")
            numPaging = result["paging"]["total"]
            if (numPaging == len(all_results)):
                break
        return all_results


for item in listSearch:
    linkBusqueda = "https://api.mercadolibre.com/sites/MLA/search?shipping=fulfillment&q="+item[0]+"&sort=price_asc&category="+item[1]+"&offset="
    results = searchLinkML(numPages, linkBusqueda)

    for result in results:        
        itemExist = buscarExistenciaResultsML(result["id"])

        if (itemExist == None):
            insertarItem(result["id"], result["price"], result["price"], result["price"], result["permalink"], False)
        elif (result["price"] != itemExist[0]):
            descPrice = calcDesc(result["price"], itemExist[0])
            descMin = calcDesc(result["price"], itemExist[2])            
            
            if(descMin >= 5):
                insertarItem(result["id"], result["price"], itemExist[0], result["price"], result["permalink"], True)
                print("OFERTA! - DesMin: "+descMin+" "+result["permalink"]+" $"+result["price"])
            else:
                insertarItem(result["id"], result["price"], itemExist[0], itemExist[2], result["permalink"], True)
                if (descPrice >= 40):
                    print("OFERTA! - Descuento: "+descPrice+" "+result["permalink"]+" $"+result["price"])
closeSQL()
    

