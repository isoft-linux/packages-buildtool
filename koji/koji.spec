%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name: koji
Version: 1.9.1
Release: 2
License: LGPLv2 and GPLv2+
# koji.ssl libs (from plague) are GPLv2+
Summary: Build system tools
Group: Applications/System
URL: https://fedorahosted.org/koji
Patch0: isoft-config.patch

Source: https://fedorahosted.org/released/koji/koji-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python-krbV >= 1.0.13
Requires: python-rpm
Requires: pyOpenSSL
Requires: python-urlgrabber
BuildRequires: python
BuildRequires: systemd
BuildRequires: pkgconfig

%description
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.

%package hub
Summary: Koji XMLRPC interface
Group: Applications/Internet
License: LGPLv2 and GPLv2
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: mod_wsgi
Requires: postgresql-python
Requires: %{name} = %{version}-%{release}

%description hub
koji-hub is the XMLRPC interface to the koji database

%package hub-plugins
Summary: Koji hub plugins
Group: Applications/Internet
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hub = %{version}-%{release}

%description hub-plugins
Plugins to the koji XMLRPC interface

%package builder
Summary: Koji RPM builder daemon
Group: Applications/System
License: LGPLv2 and GPLv2+
#mergerepos (from createrepo) is GPLv2+
Requires: %{name} = %{version}-%{release}
Requires: mock >= 0.9.14
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires(pre): /usr/sbin/useradd
Requires: /usr/bin/cvs
# Requires: /usr/bin/svn
Requires: /usr/bin/git
Requires: rpm-build
Requires: python-cheetah
Requires: createrepo >= 0.9.6
%if 0%{?rhel} == 5
Requires: python-createrepo >= 0.9.6
Requires: python-hashlib
Requires: createrepo
%endif

%description builder
koji-builder is the daemon that runs on build machines and executes
tasks that come through the Koji system.

#  %package vm
#  Summary: Koji virtual machine management daemon
#  Group: Applications/System
#  License: LGPLv2
#  Requires: %{name} = %{version}-%{release}
#  Requires(post): systemd
#  Requires(preun): systemd
#  Requires(postun): systemd
#  Requires: libvirt-python
#  Requires: libxml2-python
#  Requires: /usr/bin/virt-clone
#  Requires: qemu-img
#  
#  %description vm
#  koji-vm contains a supplemental build daemon that executes certain tasks in a
#  virtual machine. This package is not required for most installations.

%package utils
Summary: Koji Utilities
Group: Applications/Internet
Requires: postgresql-python
Requires: %{name} = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description utils
Utilities for the Koji system

%package web
Summary: Koji Web UI
Group: Applications/Internet
Requires: httpd
Requires: mod_wsgi
Requires: mod_auth_kerb
Requires: postgresql-python
Requires: python-cheetah
Requires: %{name} = %{version}-%{release}
Requires: python-krbV >= 1.0.13

%description web
koji-web is a web UI to the Koji system.

%prep
%setup -q
%patch0 -p1 -b .orig

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/koji.conf
%dir %{_sysconfdir}/koji.conf.d
%doc docs Authors COPYING LGPL

%files hub
%defattr(-,root,root)
%{_datadir}/koji-hub
%dir %{_libexecdir}/koji-hub
%config(noreplace) %{_sysconfdir}/httpd/conf.d/kojihub.conf
%dir %{_sysconfdir}/koji-hub
%config(noreplace) %{_sysconfdir}/koji-hub/hub.conf
%dir %{_sysconfdir}/koji-hub/hub.conf.d

%files hub-plugins
%defattr(-,root,root)
%dir %{_prefix}/lib/koji-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py*
%dir %{_sysconfdir}/koji-hub/plugins/
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/messagebus.conf
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/rpm2maven.conf
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/runroot.conf

%files utils
%defattr(-,root,root)
%{_sbindir}/kojira
%{_sbindir}/koji-gc
%{_sbindir}/koji-shadow
%{_unitdir}/kojira.service
%dir %{_sysconfdir}/kojira
%config(noreplace) %{_sysconfdir}/kojira/kojira.conf
%dir %{_sysconfdir}/koji-gc
%config(noreplace) %{_sysconfdir}/koji-gc/koji-gc.conf
%config(noreplace) %{_sysconfdir}/koji-shadow/koji-shadow.conf

%files web
%defattr(-,root,root)
%{_datadir}/koji-web
%{_sysconfdir}/kojiweb
%config(noreplace) %{_sysconfdir}/httpd/conf.d/kojiweb.conf
%config(noreplace) %{_sysconfdir}/kojiweb/web.conf
%dir %{_sysconfdir}/kojiweb/web.conf.d

%files builder
%defattr(-,root,root)
%{_sbindir}/kojid
%{_libexecdir}/kojid/
%{_unitdir}/kojid.service
%dir %{_sysconfdir}/kojid
%config(noreplace) %{_sysconfdir}/kojid/kojid.conf
%attr(-,kojibuilder,kojibuilder) /etc/mock/koji

%pre builder
/usr/sbin/useradd -r -s /bin/bash -G mock -d /builddir -M kojibuilder 2>/dev/null ||:

%post builder
%systemd_post kojid.service

%preun builder
%systemd_preun kojid.service

%postun builder
%systemd_postun kojid.service

#   %files vm
#   %defattr(-,root,root)
#   %{_sbindir}/kojivmd
#   %{_datadir}/kojivmd
#   %{_unitdir}/kojivmd.service
#   %dir %{_sysconfdir}/kojivmd
#   %config(noreplace) %{_sysconfdir}/kojivmd/kojivmd.conf
#   
#   %post vm
#   %systemd_post kojivmd.service
#   
#   %preun vm
#   %systemd_preun kojivmd.service
#   
#   %postun vm
#   %systemd_postun kojivmd.service

%post utils
%systemd_post kojira.service

%preun utils
%systemd_preun kojira.service

%postun utils
%systemd_postun kojira.service

%changelog
* Fri Oct 23 2015 xiaotian.wu@i-soft.com.cn - 1.9.1-2
- rebuilt, just sync to koji server.

* Wed Sep 9 2015 sulit <sulitsrc@163.com> - 1.9.0-14
- Initial packaging for new release

