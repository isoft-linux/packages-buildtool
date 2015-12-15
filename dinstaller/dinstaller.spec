Name: dinstaller
Summary:Installer Application
Version: 1.0
Release: 25
License: GPL2
Vendor: iSoft
Source0: dinstaller.tar.gz
Patch0: create-kernel-initrd-4.3-and-4.2.patch
Patch1: enable_isoftapp.patch
Patch2: init_rpmdb.patch
Patch4: modify_baloo_file.desktop.patch
# it will be removed later
Patch3: umount-livecd.patch
BuildRequires: git cmake 
BuildRequires: parted-devel 
BuildRequires: qt5-qtbase-devel qt5-qttools-devel 
BuildRequires: mesa-libGL-devel mesa-libgbm-devel libGLU-devel
Requires: parted qt5-qtbase

%description
%{summary}

%prep
%setup -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
%{_libdir}/*
%{_sysconfdir}/*

%changelog
* Tue Dec 15 2015 <ming.wang@i-soft.com.cn> - 1.0-25
- Show tip when logical partition renamed.

* Wed Dec 09 2015 <ming.wang@i-soft.com.cn> - 1.0-24
- Add executable dinstall-cmdline.

* Tue Dec 08 2015 sulit <sulitsrc@gmail.com> - 1.0-23
- enable baloo_file patch

* Mon Dec 07 2015 sulit <sulitsrc@gmail.com> - 1.0-22
- add umount-livecd patch
- it will be removed later

* Wed Dec 02 2015 wangming <ming.wang@i-soft.com.cn> - 1.0-21
- Auto install when matched specify  MAC address.

* Fri Nov 27 2015 wangming <ming.wang@i-soft.com.cn> - 1.0-20
- Modify licence file.

* Fri Nov 20 2015 sulit <sulitsrc@gmail.com> - 1.0-19
- add init-rpmdb patch

* Fri Nov 20 2015 sulit <sulitsrc@gmail.com> - 1.0-18
- add enable-isoftapp patch

* Fri Nov 20 2015 wangming <ming.wang@i-soft.com.cn> - 1.0-15
- Fixed size.

* Fri Nov 20 2015 sulit <sulitsrc@gmail.com> - 1.0-14
- modify baloo_file.desktop for new os, because baloo_file
- is disabled in live-cd.

* Wed Nov 11 2015 wangming <ming.wang@i-soft.com.cn> - 1.0-13
- Create home mount point can not with type vfat. Optimize postscript.

* Fri Nov 06 2015 wangming <ming.wang@i-soft.com.cn> - 1.0-12
- New ui for 4.0.

* Thu Nov 05 2015 sulit <sulitsrc@gmail.com> - 1.0-11
- put kernel and kernel42 to iso and use kernel as default boot kernel

* Tue Nov 03 2015 sulit <sulitsrc@gmail.com> - 1.0-10
- redo modify postscript.tmpl

* Tue Nov 03 2015 sulit <sulitsrc@gmail.com> - 1.0-5
- add enable repairdev for postscript.tmpl

* Fri Oct 30 2015 sulit <sulitsrc@gmail.com> - 1.0-2
- modify postscript.tmpl for using kernel3 and kernel

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 1.0-2
- Rebuild for new 4.0 release

