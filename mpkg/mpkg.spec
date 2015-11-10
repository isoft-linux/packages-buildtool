# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%define checksum 7db1ceb24d83c2e8b184fbf812e7cff8

Name:           mpkg
Version:        1.24
Release:        1
Summary:        Moses utility for working with dist-git

License:        GPLv2+
URL:            http://fedorahosted.org/fedpkg
Source0:	http://pkgs.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/%{checksum}/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       pyrpkg >= 1.33
Requires:       python-pycurl, koji
Requires:       packagedb-cli > 2.2
Requires:       packagedb-cli

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
# We br these things for man page generation due to imports
BuildRequires:  pyrpkg
BuildRequires:  packagedb-cli > 2.2

%description
Provides the fedpkg command for working with dist-git

%prep
%setup -q

%build
%{__python} setup.py build
%{__python} src/mpkg_man_page.py > mpkg.1


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_mandir}/man1
%{__install} -p -m 0644 mpkg.1 $RPM_BUILD_ROOT%{_mandir}/man1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%config(noreplace) %{_sysconfdir}/rpkg
%{_datadir}/bash-completion/completions
%{_bindir}/%{name}
%{_mandir}/man1
# For noarch packages: sitelib
%{python_sitelib}/*

%changelog
* Tue Nov 10 2015 xiaotian.wu@i-soft.com.cn - 1.24-1
- new version, add search command.

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 1.23-2
- Rebuild for new 4.0 release
