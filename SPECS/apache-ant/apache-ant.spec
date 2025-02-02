%define hamcrest_ver 2.2
%define maven_tasks_ver 2.1.3

Summary:    Apache Ant
Name:       apache-ant
Version:    1.10.12
Release:    1%{?dist}
License:    Apache
URL:        http://ant.apache.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://apache.mirrors.lucidnetworks.net/ant/source/%{name}-%{version}-src.tar.gz
%define sha512  %{name}=1cfd31f9b19475bd94bcf59722cfc7aade58a5bb2a4f0cd6f3b90682ac6ef4cda3596269b4a91e09f2afd1be9123d4ef80db9f3c481dc34d8685b6e020a8ba11
Source1:    https://repo1.maven.org/maven2/org/hamcrest/hamcrest/%{hamcrest_ver}/hamcrest-%{hamcrest_ver}.jar
%define sha512  hamcrest=6b1141329b83224f69f074cb913dbff6921d6b8693ede8d2599acb626481255dae63de42eb123cbd5f59a261ac32faae012be64e8e90406ae9215543fbca5546
Source2:    https://packages.vmware.com/photon/photon_sources/1.0/maven-ant-tasks-%{maven_tasks_ver}.tar.gz
%define sha512  maven-ant-tasks=4df5b96a11819f82732c54656db8b0e0f4697079113d644622b4f82dc218ac1829b97aa8dc2427d3903ebdb0eb82e2ee35f9d3160647edb09bb243d8ba266fd8

Requires:      openjdk11

BuildRequires: openjdk11

BuildArch:      noarch

%define ant_prefix /var/opt/%{name}
%define ant_bindir %{ant_prefix}/bin
%define ant_libdir %{ant_prefix}/lib

%description
The Ant package contains binaries for a build system

%package -n ant-scripts
Summary:        Additional scripts for ant
Requires:       %{name} = %{version}
Requires:       python3

%description -n ant-scripts
Apache Ant is a Java-based build tool.
This package contains additional perl and python scripts for Apache Ant.

%prep
# Using autosetup is not feasible
%setup -q -T -D -b0 -a2

%build

%install
ANT_DIST_DIR=%{buildroot}%{ant_prefix}
cp %{SOURCE1} ./lib/optional
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)
mkdir -p -m 700 ${ANT_DIST_DIR}
./bootstrap.sh && ./build.sh -Ddist.dir=${ANT_DIST_DIR}

cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-%{maven_tasks_ver}/maven-ant-tasks-%{maven_tasks_ver}.jar %{buildroot}%{ant_libdir}

mkdir -p %{buildroot}%{_datadir}/java/ant %{buildroot}%{_bindir}

for jar in %{buildroot}%{ant_libdir}/*.jar; do
  jarname=$(basename $jar .jar)
  ln -sfv %{ant_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/ant/${jarname}.jar
done

rm -f %{buildroot}%{ant_bindir}/*.bat \
      %{buildroot}%{ant_bindir}/*.cmd

for b in %{buildroot}%{ant_bindir}/*; do
  binaryname=$(basename $b)
  ln -sfv %{ant_bindir}/${binaryname} %{buildroot}%{_bindir}/${binaryname}
done

MAVEN_ANT_TASKS_DIR=%{buildroot}%{ant_prefix}/maven-ant-tasks

mkdir -p -m 700 ${MAVEN_ANT_TASKS_DIR}

cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-%{maven_tasks_ver}/LICENSE \
   %{_builddir}/%{name}-%{version}/maven-ant-tasks-%{maven_tasks_ver}/NOTICE \
   %{_builddir}/%{name}-%{version}/maven-ant-tasks-%{maven_tasks_ver}/README.txt \
   ${MAVEN_ANT_TASKS_DIR}

chown -R root:root ${MAVEN_ANT_TASKS_DIR}
chmod 644 ${MAVEN_ANT_TASKS_DIR}/*

%if 0%{?with_check}
%check
# Disable following tests which are currently failing in chrooted environment -
#   - org.apache.tools.ant.types.selectors.OwnedBySelectorTest
#   - org.apache.tools.ant.types.selectors.PosixGroupSelectorTest
#   - org.apache.tools.mail.MailMessageTest
#   - org.apache.tools.ant.AntClassLoaderTest
#   - org.apache.tools.ant.taskdefs.optional.XsltTest
if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
  rm -f src/tests/junit/org/apache/tools/ant/types/selectors/OwnedBySelectorTest.java \
        src/tests/junit/org/apache/tools/ant/types/selectors/PosixGroupSelectorTest.java \
        src/tests/junit/org/apache/tools/mail/MailMessageTest.java \
        src/tests/junit/org/apache/tools/ant/AntClassLoaderTest.java \
        src/tests/junit/org/apache/tools/ant/taskdefs/optional/XsltTest.java
fi

export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)
bootstrap/bin/ant -v run-tests
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{ant_bindir}
%dir %{ant_libdir}
%dir %{_datadir}/java/ant
%dir %{ant_prefix}/maven-ant-tasks
%{_bindir}/ant
%{_bindir}/antRun
%{ant_bindir}/ant
%{ant_bindir}/antRun
%{ant_libdir}/*
%{_datadir}/java/ant/*.jar
%{ant_prefix}/maven-ant-tasks/LICENSE
%{ant_prefix}/maven-ant-tasks/README.txt
%{ant_prefix}/maven-ant-tasks/NOTICE

%files -n ant-scripts
%defattr(-,root,root)
%{_bindir}/antRun.pl
%{_bindir}/complete-ant-cmd.pl
%{_bindir}/runant.py
%{_bindir}/runant.pl
%{ant_bindir}/antRun.pl
%{ant_bindir}/complete-ant-cmd.pl
%{ant_bindir}/runant.py
%{ant_bindir}/runant.pl

%changelog
* Mon Nov 07 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.10.12-1
- Bump to version 1.10.12
- Update hamcrest to latest version
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.10.11-3
- Use openjdk11
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.11-2
- Fix binary path
* Tue Jul 20 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.11-1
- Bump to version 1.10.11 to fix CVE CVE-2021-36373, CVE-2021-36374
* Tue Jun 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.10-1
- Bump to version 1.10.10
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.10.8-3
- Fix build with new rpm
* Thu Nov 12 2020 Michelle Wang <michellew@vmware.com> 1.10.8-2
- Update Source0 with using https://packages.vmware.com/photon
* Mon Jul 27 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.8-1
- Bump to version 1.10.8
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.10.5-5
- Require python3
* Wed Sep 11 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.5-4
- Fix Make check
* Tue Dec 04 2018 Dweep Advani <dadvani@vmware.com> 1.10.5-3
- Adding MakeCheck tests
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.10.5-2
- Removed dependency on JAVA8_VERSION macro
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 1.10.5-1
- Updated Apache Ant to 1.10.5
* Wed Jun 28 2017 Kumar Kaushik <kaushikk@vmware.com> 1.10.1-5
- Base package does not require python2.
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.10.1-4
- Removed dependency on ANT_HOME
- Moved perl and python scripts to ant-scripts package
* Mon Jun 05 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-3
- Fixed the profile.d/apache-ant.sh script to include ant in $PATH
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-2
- Renamed openjdk to openjdk8
* Mon Apr 17 2017 Chang Lee <changlee@vmware.com> 1.10.1-1
- Updated Apache Ant to 1.10.1
* Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-6
- use java rpm macros to determine versions
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-5
- Updated JAVA_HOME path to point to latest JDK.
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-4
- Updated JAVA_HOME path to point to latest JDK.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-3
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.9.6-2
- Updated JAVA_HOME path to point to latest JDK.
* Mon Feb 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-1
- Updated to version 1.9.6
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.9.4-4
- Updated JAVA_HOME path to point to latest JDK.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.9.4-3
- Changed path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-2
- Updated dependencies after repackaging openjdk.
* Wed Aug 12 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
- Added maven ant tasks
* Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
- Initial build. First version
