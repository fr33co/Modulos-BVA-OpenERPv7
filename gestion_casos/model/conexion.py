#!/usr/bin/python
# -*- encoding: utf-8 -*-
###############Credits#########################################################
#    Finance by: Industrias Diana, C.A. http://www.industriasdiana.gob.ve
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from osv import fields,osv
from tools.translate import _
import MySQLdb
import time
import sys
#~ import psycopg2
#~ import psycopg2.extras
import pprint

#######################################
# Método para la Conexón a base de Datos
#######################################


class gammu_database(osv.osv): # Se declaran los valores usurio, cla
    _name = 'gammu.database' # Metodo de Conexion para el gestor de Gammus
    _description = 'Conexion modelo gammu'

    _columns = {
        'name': fields.char('Name', size=64),
        'gammu_server': fields.char('Server IP', size=64, help="Gammu-smsd Server", required=True),
        'gammu_flag': fields.boolean('Flag', help="The Gammu-smsd server active must have this box checked."),
        'db_type': fields.selection([("mysql","MySQL"),("pgsql","PostgreSQL")], "Database Type", required=True),
        'db_user': fields.char('DB User', size=64, required=True),
        'db_pwd': fields.char('DB Password', size=64, required=True),
        'db_data': fields.char('DB Database', size=64, required=True),
        'status': fields.char('Status',size=64),
    }

    def test_conn(self, cr, uid, ids, context=None): # Testear Conexion con Gammu
        """Parametros de conexion al servidor DB Gammu/Kalkun"""

        obj = self.browse(cr, uid, ids[0])
        obj_model = self.pool.get('ir.model.data')
        db_conn = self.pool.get('gammu.database')
        gammu_database=db_conn.read(cr, uid, ids, ['gammu_server','db_user','db_pwd','db_data','gammu_flag', 'db_type'])
        obj_gammu_database=db_conn.browse(cr, uid, id, context=None)
        for data in self.browse(cr,uid,ids,context=None):
            if data.db_type == 'mysql':
                """ Comprueba conectividad con servidores MySQL """
                try:
                    conn = MySQLdb.connect (host = gammu_database[0]['gammu_server'],
                                            user = gammu_database[0]['db_user'],
                                            passwd = gammu_database[0]['db_pwd'],
                                            db = gammu_database[0]['db_data']);
                    self.write(cr, uid, ids, {'gammu_flag':True,'status':'Servidor Activo'})
                except MySQLdb.Error, e:
                    self.write(cr, uid, ids, {'gammu_flag':False,'status':'Servidor Inactivo'})
            elif data.db_type == 'pgsql':
                """ Comprueba conectividad con servidores PostgreSQL """
                db_c = gammu_database[0]['db_data']
                user_c = gammu_database[0]['db_user']
                host_c = gammu_database[0]['gammu_server']
                passwd_c = gammu_database[0]['db_pwd']
                conn_string = "host='%s' dbname='%s' user='%s' password='%s'"% (host_c, db_c, user_c, passwd_c)
                try:
                    conn = psycopg2.connect(conn_string)
                    cursor = conn.cursor()
                    self.write(cr, uid, ids, {'gammu_flag':True,'status':'Servidor Activo'})
                except:
                    self.write(cr, uid, ids, {'gammu_flag':False,'status':'Servidor Inactivo'})
            else:
                return False

    if __name__ == "__main__":
        sys.exit(main())
                #~ 
gammu_database()


#######################################
# SMS Compose
#######################################


class gammu_compose(osv.osv):
    _name = 'gammu.compose'
    _description = 'Gammu-smsd Compose Message'

    def _get_server(self,cr,uid,context=None):
        res = {}
        server = self.pool.get('gammu.database').search(cr,uid,[('gammu_flag','=',True)])
        if server:
            server_br = self.pool.get('gammu.database').browse(cr,uid,server[0],context=None)
            ret = server_br.id
        else:
            ret = "No hay servidores activos, por favor verificar!"
        return ret


    _columns = {
        'server': fields.many2one('gammu.database', 'SMS Server', required=True),
        'destination_number': fields.char('Destination Number', size=64, required=True, help="Complete el numero telefonico"),
        'destination_group': fields.many2one('res.groups', 'Destination Group'),
        'text_decoded': fields.char('Text Message', size=59, required=True),
        'send_date': fields.date("Send date", required=True),
    }

    _defaults = {
        'send_date': lambda *a: time.strftime('%Y-%m-%d'),
        'destination_number': '+584',
        'server': _get_server,
    }


    def get_dest(self, cr, uid, ids, context):
        """
        Se verifica cual sera la fuente a tomar para los numeros telefonicos.
        """

        obj_hr = self.pool.get('hr.employee')
        res={}
        for sms in self.browse(cr,uid,ids,context=None):
            if sms.destination_group:
                for row in ids:
                    group = self.browse(cr,uid,row,context=context).destination_group.id
                    cr.execute("SELECT uid FROM res_groups_users_rel WHERE gid = %s" %group)
                    members = cr.dictfetchall()
                    member_list = []
                    for n in members:
                        hr_id = obj_hr.search(cr,uid,[('user_id','=',n['uid'])])
                        if hr_id:
                            member_list.append(hr_id[0])
                    destination_number = obj_hr.browse(cr,uid,member_list)
                    for n in destination_number:
                        context.update({
                        'destination_number':  n.mobile_phone,
                        })
                        self.write(cr,uid,ids,{'destination_number' :  n.mobile_phone,}, context=context)
                        send_sing_sms = self.send_sms(cr, uid, ids,context)
                    return True
                return True
            elif len(sms.destination_number) == 13:
                context.update({
                            'destination_number': sms.destination_number,
                        })
                self.write(cr,uid,ids,{'destination_number' : sms.destination_number,}, context=context)
                send_sing_sms = self.send_sms(cr, uid, ids,context)
                return True
            else:
                raise osv.except_osv(_('Alert !'), _('Debe seleccionar un grupo o escribir el formato correcto del número telefonico'))
                return False
                    

    def send_sms(self, cr, uid, ids,context=None):
        """
        Inserccion de registros a las tablas de mayor importancia
        para los envios de sms
        """

        send_date_sms = time.strftime('%Y-%m-%d %H:%M:%S')
        res={}
        for sms in self.browse(cr,uid,ids,context):
            obj = self.browse(cr, uid, ids)
            obj_model = self.pool.get('ir.model.data')
            db_conn = self.pool.get('gammu.database')
            gammu_compose=self.read(cr, uid, ids, ['server', 'destination_number','text_decoded'])[0]
            gammu_database=db_conn.read(cr, uid, [gammu_compose['server'][0]], ['gammu_server','db_user','db_pwd','db_data','db_type'])[0]

            for data in self.browse(cr,uid,ids,context=None):
                if gammu_database['db_type'] == 'mysql':
                    conn = MySQLdb.connect (host = gammu_database['gammu_server'],
                                                        user = gammu_database['db_user'],
                                                        passwd = gammu_database['db_pwd'],
                                                        db = gammu_database['db_data']);
                    cur = conn.cursor()
                elif gammu_database['db_type'] == 'pgsql':
                    host_c = gammu_database['gammu_server']
                    db_c = gammu_database['db_data']
                    user_c = gammu_database['db_user']
                    passwd_c = gammu_database['db_pwd']
                    conn_string = "host='%s' dbname='%s' user='%s' password='%s'"% (host_c, db_c, user_c, passwd_c)
                    conn = psycopg2.connect(conn_string);
                    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                else:
                    return False

            outbox_dict=({"UpdatedInDB": send_date_sms,
                                "InsertIntoDB": send_date_sms,
                                "SendingDateTime": send_date_sms,
                                "DestinationNumber": context['destination_number'],
                                "Coding": 'Default_No_Compression',
                                "Class": '1',
                                "CreatorID": '',
                                "SenderID": '',
                                "TextDecoded": gammu_compose['text_decoded'],
                                "RelativeValidity": '-1',
                                "DeliveryReport": 'default'
                                })

            cur.execute("""INSERT INTO outbox (
                                    UpdatedInDB,
                                    InsertIntoDB,
                                    SendingDateTime,
                                    DestinationNumber,
                                    Coding,
                                    Class,
                                    CreatorID,
                                    SenderID,
                                    TextDecoded,
                                    RelativeValidity,
                                    DeliveryReport)
                                VALUES (
                                    %(UpdatedInDB)s,
                                    %(InsertIntoDB)s,
                                    %(SendingDateTime)s,
                                    %(DestinationNumber)s,
                                    %(Coding)s,
                                    %(Class)s,
                                    %(CreatorID)s,
                                    %(SenderID)s,
                                    %(TextDecoded)s,
                                    %(RelativeValidity)s,
                                    %(DeliveryReport)s);""", outbox_dict)
                                    
            cur = conn.cursor()
            cur.execute("SELECT max(id) as ids FROM outbox")
            rows = cur.fetchone()
            for row in rows:
                print row

            user_outbox_dict = ({"id_outbox":row, 
                                 "id_user":'1'
                                })

            cur = conn.cursor()
            cur.execute("""INSERT INTO user_outbox(
                                    id_outbox,
                                    id_user)
                                VALUES (
                                    %(id_outbox)s,
                                    %(id_user)s);""", user_outbox_dict)

            cur.close()

            conn.close()
        return sms    

gammu_compose()
