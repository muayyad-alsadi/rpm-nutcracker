%global github_name twemproxy
Name:           nutcracker
Version:        0.4.1
Release:        4%{?dist}
Summary:        twemproxy aka. nutcracker is a fast and lightweight proxy for memcached and redis protocol

License:        ASL 2.0
URL:            https://github.com/twitter/%{github_name}
Source0:        %{url}/archive/v%{version}/%{github_name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        README.rpm-dist

BuildRequires:  autoconf, automake, libtool, gcc, gcc-c++, sed, systemd

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and lightweight
proxy for memcached and redis protocol. It was built primarily to reduce the number
of connections to the caching servers on the backend. This, together with protocol
pipelining and sharding enables you to horizontally scale your distributed caching architecture.

%prep
%autosetup -n %{github_name}-%{version}
install -Dpm0644 %{S:2} ./

%build
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -re 's/-Wall /-Wformat /g'`
export CXXFLAGS=`echo $RPM_OPT_FLAGS | sed -re 's/-Wall /-Wformat /g'`
autoreconf -fvi
%configure
%make_build
echo 'DAEMON_ARGS="-a 127.0.0.1 -c /%{_sysconfdir}/%{name}/%{name}.yml"' > %{name}.rc


%install
rm -rf $RPM_BUILD_ROOT
%make_install
install -Dpm0644 %{name}.rc %{buildroot}%{_sysconfdir}/sysconfig/%{name}.rc
install -Dpm0644 %{S:1} %{buildroot}%{_unitdir}/%{name}.service

%files
%{_unitdir}/%{name}.service
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
%license LICENSE
%doc README.md NOTICE README.rpm-dist
%doc conf/*.yml
%doc notes/recommendation.md
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}.rc
%ghost %config(noreplace) %{_sysconfdir}/%{name}/%{name}.yml

%changelog
* Thu Aug 25 2016 Muayyad Alsadi <alsadi@gmail.com> - 0.4.1-4
- add systemd for _unitdir macro

* Thu Aug 25 2016 Muayyad Alsadi <alsadi@gmail.com> - 0.4.1-2
- add recommendation.md

* Tue Aug 23 2016 Muayyad Alsadi <alsadi@gmail.com> - 0.4.1-1
- initial package
