# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           mpkg
Version:        1.22
Release:        1%{?dist}
Summary:        Moses utility for working with dist-git

Group:          Applications/System
License:        GPLv2+
URL:            http://fedorahosted.org/fedpkg
Source0:        http://pkgs.isoft.zhcn.cc/repo/pkgs/mpkg/mpkg-%{version}.tar.gz/1a7e71096e7d1f3a375e62c085d568c7/mpkg-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       pyrpkg >= 1.33
Requires:       python-pycurl, koji
#Requires:      python-fedora, redhat-rpm-config, bodhi-client
Requires:       packagedb-cli > 2.2
#Requires:      fedora-cert
Requires:       packagedb-cli
%if 0%{?rhel} == 5 || 0%{?rhel} == 4
Requires:       python-kitchen
%endif

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
# We br these things for man page generation due to imports
BuildRequires:  pyrpkg
#BuildRequires:  fedora-cert
# This until fedora-cert gets fixed
BuildRequires:  packagedb-cli > 2.2
#BuildRequires:  python-fedora


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
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
