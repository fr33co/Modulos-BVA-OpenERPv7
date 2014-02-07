{
    'name' : "Recursos Humanos",
    'category' : "Recursos Humanos",
    'version' : "1.0",
    'depends' : ['base','hr','hr_payroll','hr_recruitment','hr_contract','hr_holidays','l10n_ve_topology'],
    'author' : "Ing en Sistemas: Jesús G. Laya R",
    'description' : '''\
     El módulo de Recursos Humanos permite el manejo y gestion de los Empleados de las diferentes Bibliotecas Virtuales de Aragua Nota: Depende de Desarrollo Social:
			Registro
      Edicion
      Generación de Reportes
			Generación de Nóminas'
      Generación de archivos TXT''',
    'data' : [
      "views/empleado.xml",
      #"views/seguridad_salud_laboral.xml",
      'categorias/groups.xml',
      'categorias/script_load.xml',
      # "views/nomina.xml", # nómina
      # "views/proceso_nomina.xml", # Procesos de nóminas
      "views/contrato.xml",
      "views/concepts.xml",
      # "views/proceso_seleccion.xml",

      # "views/tipoNomina.xml",
      # "views/carga_familiar.xml",
      # "views/clasPer.xml",
      # "views/tipoEmp.xml",
      # "views/gradoInstruccion.xml",
      # "views/grupoSanguineo.xml",
      # "views/sedes.xml",
      # "views/areas.xml",
      # "views/tipo_beca.xml",
      # "views/status.xml",
      # "views/novedades.xml",


      # "views/evaluacion.xml",
      #"reportes/report_becados.xml",
      #"seguridad/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #"seguridad/users.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #"seguridad/ir.model.access.csv",
      #"categorias/categorias.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
			# "reportes/evaluacion/report_evaluacion.xml", # Reporte para casos de novedad del becado
   #    "reportes/novedad/report_becados.xml", # Reporte para casos de novedad del becado
   #    "reportes/constancia/constancia.xml", # Reporte para la emisión de constancia
    ],
    'css': [ 'static/src/css/style.css' ],
}
