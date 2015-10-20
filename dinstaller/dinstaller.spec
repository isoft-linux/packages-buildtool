Name: dinstaller
Version: 1.0
Release: 1
License: GPL2
Vendor: iSoft
Group: moses
Source0: dinstaller.tar.gz
BuildRequires: git cmake parted-devel qt5-qtbase-devel qt5-qttools-devel mesa-libGL-devel mesa-libOpenCL-devel mesa-libOSMesa-devel mesa-libgbm-devel mesa-libGLw libGLU-devel mesa-libEGL-devel
Summary:Installer Application
Requires: parted qt5-qtbase


%description


%prep
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/dinstaller


%setup -n %{name}


%build 
cmake . -DCMAKE_INSTALL_PREFIX=/usr
make


%install
make GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 DESTDIR=%{buildroot} install


%post
glib-compile-schemas --allow-any-name usr/share/glib-2.0/schemas


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*

%changelog
