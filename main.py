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
        "productos.html", context={"title": "Pagina Principal", "user": "PRODUCTOS INGRESADOS CORRECTAMENTE"})
   


@app.ruta("/ingresoProd")
def ingresoProd(request,response):

    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='sistema-ventas')
    
    cursor=conexion.cursor()
    
    #idp=request.POST.get('id')
    nombre=request.POST.get('nombre')
    descripcion=request.POST.get('descripcion')
    precio=request.POST.get('precio')
    cantidad=request.POST.get('cantidad')
    categoria=request.POST.get('categoria')

    try:
        sql="INSERT INTO producto(idProducto,nombre,descripcion,precio,cantidad,id_cat_corresp) VALUES(%s,%s,%s,%s,%s,%s)"
        datos=(nombre,descripcion,precio,cantidad,categoria)
        
        cursor.execute(sql,datos)
        conexion.commit()


    except mysql.connector.Error as error:
        print("error al actualizar en la base de datos", error)


    conexion.close()
    


    response.text= app.template(
        "ingresoProd.html", context={"user": "PRODUCTOS INGRESADOS CORRECTAMENTE"})