import re
import sys

class Subpackage:

    # Holds the most common keywords used with SPEC file tags, along with the
    # conventional order preserved
    tag_keywords = ["Name", "Version", "Release", "Summary", "Group", "License",
                    "URL", "Source", "Patch", "BuildArch", "BuildRoot", 
                    "BuildRequires", "Requires", "Provides", "Obsoletes",
                    "Conflicts", "Vendor", "Packager"]
    
    # Holds the most common keywords use with SPEC file scripts, along with the
    # conventional order preserved
    script_keywords = ["%description", "%package", "%prep", "%build", "%pre",
                       "%install", "%check", "%post", "%preun", "%postun", 
                       "%pretrans", "%posttrans", "%clean", "%files", 
                       "%changelog"]

    def __init__(self):
        self.files = set()    #set of tuple (src_file, target, tag, attr)
                              # e.g. %config, %doc, %ghost, %dir
                              
        self.tags = {}     # dict of tags: "key" -> list[vals]
                           # e.g. "Requires" -> ["foo", "bar"]
                           # in case of single value tag, no list of values is
                           # needed, e.g. "Name" -> "foo", "Sumary" -> bar
                                                            
        self.scripts = {}  # dict of scripts: "key" -> string
                           # e.g. "%prep" -> "%autosetup"


    def write(self, out):
        """Default write method used for packages. Packages usually do not use
        all the tags nor scripts available, e.g. patches, thus these are omitted
        from the writing process."""
        
        for tag in self.tag_keywords:
            if tag in self.tags.keys():
                tag_value = self.tags.get(tag)
                value_type = type(tag_value)
                if value_type is list:  # item is a list of values
                    for val in tag_value:
                        print("{}: {}".format(tag,val), file=out)
                        
                else:  # item is a single value
                    if tag == "Name":
                        print("\n%package {}".format(tag_value), file=out)
                    else:
                        print("{}: {}".format(tag,tag_value), file=out)
        
        for script in self.script_keywords:
            if script in self.scripts.keys():
                try:
                    print("\n{}\n{}".format(script+" "+self.tags['Name'],
                                        self.scripts.get(script)), file=out)
                except TypeError:
                    print("\n{}\n{}".format(script+" "+self.tags['Name'][0],
                                        self.scripts.get(script)), file=out)
    
    def mark_doc(self, file):
        """Helper function for GUI to mark additional files as documentation.
        Function adds '%doc' attribute to a specific file or creates a new entry
        in the set of files."""
        
        pass
                     
class Spec(Subpackage):
    """SPEC properties holder"""
    
    def __init__(self):
        super(Spec, self).__init__()
        self.subpackages = None  # list[Subpackage]
        self.changelogs = None  # list[Changelog]

    def load(source_file):
        pass
    
    def write(self, out):
        """Modified inherited write method. See Subpackage.write() for more
        information."""
        
        patch_index = 1   # used for patch numbering
        
        # first tags need to written 
        for tag in self.tag_keywords:
            if tag in self.tags.keys():
                tag_value = self.tags.get(tag)
                value_type = type(tag_value)
                if value_type is list:    # item is a list of values
                    for val in tag_value:
                        if tag == "Patch":
                            print("{}: {}".format(tag+str(patch_index),val), file=out)
                            patch_index += 1
                        else:
                            print("{}: {}".format(tag,val), file=out)
                else:    # item is a single value
                    print("{}: {}".format(tag,tag_value), file=out)
                    
        # second packages and scripts need to be written       
        for script in self.script_keywords:
            if script == "%package":
                for package in self.subpackages:
                    package.write(out)
                        
            if script in self.scripts.keys():
                print("\n{}\n{}".format(script,self.scripts.get(script)), file=out)

        # changelog is the last to be written at the end of file
        print("\n%changelog", file=out)
        for changelog in self.changelogs:
            print("{}\n".format(changelog), file=out)


    class Changelog:
        _weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        _months   = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                      "Sep", "Oct", "Nov", "Dec"]
        
        def __init__(self, date, author, email, message):
            self.date = date
            self.author = author
            self.email = email
            self.message = message
        
        def __str__(self):
            return "* {} {} {} {} <{}>\n- {}".format(self._weekdays[self.date.weekday()],
                                               self._months[self.date.month],
                                               self.date.year,
                                               self.author,
                                               self.email,
                                               self.message)
