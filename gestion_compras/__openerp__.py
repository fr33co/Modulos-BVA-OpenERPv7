# -*- coding: utf-8 -*-
{
    'name' : "Gestión de Compras",
    'category' : "Gestión de Compras",
    'version' : "1.0",
    'depends' : ['base','l10n_ve_topology','materiales_almacen','presupuesto'],
    'author' : "Ing en Sistemas: Jesús G. Laya R, Gerencia de Desarrollo y Aplicaciones (2014)",
    'description' : '''
     El módulo de Gestión de Compras, permite el manejo de los compromisos Presupuestarios de una Institución
      Edicion
      Gestión de Compras
      Ultima Actualización: 11 de Septiembre del 2014''',
    'data' : [
      "views/cotizacion/cotizacion.xml", # Gestion de Compras
      #~ "views/solicitud/solicitud.xml", # Proceso de Solicitud de Materiales y o Servicios
      "views/compras_documento/compras_documento.xml", # Documentos Adjuntos sobre Compras
      "views/entrada_materiales/entrada_materiales.xml", # Entrada de Materiales para la carga de partidas Presupuestaria parta el proceso de Compras
      "views/orden_compra/orden_compra.xml", # Orden de compras
      "views/analisis_precios/analisis_precios.xml", # Vista para el analisis de Precios de los Productos y o Servicios
      "views/proveedor/proveedor.xml", # Proveedores
      #~ "views/wizard/wizard_busqueda.xml", # Proceso de filtrado de datos
      "views/control_perceptivo/control_perceptivo.xml",
      "script/script.xml",
      "groups/groups.xml",
      "segurity/ir.model.access.csv",
    ],
    'css': [ 'static/src/css/style.css' ],
}
