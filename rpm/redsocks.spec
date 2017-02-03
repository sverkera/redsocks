Name:		redsocks
Version:	0.5
Release:	1%{?dist}
Summary:	Transparent redirector of any TCP connection to proxy

Group:		System Environment/Daemons
License:	ASL 2.0
URL:		http://darkk.net.ru/redsocks
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	libevent2-devel
Requires:	libevent2

%description
Redirect any TCP connection to a SOCKS or HTTPS proxy server
 Redsocks is a daemon running on the local system, that will transparently
 tunnel any TCP connection via a remote SOCKS4, SOCKS5 or HTTP proxy server. It
 uses the system firewall's redirection facility to intercept TCP connections,
 thus the redirection is system-wide, with fine-grained control, and does 
 not depend on LD_PRELOAD libraries.

 Redsocks supports tunneling TCP connections and UDP packets. It has
 authentication support for both, SOCKS and HTTP proxies.

 Also included is a small DNS server returning answers with the "truncated" flag
 set for any UDP query, forcing the resolver to use TCP.

%prep
%setup -q -n %{name}

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT/%{_sbindir}
install -p -m 0755 redsocks $RPM_BUILD_ROOT/%{_sbindir}

install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
install -p -m 0644 debian/redsocks.conf $RPM_BUILD_ROOT/%{_sysconfdir}/
install -p -m 0644 rpm/redsocks.default $RPM_BUILD_ROOT/%{_sysconfdir}/default/redsocks
install -p -m 0755 rpm/redsocks.init $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/redsocks

install -d -m 0755 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 0644 debian/redsocks.8 $RPM_BUILD_ROOT/%{_mandir}/man8/

install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group redsocks >/dev/null || groupadd --system redsocks
getent passwd redsocks >/dev/null || adduser --system --shell /sbin/nologin --home-dir /var/run/redsocks --no-create-home -g redsocks redsocks

%post
service redsocks status >/dev/null 2>&1
if [ $? -eq 0 ]; then
	service redsocks restart
else
	service redsocks start
fi
chkconfig redsocks on

%preun
if [ "$1" -eq "0" ]; then
	service redsocks status >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		service redsocks stop
	fi
	chkconfig redsocks off
fi

%postun
#if [ "$1" -eq "0" ]; then
#  deluser --system redsocks || true
#  delgroup --system redsocks || true
#fi

%files
%defattr(-,root,root,-)
%doc debian/changelog debian/copyright 
%{_sbindir}/redsocks
%{_mandir}/man8/redsocks.8.gz
%{_sysconfdir}/init.d/redsocks 
%config(noreplace) %{_sysconfdir}/redsocks.conf
%config(noreplace) %{_sysconfdir}/default/redsocks

%ghost %attr(755,redsocks,redsocks) %{_localstatedir}/run/%{name}

%changelog
