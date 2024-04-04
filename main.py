from app import Wsgiclass
from whitenoise import WhiteNoise
from jinja2 import Environment, FileSystemLoader #para poder recorrer/cargar/acceder = gestionar a las plantillas
import mysql.connector 
from webob import Request, Response
from wsgiref.simple_server import make_server
import os #para las direcciones de los archivos

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

conexion1 = mysql.connector.connect(
    host="localhost",
    user="genaro",
    passwd="password",
    database="sistema-ventas"
)

cursor1 = conexion1.cursor()

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

        
    sql="INSERT INTO producto(nombre,descripcion,precio,cantidad,id_cat_corresp, imagen) VALUES(%s,%s,%s,%s,%s,%s)"
    datos=(nombreMax,descripcion,precio,cantidad,categoria,imagen)
    
    try:
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




@app.ruta('/update')
def actualizar_precio(request, response):
    conexion = mysql.connector.connect(host='localhost', 
                                       user='genaro', 
                                       passwd='password', 
                                       database='sistema-ventas')
    cursor = conexion.cursor()


    idProducto = request.POST.get('idp')
    nuevoPrecio = request.POST.get('precio')

    sql="UPDATE producto SET precio = %s WHERE idProducto = %s"
    datos=(nuevoPrecio, idProducto)
           
    try:
        cursor.execute(sql,datos)
        conexion.commit()
        print("actualizacion correcta")
    
    except mysql.connector.Error as error:
        print("Error MySQL:", error)

    finally:
        conexion.close()

    response.text= app.template(
        "update.html", context={"title": "Pagina Principal", "user": "PRODUCTOS INGRESADOS CORRECTAMENTE"})
    




@app.ruta("/categ")
def select(request, response):
    id = request.POST.get('pc')
    
    cursor1.execute ("SELECT * FROM producto WHERE id_cat_corresp = %s ;" , (id,))
    
    resultados = cursor1.fetchall()
    

    template= env.get_template('seleccionado.html')
    rendered_html = template.render(resultados=resultados)
    response=Response()
    response.text = rendered_html
    return response



def listabebidas():
    try:
        cursor1.execute("SELECT * FROM categorias;")
        lista = cursor1.fetchall()
        env.globals["categoria"] = lista
    except Exception as e:
        print("Error MySQL:", str(e))

def listaproductos():
    try:
        cursor1.execute("select producto.idProducto,producto.nombre,producto.descripcion,categorias.nombre,producto.cantidad,producto.precio from producto inner join categorias on categorias.idcategorias=id_cat_corresp;")
        resultados = cursor1.fetchall()
        env.globals["producto"] = resultados
    except Exception as e:
        print("Error MySQL:", str(e))

app=WhiteNoise(app, root='static/')