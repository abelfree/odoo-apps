# Odoo Apps — Abel Takele

Odoo modules by [Abel Takele](https://github.com/abelfree).

| Module | Version | Licence | Description |
|---|---|---|---|
| `daily_cash_balance` | 19.0.1.0.0 | OPL-1 | Daily cash position per bank journal: Opening, Incoming, Outgoing, Closing |
| `bank_balance` | 19.0.1.0.0 | LGPL-3 | The same report, published free |

Each module is self-contained and installs independently, with its own report
record and its own settings, so either or both can be installed.

## Branch layout

One branch per Odoo series, named exactly after the series, with one folder per
module at the root of the branch:

```
19.0
├── daily_cash_balance/
└── bank_balance/
```

## Installation

Clone into your Odoo addons path, update the apps list, and install from Apps.
On Odoo.sh, add the module to the project's repository and redeploy.

## Requirements

Odoo Enterprise — both modules depend on `account_reports`.
