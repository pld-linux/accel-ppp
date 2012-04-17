#
# TODO:
#
# - change libdir from /usr/lib to %{_libdir}
# - check accel-ppp.tmpfiles
# - add bconds
#
Summary:	High performance PPTP/L2TP/PPPoE server
Name:		accel-ppp
Version:	1.6.1
Release:	0.1
License:	GPL v2+
Group:		Networking
URL:		http://sourceforge.net/projects/accel-ppp/
Source0:	http://downloads.sourceforge.net/accel-ppp/%{name}-%{version}.tar.bz2
# Source0-md5:	8985ab9f743b952396f6dc53d6fd56a8
Source1:	%{name}.tmpfiles
Patch0:		%{name}-cmake.patch
BuildRequires:	cmake >= 2.6
BuildRequires:	libnl1-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	net-snmp-devel >= 5.0

%description
The ACCEL-PPP is completly new implementation of PPTP/PPPoE/L2TP
which was written from scratch. Userspace daemon has its own PPP
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
%patch0 -p1

%build
install -d build
cd build
%{cmake} \
	  -DSHAPER=TRUE \
	  -DRADIUS=TRUE \
          -DNETSNMP=TRUE \
	  -DLOG_PGSQL=FALSE \
	  ../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
	  DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} $RPM_BUILD_ROOT%{systemdtmpfilesdir}
install -d $RPM_BUILD_ROOT/var/{log/accel-ppp,run/accel-ppp}
install %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
echo "0" > $RPM_BUILD_ROOT/var/run/accel-ppp/seq


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README
%{_sysconfdir}/accel-ppp.conf.dist
%attr(755,root,root) %{_sbindir}/accel-pppd
/usr/lib/accel-ppp
%dir /var/run/%{name}
/var/run/%{name}/seq
%{systemdtmpfilesdir}/%{name}.conf
%{_datadir}/accel-ppp/
%{_mandir}/man5/accel-ppp.conf.5*
