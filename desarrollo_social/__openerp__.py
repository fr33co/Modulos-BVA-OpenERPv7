{
    'name' : "Desarrollo Social",
    'category' : "Desarrollo Social",
    'version' : "1.0",
    'depends' : ['base','hr','hr_payroll','hr_recruitment','hr_contract'],
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
      "views/tipoNomina.xml",
      "views/carga_familiar.xml",
      "views/clasPer.xml",
      "views/tipoEmp.xml",
      "views/gradoInstruccion.xml",
      "views/grupoSanguineo.xml",
      "views/sedes.xml",
      "views/areas.xml",
      "views/novedades.xml",
      "views/proceso_seleccion.xml",
      "views/contrato.xml",
      "views/evaluacion.xml",
      #"reportes/report_becados.xml",
      #"seguridad/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #"seguridad/permisos.csv", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #"categorias/categorias.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
    ],
}
