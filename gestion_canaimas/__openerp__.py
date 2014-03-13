# -*- coding: utf-8 -*-
{
    'name' : "Solicitud y Soporte Técnico de Canaimitas",
    'category' : "Others",
    'version' :  "1.0",
    'depends' : ['base', 'l10n_ve_topology'],
    'autor' : "Marcel Arcuri, Angel Guadarrama & A.C. Bibliotecas Virtuales de Aragua", 
    'description' : """\
        Modulo para la gestión de las solicitudes y soporte técnico para Canaimitas""",
    'data': [
        'data/tipos_grados_modelos.xml',
        'view/solicitud_soporte.xml',
        'report/reporte_soporte.xml',
        'view/solicitud_reparacion.xml',
        #'view/grafico_status.xml',
        'view/grafico_modelo.xml',
        #'view/grafico_municipio_solicitante.xml',
        'view/tipos_grados_modelos_view.xml',
        #'view/escuelas_aragua.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',

        ],
}
