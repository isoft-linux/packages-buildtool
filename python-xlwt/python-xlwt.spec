Name:           python-xlwt
Version:        0.7.4
Release:        6%{?dist}
Summary:        Spreadsheet python library

Group:          Development/Libraries
                # Utils.py is LPGL2.0+
License:        LGPLv2+ and BSD and BSD with advertising
URL:            http://pypi.python.org/pypi/xlwt
                # See also https://github.com/python-excel/xlwt
Source0:        http://pypi.python.org/packages/source/x/xlwt/xlwt-%{version}.tar.gz
                # https://github.com/python-excel/xlwt/issues/5
Patch0:         xlwt-fsf-address.patch
                # https://github.com/python-excel/xlwt/issues/4
Patch1:         xlwt-unbundle-antlr.patch
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python


%description
A library for generating spreadsheet files that are compatible with
Excel 97/2000/XP/2003, OpenOffice.org Calc, and Gnumeric. xlwt has
full support for Unicode. Excel spreadsheets can be generated on any
platform without needing Excel or a COM server. The only requirement
is Python 2.3 to 2.7.


%prep
%setup -q -n xlwt-%{version}
%patch0 -p1
#%patch1 -p1
sed -i '\;/usr/bin/env;d' xlwt/Formatting.py
iconv --from=ISO-8859-1 --to=UTF-8 licences.py > f.new && \
    touch -r licences.py f.new &&  mv f.new licences.py


%build
%{__python} setup.py --quiet build


%check
export PYTHONPATH=$(pwd)
%{__python} tests/RKbug.py 0
%{__python} tests/RKbug.py 1


%install
%{__python} setup.py --quiet install -O1 --skip-build --root %{buildroot}
mkdir tmp_docs
mv %{buildroot}%{python_sitelib}/xlwt/examples tmp_docs
mv %{buildroot}%{python_sitelib}/xlwt/doc tmp_docs


%files
%doc PKG-INFO README.html tmp_docs/* licences.py
%{python_sitelib}/xlwt
%{python_sitelib}/*.egg-info


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
