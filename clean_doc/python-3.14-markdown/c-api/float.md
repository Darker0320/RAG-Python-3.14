# Floating-Point Objects

typePyFloatObject
:   This subtype of `PyObject` represents a Python floating-point object.

PyTypeObjectPyFloat\_Type
:   *Part of the Stable ABI.*

    This instance of `PyTypeObject` represents the Python floating-point
    type. This is the same object as `float` in the Python layer.

intPyFloat\_Check(PyObject\*p)
:   Return true if its argument is a `PyFloatObject` or a subtype of
    `PyFloatObject`. This function always succeeds.

intPyFloat\_CheckExact(PyObject\*p)
:   Return true if its argument is a `PyFloatObject`, but not a subtype of
    `PyFloatObject`. This function always succeeds.

PyObject\*PyFloat\_FromString(PyObject\*str)
:   *Return value: New reference.* *Part of the Stable ABI.*

    Create a `PyFloatObject` object based on the string value in *str*, or
    `NULL` on failure.

PyObject\*PyFloat\_FromDouble(doublev)
:   *Return value: New reference.* *Part of the Stable ABI.*

    Create a `PyFloatObject` object from *v*, or `NULL` on failure.

doublePyFloat\_AsDouble(PyObject\*pyfloat)
:   *Part of the Stable ABI.*

    Return a C double representation of the contents of *pyfloat*. If
    *pyfloat* is not a Python floating-point object but has a `__float__()`
    method, this method will first be called to convert *pyfloat* into a float.
    If `__float__()` is not defined then it falls back to `__index__()`.
    This method returns `-1.0` upon failure, so one should call
    `PyErr_Occurred()` to check for errors.

    Changed in version 3.8: Use `__index__()` if available.

doublePyFloat\_AS\_DOUBLE(PyObject\*pyfloat)
:   Return a C double representation of the contents of *pyfloat*, but
    without error checking.

PyObject\*PyFloat\_GetInfo(void)
:   *Return value: New reference.* *Part of the Stable ABI.*

    Return a structseq instance which contains information about the
    precision, minimum and maximum values of a float. It’s a thin wrapper
    around the header file `float.h`.

doublePyFloat\_GetMax()
:   *Part of the Stable ABI.*

    Return the maximum representable finite float *DBL\_MAX* as C double.

doublePyFloat\_GetMin()
:   *Part of the Stable ABI.*

    Return the minimum normalized positive float *DBL\_MIN* as C double.

Py\_INFINITY
:   This macro expands to a constant expression of type double, that
    represents the positive infinity.

    On most platforms, this is equivalent to the `INFINITY` macro from
    the C11 standard `<math.h>` header.

Py\_NAN
:   This macro expands to a constant expression of type double, that
    represents a quiet not-a-number (qNaN) value.

    On most platforms, this is equivalent to the `NAN` macro from
    the C11 standard `<math.h>` header.

Py\_HUGE\_VAL
:   Equivalent to `INFINITY`.

    Deprecated since version 3.14: The macro is soft deprecated.

Py\_MATH\_E
:   The definition (accurate for a double type) of the `math.e` constant.

Py\_MATH\_El
:   High precision (long double) definition of `e` constant.

Py\_MATH\_PI
:   The definition (accurate for a double type) of the `math.pi` constant.

Py\_MATH\_PIl
:   High precision (long double) definition of `pi` constant.

Py\_MATH\_TAU
:   The definition (accurate for a double type) of the `math.tau` constant.

    Added in version 3.6.

Py\_RETURN\_NAN
:   Return `math.nan` from a function.

    On most platforms, this is equivalent to `return PyFloat_FromDouble(NAN)`.

Py\_RETURN\_INF(sign)
:   Return `math.inf` or `-math.inf` from a function,
    depending on the sign of *sign*.

    On most platforms, this is equivalent to the following:

    ```
    returnPyFloat_FromDouble(copysign(INFINITY,sign));
    ```

Py\_IS\_FINITE(X)
:   Return `1` if the given floating-point number *X* is finite,
    that is, it is normal, subnormal or zero, but not infinite or NaN.
    Return `0` otherwise.

    Deprecated since version 3.14: The macro is soft deprecated. Use `isfinite` instead.

Py\_IS\_INFINITY(X)
:   Return `1` if the given floating-point number *X* is positive or negative
    infinity. Return `0` otherwise.

    Deprecated since version 3.14: The macro is soft deprecated. Use `isinf` instead.

Py\_IS\_NAN(X)
:   Return `1` if the given floating-point number *X* is a not-a-number (NaN)
    value. Return `0` otherwise.

    Deprecated since version 3.14: The macro is soft deprecated. Use `isnan` instead.

## Pack and Unpack functions

The pack and unpack functions provide an efficient platform-independent way to
store floating-point values as byte strings. The Pack routines produce a bytes
string from a C double, and the Unpack routines produce a C
double from such a bytes string. The suffix (2, 4 or 8) specifies the
number of bytes in the bytes string.

On platforms that appear to use IEEE 754 formats these functions work by
copying bits. On other platforms, the 2-byte format is identical to the IEEE
754 binary16 half-precision format, the 4-byte format (32-bit) is identical to
the IEEE 754 binary32 single precision format, and the 8-byte format to the
IEEE 754 binary64 double precision format, although the packing of INFs and
NaNs (if such things exist on the platform) isn’t handled correctly, and
attempting to unpack a bytes string containing an IEEE INF or NaN will raise an
exception.

Note that NaN type may not be preserved on IEEE platforms (signaling NaNs become
quiet NaNs), for example on x86 systems in 32-bit mode.

On non-IEEE platforms with more precision, or larger dynamic range, than IEEE
754 supports, not all values can be packed; on non-IEEE platforms with less
precision, or smaller dynamic range, not all values can be unpacked. What
happens in such cases is partly accidental (alas).

Added in version 3.11.

### Pack functions

The pack routines write 2, 4 or 8 bytes, starting at *p*. *le* is an
int argument, non-zero if you want the bytes string in little-endian
format (exponent last, at `p+1`, `p+3`, or `p+6` and `p+7`), zero if you
want big-endian format (exponent first, at *p*). The `PY_BIG_ENDIAN`
constant can be used to use the native endian: it is equal to `1` on big
endian processor, or `0` on little endian processor.

Return value: `0` if all is OK, `-1` if error (and an exception is set,
most likely `OverflowError`).

There are two problems on non-IEEE platforms:

* What this does is undefined if *x* is a NaN or infinity.
* `-0.0` and `+0.0` produce the same bytes string.

intPyFloat\_Pack2(doublex, char\*p, intle)
:   Pack a C double as the IEEE 754 binary16 half-precision format.

intPyFloat\_Pack4(doublex, char\*p, intle)
:   Pack a C double as the IEEE 754 binary32 single precision format.

intPyFloat\_Pack8(doublex, char\*p, intle)
:   Pack a C double as the IEEE 754 binary64 double precision format.

### Unpack functions

The unpack routines read 2, 4 or 8 bytes, starting at *p*. *le* is an
int argument, non-zero if the bytes string is in little-endian format
(exponent last, at `p+1`, `p+3` or `p+6` and `p+7`), zero if big-endian
(exponent first, at *p*). The `PY_BIG_ENDIAN` constant can be used to
use the native endian: it is equal to `1` on big endian processor, or `0`
on little endian processor.

Return value: The unpacked double. On error, this is `-1.0` and
`PyErr_Occurred()` is true (and an exception is set, most likely
`OverflowError`).

Note that on a non-IEEE platform this will refuse to unpack a bytes string that
represents a NaN or infinity.

doublePyFloat\_Unpack2(constchar\*p, intle)
:   Unpack the IEEE 754 binary16 half-precision format as a C double.

doublePyFloat\_Unpack4(constchar\*p, intle)
:   Unpack the IEEE 754 binary32 single precision format as a C double.

doublePyFloat\_Unpack8(constchar\*p, intle)
:   Unpack the IEEE 754 binary64 double precision format as a C double.