Name:           packagedb-cli
Version:        2.8.2
Release:        3
Summary:        A CLI for pkgdb

License:        GPLv2+
URL:            https://fedorahosted.org/packagedb-cli/
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel} && 0%{?rhel} < 6 
# EPEL 5
BuildRequires:  python26
Requires:       python26-argparse
%else
# EPEL6+, Fedora
BuildRequires:  python
%endif
BuildRequires:  python-setuptools
#BuildRequires:  python-fedora
BuildRequires:  python-bugzilla
#BuildRequires:  fedora-cert
BuildRequires:  koji

# EPEL6+, Fedora13-
%if 0%{?rhel} >= 6 || ( 0%{?fedora} && 0%{?fedora} <= 13 )
Requires:       python-argparse
%endif

#Requires(post): python-fedora
Requires(post): python-requests
Requires:       python-bugzilla
Requires:       koji
#Requires:       fedora-cert
Requires:       python-beautifulsoup4
Requires:       python-setuptools
Provides:       pkgdb-cli = %{version}-%{release}

%description
packagedb-cli is a command line interface of the well-known
packagedb of the Fedora project.

It allows you to manage the ACL for your packages as well
as requesting new ACL for new packages.
It also allows you to orphan and/or retire your package(s).

%prep
%setup -q

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}


%files
%doc README LICENSE
%{python_sitelib}/pkgdb2client/
%{python_sitelib}/packagedb_cli*.egg-info
%{_bindir}/pkgdb-cli
%{_bindir}/pkgdb-admin


%changelog
* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 2.8.2-3
- Rebuild for new 4.0 release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.8.2-1
- Update to 2.8.2
- Add the `info` action to get detail about one or more action(s)
- Fix pkgdb-admin to complain when a package review is not set to `+`

* Fri Feb 06 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.8.1-1
- Update 2.8.1
- Fix install the pkgdb-admin script

* Fri Feb 06 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.8-1
- Update to 2.8
- Add the new pkgdb-admin script for rel-eng to process requests made in pkgdb2
- Drop the --test argument
- Add the --pkgdburl, --bzurl, --fasurl and --insecure arguments allowing to
  specify which applications to query and wether to check the SSL cert or not

* Wed Jan 21 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.7-1
- Update to 2.7
- Add the `pending` action to retrieve someone's pending ACLs requests
- Provide a better description message for the --user arguments
- Fix the instructions in the README on how to run pkgdb-cli from the git tree

* Thu Dec 11 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.6.1-1
- Update to 2.6.1
- Check the max length of the package names
  This way the first column will always be either 33 char of length or the
  maximum length of the package names plus two extra characters.
- Fix pkgdb-cli orphan --retire (Alexander Kurtakov)

* Fri Nov 21 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.6-1
- Update to 2.6
- New structure: use the traditional python module structure instead of two
  python files
- Do one API call for `orphan --retire`
- Prevent user from retiring packages that have no dead.package file
- Add support for obsoleting ACL requests (Stanislav Ochotnicky)
- Enable restricting orphan to a specific user (while specifying more branches)
- Enable restricting give to a specific user (while specifying more branches)
- Let the unorphan action call the unorphan API endpoint
- When listing packages, encode the output as UTF-8 before printing

* Wed Jul 30 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.5-1
- Update to 2.5
- Fixes https://bugzilla.redhat.com/1123524 (Don't add stream handler to root
  logger in library)
- Add the update_critpath method to pkgdb2client

* Tue Jul 15 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.4-1
- Update to 2.4
- Fixes https://bugzilla.redhat.com/1119099 (--list and --branch do not work
  together)

* Mon Jun 16 2014 Luke Macken <lmacken@redhat.com> - 2.3.1-2
- Require python-setuptools (#1108974)

* Thu Jun 12 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.3.1-1
- Update to 2.3.1
- Fixes https://bugzilla.redhat.com/1108634 (orphaned branches may have no ACLs
  registered at all)

* Tue Jun 10 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.3-1
- Update to 2.3
- Add to pkgdb2client a method to retrieve the version of the pkgdb API
- Add to pgkdb2client a method to retrieve a packager's packages
- Have pkgdb-cli list --user rely on the new pkgdb2 API endpoint (if present)
- pkgdb-cli list --user returns all the packages unless asked otherwise (which
  is what it used to do w/ pkgdb1)
- Add the pkgdb2client the possibility to save the session to a file
  ~/.cache/pkgdb-session.pickle by default
- Add a login_callback method to pkgdb2client
- Fix asking for password only if required (ie: not provided via --password)
- Add support for on-demand authentication
- Order the user in the ACL output
- Order the ACL output per branch

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2-2
- Add missing requires on python-beautifulsoup4 RHBZ#1100496

* Thu May 15 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2-1
- Update to 2.2
- Replaces `devel` by `master`
- Fix layout for groups
- Rely on /api/critpath for the get_critpath_packages method
- Log URLs before calling them rather than after

* Thu May 15 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.1-1
- Update to 2.1
- Adds supports to pkgdb2client for the critpath filtering or querying

* Wed May 14 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.0-1
- Update to 2.0 for pkgdb2
- Adjust spec to rely on the newly included setup.py
- Add BR on python-setuptools (and explicitely on python-requests)
- Adjust the BR now that we use setup.py, all R are also BR

* Mon Mar 10 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.7.0-1
- Update to 1.7.0
- Add the branches command
- Fix the --branch filter in the list command

* Sat Sep 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.6.0-1
- Update to 1.6.0
- Fixes RHBZ#1002694 (rework the retire process, remove toggling)

* Thu Sep 05 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.5.1-1
- Update to 1.5.1
- Fixes RHBZ#995430 and RHBZ#970120

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.5.0-1
- Update to 1.5.0
- Fixes RHBZ#966196

* Thu Mar 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.4.1-2
- Backport 0001-Reverse-debuggingchanges.patch from upstream repo (fixes bz#918909)

* Thu Feb 28 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.4.1-1
- Update to 1.4.1
- Fixes bug #916581

* Thu Feb 21 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.4.0-1
- Update to 1.4.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.3.0-1
- Update to 1.3.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 21 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.2.1-1
- Update to 1.2.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.0-3
- Add koji and fedora-cert as Requires

* Fri Nov 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.0-2
- Add python-bugzilla as a requires

* Thu Jul 28 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.0-1
- Update to 1.1.0

* Fri Jul 01 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0.0-6
- Bump release

* Fri Jul 01 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0.0-5
- Add a Provides to pkgdb-cli

* Wed Jun 29 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0.0-4
- Make the spec compatible with epel5 (add BuildRoot and test for R/BR)

* Wed Jun 29 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0.0-3
- Fix the usage in the -h/--help by sed (already fixed upstream)

* Wed Jun 29 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0.0-2
- Used a temporary solution for Source0 for the review

* Wed Jun 29 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0.0-1
- First package for Fedora
