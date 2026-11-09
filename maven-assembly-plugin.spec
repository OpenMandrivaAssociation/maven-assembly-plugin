Name:		maven-assembly-plugin
Version:	3.8.0
Release:	1
Summary:	Builds archives from assembly descriptors
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/plugins/maven-assembly-plugin/
Source0:	https://github.com/apache/maven-assembly-plugin/archive/refs/tags/maven-assembly-plugin-%{version}.tar.gz#/maven-assembly-plugin-%{version}.tar.gz
# Modello is not packaged. This jar holds the generated model sources.
Source1:	https://repo1.maven.org/maven2/org/apache/maven/plugins/maven-assembly-plugin/%{version}/maven-assembly-plugin-%{version}-sources.jar
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
# Generates META-INF/maven/plugin.xml. The separate annotations package
# conflicts with maven-components on the same index file.
BuildRequires:	maven-plugin-tools
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	apache-commons-io >= 1:2.22.0
Requires:	apache-commons-io >= 1:2.22.0
BuildRequires:	mvn(org.apache.maven:maven-archiver)
BuildRequires:	maven-archiver >= 3.6.6
Requires:	maven-archiver >= 3.6.6
BuildRequires:	mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:	maven-common-artifact-filters >= 3.4.0-2
Requires:	maven-common-artifact-filters >= 3.4.0-2
BuildRequires:	mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:	plexus-interpolation >= 1.30.0
Requires:	plexus-interpolation >= 1.30.0
BuildRequires:	mvn(org.apache.maven.shared:maven-filtering)
BuildRequires:	maven-filtering >= 3.5.1
Requires:	maven-filtering >= 3.5.1
BuildRequires:	mvn(org.codehaus.plexus:plexus-io)
BuildRequires:	plexus-io >= 3.8.1
Requires:	plexus-io >= 3.8.1
BuildRequires:	mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:	plexus-archiver >= 4.15.0
Requires:	plexus-archiver >= 4.15.0
BuildRequires:	mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(org.apache.maven:maven-model-builder)
BuildRequires:	mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven2-plugin-assembly <= 0:2.0.8
Provides:	maven2-plugin-assembly = %{EVRD}
Obsoletes:	maven-assembly-plugin-javadoc < %{EVRD}

%description
Builds archives from assembly descriptors, including the built-in
bin, src, and jar-with-dependencies formats. 3.8.0 copies manifest
entries from the archive configuration into the final manifest and
validates the model at the minimum level. Modello is not packaged,
so the model classes come from the upstream sources jar. Tests need
JUnit Jupiter, so they are not run.

%prep
%autosetup -n maven-assembly-plugin-maven-assembly-plugin-%{version}
rm -rf src/test src/it .github src/main/mdo
python - %{SOURCE1} <<'PY'
import sys
import zipfile
from pathlib import Path
z = zipfile.ZipFile(sys.argv[1])
root = Path("src/main/java")
for name in z.namelist():
    if name == "META-INF/NOTICE":
        Path("NOTICE").write_bytes(z.read(name))
        continue
    if not name.endswith(".java") or "/assembly/model/" not in name:
        continue
    if name.endswith("/Assemblies.java"):
        continue
    dest = root / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(z.read(name))
PY
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.plugins")
add(root, "artifactId", "maven-assembly-plugin")
add(root, "version", "%{version}")
add(root, "packaging", "maven-plugin")
add(root, "name", "Apache Maven Assembly Plugin")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
items = (
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", None),
    ("commons-io", "commons-io", "2.22.0", None),
    ("org.apache.maven", "maven-archiver", "3.6.6", None),
    ("org.apache.maven.shared", "maven-common-artifact-filters", "3.4.0", None),
    ("org.codehaus.plexus", "plexus-interpolation", "1.30.0", None),
    ("org.apache.maven.shared", "maven-filtering", "3.5.1", None),
    ("org.codehaus.plexus", "plexus-io", "3.8.1", None),
    ("org.codehaus.plexus", "plexus-archiver", "4.15.0", None),
    ("org.apache.maven.resolver", "maven-resolver-util", "2.0.24", None),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-artifact", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model-builder", "3.10.0", "provided"),
    ("org.apache.maven.resolver", "maven-resolver-api", "2.0.24", "provided"),
    ("org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3", "provided"),
    ("javax.inject", "javax.inject", "1", "provided"),
    ("org.slf4j", "slf4j-api", "1.7.36", "provided"),
    ("org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided"),
)
for group, artifact, version, scope in items:
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
build = ET.SubElement(root, tag("build"))
plugins = ET.SubElement(build, tag("plugins"))
plugin = ET.SubElement(plugins, tag("plugin"))
add(plugin, "groupId", "org.apache.maven.plugins")
add(plugin, "artifactId", "maven-plugin-plugin")
# The lifecycle binding asks for 3.15.1. The packaged plugin is 3.16.0.
add(plugin, "version", "3.16.0")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
# Sisu loads @Named classes from this index. The indexer plugin is not packaged.
python - <<'PY'
import re
from pathlib import Path
root = Path("src/main/java")
names = []
for path in sorted(root.rglob("*.java")):
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*?$", "", text, flags=re.M)
    match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
    if not match:
        continue
    if "@Named" not in text[:match.start()]:
        continue
    pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
    if not pkg:
        continue
    names.append(pkg.group(1) + "." + match.group(1))
if names:
    dest = Path("src/main/resources/META-INF/sisu")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY

%files -f .mfiles
%doc LICENSE NOTICE README.md
