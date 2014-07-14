{
    'name' : "Gestión de Eventos",
    'category' : "Gestión de Eventos",
    'version' : "2.0",
    'depends' : ['base','l10n_ve_topology'],
    'author' : "Ing en Sistemas: Jesús G. Laya R",
    'description' : '''
     El módulo de Gestión de Eventos, permite gestionar las Actividades Programadas durante la Semana, asi como actividades Especiales para la Gobernación del Estado Aragua
      Edicion
      Gestión de Eventos
      Ultima Actualización: 12 de Julio del 2014''',
    'data' : [
      "views/gestion_eventos.xml", # Gestion de eventos
      "views/institucion_gerencia.xml", # Institucion / Gerencia
      "views/gestion_documento.xml", # Gestion de Documentos
      "views/recurso_logistico.xml",
      "views/usuario_gerencia.xml", # Usuario por Gerencia
      "views/wizard_filtro.xml", # Vista para filtrado de Eventos
      "script/script.xml", # Script de carga de data
      "script/sedes.xml", # Script Sedes
      "script/ejes.xml", # Script Ejes
      "segurity/eje/ir.model.access.csv", # Seguidad para eje
      "segurity/eventos/ir.model.access.csv", # Seguidad para eventos
      "segurity/sede/ir.model.access.csv", # Seguidad para sede
      "foto/foto.xml", # Evento por Foto
      "individual/individual.xml", # Evento Individual
    ],
    'css': [ 'static/src/css/style.css' ],
}
