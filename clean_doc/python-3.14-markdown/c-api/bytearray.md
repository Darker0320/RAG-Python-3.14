# Byte Array Objects

typePyByteArrayObject
:   This subtype of `PyObject` represents a Python bytearray object.

PyTypeObjectPyByteArray\_Type
:   *Part of the Stable ABI.*

    This instance of `PyTypeObject` represents the Python bytearray type;
    it is the same object as `bytearray` in the Python layer.

## Type check macros

intPyByteArray\_Check(PyObject\*o)
:   Return true if the object *o* is a bytearray object or an instance of a
    subtype of the bytearray type. This function always succeeds.

intPyByteArray\_CheckExact(PyObject\*o)
:   Return true if the object *o* is a bytearray object, but not an instance of a
    subtype of the bytearray type. This function always succeeds.

## Direct API functions

PyObject\*PyByteArray\_FromObject(PyObject\*o)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Return a new bytearray object from any object, *o*, that implements the
    buffer protocol.

    On failure, return `NULL` with an exception set.

    Note

    If the object implements the buffer protocol, then the buffer
    must not be mutated while the bytearray object is being created.

PyObject\*PyByteArray\_FromStringAndSize(constchar\*string, Py\_ssize\_tlen)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Atomic.*

    Create a new bytearray object from *string* and its length, *len*.

    On failure, return `NULL` with an exception set.

PyObject\*PyByteArray\_Concat(PyObject\*a, PyObject\*b)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Concat bytearrays *a* and *b* and return a new bytearray with the result.

    On failure, return `NULL` with an exception set.

    Note

    If the object implements the buffer protocol, then the buffer
    must not be mutated while the bytearray object is being created.

Py\_ssize\_tPyByteArray\_Size(PyObject\*bytearray)
:   *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return the size of *bytearray* after checking for a `NULL` pointer.

char\*PyByteArray\_AsString(PyObject\*bytearray)
:   *Part of the Stable ABI.* *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Return the contents of *bytearray* as a char array after checking for a
    `NULL` pointer. The returned array always has an extra
    null byte appended.

    Note

    It is not thread-safe to mutate the bytearray object while using the returned char array.

intPyByteArray\_Resize(PyObject\*bytearray, Py\_ssize\_tlen)
:   *Part of the Stable ABI.*

    Resize the internal buffer of *bytearray* to *len*.
    Failure is a `-1` return with an exception set.

    Changed in version 3.14: A negative *len* will now result in an exception being set and -1 returned.

## Macros

These macros trade safety for speed and they don’t check pointers.

char\*PyByteArray\_AS\_STRING(PyObject\*bytearray)
:   *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Similar to `PyByteArray_AsString()`, but without error checking.

    Note

    It is not thread-safe to mutate the bytearray object while using the returned char array.

Py\_ssize\_tPyByteArray\_GET\_SIZE(PyObject\*bytearray)
:   *Thread safety: Atomic.*

    Similar to `PyByteArray_Size()`, but without error checking.