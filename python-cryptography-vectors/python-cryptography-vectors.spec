#%if 0%{?isoft} > 3
%if 0
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global modname cryptography-vectors
%global pymodname cryptography_vectors

Name:               python-%{modname}
Version:            0.8.2
Release:            1%{?dist}
Summary:            Test vectors for the cryptography package

Group:              Development/Libraries
License:            ASL 2.0 or BSD
URL:                http://pypi.python.org/pypi/cryptography-vectors
Source0:            https://pypi.python.org/packages/source/c/%{modname}/cryptography_vectors-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:      python3-devel python3-setuptools
%endif

%description
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.

%if 0%{?with_python3}
%package -n  python3-%{modname}
Group:          Development/Libraries
Summary:        Test vectors for the cryptography package

%description -n python3-%{modname}
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.
%endif

%prep
%setup -q -n %{pymodname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
%if 0%{?with_python3}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files
%doc LICENSE
%{python2_sitelib}/%{pymodname}/
%{python2_sitelib}/%{pymodname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%doc LICENSE
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}*
%endif


%changelog
* Fri Apr 17 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8.2-1
- init
