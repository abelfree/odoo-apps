{
    'name': 'Daily Cash Balance Report',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Daily cash position per bank journal: Opening, Incoming, Outgoing, Closing',
    'description': """
Daily Cash Balance Report
=========================

A daily cash position for every active bank journal, as a standard Odoo
accounting report with the usual date filter, journal filter, print, export
and fold controls.

One row per bank journal:

* Opening Balance - the position at the start of the selected period
* Incoming - debit movements in the period
* Outgoing - credit movements in the period, shown positive
* Closing Balance - Opening + Incoming - Outgoing

Closing ties out on every row by construction, so the report can be read as a
cash statement rather than checked against one.

Configuration
-------------

Everything is set under Accounting > Configuration > Settings, and every
setting has a working default:

* Bank Accounts - defaults to each bank journal's own default account.
* Outstanding Accounts - defaults to the accounts configured on the journals'
  payment methods.
* Include Outstanding Payments - off by default, giving the cleared position
  that matches the bank statement. Switched on, it adds money received or paid
  but not yet reconciled.
* Only Unreconciled Outstanding - keeps a payment from being counted twice,
  once on the outstanding account and again on the bank account after it
  clears.
* Ignore Outstanding On or Before - for databases whose opening balances were
  imported onto the outstanding accounts as the contra side of the
  bank-account openings.

Banks are discovered from the journals, so a newly created bank journal
appears in the report with no further setup. No account codes, journal names
or dates are hardcoded.
""",
    'author': 'Abel Takele',
    'maintainer': 'Abel Takele',
    'website': 'https://github.com/abelfree',
    'support': 'abeltakele3d@gmail.com',
    'price': 10.00,
    'currency': 'USD',
    'depends': ['account_reports'],
    'data': [
        'data/daily_cash_balance_report.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
