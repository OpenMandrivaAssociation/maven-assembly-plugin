Name:           maven-assembly-plugin
Version:        2.2
Release:        5
Summary:        Maven Assembly Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-assembly-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-jpp-depmap.xml

BuildArch: noarch

Obsoletes: maven2-plugin-assembly <= 0:2.0.8
Provides:  maven2-plugin-assembly = 1:%{version}-%{release}

BuildRequires: java >= 0:1.6.0
BuildRequires: jpackage-utils >= 0:1.7.2
BuildRequires:  ant, ant-nodeps
BuildRequires:  maven2 >= 0:2.0.4-9
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-shared-filtering
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools

BuildRequires: plexus-container-default
BuildRequires: plexus-utils
BuildRequires: plexus-active-collections
BuildRequires: plexus-maven-plugin
BuildRequires: plexus-io
BuildRequires: plexus-interpolation
BuildRequires: plexus-archiver

BuildRequires: maven-shared-file-management
BuildRequires: maven-shared-repository-builder
BuildRequires: maven-shared-filtering

BuildRequires: easymock2
BuildRequires: jdom
BuildRequires: jaxen
BuildRequires: saxpath
BuildRequires: junit

Requires: java >= 0:1.6.0
Requires: easymock2
Requires: jdom
Requires: jaxen
Requires: saxpath
Requires: plexus-container-default
Requires: plexus-utils
Requires: plexus-active-collections
Requires: plexus-maven-plugin
Requires: plexus-io
Requires: plexus-interpolation
Requires: plexus-archiver
Requires: maven-shared-repository-builder
Requires: maven-shared-filtering

Requires:          jpackage-utils >= 0:1.7.2
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
A Maven 2 plugin to create archives of your project's sources, classes, 
dependencies etc. from flexible assembly descriptors.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:          jpackage-utils >= 0:1.7.2

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
mkdir -p target/classes/
cp -pr src/main/resources/META-INF/ target/classes/

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
# seems koji don't have easymockclassextension
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file=%{SOURCE1} \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap org.apache.maven.plugins maven-assembly-plugin %{version} JPP maven-assembly-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

