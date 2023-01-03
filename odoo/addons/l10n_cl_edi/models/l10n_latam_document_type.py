from odoo import fields, models, _
from odoo.exceptions import UserError


class L10nLatamDocumentType(models.Model):
    _inherit = 'l10n_latam.document.type'

    l10n_cl_dte_caf_ids = fields.One2many('l10n_cl.dte.caf', 'l10n_latam_document_type_id', string='DTE Caf')

    def _is_doc_type_ticket(self):
        return self.code in ['35', '38', '39', '41', '70', '71']

    def _is_doc_type_voucher(self):
        return self.code in ['35', '39', '906', '45', '46', '70', '71']

    def _is_doc_type_exempt(self):
        return self.code in ['34', '110', '111', '112']

    def _is_doc_type_export(self):
        return self.code in ['110', '111', '112']

    def _is_doc_type_acceptance(self):
        """
        Check if the document type can be accepted or claimed
        """
        return self.code in ['33', '34', '56', '61', '43']

    def _get_caf_file(self, company_id, folio):
        caf = self.env['l10n_cl.dte.caf'].sudo().search([
            ('final_nb', '>=', folio), ('start_nb', '<=', folio), ('l10n_latam_document_type_id', '=', self.id),
            ('status', '=', 'in_use'), ('company_id', '=', company_id)], limit=1)
        if not caf:
            raise UserError(_('There are no CAFs available for folio %s in the sequence of %s. '
                            'Please upload a CAF file or ask for a new one at www.sii.cl website') % (folio, self.name))

        return caf._decode_caf()

    def _get_start_number(self):
        caf = self.sudo().l10n_cl_dte_caf_ids.filtered(lambda x: x.status == 'in_use' and
                                                                 x.l10n_latam_document_type_id == self.id)
        if not caf:
            raise UserError(_('There are no CAFs available. Please upload a CAF file or ask for a new one at www.sii.cl website'))
        return caf.start_nb
