# Dictionary Objects

typePyDictObject
:   This subtype of `PyObject` represents a Python dictionary object.

PyTypeObjectPyDict\_Type
:   *Part of the Stable ABI.*

    This instance of `PyTypeObject` represents the Python dictionary
    type. This is the same object as `dict` in the Python layer.

intPyDict\_Check(PyObject\*p)
:   *Thread safety: Atomic.*

    Return true if *p* is a dict object or an instance of a subtype of the dict
    type. This function always succeeds.

intPyDict\_CheckExact(PyObject\*p)
:   *Thread safety: Atomic.*

    Return true if *p* is a dict object, but not an instance of a subtype of
    the dict type. This function always succeeds.

PyObject\*PyDict\_New()
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return a new empty dictionary, or `NULL` on failure.

PyObject\*PyDictProxy\_New(PyObject\*mapping)
:   *Return value: New reference.* *Part of the Stable ABI.*

    Return a `types.MappingProxyType` object for a mapping which
    enforces read-only behavior. This is normally used to create a view to
    prevent modification of the dictionary for non-dynamic class types.

PyTypeObjectPyDictProxy\_Type
:   *Part of the Stable ABI.*

    The type object for mapping proxy objects created by
    `PyDictProxy_New()` and for the read-only `__dict__` attribute
    of many built-in types. A `PyDictProxy_Type` instance provides a
    dynamic, read-only view of an underlying dictionary: changes to the
    underlying dictionary are reflected in the proxy, but the proxy itself
    does not support mutation operations. This corresponds to
    `types.MappingProxyType` in Python.

voidPyDict\_Clear(PyObject\*p)
:   *Part of the Stable ABI.* *Thread safety: Atomic.*

    Empty an existing dictionary of all key-value pairs.

intPyDict\_Contains(PyObject\*p, PyObject\*key)
:   *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Determine if dictionary *p* contains *key*. If an item in *p* matches
    *key*, return `1`, otherwise return `0`. On error, return `-1`.
    This is equivalent to the Python expression `key in p`.

    Note

    The operation is atomic on free threading
    when *key* is `str`, `int`, `float`, `bool` or `bytes`.

intPyDict\_ContainsString(PyObject\*p, constchar\*key)
:   *Thread safety: Atomic.*

    This is the same as `PyDict_Contains()`, but *key* is specified as a
    constchar\* UTF-8 encoded bytes string, rather than a
    PyObject\*.

    Added in version 3.13.

PyObject\*PyDict\_Copy(PyObject\*p)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return a new dictionary that contains the same key-value pairs as *p*.

intPyDict\_SetItem(PyObject\*p, PyObject\*key, PyObject\*val)
:   *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Insert *val* into the dictionary *p* with a key of *key*. *key* must be
    hashable; if it isn’t, `TypeError` will be raised. Return
    `0` on success or `-1` on failure.
    This function *does not* “steal” a reference to *val*.

    Note

    The operation is atomic on free threading
    when *key* is `str`, `int`, `float`, `bool` or `bytes`.

intPyDict\_SetItemString(PyObject\*p, constchar\*key, PyObject\*val)
:   *Part of the Stable ABI.* *Thread safety: Atomic.*

    This is the same as `PyDict_SetItem()`, but *key* is
    specified as a constchar\* UTF-8 encoded bytes string,
    rather than a PyObject\*.

intPyDict\_DelItem(PyObject\*p, PyObject\*key)
:   *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Remove the entry in dictionary *p* with key *key*. *key* must be hashable;
    if it isn’t, `TypeError` is raised.
    If *key* is not in the dictionary, `KeyError` is raised.
    Return `0` on success or `-1` on failure.

    Note

    The operation is atomic on free threading
    when *key* is `str`, `int`, `float`, `bool` or `bytes`.

intPyDict\_DelItemString(PyObject\*p, constchar\*key)
:   *Part of the Stable ABI.* *Thread safety: Atomic.*

    This is the same as `PyDict_DelItem()`, but *key* is
    specified as a constchar\* UTF-8 encoded bytes string,
    rather than a PyObject\*.

intPyDict\_GetItemRef(PyObject\*p, PyObject\*key, PyObject\*\*result)
:   *Part of the Stable ABI since version 3.13.* *Thread safety: Safe for concurrent use on the same object.*

    Return a new strong reference to the object from dictionary *p*
    which has a key *key*:

    * If the key is present, set *\*result* to a new strong reference
      to the value and return `1`.
    * If the key is missing, set *\*result* to `NULL` and return `0`.
    * On error, raise an exception, set *\*result* to `NULL` and return `-1`.

    Note

    The operation is atomic on free threading
    when *key* is `str`, `int`, `float`, `bool` or `bytes`.

    Added in version 3.13.

    See also the `PyObject_GetItem()` function.

PyObject\*PyDict\_GetItem(PyObject\*p, PyObject\*key)
:   *Return value: Borrowed reference.* *Part of the Stable ABI.* *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Return a borrowed reference to the object from dictionary *p* which
    has a key *key*. Return `NULL` if the key *key* is missing *without*
    setting an exception.

    Note

    Exceptions that occur while this calls `__hash__()` and
    `__eq__()` methods are silently ignored.
    Prefer the `PyDict_GetItemWithError()` function instead.

    Note

    In the free-threaded build, the returned
    borrowed reference may become invalid if another thread modifies
    the dictionary concurrently. Prefer `PyDict_GetItemRef()`, which
    returns a strong reference.

    Changed in version 3.10: Calling this API without an attached thread state had been allowed for historical
    reason. It is no longer allowed.

PyObject\*PyDict\_GetItemWithError(PyObject\*p, PyObject\*key)
:   *Return value: Borrowed reference.* *Part of the Stable ABI.* *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Variant of `PyDict_GetItem()` that does not suppress
    exceptions. Return `NULL` **with** an exception set if an exception
    occurred. Return `NULL` **without** an exception set if the key
    wasn’t present.

    Note

    In the free-threaded build, the returned
    borrowed reference may become invalid if another thread modifies
    the dictionary concurrently. Prefer `PyDict_GetItemRef()`, which
    returns a strong reference.

PyObject\*PyDict\_GetItemString(PyObject\*p, constchar\*key)
:   *Return value: Borrowed reference.* *Part of the Stable ABI.* *Thread safety: Safe to call from multiple threads with external synchronization only.*

    This is the same as `PyDict_GetItem()`, but *key* is specified as a
    constchar\* UTF-8 encoded bytes string, rather than a
    PyObject\*.

    Note

    Exceptions that occur while this calls `__hash__()` and
    `__eq__()` methods or while creating the temporary `str`
    object are silently ignored.
    Prefer using the `PyDict_GetItemWithError()` function with your own
    `PyUnicode_FromString()` *key* instead.

    Note

    In the free-threaded build, the returned
    borrowed reference may become invalid if another thread modifies
    the dictionary concurrently. Prefer `PyDict_GetItemStringRef()`,
    which returns a strong reference.

intPyDict\_GetItemStringRef(PyObject\*p, constchar\*key, PyObject\*\*result)
:   *Part of the Stable ABI since version 3.13.* *Thread safety: Atomic.*

    Similar to `PyDict_GetItemRef()`, but *key* is specified as a
    constchar\* UTF-8 encoded bytes string, rather than a
    PyObject\*.

    Added in version 3.13.

PyObject\*PyDict\_SetDefault(PyObject\*p, PyObject\*key, PyObject\*defaultobj)
:   *Return value: Borrowed reference.* *Thread safety: Safe to call from multiple threads with external synchronization only.*

    This is the same as the Python-level `dict.setdefault()`. If present, it
    returns the value corresponding to *key* from the dictionary *p*. If the key
    is not in the dict, it is inserted with value *defaultobj* and *defaultobj*
    is returned. This function evaluates the hash function of *key* only once,
    instead of evaluating it independently for the lookup and the insertion.

    Added in version 3.4.

    Note

    In the free-threaded build, the returned
    borrowed reference may become invalid if another thread modifies
    the dictionary concurrently. Prefer `PyDict_SetDefaultRef()`,
    which returns a strong reference.

intPyDict\_SetDefaultRef(PyObject\*p, PyObject\*key, PyObject\*default\_value, PyObject\*\*result)
:   *Thread safety: Safe for concurrent use on the same object.*

    Inserts *default\_value* into the dictionary *p* with a key of *key* if the
    key is not already present in the dictionary. If *result* is not `NULL`,
    then *\*result* is set to a strong reference to either
    *default\_value*, if the key was not present, or the existing value, if *key*
    was already present in the dictionary.
    Returns `1` if the key was present and *default\_value* was not inserted,
    or `0` if the key was not present and *default\_value* was inserted.
    On failure, returns `-1`, sets an exception, and sets `*result`
    to `NULL`.

    For clarity: if you have a strong reference to *default\_value* before
    calling this function, then after it returns, you hold a strong reference
    to both *default\_value* and *\*result* (if it’s not `NULL`).
    These may refer to the same object: in that case you hold two separate
    references to it.

    Note

    The operation is atomic on free threading
    when *key* is `str`, `int`, `float`, `bool` or `bytes`.

    Added in version 3.13.

intPyDict\_Pop(PyObject\*p, PyObject\*key, PyObject\*\*result)
:   *Thread safety: Safe for concurrent use on the same object.*

    Remove *key* from dictionary *p* and optionally return the removed value.
    Do not raise `KeyError` if the key is missing.

    * If the key is present, set *\*result* to a new reference to the removed
      value if *result* is not `NULL`, and return `1`.
    * If the key is missing, set *\*result* to `NULL` if *result* is not
      `NULL`, and return `0`.
    * On error, raise an exception and return `-1`.

    Similar to `dict.pop()`, but without the default value and
    not raising `KeyError` if the key is missing.

    Note

    The operation is atomic on free threading
    when *key* is `str`, `int`, `float`, `bool` or `bytes`.

    Added in version 3.13.

intPyDict\_PopString(PyObject\*p, constchar\*key, PyObject\*\*result)
:   *Thread safety: Atomic.*

    Similar to `PyDict_Pop()`, but *key* is specified as a
    constchar\* UTF-8 encoded bytes string, rather than a
    PyObject\*.

    Added in version 3.13.

PyObject\*PyDict\_Items(PyObject\*p)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return a `PyListObject` containing all the items from the dictionary.

PyObject\*PyDict\_Keys(PyObject\*p)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return a `PyListObject` containing all the keys from the dictionary.

PyObject\*PyDict\_Values(PyObject\*p)
:   *Return value: New reference.* *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return a `PyListObject` containing all the values from the dictionary
    *p*.

Py\_ssize\_tPyDict\_Size(PyObject\*p)
:   *Part of the Stable ABI.* *Thread safety: Atomic.*

    Return the number of items in the dictionary. This is equivalent to
    `len(p)` on a dictionary.

Py\_ssize\_tPyDict\_GET\_SIZE(PyObject\*p)
:   *Thread safety: Atomic.*

    Similar to `PyDict_Size()`, but without error checking.

intPyDict\_Next(PyObject\*p, Py\_ssize\_t\*ppos, PyObject\*\*pkey, PyObject\*\*pvalue)
:   *Part of the Stable ABI.* *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Iterate over all key-value pairs in the dictionary *p*. The
    `Py_ssize_t` referred to by *ppos* must be initialized to `0`
    prior to the first call to this function to start the iteration; the
    function returns true for each pair in the dictionary, and false once all
    pairs have been reported. The parameters *pkey* and *pvalue* should either
    point to PyObject\* variables that will be filled in with each key
    and value, respectively, or may be `NULL`. Any references returned through
    them are borrowed. *ppos* should not be altered during iteration. Its
    value represents offsets within the internal dictionary structure, and
    since the structure is sparse, the offsets are not consecutive.

    For example:

    ```
    PyObject*key,*value;
    Py_ssize_tpos=0;

    while(PyDict_Next(self->dict,&pos,&key,&value)){
    /* do something interesting with the values... */
    ...
    }
    ```

    The dictionary *p* should not be mutated during iteration. It is safe to
    modify the values of the keys as you iterate over the dictionary, but only
    so long as the set of keys does not change. For example:

    ```
    PyObject*key,*value;
    Py_ssize_tpos=0;

    while(PyDict_Next(self->dict,&pos,&key,&value)){
    longi=PyLong_AsLong(value);
    if(i==-1&&PyErr_Occurred()){
    return-1;
    }
    PyObject*o=PyLong_FromLong(i+1);
    if(o==NULL)
    return-1;
    if(PyDict_SetItem(self->dict,key,o)<0){
    Py_DECREF(o);
    return-1;
    }
    Py_DECREF(o);
    }
    ```

    The function is not thread-safe in the free-threaded
    build without external synchronization. You can use
    `Py_BEGIN_CRITICAL_SECTION` to lock the dictionary while iterating
    over it:

    ```
    Py_BEGIN_CRITICAL_SECTION(self->dict);
    while(PyDict_Next(self->dict,&pos,&key,&value)){
    ...
    }
    Py_END_CRITICAL_SECTION();
    ```

    Note

    On the free-threaded build, this function can be used safely inside a
    critical section. However, the references returned for *pkey* and *pvalue*
    are borrowed and are only valid while the
    critical section is held. If you need to use these objects outside the
    critical section or when the critical section can be suspended, create a
    strong reference (for example, using
    `Py_NewRef()`).

intPyDict\_Merge(PyObject\*a, PyObject\*b, intoverride)
:   *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Iterate over mapping object *b* adding key-value pairs to dictionary *a*.
    *b* may be a dictionary, or any object supporting `PyMapping_Keys()`
    and `PyObject_GetItem()`. If *override* is true, existing pairs in *a*
    will be replaced if a matching key is found in *b*, otherwise pairs will
    only be added if there is not a matching key in *a*. Return `0` on
    success or `-1` if an exception was raised.

    Note

    In the free-threaded build, when *b* is a
    `dict` (with the standard iterator), both *a* and *b* are locked
    for the duration of the operation. When *b* is a non-dict mapping, only
    *a* is locked; *b* may be concurrently modified by another thread.

intPyDict\_Update(PyObject\*a, PyObject\*b)
:   *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    This is the same as `PyDict_Merge(a, b, 1)` in C, and is similar to
    `a.update(b)` in Python except that `PyDict_Update()` doesn’t fall
    back to the iterating over a sequence of key value pairs if the second
    argument has no “keys” attribute. Return `0` on success or `-1` if an
    exception was raised.

    Note

    In the free-threaded build, when *b* is a
    `dict` (with the standard iterator), both *a* and *b* are locked
    for the duration of the operation. When *b* is a non-dict mapping, only
    *a* is locked; *b* may be concurrently modified by another thread.

intPyDict\_MergeFromSeq2(PyObject\*a, PyObject\*seq2, intoverride)
:   *Part of the Stable ABI.* *Thread safety: Safe for concurrent use on the same object.*

    Update or merge into dictionary *a*, from the key-value pairs in *seq2*.
    *seq2* must be an iterable object producing iterable objects of length 2,
    viewed as key-value pairs. In case of duplicate keys, the last wins if
    *override* is true, else the first wins. Return `0` on success or `-1`
    if an exception was raised. Equivalent Python (except for the return
    value):

    ```
    defPyDict_MergeFromSeq2(a,seq2,override):
    forkey,valueinseq2:
    ifoverrideorkeynotina:
    a[key]=value
    ```

    Note

    In the free-threaded build, only *a* is locked.
    The iteration over *seq2* is not synchronized; *seq2* may be concurrently
    modified by another thread.

intPyDict\_AddWatcher(PyDict\_WatchCallbackcallback)
:   *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Register *callback* as a dictionary watcher. Return a non-negative integer
    id which must be passed to future calls to `PyDict_Watch()`. In case
    of error (e.g. no more watcher IDs available), return `-1` and set an
    exception.

    Note

    This function is not internally synchronized. In the
    free-threaded build, callers should ensure no
    concurrent calls to `PyDict_AddWatcher()` or
    `PyDict_ClearWatcher()` are in progress.

    Added in version 3.12.

intPyDict\_ClearWatcher(intwatcher\_id)
:   *Thread safety: Safe to call from multiple threads with external synchronization only.*

    Clear watcher identified by *watcher\_id* previously returned from
    `PyDict_AddWatcher()`. Return `0` on success, `-1` on error (e.g.
    if the given *watcher\_id* was never registered.)

    Note

    This function is not internally synchronized. In the
    free-threaded build, callers should ensure no
    concurrent calls to `PyDict_AddWatcher()` or
    `PyDict_ClearWatcher()` are in progress.

    Added in version 3.12.

intPyDict\_Watch(intwatcher\_id, PyObject\*dict)
:   *Thread safety: Safe to call without external synchronization on distinct objects.*

    Mark dictionary *dict* as watched. The callback granted *watcher\_id* by
    `PyDict_AddWatcher()` will be called when *dict* is modified or
    deallocated. Return `0` on success or `-1` on error.

    Added in version 3.12.

intPyDict\_Unwatch(intwatcher\_id, PyObject\*dict)
:   *Thread safety: Safe to call without external synchronization on distinct objects.*

    Mark dictionary *dict* as no longer watched. The callback granted
    *watcher\_id* by `PyDict_AddWatcher()` will no longer be called when
    *dict* is modified or deallocated. The dict must previously have been
    watched by this watcher. Return `0` on success or `-1` on error.

    Added in version 3.12.

typePyDict\_WatchEvent
:   Enumeration of possible dictionary watcher events: `PyDict_EVENT_ADDED`,
    `PyDict_EVENT_MODIFIED`, `PyDict_EVENT_DELETED`, `PyDict_EVENT_CLONED`,
    `PyDict_EVENT_CLEARED`, or `PyDict_EVENT_DEALLOCATED`.

    Added in version 3.12.

typedefint(\*PyDict\_WatchCallback)(PyDict\_WatchEventevent,PyObject\*dict,PyObject\*key,PyObject\*new\_value)
:   Type of a dict watcher callback function.

    If *event* is `PyDict_EVENT_CLEARED` or `PyDict_EVENT_DEALLOCATED`, both
    *key* and *new\_value* will be `NULL`. If *event* is `PyDict_EVENT_ADDED`
    or `PyDict_EVENT_MODIFIED`, *new\_value* will be the new value for *key*.
    If *event* is `PyDict_EVENT_DELETED`, *key* is being deleted from the
    dictionary and *new\_value* will be `NULL`.

    `PyDict_EVENT_CLONED` occurs when *dict* was previously empty and another
    dict is merged into it. To maintain efficiency of this operation, per-key
    `PyDict_EVENT_ADDED` events are not issued in this case; instead a
    single `PyDict_EVENT_CLONED` is issued, and *key* will be the source
    dictionary.

    The callback may inspect but must not modify *dict*; doing so could have
    unpredictable effects, including infinite recursion. Do not trigger Python
    code execution in the callback, as it could modify the dict as a side effect.

    If *event* is `PyDict_EVENT_DEALLOCATED`, taking a new reference in the
    callback to the about-to-be-destroyed dictionary will resurrect it and
    prevent it from being freed at this time. When the resurrected object is
    destroyed later, any watcher callbacks active at that time will be called
    again.

    Callbacks occur before the notified modification to *dict* takes place, so
    the prior state of *dict* can be inspected.

    If the callback sets an exception, it must return `-1`; this exception will
    be printed as an unraisable exception using `PyErr_WriteUnraisable()`.
    Otherwise it should return `0`.

    There may already be a pending exception set on entry to the callback. In
    this case, the callback should return `0` with the same exception still
    set. This means the callback may not call any other API that can set an
    exception unless it saves and clears the exception state first, and restores
    it before returning.

    Added in version 3.12.

## Dictionary View Objects

intPyDictViewSet\_Check(PyObject\*op)
:   Return true if *op* is a view of a set inside a dictionary. This is currently
    equivalent to PyDictKeys\_Check(op)||PyDictItems\_Check(op). This
    function always succeeds.

PyTypeObjectPyDictKeys\_Type
:   *Part of the Stable ABI.*

    Type object for a view of dictionary keys. In Python, this is the type of
    the object returned by `dict.keys()`.

intPyDictKeys\_Check(PyObject\*op)
:   Return true if *op* is an instance of a dictionary keys view. This function
    always succeeds.

PyTypeObjectPyDictValues\_Type
:   *Part of the Stable ABI.*

    Type object for a view of dictionary values. In Python, this is the type of
    the object returned by `dict.values()`.

intPyDictValues\_Check(PyObject\*op)
:   Return true if *op* is an instance of a dictionary values view. This function
    always succeeds.

PyTypeObjectPyDictItems\_Type
:   *Part of the Stable ABI.*

    Type object for a view of dictionary items. In Python, this is the type of
    the object returned by `dict.items()`.

intPyDictItems\_Check(PyObject\*op)
:   Return true if *op* is an instance of a dictionary items view. This function
    always succeeds.

## Ordered Dictionaries

Python’s C API provides interface for `collections.OrderedDict` from C.
Since Python 3.7, dictionaries are ordered by default, so there is usually
little need for these functions; prefer `PyDict*` where possible.

PyTypeObjectPyODict\_Type
:   Type object for ordered dictionaries. This is the same object as
    `collections.OrderedDict` in the Python layer.

intPyODict\_Check(PyObject\*od)
:   Return true if *od* is an ordered dictionary object or an instance of a
    subtype of the `OrderedDict` type. This function
    always succeeds.

intPyODict\_CheckExact(PyObject\*od)
:   Return true if *od* is an ordered dictionary object, but not an instance of
    a subtype of the `OrderedDict` type.
    This function always succeeds.

PyTypeObjectPyODictKeys\_Type
:   Analogous to `PyDictKeys_Type` for ordered dictionaries.

PyTypeObjectPyODictValues\_Type
:   Analogous to `PyDictValues_Type` for ordered dictionaries.

PyTypeObjectPyODictItems\_Type
:   Analogous to `PyDictItems_Type` for ordered dictionaries.

PyObject\*PyODict\_New(void)
:   Return a new empty ordered dictionary, or `NULL` on failure.

    This is analogous to `PyDict_New()`.

intPyODict\_SetItem(PyObject\*od, PyObject\*key, PyObject\*value)
:   Insert *value* into the ordered dictionary *od* with a key of *key*.
    Return `0` on success or `-1` with an exception set on failure.

    This is analogous to `PyDict_SetItem()`.

intPyODict\_DelItem(PyObject\*od, PyObject\*key)
:   Remove the entry in the ordered dictionary *od* with key *key*.
    Return `0` on success or `-1` with an exception set on failure.

    This is analogous to `PyDict_DelItem()`.

These are soft deprecated aliases to `PyDict` APIs:

| `PyODict` | `PyDict` |
| --- | --- |
| PyODict\_GetItem(od, key) | `PyDict_GetItem()` |
| PyODict\_GetItemWithError(od, key) | `PyDict_GetItemWithError()` |
| PyODict\_GetItemString(od, key) | `PyDict_GetItemString()` |
| PyODict\_Contains(od, key) | `PyDict_Contains()` |
| PyODict\_Size(od) | `PyDict_Size()` |
| PyODict\_SIZE(od) | `PyDict_GET_SIZE()` |