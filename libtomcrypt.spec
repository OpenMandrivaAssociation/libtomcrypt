%define libname %mklibname tomcrypt 0
%define libname_devel %mklibname tomcrypt -d
%define libname_static_devel %mklibname tomcrypt -d -s

%define tommath_version 0.41

Name:           libtomcrypt
Version:        1.17
Release:        4
Summary:        Comprehensive, portable cryptographic toolkit
Group:          System/Libraries
License:        Public Domain
URL:            http://www.libtom.org/?page=features&newsitems=5&whatfile=crypt
Source0:        http://www.libtom.org/files/crypt-%{version}.tar.bz2
Patch0:         libtomcrypt-makefile.patch
BuildRequires:  ghostscript
BuildRequires:  libtool
BuildRequires:  tetex-dvips
BuildRequires:  tetex-latex ghostscript-dvipdf
BuildRequires:  tommath-devel >= %{tommath_version}

%description
A comprehensive, modular and portable cryptographic toolkit that
provides developers with a vast array of well known published block
ciphers, one-way hash functions, chaining modes, pseudo-random number
generators, public key cryptography and a plethora of other routines.

Designed from the ground up to be very simple to use. It has a modular
and standard API that allows new ciphers, hashes and PRNGs to be added
or removed without change to the overall end application. It features
easy to use functions and a complete user manual which has many source
snippet examples.

%package -n	%{libname}
Summary:        Comprehensive, portable cryptographic toolkit
Group:          System/Libraries

%description -n %{libname}
A comprehensive, modular and portable cryptographic toolkit that
provides developers with a vast array of well known published block
ciphers, one-way hash functions, chaining modes, pseudo-random number
generators, public key cryptography and a plethora of other routines.

Designed from the ground up to be very simple to use. It has a modular
and standard API that allows new ciphers, hashes and PRNGs to be added
or removed without change to the overall end application. It features
easy to use functions and a complete user manual which has many source
snippet examples.

%package -n	%{libname_devel}
Summary:        Development files for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       tommath-devel >= %{tommath_version}
Provides:       tomcrypt-devel = %{version}-%{release}

%description -n %{libname_devel}
The %{libname_devel} package contains libraries and header files for
developing applications that use %{name}.

%package -n	%{libname_static_devel}
Summary:        Static development files for %{name}
Group:          Development/C
Requires:       tomcrypt-devel = %{version}-%{release}
Requires:       tommath-static-devel >= %{tommath_version}
Provides:       tomcrypt-static-devel = %{version}-%{release}

%description -n %{libname_static_devel}
The %{libname_static_devel} package contains static libraries for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .makefile~

%build
export CFLAGS="%{optflags} -DLTM_DESC -DUSE_LTM -I%{_includedir}/tommath"
%ifarch ppc64
export CFLAGS="$CFLAGS -O0"
%endif
%make LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile docs
%make LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile.shared

# making the test fucks something up somewhere...
%if 0
%check
export CFLAGS="%{optflags} -DLTM_DESC -DUSE_LTM -I%{_includedir}/tommath"
%make LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile test
./test
%endif

%install
# There is no configure script that ships with libtomcrypt but it does
# have understand DESTDIR and its installs via that and the
# INSTALL_USER and INSTALL_GROUP environment variables.
export INSTALL_USER=$(id -un)
export INSTALL_GROUP=$(id -gn)
export CFLAGS="%{optflags} -DLTM_DESC -DUSE_LTM"

%makeinstall_std INCPATH=%{_includedir}/tomcrypt LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile.shared

%files -n %{libname}
%doc LICENSE
%{_libdir}/*.so.*

%files -n %{libname_devel}
%doc doc/crypt.pdf
%{_includedir}/tomcrypt
%{_libdir}/*.so

%files -n %{libname_static_devel}
%{_libdir}/*.a
