Name: dinstaller
Summary:Installer Application
Version: 1.0
Release: 40
License: GPL2
Vendor: iSoft
Source0: dinstaller.tar.gz

Patch0: licence-changed.patch
Patch1: remove-deprecated-method.patch

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
* Mon Jan 18 2016 sulit <sulitsrc@gmail.com> - 1.0-40
- remove deprecated method

* Thu Jan 14 2016 <ming.wang@i-soft.com.cn> - 1.0-39
- Licence file changed.

* Thu Jan 14 2016 <ming.wang@i-soft.com.cn> - 1.0-37
- Merge patch, inhibit screen saver, skip over device which is busy.

* Tue Jan 05 2016 sulit <sulitsrc@gmail.com> - 1.0-36
- modify rpm remove list

* Tue Jan 05 2016 sulit <sulitsrc@gmail.com> - 1.0-35
- remove osmaintaintools from os

* Mon Jan 04 2016 sulit <sulitsrc@gmail.com> - 1.0-34
- replace rpm commandline for --os

* Mon Jan 04 2016 <ming.wang@i-soft.com.cn> - 1.0-33
- Merge patch from koji.

* Thu Dec 31 2015 <ming.wang@i-soft.com.cn> - 1.0-32
- Modify logo and licenses file.

* Mon Dec 28 2015 <ming.wang@i-soft.com.cn> - 1.0-31
- Add mac address for testing automatic install.

* Wed Dec 23 2015 <ming.wang@i-soft.com.cn> - 1.0-30
- Show detail for change of logical partition.

* Mon Dec 21 2015 sulit <sulitsrc@gmail.com> - 1.0-29
- modify grub conf for nvidia and amd
- rename os name

* Wed Dec 16 2015 <ming.wang@i-soft.com.cn> - 1.0-28
- Modify autoins.service.

* Wed Dec 16 2015 <ming.wang@i-soft.com.cn> - 1.0-27
- Set permission of check-autoins.sh

* Tue Dec 15 2015 <ming.wang@i-soft.com.cn> - 1.0-26
- fixed bug 13079.

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

