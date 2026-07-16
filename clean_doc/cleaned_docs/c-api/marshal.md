# Data marshalling support

These routines allow C code to work with serialized objects using the same
data format as the `marshal` module. There are functions to write data
into the serialization format, and additional functions that can be used to
read the data back. Files used to store marshalled data must be opened in
binary mode.

Numeric values are stored with the least significant byte first.

The module supports several versions of the data format; see
the `Python module documentation` for details.

Py\_MARSHAL\_VERSION
The current format version. See `marshal.version`.

voidPyMarshal\_WriteLongToFile(longvalue, FILE\*file, intversion)
Marshal a long integer, *value*, to *file*. This will only write
    the least-significant 32 bits of *value*; regardless of the size of the
    native long type. *version* indicates the file format.

    This function can fail, in which case it sets the error indicator.
    Use `PyErr_Occurred()` to check for that.

voidPyMarshal\_WriteObjectToFile(PyObject\*value, FILE\*file, intversion)
Marshal a Python object, *value*, to *file*.
    *version* indicates the file format.

    This function can fail, in which case it sets the error indicator.
    Use `PyErr_Occurred()` to check for that.

PyObject\*PyMarshal\_WriteObjectToString(PyObject\*value, intversion)
*Return value: New reference.*

    Return a bytes object containing the marshalled representation of *value*.
    *version* indicates the file format.

The following functions allow marshalled values to be read back in.

longPyMarshal\_ReadLongFromFile(FILE\*file)
Return a C long from the data stream in a FILE\* opened
    for reading. Only a 32-bit value can be read in using this function,
    regardless of the native size of long.

    On error, sets the appropriate exception (`EOFError`) and returns
    `-1`.

intPyMarshal\_ReadShortFromFile(FILE\*file)
Return a C short from the data stream in a FILE\* opened
    for reading. Only a 16-bit value can be read in using this function,
    regardless of the native size of short.

    On error, sets the appropriate exception (`EOFError`) and returns
    `-1`.

PyObject\*PyMarshal\_ReadObjectFromFile(FILE\*file)
*Return value: New reference.*

    Return a Python object from the data stream in a FILE\* opened for
    reading.

    On error, sets the appropriate exception (`EOFError`, `ValueError`
    or `TypeError`) and returns `NULL`.

PyObject\*PyMarshal\_ReadLastObjectFromFile(FILE\*file)
*Return value: New reference.*

    Return a Python object from the data stream in a FILE\* opened for
    reading. Unlike `PyMarshal_ReadObjectFromFile()`, this function
    assumes that no further objects will be read from the file, allowing it to
    aggressively load file data into memory so that the de-serialization can
    operate from data in memory rather than reading a byte at a time from the
    file. Only use this variant if you are certain that you won’t be reading
    anything else from the file.

    On error, sets the appropriate exception (`EOFError`, `ValueError`
    or `TypeError`) and returns `NULL`.

PyObject\*PyMarshal\_ReadObjectFromString(constchar\*data, Py\_ssize\_tlen)
*Return value: New reference.*

    Return a Python object from the data stream in a byte buffer
    containing *len* bytes pointed to by *data*.

    On error, sets the appropriate exception (`EOFError`, `ValueError`
    or `TypeError`) and returns `NULL`.
