# NOTE:
# f.d.o source is meant to be a more Linux packaging friendly copy of the
# AudioProcessing module from the WebRTC[1] project. The ideal case is that we
# make no changes to the code to make tracking upstream code easy.
# [1] http://code.google.com/p/webrtc/
#
# Conditional build:
%bcond_without	neon		# without ARM NEON instructions

%ifnarch armv7l armv7hl armv7hnl armv8l armv8hl armv8hnl armv8hcnl aarch64
%undefine	with_neon
%endif

Summary:	WebRTC Audio Processing library
Summary(pl.UTF-8):	Biblioteka WebRTC Audio Processing
Name:		webrtc-audio-processing
# keep 0.x here; for versions >= 1 (parallel installable with 0.x) see webrtc-audio-processing1.spec
Version:	0.3.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://freedesktop.org/software/pulseaudio/webrtc-audio-processing/%{name}-%{version}.tar.xz
# Source0-md5:	6e10724ca34bcbc715a4c208273acb0c
URL:		https://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebRTC is an open source project that enables web browsers with
Real-Time Communications (RTC) capabilities via simple Javascript
APIs. The WebRTC components have been optimized to best serve this
purpose. WebRTC implements the W3C's proposal for video conferencing
on the web.

%description -l pl.UTF-8
WebRTC to projekt o otwartych źródłach dodający obsługę komunikacji
w czasie rzeczywistym (RTC - Real-Time Communications) poprzez proste
API JavaScriptu. Komponenty WebRTC zostały zoptymalizowane, aby jak
najlepiej sprawdzały się w tym zastosowaniu. WebRTC implementuje
propozycje W3C do wideokonferencji w sieci.

%package devel
Summary:	Header files for WebRTC Audio Processing library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki WebRTC Audio Processing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
This package contains the header files needed to develop programs
which make use of WebRTC Audio Processing library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę WebRTC Audio Processing.

%package static
Summary:	Static WebRTC Audio Processing library
Summary(pl.UTF-8):	Biblioteka statyczna WebRTC Audio Processing
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static WebRTC Audio Processing library.

%description static -l pl.UTF-8
Biblioteka statyczna WebRTC Audio Processing.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_neon:--disable-neon} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md webrtc/PATENTS
%attr(755,root,root) %{_libdir}/libwebrtc_audio_processing.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwebrtc_audio_processing.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwebrtc_audio_processing.so
%{_includedir}/webrtc_audio_processing
%{_pkgconfigdir}/webrtc-audio-processing.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwebrtc_audio_processing.a
