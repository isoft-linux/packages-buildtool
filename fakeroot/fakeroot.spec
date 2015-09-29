Summary: Gives a fake root environment
Name: fakeroot
Version: 1.20.2
Release: 1%{?dist}
License: GPL+
Group: Development/Tools
URL: http://fakeroot.alioth.debian.org/
Source0: http://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.orig.tar.bz2
# Address some POSIX-types related problems.
Patch0: fakeroot-inttypes.patch
BuildRequires: /usr/bin/getopt
BuildRequires: libcap-devel
# uudecode used by tests/tartest
BuildRequires: sharutils
Requires: /usr/bin/getopt
Requires: fakeroot-libs = %{version}-%{release}
Requires(post): /usr/sbin/alternatives
Requires(post): /usr/bin/readlink
Requires(preun): /usr/sbin/alternatives


%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.

%package libs
Summary: Gives a fake root environment (libraries)
Group: Development/Tools

%description libs
This package contains the libraries required by %{name}.

%prep
%setup -q
%patch0 -p1 -b .inttypes

for file in ./doc/*/*.1; do
  iconv -f latin1 -t utf8 < $file > $file.new
  mv -f $file.new $file
done

%build
for type in sysv tcp; do
mkdir obj-$type
cd obj-$type
cat >> configure << 'EOF'
#!/bin/sh
exec ../configure "$@"
EOF
chmod +x configure
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --libdir=%{_libdir}/libfakeroot \
  --with-ipc=$type \
  --program-suffix=-$type
make
cd ..
done

%install
for type in sysv tcp; do
  make -C obj-$type install libdir=%{_libdir}/libfakeroot DESTDIR=%{buildroot}
  chmod 644 %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so 
  mv %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so \
     %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  strip -s %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.*la
  %find_lang faked-$type --without-mo --with-man
  %find_lang fakeroot-$type --without-mo --with-man
done

cat fake{d,root}-{sysv,tcp}.lang > fakeroot.lang

%check
for type in sysv tcp; do
  make -C obj-$type check
done

%post
link=$(readlink -e "/usr/bin/fakeroot")
if [ "$link" = "/usr/bin/fakeroot" ]; then
  rm -f /usr/bin/fakeroot
fi
link=$(readlink -e "%{_bindir}/faked")
if [ "$link" = "%{_bindir}/faked" ]; then
  rm -f "%{_bindir}/faked"
fi
link=$(readlink -e "%{_libdir}/libfakeroot/libfakeroot-0.so")
if [ "$link" = "%{_libdir}/libfakeroot/libfakeroot-0.so" ]; then
  rm -f "%{_libdir}/libfakeroot/libfakeroot-0.so"
fi

/usr/sbin/alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-tcp" 50 \
  --slave %{_bindir}/faked faked %{_bindir}/faked-tcp \
  --slave %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-tcp.so \
  --slave %{_mandir}/man1/fakeroot.1.gz fakeroot.1.gz %{_mandir}/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/man1/faked.1.gz faked.1.gz %{_mandir}/man1/faked-tcp.1.gz \
  --slave %{_mandir}/de/man1/fakeroot.1.gz fakeroot.de.1.gz %{_mandir}/de/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/de/man1/faked.1.gz faked.de.1.gz %{_mandir}/de/man1/faked-tcp.1.gz \
  --slave %{_mandir}/es/man1/fakeroot.1.gz fakeroot.es.1.gz %{_mandir}/es/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/es/man1/faked.1.gz faked.es.1.gz %{_mandir}/es/man1/faked-tcp.1.gz \
  --slave %{_mandir}/fr/man1/fakeroot.1.gz fakeroot.fr.1.gz %{_mandir}/fr/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/fr/man1/faked.1.gz faked.fr.1.gz %{_mandir}/fr/man1/faked-tcp.1.gz \
  --slave %{_mandir}/nl/man1/fakeroot.1.gz fakeroot.nl.1.gz %{_mandir}/nl/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/nl/man1/faked.1.gz faked.nl.1.gz %{_mandir}/nl/man1/faked-tcp.1.gz \
  --slave %{_mandir}/pt/man1/fakeroot.1.gz fakeroot.pt.1.gz %{_mandir}/pt/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/pt/man1/faked.1.gz faked.pt.1.gz %{_mandir}/pt/man1/faked-tcp.1.gz \
  --slave %{_mandir}/sv/man1/fakeroot.1.gz fakeroot.sv.1.gz %{_mandir}/sv/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/sv/man1/faked.1.gz faked.sv.1.gz %{_mandir}/sv/man1/faked-tcp.1.gz

/usr/sbin/alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-sysv" 40 \
  --slave %{_bindir}/faked faked %{_bindir}/faked-sysv \
  --slave %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-sysv.so \
  --slave %{_mandir}/man1/fakeroot.1.gz fakeroot.1.gz %{_mandir}/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/man1/faked.1.gz faked.1.gz %{_mandir}/man1/faked-sysv.1.gz \
  --slave %{_mandir}/de/man1/fakeroot.1.gz fakeroot.de.1.gz %{_mandir}/de/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/de/man1/faked.1.gz faked.de.1.gz %{_mandir}/de/man1/faked-sysv.1.gz \
  --slave %{_mandir}/es/man1/fakeroot.1.gz fakeroot.es.1.gz %{_mandir}/es/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/es/man1/faked.1.gz faked.es.1.gz %{_mandir}/es/man1/faked-sysv.1.gz \
  --slave %{_mandir}/fr/man1/fakeroot.1.gz fakeroot.fr.1.gz %{_mandir}/fr/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/fr/man1/faked.1.gz faked.fr.1.gz %{_mandir}/fr/man1/faked-sysv.1.gz \
  --slave %{_mandir}/nl/man1/fakeroot.1.gz fakeroot.nl.1.gz %{_mandir}/nl/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/nl/man1/faked.1.gz faked.nl.1.gz %{_mandir}/nl/man1/faked-sysv.1.gz \
  --slave %{_mandir}/pt/man1/fakeroot.1.gz fakeroot.pt.1.gz %{_mandir}/pt/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/pt/man1/faked.1.gz faked.pt.1.gz %{_mandir}/pt/man1/faked-sysv.1.gz \
  --slave %{_mandir}/sv/man1/fakeroot.1.gz fakeroot.sv.1.gz %{_mandir}/sv/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/sv/man1/faked.1.gz faked.sv.1.gz %{_mandir}/sv/man1/faked-sysv.1.gz

%preun
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove fakeroot "%{_bindir}/fakeroot-tcp"
  /usr/sbin/alternatives --remove fakeroot "%{_bindir}/fakeroot-sysv"
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS BUGS DEBUG doc/README.saving
%{_bindir}/faked-*
%ghost %{_bindir}/faked
%{_bindir}/fakeroot-*
%ghost %{_bindir}/fakeroot
%{_mandir}/man1/faked-sysv.1*
%{_mandir}/man1/faked-tcp.1*
%{_mandir}/man1/fakeroot-sysv.1*
%{_mandir}/man1/fakeroot-tcp.1*
%ghost %{_mandir}/man1/faked.1.gz
%ghost %{_mandir}/man1/fakeroot.1.gz
%ghost %lang(de) %{_mandir}/de/man1/faked.1.gz
%ghost %lang(de) %{_mandir}/de/man1/fakeroot.1.gz
%ghost %lang(es) %{_mandir}/es/man1/faked.1.gz
%ghost %lang(es) %{_mandir}/es/man1/fakeroot.1.gz
%ghost %lang(fr) %{_mandir}/fr/man1/faked.1.gz
%ghost %lang(fr) %{_mandir}/fr/man1/fakeroot.1.gz
%ghost %lang(pt) %{_mandir}/pt/man1/faked.1.gz
%ghost %lang(pt) %{_mandir}/pt/man1/fakeroot.1.gz
%ghost %lang(sv) %{_mandir}/sv/man1/faked.1.gz
%ghost %lang(sv) %{_mandir}/sv/man1/fakeroot.1.gz
%ghost %lang(nl) %{_mandir}/nl/man1/faked.1.gz
%ghost %lang(nl) %{_mandir}/nl/man1/fakeroot.1.gz

%files libs
%dir %{_libdir}/libfakeroot
%{_libdir}/libfakeroot/libfakeroot-sysv.so
%{_libdir}/libfakeroot/libfakeroot-tcp.so
%ghost %{_libdir}/libfakeroot/libfakeroot-0.so

%changelog
* Thu Jun 18 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.20.2-1
- update to 1.20.2
- alternativize libfakeroot and faked as well (bug 817088)
- include Portugese manpages
- add missing BR: libcap-devel
- autogenerate most of the file list

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.18.4-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.18.4-2
- Add alternatives (Mimic Debian's behavior).

* Fri Jul 26 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.18.4-1
- Upstream update.
- Spec cleanup.
- Add fakeroot-1.18.4-inttypes.patch.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.4-2
- Strip libfakeroot-*.so (RHBZ#596735).
- Verified that libguestfs still builds and runs with this change (this
  represents a fairly aggressive test of fakeroot).

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.4-1
- Upstream removed the tarball for 1.12.2, which made Source0 invalid.
- There is a new version (1.12.4), so update to the new version.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.12.2-21
- Update to 1.12.2.
- Create a fakeroot-libs subpackage so that the package is multilib
  aware (by Richard W.M. Jones <rjones@redhat.com>, see RH bug
  #490953).

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.12.1-20
- Update to 1.12.1.

* Sat Nov 22 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.11-19
- Update to 1.11.

* Fri Oct  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.7-18
- Update to 1.9.7.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.6-17
- %%check || : does not work anymore.

* Sun Aug  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.6-16
- Update to 1.9.6.

* Thu Mar  8 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.6.4-15
- Update to 1.6.4.

* Wed Jan 10 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.12-14
- Update to 1.5.12.

* Sun Jan  7 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-13
- po4a currently not need as a BR.
- remove empty README, add debian/changelog.

* Sun Dec 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-12
- Add %%{_libdir}/libfakeroot to %%files.
- Add %%check.

* Fri Dec 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-11
- Extend the %%description a bit.

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-10
- Don't build static lib.
- Exclude libtool lib.
- %%makeinstall to make install DESTDIR=%%buildroot.

* Mon Aug  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-9
- Update to 1.5.10.

* Fri Feb 17 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.7.

* Thu Nov 24 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.5.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.1.

* Fri Sep  2 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.4.3.

* Sun Jul  3 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.4.1.

* Sun Feb  6 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.4.

* Sun Jan 25 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.8.3.

* Wed Oct  8 2003 Axel Thimm <Axel.Thimm@ATrpms.net> 
- Initial build.