from ..fields import snake_case
#from openerp import models, fields, api
from odoo import models, fields, api

__author__ = 'one'


class KanbanView(models.Model):
    _name = 'builder.views.kanban'

    _inherit = ['ir.mixin.polymorphism.subclass']

    _inherits = {
        'builder.ir.ui.view': 'view_id'
    }

    view_id = fields.Many2one('builder.ir.ui.view', string='View', required=True, ondelete='cascade')
    attr_create = fields.Boolean('Allow Create', default=True)
    attr_edit = fields.Boolean('Allow Edit', default=True)
    attr_delete = fields.Boolean('Allow Delete', default=True)
    attr_default_group_by_field_id = fields.Many2one('builder.ir.model.fields', 'Default Group By Field',
                                                     ondelete='set null')
    attr_template = fields.Text('Template', default='    <div t-attf-class="oe_kanban_card oe_kanban_global_click">  \n\
       <div class="row">  \n\
           <div class="col-xs-6">  \n\
               <strong><span><t t-esc="record.partner_id.value"/></span></strong>  \n\
           </div>  \n\
           <div class="col-xs-6 pull-right text-right">  \n\
               <strong><field name="amount_total" widget="monetary"/></strong>  \n\
           </div>  \n\
       </div>  \n\
       <div class="row">  \n\
           <div class="col-xs-6 text-muted">  \n\
               <span><t t-esc="record.name.value"/> <t t-esc="record.date_order.value"/></span>  \n\
           </div>  \n\
           <div class="col-xs-6">  \n\
               <span class="pull-right text-right">  \n\
                   <field name="state" />  \n\
               </span>  \n\
           </div>  \n\
       </div>  \n\
    </div> ')
    attr_quick_create = fields.Boolean('Quick Create', default=True)
    # attr_quick_create = fields.Selection([(1, 'Quick Create'), (2, 'No Quick Create')], 'Quick Create')
    field_ids = fields.Many2many('builder.ir.model.fields', 'builder_view_views_kanban_field_rel', 'view_id',
                                 'field_id', 'Items')
    # field_ids = fields.One2many('builder.views.kanban.field', 'view_id', 'Items')

    _defaults = {
        'type': 'kanban',
        'subclass_model': lambda self: self._name,
#        'subclass_model': lambda s, c, u, cxt=None: s._name,
    }

    @api.model
    def create_instance(self, id):
        self.create({
            'view_id': id,
        })

    @api.multi
    def action_save(self):
#Ashrevert : Next statement by Ash as defaults above not working
        self.type = 'kanban'
        self.subclass_model = 'builder.views.kanban'
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.name = self.model_id.name
        self.xml_id = "view_{snake}_kanban".format(snake=snake_case(self.model_id.model))
        self.model_inherit_type = self.model_id.inherit_type  # shouldn`t be doing that
        self.model_name = self.model_id.model  # shouldn`t be doing that


class KanbanField(models.Model):
    _name = 'builder.views.kanban.field'
    _inherit = 'builder.views.abstract.field'

    view_id = fields.Many2one('builder.views.kanban', string='View', ondelete='cascade')
    invisible = fields.Boolean('Invisible')
