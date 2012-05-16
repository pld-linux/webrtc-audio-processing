# NOTE:
# f.d.o source is meant to be a more Linux packaging friendly copy of the
# AudioProcessing module from the WebRTC[1] project. The ideal case is that we
# make no changes to the code to make tracking upstream code easy.
# [1] http://code.google.com/p/webrtc/
Summary:	WebRTC Audio Processing library
Name:		webrtc-audio-processing
Version:	0.1
Release:	1
License:	BSD
Group:		Libraries
URL:		http://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing/
Source0:	http://freedesktop.org/software/pulseaudio/webrtc-audio-processing/%{name}-%{version}.tar.xz
# Source0-md5:	da25bb27812c8404060d4cc0dc712f04
Patch0:		link.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebRTC is an open source project that enables web browsers with
Real-Time Communications (RTC) capabilities via simple Javascript
APIs. The WebRTC components have been optimized to best serve this
purpose. WebRTC implements the W3C's proposal for video conferencing
on the web.

%package devel
Summary:	WebRTC Audio Processing library and header files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This contains the libraries and header files needed to develop
programs which make use of webrtc-audio-processing.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS PATENTS README
%attr(755,root,root) %{_libdir}/libwebrtc_audio_processing.so.*.*.*
%{_libdir}/libwebrtc_audio_processing.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/webrtc_audio_processing
%{_libdir}/libwebrtc_audio_processing.so
%{_pkgconfigdir}/webrtc-audio-processing.pc
