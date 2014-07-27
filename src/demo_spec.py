#! /usr/bin/python3
from datetime import datetime
from spec import *

# necessary initialization, because attributes are initialized to None by default
myspec = Spec()
myspec.tags = {}
myspec.scripts = {}
myspec.changelogs = []
myspec.subpackages = []

#add some tags
print("demo rpg: adding some tags into the Spec class...", file=sys.stderr)
myspec.tags["Name"] = ["demo rpg"]
myspec.tags["Version"] = ["1.0"]
myspec.tags["Summary"] = ["This is only a demo"]
myspec.tags["Requires"] = ["vlc"]
myspec.tags["Requires"].append("python")
myspec.tags["Requires"].append("dbus")
myspec.tags["BuildRequires"] = ["python2-devel"]
myspec.tags["BuildRequires"].append("python-simplejson")
myspec.tags["Patch"] = ["test_patch1"]
myspec.tags["Patch"].append("test patch2")
myspec.tags["Patch"].append("test patch3")

print("demo rpg: adding some scripts into Spec class...", file=sys.stderr)
myspec.scripts["%description"] = "lorem ipsum dolor sit amet"
myspec.scripts["%prep"] = "%setup -q -n %{name}-%{tar_ver}"
myspec.scripts["%build"] = "%{__python} setup.py build"
myspec.scripts["%install"] = "rm -rf $RPM_BUILD_ROOT\n\
make install INSTALLPREFIX=$RPM_BUILD_ROOT INSTALL='install -p -m 755'\n\
make install-man INSTALLPREFIX=$RPM_BUILD_ROOT INSTALL='install -p -m 644'"
myspec.scripts["%post"] = "/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :"
myspec.scripts["%postun"] = "if [ $1 -eq 0 ] ; then\n\
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null\n\
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :\n\
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :\n\
fi"

print("demo rpg: adding some changelogs...", file=sys.stderr)
date = datetime.now()
changelog1 = myspec.Changelog(date,"Erik","xskult00@stud.fit.vutbr.cz","changelog test 1")
changelog2 = myspec.Changelog(date,"Erik","xskult00@stud.fit.vutbr.cz","changelog test 2")
myspec.changelogs.append(changelog1)
myspec.changelogs.append(changelog2)
#print(changelog.date.month)
#myspec.add_tag("Requires","vlc","python","dbus")
#myspec.add_tag("BuildRequires", "python2-devel", "python-simplejson")
#myspec.add_script("description", "lorem ipsum dolor sit amet")

print("demo rpg: creating subpackages...", file=sys.stderr)
mypackage1 = Subpackage()
mypackage1.tags = {}
mypackage1.scripts = {}
mypackage1.files = set()

mypackage1.tags["Name"] = ["devel"]
mypackage1.tags["Summary"] = ["Development files for demo"]
mypackage1.tags["Group"] = ["Development/Libraries"]
mypackage1.tags["Requires"] = ["%{name}-libs%{?_isa} = %{version}-%{release}"]
mypackage1.tags["Requires"].append("glib2-devel%{?_isa}")
mypackage1.tags["Requires"].append("dbus-glib-devel%{?_isa}")
mypackage1.scripts["%description"] = "Files needed when building software for demo"

mypackage2 = Subpackage()
mypackage2.tags = {}
mypackage2.scripts = {}
mypackage2.files = set()

mypackage2.tags["Name"] = ["doc"]
mypackage2.tags["Summary"] = ["Documentation files for demo"]
mypackage2.tags["Group"] = ["Documentation"]
mypackage2.tags["BuildArch"] = ["noarch"]
mypackage2.scripts["%description"] = "Extra documentation files for demo"

print("demo rpg: appending subpackages into Spec class", file=sys.stderr)
myspec.subpackages.append(mypackage1)
myspec.subpackages.append(mypackage2)

print("demo rpg: writing final SPEC file...", file=sys.stderr)

file = open('demo_spec.spec', mode='w')
myspec.write(file)
file.close()
