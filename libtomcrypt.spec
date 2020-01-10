%define debug_package %{nil}
%define major 1
%define libname %mklibname tomcrypt %{major}
%define develname %mklibname tomcrypt -d
%define _disable_lto 1
%global optflags %{optflags} -Ofast -falign-functions=32 -fno-math-errno -fno-trapping-math

%define tommath_version 1.0.1

Name:		libtomcrypt
Version:	1.18.1
Release:	2
Summary:	Comprehensive, portable cryptographic toolkit
Group:		System/Libraries
License:	Public Domain
URL:		http://www.libtom.net/LibTomCrypt/
Source0:	http://www.libtom.org/files/crypt-%{version}.tar.xz
#Patch0:		libtomcrypt-1.17-clang-4.0.patch
BuildRequires:	ghostscript
BuildRequires:	libtool
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex ghostscript-dvipdf
BuildRequires:	tommath-devel >= %{tommath_version}

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

%package -n %{libname}
Summary:	Comprehensive, portable cryptographic toolkit
Group:		System/Libraries
Obsoletes:		%{mklibname tomcrypt 0} < 1.18

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

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	tommath-devel >= %{tommath_version}
Provides:	tomcrypt-devel = %{EVRD}
Obsoletes:	%{mklibname tomcrypt -d -s} < 1.18
Provides:	%{mklibname tomcrypt -d -s} = 1.18

%description -n %{develname}
The %{develname} package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%autopatch -p1
sed -i -e 's,libtool,libtool --tag=CC,g' makefile* */makefile*

%build
%setup_compile_flags
export CFLAGS="%{optflags} -DLTM_DESC -DUSE_LTM -I%{_includedir}/tommath"
%ifarch ppc64
export CFLAGS="$CFLAGS -O0"
%endif

# (tpg) don't hardcode gcc
# sed -i -e "s#gcc#%{__cc}#g" makefile*

export CC=gcc
export CXX=g++
export PREFIX="%{_prefix}"
export INCPATH="%{_includedir}"
export LIBPATH="%{_libdir}"
export EXTRALIBS="-ltommath"

# build shared library
%make V=0 -f makefile.shared library
#make V=0 -f makefile docs
#make V=0 -f makefile.shared test

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

# Remove unneeded files
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

# Fix pkgconfig path
sed -i -e 's|^prefix=.*|prefix=%{_prefix}|g' -e 's|^libdir=.*|libdir=${prefix}/%{_lib}|g' -e 's|^includedir=.*|includedir=${prefix}/include/tomcrypt|g' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
    
%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc LICENSE
%{_includedir}/tomcrypt
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
