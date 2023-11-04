%define		vendor_version	2.3.7

Summary:	Execute scripts on IMAP mailbox changes using IDLE
Name:		goimapnotify
Version:	2.3.7
Release:	1
License:	GPL v3+
Group:		Applications/Networking
Source0:	https://gitlab.com/shackra/goimapnotify/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	4e1ac45fe419c969b48c471f25e70294
# cd goimapnotify-%{version}
# go mod vendor
# cd ..
# tar cJf goimapnotify-vendor-%{version}.tar.xz goimapnotify-%{version}/vendor
Source1:	%{name}-vendor-%{vendor_version}.tar.xz
# Source1-md5:	56594c09b58987171333fb4a6fb2e1a8
URL:		https://gitlab.com/shackra/goimapnotify
BuildRequires:	golang >= 1.15
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	systemd-units >= 38
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
Execute scripts on IMAP mailbox changes (new/deleted/updated messages)
using IDLE, golang version.

%prep
%setup -q -a1

%{__mv} %{name}-%{vendor_version}/vendor .

%{__mkdir_p} .go-cache

%build
%__go build -v -mod=vendor -o target/%{name}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{systemduserunitdir}}

cp -p target/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
sed -e 's@/usr/bin/goimapnotify@%{_bindir}/goimapnotify@'  goimapnotify@.service > $RPM_BUILD_ROOT%{systemduserunitdir}/goimapnotify@.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.md
%attr(755,root,root) %{_bindir}/%{name}
%{systemduserunitdir}/goimapnotify@.service
