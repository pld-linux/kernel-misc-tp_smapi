#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define		_name	tp_smapi
%define		_rel	0.1
Summary:	sysfs interface to access ThinkPad's SMAPI functionality
Summary(pl.UTF-8):	Interfejs sysfs do funkcjonalności SMAPI ThinkPadów
Name:		kernel%{_alt_kernel}-misc-tp_smapi
Version:	0.32
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/tpctl/%{_name}-%{version}.tgz
# Source0-md5:	4f721dc1c1d16494ddda7ac6c6e9a92f
URL:		http://tpctl.sourceforge.net/
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRequires:	rpmbuild(macros) >= 1.348
Requires(post,postun):  /sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sysfs interface to access ThinkPad's SMAPI functionality.

This package contains Linux kernel module.

%description -l pl.UTF-8
Interfejs sysfs do funkcjonalności SMAPI ThinkPadów.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n tp_smapi-%{version}
echo "obj-m := thinkpad_ec.o tp_smapi.o hdaps.o" > Makefile
echo > dmi_ec_oem_string.h

%build
%define _CFLAGS CFLAGS="%{rpmcflags} -I$PWD/include -I$PWD/o/include/asm/mach-default -I$PWD/o/include2/asm/mach-default"
%build_kernel_modules -m tp_smapi,thinkpad_ec,hdaps %{_CFLAGS}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m tp_smapi,thinkpad_ec,hdaps -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-misc-tp_smapi
%defattr(644,root,root,755)
%doc CHANGES README
/lib/modules/%{_kernel_ver}/misc/*.ko*
