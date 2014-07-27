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
        self.files    = None  #set of tuple (src_file, target, tag, attr)
                              # e.g. %config, %doc, %ghost, %dir
                              
        self.tags     = None  # dict of tags: "key" -> list[vals]
                              # e.g. "Requires" -> ["foo", "bar"]
                                                            
        self.scripts  = None  # dict of scripts: "key" -> string
                              # e.g. "%prep" -> "%autosetup"
    
    # default write method used for packages
    # packages usually do not use all the tags nor scripts available,
    # e.g. patches, thus these are omitted from the writing process                     
    def write(self, out=sys.stdout):
        for tag in self.tag_keywords:
            if tag in self.tags.keys():
                for val in self.tags.get(tag):
                    if tag == "Name":
                        print("\n%package {}".format(val), file=out)
                    else:
                        print("{}: {}".format(tag,val), file=out)
        
        for script in self.script_keywords:
            if script in self.scripts.keys():
                print("\n{}\n{}".format(script+" "+self.tags['Name'][0],self.scripts.get(script)), file=out)


                     
class Spec(Subpackage):
    """SPEC properties holder"""
    def __init__(self):
        super(Spec, self).__init__()
        #self.license     = None
        #self.url         = None
        #self.vendor      = None
        #self.packager    = None
        self.subpackages = None  # list[Subpackage]
        self.changelogs  = None  # list[Changelog]
        #self.patches     = None  # list[str:paths]

    def load(source_file):
        pass
    
    
    # modified inherited write method
    def write(self, out=sys.stdout):
        patch_index = 1   # used for patch numbering
        
        # first tags need to written 
        for tag in self.tag_keywords:
            if tag in self.tags.keys():
                for val in self.tags.get(tag):
                    if tag == "Patch":
                        print("{}: {}".format(tag+str(patch_index),val), file=out)
                        patch_index += 1
                    else:
                        print("{}: {}".format(tag,val), file=out)
        
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
        __weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        __months   = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                      "Sep", "Oct", "Nov", "Dec"]
        
        def __init__(self, date, author, email, message):
            self.date = date
            self.author = author
            self.email = email
            self.message = message
        
        def __str__(self):
            return "* {} {} {} {} <{}>\n- {}".format(self.__weekdays[self.date.weekday()],
                                               self.__months[self.date.month],
                                               self.date.year,
                                               self.author,
                                               self.email,
                                               self.message)
