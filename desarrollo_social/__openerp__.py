{
    'name' : "Desarrollo Social",
    'category' : "Desarrollo Social",
    'version' : "1.0",
    'depends' : ['hr','hr_payroll'],
    'author' : "Desarrollo y Aplicaciones",
    'description' : '''\
     El modulo de Desarrollo Social permite el manejo y gestion de los becados de las diferentes Bibliotecas Virtuales de Aragua:
			Registro
      Edicion
      Generación de Reportes
			Generación de Nóminas''',
    'data' : [
      "views/becado.xml",
      "views/nomina.xml",
      "views/carga_familiar.xml",
      "seguridad/groups.xml",
      #"seguridad/permisos.csv",
      "categorias/categorias.xml",
    ],
}
