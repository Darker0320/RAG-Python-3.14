# Module Objects

PyTypeObjectPyModule\_Type
*Part of the Stable ABI.*

    This instance of `PyTypeObject` represents the Python module type. This
    is exposed to Python programs as `types.ModuleType`.

intPyModule\_Check(PyObject\*p)
Return true if *p* is a module object, or a subtype of a module object.
    This function always succeeds.

intPyModule\_CheckExact(PyObject\*p)
Return true if *p* is a module object, but not a subtype of
    `PyModule_Type`. This function always succeeds.

PyObject\*PyModule\_NewObject(PyObject\*name)
*Return value: New reference.* *Part of the Stable ABI since version 3.7.*

    Return a new module object with `module.__name__` set to *name*.
    The module’s `__name__`, `__doc__`,
    `__package__` and `__loader__` attributes are
    filled in (all but `__name__` are set to `None`). The caller is
    responsible for setting a `__file__` attribute.

    Return `NULL` with an exception set on error.

    Added in version 3.3.

    Changed in version 3.4: `__package__` and `__loader__` are now set to
    `None`.

PyObject\*PyModule\_New(constchar\*name)
*Return value: New reference.* *Part of the Stable ABI.*

    Similar to `PyModule_NewObject()`, but the name is a UTF-8 encoded
    string instead of a Unicode object.

PyObject\*PyModule\_GetDict(PyObject\*module)
*Return value: Borrowed reference.* *Part of the Stable ABI.*

    Return the dictionary object that implements *module*’s namespace; this object
    is the same as the `__dict__` attribute of the module object.
    If *module* is not a module object (or a subtype of a module object),
    `SystemError` is raised and `NULL` is returned.

    It is recommended extensions use other `PyModule_*` and
    `PyObject_*` functions rather than directly manipulate a module’s
    `__dict__`.

    The returned reference is borrowed from the module; it is valid until
    the module is destroyed.

PyObject\*PyModule\_GetNameObject(PyObject\*module)
*Return value: New reference.* *Part of the Stable ABI since version 3.7.*

    Return *module*’s `__name__` value. If the module does not
    provide one, or if it is not a string, `SystemError` is raised and
    `NULL` is returned.

    Added in version 3.3.

constchar\*PyModule\_GetName(PyObject\*module)
*Part of the Stable ABI.*

    Similar to `PyModule_GetNameObject()` but return the name encoded to
    `'utf-8'`.

    The returned buffer is only valid until the module is renamed or destroyed.
    Note that Python code may rename a module by setting its `__name__`
    attribute.

void\*PyModule\_GetState(PyObject\*module)
*Part of the Stable ABI.*

    Return the “state” of the module, that is, a pointer to the block of memory
    allocated at module creation time, or `NULL`. See
    `PyModuleDef.m_size`.

PyModuleDef\*PyModule\_GetDef(PyObject\*module)
*Part of the Stable ABI.*

    Return a pointer to the `PyModuleDef` struct from which the module was
    created, or `NULL` if the module wasn’t created from a definition.

    On error, return `NULL` with an exception set.
    Use `PyErr_Occurred()` to tell this case apart from a missing
    `PyModuleDef`.

PyObject\*PyModule\_GetFilenameObject(PyObject\*module)
*Return value: New reference.* *Part of the Stable ABI.*

    Return the name of the file from which *module* was loaded using *module*’s
    `__file__` attribute. If this is not defined, or if it is not a
    string, raise `SystemError` and return `NULL`; otherwise return
    a reference to a Unicode object.

    Added in version 3.2.

constchar\*PyModule\_GetFilename(PyObject\*module)
*Part of the Stable ABI.*

    Similar to `PyModule_GetFilenameObject()` but return the filename
    encoded to ‘utf-8’.

    The returned buffer is only valid until the module’s `__file__` attribute
    is reassigned or the module is destroyed.

    Deprecated since version 3.2: `PyModule_GetFilename()` raises `UnicodeEncodeError` on
    unencodable filenames, use `PyModule_GetFilenameObject()` instead.

# Module definitions

The functions in the previous section work on any module object, including
modules imported from Python code.

Modules defined using the C API typically use a *module definition*,
`PyModuleDef` – a statically allocated, constant “description” of
how a module should be created.

The definition is usually used to define an extension’s “main” module object
(see Defining extension modules for details).
It is also used to
create extension modules dynamically.

Unlike `PyModule_New()`, the definition allows management of
*module state* – a piece of memory that is allocated and cleared together
with the module object.
Unlike the module’s Python attributes, Python code cannot replace or delete
data stored in module state.

typePyModuleDef
*Part of the Stable ABI (including all members).*

    The module definition struct, which holds all information needed to create
    a module object.
    This structure must be statically allocated (or be otherwise guaranteed
    to be valid while any modules created from it exist).
    Usually, there is only one variable of this type for each extension module.

    PyModuleDef\_Basem\_base
Always initialize this member to `PyModuleDef_HEAD_INIT`.

    constchar\*m\_name
Name for the new module.

    constchar\*m\_doc
Docstring for the module; usually a docstring variable created with
        `PyDoc_STRVAR` is used.

    Py\_ssize\_tm\_size
Module state may be kept in a per-module memory area that can be
        retrieved with `PyModule_GetState()`, rather than in static globals.
        This makes modules safe for use in multiple sub-interpreters.

        This memory area is allocated based on *m\_size* on module creation,
        and freed when the module object is deallocated, after the
        `m_free` function has been called, if present.

        Setting it to a non-negative value means that the module can be
        re-initialized and specifies the additional amount of memory it requires
        for its state.

        Setting `m_size` to `-1` means that the module does not support
        sub-interpreters, because it has global state.
        Negative `m_size` is only allowed when using
        legacy single-phase initialization
        or when creating modules dynamically.

        See **PEP 3121** for more details.

    PyMethodDef\*m\_methods
A pointer to a table of module-level functions, described by
        `PyMethodDef` values. Can be `NULL` if no functions are present.

    PyModuleDef\_Slot\*m\_slots
An array of slot definitions for multi-phase initialization, terminated by
        a `{0, NULL}` entry.
        When using legacy single-phase initialization, *m\_slots* must be `NULL`.

        Changed in version 3.5: Prior to version 3.5, this member was always set to `NULL`,
        and was defined as:

        > inquirym\_reload

    traverseprocm\_traverse
A traversal function to call during GC traversal of the module object, or
        `NULL` if not needed.

        This function is not called if the module state was requested but is not
        allocated yet. This is the case immediately after the module is created
        and before the module is executed (`Py_mod_exec` function). More
        precisely, this function is not called if `m_size` is greater
        than 0 and the module state (as returned by `PyModule_GetState()`)
        is `NULL`.

        Changed in version 3.9: No longer called before the module state is allocated.

    inquirym\_clear
A clear function to call during GC clearing of the module object, or
        `NULL` if not needed.

        This function is not called if the module state was requested but is not
        allocated yet. This is the case immediately after the module is created
        and before the module is executed (`Py_mod_exec` function). More
        precisely, this function is not called if `m_size` is greater
        than 0 and the module state (as returned by `PyModule_GetState()`)
        is `NULL`.

        Like `PyTypeObject.tp_clear`, this function is not *always*
        called before a module is deallocated. For example, when reference
        counting is enough to determine that an object is no longer used,
        the cyclic garbage collector is not involved and
        `m_free` is called directly.

        Changed in version 3.9: No longer called before the module state is allocated.

    freefuncm\_free
A function to call during deallocation of the module object, or `NULL`
        if not needed.

        This function is not called if the module state was requested but is not
        allocated yet. This is the case immediately after the module is created
        and before the module is executed (`Py_mod_exec` function). More
        precisely, this function is not called if `m_size` is greater
        than 0 and the module state (as returned by `PyModule_GetState()`)
        is `NULL`.

        Changed in version 3.9: No longer called before the module state is allocated.

PyTypeObjectPyModuleDef\_Type
*Part of the Stable ABI since version 3.5.*

    The type of `PyModuleDef` objects.

## Module slots

typePyModuleDef\_Slot
*Part of the Stable ABI (including all members) since version 3.5.*

    intslot
A slot ID, chosen from the available values explained below.

    void\*value
Value of the slot, whose meaning depends on the slot ID.

    Added in version 3.5.

The available slot types are:

Py\_mod\_create
*Part of the Stable ABI since version 3.5.*

    Specifies a function that is called to create the module object itself.
    The *value* pointer of this slot must point to a function of the signature:

    PyObject\*create\_module(PyObject\*spec, PyModuleDef\*def)

    The function receives a `ModuleSpec`
    instance, as defined in **PEP 451**, and the module definition.
    It should return a new module object, or set an error
    and return `NULL`.

    This function should be kept minimal. In particular, it should not
    call arbitrary Python code, as trying to import the same module again may
    result in an infinite loop.

    Multiple `Py_mod_create` slots may not be specified in one module
    definition.

    If `Py_mod_create` is not specified, the import machinery will create
    a normal module object using `PyModule_New()`. The name is taken from
    *spec*, not the definition, to allow extension modules to dynamically adjust
    to their place in the module hierarchy and be imported under different
    names through symlinks, all while sharing a single module definition.

    There is no requirement for the returned object to be an instance of
    `PyModule_Type`. Any type can be used, as long as it supports
    setting and getting import-related attributes.
    However, only `PyModule_Type` instances may be returned if the
    `PyModuleDef` has non-`NULL` `m_traverse`, `m_clear`,
    `m_free`; non-zero `m_size`; or slots other than `Py_mod_create`.

    Added in version 3.5.

Py\_mod\_exec
*Part of the Stable ABI since version 3.5.*

    Specifies a function that is called to *execute* the module.
    This is equivalent to executing the code of a Python module: typically,
    this function adds classes and constants to the module.
    The signature of the function is:

    intexec\_module(PyObject\*module)

    If multiple `Py_mod_exec` slots are specified, they are processed in the
    order they appear in the *m\_slots* array.

    Added in version 3.5.

Py\_mod\_multiple\_interpreters
*Part of the Stable ABI since version 3.12.*

    Specifies one of the following values:

    Py\_MOD\_MULTIPLE\_INTERPRETERS\_NOT\_SUPPORTED
The module does not support being imported in subinterpreters.

    Py\_MOD\_MULTIPLE\_INTERPRETERS\_SUPPORTED
The module supports being imported in subinterpreters,
        but only when they share the main interpreter’s GIL.
        (See Isolating Extension Modules.)

    Py\_MOD\_PER\_INTERPRETER\_GIL\_SUPPORTED
The module supports being imported in subinterpreters,
        even when they have their own GIL.
        (See Isolating Extension Modules.)

    This slot determines whether or not importing this module
    in a subinterpreter will fail.

    Multiple `Py_mod_multiple_interpreters` slots may not be specified
    in one module definition.

    If `Py_mod_multiple_interpreters` is not specified, the import
    machinery defaults to `Py_MOD_MULTIPLE_INTERPRETERS_SUPPORTED`.

    Added in version 3.12.

Py\_mod\_gil
*Part of the Stable ABI since version 3.13.*

    Specifies one of the following values:

    Py\_MOD\_GIL\_USED
The module depends on the presence of the global interpreter lock (GIL),
        and may access global state without synchronization.

    Py\_MOD\_GIL\_NOT\_USED
The module is safe to run without an active GIL.

    This slot is ignored by Python builds not configured with
    `--disable-gil`. Otherwise, it determines whether or not importing
    this module will cause the GIL to be automatically enabled. See
    Free-threaded CPython for more detail.

    Multiple `Py_mod_gil` slots may not be specified in one module definition.

    If `Py_mod_gil` is not specified, the import machinery defaults to
    `Py_MOD_GIL_USED`.

    Added in version 3.13.

# Creating extension modules dynamically

The following functions may be used to create a module outside of an
extension’s initialization function.
They are also used in
single-phase initialization.

PyObject\*PyModule\_Create(PyModuleDef\*def)
*Return value: New reference.*

    Create a new module object, given the definition in *def*.
    This is a macro that calls `PyModule_Create2()` with
    *module\_api\_version* set to `PYTHON_API_VERSION`, or
    to `PYTHON_ABI_VERSION` if using the
    limited API.

PyObject\*PyModule\_Create2(PyModuleDef\*def, intmodule\_api\_version)
*Return value: New reference.* *Part of the Stable ABI.*

    Create a new module object, given the definition in *def*, assuming the
    API version *module\_api\_version*. If that version does not match the version
    of the running interpreter, a `RuntimeWarning` is emitted.

    Return `NULL` with an exception set on error.

    This function does not support slots.
    The `m_slots` member of *def* must be `NULL`.

    Note

    Most uses of this function should be using `PyModule_Create()`
    instead; only use this if you are sure you need it.

PyObject\*PyModule\_FromDefAndSpec(PyModuleDef\*def, PyObject\*spec)
*Return value: New reference.*

    This macro calls `PyModule_FromDefAndSpec2()` with
    *module\_api\_version* set to `PYTHON_API_VERSION`, or
    to `PYTHON_ABI_VERSION` if using the
    limited API.

    Added in version 3.5.

PyObject\*PyModule\_FromDefAndSpec2(PyModuleDef\*def, PyObject\*spec, intmodule\_api\_version)
*Return value: New reference.* *Part of the Stable ABI since version 3.7.*

    Create a new module object, given the definition in *def* and the
    ModuleSpec *spec*, assuming the API version *module\_api\_version*.
    If that version does not match the version of the running interpreter,
    a `RuntimeWarning` is emitted.

    Return `NULL` with an exception set on error.

    Note that this does not process execution slots (`Py_mod_exec`).
    Both `PyModule_FromDefAndSpec` and `PyModule_ExecDef` must be called
    to fully initialize a module.

    Note

    Most uses of this function should be using `PyModule_FromDefAndSpec()`
    instead; only use this if you are sure you need it.

    Added in version 3.5.

intPyModule\_ExecDef(PyObject\*module, PyModuleDef\*def)
*Part of the Stable ABI since version 3.7.*

    Process any execution slots (`Py_mod_exec`) given in *def*.

    Added in version 3.5.

PYTHON\_API\_VERSION
The C API version. Defined for backwards compatibility.

    Currently, this constant is not updated in new Python versions, and is not
    useful for versioning. This may change in the future.

PYTHON\_ABI\_VERSION
Defined as `3` for backwards compatibility.

    Currently, this constant is not updated in new Python versions, and is not
    useful for versioning. This may change in the future.

# Support functions

The following functions are provided to help initialize a module
state.
They are intended for a module’s execution slots (`Py_mod_exec`),
the initialization function for legacy single-phase initialization,
or code that creates modules dynamically.

intPyModule\_AddObjectRef(PyObject\*module, constchar\*name, PyObject\*value)
*Part of the Stable ABI since version 3.10.*

    Add an object to *module* as *name*. This is a convenience function which
    can be used from the module’s initialization function.

    On success, return `0`. On error, raise an exception and return `-1`.

    Example usage:

    ```
    staticint
    add_spam(PyObject*module,intvalue)
    {
    PyObject*obj=PyLong_FromLong(value);
    if(obj==NULL){
    return-1;
    }
    intres=PyModule_AddObjectRef(module,"spam",obj);
    Py_DECREF(obj);
    returnres;
    }
    ```

    To be convenient, the function accepts `NULL` *value* with an exception
    set. In this case, return `-1` and just leave the raised exception
    unchanged.

    The example can also be written without checking explicitly if *obj* is
    `NULL`:

    ```
    staticint
    add_spam(PyObject*module,intvalue)
    {
    PyObject*obj=PyLong_FromLong(value);
    intres=PyModule_AddObjectRef(module,"spam",obj);
    Py_XDECREF(obj);
    returnres;
    }
    ```

    Note that `Py_XDECREF()` should be used instead of `Py_DECREF()` in
    this case, since *obj* can be `NULL`.

    The number of different *name* strings passed to this function
    should be kept small, usually by only using statically allocated strings
    as *name*.
    For names that aren’t known at compile time, prefer calling
    `PyUnicode_FromString()` and `PyObject_SetAttr()` directly.
    For more details, see `PyUnicode_InternFromString()`, which may be
    used internally to create a key object.

    Added in version 3.10.

intPyModule\_Add(PyObject\*module, constchar\*name, PyObject\*value)
*Part of the Stable ABI since version 3.13.*

    Similar to `PyModule_AddObjectRef()`, but “steals”
    a reference to *value* (even on error).
    It can be called with a result of function that returns a new reference
    without bothering to check its result or even saving it to a variable.

    Example usage:

    ```
    if(PyModule_Add(module,"spam",PyBytes_FromString(value))<0){
    gotoerror;
    }
    ```

    Added in version 3.13.

intPyModule\_AddObject(PyObject\*module, constchar\*name, PyObject\*value)
*Part of the Stable ABI.*

    Similar to `PyModule_AddObjectRef()`, but steals
    a reference to *value* on success (if it returns `0`).

    The new `PyModule_Add()` or `PyModule_AddObjectRef()`
    functions are recommended, since it is
    easy to introduce reference leaks by misusing the
    `PyModule_AddObject()` function.

    Note

    Unlike other functions that steal references, `PyModule_AddObject()`
    only releases the reference to *value* **on success**.

    This means that its return value must be checked, and calling code must
    `Py_XDECREF()` *value* manually on error.

    Example usage:

    ```
    PyObject*obj=PyBytes_FromString(value);
    if(PyModule_AddObject(module,"spam",obj)<0){
    // If 'obj' is not NULL and PyModule_AddObject() failed,
    // 'obj' strong reference must be deleted with Py_XDECREF().
    // If 'obj' is NULL, Py_XDECREF() does nothing.
    Py_XDECREF(obj);
    gotoerror;
    }
    // PyModule_AddObject() stole a reference to obj:
    // Py_XDECREF(obj) is not needed here.
    ```

    Soft deprecated since version 3.13.

intPyModule\_AddIntConstant(PyObject\*module, constchar\*name, longvalue)
*Part of the Stable ABI.*

    Add an integer constant to *module* as *name*. This convenience function can be
    used from the module’s initialization function.
    Return `-1` with an exception set on error, `0` on success.

    This is a convenience function that calls `PyLong_FromLong()` and
    `PyModule_AddObjectRef()`; see their documentation for details.

intPyModule\_AddStringConstant(PyObject\*module, constchar\*name, constchar\*value)
*Part of the Stable ABI.*

    Add a string constant to *module* as *name*. This convenience function can be
    used from the module’s initialization function. The string *value* must be
    `NULL`-terminated.
    Return `-1` with an exception set on error, `0` on success.

    This is a convenience function that calls
    `PyUnicode_InternFromString()` and `PyModule_AddObjectRef()`;
    see their documentation for details.

PyModule\_AddIntMacro(module, macro)
Add an int constant to *module*. The name and the value are taken from
    *macro*. For example `PyModule_AddIntMacro(module, AF_INET)` adds the int
    constant *AF\_INET* with the value of *AF\_INET* to *module*.
    Return `-1` with an exception set on error, `0` on success.

PyModule\_AddStringMacro(module, macro)
Add a string constant to *module*.

intPyModule\_AddType(PyObject\*module, PyTypeObject\*type)
*Part of the Stable ABI since version 3.10.*

    Add a type object to *module*.
    The type object is finalized by calling internally `PyType_Ready()`.
    The name of the type object is taken from the last component of
    `tp_name` after dot.
    Return `-1` with an exception set on error, `0` on success.

    Added in version 3.9.

intPyModule\_AddFunctions(PyObject\*module, PyMethodDef\*functions)
*Part of the Stable ABI since version 3.7.*

    Add the functions from the `NULL` terminated *functions* array to *module*.
    Refer to the `PyMethodDef` documentation for details on individual
    entries (due to the lack of a shared module namespace, module level
    “functions” implemented in C typically receive the module as their first
    parameter, making them similar to instance methods on Python classes).

    This function is called automatically when creating a module from
    `PyModuleDef` (such as when using Multi-phase initialization,
    `PyModule_Create`, or `PyModule_FromDefAndSpec`).
    Some module authors may prefer defining functions in multiple
    `PyMethodDef` arrays; in that case they should call this function
    directly.

    The *functions* array must be statically allocated (or otherwise guaranteed
    to outlive the module object).

    Added in version 3.5.

intPyModule\_SetDocString(PyObject\*module, constchar\*docstring)
*Part of the Stable ABI since version 3.7.*

    Set the docstring for *module* to *docstring*.
    This function is called automatically when creating a module from
    `PyModuleDef` (such as when using Multi-phase initialization,
    `PyModule_Create`, or `PyModule_FromDefAndSpec`).

    Return `0` on success.
    Return `-1` with an exception set on error.

    Added in version 3.5.

intPyUnstable\_Module\_SetGIL(PyObject\*module, void\*gil)
*This is Unstable API. It may change without warning in minor releases.*

    Indicate that *module* does or does not support running without the global
    interpreter lock (GIL), using one of the values from
    `Py_mod_gil`. It must be called during *module*’s initialization
    function when using Legacy single-phase initialization.
    If this function is not called during module initialization, the
    import machinery assumes the module does not support running without the
    GIL. This function is only available in Python builds configured with
    `--disable-gil`.
    Return `-1` with an exception set on error, `0` on success.

    Added in version 3.13.

## Module lookup (single-phase initialization)

The legacy single-phase initialization
initialization scheme creates singleton modules that can be looked up
in the context of the current interpreter. This allows the module object to be
retrieved later with only a reference to the module definition.

These functions will not work on modules created using multi-phase initialization,
since multiple such modules can be created from a single definition.

PyObject\*PyState\_FindModule(PyModuleDef\*def)
*Return value: Borrowed reference.* *Part of the Stable ABI.*

    Returns the module object that was created from *def* for the current interpreter.
    This method requires that the module object has been attached to the interpreter state with
    `PyState_AddModule()` beforehand. In case the corresponding module object is not
    found or has not been attached to the interpreter state yet, it returns `NULL`.

intPyState\_AddModule(PyObject\*module, PyModuleDef\*def)
*Part of the Stable ABI since version 3.3.*

    Attaches the module object passed to the function to the interpreter state. This allows
    the module object to be accessible via `PyState_FindModule()`.

    Only effective on modules created using single-phase initialization.

    Python calls `PyState_AddModule` automatically after importing a module
    that uses single-phase initialization,
    so it is unnecessary (but harmless) to call it from module initialization
    code. An explicit call is needed only if the module’s own init code
    subsequently calls `PyState_FindModule`.
    The function is mainly intended for implementing alternative import
    mechanisms (either by calling it directly, or by referring to its
    implementation for details of the required state updates).

    If a module was attached previously using the same *def*, it is replaced
    by the new *module*.

    The caller must have an attached thread state.

    Return `-1` with an exception set on error, `0` on success.

    Added in version 3.3.

intPyState\_RemoveModule(PyModuleDef\*def)
*Part of the Stable ABI since version 3.3.*

    Removes the module object created from *def* from the interpreter state.
    Return `-1` with an exception set on error, `0` on success.

    The caller must have an attached thread state.

    Added in version 3.3.
