import logging
import re
from rpg.command import Command
from rpg.utils import path_to_str
import subprocess
import tempfile
from pathlib import Path


class BuildException(Exception):
    """ This is thrown when mock build fails, contains information
        about error and return code """

    def __init__(self, errors, return_code):
        self.return_code = return_code
        self.errors = errors

    def __str__(self):
        return "\n".join(self.errors)


class PackageBuilder(object):
    """ Builder of RPM packages with use of Mock

:Example:

>>> from pathlib import Path
>>> from rpg.package_builder import PackageBuilder
>>> from rpg.spec import Spec
>>> pck_builder = PackageBuilder()
>>> spec_file = Spec()
>>> tarball = "archive.tar"
>>> output_dir = Path("/tmp/rpg-854ABCD50/")
>>> pck_builder.build_srpm(spec_file, tarball, output_dir)
>>> pck_builder.build_rpm(output_dir / "*.src.rpm", "fedora-22",
                          "x86-64", output_dir)
"""
    _regex = re.compile(r"[eE][rR][rR][oO][rR]|" +
                        r"[eE][xX][cC][eE][pP][tT][iI][oO][nN]|" +
                        r"[cC][oO][mM][mM][aA][nN][dD] [nN][oO][tT] " +
                        r"[fF][oO][uU][nN][dD]")

    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir())
        self.mock_logs = Path()

    @staticmethod
    def build_srpm(spec_file, tarball, output_dir):
        """ Builds source rpm from spec and tarball and moves it to the
            output directory """
        Command("rpmdev-setuptree").execute()
        Command("cp " + path_to_str(tarball) +
                ' $(rpm --eval "%{_topdir}")/SOURCES').execute()
        output = Command("rpmbuild -bs " + path_to_str(spec_file)).execute()
        Command("mv " + path_to_str(output.split()[-1]) +
                " " + path_to_str(output_dir)).execute()

    @staticmethod
    def _check_logs(path):
        with open(str(path / "build.log")) as build_log:
            for line in build_log.readlines():
                if PackageBuilder._regex.search(line):
                    yield line

    @staticmethod
    def _move_files(output, files):
        if not output.exists() and not output.is_dir():
            Command("mkdir " + path_to_str(output)).execute()
        for _out in files:
            try:
                Command("mv " + path_to_str(_out) +
                        " " + path_to_str(output)).execute()
            except:
                pass

    def build_rpm(self, srpm, distro, arch, output_dir):
        """ builds rpm from source RPM to distro and architecture
            binary RPM into output_dir """
        self.build_ret_code = 0

        def check_output(proc):
            while proc.poll() is None:
                line = proc.stdout.readline().decode("utf-8")
                if self._regex.search(line):
                    yield line
                print(line)
            self.build_ret_code = proc.returncode

        _ret = list(
            check_output(
                subprocess.Popen(
                    [
                        "mock", "--no-clean",
                        "--verbose",
                        "--root", distro + '-' + arch,
                        "--rebuild", path_to_str(srpm),
                        "--resultdir=" + path_to_str(self.temp_dir)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
            )
        ) + list(self._check_logs(self.temp_dir))
        self._move_files(output_dir, self.temp_dir.glob("*.rpm"))
        self.mock_logs = output_dir / "mock_logs"
        self._move_files(self.mock_logs, self.temp_dir.glob("*.log"))
        raise BuildException(_ret, self.build_ret_code)

    @staticmethod
    def fetch_repos(dist, arch):
        """ Initialize mock on distro and architecture for example:
            fedora-22 and x86-64 """
        logging.info("New thread for fetch repos started")
        config_file = dist + '-' + arch
        Command("mock --init -r " + config_file).execute()
