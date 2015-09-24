Name:           mpkg-minimal
Version:        1.0
Release:        1%{?dist}
Summary:        Script to allow mpkg fetch to work

Group:          Applications/System
License:        GPLv2+
URL:            http://git.isoft.zhcn.cc/version-4/%{name}
Source0:	http://pkgs.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/eadb68b02eb91f2447063e84645e5e41/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       curl, coreutils, rpmdevtools

Conflicts:      fedpkg, mpkg


%description
Script for use in Koji to allow sources to be fetched

%prep
%setup -q

%build

%install
make PREFIX=%{buildroot}%{_prefix} install

%files
%doc README.md LICENSE
%{_bindir}/mpkg

%changelog
