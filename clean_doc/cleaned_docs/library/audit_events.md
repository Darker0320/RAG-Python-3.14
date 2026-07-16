# Audit events table

This table contains all events raised by `sys.audit()` or
`PySys_Audit()` calls throughout the CPython runtime and the
standard library. These calls were added in 3.8 or later (see **PEP 578**).

See `sys.addaudithook()` and `PySys_AddAuditHook()` for
information on handling these events.

**CPython implementation detail:** This table is generated from the CPython documentation, and may not
represent events raised by other implementations. See your runtime
specific documentation for actual events raised.

| Audit event | Arguments | References |
| --- | --- | --- |
| \_thread.start\_new\_thread | `function`, `args`, `kwargs` | [1] |
| array.\_\_new\_\_ | `typecode`, `initializer` | [1] |
| builtins.breakpoint | `breakpointhook` | [1] |
| builtins.id | `id` | [1] |
| builtins.input | `prompt` | [1] |
| builtins.input/result | `result` | [1] |
| code.\_\_new\_\_ | `code`, `filename`, `name`, `argcount`, `posonlyargcount`, `kwonlyargcount`, `nlocals`, `stacksize`, `flags` | [1] |
| compile | `source`, `filename` | [1] |
| cpython.PyConfig\_Set | `name`, `value` | [1] |
| cpython.PyInterpreterState\_Clear | [1] |
| cpython.PyInterpreterState\_New | [1] |
| cpython.\_PySys\_ClearAuditHooks | [1] |
| cpython.remote\_debugger\_script | `script_path` | [1] |
| cpython.run\_command | `command` | [1] |
| cpython.run\_file | `filename` | [1] |
| cpython.run\_interactivehook | `hook` | [1] |
| cpython.run\_module | `module-name` | [1] |
| cpython.run\_startup | `filename` | [1] |
| cpython.run\_stdin | [1][2][3] |
| ctypes.addressof | `obj` | [1] |
| ctypes.call\_function | `func_pointer`, `arguments` | [1] |
| ctypes.cdata | `address` | [1] |
| ctypes.cdata/buffer | `pointer`, `size`, `offset` | [1][2] |
| ctypes.create\_string\_buffer | `init`, `size` | [1] |
| ctypes.create\_unicode\_buffer | `init`, `size` | [1] |
| ctypes.dlopen | `name` | [1] |
| ctypes.dlsym | `library`, `name` | [1] |
| ctypes.dlsym/handle | `handle`, `name` | [1] |
| ctypes.get\_errno | [1] |
| ctypes.get\_last\_error | [1] |
| ctypes.memoryview\_at | `address`, `size`, `readonly` | [1] |
| ctypes.set\_errno | `errno` | [1] |
| ctypes.set\_exception | `code` | [1] |
| ctypes.set\_last\_error | `error` | [1] |
| ctypes.string\_at | `ptr`, `size` | [1] |
| ctypes.wstring\_at | `ptr`, `size` | [1] |
| ensurepip.bootstrap | `root` | [1] |
| exec | `code_object` | [1][2] |
| fcntl.fcntl | `fd`, `cmd`, `arg` | [1] |
| fcntl.flock | `fd`, `operation` | [1] |
| fcntl.ioctl | `fd`, `request`, `arg` | [1] |
| fcntl.lockf | `fd`, `cmd`, `len`, `start`, `whence` | [1] |
| ftplib.connect | `self`, `host`, `port` | [1] |
| ftplib.sendcmd | `self`, `cmd` | [1][2] |
| function.\_\_new\_\_ | `code` | [1] |
| gc.get\_objects | `generation` | [1] |
| gc.get\_referents | `objs` | [1] |
| gc.get\_referrers | `objs` | [1] |
| glob.glob | `pathname`, `recursive` | [1][2] |
| glob.glob/2 | `pathname`, `recursive`, `root_dir`, `dir_fd` | [1][2] |
| http.client.connect | `self`, `host`, `port` | [1] |
| http.client.send | `self`, `data` | [1] |
| imaplib.open | `self`, `host`, `port` | [1] |
| imaplib.send | `self`, `data` | [1] |
| import | `module`, `filename`, `sys.path`, `sys.meta_path`, `sys.path_hooks` | [1] |
| marshal.dumps | `value`, `version` | [1] |
| marshal.load | [1] |
| marshal.loads | `bytes` | [1] |
| mmap.\_\_new\_\_ | `fileno`, `length`, `access`, `offset` | [1] |
| msvcrt.get\_osfhandle | `fd` | [1] |
| msvcrt.locking | `fd`, `mode`, `nbytes` | [1] |
| msvcrt.open\_osfhandle | `handle`, `flags` | [1] |
| object.\_\_delattr\_\_ | `obj`, `name` | [1] |
| object.\_\_getattr\_\_ | `obj`, `name` | [1] |
| object.\_\_setattr\_\_ | `obj`, `name`, `value` | [1] |
| open | `path`, `mode`, `flags` | [1][2][3] |
| os.add\_dll\_directory | `path` | [1] |
| os.chdir | `path` | [1][2] |
| os.chflags | `path`, `flags` | [1][2] |
| os.chmod | `path`, `mode`, `dir_fd` | [1][2][3] |
| os.chown | `path`, `uid`, `gid`, `dir_fd` | [1][2][3] |
| os.exec | `path`, `args`, `env` | [1] |
| os.fork | [1] |
| os.forkpty | [1] |
| os.fwalk | `top`, `topdown`, `onerror`, `follow_symlinks`, `dir_fd` | [1] |
| os.getxattr | `path`, `attribute` | [1] |
| os.kill | `pid`, `sig` | [1] |
| os.killpg | `pgid`, `sig` | [1] |
| os.link | `src`, `dst`, `src_dir_fd`, `dst_dir_fd` | [1] |
| os.listdir | `path` | [1] |
| os.listdrives | [1] |
| os.listmounts | `volume` | [1] |
| os.listvolumes | [1] |
| os.listxattr | `path` | [1] |
| os.lockf | `fd`, `cmd`, `len` | [1] |
| os.mkdir | `path`, `mode`, `dir_fd` | [1][2] |
| os.posix\_spawn | `path`, `argv`, `env` | [1][2] |
| os.putenv | `key`, `value` | [1] |
| os.remove | `path`, `dir_fd` | [1][2][3] |
| os.removexattr | `path`, `attribute` | [1] |
| os.rename | `src`, `dst`, `src_dir_fd`, `dst_dir_fd` | [1][2][3] |
| os.rmdir | `path`, `dir_fd` | [1] |
| os.scandir | `path` | [1] |
| os.setxattr | `path`, `attribute`, `value`, `flags` | [1] |
| os.spawn | `mode`, `path`, `args`, `env` | [1] |
| os.startfile | `path`, `operation` | [1] |
| os.startfile/2 | `path`, `operation`, `arguments`, `cwd`, `show_cmd` | [1] |
| os.symlink | `src`, `dst`, `dir_fd` | [1] |
| os.system | `command` | [1] |
| os.truncate | `fd`, `length` | [1][2] |
| os.unsetenv | `key` | [1] |
| os.utime | `path`, `times`, `ns`, `dir_fd` | [1] |
| os.walk | `top`, `topdown`, `onerror`, `followlinks` | [1] |
| pathlib.Path.glob | `self`, `pattern` | [1] |
| pathlib.Path.rglob | `self`, `pattern` | [1] |
| pdb.Pdb | [1] |
| pickle.find\_class | `module`, `name` | [1] |
| poplib.connect | `self`, `host`, `port` | [1][2] |
| poplib.putline | `self`, `line` | [1][2] |
| pty.spawn | `argv` | [1] |
| resource.prlimit | `pid`, `resource`, `limits` | [1] |
| resource.setrlimit | `resource`, `limits` | [1] |
| setopencodehook | [1] |
| shutil.chown | `path`, `user`, `group` | [1] |
| shutil.copyfile | `src`, `dst` | [1][2][3] |
| shutil.copymode | `src`, `dst` | [1][2] |
| shutil.copystat | `src`, `dst` | [1][2] |
| shutil.copytree | `src`, `dst` | [1] |
| shutil.make\_archive | `base_name`, `format`, `root_dir`, `base_dir` | [1] |
| shutil.move | `src`, `dst` | [1] |
| shutil.rmtree | `path`, `dir_fd` | [1] |
| shutil.unpack\_archive | `filename`, `extract_dir`, `format` | [1] |
| signal.pthread\_kill | `thread_id`, `signalnum` | [1] |
| smtplib.connect | `self`, `host`, `port` | [1] |
| smtplib.send | `self`, `data` | [1] |
| socket.\_\_new\_\_ | `self`, `family`, `type`, `protocol` | [1] |
| socket.bind | `self`, `address` | [1] |
| socket.connect | `self`, `address` | [1][2] |
| socket.getaddrinfo | `host`, `port`, `family`, `type`, `protocol` | [1] |
| socket.gethostbyaddr | `ip_address` | [1] |
| socket.gethostbyname | `hostname` | [1][2] |
| socket.gethostname | [1] |
| socket.getnameinfo | `sockaddr` | [1] |
| socket.getservbyname | `servicename`, `protocolname` | [1] |
| socket.getservbyport | `port`, `protocolname` | [1] |
| socket.sendmsg | `self`, `address` | [1] |
| socket.sendto | `self`, `address` | [1] |
| socket.sethostname | `name` | [1] |
| sqlite3.connect | `database` | [1] |
| sqlite3.connect/handle | `connection_handle` | [1] |
| sqlite3.enable\_load\_extension | `connection`, `enabled` | [1] |
| sqlite3.load\_extension | `connection`, `path` | [1] |
| subprocess.Popen | `executable`, `args`, `cwd`, `env` | [1] |
| sys.\_current\_exceptions | [1] |
| sys.\_current\_frames | [1] |
| sys.\_getframe | `frame` | [1] |
| sys.\_getframemodulename | `depth` | [1] |
| sys.addaudithook | [1][2] |
| sys.excepthook | `hook`, `type`, `value`, `traceback` | [1] |
| sys.monitoring.register\_callback | `func` | [1] |
| sys.remote\_exec | `pid` | [1] |
| sys.set\_asyncgen\_hooks\_finalizer | [1] |
| sys.set\_asyncgen\_hooks\_firstiter | [1] |
| sys.setprofile | [1] |
| sys.settrace | [1] |
| sys.unraisablehook | `hook`, `unraisable` | [1] |
| syslog.closelog | [1] |
| syslog.openlog | `ident`, `logoption`, `facility` | [1] |
| syslog.setlogmask | `maskpri` | [1] |
| syslog.syslog | `priority`, `message` | [1] |
| tempfile.mkdtemp | `fullpath` | [1][2] |
| tempfile.mkstemp | `fullpath` | [1][2][3] |
| time.sleep | `secs` | [1] |
| urllib.Request | `fullurl`, `data`, `headers`, `method` | [1] |
| webbrowser.open | `url` | [1] |
| winreg.ConnectRegistry | `computer_name`, `key` | [1] |
| winreg.CreateKey | `key`, `sub_key`, `access` | [1][2] |
| winreg.DeleteKey | `key`, `sub_key`, `access` | [1][2] |
| winreg.DeleteValue | `key`, `value` | [1] |
| winreg.DisableReflectionKey | `key` | [1] |
| winreg.EnableReflectionKey | `key` | [1] |
| winreg.EnumKey | `key`, `index` | [1] |
| winreg.EnumValue | `key`, `index` | [1] |
| winreg.ExpandEnvironmentStrings | `str` | [1] |
| winreg.LoadKey | `key`, `sub_key`, `file_name` | [1] |
| winreg.OpenKey | `key`, `sub_key`, `access` | [1] |
| winreg.OpenKey/result | `key` | [1][2][3] |
| winreg.PyHKEY.Detach | `key` | [1] |
| winreg.QueryInfoKey | `key` | [1] |
| winreg.QueryReflectionKey | `key` | [1] |
| winreg.QueryValue | `key`, `sub_key`, `value_name` | [1][2] |
| winreg.SaveKey | `key`, `file_name` | [1] |
| winreg.SetValue | `key`, `sub_key`, `type`, `value` | [1][2] |

The following events are raised internally and do not correspond to any
public API of CPython:

| Audit event | Arguments |
| --- | --- |
| \_winapi.CreateFile | `file_name`, `desired_access`, `share_mode`, `creation_disposition`, `flags_and_attributes` |
| \_winapi.CreateJunction | `src_path`, `dst_path` |
| \_winapi.CreateNamedPipe | `name`, `open_mode`, `pipe_mode` |
| \_winapi.CreatePipe |
| \_winapi.CreateProcess | `application_name`, `command_line`, `current_directory` |
| \_winapi.OpenProcess | `process_id`, `desired_access` |
| \_winapi.TerminateProcess | `handle`, `exit_code` |
| \_posixsubprocess.fork\_exec | `exec_list`, `args`, `env` |
| ctypes.PyObj\_FromPtr | `obj` |

Added in version 3.14: The `_posixsubprocess.fork_exec` internal audit event.
