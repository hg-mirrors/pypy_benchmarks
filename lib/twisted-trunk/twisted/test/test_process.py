
@var CONCURRENT_PROCESS_TEST_COUNT: The number of concurrent processes to use
    to stress-test the spawnProcess API.  This value is tuned to a number of
    processes which has been determined to stay below various
    experimentally-determined limitations of our supported platforms.
    Particularly, Windows XP seems to have some undocumented limitations which
    cause spurious failures if this value is pushed too high.  U{Please see
    this ticket for a discussion of how we arrived at its current value.
    <http://twistedmatrix.com/trac/ticket/3404>}

@var properEnv: A copy of L{os.environ} which has L{bytes} keys/values on POSIX
    platforms and native L{str} keys/values on Windows.
from __future__ import division, absolute_import, print_function



from io import BytesIO

from twisted.python import runtime, procutils
from twisted.python.compat import _PY3, networkString, range, bytesEnviron
from twisted.python.filepath import FilePath


# Get the current Python executable as a bytestring.
pyExe = FilePath(sys.executable)._asBytesPath()
CONCURRENT_PROCESS_TEST_COUNT = 25
if not runtime.platform.isWindows():
    properEnv = bytesEnviron()
    properEnv[b"PYTHONPATH"] = os.pathsep.join(sys.path).encode(
        sys.getfilesystemencoding())
else:
    properEnv = dict(os.environ)
    properEnv["PYTHONPATH"] = os.pathsep.join(sys.path)




        bytesToSend = b"bytes"
        p.childDataReceived(1, bytesToSend)
        self.assertEqual(received, [bytesToSend])
        bytesToSend = b"bytes"
        p.childDataReceived(2, bytesToSend)
        self.assertEqual(received, [bytesToSend])




        self.data = b''
        self.err = b''
        self.transport.write(b"abcd")

            if self.data != b"abcd":
                raise RuntimeError(
                    "Data was %r instead of 'abcd'" % (self.data,))
            self.transport.write(b"1234")
            if self.err != b"1234":
                raise RuntimeError(
                    "Err was %r instead of '1234'" % (self.err,))
            self.transport.write(b"abcd")


    s = b"1234567" * 1001


        if self.buffer[self.count:self.count+len(data)] != data:

        Callback C{self.deferred} with L{None} if C{reason} is a
        L{error.ProcessTerminated} failure with C{exitCode} set to L{None},

    @ivar programName: The name of the program to run.
    programName = None
    @classmethod
            self, pyExe, [pyExe, b"-u", b"-m", self.programName] + argv,
            env=env)
    programName = b"twisted.test.process_getargv"
        return b''.join(chunks).split(b'\0')
    programName = b"twisted.test.process_getenv"
        environString = b''.join(chunks)
        environ = iter(environString.split(b'\0'))
                k = next(environ)
                v = next(environ)
class ProcessTests(unittest.TestCase):
    """
    Test running a process.
    """
    def test_stdio(self):
        """
        L{twisted.internet.stdio} test.
        """
        scriptPath = b"twisted.test.process_twisted"
        reactor.spawnProcess(p, pyExe, [pyExe, b'-u', b"-m", scriptPath],
                             env=properEnv,
        p.transport.write(b"hello, world")
        p.transport.write(b"abc")
        p.transport.write(b"123")
            self.assertEqual(p.outF.getvalue(), b"hello, worldabc123",
        scriptPath = b"twisted.test.process_echoer"
        procTrans = reactor.spawnProcess(p, pyExe,
                                         [pyExe, b'-u', b"-m", scriptPath],
                                         env=properEnv)
        self.assertTrue(procTrans.pid)
            self.assertIsNone(procTrans.pid)
        scriptPath = b"twisted.test.process_tester"
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", b"-m", scriptPath],
                             env=properEnv)
            # self.assertIsNone(f.value.signal)

    def test_manyProcesses(self):
                self.assertEqual(p.stages, [1, 2, 3, 4, 5],
                                 "[%d] stages = %s" % (id(p.transport),
                                                       str(p.stages)))
        scriptPath = b"twisted.test.process_tester"
        args = [pyExe, b'-u', b"-m", scriptPath]
        for i in range(CONCURRENT_PROCESS_TEST_COUNT):
            reactor.spawnProcess(p, pyExe, args, env=properEnv)
        L{IReactorProcess.spawnProcess} will result in that echoed output being
        scriptPath = b"twisted.test.process_echoer"
        reactor.spawnProcess(p, pyExe, [pyExe, b'-u', b"-m", scriptPath],
                             env=properEnv)
            self.assertFalse(p.failure, p.failure)
            self.assertTrue(hasattr(p, 'buffer'))
            self.assertEqual(len(p.buffer), len(p.s * p.n))
    def test_commandLine(self):
        args = [br'a\"b ', br'a\b ', br' a\\"b', br' a\\b', br'"foo bar" "',
                b'\tab', b'"\\', b'a"b', b"a'b"]
        scriptPath = b"twisted.test.process_cmdline"
        reactor.spawnProcess(p, pyExe,
                             [pyExe, b"-u", b"-m", scriptPath] + args,
                             env=properEnv, path=None)
            self.assertEqual(p.errF.getvalue(), b"")
            {b"foo": 2},
            {b"foo": b"egg\0a"},
            {3: b"bar"},
            {b"bar\0foo": b"bar"}]
            [pyExe, 2],
            b"spam",
            [pyExe, b"foo\0bar"]]
            badUnicode.encode(sys.getfilesystemencoding())
            badArgs.append([pyExe, badUnicode])
                reactor.spawnProcess, p, pyExe, [pyExe, b"-c", b""], env=env)
                reactor.spawnProcess, p, pyExe, args, env=None)







        scriptPath = b"twisted.test.process_reader"
            p = reactor.spawnProcess(self.pp[num], pyExe,
                                     [pyExe, b"-u", b"-m", scriptPath],
                                     env=properEnv, usePTY=usePTY)

        if self.verbose: print("closing stdin [%d]" % num)
        self.assertFalse(pp.finished, "Process finished too early")
        if self.verbose: print(self.pp[0].finished, self.pp[1].finished)


    def test_close(self):
        if self.verbose: print("starting processes")


class TwoProcessesNonPosixTests(TestTwoProcessesBase, unittest.TestCase):


class TwoProcessesPosixTests(TestTwoProcessesBase, unittest.TestCase):

        if self.verbose: print("kill [%d] with SIGTERM" % num)
        self.assertFalse(pp.finished, "Process finished too early")
        if self.verbose: print(self.pp[0].finished, self.pp[1].finished)

    def test_kill(self):
        if self.verbose: print("starting processes")

    def test_closePty(self):
        if self.verbose: print("starting processes")

    def test_killPty(self):
        if self.verbose: print("starting processes")


    data = b""


        self.transport.writeToChild(0, b"abcd")

                if self.data != b"righto":
                self.data = b""
                self.transport.writeToChild(3, b"efgh")
                if self.data != b"closed":


class FDTests(unittest.TestCase):

    def test_FD(self):
        scriptPath = b"twisted.test.process_fds"
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", b"-m", scriptPath],
                             env=properEnv,
        d.addCallback(lambda x : self.assertFalse(p.failed, p.failed))

    def test_linger(self):
        scriptPath = b"twisted.test.process_linger"
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", b"-m", scriptPath],
                             env=properEnv,
                             b"here is some text\ngoodbye\n")
        self.outF = BytesIO()
        self.errF = BytesIO()






class PosixProcessBase(object):
        binLoc = FilePath('/bin').child(commandName)
        usrbinLoc = FilePath('/usr/bin').child(commandName)

        if binLoc.exists():
            return binLoc._asBytesPath()
        elif usrbinLoc.exists():
            return usrbinLoc._asBytesPath()

    def test_normalTermination(self):
        reactor.spawnProcess(p, cmd, [b'true'], env=None,
            self.assertIsNone(p.reason.value.signal)
        reactor.spawnProcess(p, pyExe,
                             [pyExe, b'-c', b'import sys; sys.exit(1)'],
            self.assertIsNone(p.reason.value.signal)
        scriptPath = b"twisted.test.process_signal"
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", "-m", scriptPath],
                             env=properEnv, usePTY=self.usePTY)
        with the C{exitCode} set to L{None} and the C{signal} attribute set to
        with the C{exitCode} set to L{None} and the C{signal} attribute set to
        with the C{exitCode} set to L{None} and the C{signal} attribute set to
        with the C{exitCode} set to L{None} and the C{signal} attribute set to
            reactor.spawnProcess(p, cmd, [b'false'], env=None,
                errData = b"".join(p.errData + p.outData)
                self.assertIn(b"Upon execvpe", errData)
                self.assertIn(b"Ouch", errData)
    if runtime.platform.isMacOSX():
        test_executionError.skip = (
            "Test is flaky from a Darwin bug. See #8840.")

        scriptPath = b"twisted.test.process_echoer"

            ErrorInProcessEnded(), pyExe,
            [pyExe, b"-u", b"-m", scriptPath],
            env=properEnv, path=None)


    @ivar raiseFork: if not L{None}, subsequent calls to fork will raise this
    @type raiseFork: L{None} or C{Exception}
    @type fdio: C{BytesIO} or C{BytesIO}
    @type closed: C{list} of C{int}
    @ivar raiseWaitPid: if set, subsequent calls to waitpid will raise
    @type raiseWaitPid: L{None} or a class
    @type waitChild: L{None} or a tuple

    @ivar raiseKill: if set, subsequent call to kill will raise the error
        specified.
    @type raiseKill: L{None} or an exception instance.

    @ivar readData: data returned by C{os.read}.
    @type readData: C{str}
    raiseKill = None
    readData = b""
        Fake C{os.fdopen}. Return a file-like object whose content can
        be tested later via C{self.fdio}.
        if flag == "wb":
            self.fdio = BytesIO()
        else:
            assert False
        Fake C{os.setsid}. Save action.
        self.actions.append('setsid')
        Fake C{os.write}. Save action.
        self.actions.append(("write", fd, data))


    def read(self, fd, size):
        """
        Fake C{os.read}: save action, and return C{readData} content.

        @param fd: The file descriptor to read.

        @param size: The maximum number of bytes to read.

        @return: A fixed C{bytes} buffer.
        """
        self.actions.append(('read', fd, size))
        return self.readData
        self.actions.append(('exit', code))
        Override L{util.switchUID}. Save the action.
    def chdir(self, path):
        """
        Override C{os.chdir}. Save the action.

        @param path: The path to change the current directory to.
        """
        self.actions.append(('chdir', path))



    def kill(self, pid, signalID):
        """
        Override C{os.kill}: save the action and raise C{self.raiseKill} if
        specified.
        """
        self.actions.append(('kill', pid, signalID))
        if self.raiseKill is not None:
            raise self.raiseKill


    def unlink(self, filename):
        """
        Override C{os.unlink}. Save the action.

        @param filename: The file name to remove.
        """
        self.actions.append(('unlink', filename))


    def umask(self, mask):
        """
        Override C{os.umask}. Save the action.

        @param mask: The new file mode creation mask.
        """
        self.actions.append(('umask', mask))


    def getpid(self):
        """
        Return a fixed PID value.

        @return: A fixed value.
        """
        return 6789


    def getfilesystemencoding(self):
        """
        Return a fixed filesystem encoding.

        @return: A fixed value of "utf8".
        """
        return "utf8"

class MockProcessTests(unittest.TestCase):

        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
            self.assertTrue(self.mockos.exited)
                self.mockos.actions, [("fork", False), "exec", ("exit", 1)])
        cmd = b'/mock/ouch'
        reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        self.assertRaises(SystemError, reactor.spawnProcess, p, cmd, [b'ouch'],
                          env=None, usePTY=True)
        self.assertTrue(self.mockos.exited)
        self.assertEqual(
            self.mockos.actions,
            [("fork", False), "setsid", "exec", ("exit", 1)])
        self.assertEqual(set(self.mockos.closed),
                         set([-1, -4, -6, -2, -3, -5]))
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
            self.assertTrue(self.mockos.exited)
                self.mockos.actions, [("fork", False), "exec", ("exit", 1)])
            self.assertIn(b"RuntimeError: Bar", self.mockos.fdio.getvalue())
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
            self.assertTrue(self.mockos.exited)
            self.assertEqual(
                self.mockos.actions,
                [('fork', False), ('setuid', 0), ('setgid', 0),
                 ('switchuid', 8080, 1234), 'exec', ('exit', 1)])
        When spawning a child process with a UID different from the UID of the
        current process, the current process does not have its UID changed.
        cmd = b'/mock/ouch'
        reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        self.assertEqual(self.mockos.actions, [('fork', False), 'waitpid'])
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
            self.assertTrue(self.mockos.exited)
            self.assertEqual(
                self.mockos.actions,
                [('fork', False), 'setsid', ('setuid', 0), ('setgid', 0),
                 ('switchuid', 8081, 1234), 'exec', ('exit', 1)])
        When spawning a child process with PTY and a UID different from the UID
        of the current process, the current process does not have its UID
        changed.
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        self.assertEqual(self.mockos.actions, [('fork', False), 'waitpid'])
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
    def test_kill(self):
        L{process.Process.signalProcess} calls C{os.kill} translating the given
        signal string to the PID.
        self.mockos.child = False
        self.mockos.waitChild = (0, 0)
        cmd = b'/mock/ouch'
        p = TrivialProcessProtocol(None)
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        proc.signalProcess("KILL")
            [('fork', False), 'waitpid', ('kill', 21, signal.SIGKILL)])
    def test_killExited(self):
        """
        L{process.Process.signalProcess} raises L{error.ProcessExitedAlready}
        if the process has exited.
        """
        self.mockos.child = False
        cmd = b'/mock/ouch'
        p = TrivialProcessProtocol(None)
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        # We didn't specify a waitpid value, so the waitpid call in
        # registerReapProcessHandler has already reaped the process
        self.assertRaises(error.ProcessExitedAlready,
                          proc.signalProcess, "KILL")

    def test_killExitedButNotDetected(self):
        """
        L{process.Process.signalProcess} raises L{error.ProcessExitedAlready}
        if the process has exited but that twisted hasn't seen it (for example,
        if the process has been waited outside of twisted): C{os.kill} then
        raise C{OSError} with C{errno.ESRCH} as errno.
        """
        self.mockos.child = False
        self.mockos.waitChild = (0, 0)
        cmd = b'/mock/ouch'
        p = TrivialProcessProtocol(None)
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        self.mockos.raiseKill = OSError(errno.ESRCH, "Not found")
        self.assertRaises(error.ProcessExitedAlready,
                          proc.signalProcess, "KILL")


    def test_killErrorInKill(self):
        """
        L{process.Process.signalProcess} doesn't mask C{OSError} exceptions if
        the errno is different from C{errno.ESRCH}.
        """
        self.mockos.child = False
        self.mockos.waitChild = (0, 0)
        cmd = b'/mock/ouch'
        p = TrivialProcessProtocol(None)
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        self.mockos.raiseKill = OSError(errno.EINVAL, "Invalid signal")
        err = self.assertRaises(OSError,
                                proc.signalProcess, "KILL")
        self.assertEqual(err.errno, errno.EINVAL)



class PosixProcessTests(unittest.TestCase, PosixProcessBase):
        reactor.spawnProcess(p, pyExe,
                             [pyExe, b"-c",
                              networkString("import sys; sys.stderr.write"
                                            "('{0}')".format(value))],
            self.assertEqual(b"42", p.errF.getvalue())
    def test_process(self):
        s = b"there's no place like home!\n" * 3
        reactor.spawnProcess(p, cmd, [cmd, b"-c"], env=None, path="/tmp",
            with gzip.GzipFile(fileobj=f) as gf:
                self.assertEqual(gf.read(), s)
class PosixProcessPTYTests(unittest.TestCase, PosixProcessBase):
    Just like PosixProcessTests, but use ptys instead of pipes.
    def test_openingTTY(self):
        scriptPath = b"twisted.test.process_tty"
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", b"-m", scriptPath],
                             env=properEnv, usePTY=self.usePTY)
        p.transport.write(b"hello world!\n")
                b"hello world!\r\nhello world!\r\n",
                ("Error message from process_tty "
                 "follows:\n\n%s\n\n" % (p.outF.getvalue(),)))
    def test_badArgs(self):
        pyArgs = [pyExe, b"-u", b"-c", b"print('hello')"]
            usePTY=1, childFDs={1:b'r'})
        Callback C{self.deferred} with L{None} if C{reason} is a
                ValueError("Wrong exit code: %s" % (v.exitCode,)))
class Win32ProcessTests(unittest.TestCase):
    def _test_stdinReader(self, pyExe, args, env, path):
        """
        Spawn a process, write to stdin, and check the output.
        """
        reactor.spawnProcess(p, pyExe, args, env, path)
        p.transport.write(b"hello, world")
            self.assertEqual(p.errF.getvalue(), b"err\nerr\n")
            self.assertEqual(p.outF.getvalue(), b"out\nhello, world\nout\n")
    def test_stdinReader_bytesArgs(self):
        """
        Pass L{bytes} args to L{_test_stdinReader}.
        """
        import win32api

        pyExe = FilePath(sys.executable)._asBytesPath()
        args = [pyExe, b"-u", b"-m", b"twisted.test.process_stdinreader"]
        env = bytesEnviron()
        env[b"PYTHONPATH"] = os.pathsep.join(sys.path).encode(
                                             sys.getfilesystemencoding())
        path = win32api.GetTempPath()
        path = path.encode(sys.getfilesystemencoding())
        d = self._test_stdinReader(pyExe, args, env, path)
        return d


    def test_stdinReader_unicodeArgs(self):
        """
        Pass L{unicode} args to L{_test_stdinReader}.
        """
        import win32api

        pyExe = FilePath(sys.executable)._asTextPath()
        args = [pyExe, u"-u", u"-m", u"twisted.test.process_stdinreader"]
        env = properEnv
        pythonPath = os.pathsep.join(sys.path)
        if isinstance(pythonPath, bytes):
            pythonPath = pythonPath.decode(sys.getfilesystemencoding())
        env[u"PYTHONPATH"] = pythonPath
        path = win32api.GetTempPath()
        if isinstance(path, bytes):
            path = path.decode(sys.getfilesystemencoding())
        d = self._test_stdinReader(pyExe, args, env, path)
        return d


    def test_badArgs(self):
        pyArgs = [pyExe, b"-u", b"-c", b"print('hello')"]
                          reactor.spawnProcess, p, pyExe, pyArgs, uid=1)
                          reactor.spawnProcess, p, pyExe, pyArgs, gid=1)
                          reactor.spawnProcess, p, pyExe, pyArgs, usePTY=1)
                          reactor.spawnProcess, p, pyExe, pyArgs, childFDs={1:'r'})
        scriptPath = b"twisted.test.process_signal"
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", b"-m", scriptPath],
                             env=properEnv)
        pyArgs = [pyExe, b"-u", b"-c", b"print('hello')"]
            self.assertIs(transport, proc)
            self.assertIsNone(proc.pid)
            self.assertIsNone(proc.hProcess)
            self.assertIsNone(proc.hThread)
class Win32UnicodeEnvironmentTests(unittest.TestCase):
        supported on Python 2).
        p = GetEnvironmentDictionary.run(reactor, [], properEnv)
class DumbWin32ProcTests(unittest.TestCase):
    L{twisted.internet._dumbwin32proc} tests.
        Simple test for the pid attribute of Process on win32.
        scriptPath = FilePath(__file__).sibling(u"process_cmdline.py").path
        pyExe = FilePath(sys.executable).asTextMode().path
        comspec = u"cmd.exe"
        cmd = [comspec, u"/c", pyExe, scriptPath]

        p = _dumbwin32proc.Process(
            reactor, processProto, None, cmd, {}, None)
            self.assertIsNone(p.pid)
    def test_findShebang(self):
        """
        Look for the string after the shebang C{#!}
        in a file.
        """
        from twisted.internet._dumbwin32proc import _findShebang
        cgiScript = FilePath(b"example.cgi")
        cgiScript.setContent(b"#!/usr/bin/python")
        program = _findShebang(cgiScript.path)
        self.assertEqual(program, "/usr/bin/python")



class Win32CreateProcessFlagsTests(unittest.TestCase):
    """
    Check the flags passed to CreateProcess.
    """

    @defer.inlineCallbacks
    def test_flags(self):
        """
        Verify that the flags passed to win32process.CreateProcess() prevent a
        new console window from being created. Use the following script
        to test this interactively::

            # Add the following lines to a script named
            #   should_not_open_console.pyw
            from twisted.internet import reactor, utils

            def write_result(result):
            open("output.log", "w").write(repr(result))
            reactor.stop()

            PING_EXE = r"c:\windows\system32\ping.exe"
            d = utils.getProcessOutput(PING_EXE, ["slashdot.org"])
            d.addCallbacks(write_result)
            reactor.run()

        To test this, run::

            pythonw.exe should_not_open_console.pyw
        """
        from twisted.internet import _dumbwin32proc
        flags = []
        realCreateProcess = _dumbwin32proc.win32process.CreateProcess

        def fakeCreateprocess(appName, commandLine, processAttributes,
                              threadAttributes, bInheritHandles, creationFlags,
                              newEnvironment, currentDirectory, startupinfo):
            """
            See the Windows API documentation for I{CreateProcess} for further details.

            @param appName: The name of the module to be executed
            @param commandLine: The command line to be executed.
            @param processAttributes: Pointer to SECURITY_ATTRIBUTES structure or None.
            @param threadAttributes: Pointer to SECURITY_ATTRIBUTES structure or  None
            @param bInheritHandles: boolean to determine if inheritable handles from this
                                    process are inherited in the new process
            @param creationFlags: flags that control priority flags and creation of process.
            @param newEnvironment: pointer to new environment block for new process, or None.
            @param currentDirectory: full path to current directory of new process.
            @param startupinfo: Pointer to STARTUPINFO or STARTUPINFOEX structure
            @return: True on success, False on failure
            @rtype: L{bool}
            """
            flags.append(creationFlags)
            return realCreateProcess(appName, commandLine,
                            processAttributes, threadAttributes,
                            bInheritHandles, creationFlags, newEnvironment,
                            currentDirectory, startupinfo)

        self.patch(_dumbwin32proc.win32process, "CreateProcess",
                   fakeCreateprocess)
        exe = sys.executable
        scriptPath = FilePath(__file__).sibling("process_cmdline.py")

        d = defer.Deferred()
        processProto = TrivialProcessProtocol(d)
        comspec = str(os.environ["COMSPEC"])
        cmd = [comspec, "/c", exe, scriptPath.path]
        _dumbwin32proc.Process(reactor, processProto, None, cmd, {}, None)
        yield d
        self.assertEqual(flags,
                         [_dumbwin32proc.win32process.CREATE_NO_WINDOW])


class UtilTests(unittest.TestCase):
        for name, mode in [(j(self.foobaz, "executable"), 0o700),
                           (j(self.foo, "executable"), 0o700),
                           (j(self.bazfoo, "executable"), 0o700),
                           (j(self.bazfoo, "executable.bin"), 0o700),
            open(name, "wb").close()
    def test_which(self):
    def test_whichPathExt(self):
    output = b''
    errput = b''



class ClosingPipesTests(unittest.TestCase):
            p, pyExe, [
                pyExe, b'-u', b'-c',
                networkString('try: input = raw_input\n'
                'except NameError: pass\n'
                'input()\n'
                # instead of relying on an os.write to fail with SIGPIPE.
                # However, that wouldn't work on macOS (or Windows?).
                '    os.write(%d, b"foo\\n")\n'
                'sys.exit(42)\n' % (fd,))
        p.transport.write(b'go\n')
        self.assertNotEqual(
        self.assertEqual(p.output, b'')
            if _PY3:
                if runtime.platform.isWindows():
                    self.assertIn(b"OSError", errput)
                    self.assertIn(b"22", errput)
                else:
                    self.assertIn(b'BrokenPipeError', errput)
            else:
                self.assertIn(b'OSError', errput)
                self.assertIn(b'Broken pipe', errput)
            self.assertEqual(errput, b'')
    PosixProcessTests.skip = skipMessage
    PosixProcessPTYTests.skip = skipMessage
    TwoProcessesPosixTests.skip = skipMessage
    FDTests.skip = skipMessage
    Win32ProcessTests.skip = skipMessage
    TwoProcessesNonPosixTests.skip = skipMessage
    DumbWin32ProcTests.skip = skipMessage
    Win32CreateProcessFlagsTests.skip = skipMessage
    Win32UnicodeEnvironmentTests.skip = skipMessage
    ProcessTests.skip = skipMessage
    ClosingPipesTests.skip = skipMessage