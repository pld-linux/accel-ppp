# TODO:
# - check accel-ppp.tmpfiles
# - logrotate archivedir
# - add bconds
# - initscript: remove duplicate force-reload, remove one depending whether it supports reload or not
#
Summary:	High performance PPTP/L2TP/PPPoE server
Name:		accel-ppp
Version:	1.8.0
Release:	1
License:	GPL v2+
Group:		Networking
URL:		http://sourceforge.net/projects/accel-ppp
Source0:	http://downloads.sourceforge.net/accel-ppp/%{name}-%{version}.tar.bz2
# Source0-md5:	bc3a02b24fb9f304f7417a9011a494d6
Source1:	%{name}.tmpfiles
Source2:	%{name}.init
Source3:	%{name}.logrotate
BuildRequires:	cmake >= 2.6
BuildRequires:	libnl1-devel
BuildRequires:	net-snmp-devel >= 5.0
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ACCEL-PPP is completly new implementation of PPTP/PPPoE/L2TP which
was written from scratch. Userspace daemon has its own PPP
implementation, so it does not uses pppd and one process
(multi-threaded) manages all connections. ACCEL-PPP uses only
kernel-mode implementations of pptp/l2tp/pppoe.

Features:
- PPTP server
- PPPoE server
- L2TPv2 server
- Radius CoA/DM(PoD)
- Built-in shaper (tbf)
- Command line interface (telnet)
- SNMP
- IPv6 (including builtin Neighbor Discovery and DHCPv6)

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DSHAPER=TRUE \
	-DRADIUS=TRUE \
	-DNETSNMP=TRUE \
	-DBUILD_INSTALL_PREFIX=$RPM_BUILD_ROOT \
	-DLOG_PGSQL=FALSE \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
	  DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,logrotate.d,rc.d/init.d} $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/accel-pppd
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install -d $RPM_BUILD_ROOT/var/log/accel-ppp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-ppp.conf.dist
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(755,root,root) %{_bindir}/accel-cmd
%attr(755,root,root) %{_sbindir}/accel-pppd
%attr(755,root,root) %{_libdir}/accel-ppp
%attr(754,root,root) /etc/rc.d/init.d/accel-pppd
%dir /var/run/%{name}
%{systemdtmpfilesdir}/%{name}.conf
%{_datadir}/%{name}
%{_mandir}/man1/accel-cmd.*
%{_mandir}/man5/accel-ppp.conf.5*
%dir /var/log/accel-ppp
