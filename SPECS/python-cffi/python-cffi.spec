Summary:        Interface for Python to call C code
Name:           python3-cffi
Version:        1.15.1
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/cffi
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://pypi.python.org/packages/source/c/cffi/cffi-%{version}.tar.gz
%define sha512  cffi=e99cafcb029076abc29e435b490fa0573ee2856f4051b7ca8a5b38cd125d56dd9dae8b189f59ceb3d728a675da8ee83239e09e19f8b0feeddea4b186ab5173a5

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libffi-devel
BuildRequires:  python3-pycparser
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:	openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-pycparser

%description
Foreign Function Interface for Python, providing a convenient and reliable way of calling existing C code from Python. The interface is based on LuaJIT’s FFI.

%prep
%autosetup -p1 -n cffi-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.15.1-1
- Automatic Version Bump
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.3-3
- Bump version as a part of libffi upgrade
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.3-2
- openssl 1.1.1
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.3-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.11.5-5
- Mass removal python2
* Wed Feb 26 2020 Tapas Kundu <tkundu@vmware.com> 1.11.5-4
- Fixed make check errors.
* Thu Sep 05 2019 Shreyas B. <shreyasb@vmware.com> 1.11.5-3
- Fixed make check errors.
* Thu Nov 15 2018 Tapas Kundu <tkundu@vmware.com> 1.11.5-2
- Fixed make check errors.
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.11.5-1
- Update to version 1.11.5
* Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> 1.10.0-3
- Added build time dependecies required during check
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 1.10.0-1
- Update to 1.10.0
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.1-1
- Updated to version 1.9.1.
* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-4
- Added python3 site-packages.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.5.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.2-1
- Updated to version 1.5.2
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.5.0-1
- Upgrade version
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.0-1
- nitial packaging for Photon
