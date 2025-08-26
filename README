# 🧵 fabrix

**fabrix** is a Python toolkit to **evaluate, validate, and debug**
[Microsoft Fabric / Azure Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/expression-language) pipeline expressions.
It helps you test expressions locally, manage variables & parameters, and visualize execution with **rich tracing**.

> ⚠️ This project is still in progress. Expect changes and new features soon.

---

## 🔗 Links
- 📖 [Documentation (WIP)](https://github.com/yourname/fabrix/wiki)
- 💻 [Source Code](https://github.com/yourname/fabrix)

---

## ✨ Features
- Parse & evaluate Fabric/ADF expressions locally
- Manage **variables**, **pipeline parameters**, and **scope values**
- Validate syntax: unmatched brackets, wrong quotes, unknown functions
- Debug with **beautiful Rich tree traces**
- Extend with your own custom functions via a registry

---

## 📦 Requirements
- Python **3.11+**
- [pydantic](https://docs.pydantic.dev) v2
- [rich](https://rich.readthedocs.io/)

---

## ⚙️ Installation
```bash
pip install fabrix
```

## 🚀 Usage

```python
from fabrix import Context, evaluate

# Create a context with parameters & variables
ctx = Context(
    pipeline_parameters={"myNumber": 42},
    variables={"greeting": "hello"}
)

# Simple expression
result = evaluate("@concat('Answer is: ', string(pipeline().parameters.myNumber))", ctx)
print(result)  # Answer is: 42

# With variable assignment
from fabrix import Expression

expr = Expression(expression="@toUpper(variables('greeting'))", result="shout")
evaluate(expr, context=ctx)

print(ctx.variables["shout"])  # HELLO

```

## 🗺️ Roadmap

- [ ] Add more Fabric/ADF built-in functions
- [ ] Improve error messages with fuzzy suggestions
- [ ] Advanced type checking for function arguments
- [ ] VS Code extension with syntax highlighting & validation
- [ ] Better documentation and tutorials
- [ ] Publish first stable release on PyPI
