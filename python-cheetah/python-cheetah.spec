Name:           python-cheetah
Version:        2.4.4
Release:        12
Summary:        Template engine and code generator

Group:          Development/Libraries
License:        MIT
URL:            http://cheetahtemplate.org/
Source:         http://pypi.python.org/packages/source/C/Cheetah/Cheetah-%{version}.tar.gz

Patch0:         cheetah-2.4.4-dont-run-tests-twice.patch
Patch1:         cheetah-optional-deps.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: python
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: python-markdown
BuildRequires: python-pygments

%description
Cheetah is an open source template engine and code generation tool,
written in Python. It can be used standalone or combined with other
tools and frameworks. Web development is its principal use, but
Cheetah is very flexible and is also being used to generate C++ code,
Java, SQL, form emails and even Python code.

%prep
%setup -q -n Cheetah-%{version}
%patch0 -p1
%patch1 -p1
# remove unnecessary shebang lines to silence rpmlint
%{__sed} -i -e '/^#!/,1d' cheetah/Tests/* \
	 cheetah/DirectiveAnalyzer.py cheetah/Utils/Misc.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
export PATH="%{buildroot}/%{_bindir}:$PATH"
export PYTHONPATH="%{buildroot}/%{python_sitearch}"
%{buildroot}/%{_bindir}/cheetah test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES README.markdown TODO

%{_bindir}/cheetah
%{_bindir}/cheetah-analyze
%{_bindir}/cheetah-compile

%dir %{python_sitearch}/Cheetah
%{python_sitearch}/Cheetah/*.py*
%{python_sitearch}/Cheetah/_namemapper.so

%dir %{python_sitearch}/Cheetah/Macros
%{python_sitearch}/Cheetah/Macros/*.py*

%dir %{python_sitearch}/Cheetah/Templates
%{python_sitearch}/Cheetah/Templates/*.py*
%{python_sitearch}/Cheetah/Templates/*.tmpl

%dir %{python_sitearch}/Cheetah/Tests
%{python_sitearch}/Cheetah/Tests/*.py*

%dir %{python_sitearch}/Cheetah/Tools
%{python_sitearch}/Cheetah/Tools/*.py*
%{python_sitearch}/Cheetah/Tools/*.txt

%dir %{python_sitearch}/Cheetah/Utils
%{python_sitearch}/Cheetah/Utils/*.py*

%dir %{python_sitearch}/Cheetah-%{version}-*.egg-info
%{python_sitearch}/Cheetah-%{version}-*.egg-info/PKG-INFO
%{python_sitearch}/Cheetah-%{version}-*.egg-info/*.txt

%changelog
* Mon Sep 21 2015 sulit <sulitsrc@gmail.com> - 2.4.4-12
- Initial packaging for new release

