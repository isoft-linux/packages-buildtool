%if 1
%global with_python3 1
%endif

%define srcname Markdown

Name:           python-markdown
Version:        2.6.2
Release:        2
Summary:        Markdown implementation in Python
Group:          Development/Languages
License:        BSD
URL:            https://pythonhosted.org/%{srcname}/
Source0:        http://pypi.python.org/packages/source/M/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel >= 2.6
BuildRequires:  python-nose
BuildRequires:  PyYAML
%if 0%{?with_python3}
BuildRequires:  python3-devel >= 3.1
BuildRequires:  python3-nose
BuildRequires:  python3-PyYAML
%endif # with_python3
Requires:       python2 >= 2.6


%description
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.


%if 0%{?with_python3}
%package -n python3-markdown
Summary:        Markdown implementation in Python
Group:          Development/Languages
Requires:       python3 >= 3.1


%description -n python3-markdown
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.
%endif # with_python3


%prep
%setup -qc -n %{srcname}-%{version}

pushd %{srcname}-%{version}

# remove shebangs
find markdown -type f -name '*.py' \
  -exec sed -i -e '/^#!/{1D}' {} \;

# fix line-ending
find bin docs -type f \
  -exec sed -i 's/\r//' {} \;

popd

mv %{srcname}-%{version} python2
%if 0%{?with_python3}
cp -a python2 python3
%endif # with_python3


%build
pushd python2
%{__python2} setup.py build
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with_python3


%install
pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# rename binary
mv %{buildroot}%{_bindir}/markdown_py{,-%{python2_version}}

# process license file
PYTHONPATH=%{buildroot}%{python2_sitelib} \
  %{buildroot}%{_bindir}/markdown_py-%{python2_version} \
  LICENSE.md > LICENSE.html
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# rename binary
mv %{buildroot}%{_bindir}/markdown_py{,-%{python3_version}}

# process license file
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/markdown_py-%{python3_version} \
  LICENSE.md > LICENSE.html
popd
%endif # with_python3

# 2.X binary is called by default for now
ln -s markdown_py-%{python2_version} %{buildroot}%{_bindir}/markdown_py


%check
pushd python2
%{__python2} run-tests.py
popd

%if 0%{?with_python3}
pushd python3
%{__python3} run-tests.py
popd
%endif # with_python3


%files
%doc python2/build/docs/*
%license python2/LICENSE.*
%{python2_sitelib}/*
%{_bindir}/markdown_py
%{_bindir}/markdown_py-%{python2_version}


%if 0%{?with_python3}
%files -n python3-markdown
%doc python3/build/docs/*
%license python3/LICENSE.*
%{python3_sitelib}/*
%{_bindir}/markdown_py-%{python3_version}
%endif # with_python3


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.2-1
- Update to 2.6.2.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-2
- Add license file.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-1
- Update to 2.6.1.
- Apply updated Python packaging guidelines.

* Sun Feb 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6-1
- Update to 2.6.
- Update the upstream URL.

* Sun Nov 23 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to 2.5.2.

* Thu Oct  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.1-1
- Update to 2.5.1.

* Thu Sep 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5-1
- Update to 2.5.
- Add BR on PyYAML.

* Wed Jun  4 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.1-1
- Update to 2.4.1.

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 15 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.4-1
- Update to 2.4.
- Update Python3 conditional.
- Fix wrong line endings.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Thomas Moschny <thomas.moschny@gmx.dee> - 2.3.1-2
- Move python3 runtime dependency to python3 subpackage (rhbz#986376).

* Mon Apr  8 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.

* Mon Mar 18 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3-1
- Update to 2.3.
- Spec file cleanups.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.
- Update url.
- Add patch from upstream git for failing test.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.
- Fix rhel conditional.
- Binary has been renamed.
- Build python3 subpackage.
- Include documentation in HTML instead of Markdown format.
- Run tests.

* Wed Sep 07 2011 Jesse Keating <jkeating@redhat.com> - 2.0.3-4
- Set a version in the rhel macro

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Oct  8 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-3
- Add requirement on python-elementtree, which was a separate package
  before Python 2.5.
- Re-add changelog entries accidentally removed earlier.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-1
- Update to 2.0.1.
- Upstream stripped .py of the cmdline script.

* Sat Apr 25 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-1
- Update to 2.0.
- Adjusted source URL.
- License changed to BSD only.
- Upstream now provides a script to run markdown from the cmdline.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7-2
- Rebuild for Python 2.6

* Mon Aug  4 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.7-1
- New package.
