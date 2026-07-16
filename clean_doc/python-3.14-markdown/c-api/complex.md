# Complex Number Objects

Python’s complex number objects are implemented as two distinct types when
viewed from the C API: one is the Python object exposed to Python programs, and
the other is a C structure which represents the actual complex number value.
The API provides functions for working with both.

## Complex Numbers as C Structures

Note that the functions which accept these structures as parameters and return
them as results do so *by value* rather than dereferencing them through
pointers. This is consistent throughout the API.

typePy\_complex
:   The C structure which corresponds to the value portion of a Python complex
    number object. Most of the functions for dealing with complex number objects
    use structures of this type as input or output values, as appropriate.

    doublereal

    doubleimag

    The structure is defined as:

    ```
    typedefstruct{
    doublereal;
    doubleimag;
    }Py_complex;
    ```

Py\_complex\_Py\_c\_sum(Py\_complexleft, Py\_complexright)
:   Return the sum of two complex numbers, using the C `Py_complex`
    representation.

Py\_complex\_Py\_c\_diff(Py\_complexleft, Py\_complexright)
:   Return the difference between two complex numbers, using the C
    `Py_complex` representation.

Py\_complex\_Py\_c\_neg(Py\_complexnum)
:   Return the negation of the complex number *num*, using the C
    `Py_complex` representation.

Py\_complex\_Py\_c\_prod(Py\_complexleft, Py\_complexright)
:   Return the product of two complex numbers, using the C `Py_complex`
    representation.

Py\_complex\_Py\_c\_quot(Py\_complexdividend, Py\_complexdivisor)
:   Return the quotient of two complex numbers, using the C `Py_complex`
    representation.

    If *divisor* is null, this method returns zero and sets
    `errno` to `EDOM`.

Py\_complex\_Py\_c\_pow(Py\_complexnum, Py\_complexexp)
:   Return the exponentiation of *num* by *exp*, using the C `Py_complex`
    representation.

    If *num* is null and *exp* is not a positive real number,
    this method returns zero and sets `errno` to `EDOM`.

    Set `errno` to `ERANGE` on overflows.

## Complex Numbers as Python Objects

typePyComplexObject
:   This subtype of `PyObject` represents a Python complex number object.

PyTypeObjectPyComplex\_Type
:   *Part of the Stable ABI.*

    This instance of `PyTypeObject` represents the Python complex number
    type. It is the same object as `complex` in the Python layer.

intPyComplex\_Check(PyObject\*p)
:   Return true if its argument is a `PyComplexObject` or a subtype of
    `PyComplexObject`. This function always succeeds.

intPyComplex\_CheckExact(PyObject\*p)
:   Return true if its argument is a `PyComplexObject`, but not a subtype of
    `PyComplexObject`. This function always succeeds.

PyObject\*PyComplex\_FromCComplex(Py\_complexv)
:   *Return value: New reference.*

    Create a new Python complex number object from a C `Py_complex` value.
    Return `NULL` with an exception set on error.

PyObject\*PyComplex\_FromDoubles(doublereal, doubleimag)
:   *Return value: New reference.* *Part of the Stable ABI.*

    Return a new `PyComplexObject` object from *real* and *imag*.
    Return `NULL` with an exception set on error.

doublePyComplex\_RealAsDouble(PyObject\*op)
:   *Part of the Stable ABI.*

    Return the real part of *op* as a C double.

    If *op* is not a Python complex number object but has a
    `__complex__()` method, this method will first be called to
    convert *op* to a Python complex number object. If `__complex__()` is
    not defined then it falls back to call `PyFloat_AsDouble()` and
    returns its result.

    Upon failure, this method returns `-1.0` with an exception set, so one
    should call `PyErr_Occurred()` to check for errors.

    Changed in version 3.13: Use `__complex__()` if available.

doublePyComplex\_ImagAsDouble(PyObject\*op)
:   *Part of the Stable ABI.*

    Return the imaginary part of *op* as a C double.

    If *op* is not a Python complex number object but has a
    `__complex__()` method, this method will first be called to
    convert *op* to a Python complex number object. If `__complex__()` is
    not defined then it falls back to call `PyFloat_AsDouble()` and
    returns `0.0` on success.

    Upon failure, this method returns `-1.0` with an exception set, so one
    should call `PyErr_Occurred()` to check for errors.

    Changed in version 3.13: Use `__complex__()` if available.

Py\_complexPyComplex\_AsCComplex(PyObject\*op)
:   Return the `Py_complex` value of the complex number *op*.

    If *op* is not a Python complex number object but has a `__complex__()`
    method, this method will first be called to convert *op* to a Python complex
    number object. If `__complex__()` is not defined then it falls back to
    `__float__()`. If `__float__()` is not defined then it falls back
    to `__index__()`.

    Upon failure, this method returns `Py_complex`
    with `real` set to `-1.0` and with an exception set, so one
    should call `PyErr_Occurred()` to check for errors.

    Changed in version 3.8: Use `__index__()` if available.