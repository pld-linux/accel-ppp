# TODO:
# - check accel-ppp.tmpfiles
# - logrotate archivedir
# - add bconds
# - initscript: remove duplicate force-reload, remove one depending whether it supports reload or not
#
Summary:	High performance PPTP/PPPoE/L2TP/SSTP server
Summary(pl.UTF-8):	Wydajny serwer PPTP/PPPoE/L2TP/SSTP
Name:		accel-ppp
Version:	1.13.0
Release:	1
License:	GPL v2+
Group:		Networking
#Source0Download: https://github.com/accel-ppp/accel-ppp/releases
Source0:	https://github.com/accel-ppp/accel-ppp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	239f03b9e3b81d6a156950dd3e983b28
Source1:	%{name}.tmpfiles
Source2:	%{name}.init
Source3:	%{name}.logrotate
Source4:	%{name}.sysconfig
Patch0:		%{name}-snmp.patch
URL:		https://accel-ppp.org/
BuildRequires:	cmake >= 2.6
BuildRequires:	net-snmp-devel >= 5.0
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ACCEL-PPP is completely new implementation of PPTP/PPPoE/L2TP/SSTP
which was written from scratch. Userspace daemon has its own PPP
implementation, so it does not uses pppd and one process
(multi-threaded) manages all connections. ACCEL-PPP uses only
kernel-mode implementations of pptp/l2tp/pppoe.

Features:
- modular architecture with multi-threaded I/O core
- PPTP support
- PPPoE support (including TR-101 extension)
- L2TPv2 support (without IPsec)
- Radius authentication/accounting with CoA/DM extension
- supported authentication: PAP, CHAP (md5), MS CHAP extensions
- MPPE support
- Built-in tbf/htb shaper
- Command line interface via telnet
- SNMP support
- SSTP support

%description -l pl.UTF-8
ACCEL-PPP to zupełnie nowa implementacja PPTP/PPPoE/L2TP/SSTP,
napisana od zera. Demon przestrzeni użytkownika wykorzystuje własną
implementację PPP, więc nie używa pppd, a jeden proces (wielowątkowy)
zarządza wszystkimi połączeniami. ACCEL-PPP wykorzystuje tylko
implementacje pptp/l2tp/pppoe po stronie jądra.

Możliwości:
- modularna architektura z wielowątkową obsługą wejścia/wyjścia
- obsługa PPTP
- obsługa PPPoE (wraz z rozszerzeniem TR-101)
- obsługa L2TPv2 (bez IPsec)
- uwierzetelnianie/rozliczanie Radius z rozszerzeniem CoA/DM
- obsługiwane uwierzytelnienia: PAP, CHAP (md5), rozszerzenia MS CHAP
- obsługa MPPE
- wbudowane ograniczanie urchu tbf/htb
- interfejs linii poleceń przez telnet
- obsługa SNMP
- obsługa SSTP

%prep
%setup -q
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
	-DSHAPER=ON \
	-DRADIUS=ON \
	-DNETSNMP=ON \
	-DLOG_PGSQL=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
	  DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,logrotate.d,rc.d/init.d} $RPM_BUILD_ROOT%{systemdtmpfilesdir} $RPM_BUILD_ROOT/var/log/accel-ppp
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/accel-pppd
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/accel-ppp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-ppp.conf.dist
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/accel-ppp
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/accel-ppp
%attr(755,root,root) %{_bindir}/accel-cmd
%attr(755,root,root) %{_sbindir}/accel-pppd
%attr(755,root,root) %{_libdir}/accel-ppp
%attr(754,root,root) /etc/rc.d/init.d/accel-pppd
%{systemdtmpfilesdir}/accel-ppp.conf
%{_datadir}/%{name}
%{_mandir}/man1/accel-cmd.1*
%{_mandir}/man5/accel-ppp.conf.5*
%dir /var/log/accel-ppp
