A Python library for fixed-width formatted logging. Built on [fixfmt](https://github.com/alexhsamuel/fixfmt).

### Example

```python
from   flogger import TableLogger
import random

logger = TableLogger(
    fpath='out.txt',
    header=['iter', 'train acc', 'test acc'],
    cell_width=10,
    metadata={
        'model': 'logistic regression',
        'n_iters': 100
})

for t in range(2):
    logger.log({
        'iter'     : t,
        'train acc': random.random(),
        'test acc' : random.random()
    })
```

will create a file, `out.txt`, with the following contents:

```bash
===============================================================================
Metadata
  model  : logistic regression
  n_iters: 100
===============================================================================
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

- `TableLogger` should take...
    - common `width` parameter or...
    - ...or array of widths (`len(widths) == len(headers)`)...
    - ...or array for `fixfmt` loggers
- Build out base `Parse`.
