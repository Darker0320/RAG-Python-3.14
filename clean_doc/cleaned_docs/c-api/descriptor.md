# Descriptor Objects

“Descriptors” are objects that describe some attribute of an object. They are
found in the dictionary of type objects.

PyTypeObjectPyProperty\_Type
*Part of the Stable ABI.*

    The type object for the built-in descriptor types.

PyObject\*PyDescr\_NewGetSet(PyTypeObject\*type, structPyGetSetDef\*getset)
*Return value: New reference.* *Part of the Stable ABI.*

PyObject\*PyDescr\_NewMember(PyTypeObject\*type, structPyMemberDef\*meth)
*Return value: New reference.* *Part of the Stable ABI.*

PyTypeObjectPyMemberDescr\_Type
*Part of the Stable ABI.*

    The type object for member descriptor objects created from
    `PyMemberDef` structures. These descriptors expose fields of a
    C struct as attributes on a type, and correspond
    to `types.MemberDescriptorType` objects in Python.

PyTypeObjectPyGetSetDescr\_Type
*Part of the Stable ABI.*

    The type object for get/set descriptor objects created from
    `PyGetSetDef` structures. These descriptors implement attributes
    whose value is computed by C getter and setter functions, and are used
    for many built-in type attributes.

PyObject\*PyDescr\_NewMethod(PyTypeObject\*type, structPyMethodDef\*meth)
*Return value: New reference.* *Part of the Stable ABI.*

PyTypeObjectPyMethodDescr\_Type
*Part of the Stable ABI.*

    The type object for method descriptor objects created from
    `PyMethodDef` structures. These descriptors expose C functions as
    methods on a type, and correspond to `types.MemberDescriptorType`
    objects in Python.

PyObject\*PyDescr\_NewWrapper(PyTypeObject\*type, structwrapperbase\*wrapper, void\*wrapped)
*Return value: New reference.*

PyTypeObjectPyWrapperDescr\_Type
*Part of the Stable ABI.*

    The type object for wrapper descriptor objects created by
    `PyDescr_NewWrapper()` and `PyWrapper_New()`. Wrapper
    descriptors are used internally to expose special methods implemented
    via wrapper structures, and appear in Python as
    `types.WrapperDescriptorType` objects.

PyObject\*PyDescr\_NewClassMethod(PyTypeObject\*type, PyMethodDef\*method)
*Return value: New reference.* *Part of the Stable ABI.*

intPyDescr\_IsData(PyObject\*descr)
Return non-zero if the descriptor object *descr* describes a data attribute, or
    `0` if it describes a method. *descr* must be a descriptor object; there is
    no error checking.

PyObject\*PyWrapper\_New(PyObject\*, PyObject\*)
*Return value: New reference.* *Part of the Stable ABI.*

## Built-in descriptors

PyTypeObjectPySuper\_Type
*Part of the Stable ABI.*

    The type object for super objects. This is the same object as
    `super` in the Python layer.

PyTypeObjectPyClassMethod\_Type
The type of class method objects. This is the same object as
    `classmethod` in the Python layer.

PyTypeObjectPyClassMethodDescr\_Type
*Part of the Stable ABI.*

    The type object for C-level class method descriptor objects.
    This is the type of the descriptors created for `classmethod()` defined in
    C extension types, and is the same object as `classmethod`
    in Python.

PyObject\*PyClassMethod\_New(PyObject\*callable)
Create a new `classmethod` object wrapping *callable*.
    *callable* must be a callable object and must not be `NULL`.

    On success, this function returns a strong reference to a new class
    method descriptor. On failure, this function returns `NULL` with an
    exception set.

PyTypeObjectPyStaticMethod\_Type
The type of static method objects. This is the same object as
    `staticmethod` in the Python layer.

PyObject\*PyStaticMethod\_New(PyObject\*callable)
Create a new `staticmethod` object wrapping *callable*.
    *callable* must be a callable object and must not be `NULL`.

    On success, this function returns a strong reference to a new static
    method descriptor. On failure, this function returns `NULL` with an
    exception set.
