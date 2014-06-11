{
    'name' : "Recursos Humanos",
    'category' : "Recursos Humanos",
    'version' : "9.1",
    'depends' : ['base','hr','hr_payroll','hr_recruitment','hr_contract','hr_holidays','l10n_ve_topology','desarrollo_social','account','presupuesto'],
    'author' : "Ing en Sistemas: Jesús G. Laya R",
    'description' : '''
     El módulo de Recursos Humanos permite el manejo y gestión de los Empleados de las diferentes Bibliotecas Virtuales de Aragua Nota: Depende de Desarrollo Social:
			Registro
      Edicion
      Generación de Reportes
			Generación de Nóminas'
      Generación de archivos TXT
      Ultima Actualización: 09 de Junio del 2014''',
    'data' : [
      "views/empleado.xml",
      #"views/seguridad_salud_laboral.xml",
      # 'categorias/groups.xml',
      'categorias/script_load.xml',
      'categorias/script_concepts.xml', #Scrit para concentos
      'categorias/data_partida.xml', #Script para la carga de partidas
      "views/nomina.xml", # nómina
      "views/proceso_nomina.xml", # Procesos de nóminas
      "views/contrato.xml",
      "views/selection.xml",
      "views/concepts.xml",
      "views/profesion_oficio.xml",
      "views/degree.xml",
      "views/change_status.xml",
      "views/change_salary_employee.xml",
      #"views/onchange_slip.xml",
      "views/hr_departament.xml",
      "views/hr_bank.xml",
      "views/payslip.xml",
      "views/hr_document.xml", # Sub modulo de ir_attachment_employee (Documentos adjuntos
      "views/update_employee.xml",
      "views/shuttle_ascent_employee.xml",
      "views/charge.xml",
      "views/movement_employee.xml",
      "views/asignacion_nomina_regular.xml", # Nomina regular
      "views/asignacion_nomina_vacaciones.xml", # Nomina vacaciones
      "views/configuracion_asignacion.xml",
      "views/propietario.xml",

      # "views/tipoNomina.xml",
      "views/carga_familiar_employee.xml",

      "categorias/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #"script/departamentos.xml",
      #"segurity/acceso.csv", # PRIVILEGIOS PARA LOS MODELOS
      # "segurity/ir.view.access.csv", # PRIVILEGIOS PARA LAS VISTAS
      #"reportes/constancia/constancia.xml", # Reporte para la emisión de constancia
      #"reportes/candidato/candidato.xml", # Reporte para la emisión de candidato
    ],
    'css': [ 'static/src/css/style.css' ],
}
