Name:		PyGreSQL
Version:	4.1.1
Release:	7
Summary:	A Python client library for PostgreSQL

URL:		http://www.pygresql.org/
# Author states his intention is to dual license under PostgreSQL or Python
# licenses --- this is not too clear from the current tarball documentation,
# but hopefully will be clearer in future releases.
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License:	PostgreSQL or Python

Source0:	http://www.pygresql.org/files/PyGreSQL-%{version}.tgz

# PyGreSQL was originally shipped as a sub-RPM of the PostgreSQL package;
# these Provides/Obsoletes give a migration path.  Note there is no
# intention of changing the version numbers in future.
Provides:	postgresql-python = 8.5.0-1
Obsoletes:	postgresql-python < 8.5

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	postgresql-devel python-devel

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
PostgreSQL is an advanced Object-Relational database management system.
The PyGreSQL package provides a module for developers to use when writing
Python code for accessing a PostgreSQL database.

%prep
%setup -q 

# Some versions of PyGreSQL.tgz contain wrong file permissions
chmod 755 tutorial
chmod 644 tutorial/*.py

%build

CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc docs/*.txt
%doc tutorial
%{python_sitearch}/*.so
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%{python_sitearch}/*.egg-info

%changelog
* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 4.1.1-7
- Rebuild for new 4.0 release

* Mon Sep 21 2015 sulit <sulitsrc@gmail.com> - 4.1.1-6
- Initial packaging for new release

