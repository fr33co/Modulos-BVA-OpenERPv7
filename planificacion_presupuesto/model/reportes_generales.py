# -*- coding: utf-8 -*-
import hashlib
import itertools
import logging
import os
import re

from openerp import tools
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class reportes_generales(osv.osv):
    """Attachments are used to link binary files or url to any openerp document.

    External attachment storage
    ---------------------------
    
    The 'data' function field (_data_get,data_set) is implemented using
    _file_read, _file_write and _file_delete which can be overridden to
    implement other storage engines, shuch methods should check for other
    location pseudo uri (example: hdfs://hadoppserver)
    
    The default implementation is the file:dirname location that stores files
    on the local filesystem using name based on their sha1 hash
    """
    def _name_get_resname(self, cr, uid, ids, object, method, context):
        data = {}
        for attachment in self.browse(cr, uid, ids, context=context):
            model_object = attachment.res_model
            res_id = attachment.res_id
            if model_object and res_id:
                model_pool = self.pool.get(model_object)
                res = model_pool.name_get(cr,uid,[res_id],context)
                res_name = res and res[0][1] or False
                if res_name:
                    field = self._columns.get('res_name',False)
                    if field and len(res_name) > field.size:
                        res_name = res_name[:field.size-3] + '...' 
                data[attachment.id] = res_name
            else:
                data[attachment.id] = False
        return data

    # 'data' field implementation
    def _full_path(self, cr, uid, location, path):
        # location = 'file:filestore'
        assert location.startswith('file:'), "Unhandled filestore location %s" % location
        location = location[5:]

        # sanitize location name and path
        location = re.sub('[.]','',location)
        location = location.strip('/\\')

        path = re.sub('[.]','',path)
        path = path.strip('/\\')
        return os.path.join(tools.config['root_path'], location, cr.dbname, path)

    def _file_read(self, cr, uid, location, fname, bin_size=False):
        full_path = self._full_path(cr, uid, location, fname)
        r = ''
        try:
            if bin_size:
                r = os.path.getsize(full_path)
            else:
                r = open(full_path,'rb').read().encode('base64')
        except IOError:
            _logger.error("_read_file reading %s",full_path)
        return r

    def _file_write(self, cr, uid, location, value):
        bin_value = value.decode('base64')
        fname = hashlib.sha1(bin_value).hexdigest()
        # scatter files across 1024 dirs
        # we use '/' in the db (even on windows)
        fname = fname[:3] + '/' + fname
        full_path = self._full_path(cr, uid, location, fname)
        try:
            dirname = os.path.dirname(full_path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            open(full_path,'wb').write(bin_value)
        except IOError:
            _logger.error("_file_write writing %s",full_path)
        return fname

    def _file_delete(self, cr, uid, location, fname):
        count = self.search(cr, 1, [('store_fname','=',fname)], count=True)
        if count <= 1:
            full_path = self._full_path(cr, uid, location, fname)
            try:
                os.unlink(full_path)
            except OSError:
                _logger.error("_file_delete could not unlink %s",full_path)
            except IOError:
                # Harmless and needed for race conditions
                _logger.error("_file_delete could not unlink %s",full_path)

    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            if location and attach.store_fname:
                result[attach.id] = self._file_read(cr, uid, location, attach.store_fname, bin_size)
            else:
                result[attach.id] = attach.db_datas
        return result

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        # We dont handle setting data to null
        if not value:
            return True
        if context is None:
            context = {}
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(cr, uid, id, context=context)
            if attach.store_fname:
                self._file_delete(cr, uid, location, attach.store_fname)
            fname = self._file_write(cr, uid, location, value)
            # SUPERUSER_ID as probably don't have write access, trigger during create
            super(reportes_generales, self).write(cr, SUPERUSER_ID, [id], {'store_fname': fname, 'file_size': file_size}, context=context)
        else:
            super(reportes_generales, self).write(cr, SUPERUSER_ID, [id], {'db_datas': value, 'file_size': file_size}, context=context)
        return True

    _name = 'reportes.generales'
    _columns = {
        'name': fields.char('Nombre de Referencia',size=256, required=True),
        'datas_fname': fields.char('Nombre del Archivo',size=256),
        'description': fields.text('Descripción'),
        'res_name': fields.function(_name_get_resname, type='char', size=128, string='Nombre del Recurso', store=True),
        'res_model': fields.char('Modulo relacionado',size=64, readonly=True, help="El objeto en la base al cual se le adjuntará"),
        'res_id': fields.integer('ID', readonly=True, help="La ID de registro se adjunta a este"),
        'create_date': fields.datetime('Fecha de creación', readonly=True),
        'create_uid':  fields.many2one('res.users', 'Registrado por', readonly=True),
        'company_id': fields.many2one('res.company', 'Compañia', change_default=True),
        'type': fields.selection( [ ('url','URL'), ('binary','Binario'), ],
                'Tipo de archivo', help="Archivo de tipo Binario or URL", required=True, change_default=True),
        'url': fields.char('Url', size=1024),
        # al: We keep shitty field names for backward compatibility with document
        'datas': fields.function(_data_get, fnct_inv=_data_set, string='Contenido del Archivo', type="binary", nodrop=True),
        'store_fname': fields.char('Nombre del archivo almacenado', size=256),
        'db_datas': fields.binary('Data de base de datos'),
        'file_size': fields.integer('Tamaño del archivo'),
        'registro': fields.char('Registro de:',size=50),
    }

    _defaults = {
        'type': 'binary',
        'file_size': 0,
        'company_id': lambda s,cr,uid,c: s.pool.get('res.company')._company_default_get(cr, uid, 'reportes.generales', context=c),
    }

    def _auto_init(self, cr, context=None):
        super(reportes_generales, self)._auto_init(cr, context)
        cr.execute('SELECT indexname FROM pg_indexes WHERE indexname = %s', ('ir_attachment_res_idx',))
        if not cr.fetchone():
            cr.execute('CREATE INDEX ir_attachment_res_idx ON reportes_generales (res_model, res_id)')
            cr.commit()

    def check(self, cr, uid, ids, mode, context=None, values=None):
        """Restricts the access to an reportes_generales , according to referred model
        In the 'document' module, it is overriden to relax this hard rule, since
        more complex ones apply there.
        """
        res_ids = {}
        if ids:
            if isinstance(ids, (int, long)):
                ids = [ids]
            cr.execute('SELECT DISTINCT res_model, res_id FROM reportes_generales WHERE id = ANY (%s)', (ids,))
            for rmod, rid in cr.fetchall():
                if not (rmod and rid):
                    continue
                res_ids.setdefault(rmod,set()).add(rid)
        if values:
            if values.get('res_model') and values.get('res_id'):
                res_ids.setdefault(values['res_model'],set()).add(values['res_id'])

        ima = self.pool.get('ir.model.access')
        for model, mids in res_ids.items():
            # ignore attachments that are not attached to a resource anymore when checking access rights
            # (resource was deleted but attachment was not)
            mids = self.pool.get(model).exists(cr, uid, mids)
            ima.check(cr, uid, model, mode)
            self.pool.get(model).check_access_rule(cr, uid, mids, mode, context=context)

    def _search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False, access_rights_uid=None):
        ids = super(reportes_generales, self)._search(cr, uid, args, offset=offset,
                                                 limit=limit, order=order,
                                                 context=context, count=False,
                                                 access_rights_uid=access_rights_uid)
        if not ids:
            if count:
                return 0
            return []

        # Work with a set, as list.remove() is prohibitive for large lists of documents
        # (takes 20+ seconds on a db with 100k docs during search_count()!)
        orig_ids = ids
        ids = set(ids)

        # For attachments, the permissions of the document they are attached to
        # apply, so we must remove attachments for which the user cannot access
        # the linked document.
        # Use pure SQL rather than read() as it is about 50% faster for large dbs (100k+ docs),
        # and the permissions are checked in super() and below anyway.
        cr.execute("""SELECT id, res_model, res_id FROM reportes_generales WHERE id = ANY(%s)""", (list(ids),))
        targets = cr.dictfetchall()
        model_attachments = {}
        for target_dict in targets:
            if not (target_dict['res_id'] and target_dict['res_model']):
                continue
            # model_attachments = { 'model': { 'res_id': [id1,id2] } }
            model_attachments.setdefault(target_dict['res_model'],{}).setdefault(target_dict['res_id'],set()).add(target_dict['id'])

        # To avoid multiple queries for each attachment found, checks are
        # performed in batch as much as possible.
        ima = self.pool.get('ir.model.access')
        for model, targets in model_attachments.iteritems():
            if not self.pool.get(model):
                continue
            if not ima.check(cr, uid, model, 'read', False):
                # remove all corresponding attachment ids
                for attach_id in itertools.chain(*targets.values()):
                    ids.remove(attach_id)
                continue # skip ir.rule processing, these ones are out already

            # filter ids according to what access rules permit
            target_ids = targets.keys()
            allowed_ids = self.pool.get(model).search(cr, uid, [('id', 'in', target_ids)], context=context)
            disallowed_ids = set(target_ids).difference(allowed_ids)
            for res_id in disallowed_ids:
                for attach_id in targets[res_id]:
                    ids.remove(attach_id)

        # sort result according to the original sort ordering
        result = [id for id in orig_ids if id in ids]
        return len(result) if count else list(result)

    def read(self, cr, uid, ids, fields_to_read=None, context=None, load='_classic_read'):
        if isinstance(ids, (int, long)):
            ids = [ids]
        self.check(cr, uid, ids, 'read', context=context)
        return super(reportes_generales, self).read(cr, uid, ids, fields_to_read, context, load)

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        self.check(cr, uid, ids, 'write', context=context, values=vals)
        if 'file_size' in vals:
            del vals['file_size']
        return super(reportes_generales, self).write(cr, uid, ids, vals, context)

    def copy(self, cr, uid, id, default=None, context=None):
        self.check(cr, uid, [id], 'write', context=context)
        return super(reportes_generales, self).copy(cr, uid, id, default, context)

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        self.check(cr, uid, ids, 'unlink', context=context)
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
        if location:
            for attach in self.browse(cr, uid, ids, context=context):
                if attach.store_fname:
                    self._file_delete(cr, uid, location, attach.store_fname)
        return super(reportes_generales, self).unlink(cr, uid, ids, context)

    def create(self, cr, uid, values, context=None):
        self.check(cr, uid, [], mode='write', context=context, values=values)
        if 'file_size' in values:
            del values['file_size']
        return super(reportes_generales, self).create(cr, uid, values, context)

    def action_get(self, cr, uid, context=None):
        return self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'base', 'action_attachment', context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
