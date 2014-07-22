{
    'name' : "Tesoreria",
    'category' : "Tesoreria",
    'version' : "1.0",
    'depends' : ['base','l10n_ve_topology'],
    'author' : "José Solorzano - Departamento de Desarrollo y Aplicaciones - AC. Bibliotecas Virtuales de Aragua",
    'description' : '''\
     El modulo de Tesorería permite el manejo y gestión de emisiones de cheques y ordenes de pagos para los beneficiarios y proveedores de la institución:
			Registro
      Edición
      Generación de Reportes''',
    'data' : [
      "views/beneficiario.xml",
      "views/bancos.xml",
      "views/cuentas.xml",
      "views/anyo_fiscal.xml",
      #~ "data/reg_grados_instruc.xml",
      #"reportes/report_becados.xml",
      #~ "categorias/mantenimiento.xml",
      #~ "seguridad/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #""seguridad/users.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #~ "seguridad/ir.model.access.csv",
      #"categorias/categorias.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
			#~ "reportes/evaluacion/report_evaluacion.xml", # Reporte para casos de novedad del becado
    ],
    'css': [ 'static/src/css/style.css' ],
}
