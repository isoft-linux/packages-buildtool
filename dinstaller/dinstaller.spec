Name: dinstaller
Summary:Installer Application
Version: 1.0
Release: 4
License: GPL2
Vendor: iSoft
Source0: dinstaller.tar.gz
BuildRequires: git cmake 
BuildRequires: parted-devel 
BuildRequires: qt5-qtbase-devel qt5-qttools-devel 
BuildRequires: mesa-libGL-devel mesa-libgbm-devel libGLU-devel
Requires: parted qt5-qtbase

%description
%{summary}

%prep
%setup -n %{name}


%build 
cmake . -DCMAKE_INSTALL_PREFIX=/usr
make


%install
make GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 DESTDIR=%{buildroot} install


%post
glib-compile-schemas --allow-any-name usr/share/glib-2.0/schemas ||:

%postun
glib-compile-schemas --allow-any-name usr/share/glib-2.0/schemas ||:

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*

%changelog
* Fri Oct 30 2015 sulit <sulitsrc@gmail.com.cn> - 1.0-2
- modify postscript.tmpl for using kernel3 and kernel

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 1.0-2
- Rebuild for new 4.0 release

