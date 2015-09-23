
%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.5.4
Release: 4
License: ASL 2.0
Group: CoreDev/Runtime/Library
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
BuildRequires: autoconf, apr-devel >= 1.3.0
BuildRequires: libdb-devel, expat-devel, libuuid-devel, sqlite-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package devel
Group: CoreDev/Development/Library
Summary: APR utility library development kit
Requires: apr-util = %{version}-%{release}, apr-devel, pkgconfig
Requires: libdb-devel, expat-devel

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.

%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
BuildRequires: openldap-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description ldap
This package provides the LDAP support for the apr-util.

%prep
%setup -q

#        --without-ldap \
#	--with-ldap=ldap_r \
%build
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
	--enable-authnz-ldap \
	--enable-ldap \
	--with-ldap=ldap_r \
        --without-gdbm \
        --with-sqlite3 \
        --without-pgsql \
        --without-mysql \
        --without-freetds \
        --without-odbc \
        --with-berkeley-db \
        --without-sqlite2
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apu.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Unpackaged files; remove the static libaprutil
rm -f $RPM_BUILD_ROOT%{_libdir}/aprutil.exp \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.a

# And remove the reference to the static libaprutil from the .la
# file.
sed -i '/^old_library/s,libapr.*\.a,,' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Remove unnecessary exports from dependency_libs
sed -ri '/^dependency_libs/{s,-l(pq|sqlite[0-9]|rt|dl|uuid) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Trim libtool DSO cruft
rm -f $RPM_BUILD_ROOT%{_libdir}/apr-util-%{apuver}/*.*a
rpmclean

%check
# Run the less verbose test suites
export MALLOC_CHECK_=2 MALLOC_PERTURB_=$(($RANDOM % 255 + 1))
cd test
make %{?_smp_mflags} testall
# testall breaks with DBD DSO; ignore
export LD_LIBRARY_PATH="`echo "../dbm/.libs:../dbd/.libs:../ldap/.libs:$LD_LIBRARY_PATH" | sed -e 's/::*$//'`"
./testall -v -q || true
./testall testrmm
./testall testdbm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libaprutil-%{apuver}.so.*
%dir %{_libdir}/apr-util-%{apuver}
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*
%{_libdir}/apr-util-%{apuver}/apr_dbm_db*

%files devel
%defattr(-,root,root,-)
%{_bindir}/apu-%{apuver}-config
%{_libdir}/libaprutil-%{apuver}.so
%{_includedir}/apr-%{apuver}/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%files ldap
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_ldap*

%changelog
* Mon Sep 21 2015 sulit <sulitsrc@gmail.com>
- update to 1.5.4-4

* Tue Jul 14 2015 Cjacker <cjacker@foxmail.com>
- update to 1.5.4

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

