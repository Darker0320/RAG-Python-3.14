# Codec registry and support functions

intPyCodec\_Register(PyObject\*search\_function)
*Part of the Stable ABI.*

    Register a new codec search function.

    As a side effect, this tries to load the `encodings` package, if not yet
    done, to make sure that it is always first in the list of search functions.

intPyCodec\_Unregister(PyObject\*search\_function)
*Part of the Stable ABI since version 3.10.*

    Unregister a codec search function and clear the registry’s cache.
    If the search function is not registered, do nothing.
    Return 0 on success. Raise an exception and return -1 on error.

    Added in version 3.10.

intPyCodec\_KnownEncoding(constchar\*encoding)
*Part of the Stable ABI.*

    Return `1` or `0` depending on whether there is a registered codec for
    the given *encoding*. This function always succeeds.

PyObject\*PyCodec\_Encode(PyObject\*object, constchar\*encoding, constchar\*errors)
*Return value: New reference.* *Part of the Stable ABI.*

    Generic codec based encoding API.

    *object* is passed through the encoder function found for the given
    *encoding* using the error handling method defined by *errors*. *errors* may
    be `NULL` to use the default method defined for the codec. Raises a
    `LookupError` if no encoder can be found.

PyObject\*PyCodec\_Decode(PyObject\*object, constchar\*encoding, constchar\*errors)
*Return value: New reference.* *Part of the Stable ABI.*

    Generic codec based decoding API.

    *object* is passed through the decoder function found for the given
    *encoding* using the error handling method defined by *errors*. *errors* may
    be `NULL` to use the default method defined for the codec. Raises a
    `LookupError` if no decoder can be found.

## Codec lookup API

In the following functions, the *encoding* string is looked up converted to all
lower-case characters, which makes encodings looked up through this mechanism
effectively case-insensitive. If no codec is found, a `KeyError` is set
and `NULL` returned.

PyObject\*PyCodec\_Encoder(constchar\*encoding)
*Return value: New reference.* *Part of the Stable ABI.*

    Get an encoder function for the given *encoding*.

PyObject\*PyCodec\_Decoder(constchar\*encoding)
*Return value: New reference.* *Part of the Stable ABI.*

    Get a decoder function for the given *encoding*.

PyObject\*PyCodec\_IncrementalEncoder(constchar\*encoding, constchar\*errors)
*Return value: New reference.* *Part of the Stable ABI.*

    Get an `IncrementalEncoder` object for the given *encoding*.

PyObject\*PyCodec\_IncrementalDecoder(constchar\*encoding, constchar\*errors)
*Return value: New reference.* *Part of the Stable ABI.*

    Get an `IncrementalDecoder` object for the given *encoding*.

PyObject\*PyCodec\_StreamReader(constchar\*encoding, PyObject\*stream, constchar\*errors)
*Return value: New reference.* *Part of the Stable ABI.*

    Get a `StreamReader` factory function for the given *encoding*.

PyObject\*PyCodec\_StreamWriter(constchar\*encoding, PyObject\*stream, constchar\*errors)
*Return value: New reference.* *Part of the Stable ABI.*

    Get a `StreamWriter` factory function for the given *encoding*.

## Registry API for Unicode encoding error handlers

intPyCodec\_RegisterError(constchar\*name, PyObject\*error)
*Part of the Stable ABI.*

    Register the error handling callback function *error* under the given *name*.
    This callback function will be called by a codec when it encounters
    unencodable characters/undecodable bytes and *name* is specified as the error
    parameter in the call to the encode/decode function.

    The callback gets a single argument, an instance of
    `UnicodeEncodeError`, `UnicodeDecodeError` or
    `UnicodeTranslateError` that holds information about the problematic
    sequence of characters or bytes and their offset in the original string (see
    Unicode Exception Objects for functions to extract this information). The
    callback must either raise the given exception, or return a two-item tuple
    containing the replacement for the problematic sequence, and an integer
    giving the offset in the original string at which encoding/decoding should be
    resumed.

    Return `0` on success, `-1` on error.

PyObject\*PyCodec\_LookupError(constchar\*name)
*Return value: New reference.* *Part of the Stable ABI.*

    Lookup the error handling callback function registered under *name*. As a
    special case `NULL` can be passed, in which case the error handling callback
    for “strict” will be returned.

PyObject\*PyCodec\_StrictErrors(PyObject\*exc)
*Return value: Always NULL.* *Part of the Stable ABI.*

    Raise *exc* as an exception.

PyObject\*PyCodec\_IgnoreErrors(PyObject\*exc)
*Return value: New reference.* *Part of the Stable ABI.*

    Ignore the unicode error, skipping the faulty input.

PyObject\*PyCodec\_ReplaceErrors(PyObject\*exc)
*Return value: New reference.* *Part of the Stable ABI.*

    Replace the unicode encode error with `?` or `U+FFFD`.

PyObject\*PyCodec\_XMLCharRefReplaceErrors(PyObject\*exc)
*Return value: New reference.* *Part of the Stable ABI.*

    Replace the unicode encode error with XML character references.

PyObject\*PyCodec\_BackslashReplaceErrors(PyObject\*exc)
*Return value: New reference.* *Part of the Stable ABI.*

    Replace the unicode encode error with backslash escapes (`\x`, `\u` and
    `\U`).

PyObject\*PyCodec\_NameReplaceErrors(PyObject\*exc)
*Return value: New reference.* *Part of the Stable ABI since version 3.7.*

    Replace the unicode encode error with `\N{...}` escapes.

    Added in version 3.5.

## Codec utility variables

constchar\*Py\_hexdigits
A string constant containing the lowercase hexadecimal digits: `"0123456789abcdef"`.

    Added in version 3.3.
