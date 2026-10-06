from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    dcb_bank_account_ids = fields.Many2many(
        'account.account',
        'dcb_company_bank_account_rel', 'company_id', 'account_id',
        string='Bank Accounts (Daily Cash Balance)',
        domain="[('account_type', '=', 'asset_cash')]",
        help="Accounts holding the cleared bank position.\n"
             "Leave empty to use each bank journal's own default account.",
    )
    dcb_outstanding_account_ids = fields.Many2many(
        'account.account',
        'dcb_company_outstanding_account_rel', 'company_id', 'account_id',
        string='Outstanding Accounts (Daily Cash Balance)',
        help="Outstanding Receipts / Outstanding Payments accounts.\n"
             "Leave empty to read them from the journals' payment methods.",
    )
    dcb_include_outstanding = fields.Boolean(
        string='Include Outstanding Payments',
        default=False,
        help="Include money received or paid but not yet cleared to the bank.\n"
             "Off = cleared position only, matching the bank statement.",
    )
    dcb_outstanding_unreconciled_only = fields.Boolean(
        string='Only Unreconciled Outstanding',
        default=True,
        help="Count an outstanding item only while it is unreconciled, so a "
             "payment is not counted twice once it has cleared to the bank.",
    )
    dcb_outstanding_cutoff_date = fields.Date(
        string='Ignore Outstanding On or Before',
        help="Lines on the outstanding accounts dated on or before this date "
             "are ignored.\n"
             "Use it when opening balances were imported onto the outstanding "
             "accounts as the contra side of the bank-account openings; "
             "without it those entries are counted twice.\n"
             "Leave empty when there is no such import.",
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dcb_bank_account_ids = fields.Many2many(
        related='company_id.dcb_bank_account_ids', readonly=False,
    )
    dcb_outstanding_account_ids = fields.Many2many(
        related='company_id.dcb_outstanding_account_ids', readonly=False,
    )
    dcb_include_outstanding = fields.Boolean(
        related='company_id.dcb_include_outstanding', readonly=False,
    )
    dcb_outstanding_unreconciled_only = fields.Boolean(
        related='company_id.dcb_outstanding_unreconciled_only', readonly=False,
    )
    dcb_outstanding_cutoff_date = fields.Date(
        related='company_id.dcb_outstanding_cutoff_date', readonly=False,
    )
