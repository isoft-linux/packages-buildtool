Name: isoft-update-server
Version: 1.0
Release: 2
Summary: 普华操作系统更新包发布工具（服务器端）。
Vendor:  isoft

License: GPL
#URL:
Source0: isoft-update-server-1.0.tar.gz

#BuildRequires:
BuildRequires:  libxml2-devel >= 2.9
BuildRequires:  libtar-devel >= 1.2
buildRequires:  xz-devel >= 5.2

%description
普华操作系统更新包发布工具，应用在服务器端，可对更新包进行打包/校验/合并等操作。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
mv %{buildroot}/usr/bin/isoft_update_server %{buildroot}/usr/bin/%{name}
mkdir -p %{buildroot}/usr/share/%{name}
cp %{_builddir}/%{name}-%{version}/doc/update.xsd %{buildroot}/usr/share/%{name}

%files
/usr/bin/isoft-update-server
%doc
/usr/share/isoft-update-server/update.xsd

%changelog
* Tue Dec 29 2015 sulit <sulitsrc@gmail.com> - 1.0-2
- Init for isoft4
- It's from James(Jian Feng)
