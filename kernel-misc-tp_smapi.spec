#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%define		_name	tp_smapi
%define		_rel	0.1
Summary:	sysfs interface to access ThinkPad's SMAPI functionality
Summary(pl):	Interfejs sysfs do funkcjonalno¶ci SMAPI ThinkPadów
Name:		kernel%{_alt_kernel}-misc-tp_smapi
Version:	0.30
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Applications
Source0:	http://dl.sourceforge.net/tpctl/%{_name}-%{version}.tgz
# Source0-md5:	06e15345276d8389950bd89c8bd96717
URL:		http://tpctl.sourceforge.net/
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRequires:	rpmbuild(macros) >= 1.286
Requires(post,postun):  /sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sysfs interface to access ThinkPad's SMAPI functionality.

This package contains Linux kernel module.

%description -l pl
Interfejs sysfs do funkcjonalno¶ci SMAPI ThinkPadów.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel%{_alt_kernel}-smp-misc-tp_smapi
Summary:	Linux SMP driver for tp_smapi
Summary(pl):	Sterownik dla Linuksa SMP do tp_smapi
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

%description -n kernel%{_alt_kernel}-smp-misc-tp_smapi -l pl
Interfejs sysfs do funkcjonalno¶ci SMAPI ThinkPadów.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n tp_smapi-%{version}
echo "obj-m := thinkpad_ec.o tp_smapi.o hdaps.o" > Makefile
echo > dmi_ec_oem_string.h

%build
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} o/include/asm
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CFLAGS="%{rpmcflags} -I$PWD/include -I$PWD/o/include/asm/mach-default" \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv tp_smapi{,-$cfg}.ko
	mv thinkpad_ec{,-$cfg}.ko
	mv hdaps{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install tp_smapi-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/tp_smapi.ko
install thinkpad_ec-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/thinkpad_ec.ko
install hdaps-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/hdaps.ko
%if %{with smp} && %{with dist_kernel}
install tp_smapi-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/tp_smapi.ko
install thinkpad_ec-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/thinkpad_ec.ko
install hdpaps-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/hdaps.ko
%endif

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
