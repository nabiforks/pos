# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
try:
    from num2words import num2words
except ImportError:
    raise ValidationError('In order to proceed, please install python module called `num2words`.\n How to install the latest version in Linux/UNIX or Windows System:\n 1. Download it from https://github. com/savoirfairelinux/num2words \n 2. Unzip the downloaded file\n 3. Change directory to the unziped `num2words` folder  and run this command: "python setup.py install"\n')

class SO(models.Model):
	_inherit=["sale.order"]

        @api.onchange('partner_id')
        def onchange_partner_style(self):
            self.style = self.partner_id.style or self.env.user.company_id.default_style or self.env.ref('professional_templates.default_style_for_all_reports').id

        style = fields.Many2one('report.template.settings', 'Quote/Order Style', help="Select Style to use when printing the Sales Order or Quote", default= lambda self: self.partner_id.style or self.env.user.company_id.default_style)	
        project_title = fields.Char('Title', help="The title of your customer project or work you are doing for your customer")
        amount_words= fields.Char('Amount in Words:', help="The total amount in words is automatically generated by the system..few languages are supported currently", compute='_compute_num2words')

        @api.one
        def _compute_num2words(self):
            try:
                self.amount_words = (num2words(self.amount_total, lang=self.partner_id.lang) + ' ' + (self.currency_id.currency_name or '')).upper()
            except NotImplementedError:
                self.amount_words = (num2words(self.amount_total, lang='en') + ' ' + (self.currency_id.currency_name or '')).upper()

	##Override print_quotation method in sale module
	@api.multi
	def print_quotation(self):
            """ Method called when print button is clicked 
	       This Method overrides the one in the original sale module
            """
            self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
            return self.env['report'].get_action(self, 'professional_templates.sale_order')

