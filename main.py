import mysql.connector
from jinja2 import environment
from app import Wsgiclass

app=Wsgiclass()
#waitress-serve --listen=*:8000 main:app
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
    

    
@app.ruta("/productos")
def home(request,response):

     response.text= app.template(
        "productos.html", context={"title": "Pagina Principal", "user": "PRODUCTOS"})
   


@app.ruta("/ingresoProd")
def ingresoProd(request,response):
    response.text= app.template(
        "ingresoProd.html", context={"title": "Ingresar productos al stock","user": "INGRESAR PRODUCTOS"})