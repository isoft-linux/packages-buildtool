%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Summary: Kerberos authentication module for HTTP
Name: mod_auth_kerb
Version: 5.4
Release: 33
# src/mod_auth_kerb.c is under 3-clause BSD, ASL 2.0 code is patched in (-s4u2proxy.patch)
# src/mit-internals.h contains MIT-licensed code.
License: BSD and MIT and ASL 2.0
URL: http://modauthkerb.sourceforge.net/
Source0: http://downloads.sourceforge.net/modauthkerb/%{name}-%{version}.tar.gz
Source1: auth_kerb.conf
Source2: LICENSE.ASL
Patch1: mod_auth_kerb-5.4-rcopshack.patch
Patch2: mod_auth_kerb-5.4-fixes.patch
Patch3: mod_auth_kerb-5.4-s4u2proxy.patch
Patch4: mod_auth_kerb-5.4-httpd24.patch
Patch5: mod_auth_kerb-5.4-delegation.patch
Patch6: mod_auth_kerb-5.4-cachedir.patch
Patch7: mod_auth_kerb-5.4-longuser.patch
Patch8: mod_auth_kerb-5.4-handle-continue.patch
BuildRequires: httpd-devel, krb5-devel
Requires: httpd-mmn = %{_httpd_mmn}
Requires(pre): httpd

# Suppres auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
mod_auth_kerb is module for the Apache HTTP Server designed to
provide Kerberos authentication over HTTP.  The module supports the
Negotiate authentication method, which performs full Kerberos
authentication based on ticket exchanges.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .rcopshack
%patch2 -p1 -b .fixes
%patch3 -p1 -b .s4u2proxy
%patch4 -p1 -b .httpd24
%patch5 -p1 -b .delegation
%patch6 -p1 -b .cachedir
%patch7 -p1 -b .longuser
%patch8 -p1 -b .continue

%build
export APXS=%{_httpd_apxs}
%configure --without-krb4 --with-krb5=%{_prefix}
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 755 src/.libs/mod_auth_kerb.so \
        $RPM_BUILD_ROOT%{_httpd_moddir}/mod_auth_kerb.so

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
sed -n /^LoadModule/p %{SOURCE1} > 10-auth_kerb.conf
sed '/LoadModule/d;/Location /,/Location>/s,^#,,' %{SOURCE1} > example.conf
install -Dp -m 0644 10-auth_kerb.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-auth_kerb.conf
%else
# httpd <= 2.2.x
install -Dp -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/auth_kerb.conf
%endif

# Credentials cache
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
echo 'd /run/httpd/krbcache 700 apache apache' \
     > $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd-krbcache.conf
mkdir -p $RPM_BUILD_ROOT/run/httpd/krbcache

# Copy the license files here so we can include them in %doc
cp -p %{SOURCE2} .

%files
%doc README LICENSE LICENSE.ASL
%config(noreplace) %{_httpd_modconfdir}/*.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%doc example.conf
%endif
%{_httpd_moddir}/*.so
%{_prefix}/lib/tmpfiles.d/httpd-krbcache.conf
%attr(0700,apache,apache) %dir /run/httpd/krbcache

%changelog
* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 5.4-33
- Rebuild for new 4.0 release

* Mon Sep 21 2015 sulit <sulitsrc@gmail.com> - 5.4-33
- Initial packaging for new release

