#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%define		_name	tp_smapi
%define		_rel	0.1
Summary:	sysfs interface to access ThinkPad's SMAPI functionality
Summary(pl.UTF-8):	Interfejs sysfs do funkcjonalności SMAPI ThinkPadów
Name:		kernel%{_alt_kernel}-misc-tp_smapi
Version:	0.30
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/tpctl/%{_name}-%{version}.tgz
# Source0-md5:	06e15345276d8389950bd89c8bd96717
URL:		http://tpctl.sourceforge.net/
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
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

%package -n kernel%{_alt_kernel}-smp-misc-tp_smapi
Summary:	Linux SMP driver for tp_smapi
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do tp_smapi
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Requires(post,postun):  /sbin/depmod

%description -n kernel%{_alt_kernel}-smp-misc-tp_smapi
sysfs interface to access ThinkPad's SMAPI functionality.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-misc-tp_smapi -l pl.UTF-8
Interfejs sysfs do funkcjonalności SMAPI ThinkPadów.

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -n tp_smapi-%{version}
echo "obj-m := thinkpad_ec.o tp_smapi.o hdaps.o" > Makefile
echo > dmi_ec_oem_string.h

%build
%define _CFLAGS CFLAGS="%{rpmcflags} -I$PWD/include -I$PWD/o/include/asm/mach-default"
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

%post	-n kernel%{_alt_kernel}-smp-misc-tp_smapi
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-misc-tp_smapi
%depmod %{_kernel_ver}smp

%files -n kernel%{_alt_kernel}-misc-tp_smapi
%defattr(644,root,root,755)
%doc CHANGES README
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-tp_smapi
%defattr(644,root,root,755)
%doc CHANGES README
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
