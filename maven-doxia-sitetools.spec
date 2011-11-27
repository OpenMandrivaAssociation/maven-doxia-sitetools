# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global parent maven-doxia
%global subproj sitetools

Name:           %{parent}-%{subproj}
Version:        1.1.3
Release:        5
Summary:        Doxia content generation framework
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/doxia/

#  svn export http://svn.apache.org/repos/asf/maven/doxia/doxia-sitetools/tags/doxia-sitetools-1.1.3/ \
#  maven-doxia-sitetools-1.1.3
# tar czf maven-doxia-sitetools-1.1.3.tar.gz maven-doxia-sitetools-1.1.3
Source0:        %{name}-%{version}.tar.gz

# Point it at the correct plexus-container-default
Source1:    maven-doxia-depmap.xml

Patch0:         %{name}-clirr.patch
Patch1:         %{name}-disablehtmlunit.patch

BuildRequires:  itext >= 2.1.7
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven2
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia
BuildRequires:  plexus-maven-plugin >= 0:1.2-2
BuildRequires:  modello-maven-plugin >= 0:1.0-0.a8.3
BuildRequires:  plexus-xmlrpc >= 0:1.0-0.b4.3
BuildRequires:  classworlds
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-configuration
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-validator
BuildRequires:  junit
BuildRequires:  jakarta-oro
BuildRequires:  plexus-container-default
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-containers-component-javadoc
BuildRequires:  plexus-i18n
BuildRequires:  plexus-utils >= 1.5.7
BuildRequires:  plexus-velocity
BuildRequires:  velocity

Requires:       classworlds
Requires:       apache-commons-collections
Requires:       apache-commons-configuration
Requires:       apache-commons-logging
Requires:       apache-commons-validator
Requires:       junit
Requires:       maven-doxia
Requires:       jakarta-oro
Requires:       plexus-container-default
Requires:       plexus-containers-container-default
Requires:       plexus-i18n
Requires:       plexus-utils >= 1.5.7
Requires:       plexus-velocity
Requires:       velocity

Requires:       java >= 0:1.6.0
Requires:       jpackage-utils >= 0:1.7.2
Requires(post):   jpackage-utils >= 0:1.7.2
Requires(postun): jpackage-utils >= 0:1.7.2

BuildArch:      noarch

%description
Doxia is a content generation framework which aims to provide its
users with powerful techniques for generating static and dynamic
content. Doxia can be used to generate static sites in addition to
being incorporated into dynamic content generation systems like blogs,
wikis and content management systems.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q

%patch0 -p1

# Disable tests that need htmlunit, until we get it in Fedora
%patch1 -p1
rm -rf doxia-site-renderer/src/test/java/org/apache/maven/doxia/siterenderer/

# use new taglet name
sed -i 's:plexus-javadoc:plexus-component-javadoc:' pom.xml

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
      -e \
      -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
      -Dmaven.test.failure.ignore=true \
      -Dmaven.test.skip=true \
      -Dmaven2.jpp.depmap.file=%{SOURCE1} \
      install javadoc:aggregate


%post
%update_maven_depmap

%postun
%update_maven_depmap

%install
rm -rf $RPM_BUILD_ROOT

# jars/poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

install -m 644 -p pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-sitetools.pom
install -m 644 -p doxia-decoration-model/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-decoration-model.pom
install -m 644 -p doxia-site-renderer/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-site-renderer.pom
install -m 644 -p doxia-doc-renderer/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-doc-renderer.pom

%add_to_maven_depmap org.apache.maven.doxia doxia-sitetools %{version} JPP/%{parent} sitetools
%add_to_maven_depmap org.apache.maven.doxia doxia-decoration-model %{version} JPP/%{parent} decoration-model
%add_to_maven_depmap org.apache.maven.doxia doxia-site-renderer %{version} JPP/%{parent} site-renderer
%add_to_maven_depmap org.apache.maven.doxia doxia-doc-renderer %{version} JPP/%{parent} doc-renderer

install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{parent}

install -m 644 -p doxia-decoration-model/target/doxia-decoration-model-%{version}.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{parent}/decoration-model.jar
install -m 644 -p doxia-site-renderer/target/doxia-site-renderer-%{version}.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{parent}/site-renderer.jar
install -m 644 -p doxia-doc-renderer/target/doxia-doc-renderer-%{version}.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{parent}/doc-renderer.jar

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%files
%defattr(-,root,root,-)
%{_javadir}/%{parent}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

