# Iterator Objects

Python provides two general-purpose iterator objects. The first, a sequence
iterator, works with an arbitrary sequence supporting the `__getitem__()`
method. The second works with a callable object and a sentinel value, calling
the callable for each item in the sequence, and ending the iteration when the
sentinel value is returned.

PyTypeObjectPySeqIter\_Type
*Part of the Stable ABI.*

    Type object for iterator objects returned by `PySeqIter_New()` and the
    one-argument form of the `iter()` built-in function for built-in sequence
    types.

intPySeqIter\_Check(PyObject\*op)
Return true if the type of *op* is `PySeqIter_Type`. This function
    always succeeds.

PyObject\*PySeqIter\_New(PyObject\*seq)
*Return value: New reference.* *Part of the Stable ABI.*

    Return an iterator that works with a general sequence object, *seq*. The
    iteration ends when the sequence raises `IndexError` for the subscripting
    operation.

PyTypeObjectPyCallIter\_Type
*Part of the Stable ABI.*

    Type object for iterator objects returned by `PyCallIter_New()` and the
    two-argument form of the `iter()` built-in function.

intPyCallIter\_Check(PyObject\*op)
Return true if the type of *op* is `PyCallIter_Type`. This
    function always succeeds.

PyObject\*PyCallIter\_New(PyObject\*callable, PyObject\*sentinel)
*Return value: New reference.* *Part of the Stable ABI.*

    Return a new iterator. The first parameter, *callable*, can be any Python
    callable object that can be called with no parameters; each call to it should
    return the next item in the iteration. When *callable* returns a value equal to
    *sentinel*, the iteration will be terminated.

## Range Objects

PyTypeObjectPyRange\_Type
*Part of the Stable ABI.*

    The type object for `range` objects.

intPyRange\_Check(PyObject\*o)
Return true if the object *o* is an instance of a `range` object.
    This function always succeeds.

## Builtin Iterator Types

These are built-in iteration types that are included in Python’s C API, but
provide no additional functions. They are here for completeness.

| C type | Python type |
| --- | --- |
| PyTypeObjectPyEnum\_Type  *Part of the Stable ABI.* | `enumerate` |
| PyTypeObjectPyFilter\_Type  *Part of the Stable ABI.* | `filter` |
| PyTypeObjectPyMap\_Type  *Part of the Stable ABI.* | `map` |
| PyTypeObjectPyReversed\_Type  *Part of the Stable ABI.* | `reversed` |
| PyTypeObjectPyZip\_Type  *Part of the Stable ABI.* | `zip` |

## Other Iterator Objects

PyTypeObjectPyByteArrayIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyBytesIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyListIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyListRevIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPySetIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyTupleIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyRangeIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyLongRangeIter\_Type
*Part of the Stable ABI.*

PyTypeObjectPyDictIterKey\_Type
*Part of the Stable ABI.*

PyTypeObjectPyDictRevIterKey\_Type
*Part of the Stable ABI since version 3.8.*

PyTypeObjectPyDictIterValue\_Type
*Part of the Stable ABI.*

PyTypeObjectPyDictRevIterValue\_Type
*Part of the Stable ABI since version 3.8.*

PyTypeObjectPyDictIterItem\_Type
*Part of the Stable ABI.*

PyTypeObjectPyDictRevIterItem\_Type
*Part of the Stable ABI since version 3.8.*

PyTypeObjectPyODictIter\_Type
Type objects for iterators of various built-in objects.

    Do not create instances of these directly; prefer calling
    `PyObject_GetIter()` instead.

    Note that there is no guarantee that a given built-in type uses a given iterator
    type. For example, iterating over `range` will use one of two iterator
    types depending on the size of the range. Other types may start using a
    similar scheme in the future, without warning.
