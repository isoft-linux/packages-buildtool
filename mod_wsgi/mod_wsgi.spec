%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

%global with_python3 1

Name:           mod_wsgi
Version:        4.4.8
Release:        5
Summary:        A WSGI interface for Python web applications in Apache
License:        ASL 2.0
URL:            http://modwsgi.org
Source0:        http://github.srcurl.net/GrahamDumpleton/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        wsgi.conf
Source2:        wsgi-python3.conf

BuildRequires:  httpd-devel, python-devel, autoconf
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif
Requires:       httpd-mmn = %{_httpd_mmn}

# Suppress auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}


%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        A WSGI interface for Python3 web applications in Apache
Requires:       httpd-mmn = %{_httpd_mmn}

%description -n python3-%{name}
The mod_wsgi adapter is an Apacheache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is writtentten completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.
%endif

%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -qn %{name}-%{version}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
export LDFLAGS="$RPM_LD_FLAGS -L%{_libdir}"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --enable-shared --with-apxs=%{_httpd_apxs}
make %{?_smp_mflags}

%if 0%{?with_python3}
pushd %{py3dir}
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=python3
make %{?_smp_mflags}
popd
%endif

%install
# first install python3 variant and rename the so file
%if 0%{?with_python3}
pushd %{py3dir}
make install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_httpd_moddir}
mv  $RPM_BUILD_ROOT%{_httpd_moddir}/mod_wsgi{,_python3}.so

install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_confdir}/wsgi-python3.conf
%else
# httpd >= 2.4.x
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi-python3.conf
%endif
popd
%endif

make install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_httpd_moddir}

install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/wsgi.conf
%else
# httpd >= 2.4.x
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi.conf
%endif

%files
%doc LICENSE README.rst
%config(noreplace) %{_httpd_modconfdir}/*wsgi.conf
%{_httpd_moddir}/mod_wsgi.so

%if 0%{?with_python3}
%files -n python3-%{name}
%doc LICENSE README.rst
%config(noreplace) %{_httpd_modconfdir}/*wsgi-python3.conf
%{_httpd_moddir}/mod_wsgi_python3.so
%endif

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 4.4.8-5
- Rebuild with python 3.5

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 4.4.8-4
- Rebuild for new 4.0 release

* Mon Sep 21 2015 sulit <sulitsrc@gmail.com> - 4.4.8-3
- Initial packaging for new release

