from odoo import models, _


class DailyCashBalanceHandler(models.AbstractModel):
    _name = 'daily.cash.balance.report.handler'
    _inherit = 'account.report.custom.handler'
    _description = 'Daily Cash Balance Report Custom Handler'

    # ------------------------------------------------------------------
    # Configuration (Accounting > Configuration > Settings)
    # ------------------------------------------------------------------
    def _dcb_company(self, options):
        company_ids = [
            c['id'] for c in options.get('companies', [])
        ] or self.env.companies.ids
        return self.env['res.company'].browse(company_ids[0])

    def _get_bank_journals(self, options):
        """Active bank journals, narrowed by the Journals filter when used."""
        domain = [('type', '=', 'bank')]
        journal_ids = [
            j['id'] for j in options.get('journals', [])
            if j.get('selected') and j.get('model') == 'account.journal'
        ]
        if journal_ids:
            domain.append(('id', 'in', journal_ids))
        return self.env['account.journal'].search(domain, order='name')

    def _get_bank_accounts(self, company, journals):
        """Configured bank accounts, else each journal's default account."""
        if company.dcb_bank_account_ids:
            return company.dcb_bank_account_ids
        return journals.mapped('default_account_id')

    def _get_outstanding_accounts(self, company, journals):
        """Configured outstanding accounts, else the journals' payment methods."""
        if company.dcb_outstanding_account_ids:
            return company.dcb_outstanding_account_ids
        lines = self.env['account.payment.method.line'].search([
            ('journal_id', 'in', journals.ids),
            ('payment_account_id', '!=', False),
        ])
        accounts = lines.mapped('payment_account_id')
        if not accounts:
            accounts = (
                company.account_journal_payment_debit_account_id
                | company.account_journal_payment_credit_account_id
            )
        return accounts

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------
    def _sum_by_journal(self, domain):
        """{journal_id: summed balance} for the given domain."""
        result = {}
        grouped = self.env['account.move.line']._read_group(
            domain, ['journal_id'], ['balance:sum'],
        )
        for journal, balance in grouped:
            result[journal.id] = balance or 0.0
        return result

    def _dcb_domains(self, options, company, journals, date_domain, extra_domain=None):
        """One domain per population, so nothing is counted twice.

        A payment sits on the outstanding account while it is pending and on
        the bank account once it has cleared, so the two sets never overlap
        when 'only unreconciled' is on.
        """
        base = [('journal_id', 'in', journals.ids)]
        if options.get('all_entries'):
            base.append(('parent_state', 'in', ('draft', 'posted')))
        else:
            base.append(('parent_state', '=', 'posted'))
        base += date_domain + (extra_domain or [])

        bank_accounts = self._get_bank_accounts(company, journals)
        domains = [base + [('account_id', 'in', bank_accounts.ids)]]

        if company.dcb_include_outstanding:
            outstanding = self._get_outstanding_accounts(company, journals)
            if outstanding:
                outstanding_domain = base + [('account_id', 'in', outstanding.ids)]
                if company.dcb_outstanding_unreconciled_only:
                    outstanding_domain.append(('full_reconcile_id', '=', False))
                if company.dcb_outstanding_cutoff_date:
                    outstanding_domain.append(
                        ('date', '>', company.dcb_outstanding_cutoff_date))
                domains.append(outstanding_domain)
        return domains

    def _totals(self, options, company, journals, date_domain, extra_domain=None):
        totals = {}
        for domain in self._dcb_domains(
                options, company, journals, date_domain, extra_domain):
            for journal_id, amount in self._sum_by_journal(domain).items():
                totals[journal_id] = totals.get(journal_id, 0.0) + amount
        return totals

    # ------------------------------------------------------------------
    # Lines
    # ------------------------------------------------------------------
    def _dynamic_lines_generation(self, report, options,
                                  all_column_groups_expression_totals,
                                  warnings=None):
        journals = self._get_bank_journals(options)
        if not journals:
            return []

        company = self._dcb_company(options)
        date_from = options['date']['date_from']
        date_to = options['date']['date_to']
        period = [('date', '>=', date_from), ('date', '<=', date_to)]

        opening = self._totals(
            options, company, journals, [('date', '<', date_from)])
        incoming = self._totals(
            options, company, journals, period, [('balance', '>', 0)])
        outgoing = self._totals(
            options, company, journals, period, [('balance', '<', 0)])

        lines = []
        running = [0.0, 0.0, 0.0, 0.0]

        for journal in journals:
            open_amount = opening.get(journal.id, 0.0)
            in_amount = incoming.get(journal.id, 0.0)
            # Credit movement is negative in the ledger; show it positive.
            out_amount = -outgoing.get(journal.id, 0.0)
            close_amount = open_amount + in_amount - out_amount

            values = [open_amount, in_amount, out_amount, close_amount]
            for index, value in enumerate(values):
                running[index] += value

            lines.append((0, {
                'id': report._get_generic_line_id('account.journal', journal.id),
                'name': journal.name,
                'level': 2,
                'columns': self._build_columns(report, options, values),
            }))

        lines.append((0, {
            'id': report._get_generic_line_id(None, None, markup='total'),
            'name': _('Total'),
            'level': 1,
            'class': 'total',
            'columns': self._build_columns(report, options, running),
        }))
        return lines

    def _build_columns(self, report, options, values):
        return [{
            'name': report.format_value(options, value, figure_type='monetary'),
            'no_format': value,
            'figure_type': 'monetary',
        } for value in values]
