# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           rpkg
Version:        1.38
Release:        1
Summary:        Utility for interacting with rpm+git packaging systems

Group:          Applications/System
License:        GPLv2+ and LGPLv2
URL:            https://fedorahosted.org/rpkg
Source0:        http://pkgs.isoft.zhcn.cc/repo/pkgs/rpkg/rpkg-%{version}.tar.gz/9b65de012587d0607d46b9a7a086acfc/rpkg-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       python
Requires:       pyrpkg >= %{version}-%{release}
Requires:       osbs

# Use this to force plugins to update
Conflicts:      fedpkg <= 1.7

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
# We br these things for man page generation due to imports
BuildRequires:  GitPython, koji, python-pycurl
BuildRequires:  python-kitchen
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  osbs

%description
A tool for managing RPM package sources in a git repository.

%package -n pyrpkg
Summary:        Python library for interacting with rpm+git
Group:          Applications/Databases
Requires:       GitPython >= 0.2.0
Requires:       python-pycurl, koji
Requires:       rpm-build, python-rpm
Requires:       rpmlint, mock, curl, openssh-clients
Requires:       python-kitchen
Requires:       python
Requires:       python-osbs

%description -n pyrpkg
A python library for managing RPM package sources in a git repository.


%prep
%setup -q


%build
%{__python} setup.py build
%{__python} src/rpkg_man_page.py > rpkg.1


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_mandir}/man1
%{__install} -p -m 0644 rpkg.1 $RPM_BUILD_ROOT%{_mandir}/man1

#%check
#%{__python} setup.py test
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%config(noreplace) %{_sysconfdir}/rpkg
%{_datadir}/bash-completion/completions/rpkg
%{_bindir}/%{name}
%{_mandir}/*/*

%files -n pyrpkg
%doc COPYING COPYING-koji LGPL README
# For noarch packages: sitelib
%{python_sitelib}/pyrpkg
#%{python_sitelib}/rpkg-%{version}-py?.?.egg-info


%changelog
* Wed Jul 15 2015 Pavol Babincak <pbabinca@redhat.com> - 1.36-1
- container-build: support yum repos with --build-with=koji (pbabinca)
- container-build: move --scratch option to koji group (pbabinca)
- Print task info for container-build (pbabinca)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Dennis Gilmore <dennis@ausil.us> - 1.35-2
- pyrpkg Requires python-osbs

* Tue May 26 2015 Pavol Babincak <pbabinca@redhat.com> - 1.35-1
- Test for scratch opt in the actual argument of container_build_koji
  (pbabinca)
- Move the GitIgnore class to its own module (bochecha)
- Modernize the gitignore-handling code (bochecha)
- gitignore: Properly handle adding matching lines (bochecha)
- Refactor: remove unnecessary code (pbabinca)
- Move custom UnknownTargetError to errors module (pbabinca)
- New command: container-build (jluza)
- lookaside: Take over file uploads (bochecha)
- Remove unnecessary log message (bochecha)
- Stop making source files read-only (bochecha)
- Drop some useless comments (bochecha)
- Only report we're uploading when we actually are (bochecha)
- lookaside: Check if a file already was uploaded (bochecha)
- lookaside: Allow client-side and custom CA certificates (bochecha)
- lookaside: Be more flexible when building the download URL (bochecha)
- lookaside: Use the hashtype for the URL interpolation (bochecha)
- lookaside: Add a progress callback (bochecha)
- lookaside: Handle downloading of source files (bochecha)
- lookaside: Move handling of file verification (bochecha)
- lookaside: Move handling of file hashing (bochecha)
- utils: Add a new warn_deprecated helper (bochecha)
- Add a new lookaside module (bochecha)
- Add a new utils module (bochecha)
- Properly set the logger (bochecha)
- Move our custom errors to their own module (bochecha)
- Don't assume MD5 for the lookaside cache (bochecha)
- Remove dead code (bochecha)
- Use the proper exception syntax (bochecha)

* Thu Apr 16 2015 Pavol Babincak <pbabinca@redhat.com> - 1.34-1
- tests: Don't use assertIsNone (bochecha)
- tests: Don't use assertRaises as a context manager (bochecha)
- Add long --verbose option to -v, new --debug and -d option (pbabinca)

* Mon Apr 13 2015 Pavol Babincak <pbabinca@redhat.com> - 1.33-1
- New mockbuild options: --no-clean --no-cleanup-after (jskarvad)
- Catch ssl auth problems and print more helpful messages (pbabinca)
- New exception - rpkgAuthError to allow clients detect auth problems
  (pbabinca)

* Mon Mar 23 2015 Pavol Babincak <pbabinca@redhat.com> - 1.32-1
- tests: Properly open/close the file (bochecha)
- sources: Support writing in either the old or new format (bochecha)
- sources: Reindent code (bochecha)

* Fri Mar 06 2015 Pavol Babincak <pbabinca@redhat.com> - 1.31-1
- Refactor: remove unused imports from test_sources (pbabinca)
- Don't do several times the same thing (bochecha)
- sources: Forbid mixing hash types (bochecha)
- sources: Move to the new file format (bochecha)
- Rewrite the sources module (bochecha)

* Wed Dec 03 2014 Pavol Babincak <pbabinca@redhat.com> - 1.30-2
- Use %%{__python} instead of %%{__python2} as it might be not defined

* Wed Oct 08 2014 Pavol Babincak <pbabinca@redhat.com> - 1.30-1
- add python-nose as BuildRequires as run tests in check section (pbabinca)
- pass extra data to the Commands object via properties instead of __init__()
  (mikeb)
- clean up Koji login, and properly support password auth (mikeb)
- add --runas option (mikeb)
- run os.path.expanduser on the kojiconfig attribute in case the path is in the
  user's home directory (bstinson)
- Override GIT_EDITOR in tests (pbabinca)
- Massive Flake8 fix (bochecha)
- Fix some more Flake8 issues (bochecha)
- Fix some flake8 issues (bochecha)
- Simplify some code (bochecha)
- Fix typo (bochecha)
- tests: Ensure functioning of Commands.list_tag (bochecha)
- list_tags: Stop executing a command (bochecha)
- list_tags: Fix the docstring (bochecha)
- delete_tag: Stop executing a command (bochecha)
- tests: Ensure functioning of Commands.delete_tag (bochecha)
- add_tag: Run the tag command in the right directory (bochecha)
- tests: Ensure proper functioning of Commands.add_tag (bochecha)
- tests: Factor out some code (bochecha)
- tests: Ensure functioning of Commands.clone (bochecha)
- gitignore: Make sure each line ends with a \n (bochecha)
- gitignore: We're not modified any more after we wrote to disk (bochecha)
- tests: Ensure proper functioning of GitIgnore (bochecha)
- tests: Use nose (bochecha)
- Remove unused import (bochecha)
- Some more PEP8 (bochecha)
- Add classifiers to setup.py (pbabinca)
- Add new sources file parser even with unit tests (pbabinca)
- If source file doesn't exist continue without downloading files (pbabinca)
- Reformat setup.py to be compliant with PEP 8 (pbabinca)

* Tue Sep 30 2014 Pavol Babincak <pbabinca@redhat.com> - 1.28-1
- Compare fuller remote branch name with local branch before build

* Fri Sep 26 2014 Pavol Babincak <pbabinca@redhat.com> - 1.27-1
- Explicitly define pyrpkg's client name for man pages (pbabinca)
- Refactor mock results dir to property (pbabinca)
- Add skip-diffs option for import_srpms (lars)
- Properly remove possible .py when creating man pages (lars)
- Process srpm imports to empty repositories more explicitly (pbabinca)
- Make UPLOADEXTS a class variable that can be extended (lars)
- Introduce self.default_branch_remote for fresh clones (pbabinca)
- On self.path change reset properties which could used old value (pbabinca)
- Remove empty entry from git ls-files to not confuse following code (pbabinca)
- Remove file names during srpm import in more extensible way (pbabinca)
- Fix issue causing all current local builds via fedpkg to use md5 rather than
  sha256 (spot)
- License replaced with official GPL 2.0 license from gnu.org (pbabinca)
- Allow "rpkg commit -s" (pjones)

* Tue Jul 29 2014 Pavol Babincak <pbabinca@redhat.com> - 1.26-1
- rpkg doesn't have a python module so use pyrpkg instead (pbabinca)

* Tue Jul 29 2014 Pavol Babincak <pbabinca@redhat.com> - 1.25-1
- 1.25 release (pbabinca)
- Note to do_imports() doc. (pbabinca)
- Change default option for switch-branch from --no-fetch to --fetch (pbabinca)
- Allow default name of the library to be set by subclasses (pbabinca)
- Use name attribute of cliClient to get configuration (pbabinca)
- Make setup.py executable (pbabinca)
- Use direct git call for fetches (pbabinca)
- Print reason for failed switch-branch (pbabinca)
- Match whole branch with remote name when switching branch (pbabinca)
- Refactor: deduplicate remote & branch_merge (pbabinca)
- De-hardcode 'origin' as the remote name (bochecha)
- Fallback the remote on 'origin' (bochecha)

* Mon Jun 09 2014 Pavol Babincak <pbabinca@redhat.com> - 1.24-1
- 1.24 release (pbabinca)
- Work around signed srpms (Till Maas)
- Properly raise the error (bochecha)
- Ability to skip NVR construction altogether for builds (pbabinca)
- If we failed to parse NVRE from rpm output use better error message
  (pbabinca)
- If command to get NVRE printed anything to stderr log that command (pbabinca)
- Refactor: correctly split string on multi lines (pbabinca)
- Use nvr_check as an optional argument for build (pbabinca)
- 1.23 release (pbabinca)
- Use module_name setter instead of constructor parameter (pbabinca)
- Set pushurl & branch_remote by default (pbabinca)
- 1.22 release (pbabinca)
- Define module name from command line, git url and lastly from spec (pbabinca)
- Revert "Define module name from command line, git url and lastly from spec"
  (pbabinca)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Pavol Babincak <pbabinca@redhat.com> - 1.21-1
- Refactor: split strings on multi lines without spaces from indentation
  (pbabinca)
- Refactor: remove spaces at the end of lines (pbabinca)
- Define module name from command line, git url and lastly from spec (pbabinca)
- Option to skip NVR existence check in build system before build (pbabinca)
- Add an 'epoch' property to pyrpkg.Commands (bochecha)
- Fetch remotes before switch-branch by default (pbabinca)
- Protect rhpkg's --arches argument (pbabinca)

* Tue Feb 18 2014 Dennis Gilmore <dennis@ausil.us> - 1.20-1
- read krbservice from the koji config file (dennis)
- We can assume that rpkg is installed if the (ville.skytta)
- clog: Don't require empty line between changelog entries. (ville.skytta)
- Spelling fixes. (ville.skytta)
- expand %%{name} and %%{verion} macros when checking for unused_patches check
  for .patch and .diff files as patches (dennis)
- clean up some language ambiguities (dennis)
- clog: Support %changelog tag written in non-lowercase. (ville.skytta)
- add spkg as a binary file extention rhbz#972903 (dennis)
- Fixed version to 1.19 (pbabinca)
- Don't track spec file here (pbabinca)
- 1.20 (pbabinca)
- Mock config temp dir in the form $(target)-$(localarch).$(mktemp)mockconfig
  (pbabinca)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 08 2013 Pavol Babincak <pbabinca@redhat.com> - 1.19-1
- Generate mock-config for mockbuild if needed (rhbz#856928) (pbabinca)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Robert Scheck <robert@fedoraproject.org> - 1.18-3
- Require %%{version}-%%{release} rather %%{name}-%%{version}

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Jesse Keating <jkeating@redhat.com> - 1.18-1
- Use rpmdefines when querying for package name

* Mon Apr 09 2012 Jesse Keating <jkeating@redhat.com> - 1.17-1
- Don't assume master branch for chain builds (jkeating)

* Mon Mar 26 2012 Jesse Keating <jkeating@redhat.com> - 1.16-1
- Only read from .koji/config (jkeating)

* Wed Mar 21 2012 Jesse Keating <jkeating@redhat.com> - 1.15-1
- Fix branch push warning (jkeating)
- Handle CVS based builds when getting build hash (jkeating)

* Mon Mar 12 2012 Jesse Keating <jkeating@redhat.com> - 1.14-1
- Warn if the checked out branch cannot be pushed (jkeating)
- Warn if commit or tag fails and we don't push (#21) (jkeating)
- Honor ~/.koji/config (rhbz#785776) (jkeating)
- Update help output for switch-branch (rhbz#741742) (jkeating)

* Thu Mar 01 2012 Jesse Keating <jkeating@redhat.com> - 1.13-1
- Return proper exit code from builds (#20) (jkeating)
- Fix md5 option in the build parser (jkeating)
- More completion fixes (jkeating)
- Add mock-config and mockbuild completion (jkeating)
- Simplify test for rpkg availability. (ville.skytta)
- Fix ~/... path completion. (ville.skytta (jkeating)
- Add a --raw option to clog (#15) (jkeating)
- Make things quiet when possible (jkeating)
- Fix up figuring out srpm hash type (jkeating)
- Allow defining an alternative builddir (jkeating)
- Conflict with older fedpkg (jkeating)
- Attempt to automatically set the md5 flag (jkeating)
- Use -C not -c for config.  (#752411) (jkeating)
- Don't check gpg sigs when importing srpms (ticket #16) (jkeating)
- Enable md5 option in mockbuild (twaugh) (jkeating)

* Tue Jan 24 2012 Jesse Keating <jkeating@redhat.com> - 1.12-1
- Fix mock-config (ticket #13) (jkeating)
- Make md5 a common build argument (jkeating)
- Move arches to be a common build argument (ticket #3) (jkeating)
- Find remote branch to track better (jkeating)

* Fri Jan 13 2012 Jesse Keating <jkeating@redhat.com> - 1.11-1
- Change clog output to be more git-like (sochotnicky)
- Fix mockconfig property (bochecha)
- Use only new-style classes everywhere. (bochecha)
- Testing for access before opening a file is unsafe (bochecha)
- Add a gitbuildhash command (jkeating)
- Always make sure you have a absolute path (aj) (jkeating)
- don't try to import brew, just do koji (jkeating)

* Mon Nov 21 2011 Jesse Keating <jkeating@redhat.com> - 1.10-1
- Use -C for --config shortcut (jkeating)
- Don't leave a directory on failure (#754082) (jkeating)
- Fix chain build (#754189) (jkeating)
- Don't hardcode brew here (jkeating)

* Mon Nov 07 2011 Jesse Keating <jkeating@redhat.com> - 1.9-1
- Don't upload if there is nothing to upload. (jkeating)
- --branch option for import is not supported yet (jkeating)
- Add epilog about mock-config generation (jkeating)
- Don't assume we can create a folder named after the module. (bochecha)
- Fix passing the optional mock root to mockbuild (bochecha)
- Add missing registration for mockbuild target (bochecha)
- Make the clean target work with --path. (bochecha)
- Fix typo in a comment. (bochecha)
- Fix syntax error in main script. (bochecha)
- Fix typo. (bochecha)

* Fri Oct 28 2011 Jesse Keating <jkeating@redhat.com> - 1.8-1
- Get more detailed error output from lookaside (jkeating)
- Move the curl call out to it's own function (jkeating)
- Hide build_common from help/usage (jkeating)
- Fix the help command (jkeating)

* Tue Oct 25 2011 Jesse Keating <jkeating@redhat.com> - 1.7-1
- Support a manually specified mock root (jkeating)
- Add a mock-config subcommand (jkeating)
- Fix a traceback on error. (jkeating)
- Remove debugging code (jkeating)
- More git api updates (jkeating)
- Add topurl as a koji config and property (jkeating)
- Add a mockconfig property (jkeating)
- Turn the latest commit into a property (jkeating)

* Tue Sep 20 2011 Jesse Keating <jkeating@redhat.com> - 1.6-1
- Allow name property to load by itself (jkeating)

* Mon Sep 19 2011 Jesse Keating <jkeating@redhat.com> - 1.5-1
- Fix tag listing (#717528) (jkeating)
- Revamp n-v-r property loading (#721389) (jkeating)
- Don't use os.getlogin (jkeating)
- Code style changes (jkeating)
- Allow fedpkg lint to be configurable and to check spec file. (pingou)
- Handle non-scratch srpm builds better (jkeating)

* Wed Aug 17 2011 Jesse Keating <jkeating@redhat.com> - 1.4-1
- Be more generic when no spec file is found (jkeating)
- Hint about use of git status when dirty (jkeating)
- Don't use print when we can log.info it (jkeating)
- Don't exit from a library (jkeating)
- Do the rpm query in our module path (jkeating)
- Use git's native ability to checkout a branch (jkeating)
- Use keyword arg with clone (jkeating)
- Allow the on-demand generation of an srpm (jkeating)
- Fix up exit codes (jkeating)

* Mon Aug 01 2011 Jesse Keating <jkeating@redhat.com> - 1.3-1
- Fix a debug string (jkeating)
- Set the right property (jkeating)
- Make sure we have a default hashtype (jkeating)
- Use underscore for the dist tag (jkeating)
- Fix the kojiweburl property (jkeating)

* Wed Jul 20 2011 Jesse Keating <jkeating@redhat.com> - 1.2-1
- Fill out the krb_creds function (jkeating)
- Fix the log message (jkeating)
- site_setup is no longer needed (jkeating)
- Remove some rhtisms (jkeating)
- Wire up the patch command in client code (jkeating)
- Add a patch command (jkeating)

* Fri Jun 17 2011 Jesse Keating <jkeating@redhat.com> - 1.1-2
- Use version macro in files

* Fri Jun 17 2011 Jesse Keating <jkeating@redhat.com> - 1.1-1
- New tarball release with correct license files

* Fri Jun 17 2011 Jesse Keating <jkeating@redhat.com> - 1.0-2
- Fix up things found in review

* Tue Jun 14 2011 Jesse Keating <jkeating@redhat.com> - 1.0-1
- Initial package
