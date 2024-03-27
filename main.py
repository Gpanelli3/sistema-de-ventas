import mysql.connector
from jinja2 import environment
from app import Wsgiclass

app=Wsgiclass()

@app.ruta("/home")
def home(request,response):
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='sistema-ventas')
    cursor=conexion.cursor()
    cursor.execute("select producto.idProducto,producto.nombre,producto.descripcion,categorias.nombre,producto.cantidad,producto.precio FROM producto inner join categorias on categorias.idcategorias=id_cat_corresp")

    productos=[]
    for i in cursor:
        productos.append(i)


    response.text= app.template(
        "home.html", context={"title": "Pagina Principal", "user": "a nuestra pagina de productos", "producto":productos})
