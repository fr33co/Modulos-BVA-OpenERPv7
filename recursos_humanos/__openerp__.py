{
    'name' : "Recursos Humanos",
    'category' : "Recursos Humanos",
    'version' : "6.1",
    'depends' : ['base','hr','hr_payroll','hr_recruitment','hr_contract','hr_holidays','l10n_ve_topology','desarrollo_social'],
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
      # 'categorias/groups.xml',
      'categorias/script_load.xml',
      # "views/nomina.xml", # nómina
      # "views/proceso_nomina.xml", # Procesos de nóminas
      "views/contrato.xml",
      "views/selection.xml",
      "views/concepts.xml",
      "views/profesion_oficio.xml",
      "views/degree.xml",
      "views/change_status.xml",
      # "views/proceso_seleccion.xml",

      # "views/tipoNomina.xml",
      "views/carga_familiar_employee.xml",
      # "views/clasPer.xml",
      # "views/tipoEmp.xml",
      # "views/gradoInstruccion.xml",
      # "views/grupoSanguineo.xml",
      # "views/sedes.xml",
      # "views/areas.xml",
      # "views/tipo_beca.xml",
      # "views/status.xml",
      # "views/novedades.xml",


      
      "segurity/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      # "segurity/acceso.csv", # PRIVILEGIOS PARA LOS MODELOS
      # "segurity/ir.view.access.csv", # PRIVILEGIOS PARA LAS VISTAS
      "reportes/constancia/constancia.xml", # Reporte para la emisión de constancia
    ],
    'css': [ 'static/src/css/style.css' ],
}
