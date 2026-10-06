# Odoo Apps — Abel Takele

Odoo modules by [Abel Takele](https://github.com/abelfree).

| Module | Version | Description |
|---|---|---|
| `daily_cash_balance` | 19.0.1.0.0 | Daily cash position per bank journal: Opening, Incoming, Outgoing, Closing |

## Branch layout

One branch per Odoo series, named exactly after the series, with one folder per
module at the root of the branch:

```
19.0
└── daily_cash_balance/
```

## Installation

Clone into your Odoo addons path, update the apps list, and install from Apps.
On Odoo.sh, add the module to the project's repository and redeploy.

## Requirements

`daily_cash_balance` depends on `account_reports`, which is Odoo Enterprise.

## Licence

OPL-1. See each module's `LICENSE`.
