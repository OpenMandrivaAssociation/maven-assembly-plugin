%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-assembly-plugin
Version:        2.4.1
Release:        1.1
Group:		System/Libraries
Summary:        Maven Assembly Plugin
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-assembly-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.shared:file-management)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-filtering)
BuildRequires:  mvn(org.apache.maven.shared:maven-repository-builder)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-io)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:	mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-io)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

Provides:       maven2-plugin-assembly = 1:%{version}-%{release}
Obsoletes:      maven2-plugin-assembly <= 0:2.0.8

%description
A Maven plugin to create archives of your project's sources, classes,
dependencies etc. from flexible assembly descriptors.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q

%build
# Tests need easymockclassextension version 2.x, which is incompatible
# with easymockclassextension version 3.x we have in Fedora.
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4-6
- Build with xmvn
- Install license files
- Resolves: rhbz#915608

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Dec 13 2012 Tomas Radej <tradej@redhat.com> - 2.4-1
- Updated to latest upstream version.
- Fixed mail in changelog

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> - 2.3-3
- Migration to plexus-containers-container-default

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 07 2012 Tomas Radej <tradej@redhat.com> - 2.3-1
- Update to latest upstream vresion.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Tomas Radej <tradej@redhat.com> - 2.2.2-3
- Added R on plexus-containers-component-metadata

* Mon Dec 12 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-2
- Remove plexus-maven-plugin require.

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-1
- Update to latest upstream version.

* Sun Oct 2 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-4
- Add missing BR/R.

* Thu Jul 15 2011 Jaromir Capik <jcapik@redhat.com> 2.2.1-3
- modello removed from requires
- %update_maven_depmap removed

* Thu May 23 2011 Jaromir Capik <jcapik@redhat.com> 2.2.1-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Missing modello dependency added
- Minor spec file changes according to the latest guidelines

* Thu Mar 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to upstream 2.2.1 release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to final release.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-0.4.beta5
- Add missing BuildRequires.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-0.3.beta5
- Add missing Requires.

* Thu Jun 03 2010 Yong Yang <yyang@redhat.com> - 2.2-0.2.beta5
- Chmod 0644 for depmap.xml
- Fix Obsoletes and Provides
- Change to BR java

* Thu May 20 2010 Yong Yang <yyang@redhat.com> - 2.2-0.1.beta5
- Initial build
