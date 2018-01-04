#from openerp import models, fields, api, pooler
#from openerp.api import Environment
from odoo import models, fields, api
from odoo.api import Environment
#from pudb import set_trace;

__author__ = 'deimos'


class Superclass(models.AbstractModel):
    _name = 'ir.mixin.polymorphism.superclass'

    subclass_id = fields.Integer('Subclass ID', compute='_compute_res_id')
#    subclass_model = fields.Char("Subclass Model", required=True)
    subclass_model = fields.Char("Subclass Model", default=lambda self: self._name, required=True)

#    _defaults = {
#        'subclass_model': lambda s, c, u, cxt=None: s._name
#    }

    @api.one
    def _compute_res_id(self):
#        set_trace()
#Ashrevert        if self.subclass_model == self._model._name:
        if self.subclass_model == self._name:
            self.subclass_id = self.id
        else:
            subclass_model = self.env[self.subclass_model]
#Ashrevert            attr = subclass_model._inherits.get(self._model._name)
            attr = subclass_model._inherits.get(self._name)
            if attr:
                self.subclass_id = subclass_model.search([
                    (attr, '=', self.id)
                ]).id
            else:
                self.subclass_id = self.id

    # def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
    #     record = self.browse(cr, uid, 2, context=context)
    #     if self._name == record.subclass_model:
    #         view = super(Superclass, self).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar, submenu=submenu)
    #     else:
    #         view = self.pool.get(record.subclass_model).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar, submenu=submenu)
    #     return view

    @api.multi
    def get_formview_action(self):
#    def get_formview_action(self,id):
#    def get_formview_action(self, cr, uid, id, context=None):
        """
        @return <ir.actions.act_window>
        """
#        set_trace()
#Ashrevert        record = self.browse(cr, uid, id, context=context)[0]
#        record = self.browse()
        record = self
        if not record.subclass_model:
#            return super(Superclass, self).get_formview_action(cr, uid, id, context=context)
            return super(Superclass, self).get_formview_action()

#        set_trace()
        create_instance = False
        # try:
        if not record.subclass_id:
            create_instance = True
        # except:
        #     create_instance = True

        if create_instance:
#Ashrevert            env = Environment(cr, uid, context)
#Ashrevert           self.env[record.subclass_model].create_instance(id[0] if isinstance(id, list) else id)
           self.env[record.subclass_model].create_instance(self.id)
        if self._name == record.subclass_model:
#Ashrevert            view = super(Superclass, self).get_formview_action(cr, uid, id, context=context)
#            view = super(Superclass, self).get_formview_action(self.id)
            view = super(Superclass, self).get_formview_action()
        else:
#            view = self.env[record.subclass_model].get_formview_action()
            view = self.env[record.subclass_model].browse(record.subclass_id).get_formview_action()
#Ashrevert            view = self.pool.get(record.subclass_model).get_formview_action(cr, uid, record.subclass_id,
#Ashrevert                                                                            context=context)
        return view

    @api.one
    def get_instance(self):
        return self.env[self.subclass_model].browse(self.subclass_id)

    @property
    def instance(self):
        return self.env[self.subclass_model].browse(self.subclass_id)

#    @api.model
#    def create_instance(self, id):
#        raise NotImplementedError

    @api.multi
    def action_edit(self):
        cr, uid, cxt = self.env.args
#Ashrevert        data = self._model.get_formview_action(cr, uid, self.id, context=cxt)
        data = self.get_formview_action(self.id)
        return data


class Subclass(models.AbstractModel):
    _name = 'ir.mixin.polymorphism.subclass'

#Ashrevert    def get_formview_id(self, cr, uid, id, context=None):
    @api.multi
    def get_formview_id(self):
#        set_trace()
#Ashrevert        view = self.pool.get('ir.ui.view').search(cr, uid, [
        view = self.env['ir.ui.view'].search([
            ('type', '=', 'form'),
            ('model', '=', self._name)
#Ashrevert        ], context=context)
        ])
#Ashrevert        return view[0] if len(view) else False
        return view.id if view.id else False

    def unlink(self, cr, uid, ids, context=None):
        records = self.browse(cr, uid, ids, context=context)
        parent_ids = {
            model: [rec[field].id for rec in records] for model, field in self._inherits.items()
        }

        res = super(Subclass, self).unlink(cr, uid, ids, context=context)
        if res:
            for model in parent_ids:
                self.pool.get(model).unlink(cr, uid, parent_ids.get(model, []), context=context)
        return res
