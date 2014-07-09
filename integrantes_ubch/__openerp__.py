{
    'name' : "Integrantes UBCH",
    'category' : "Integrantes UBCH",
    'version' : "1.0",
    'depends' : ['base','l10n_ve_topology'],
    'author' : "Departamento de Desarrollo y Aplicaciones",
    'description' : '''\
     El modulo de Integrnates UBCH permite el manejo y gestion de las personas que forman parte de las UBCH:
			Registro
      Edición
      Generación de Reportes''',
    'data' : [
      "views/integrante.xml",
      "views/grupo_familiar.xml",
      "views/gradoInstruccion.xml",
      "views/profesion.xml",
      "views/ocupacion.xml",
      "views/misiones.xml",
      "views/consejo_comunal.xml",
      "views/archivos_integrantes.xml",
      "views/estadisticas_ubch.xml",
      "views/centro_electoral.xml",
      "data/reg_grados_instruc.xml",
      #"reportes/report_becados.xml",
      #~ "categorias/mantenimiento.xml",
      "seguridad/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #""seguridad/users.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      "seguridad/ir.model.access.csv",
      #"categorias/categorias.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
			#~ "reportes/evaluacion/report_evaluacion.xml", # Reporte para casos de novedad del becado
    ],
    'css': [ 'static/src/css/style.css' ],
}
