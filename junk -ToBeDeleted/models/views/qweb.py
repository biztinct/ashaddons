from ..fields import snake_case
#from openerp import models, fields, api
from odoo import models, fields, api

__author__ = 'one'

# All of the cod ebelow is written in the same format as that of kanban view

class QwebView(models.Model):
    _name = 'builder.views.qweb'

    _inherit = ['ir.mixin.polymorphism.subclass']

    _inherits = {
        'builder.ir.ui.view': 'view_id'
    }

    view_id = fields.Many2one('builder.ir.ui.view', string='View', required=True, ondelete='cascade')
    attr_create = fields.Boolean('Allow Create', default=True)
    attr_edit = fields.Boolean('Allow Edit', default=True)
    attr_delete = fields.Boolean('Allow Delete', default=True)
    attr_mail = fields.Boolean('Mail Template', default=False)
    email_from = fields.Char('Email From', default="${(object.user_id.email and '%s &lt;%s&gt;' % (object.user_id.name, object.user_id.email) or '')|safe}")
    subject = fields.Char('Subject' )
    email_to = fields.Char('Email To', default="${(object.user_id.email and '%s &lt;%s&gt;' % (object.user_id.name, object.user_id.email) or '')|safe}")
    partner_to = fields.Char('Partner To', default='${object.partner_id.id}' )
    auto_delete = fields.Boolean('Auto Delete', default=True)
    report_template = fields.Many2one('builder.ir.ui.view', string='Report Template')
    report_name = fields.Char('Report Name', default="${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}")
    lang = fields.Char('Language', default='${object.partner_id.lang}' )
    attr_default_group_by_field_id = fields.Many2one('builder.ir.model.fields', 'Default Group By Field',
                                                     ondelete='set null')
    attr_template = fields.Text('Template', default='<t t-call="report.external_layout"> \n\
    <div class="page"> \n\
       <h1>Report For <t t-esc="doc.streetaddress"/> <t t-esc="doc.suburb"/></h1> \n\
          <table> \n\
           <tr> \n\
              <th>Property ID</th> \n\
              <th>Visit Type</th> \n\
              <th>Date</th> \n\
           </tr> \n\
           <t t-foreach="doc.visit_ids" t-as="o"> \n\
               <tr> \n\
                   <td><t t-esc="o.property_id.title"/></td> \n\
                   <td><t t-esc="o.visittype"/></td> \n\
                   <td><t t-esc="o.startdate"/></td> \n\
               </tr> \n\
           </t> \n\
          </table> \n\
     </div> \n\
 </t>')
    attr_mailtemplate = fields.Text('Mail Template', default='<![CDATA[ \n\
<p>Dear ${object.partner_id.name} \n\
% set access_action = object.get_access_action() \n\
% set doc_name = \'quotation\' if object.state in (\'draft\', \'sent\') else \'order confirmation\' \n\
% set is_online = access_action and access_action[\'type\'] == \'ir.actions.act_url\' \n\
% set access_name = is_online and object.template_id and \'Accept and pay %s online\' % doc_name or \'View %s\' % doc_name \n\
% set access_url = is_online and access_action[\'url\'] or object.get_signup_url() \n\
 \n\
% if object.partner_id.parent_id: \n\
    (<i>${object.partner_id.parent_id.name}</i>) \n\
% endif \n\
,</p> \n\
<p> \n\
Here is your ${doc_name} <strong>${object.name}</strong> \n\
% if object.origin: \n\
(with reference: ${object.origin} ) \n\
% endif \n\
amounting in <strong>${object.amount_total} ${object.pricelist_id.currency_id.name}</strong> \n\
from ${object.company_id.name}. \n\
</p> \n\
 \n\
    <br/><br/> \n\
% if is_online: \n\
    <center> \n\
        <a href="${access_url}" style="background-color: #1abc9c; padding: 20px; text-decoration: none; color: #fff; border-radius: 5px; font-size: 16px;" class="o_default_snippet_text">${access_name}</a> \n\
        <br/><br/> \n\
        <span style="color:#888888">(or view attached PDF)</span> \n\
    </center> \n\
    <br/> \n\
% endif \n\
 \n\
<p>You can reply to this email if you have any questions.</p> \n\
<p>Thank you,</p> \n\
 \n\
<p style="color:#eeeeee;"> \n\
% if object.user_id and object.user_id.signature: \n\
    ${object.user_id.signature | safe} \n\
% endif \n\
</p> \n\
]]> ')
    attr_quick_create = fields.Boolean('Quick Create', default=True)
    # attr_quick_create = fields.Selection([(1, 'Quick Create'), (2, 'No Quick Create')], 'Quick Create')
    field_ids = fields.Many2many('builder.ir.model.fields', 'builder_view_views_qweb_field_rel', 'view_id',
                                 'field_id', 'Items')

    _defaults = {
        'type': 'qweb',
        'subclass_model': lambda self: self._name,
#Ashrevert        'subclass_model': lambda s, c, u, cxt=None: s._name,
    }

    @api.model
    def create_instance(self, id):
        self.create({
            'view_id': id,
        })

    @api.multi
    def action_save(self):
#Ashrevert : Next statement by Ash as defaults above not working
        self.type = 'qweb'
        self.subclass_model = 'builder.views.qweb'
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.name = self.model_id.name
        self.xml_id = "view_{snake}_qweb".format(snake=snake_case(self.model_id.model))
        self.model_inherit_type = self.model_id.inherit_type  # shouldn`t be doing that
        self.model_name = self.model_id.model  # shouldn`t be doing that


class QwebField(models.Model):
    _name = 'builder.views.qweb.field'
    _inherit = 'builder.views.abstract.field'

    view_id = fields.Many2one('builder.views.qweb', string='View', ondelete='cascade')
    invisible = fields.Boolean('Invisible')
