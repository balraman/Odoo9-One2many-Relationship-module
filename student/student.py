import time
from openerp import api, models, fields, _
from openerp.exceptions import UserError, ValidationError
import openerp.addons.decimal_precision as dp
import re
import datetime
import logging
_logger = logging.getLogger(__name__)

class Student(models.Model):
	_name = 'student.detail'

	name = fields.Char('Name', required=True)
	street = fields.Char('Street')
	street2 = fields.Char('Street2')
	zip_code = fields.Char('Zip', size=24)
	city = fields.Char('City')
	state_id = fields.Many2one('res.country.state', string='State')
	country_id = fields.Many2one('res.country', string='Country')
	education = fields.Char('Education')
	mark_lines = fields.One2many('student.marks','mark_id', 'Student Marks')
	
	@api.multi
	def onchange_state(self, state_id):
		if state_id:
			state = self.env['res.country.state'].browse(state_id)
			return {'value': {'country_id': state.country_id.id}}
		return {'value': {}}

class student_marks(models.Model):
	_name="student.marks"

	mark_id = fields.Many2one('student.detail', 'Student Reference', select=True)
	mark_one = fields.Float('Mark 1')
	mark_two = fields.Float('Mark 2')
	mark_three = fields.Float('Mark 3')
	total = fields.Float('Total', compute="_get_total")
   
	@api.one
	@api.depends('mark_one','mark_two','mark_three')
	def _get_total(self):
		self.total = self.mark_one+self.mark_two+self.mark_three
