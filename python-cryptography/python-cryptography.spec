#%if 0%{?isoft} > 3
%if 0
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-cryptography
Version:        0.8.2
Release:        1%{?dist}
Summary:        PyCA's cryptography library

Group:          Development/Libraries
License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz

BuildRequires:  openssl-devel
BuildRequires:  python-enum34

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi >= 0.8
BuildRequires:  python-six
BuildRequires:  python-cryptography-vectors = %{version}
BuildRequires:  python-pyasn1
BuildRequires:  python-iso8601
BuildRequires:  python-pretend
BuildRequires:  pytest

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi >= 0.8
BuildRequires:  python3-six
BuildRequires:  python3-cryptography-vectors = %{version}
BuildRequires:  python3-pyasn1
BuildRequires:  python3-iso8601
BuildRequires:  python3-pretend
BuildRequires:  python3-pytest
%endif

Requires:       openssl
Requires:       python-enum34
Requires:       python-cffi >= 0.8
Requires:       python-six >= 1.6.1
Requires:       python-pyasn1

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python3}
%package -n  python3-cryptography
Group:          Development/Libraries
Summary:        PyCA's cryptography library

Requires:       openssl
Requires:       python3-cffi >= 0.8
Requires:       python3-six >= 1.6.1
Requires:       python3-pyasn1

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
%setup -q -n cryptography-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete

%{__python2} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
popd
%endif


%check
%if 0%{?fedora} > 20
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif
%endif


%files
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python_sitearch}/*


%if 0%{?with_python3}
%files -n python3-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python3_sitearch}/*
%endif


%changelog
* Fri Apr 17 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8.2-1
- init
