from tests.support import RpgTestCase
from rpg import Base
import os


class BuildTest(RpgTestCase):

    def test_libhif(self):
        self.base = Base()
        self.base.sack = self.base.load_dnf_sack()
        self.base.load_plugins()
        self.base.load_project_from_url(
            "https://github.com/rpm-software-management/libhif")
        self.base.spec.Name = "LibHif"
        self.base.spec.Version = "0.6.11"
        self.base.spec.Release = "1%{?snapshot}%{?dist}"
        self.base.spec.License = "GPLv2"
        self.base.spec.Summary = "Library ..."
        self.base.spec.description = (
            "LibHif ...")
        self.base.spec.URL =\
            "https://github.com/rpm-software-management/libhif"
        self.base.target_arch = "x86_64"
        self.base.target_distro = "fedora-22"
        self.base.fetch_repos(self.base.target_distro, self.base.target_arch)
        self.base.run_extracted_source_analysis()
        self.base.run_patched_source_analysis()
        self.base.build_project()
        self.base.run_compiled_source_analysis()
        self.base.install_project()
        self.base.run_installed_source_analysis()
        self.base.build_srpm()
        self.assertTrue(self.base.srpm_path.exists())
        self.base.build_rpm_recover(
            self.base.target_distro, self.base.target_arch)
        self.assertTrue(self.base.rpm_path)

    def tearDown(self):
        for _rpm in self.base.rpm_path:
            os.remove(str(_rpm))
        os.remove(str(self.base.srpm_path))
        os.remove(str(self.base.spec_path))
