%define checksum b02404a8661d8084692292138c247ef4
Name:           minipkg
Version:        1.2
Release:        1%{?dist}
Summary:        Script to allow mpkg fetch to work

License:        GPLv2+
URL:            http://git.isoft.zhcn.cc/version-4/%{name}
Source0:	http://pkgs.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/%{checksum}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       curl, coreutils, rpmdevtools

#Conflicts:      fedpkg, mpkg


%description
Script for use in Koji to allow sources to be fetched

%prep
%setup -q

%build

%install
make PREFIX=%{buildroot}%{_prefix} install

%files
%doc README.md LICENSE
%{_bindir}/minipkg

%changelog
* Thu Nov 05 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 1.2-1
- update to minipkg 1.2, support empty sources.

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 1.1-2
- Rebuild for new 4.0 release
