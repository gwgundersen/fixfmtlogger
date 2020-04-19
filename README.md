A Python library for fixed-width formatted logging. Built on [fixfmt](https://github.com/alexhsamuel/fixfmt). For example:


```python
from   flogger import TableLogger
import random

logger = TableLogger(header=['iter', 'train acc', 'test acc'],
                     cell_width=10,
                     metadata={
                         'model': 'logistic regression',
                         'n_iters': 100
                     })
for t in range(2):
    data = {
        'iter': t,
        'train acc': random.random(),
        'test acc': random.random()
    }
    logger.log(data)
```

will create

```bash
================================================================================
Metadata
  model  : logistic regression
  n_iters: 100
================================================================================
│ iter       │ train acc  │ test acc   │
├────────────┼────────────┼────────────┤
│ 0          │ 0.4397604… │ 0.9686414… │
│ 1          │ 0.5595392… │ 0.8260999… │
```

## API

TK.

## Install

From PyPI:

```bash
pip install flogger
```

## Todo

- Create stateless table that takes fixed set of headers and formatters.
- Support tabular data; `TableLogger`?
- Build out base `Parse`.
