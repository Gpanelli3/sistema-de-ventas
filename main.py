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
    cursor.execute("select producto.idProducto,producto.nombre,producto.descripcion,categorias.nombre,producto.cantidad,producto.precio from producto inner join categorias on categorias.idcategorias=id_cat_corresp")

    productos=[]
    #cont=0
    for i in cursor:
        productos.append(i)
    conexion.close()
    #print(productos)
    #print(cont)

    response.text= app.template(
        "home.html", context={"title": "Pagina Principal", "user": "a nuestra pagina de productos", "producto":productos})
  

    
   

@app.ruta("/ingresoProd")
def ingresoProd(request,response):


    #conexion para insertar productos
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='sistema-ventas')
    
    cursor=conexion.cursor()
    
    #idp=cont+1
    nombre=request.POST.get('nombre')
    descripcion=request.POST.get('descripcion')
    precio=request.POST.get('precio')
    cantidad=request.POST.get('cantidad')
    categoria=request.POST.get('categoria')
    imagen=request.POST.get('imagen')

    nombreMax=""
    nombreMax=nombre.upper()

    try:
        #while not nombre or descripcion or precio or cantidad:
        print("no ingreso nombre del producto")
        
        sql="INSERT INTO producto(nombre,descripcion,precio,cantidad,id_cat_corresp, imagen) VALUES(%s,%s,%s,%s,%s,%s)"
        datos=(nombreMax,descripcion,precio,cantidad,categoria,imagen)
            
        
        cursor.execute(sql,datos)
        conexion.commit()

    except mysql.connector.Error as error:
        response.text=app.template(
            "error.html", context={"user": "ERROR EN LA BASE DE DATOS"}
        )

    conexion.close()


    response.text= app.template(
        "ingresoProd.html", context={"user": "PRODUCTOS INGRESADOS CORRECTAMENTE"})

    

    


@app.ruta("/productos")
def home(request,response):

     response.text= app.template(
        "productos.html", context={"title": "Pagina Principal", "user": "PRODUCTOS INGRESADOS CORRECTAMENTE"})