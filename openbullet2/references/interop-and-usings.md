# Interop And Usings

In OB2, LoliCode can interoperate with:

- inline C# mixed directly into the script
- the `Script` block with `NodeJS`, `Python`, `IronPython`, or `Jint`

## Inline C# and custom usings

If the C# uses types from namespaces not already imported, add them through config's custom usings.

Example requiring `System.Text.RegularExpressions`:
```csharp
string match = new Regex(@"^\d{4}").Match(input.DATA).ToString();
```

Custom usings matter for C# compilation. They do not install packages and do not affect Python or NodeJS imports.

## Script block interop

```loli
BLOCK:Script
INTERPRETER:Python
INPUT x,y
BEGIN SCRIPT
result = x + y
END SCRIPT
OUTPUT Int @result
ENDBLOCK
```

- INPUT explicitly copies selected OB2 variables into the foreign runtime
- OUTPUT marshals values back into OB2 variables
- Keep the interface narrow

## NodeJS

- Must be installed on target system
- Third-party packages must be in `Scripts/node_modules`
- Do not assume Node/npm packages are available

Example with external package:
```loli
BLOCK:Script
INTERPRETER:NodeJS
BEGIN SCRIPT
import axios from 'axios';
const response = await axios.get('https://api.example.com');
const responseSource = response.data;
END SCRIPT
OUTPUT String @responseSource
ENDBLOCK
```

## Python

Supported INPUT/OUTPUT types: String, Int, Float, Bool, ListOfStrings, DictionaryOfStrings, ByteArray

### Runtime resolution

1. If `Scripts/.venv` exists → uses that venv
2. Otherwise → auto-downloads Python 3.14 redistributable

### Concurrency

- Shared CPython runtime across OB2 process
- Cannot switch Python version/venv without restart
- Prefer async libraries (httpx, aiohttp) for network-heavy scripts

## Legacy interpreters

- IronPython: Python 2 semantics, planned deprecation
- Jint: planned deprecation
- Prefer Python for new Python-based configs, NodeJS for new JS-based configs
