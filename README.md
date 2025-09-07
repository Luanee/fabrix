<p align="center">
  <a href="https://github.com/Luanee/fabrix"><img src="https://github.com/Luanee/fabrix/blob/main/docs/assets/images/logo.png?raw=true" alt="fabrix"></a>
</p>
<p align="center">
    <em>Evaluate expressions without the need of pipelines.</em>
</p>
<a href="https://pypi.org/project/fabrix" target="_blank">
    <img src="https://img.shields.io/pypi/v/fabrix?color=%2647141&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fabrix" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fabrix.svg?color=%2647141" alt="Supported Python versions">
</a>
</p>

**fabrix** is a Python toolkit to **evaluate, validate, and debug**
[Microsoft Fabric / Azure Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/expression-language) pipeline expressions.
It helps you test expressions locally, manage variables & parameters, and visualize execution with **rich tracing**.

> ⚠️ This project is still in progress. Expect changes and new features soon.

---

**Documentation:** [https://github.com/luanee/fabrix/wiki](https://github.com/luanee/fabrix)
**Source Code:** [https://github.com/luanee/fabrix](https://github.com/luanee/fabrix)

---

## Features

- Parse & evaluate Fabric/ADF expressions locally
- Manage **variables**, **pipeline parameters**, and **scope values**
- Validate syntax: unmatched brackets, wrong quotes, unknown functions
- Debug with **beautiful Rich tree traces**
- Extend with your own custom functions via a registry

---

## Requirements

- [pydantic](https://docs.pydantic.dev) for smaller validations
- [rich](https://rich.readthedocs.io/) for beautiful output

---

## ⚙️ Installation

```bash
pip install fabrix
```

## 🚀 Usage

```python
from fabrix import Context, Expression, evaluate, run

# Create a context with parameters & variables
ctx = Context(
    pipeline_parameters={
        "myNumber": 42,
    },
    variables={
        "greeting": "hello",
        "row_index": 1,
    },
)

# Simple expression
result = evaluate("@concat('Answer is: ', string(pipeline().parameters.myNumber))", ctx)
print(result)  # Answer is: 42

# With variable assignment
expr_1 = Expression(expression="@toUpper(variables('greeting'))", variable="shout")
expr_2 = Expression(expression="@add(variables('row_index'),mul(4,5),add(variables('row_index'),max(4.5,3.9,578.4)))")

run(expr_1, expr_2, context=ctx, show_output=True)  # see output below
print(ctx.variables["shout"])  # HELLO
```

![expression console output](https://github.com/Luanee/fabrix/blob/main/docs/assets/images/example_output.png?raw=true)

## 🗺️ Roadmap

- [ ] Add more Fabric/ADF built-in functions
- [ ] Improve error messages with fuzzy suggestions
- [ ] Advanced type checking for function arguments
- [ ] VS Code extension with syntax highlighting & validation
- [ ] Better documentation and tutorials
- [x] Publish first stable release on PyPI
