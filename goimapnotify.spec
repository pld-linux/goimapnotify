Summary:	Execute scripts on IMAP mailbox changes using IDLE
Name:		goimapnotify
Version:	2.6.0
Release:	1
License:	GPL v3+
Group:		Applications/Networking
Source0:	https://gitlab.com/shackra/goimapnotify/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	f2b37209e29c9fb6cb90df74b26311b2
URL:		https://gitlab.com/shackra/goimapnotify
BuildRequires:	golang >= 1.23
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	systemd-units >= 38
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	_debugsource_packages

%description
Execute scripts on IMAP mailbox changes (new/deleted/updated messages)
using IDLE, golang version.

%prep
%setup -q

%{__mkdir_p} .go-cache

%build
%__go build -v -mod=vendor -o target/%{name} ./cmd/goimapnotify

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{systemduserunitdir}}

cp -p target/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
sed -e 's@/usr/bin/goimapnotify@%{_bindir}/goimapnotify@'  goimapnotify@.service > $RPM_BUILD_ROOT%{systemduserunitdir}/goimapnotify@.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/%{name}
%{systemduserunitdir}/goimapnotify@.service
