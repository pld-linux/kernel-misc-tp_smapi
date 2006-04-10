# TODO:
#  - make it build
#  - wouldn't it be better to replace this spec with a kernel patch ?
##
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

#
# main package.
#
%define		_rel	0.1
Summary:	sysfs interface to access ThinkPad's SMAPI functionality
Name:		kernel-misc-tp_smapi
Version:	0.19
Release:	%{_rel}
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/tpctl/tp_smapi-%{version}.tgz
# Source0-md5:	fdb192b59e05bb826c4ca05a39b42649
URL:		http://tpctl.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.286
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%description -n kernel-misc-tp_smapi -l pl
Sterownik dla Linuksa do tp_smapi.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-misc-tp_smapi
Summary:	Linux SMP driver for tp_smapi
Summary(pl):	Sterownik dla Linuksa SMP do tp_smapi
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-misc-tp_smapi
This is driver for tp_smapi for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-misc-tp_smapi -l pl
Sterownik dla Linuksa do tp_smapi.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n tp_smapi-%{version}

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
%if %{with dist_kernel}
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} \
		TP_VER="%{version}" \
		CFLAGS="%{rpmcflags} -Iinclude/" \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CFLAGS="%{rpmcflags} -Iinclude/" \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv tp_smapi{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install tp_smapi-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/tp_smapi.ko
%if %{with smp} && %{with dist_kernel}
install tp_smapi-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/tp_smapi.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-tp_smapi
%depmod %{_kernel_ver}

%postun	-n kernel-misc-tp_smapi
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-tp_smapi
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-tp_smapi
%depmod %{_kernel_ver}smp

%files -n kernel-misc-tp_smapi
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-tp_smapi
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
