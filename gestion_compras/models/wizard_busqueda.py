# -*- coding: utf-8 -*-

import urllib2, urllib
import time
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval
#####################################################
#from fpdf import FPDF # Importar la libreria pdf
#import fpdf # Importar la libreria pdf
####################################################
from openerp.osv import fields, osv
import base64 #Necesario para la generaci?n del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generaci?n del .xsl
import xlwt
import netsvc
import tools
import logging
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import commands
import math


from openerp.osv import osv, fields

class Proceso_busqueda(osv.osv_memory):
    
    _name="wizard.busqueda"
    # _order = 'cantidad'
    
    # _rec_name = 'cantidad'

    #################################################################
    _columns = {

        'desde': fields.datetime(string="Desde", required = False),
        'hasta': fields.datetime(string="Hasta", required = False),
				#'targeta' : fields.boolean(string="Targeta"),
				#'recarga' : fields.boolean(string="Recarga"),
				#'constancia' : fields.boolean(string="Constancia"),
				#'class_personal_targeta' : fields.many2one("becados.clasper", "Personal", required = False),
				#'class_personal_recarga' : fields.many2one("becados.clasper", "Personal", required = False),
				#'alim_ids' : fields.many2many("hr.ticket","proceso_targeta","id_model","id_targeta","Targeta",required=False),
				#'recarga_ids' : fields.many2many("hr.ticket","proceso_recarga","id_model","id_recarga","Recarga",required=False),
						
    }

    _defaults = {
        
    }
    
