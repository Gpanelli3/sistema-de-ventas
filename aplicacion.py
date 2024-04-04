from apiwsgi import Wsgiclass
from whitenoise import WhiteNoise
from jinja2 import Environment, FileSystemLoader #para poder recorrer/cargar/acceder = gestionar a las plantillas
import mysql.connector 
from webob import Request, Response
from wsgiref.simple_server import make_server
import os #para las direcciones de los archivos

#waitress-serve --listen=127.0.0.1:8000 aplicacion:app
#.\env\Scripts\activate

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

conexion1 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="PROGRAMACION2023",
    database="sistemadeventas"
)

cursor1 = conexion1.cursor()

app = Wsgiclass()


@app.ruta("/")
def index(request, response):
    listabebidas()
    listaproductos()
    template = env.get_template('home.html')
    rendered_html = template.render()
    response.text = rendered_html
    return response

@app.ruta("/categ", methods=['GET', 'POST'])
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




