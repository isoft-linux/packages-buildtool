Name:           mailcap
Version:        2.1.44
Release:        3
Summary:        Helper application and MIME type associations for file types

Group:          System Environment/Base
License:        Public Domain and MIT
URL:            http://git.fedorahosted.org/git/mailcap.git
Source0:        https://fedorahosted.org/released/mailcap/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
The mailcap file is used by the metamail program.  Metamail reads the
mailcap file to determine how it should display non-text or multimedia
material.  Basically, mailcap associates a particular type of file
with a particular program that a mail agent or other program can call
in order to handle the file.  Mailcap should be installed to allow
certain programs to be able to handle non-text files.

Also included in this package is the mime.types file which contains a
list of MIME types and their filename "extension" associations, used
by several applications e.g. to determine MIME types for filenames.


%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT sysconfdir=%{_sysconfdir} mandir=%{_mandir}


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS
%config(noreplace) %{_sysconfdir}/mailcap
%config(noreplace) %{_sysconfdir}/mime.types
%{_mandir}/man4/mailcap.*


%changelog
* Mon Sep 21 2015 sulit <sulitsrc@gmail.com> - 2.1.44-3
- Initial packaging for new release

