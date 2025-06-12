Name:           osmo-msc
Version:        1.13.0
Release:        1.dcbw%{?dist}
Summary:        3GPP MSC (Mobile Switching Centre)
License:        AGPL-3.0-or-later AND GPL-2.0-or-later

URL:            https://github.com/osmocom/osmo-msc

BuildRequires:  git gcc autoconf automake libtool doxygen systemd-devel
BuildRequires:  libdbi-devel sqlite-devel
BuildRequires:  libosmocore-devel >= 1.10.0
BuildRequires:  libosmo-netif-devel >= 1.6.0
BuildRequires:  libosmo-abis-devel >= 2.0.0
BuildRequires:  libasn1c-devel >= 0.9.38
BuildRequires:  libsmpp34-devel >= 1.14.4
BuildRequires:  libosmo-sigtran-devel >= 2.1.1
BuildRequires:  osmo-mgw-devel >= 1.14.0
BuildRequires:  osmo-hlr-devel >= 1.9.1
BuildRequires:  osmo-iuh-devel >= 1.7.0

Source0: %{name}-%{version}.tar.bz2

Requires: osmo-usergroup


%description
OsmoMSC is an implementation of the 3GPP MSC
(Mobile Switching Centre) network element.

%global _lto_cflags %{nil}

%prep
%autosetup -p1


%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fiv
%configure --enable-shared \
           --disable-static \
           --enable-smpp \
           --enable-iu \
           --with-systemdsystemunitdir=%{_unitdir}

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
make check

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

%ldconfig_scriptlets

%files
%doc %{_docdir}/%{name}
%doc README.md
%doc doc contrib
%license COPYING
%{_bindir}/*
%{_unitdir}/%{name}.service
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/osmocom/%{name}.cfg


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.13.0
- Update to 1.13.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- git update releases
