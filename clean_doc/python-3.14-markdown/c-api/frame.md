# Frame objects

typePyFrameObject
:   *Part of the Limited API (as an opaque struct).*

    The C structure of the objects used to describe frame objects.

    There are no public members in this structure.

    Changed in version 3.11: The members of this structure were removed from the public C API.
    Refer to the What’s New entry
    for details.

The `PyEval_GetFrame()` and `PyThreadState_GetFrame()` functions
can be used to get a frame object.

See also Reflection.

PyTypeObjectPyFrame\_Type
:   The type of frame objects.
    It is the same object as `types.FrameType` in the Python layer.

    Changed in version 3.11: Previously, this type was only available after including
    `<frameobject.h>`.

PyFrameObject\*PyFrame\_New(PyThreadState\*tstate, PyCodeObject\*code, PyObject\*globals, PyObject\*locals)
:   Create a new frame object. This function returns a strong reference
    to the new frame object on success, and returns `NULL` with an exception
    set on failure.

intPyFrame\_Check(PyObject\*obj)
:   Return non-zero if *obj* is a frame object.

    Changed in version 3.11: Previously, this function was only available after including
    `<frameobject.h>`.

PyFrameObject\*PyFrame\_GetBack(PyFrameObject\*frame)
:   *Return value: New reference.*

    Get the *frame* next outer frame.

    Return a strong reference, or `NULL` if *frame* has no outer
    frame.
    This raises no exceptions.

    Added in version 3.9.

PyObject\*PyFrame\_GetBuiltins(PyFrameObject\*frame)
:   *Return value: New reference.*

    Get the *frame*’s `f_builtins` attribute.

    Return a strong reference. The result cannot be `NULL`.

    Added in version 3.11.

PyCodeObject\*PyFrame\_GetCode(PyFrameObject\*frame)
:   *Return value: New reference.* *Part of the Stable ABI since version 3.10.*

    Get the *frame* code.

    Return a strong reference.

    The result (frame code) cannot be `NULL`.

    Added in version 3.9.

PyObject\*PyFrame\_GetGenerator(PyFrameObject\*frame)
:   *Return value: New reference.*

    Get the generator, coroutine, or async generator that owns this frame,
    or `NULL` if this frame is not owned by a generator.
    Does not raise an exception, even if the return value is `NULL`.

    Return a strong reference, or `NULL`.

    Added in version 3.11.

PyObject\*PyFrame\_GetGlobals(PyFrameObject\*frame)
:   *Return value: New reference.*

    Get the *frame*’s `f_globals` attribute.

    Return a strong reference. The result cannot be `NULL`.

    Added in version 3.11.

intPyFrame\_GetLasti(PyFrameObject\*frame)
:   Get the *frame*’s `f_lasti` attribute.

    Returns -1 if `frame.f_lasti` is `None`.

    Added in version 3.11.

PyObject\*PyFrame\_GetVar(PyFrameObject\*frame, PyObject\*name)
:   *Return value: New reference.*

    Get the variable *name* of *frame*.

    * Return a strong reference to the variable value on success.
    * Raise `NameError` and return `NULL` if the variable does not exist.
    * Raise an exception and return `NULL` on error.

    *name* type must be a `str`.

    Added in version 3.12.

PyObject\*PyFrame\_GetVarString(PyFrameObject\*frame, constchar\*name)
:   *Return value: New reference.*

    Similar to `PyFrame_GetVar()`, but the variable name is a C string
    encoded in UTF-8.

    Added in version 3.12.

PyObject\*PyFrame\_GetLocals(PyFrameObject\*frame)
:   *Return value: New reference.*

    Get the *frame*’s `f_locals` attribute.
    If the frame refers to an optimized scope, this returns a
    write-through proxy object that allows modifying the locals.
    In all other cases (classes, modules, `exec()`, `eval()`) it returns
    the mapping representing the frame locals directly (as described for
    `locals()`).

    Return a strong reference.

    Added in version 3.11.

    Changed in version 3.13: As part of **PEP 667**, return an instance of `PyFrameLocalsProxy_Type`.

intPyFrame\_GetLineNumber(PyFrameObject\*frame)
:   *Part of the Stable ABI since version 3.10.*

    Return the line number that *frame* is currently executing.

## Frame locals proxies

Added in version 3.13.

The `f_locals` attribute on a frame object
is an instance of a “frame-locals proxy”. The proxy object exposes a
write-through view of the underlying locals dictionary for the frame. This
ensures that the variables exposed by `f_locals` are always up to date with
the live local variables in the frame itself.

See **PEP 667** for more information.

PyTypeObjectPyFrameLocalsProxy\_Type
:   The type of frame `locals()` proxy objects.

intPyFrameLocalsProxy\_Check(PyObject\*obj)
:   Return non-zero if *obj* is a frame `locals()` proxy.

## Legacy local variable APIs

These APIs are soft deprecated. As of Python 3.13, they do nothing.
They exist solely for backwards compatibility.

voidPyFrame\_LocalsToFast(PyFrameObject\*f, intclear)
:   Prior to Python 3.13, this function would copy the `f_locals`
    attribute of *f* to the internal “fast” array of local variables, allowing
    changes in frame objects to be visible to the interpreter. If *clear* was
    true, this function would process variables that were unset in the locals
    dictionary.

    Soft deprecated since version 3.13: This function now does nothing.

voidPyFrame\_FastToLocals(PyFrameObject\*f)
:   Prior to Python 3.13, this function would copy the internal “fast” array
    of local variables (which is used by the interpreter) to the
    `f_locals` attribute of *f*, allowing changes in local
    variables to be visible to frame objects.

    Soft deprecated since version 3.13: This function now does nothing.

intPyFrame\_FastToLocalsWithError(PyFrameObject\*f)
:   Prior to Python 3.13, this function was similar to
    `PyFrame_FastToLocals()`, but would return `0` on success, and
    `-1` with an exception set on failure.

    Soft deprecated since version 3.13: This function now does nothing.

See also

**PEP 667**

## Internal frames

Unless using **PEP 523**, you will not need this.

struct\_PyInterpreterFrame
:   The interpreter’s internal frame representation.

    Added in version 3.11.

PyObject\*PyUnstable\_InterpreterFrame\_GetCode(struct\_PyInterpreterFrame\*frame);
:   *This is Unstable API. It may change without warning in minor releases.*

    > Return a strong reference to the code object for the frame.

    Added in version 3.12.

intPyUnstable\_InterpreterFrame\_GetLasti(struct\_PyInterpreterFrame\*frame);
:   *This is Unstable API. It may change without warning in minor releases.*

    Return the byte offset into the last executed instruction.

    Added in version 3.12.

intPyUnstable\_InterpreterFrame\_GetLine(struct\_PyInterpreterFrame\*frame);
:   *This is Unstable API. It may change without warning in minor releases.*

    Return the currently executing line number, or -1 if there is no line number.

    Added in version 3.12.